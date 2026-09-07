> **The question:** Your agent's tool server stopped answering an hour ago. How does the runtime know?

Chapter 25 made the loop a process. Processes fail in exactly two ways: they crash, which is loud, or they wedge, which is quiet. A crashed server pages someone. A wedged one accepts connections, never answers, and lets the agent wait forever - or worse, lets it hallucinate around the silence. Supervision is the discipline that makes both failures boring: every long-lived component has a parent that watches it, a health definition it must meet, a restart policy when it doesn't, and a circuit breaker that protects the agent from flapping.

## The mental model

Supervisors, not scripts. The instinct is to bolt health checks onto the agent loop: ping the calendar server before each call, retry on failure. That scatters lifecycle logic through the one place that should never contain it. The runtime instead runs a supervision tree, the pattern Erlang proved decades ago: a supervisor owns each component - the model client, each tool server, the scheduler, the memory store - and the supervisor's only jobs are to watch, restart, and escalate. The agent loop talks to the supervisor's handle, never to the raw process.

The load-bearing insight: supervision separates the failure from the policy. The component fails; the supervisor decides what that means. A dead calendar server might mean restart, might mean degrade to read-only, might mean ask the human. The loop shouldn't know which, and with a tree in place, it doesn't.

## Health is a definition, not a ping

"Is it up?" is the wrong question for agent components, because a server can be up and useless. Health is a contract per component: the model client must complete a trivial call inside its deadline; the calendar server must answer a real read, not just a TCP handshake; the memory store must return a known key. Chapter 8's lesson applies unchanged - measure the useful capacity limit, not the heartbeat. A liveness check that can't fail when the component is useless isn't a check; it's decoration.

Define health budgets the same way: how many consecutive failed checks before the component is declared down, how long a restart may take before escalation, what the agent may safely do while the component is out. That last one matters most. Degraded operation is a designed state - the event assistant without its calendar can still answer questions about past briefings - not an improvised one.

## Restart policy and the circuit breaker

Restarts fix wedged processes so reliably that the temptation is to restart everything, always. The failure mode is the flapping component: crash, restart, crash again, each restart replaying load onto its dependencies. So restarts come with policy: bounded retries with backoff, then the circuit opens. An open breaker is a first-class runtime state the agent can see - "calendar is down, I've stopped trying" - which lets the model route around it honestly instead of timing out per call, per turn, forever.

```python
# Pseudocode: supervision around the calendar tool server.
class Supervisor:
    def call(self, component, request):
        if self.breaker[component].is_open:
            return Degraded(component, reason="circuit open")
        try:
            return component.request(request, timeout=self.deadline(component))
        except (Timeout, Wedged) as fault:
            self.health[component].record_failure(fault)
            if self.health[component].failures >= 3:
                self.restart(component)          # bounded, backed off
                self.breaker[component].trip_if_flapping()
            raise
```

## Graceful shutdown and leases

Supervision cuts both ways: components get killed, and a killed component mid-write corrupts whatever it touches. The contract from chapter 03 returns at the process layer: work is leased, checkpoints are atomic, and shutdown is a sequence - stop accepting turns, drain in-flight calls or park them back on the queue, checkpoint, exit. The supervisor enforces the sequence with a deadline, then escalates from SIGTERM to SIGKILL without guilt. A runtime that can be killed safely at any line of code is the real ship gate; everything else in this chapter is how rarely you need to.

## Lab: supervise a wedged server

Take chapter 25's runtime loop and wrap its calendar tool in a supervisor: a real health check (a known-event read with a 500ms deadline), three-failure restart with exponential backoff, a circuit breaker that opens after three restarts in a minute, and a degraded mode where the agent answers from checkpointed state. Then break it four ways: kill the server, hang it so it accepts but never answers, make it flap, and SIGKILL the supervisor itself mid-restart. The first three must self-heal or degrade honestly; the fourth must come back from checkpoint with the morning briefing sent exactly once.

## Failure drills

Hang the tool server without killing it and time how long the agent takes to notice - that number is your detection latency, and it is probably infinity today. Restart the server underneath an in-flight write and check what the outbox replayed. Open the breaker and confirm the agent tells the user the calendar is down instead of silently guessing. Trip the breaker during the briefing send and count deliveries. Every drill ends in either a clean recovery or a named gap in the tree.

## Ship gate

Every long-lived component runs under a supervisor with a health definition that can fail when the component is useless, a bounded restart policy with backoff, a circuit breaker the agent can read, and a shutdown sequence that checkpoints before it exits. Detection latency for a wedged component is measured and bounded. The tree survives its own supervisor dying. Which raises the question the restart policy keeps dodging: what state was that process holding, and what happens to it on restart - the subject of [state, sessions, and statelessness](/agentic-eng/chapters/state-sessions-statelessness/).
