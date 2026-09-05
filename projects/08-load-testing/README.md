# 08 — Queueing Workload Simulator

Simulate an open-loop arrival schedule, one or more workers, deadlines, and
accepted outcomes. Find the point where offered load increases while goodput
falls.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

This deterministic simulator teaches measurement boundaries. It is not a
replacement for a real client-side benchmark.

## Challenge

Implement `simulate()` and `percentile()` in `starter.py`. Include failures and
deadline misses in the attempted-work denominator.

## Extension

Add mixed short/long requests, burst arrivals, dependency errors, and an
admission limit. Compare open-loop with closed-loop load generation.
