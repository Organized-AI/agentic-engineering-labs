# 18 — Rail Pipeline

[Read the Guardrails in the request path chapter →](https://guide.organizedai.vip/agentic-eng/chapters/guardrails/)

Build the pipeline of named rails every covered call passes through. The
checkpoint logs each rail's decision, measures its latency cost, and fails
closed: a rail that errors denies the call instead of skipping.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

An injection rail, a scope rail, and a topic rail wrap one tool call. The
clean call passes with every decision and the total latency logged. A
poisoned call is denied by the injection rail. A rail that throws turns into
a deny, never a silent pass.

## Challenge

Implement `run()` in `starter.py`. Then point the tests at the starter.
Every outcome must name the rail and the reason, and rail errors must deny.

## Extension

Add a latency budget: rails whose cumulative cost exceeds the budget are
reported, and the pipeline names which rail to move, sample, or drop first.
