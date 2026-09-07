# 29 — Containment Matrix

[Read the Isolation & failure containment chapter →](https://guide.organizedai.vip/agentic-eng/chapters/isolation-failure-containment/)

Draw the blast radius before it exists: two tenants on one runtime, and an
executable matrix that proves which failures spread and which stop at the
wall.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

Tenant A's agent, treated as compromised: it tries to read tenant B's
store, call a tool outside its scope, and exceed its token budget. All
three fail with a logged denial. The mirror check runs too: nothing of
B's is reachable from A.

## Challenge

Implement `check_reach()`, `mirror_check()`, and `enforce_budget()` in
`starter.py`. Then point the tests at the starter. The matrix must be
green on evidence, not assertion.

## Extension

Fill tenant A's store with a poisoned memory and trace every place it can
surface; the trace is your real containment matrix.
