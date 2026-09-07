> **The question:** Which rules apply to this system, and where is the evidence?

Chapter 09 covered retention as a privacy discipline. Governance is the external version: obligations set by regulators, documented so someone else can verify them. The EU AI Act is the live example with real deadlines and real penalties, and it reaches builders who never incorporated anywhere near Europe - if EU users can use the system, its rules can apply.

## The mental model

The Act sorts obligations by who you are and what the system does. **Model providers** - organizations shipping general-purpose AI models - owe technical documentation, a copyright policy, and training-data summaries (Article 53), with a systemic-risk tier above a compute threshold carrying heavier duties (Article 55). **Deployers** - organizations putting systems to use, which includes anyone building on top of a model API - owe their own set when the use case is high-risk: human oversight, logging, instructions followed, input quality.

The guide's running event assistant is almost certainly not high-risk. The point of this chapter is not that your system is regulated today; it is that the classification exercise is cheap, the deadline math is not forgiving, and the artifacts overlap heavily with work this guide already does.

## The artifact map is the practical shortcut

Most governance work is producing evidence, and most of the evidence already has a home in earlier chapters. The human-oversight demonstration is chapter 15's approval architecture plus its audit log. The logging obligation is chapter 17's traces with chapter 09's retention policy. The quality-management and risk records are chapter 06's eval gates and chapter 01's decision log, written down. Data-governance documentation is chapter 09's persistence inventory.

```python
# Pseudocode: obligations map to artifacts you already produce.
obligations = {
    "human_oversight": ["approval_queue", "audit_log"],      # ch. 15
    "logging":         ["traces", "retention_policy"],       # ch. 17, ch. 09
    "risk_management": ["eval_gates", "decision_log"],       # ch. 06, ch. 01
    "data_governance": ["persistence_inventory"],            # ch. 09
}
```

The human-oversight duties for high-risk systems took effect in August 2026, with penalties up to 7% of global turnover. Classification first, artifacts second, panic never.

Two habits keep the memo honest. Revisit it on a schedule and on every feature that changes intended purpose, because classification follows what the system does, not what you meant when you wrote the memo. And keep the underlying evidence where auditors actually look - in the systems themselves, with dates and owners - rather than in a compliance folder assembled the week before someone asks.

Note also what the Act is not: a reason to stop shipping. For most builder-side systems the obligations are documentation duties on work a careful team already does, and the penalty tier exists to make ignoring them expensive, not to make building impossible.

## Lab: the classification memo

Write the one-page classification memo for the event assistant: intended purpose, users, geography, which Act categories might touch it, and the conclusion with its reasoning. Then build the artifact index: for each obligation that would apply if the classification changed, name the existing system that produces the evidence and the gap where none does.

Run the same exercise for a fictional hiring-screening feature - deliberately high-risk territory - and notice how the memo, not the code, is where the answer lives.

## Failure drills

Ship a feature that changes intended purpose without revisiting the memo. Let the audit log's retention fall short of the logging obligation. Discover an EU customer in a system classified as out of scope. Produce an oversight demonstration that names a person who no longer works there. Each case is a process failure, and each has a process fix.

## Ship gate

The classification memo exists, is dated, names an owner, and the artifact index shows where every applicable obligation is evidenced. Governance is the one the system cannot do for you: it is the discipline of answering to someone outside the build. Next, the boundary underneath all of it: [tailnets and agent networking](/agentic-eng/chapters/tailnets/).
