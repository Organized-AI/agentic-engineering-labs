# 25 — Turn Loop Harness

[Read the Agent runtimes chapter →](https://guide.organizedai.vip/agentic-eng/chapters/agent-runtimes/)

Build the turn loop as a real harness: context assembly under budget, a
policy choke point for every effect, tool dispatch with timeouts, and a
checkpoint after every turn. The model sits behind an interface narrow
enough to stub.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A stub model proposes two calls: read the calendar, send the briefing. The
runtime assembles context within budget, runs both through the policy
check, rejects a send to an unknown recipient, and checkpoints the turn.

## Challenge

Implement `assemble()`, `policy_check()`, and `run_turn()` in
`starter.py`. Then point the tests at the starter. The stub model must
never be called with an over-budget context.

## Extension

Kill the process mid-turn and resume from the checkpoint: the briefing
must be sent exactly once.
