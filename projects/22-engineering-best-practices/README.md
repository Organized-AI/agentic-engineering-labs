# 22 — Foundation Audit

[Read the Engineering best practices chapter →](https://guide.organizedai.vip/agentic-eng/chapters/engineering-best-practices/)

Build the audit that scores the classic engineering blocks on evidence
before agent scope expands. The checkpoint runs each block's check against a
repo report, names the weakest block, and shows the evidence behind the
score - never a vibe.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A repo report goes in: commits exist, tests run in CI, but the last deploy
has no documented rollback and the production prompt is not in git. The
audit scores each block, names rollback as the weakest, and prints the exact
evidence.

## Challenge

Implement `audit()` in `starter.py`. Then point the tests at the starter.
Every score must carry its evidence, and any block below threshold lands on
the fix-first list in dependency order.

## Extension

Wire the audit into CI: a pull request that weakens a block's evidence
fails the build, the same way a failing test does.
