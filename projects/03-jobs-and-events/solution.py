import sqlite3
import uuid
import secrets

class Jobs:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, op_key TEXT UNIQUE, payload TEXT,
          state TEXT DEFAULT 'queued', attempts INTEGER DEFAULT 0, token TEXT, lease_until REAL);
        CREATE TABLE IF NOT EXISTS results(job_id TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS outbox(job_id TEXT PRIMARY KEY, event_type TEXT);
        """)

    def submit(self, op_key: str, payload: str) -> str:
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT * FROM jobs WHERE op_key=?", (op_key,)).fetchone()
            if row:
                if row["payload"] != payload: raise ValueError("operation key reused with different intent")
                job_id = row["id"]
            else:
                job_id = str(uuid.uuid4())
                self.db.execute("INSERT INTO jobs(id,op_key,payload) VALUES(?,?,?)", (job_id, op_key, payload))
            self.db.execute("COMMIT")
            return job_id
        except Exception:
            self.db.execute("ROLLBACK"); raise

    def claim(self, job_id: str, now: float, lease_seconds=10, max_attempts=3):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
            if not row: raise KeyError(job_id)
            if row["state"] in {"succeeded", "failed"} or (row["state"] == "running" and row["lease_until"] > now):
                self.db.execute("COMMIT"); return None
            if row["attempts"] >= max_attempts:
                self.db.execute("UPDATE jobs SET state='failed' WHERE id=?", (job_id,))
                self.db.execute("COMMIT"); raise RuntimeError("attempt limit")
            token = secrets.token_hex(12)
            self.db.execute("UPDATE jobs SET state='running',attempts=attempts+1,token=?,lease_until=? WHERE id=?", (token, now+lease_seconds, job_id))
            self.db.execute("COMMIT"); return token
        except Exception:
            if self.db.in_transaction: self.db.execute("ROLLBACK")
            raise

    def complete(self, job_id: str, token: str, value: str, now: float):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
            if row and row["state"] == "succeeded" and row["token"] == token:
                existing = self.db.execute("SELECT value FROM results WHERE job_id=?", (job_id,)).fetchone()[0]
                self.db.execute("COMMIT"); return existing
            if not row or row["state"] != "running" or row["token"] != token or row["lease_until"] <= now:
                raise RuntimeError("stale worker")
            self.db.execute("INSERT INTO results VALUES(?,?)", (job_id, value))
            self.db.execute("INSERT INTO outbox VALUES(?,?)", (job_id, "job_succeeded"))
            self.db.execute("UPDATE jobs SET state='succeeded' WHERE id=?", (job_id,))
            self.db.execute("COMMIT"); return value
        except Exception:
            if self.db.in_transaction: self.db.execute("ROLLBACK")
            raise

if __name__ == "__main__":
    jobs=Jobs(); job=jobs.submit("demo-1", "build brief"); token=jobs.claim(job, 0)
    print(jobs.complete(job, token, "brief ready", 1))
