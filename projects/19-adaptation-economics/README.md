# 19 — Adaptation Lever Pricer

[Read the Adaptation economics chapter →](https://guide.organizedai.vip/agentic-eng/chapters/adaptation-economics/)

Build the comparison that prices prompt, retrieval, and fine-tuning on the
same ledger before pulling any lever. The checkpoint scores each option on
measured quality and cost per accepted outcome, and records the comparison
so it can be rerun.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

Three options run the same 30-task suite: a prompt revision, a retrieval
pack, and a fine-tune with fixed training cost. The pricer includes failed
attempts and review time, and the cheapest acceptable option wins - which is
not the one with the highest raw pass rate.

## Challenge

Implement `price()` and `winner()` in `starter.py`. Then point the tests at
the starter. Fixed costs amortize over expected volume, and review time is
real money.

## Extension

Add a rerun trigger: when production eval scores drift more than a threshold
below the measured trial quality, the comparison reruns itself.
