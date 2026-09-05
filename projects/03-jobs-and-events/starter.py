import sqlite3

class Jobs:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
        CREATE TABLE jobs(id TEXT PRIMARY KEY, op_key TEXT UNIQUE, payload TEXT,
          state TEXT DEFAULT 'queued', attempts INTEGER DEFAULT 0, token TEXT, lease_until REAL);
        CREATE TABLE results(job_id TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE outbox(job_id TEXT PRIMARY KEY, event_type TEXT);
        """)

    def submit(self, op_key: str, payload: str) -> str:
        """TODO: same key+payload returns same job; changed payload conflicts."""
        raise NotImplementedError

    def claim(self, job_id: str, now: float, lease_seconds=10, max_attempts=3):
        """TODO: return a fresh fencing token or None when unavailable."""
        raise NotImplementedError

    def complete(self, job_id: str, token: str, value: str, now: float):
        """TODO: atomically fence, store one result, and add one outbox row."""
        raise NotImplementedError
