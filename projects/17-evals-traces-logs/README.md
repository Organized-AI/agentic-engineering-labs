# 17 — Three-Signal Debugger

[Read the Evals, traces & logs chapter →](https://guide.organizedai.vip/agentic-eng/chapters/evals-traces-logs/)

Build the join that makes one task explainable: logs for what happened,
traces for why, evals for whether it went well. The checkpoint keys all three
signals on one task id and answers "why did it do that" in one call.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A task emits a tool log line, a model span naming the record version it
read, and a sampled grader score. Querying the task id returns all three
joined. A log line with no task id is rejected at write time.

## Challenge

Implement `log_event()`, `add_span()`, `score()`, and `why()` in
`starter.py`. Then point the tests at the starter. Any event without a task
id must fail loudly.

## Extension

Feed failures back: when a sampled grader fails a live trace, append the
trace to the offline eval suite so the surprise becomes a permanent case.
