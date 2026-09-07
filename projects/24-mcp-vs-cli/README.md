# 24 — Tool Door Router

[Read the MCP vs CLI chapter →](https://guide.organizedai.vip/agentic-eng/chapters/mcp-vs-cli/)

Route each capability an agent uses to the right door - MCP, CLI, or a
hardened script - on measured cost, validation strength, and determinism
requirements instead of on fashion.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A calendar capability is driven through both doors. The MCP door is a minimal
stateless server: one HTTP-style handler answering `initialize`, `tools/list`,
and `tools/call`, assigning no session ID, so every request stands alone. The
CLI door runs command strings. The router measures discovery tokens and
validation catches per door, then routes on the chapter's rules: repeated and
exact work hardens into a script, stateful or complex-schema work goes to MCP,
composable installed tools stay on the CLI.

## Challenge

Implement `measure()`, `route()`, and `harden()` in `starter.py`. Then point
the tests at the starter. A capability marked `repeated=True, exact=True` must
never route to a model-mediated door.

## Extension

Add a stateful MCP door that assigns session IDs, then kill it mid-call and
record what the client must handle (404 on expired session, re-initialize)
that the stateless door never asks for.
