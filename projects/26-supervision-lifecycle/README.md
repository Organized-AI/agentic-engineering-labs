# 26 — Supervisor Tree

[Read the Supervision & lifecycle chapter →](https://guide.organizedai.vip/agentic-eng/chapters/supervision-lifecycle/)

Wrap a tool server in a supervisor: a health definition that can fail when
the component is useless, bounded restarts with backoff, a circuit breaker
the agent can read, and a degraded mode that tells the truth.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A calendar server hangs - it accepts connections but never answers. Three
failed health checks trigger a bounded restart; three restarts in a minute
open the breaker. The agent reads the open breaker and degrades to
checkpointed state instead of timing out per call.

## Challenge

Implement `health_check()`, `record_failure()`, and `call()` in
`starter.py`. Then point the tests at the starter. A wedged server must be
detected by deadline, not by luck.

## Extension

SIGKILL the supervisor mid-restart and resume from checkpoint: what state
did the tree lose, and what does the state audit say about it?
