# 14 — Identity-Aware Tool Gateway

[Read the Agent identity chapter →](https://guide.organizedai.vip/agentic-eng/chapters/agent-identity/)

Build the gateway that answers "who is the agent acting as" on every call.
The checkpoint exchanges a user token for an audience-scoped token, verifies
subject and scope at call time, and refuses to let a shared service account
stand in for identity.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A user's token is exchanged for a token scoped to `calendar` with
`event:write`. The gateway executes a matching call, rejects the same token
against a `billing` tool, and rejects a service-account token that names no
subject at all.

## Challenge

Implement `exchange()` and `call()` in `starter.py`. Then point the tests at
the starter. Every rejection must say which identity check fired.

## Extension

Add delegation depth: an agent acting for an agent acting for a user. Carry
the full actor chain in the token and reject calls where any link is missing.
