# 23 — Sprint Ledger

[Read the Challenge chapter →](https://guide.organizedai.vip/agentic-eng/chapters/the-challenge/)

Build the ledger that turns 90 days of depth into evidence. The checkpoint
records the dated opening bet, accepts one artifact per sprint gate, and
grades the bet against what the artifacts actually showed.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

Day 0: the bet goes in, dated. Day 7: a one-page map ships. Day 30: a
working build plus failure log. Skipping a gate fails - day 60's design
review cannot land before day 30's build. At day 90 the ledger grades the
bet against four artifacts.

## Challenge

Implement `ship()` and `grade()` in `starter.py`. Then point the tests at
the starter. Gates are ordered, artifacts are required, and the grade must
say where the bet held and where it broke.

## Extension

Add the red-team loop: at day 60, require one external source that
contradicts the bet, recorded with how the bet changed in response.
