# 05 — Bounded Tool Agent

[Read the Agent Design chapter →](https://guide.organizedai.vip/agentic-eng/chapters/agent-design/)

Build a deterministic agent harness that can read approved event data or ask a
question, but cannot turn text inside a record into new authority.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

The “model” is a scripted policy so the control loop is transparent. Replace it
only after the harness tests are green.

## Challenge

Implement `run_agent()` in `starter.py`: validate tool names, authorize every
call, cap steps, and detect repeated calls that make no progress.

## Extension

Add an approval object bound to an exact action, arguments, source version,
approver, and expiration. Test that editing the action invalidates approval.
