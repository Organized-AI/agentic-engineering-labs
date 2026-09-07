> **The question:** Should this knowledge live in the prompt, in retrieval, or in the weights?

The guide has quietly assumed two adaptation levers: context (chapters 05 and 16) and retrieval (chapter 11). There is a third: fine-tuning, which changes the model itself. Choosing among the three is an economics problem, which is why it sits next to chapter 12's cost ledger.

## The mental model

**Prompt first.** Instructions and examples in context are the cheapest change to make, the easiest to revert, and the only lever with zero training surface. **Retrieve** when the knowledge is volatile, large, or private: the corpus changes daily, exceeds any window, or must stay cited and deletable per chapter 09. **Fine-tune** for behavior, format, and domain style - the things that are expensive to say in every prompt and stable enough to bake in.

Long-context windows keep moving the boundary. Tasks that required retrieval at 8k tokens sometimes fit in the window now; the honest comparison is cost and accuracy at your operating point, not the architecture diagram.

## Price each lever on the same ledger

Prompting costs tokens on every call - cheap to start, expensive at scale. Retrieval costs an index, a query path, and the eval work of chapter 06 to keep answer quality honest. Fine-tuning costs a training run, an eval gate, and a new deployment for every knowledge refresh - and it cannot cite its sources, which chapter 11's provenance rules may require.

```python
# Pseudocode: the comparison is cost per accepted outcome, per lever.
for lever in ["prompt", "rag", "fine_tune"]:
    quality = eval_suite.run(lever, tasks)          # chapter 06 harness
    unit_cost = ledger.cost_per_accepted(lever)     # chapter 12 ledger
    report(lever, quality, unit_cost)
```

The decision framework that survives contact with practice: start with the prompt, add retrieval when the corpus wins the argument, fine-tune only when the first two provably cannot carry the behavior - and re-run the comparison when prices or context windows move, because they move constantly.

Two failure modes deserve their own warnings. Fine-tuning on unvetted examples teaches the model your mistakes at scale, and unlike a bad prompt, the result cannot be edited afterward - only retrained. And hybrid systems leak cost: a fine-tuned model behind a retrieval stack behind a long prompt can cost more than any two levers alone, so the ledger covers the whole path, not the favorite component.

## Lab: three levers, one task

Take one event-assistant task - say, matching the house style of briefs. Build the prompt-only version with examples in context, the retrieval version over a style corpus, and a small fine-tune on approved examples (a hosted fine-tuning API keeps this cheap and reversible).

Grade all three on the same chapter 06 suite and price them on the chapter 12 ledger, including the retrieval infrastructure and the training run, amortized honestly. The result is usually a ranking you could not have argued into existence in advance.

One honest note on scope: fine-tuning changes what the model is, which means chapter 01's experimentation discipline applies with double force - hold out a final eval the tuning process never saw, and keep the base model's scores beside the tuned one's so regression has nowhere to hide. A lever you cannot roll back safely is not an adaptation strategy; it is a commitment.

## Failure drills

Change the corpus daily and watch the fine-tuned version go stale while retrieval keeps up. Grow the prompt until its per-call cost passes the fine-tune's amortized cost. Remove a source the brief must cite and confirm only the retrieval path notices. Degrade the style corpus and check which lever's eval moves first.

## Ship gate

The chosen lever won on measured quality and cost per accepted outcome, with the comparison recorded and dated so it can be rerun. Economics is the last internal lever; the final chapter looks outward, at the rules builders do not get to set: [AI Act and governance](/agentic-eng/chapters/ai-act-governance/).
