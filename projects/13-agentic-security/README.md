# 13 — Injection Gauntlet

[Read the Agentic security chapter →](https://guide.organizedai.vip/agentic-eng/chapters/agentic-security/)

Build the policy gate that sits between model proposals and real effects. The
checkpoint rejects effects proposed under untrusted influence, enforces
per-principal capabilities, and detects tool-description rug pulls.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A batch of proposed calls arrives, each marked by whether the model read
untrusted content before proposing it. Reads pass. Effects proposed under
tainted influence are rejected with a reason. A tool whose description changed
since approval is rejected before it runs.

## Challenge

Implement `execute()` and `run_gauntlet()` in `starter.py`. Then point the
tests at the starter. Every rejection must carry its reason so the trace shows
which check fired.

## Extension

Add a poisoned-memory case: a saved preference planted by an earlier document
tries to skip a confirmation step. Mark it tainted at write time and show the
gate still holds in a later session.
