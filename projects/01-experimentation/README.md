# 01 — Paired Experiment Ledger

Build a tiny experiment runner that compares two configurations on the **same**
cases. The checkpoint reports wins, regressions, unresolved failures, and the
cost per accepted result.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

Configuration A and B each process the same cases. A result is accepted only if
its fact is correct and it does not violate a hard gate. The paired table tells
you which cases improved and which regressed; an aggregate score alone does not.

## Challenge

Implement `compare()` and `decision()` in `starter.py`. Then point the tests at
the starter. Preserve every attempted case in the denominator.

## Extension

Add repeated trials and report how often the winner changes. Explain why
best-of-many is not the same product as first-attempt reliability.
