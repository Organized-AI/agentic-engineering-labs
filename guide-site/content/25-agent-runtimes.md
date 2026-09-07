> **The question:** What actually runs your agent between one user message and the next?

Strip an agent down and two things remain: the model, which proposes, and the runtime, which disposes. The model gets the attention, but the runtime decides what the model sees, which of its proposals execute, what happens when they fail, and when the whole thing stops. Chapters 04 and 05 designed that boundary as a contract; this group operates it as a process. Because a runtime is not a diagram. It is a long-lived process that holds state, supervises connections, schedules work, and dies badly if you let it.

## The mental model

The runtime is an operating system for one agent. The turn loop is its scheduler: receive input, assemble context, call the model, dispatch tool calls, feed results back, repeat until done. Context assembly is its memory management: a fixed window, an allocation policy, eviction under pressure. Tool dispatch is its syscall layer: the only path from model intent to real effect, and therefore the only place policy can live. Persistence is its filesystem: transcripts, checkpoints, and the memory stores of chapter 16.

The analogy earns its keep the moment something breaks. Operating systems do not trust the programs they run; they isolate them, account for them, and kill them. A runtime that trusts the model's proposals is a kernel running every binary as root.

## The anatomy of one turn

A turn is smaller than people think, and every line of it is a design decision:

```python
# Pseudocode: one turn of the event-operations assistant.
def turn(runtime, user_message):
    runtime.log("turn.start", trace_id=runtime.trace)
    ctx = runtime.assemble(user_message, budget=runtime.context_budget)
    proposal = runtime.model.complete(ctx, tools=runtime.tool_schemas())
    for call in proposal.tool_calls:
        runtime.policy.check(call)          # the only choke point
        result = runtime.tools.dispatch(call, timeout=call.budget)
        runtime.log("tool.result", call=call.name, ms=result.ms)
        ctx.append(call, result)
    runtime.checkpoint(ctx)                 # state survives a crash
    return proposal.final_text
```

Three things to notice. First, the model appears once, behind an interface; everything else is the runtime's job. Second, every effect passes a choke point, so policy has exactly one home. Third, the loop checkpoints, because the next chapter's question - what happens when this process dies mid-turn - is answered here or nowhere.

## What the runtime owns, what the model owns

The model owns judgment: reading, reasoning, choosing the next action, writing the final answer. The runtime owns everything with a correctness property: the context budget, the tool list, argument validation, timeouts, retries, logging, checkpointing, and the stop condition. Disputes between the two are always resolved the same way - if you can write a test for it, the runtime owns it. The model's output is untrusted input to every runtime mechanism, which is why chapter 13's injection defenses live in the dispatch layer and not in the prompt.

This split is also what makes agents debuggable. When the event assistant sends a briefing to the wrong list, the first question is never "why did the model do that" - it is "which runtime mechanism allowed it." Missing validation, a too-wide tool scope, a checkpoint that replayed stale state: each is a runtime bug with a fix. "The model felt like it" has no fix.

## The loop is a process

Everything this implies is the subject of the rest of this group. A process needs supervision, because hung tools and wedged connections are chapter 26's daily reality. It needs a state discipline, because what lives in context, in session, and in stores decides whether restarts are free or fatal - chapter 27. It needs scheduling, because real agents run on timers and events, not just user messages - chapter 28. And it needs isolation, because one tenant's agent must never read another's state - chapter 29. Run the loop like the process it is, and each of those becomes engineering instead of incident response.

## Lab: a minimal runtime loop

Build the turn loop above for real, in under a hundred lines. Give it two pluggable tools - a calendar reader and a brief sender - a context budget it enforces by evicting oldest tool results, a policy check that rejects sends to unknown recipients, and a checkpoint file written after every turn. Then run the event assistant's morning briefing through it. The deliverable is not the agent; it is the harness: swap the model for a stub that returns canned proposals, and your tests should still pass, because the runtime's guarantees never depended on the model.

## Failure drills

Kill the process mid-turn and resume from the checkpoint. Hand the model a tool result larger than the context budget and watch eviction behave. Make a tool hang and find out whether your loop has a timeout (it does not, yet). Feed the policy check a send to a recipient one character off an approved one. Each drill maps to a chapter that follows; each should fail loudly today.

## Ship gate

The runtime runs the turn loop with a single choke point for every effect, a context budget enforced by policy rather than hope, a checkpoint after every turn, and a stop condition the model cannot talk its way around. The model sits behind an interface narrow enough to stub in tests. With the loop running as a real process, the next question is keeping it alive: [supervision and lifecycle](/agentic-eng/chapters/supervision-lifecycle/).
