# 27 — State Auditor

[Read the State, sessions & statelessness chapter →](https://guide.organizedai.vip/agentic-eng/chapters/state-sessions-statelessness/)

Give every piece of agent state a home - context, session, or stores - with
an owner, a lifetime, and a recovery path. State with no home is a leak,
and leaks are what restarts turn into incidents.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A runtime inventories its state: the conversation transcript (rebuildable
from stores), a tool session ID (contained in one supervised component,
with a rebuild path), and a recipient list hiding in a module global - home
None, owner nobody, a finding. The audit fails until the list moves into a
store.

## Challenge

Implement `audit()` and `kill_and_resume()` in `starter.py`. Then point
the tests at the starter. The kill-between-any-two-lines test is the
acceptance criterion.

## Extension

Expire the tool session server-side mid-turn and watch whether the client
rebuilds from stores or errors out.
