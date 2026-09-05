# 07 — Inference Memory & Hosting Planner

Estimate weight memory and conventional KV-cache memory, then compare managed
and self-operated hosting with explicit operational assumptions.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

The formulas are educational estimates—not sizing guarantees for every model
architecture or runtime.

## Challenge

Implement the byte estimators and reject a plan that does not fit the declared
memory headroom.

## Extension

Add quantized weights, cache precision, concurrent sequences, and sliding-window
attention. Compare estimates with measured runtime metrics on hardware you own.
