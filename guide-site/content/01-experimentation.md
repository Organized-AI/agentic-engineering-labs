> **The question:** How do you turn a week of building into knowledge that makes the next week better?

An experiment is a decision-making instrument. It is not simply a new prompt, a different model, or another demo. Before changing a system, decide what evidence would make you keep the change—and what would make you reject it.

This chapter proposes a small research process for the event-operations assistant used throughout the guide. The goal is to produce accurate organizer briefs from approved event records, not to maximize how sophisticated the implementation sounds.

## The mental model

Separate three kinds of work. **Exploration** asks whether something is possible. **Comparison** asks whether a candidate is better than a baseline. **Validation** asks whether a particular configuration meets a release requirement. A surprising exploratory result deserves a controlled comparison; it does not automatically justify a production release.

In an evaluation, the task is the problem being attempted and the trial is one attempt. Repeat trials when output variability matters. This vocabulary comes from [Anthropic’s evaluation guidance](/agentic-eng/sources/#evals); the experiment process below is a suggested application of it.

Define the unit you care about. If you test a brief generator, one unit might be “one complete brief for one event,” not “one model response.” A brief may require retrieval, several calls, validation, and human correction. Measuring only one call hides the rest of the work.

## Design a decision before a test

Write a short experiment card:

```text
ID: event-brief-014
Question: Does canonical venue lookup reduce invented venue facts?
Baseline: Existing workflow and prompt, version A.
Candidate: Same workflow, with approved venue records included.
Primary measure: Accepted briefs / attempted tasks.
Guardrails: No cross-tenant access; no material latency regression.
Budget: Fixed test set, maximum trials, spending ceiling.
Decision: Adopt only after reviewing improvements and new failures.
```

Choose one primary outcome and a few guardrails. If you optimize ten metrics independently, almost any experiment can be described as a win. A primary measure makes the decision harder to manipulate; guardrails stop a quality gain from concealing a permission failure or unacceptable delay.

Keep a baseline even when the baseline is manual work. Otherwise, you may demonstrate that a new system works without learning whether it is useful relative to the current process.

## Worked example: paired comparisons

Suppose two configurations each process the same 40 synthetic events. A succeeds on 30; B succeeds on 33. The headline is a 7.5-percentage-point gain, but the paired results matter more:

| Outcome on the same event | Count |
| --- | ---: |
| Both succeed | 28 |
| Only A succeeds | 2 |
| Only B succeeds | 5 |
| Both fail | 5 |

These invented numbers reveal five improvements, two regressions, and five unresolved problems. Inspect all three groups. If B’s two regressions expose unauthorized information, its aggregate score does not make it deployable.

This is descriptive arithmetic, not a claim of statistical significance. Forty events may be useful for discovering failure patterns while being inadequate for estimating rare failures. Correlated tasks—such as ten rewrites of the same event—also provide less independent evidence than the raw count suggests.

## Control what can mislead you

Record model identifier, prompt version, retrieval snapshot, tool version, limits, and test-set revision. Keep outputs from both variants. Randomize or alternate execution order if provider load or caching could favor the second run. Run warm-cache and cold-cache comparisons separately when those conditions matter.

Start with one change at a time to make attribution easier. Later, deliberately test interactions: a shorter prompt may work with a better retriever but fail with the original retriever. A factorial design can investigate interacting factors, but only after you can trust the task set and measurements.

Avoid repeated tuning against a supposedly untouched holdout. Once its failures influence the design, it has become development data. Keep that history and reserve fresh validation cases for consequential decisions.

## Lab: create a research ledger

Allow 60–90 minutes for the first version.

1. Create 24 synthetic events: eight complete, eight missing important facts, and eight containing conflicts or distracting instructions.
2. Define acceptance rules before generating outputs. List which missing facts must cause a question or an explicit unknown.
3. Compare the current workflow with exactly one candidate change. Preserve the same records and task order metadata.
4. Record outcome, failure category, elapsed time, and attributable cost per task. For an offline exercise, mark cost as simulated rather than real.
5. Repeat the six most variable cases. Do not hide repeated failures behind a best-of-many result.
6. Write a decision memo including one example that improved and one that did not.

The deliverable is a ledger plus a decision, not a leaderboard. A valid decision can be “the evidence is inconclusive; collect a better sample.”

## Failure drills

**The winner changes on rerun.** Examine variability, task ambiguity, and unstable dependencies before declaring a regression.

**A large gain appears after a dataset change.** Re-run both baseline and candidate on the new dataset. Scores on different task mixes are not directly comparable.

**Everything improves except one severe failure.** Separate safety or authorization gates from average quality. Do not offset a severe violation with better prose.

**Experiments pile up without decisions.** Require a short conclusion and a named next action. Archive rejected ideas with the reason so they do not consume the same time again.

## Ship gate

You are ready to use this process when another person can reproduce the comparison, understand the acceptance rules, see the failures, and explain why the candidate was accepted or rejected. Carry this ledger into [evaluations](/agentic-eng/chapters/evaluations/) and [cost of cognition](/agentic-eng/chapters/cost-of-cognition/).
