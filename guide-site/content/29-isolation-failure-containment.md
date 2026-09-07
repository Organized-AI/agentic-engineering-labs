> **The question:** One agent gets compromised, confused, or just expensive tonight - what else does it take down with it?

The group so far built one runtime that runs well: supervised, state-disciplined, awake on schedule. Production reality is many runtimes sharing iron, credentials, and data - multiple tenants, multiple agents per tenant, tools and models in common. Every shared thing is a coupling, and couplings are how a bad hour for one agent becomes a bad night for the platform. Isolation is the design work of deciding, in advance and on purpose, which failures are allowed to spread. Chapter 13 asked how the agent gets attacked; this chapter asks what the blast radius is when the defense misses.

## The mental model

Draw the blast radius before it exists. Containment is not a feature you add after an incident; it is a property of boundaries you drew on a Tuesday. The method is mechanical: enumerate the failure - compromised, confused, or costly - and trace what it can reach through each shared resource. If tenant A's agent can read tenant B's store, the boundary is fictional regardless of what the architecture diagram says. If a runaway agent can spend the whole model budget, every other tenant's latency SLO is a hope, not a property.

The rule that organizes the work: isolate at the layer where the failure actually travels. Prompt-level attacks travel through context, so the boundary is per-conversation state (chapter 27). Tool-level attacks travel through credentials and network, so the boundary is per-agent identity (chapter 14) and egress. Runaway consumption travels through schedulers and queues, so the boundary is per-tenant budgets. A boundary drawn at the wrong layer is decoration.

## The three failures, the three walls

**Compromised** - the agent is working for someone else. The wall is least privilege at runtime granularity: per-agent credentials with per-tool scopes (chapter 14's subject verification on every call), egress allowlists per agent rather than per host, and stores namespaced so one agent's memory is never another's context. Assume the prompt injection succeeds (chapter 13 says it eventually does) and make success boring: the compromised agent can read only its own tenant's data, call only its own tools, and its every call still passes the chapter 15 approval queue for anything consequential.

**Confused** - the agent is wrong with full confidence. The wall is scope: the confused agent's writes go through the same validation and gates as anyone's, and chapter 27's state discipline pays off here - its corruption is confined to its own stores, replayable from checkpoint, and visible in provenance. Confusion spreads through shared mutable state, so shared state is read-only or versioned, and one agent's canonical record is never silently overwritten by another's.

**Costly** - the agent is a resource fire. The wall is budget enforcement at the runtime layer: per-tenant and per-agent caps on tokens, tool calls, and concurrent turns, enforced by the scheduler (chapter 28) and the gateway (chapter 04) rather than by the agent's good behavior. A loop that never terminates is a supervision problem with a price tag, and chapter 12's cost ledger is how you find out which agent it was.

```python
# Pseudocode: the containment matrix, one row per shared thing.
def audit_blast_radius(runtime, tenant):
    for resource in runtime.shared_resources():
        reach = resource.accessible_by(tenant.agent)
        assert reach <= resource.policy[tenant], \
            f"{resource.name}: {tenant.agent} reaches beyond its policy"
    # And the mirror: what reaches INTO this tenant?
    for other in runtime.tenants - {tenant}:
        assert not tenant.store.readable_by(other.agent)
```

## Isolation granularity is a dial

How much to isolate is an engineering trade, not a principle. Process-per-agent is cheap and weak; container-per-agent is the workhorse; VM-per-tenant is for the genuinely hostile or regulated. Choose per boundary by the cost of the failure it contains, measured against the operational tax of running it - chapter 26's supervision tree already gives you the process inventory to hang the decision on. What is not a dial: tenant data. That wall is load-bearing regardless of what the other boundaries cost.

## Lab: prove the walls

Stand up two tenants on one runtime: shared model gateway, shared scheduler, namespaced stores. Then attack the boundaries. As tenant A's compromised agent, attempt to read tenant B's memory store, call a tool outside its scope, and exceed its token budget; all three must fail with a logged denial. As tenant A's confused agent, write garbage to its own store, then roll back from checkpoint and confirm tenant B never saw it. As tenant A's runaway agent, open a non-terminating turn loop and confirm the scheduler kills it at budget while tenant B's latency stays flat. The deliverable is the containment matrix, green - evidence, not assertion.

## Failure drills

Swap two tenants' credentials in config and check the runtime refuses to start rather than running cross-wired. Fill tenant A's store with a poisoned memory (chapter 13) and trace every place it can surface. Let tenant A's agent exhaust the shared queue and watch whether chapter 03's backpressure protects tenant B or merely queues its death. Restore tenant A from checkpoint after the rollback drill and count what leaked during the window. Each drill names a wall, and the wall either holds or becomes a ticket.

## Ship gate

Every shared resource has a written access policy per tenant, and the containment matrix runs in CI, not in someone's head. Per-agent identity, egress, and budget enforcement live in the runtime layers where those failures travel. Compromise, confusion, and cost each have a demonstrated, not asserted, blast radius. The group's arc is complete: the loop is a process, the process is supervised, its state is chosen, its clock is durable, and its failures are contained. What remains is the question that started all of this - when the agent misbehaves anyway, how do you prove where the fault lives: [the other half of the model](/agentic-eng/chapters/other-half-of-the-model/).
