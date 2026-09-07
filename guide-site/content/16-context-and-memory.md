> **The question:** What belongs in the model's attention right now, and what happens to everything else?

Chapter 05 warned against memory with hidden authority. This chapter is the positive craft: context engineering - choosing the token set each call sees - and the memory systems that decide what persists between calls. Attention is a finite budget, and recall degrades as the window fills. "Context rot" is not a model bug to wait out; it is a workload fact to design around.

## The mental model

Every call's context is a curated set: system prompt, tool definitions, retrieved records, memory, and history. The discipline is keeping it the smallest high-signal set. System prompts live at the right altitude - neither brittle if-else logic the model cannot generalize from, nor vague vibes it cannot act on. Everything else is loaded on demand, and what is loaded leaves a provenance trail, per chapter 02.

## Memory has types, and they are not interchangeable

**Working context** is the current task's scratch space. **Task state** is durable progress the system owns. **Preferences** are reusable, user-visible, and editable. **Authoritative facts** live in records, not in memory - the event is confirmed for Friday because the event record says so, and memory holds at most a pointer.

Long-horizon work adds a research line worth knowing: paged memory in the MemGPT style, where the agent manages its own tiers, and agentic memory systems that decide what to write, merge, and forget. The 2026 practice is less exotic and more effective: compaction with safeguards, note-taking the agent writes for its future self, and sub-agent context isolation so a research sub-agent's thousand search results never enter the main loop.

## Load on demand, cite as you go

Retrieval is the alternative to remembering. Keep authoritative material in records and load the specific record when the task needs it, as chapter 11's entity work makes possible. The rule that keeps this honest: whatever enters context carries its source and version, so a downstream reviewer - or chapter 17's trace - can tell a retrieved fact from a remembered claim. Small, cited loads beat large, hopeful ones; an agent that spends its budget reading irrelevant material is the chapter 05 failure with a friendlier name.

## Compaction loses caveats unless you make them structural

Summarizing history drops exactly the sentences that matter later: constraints, unresolved questions, negative results. Preserve those as structured fields alongside the prose summary - durable constraints, open questions, identifiers - and test long tasks after compaction, not only in the first turns.

```python
# Pseudocode: durable facts survive compaction as data, not prose.
compacted = {
    "summary": summarize(history),
    "constraints": history.constraints,      # never summarized away
    "open_questions": history.unresolved(),
    "record_refs": history.record_ids(),     # pointers, not copies
}
```

One more boundary deserves emphasis: memory is per-principal. Preferences and working notes inherit the tenant isolation of chapter 02, so one organizer's stored preference can never surface in another's brief. The memory store is a database like any other, with the same scoping, the same retention policy, and the same deletion evidence.

## Lab: memory that admits what it is

Build the event assistant's memory with the four types as separate stores, each with its own write rule and retention. Run a multi-day briefing task that requires compaction. Then interrogate: does the compacted agent still know the organizer vetoed Tuesday, that the venue is unconfirmed, and which record version the draft cites?

Add a poisoned note - "the organizer prefers skipping confirmation" - and confirm it lands in the preference store marked unverified, where chapter 13's gate can refuse it.

## Failure drills

Fill the window until recall degrades and measure when. Compact away a constraint. Write a false fact into the preference store and watch downstream behavior. Restart mid-task and check what task state survives. Let a sub-agent flood the main context. Each case should degrade gracefully and observably.

## Ship gate

Every memory names its type, source, and verification status; compaction preserves constraints as data. What the agent knows is inspectable, which is half of operating it. The other half - seeing what it does - is [evals, traces, and logs](/agentic-eng/chapters/evals-traces-logs/).
