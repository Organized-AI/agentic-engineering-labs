# 15 — Approval Queue State Machine

[Read the Human oversight operations chapter →](https://guide.organizedai.vip/agentic-eng/chapters/human-oversight/)

Build the queue that keeps consequential actions behind live, exact,
single-use approvals. The checkpoint binds each approval to a context hash,
lets one decision execute exactly once, and writes the audit entry before
the effect.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

An agent submits `send_brief` with the hash of the exact brief. The organizer
approves. The first execution writes the audit row and runs; a second
execution attempt raises because the approval is consumed; a doctored brief
fails the context hash.

## Challenge

Implement `decide()` and `execute()` in `starter.py`. Then point the tests at
the starter. Approvals must be exact (context hash), live (not expired), and
single-use.

## Extension

Route by risk: reads auto-approve, low-risk writes batch into a digest, and
irreversible actions require two distinct approvers.
