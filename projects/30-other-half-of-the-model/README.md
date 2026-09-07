# 30 — Attribution Bench

[Read The other half of the model →](https://guide.organizedai.vip/agentic-eng/chapters/other-half-of-the-model/)

Based on Colin McNamara's talk
[Your Harness Is the Other Half of the Model](https://colinmcnamara.com/talks/harness)
([full write-up](https://colinmcnamara.com/blog/engine-other-half-of-the-model)).
Four harness faults are planted behind an endpoint. Your tests get only
black-box signals; produce the diagnosis table that names which signal
caught each fault - and which cheap check would have sworn all was well.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

Decode jumps 43 percent while prefill holds flat: prefill and decode load
the same silicon in opposite ways, so overhead work lands on one and not
the other - the serving stack takes the blame. The endpoint checks pass
throughout; only the full agent loop catches the tool-calling fault.

## Challenge

Implement `diagnose()` and `probe_full_loop()` in `starter.py`. Then point
the tests at the starter. "model" may only be reached by elimination.

## Extension

Plant a fifth fault of your own and watch which existing signal names it -
or discover that none does, which is the real finding.
