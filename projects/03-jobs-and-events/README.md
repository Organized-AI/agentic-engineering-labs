# 03 — Leased Job Runner

Use SQLite to implement idempotent submission, leases, fencing tokens, an
attempt limit, atomic completion, and a transactional outbox record.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Challenge

Complete `submit`, `claim`, and `complete` in `starter.py`. Keep slow work
outside transactions. A stale worker must never finalize after a later claim.

## Extension

Write an outbox relay and a deduplicating consumer. Simulate a crash after
publication but before the outbox row is marked delivered.
