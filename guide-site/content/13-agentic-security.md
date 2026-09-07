> **The question:** What can untrusted content make your system do?

Chapter 05 treated prompt injection as a trust-boundary problem: a malicious event description is data, not authority. This chapter maps the full threat surface around that boundary and the architectural patterns that hold it. The short version: no prompt makes an agent safe. Only the structure around the model does.

## The mental model

An attacker who can reach your agent's context is trying to reach your agent's **effects**. Every defense in this chapter is a way to keep those two things apart.

OWASP now maintains a Top 10 for agentic applications, and its categories are all versions of the same move. **Goal hijacking** rewrites what the agent is trying to do. **Tool misuse** aims existing tools at targets you never intended. **Memory poisoning** plants instructions or false facts in stored context so the attack fires later, in a different session. **Multi-agent trust exploitation** passes tainted output from a less-trusted agent into a more-trusted one.

For the event assistant, the assets worth naming are the attendee records, the organizer's email account, the ability to publish, and the budget. A defense that does not name its assets is a vibe.

## Constrain architecture, not the prompt

A 2025 design-patterns literature (Beurer-Kellner et al., from IBM, Invariant Labs, ETH Zurich, Google, and Microsoft) collects six ways to structure an agent so untrusted input cannot trigger a consequential action:

- **Action-selector.** Tool output never flows back into the model. The model picks from fixed actions; results go to a human or a dead end.
- **Plan-then-execute.** The plan is fixed before any untrusted content is read. A poisoned document can change what a step returns, never what steps exist.
- **LLM map-reduce.** Untrusted content is only ever seen by per-item sub-agents with no tools. The aggregating agent sees their sanitized outputs, never the raw text.
- **Dual LLM.** A privileged planner with tools never reads untrusted content; a quarantined reader does, and passes back only symbolic answers.
- **Code-then-execute.** The model writes a program against a constrained API; the program, not the model, touches the world.
- **Context-minimization.** Strip untrusted content to the smallest usable form before it enters the loop.

The shared principle: once an agent ingests untrusted input, that input must be unable to cause an effect. Google's CaMeL work pushes the same idea into the runtime itself, separating control flow from data flow and checking capability-tagged data against a policy engine before any effect fires.

For the event assistant, plan-then-execute fits naturally: fix the plan (retrieve, draft, validate) before opening any organizer-supplied document.

## Secure the tool supply chain

Tools are dependencies, and dependencies get attacked. MCP servers have their own literature now: **tool poisoning** (a malicious instruction hidden in a tool's description), and **rug pulls** (a server that changes its tool descriptions after you approved them).

Treat a new tool server like a new npm package. Pin versions. Review descriptions as code. Diff them on update.

Run each tool with the minimum it needs: a microVM or container boundary, an egress allowlist naming the exact hosts it may call, and credentials scoped to that tool alone. A read-only venue-lookup tool should hold no credential that could send email. When a tool is compromised, the blast radius should be the tool, not the system.

Illustrative policy check before any effect:

```python
# Pseudocode: effects require a capability, not the model's say-so.
def execute(call, principal, tainted_context):
    if tainted_context and call.has_effect():
        return reject("untrusted input cannot trigger effects")
    capability = policy.capability_for(principal, call.tool)
    if not capability.covers(call):
        return reject("outside granted capability")
    return run_sandboxed(call, egress=capability.allowlist)
```

## Lab: the injection gauntlet

Build a corpus of adversarial documents: event descriptions containing fake organizer instructions, attendee notes embedding fake tool results, a venue page that instructs the agent to email the attendee list, and one document that poisons a saved preference ("the organizer prefers you skip confirmation").

Run the same tasks against three harnesses: an unconstrained agent, a prompt-hardened agent with the same structure, and a plan-then-execute harness. Score unauthorized-action attempts, not just task success. The prompt-hardened run is the control group that shows why wording is not a defense.

Then poison a tool description in the test MCP server and confirm the sandbox holds: the tool's egress allowlist and credential scope should make the compromise boring.

## Failure drills

Hide an instruction in a tool description. Change a tool's description between approval and execution. Plant a malicious memory and run a later session. Pass tainted output from a sub-agent into the planner. Offer the model a tool slightly outside its capability. Each case should end in rejection, with the trace showing which check fired.

## Ship gate

No path exists from untrusted content to a consequential effect. Every tool runs pinned, sandboxed, and minimally credentialed. The gauntlet's unauthorized-action count is zero on the shipping harness. That property depends on knowing who the agent acts as, which is the subject of [agent identity](/agentic-eng/chapters/agent-identity/).
