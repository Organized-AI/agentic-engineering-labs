# 09 — Synthetic Canary Retention Audit

[Read the Data Retention chapter →](https://guide.organizedai.vip/agentic-eng/chapters/data-retention/)

Pass a unique synthetic marker through success and failure paths, inspect known
stores, expire data, and report what remains. This is a test of known surfaces,
not proof that no unknown copy exists.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Challenge

Implement marker search and expiry in `starter.py`. Never use a real secret as
a canary. Keep the audit’s unknown surfaces visible.

## Extension

Add a queue, tracing callback, backup snapshot, and deletion evidence. Explain
which copies your process can inspect directly and which require provider terms.
