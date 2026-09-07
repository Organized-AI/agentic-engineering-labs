# 16 — Typed Memory Store

[Read the Context & memory systems chapter →](https://guide.organizedai.vip/agentic-eng/chapters/context-and-memory/)

Build the store that keeps profile, episodic, semantic, and working memory
separate, sourced, and inspectable. The checkpoint assembles a context under
a budget, records provenance on every entry, and compacts without dropping
constraints.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A verified preference, an episode from one meeting, and an unverified rumor
all enter the store with their types and sources. Assembly fills the token
budget with verified entries first. Compaction folds the episode into a
summary while the constraint list survives as data.

## Challenge

Implement `assemble()` and `compact()` in `starter.py`. Then point the tests
at the starter. Compaction may summarize episodes but must never drop a
constraint or an open loop.

## Extension

Add memory poisoning defense: entries written from untrusted sources land in
a quarantine lane and can only promote after a verified source agrees.
