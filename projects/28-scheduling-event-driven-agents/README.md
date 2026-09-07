# 28 — Durable Scheduler

[Read the Scheduling & event-driven agents chapter →](https://guide.organizedai.vip/agentic-eng/chapters/scheduling-event-driven-agents/)

Cron for chores, events for reflexes. Build the scheduler whose timers are
claims, not facts: stored jobs, leases, per-job missed-fire policy, and a
heartbeat the supervisor can watch - plus an event trigger that dedupes
and gates before it spends a wake.

## Run it

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Worked example

A 7:30 briefing job fires three hours late after a restart: its missed-fire
policy says send-with-note. A market-open job in the same situation skips
and logs. The same invite-change event delivered three times wakes the
agent once.

## Challenge

Implement `tick()`, `dedupe()`, and `should_wake()` in `starter.py`. Then
point the tests at the starter. No timer may live only in process memory.

## Extension

Silence the heartbeat and wire the supervisor to page on it - the quietest
failure in the system is a stopped clock.
