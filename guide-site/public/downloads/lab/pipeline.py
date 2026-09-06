"""Offline teaching lab: SQLite jobs, leases, scoped access, and an outbox.

No network, model, credentials, or production authentication. `tenant` is a
trusted principal supplied by the caller/test harness, not an auth mechanism.
Only synthetic fixture data should be used. This intentionally persists data.
"""
import argparse
import hashlib
import json
import secrets
import sqlite3
import tempfile
import time
import uuid
from pathlib import Path


class Conflict(ValueError):
    pass


class LeaseError(RuntimeError):
    pass


class AttemptLimit(RuntimeError):
    pass


class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(str(path), timeout=5, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
          CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY, tenant TEXT NOT NULL, venue TEXT NOT NULL,
            version INTEGER NOT NULL DEFAULT 1, enabled INTEGER NOT NULL DEFAULT 1
          );
          CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY, tenant TEXT NOT NULL, op_key TEXT NOT NULL,
            fingerprint TEXT NOT NULL, event_id TEXT NOT NULL REFERENCES events(id),
            source_version INTEGER NOT NULL, state TEXT NOT NULL DEFAULT 'queued',
            attempts INTEGER NOT NULL DEFAULT 0, token TEXT, lease_until REAL,
            UNIQUE(tenant, op_key)
          );
          CREATE TABLE IF NOT EXISTS briefs (
            job_id TEXT PRIMARY KEY REFERENCES jobs(id), content TEXT NOT NULL
          );
          CREATE TABLE IF NOT EXISTS outbox (
            id TEXT PRIMARY KEY, job_id TEXT NOT NULL UNIQUE REFERENCES jobs(id),
            event_type TEXT NOT NULL, delivered INTEGER NOT NULL DEFAULT 0
          );
        """)
        self.db.executemany(
            "INSERT OR IGNORE INTO events(id,tenant,venue) VALUES(?,?,?)",
            [('event_a', 'org_a', 'Hall A'), ('event_a2', 'org_a', 'Hall C'),
             ('event_b', 'org_b', 'Hall B')])

    def close(self):
        self.db.close()

    def _begin(self):
        self.db.execute('BEGIN IMMEDIATE')

    def _rollback(self):
        if self.db.in_transaction:
            self.db.execute('ROLLBACK')

    def submit(self, tenant, op_key, event_id):
        if not isinstance(op_key, str) or not 1 <= len(op_key) <= 128:
            raise ValueError('Operation key must contain 1–128 characters')
        fingerprint = hashlib.sha256(json.dumps(
            {'event_id': event_id}, sort_keys=True).encode()).hexdigest()
        self._begin()
        try:
            event = self.db.execute(
                'SELECT * FROM events WHERE id=? AND tenant=? AND enabled=1',
                (event_id, tenant)).fetchone()
            if event is None:
                raise PermissionError('Event unavailable in this scope')
            existing = self.db.execute(
                'SELECT * FROM jobs WHERE tenant=? AND op_key=?',
                (tenant, op_key)).fetchone()
            if existing:
                if existing['fingerprint'] != fingerprint:
                    raise Conflict('Operation key was reused with different input')
                job_id = existing['id']
            else:
                job_id = str(uuid.uuid4())
                self.db.execute('''INSERT INTO jobs
                    (id,tenant,op_key,fingerprint,event_id,source_version)
                    VALUES(?,?,?,?,?,?)''',
                    (job_id, tenant, op_key, fingerprint, event_id, event['version']))
            self.db.execute('COMMIT')
            return job_id
        except Exception:
            self._rollback()
            raise

    def get_job(self, tenant, job_id):
        row = self.db.execute('SELECT * FROM jobs WHERE id=? AND tenant=?',
                              (job_id, tenant)).fetchone()
        if row is None:
            raise PermissionError('Job unavailable in this scope')
        # Worker lease tokens are internal and are not part of the user view.
        return {k: row[k] for k in ('id', 'event_id', 'state', 'attempts')}

    def claim(self, job_id, now=None, lease_seconds=30, max_attempts=3):
        """Internal worker operation; claim transactions do no external work."""
        now = time.time() if now is None else now
        if lease_seconds <= 0 or max_attempts < 1:
            raise ValueError('Positive lease and attempt limit required')
        self._begin()
        try:
            row = self.db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
            if row is None:
                raise KeyError('Unknown job')
            if row['state'] in ('succeeded', 'failed') or (
                    row['state'] == 'running' and row['lease_until'] > now):
                self.db.execute('COMMIT')
                return None
            if row['attempts'] >= max_attempts:
                self.db.execute("UPDATE jobs SET state='failed' WHERE id=?", (job_id,))
                self.db.execute('COMMIT')
                raise AttemptLimit('Attempt limit reached; manual review required')
            token = secrets.token_hex(16)
            self.db.execute('''UPDATE jobs SET state='running',token=?,lease_until=?,
                attempts=attempts+1 WHERE id=?''', (token, now+lease_seconds, job_id))
            self.db.execute('COMMIT')
            return token
        except Exception:
            self._rollback()
            raise

    def fake_model(self, job_id):
        """Purely deterministic fixture adapter: no actual model call."""
        row = self.db.execute('''SELECT e.* FROM events e JOIN jobs j
            ON j.event_id=e.id AND j.tenant=e.tenant WHERE j.id=? AND e.enabled=1''',
            (job_id,)).fetchone()
        if row is None:
            raise PermissionError('Source no longer available')
        return {'event_id': row['id'], 'venue': row['venue'],
                'source_id': row['id'], 'source_version': row['version'], 'unresolved': []}

    def complete(self, job_id, token, brief, now=None):
        now = time.time() if now is None else now
        self._begin()
        try:
            job = self.db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
            if job is None:
                raise KeyError('Unknown job')
            if job['state'] == 'succeeded' and job['token'] == token:
                saved = self.db.execute('SELECT content FROM briefs WHERE job_id=?',
                                        (job_id,)).fetchone()['content']
                self.db.execute('COMMIT')
                return json.loads(saved)
            if (job['state'] != 'running' or job['token'] != token or
                    job['lease_until'] <= now):
                raise LeaseError('Expired or stale worker cannot finalize')
            event = self.db.execute('''SELECT * FROM events
                WHERE id=? AND tenant=? AND enabled=1''',
                (job['event_id'], job['tenant'])).fetchone()
            if event is None:
                raise PermissionError('Source no longer available')
            if event['version'] != job['source_version']:
                raise Conflict('Source changed; submit a new operation after review')
            expected = {'event_id': event['id'], 'venue': event['venue'],
                        'source_id': event['id'], 'source_version': event['version'],
                        'unresolved': []}
            if (not isinstance(brief, dict) or
                    type(brief.get('source_version')) is not int or brief != expected):
                raise ValueError('Brief does not match the approved synthetic facts')
            self.db.execute('INSERT INTO briefs(job_id,content) VALUES(?,?)',
                            (job_id, json.dumps(brief, sort_keys=True)))
            self.db.execute('INSERT INTO outbox(id,job_id,event_type) VALUES(?,?,?)',
                            ('brief-ready:'+job_id, job_id, 'brief_ready'))
            self.db.execute("UPDATE jobs SET state='succeeded' WHERE id=?", (job_id,))
            self.db.execute('COMMIT')
            return brief
        except Exception:
            self._rollback()
            raise

    def counts(self):
        return {name: self.db.execute('SELECT COUNT(*) FROM '+name).fetchone()[0]
                for name in ('jobs', 'briefs', 'outbox')}


def demo(path):
    store = Store(path)
    try:
        job = store.submit('org_a', 'demo-operation-1', 'event_a')
        token = store.claim(job)
        if token:
            result = store.complete(job, token, store.fake_model(job))
        else:
            result = {'message': 'Existing operation; no duplicate execution.'}
        print(json.dumps({'mode': 'offline simulation', 'result': result,
                          'counts': store.counts()}, indent=2))
    finally:
        store.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', help='Optional SQLite path to preserve synthetic demo state')
    args = parser.parse_args()
    if args.db:
        demo(Path(args.db))
    else:
        with tempfile.TemporaryDirectory(prefix='agentic-eng-lab-') as directory:
            demo(Path(directory)/'demo.sqlite')
