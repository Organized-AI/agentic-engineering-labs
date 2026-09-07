# 31 — Five Walls Bench

[Read the Sandboxing chapter →](https://guide.organizedai.vip/agentic-eng/chapters/sandboxing/)

A sandbox is a promise with an edge: filesystem, network, credentials,
resources, lifetime. Build the sandbox-per-task pattern, then attack all
five walls - a wall that was never attacked is an assumption, not a
boundary.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

The event assistant's report generator runs in a fresh sandbox: its own
scratch filesystem, egress denied by default except one allowlisted host,
a scoped token minted for the task and revoked at teardown, hard resource
caps, and total destruction at the end. State that must survive is written
to a store outside the boundary.

## Challenge

Implement `Sandbox.exec()` policy enforcement, `mint()`, and
`run_generated_report()` in `starter.py`. Then point the tests at the
starter. Teardown must revoke credentials and destroy the sandbox even
when execution raises.

## Extension

Restore a checkpoint written by a different tenant's namespace and check
whether the sandbox notices. It should.
