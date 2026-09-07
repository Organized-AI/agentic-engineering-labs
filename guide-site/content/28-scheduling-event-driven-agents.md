> **The question:** Your agent does great work - when someone asks. What wakes it up when nobody does?

So far the runtime has been reactive: a user message arrives, the loop runs. Real agents are not like that. The morning briefing fires at 7:30 whether or not anyone is awake. The inbox watcher should act when mail lands, not when someone remembers to poll. The weekly report is due Friday even if Friday's process restarted Thursday night. Chapter 27 made the runtime safe to leave running; this chapter is about what "running" means between requests - a scheduler with opinions about time, and a trigger layer with opinions about events.

## The mental model

Cron for chores, events for reflexes. The two wake sources have opposite shapes and mixing them up is the classic mistake. Scheduled work is predictable, batched, and tolerant of lateness: briefings, digests, cleanups, reports. Event-driven work is unpredictable, singular, and latency-sensitive: an email arrives, a calendar invite changes, a monitor trips. Cron answers "is it time yet" on a loop; events answer "something happened" once. A briefing built on polling burns tokens checking an empty inbox; a reflex built on a timer either fires late or fires constantly. Choose by the shape of the work, not by which mechanism you set up first.

Both shapes reduce to the same primitive: a wake is a claim that work is due now, and the runtime's job is to turn claims into exactly-once effect - which makes this chapter 03's delivery problem wearing a clock.

## Scheduled work: timers are claims, not facts

A timer does not guarantee a fire; it guarantees at best one fire, possibly late, possibly after a restart that erased it. So durable schedules live in stores (chapter 27's discipline), not in process memory: each job is a row with a fire time, a payload, and a state. The scheduler's loop is embarrassingly small - claim due jobs, lease them (chapter 03), run them, record the outcome - because every hard problem was already solved there. Missed-fire policy is the one genuinely new decision: a briefing that fires three hours late should usually send anyway with a note; a market-open task that fires three hours late should skip and log. That policy belongs to the job, not the scheduler.

```python
# Pseudocode: the scheduler's entire loop.
def tick(scheduler):
    for job in scheduler.store.due(now=clock.now()):
        if not scheduler.lease(job, holder=scheduler.id, ttl=job.deadline):
            continue                        # another scheduler claimed it
        if clock.now() > job.fire_at + job.lateness_budget:
            job.skip(reason="missed window", policy=job.missed_fire_policy)
        else:
            job.run()                       # checkpoints per chapter 25
        scheduler.store.record(job)
```

Heartbeats close the loop: the scheduler itself emits a liveness tick, and chapter 26's supervisor treats a silent scheduler as a wedged one. Otherwise the quietest failure in the system is a clock that stopped - every job healthy, nothing firing.

## Event-driven work: triggers as filters

Events arrive as a firehose and the agent needs a thimble. The trigger layer's job is to turn ten thousand raw events into three wakes worth spending model tokens on: dedupe (the same email delivered twice), match (is this the thread we're watching), and gate (does this event actually change the agent's next action). A trigger with no gate is a polling loop with extra latency.

The pattern that scales: cheap filters in the trigger layer, expensive judgment in the loop. The filter asks binary questions with the event's data - sender, thread, state transition - and only a pass wakes the model. When the wake fires, the runtime assembles context per chapter 25 and the event becomes just another turn, with one addition: the wake carries its provenance (which trigger, which event, why it matched), because an agent acting on an event it can't explain is an agent one prompt injection away from trouble - chapter 13's lesson at the boundary where the outside world pokes the loop.

## Lab: the durable scheduler

Build the event assistant's briefing schedule as a stored job table with leases, a per-job missed-fire policy, and a heartbeat. Add one event trigger: a watcher for calendar-invite changes with a dedupe window and a match filter. Then abuse it. Kill the scheduler before a fire time and restart after: the briefing must recover per its policy, not vanish and not double-send. Fire the same invite-change event three times: the agent must act once. Silence the heartbeat: the supervisor must page. The deliverable is a scheduler whose failures are all in the designed set.

## Failure drills

Stop the clock for an hour and start it: which jobs fire, which skip, and is the difference policy or luck? Deliver the same event from two sources and watch dedupe. Restart between job claim and job completion and count the briefing sends. Feed the trigger an event crafted to make the agent email the wrong list and check whether provenance follows it into the turn. Set the lateness budget to zero and discover which jobs were silently depending on a generous one.

## Ship gate

Every schedule is a stored row with a lease, a missed-fire policy, and a recorded outcome; no timer lives only in process memory. The scheduler heartbeats and its silence is a supervised fault. Every wake carries provenance into the turn. Duplicated events produce single effects, and late fires follow written policy. The agent now runs unattended - which means it runs alongside other agents and other tenants, and that is a containment problem: [isolation and failure containment](/agentic-eng/chapters/isolation-failure-containment/).
