# 20 — Classification Memo Builder

[Read the AI Act & governance chapter →](https://guide.organizedai.vip/agentic-eng/chapters/ai-act-governance/)

Build the memo that answers the two governance questions before launch: what
class is this system, and which duties are ours. The checkpoint classifies a
system profile against written rules, splits provider from deployer duties,
and maps every applicable obligation to an artifact that evidences it.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

An event-operations assistant profile goes in: it ranks content and sends
messages, but does not score people or make eligibility decisions. The memo
lands on limited-risk with transparency duties, names the deployer, and maps
each duty to a chapter artifact - eval reports, the audit log, the oversight
queue.

## Challenge

Implement `classify()`, `assign()`, and `map_artifacts()` in `starter.py`.
Then point the tests at the starter. Every applicable duty must map to at
least one artifact, or the memo is incomplete.

## Extension

Add the oversight clock: log when a human last reviewed the system's
outputs, and flag the memo stale when the review interval lapses.
