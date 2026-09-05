# 12 — Accepted-Outcome Cost Ledger

Calculate cost per accepted result from every attempted task, including retries
and review time. Compare a two-stage route and a self-hosting break-even case.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

All dollar values are synthetic. The point is the denominator and the decision
logic, not a vendor price forecast.

## Challenge

Implement the ledger and break-even formula in `starter.py`. Never silently
drop failed attempts or divide by zero accepted outcomes.

## Extension

Add scenario slices, correlated outages, reserved-capacity utilization, and a
sensitivity table for review time and demand.
