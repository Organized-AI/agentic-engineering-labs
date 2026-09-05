# 06 — Outcome Evaluation Harness

[Read the Evaluations chapter →](https://guide.organizedai.vip/agentic-eng/chapters/evaluations/)

Run repeated trials, grade environment state and forbidden effects, keep every
attempt in the denominator, and make a release decision from hard gates plus a
minimum acceptance rate.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Challenge

Implement `evaluate()` and `release_gate()` in `starter.py`. Do not grade the
agent’s claim when the environment can prove the real result.

## Extension

Add scenario slices and a pairwise style grader. Calibrate the style grader
against a small set of human-reviewed anchors.
