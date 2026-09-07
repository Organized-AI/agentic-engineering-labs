# 21 — Mesh Policy Checker

[Read the Tailnets & agent networking chapter →](https://guide.organizedai.vip/agentic-eng/chapters/tailnets/)

Build the checker that proves the mesh allows exactly the intended paths.
The checkpoint loads a tailnet policy, confirms the agent hosts can reach the
services they need, and confirms everything else is denied by default.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A policy grants the dev machines access to the services hub on the Ollama
port and SSH, and grants the phone the dashboard port only. The checker
verifies the intended path, verifies the phone cannot SSH, and verifies a
brand-new device gets nothing until policy admits it.

## Challenge

Implement `allows()` and `audit()` in `starter.py`. Then point the tests at
the starter. Default is deny: an unmatched rule set means no access, and
unknown devices are never implicitly trusted.

## Extension

Add the Funnel exception: mark one service as publicly exposed and make the
audit print it as the single deliberate hole in an otherwise private mesh.
