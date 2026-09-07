> **The question:** Now that you've read the whole arc - can you go deep enough that the goalposts move?

Breadth is what the guide gives you. Depth is what you owe yourself. This closing chapter is a structured challenge: pick one connected thread that spans the material and go deep on it through escalating study sprints - one week, then 30, 60, and 90 days. Each sprint raises the bar on what "understanding" means, so by day 90 you are not summarizing the topic, you are arguing with it.

## The mental model

Depth follows a predictable ladder, and the sprints walk it. A week gets you fluency: the vocabulary, the canonical sources, the shape of the debate. Thirty days gets you working knowledge: you have built or operated the thing once, badly, and know where it breaks. Sixty days gets you judgment: you can predict failure modes before you meet them and defend a design choice against a skeptic. Ninety days gets you an edge: an opinion or artifact the field doesn't already have - a benchmark, a post, a patch, a better pattern.

The rule that makes it work: each sprint ends with a public or private artifact, never just reading. Depth that produces nothing is tourism.

## Picking your thread

Choose a topic that *spans* chapters, because the seams are where shallow coverage hides. Strong candidates from this guide:

- **Security end to end** - threat models (13) through identity (14), guardrails (18), and the network boundary (21). One attack surface, every layer.
- **The evaluation stack** - graders (06), staging (07), observability and evals on live traffic (17), and the economics of what to measure (19).
- **Memory and context as a system** - records (03), compaction and memory types (16), provenance (02), and what oversight does with them (15).
- **Your own tailnet as a lab** - chapters 21 and 22 applied to real hardware you own, with chapter 12's cost ledger scoring every choice.

The wrong pick is the one that sounds impressive. The right pick is the one your current project already keeps bumping into.

## The sprints

**Week one: fluency.** Read the primary sources behind the chapter set - the papers and docs in the [sources](/agentic-eng/sources/), not summaries of them. Build the chapter's lab yourself before reading the solution. Deliverable: a one-page map of the topic's open questions, in your own words.

**Days 8-30: working knowledge.** Implement the pattern against a real system - your own. For the security thread, that means actually running the Injection Gauntlet against your harness and writing ACLs for your real tailnet. Expect it to break; the breakage is the curriculum. Deliverable: a working thing plus a failure log.

**Days 31-60: judgment.** Red-team your own build. Hand it to the failure drills from each chapter in the thread and run every one. Compare your design against two production-grade alternatives and write down what you chose differently and why. Deliverable: a design review of your own work, with the trade-offs named.

**Days 61-90: edge.** Contribute something back. Publish the benchmark nobody had, open-source the tool you wished existed, write the deep dive your week-one self needed. Deliverable: an artifact with your name on it that moves the topic.

```python
# Pseudocode: the sprint ladder.
sprints = [(7,  "fluency",           "one-page map of open questions"),
           (30, "working knowledge", "working build + failure log"),
           (60, "judgment",          "self design-review with trade-offs"),
           (90, "edge",              "public artifact that moves the topic")]
for days, level, artifact in sprints:
    work(thread, until=days)
    ship(artifact)            # no artifact, no level-up
```

## Lab: sprint zero

Today, before day one: pick the thread, write the one-paragraph bet on what you currently believe about it, and date it. Every sprint after that gets scored against the bet - where it held, where it broke. The bet is what turns 90 days of work into evidence about how you learn.

## Failure drills

Two weeks in, explain the topic out loud without notes - the gaps are your day-30 reading list. Miss an artifact deadline and diagnose the sprint, not yourself. Find a source that contradicts the guide and run it to ground. At day 60, have someone skeptical read your design review.

## Ship gate

Four artifacts shipped, the bet graded honestly, and the goalposts visibly moved from where they started. That is the whole method - the guide ends, and the practice becomes yours. The [deep research expansion](/agentic-eng/deep-research/) is standing by when you want the next thread.
