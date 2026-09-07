"""Durable Scheduler - reference solution."""
import time
from dataclasses import dataclass, field


@dataclass
class Job:
    name: str
    fire_at: float
    lateness_budget_s: float
    on_missed: str          # "send_with_note" | "skip"
    state: str = "pending"  # pending | leased | ran | skipped
    leased_by: str | None = None
    outcome: str | None = None


class Store:
    def __init__(self):
        self.jobs = []
        self.seen_events = {}
        self.heartbeats = []

    def due(self, now):
        return [j for j in self.jobs if j.state == "pending" and j.fire_at <= now]


def tick(store, now, scheduler_id, effects):
    """Claim due jobs under lease; run or skip per the JOB's missed-fire policy."""
    for job in store.due(now):
        if job.leased_by is not None:
            continue
        job.leased_by = scheduler_id
        job.state = "leased"
        if now > job.fire_at + job.lateness_budget_s:
            if job.on_missed == "skip":
                job.state, job.outcome = "skipped", "missed window"
                continue
            effects.append((job.name, "late-note"))
        else:
            effects.append((job.name, "on-time"))
        job.state, job.outcome = "ran", "ok"
    store.heartbeats.append(now)


def dedupe(store, event_id, window_s=300, now=None):
    now = time.monotonic() if now is None else now
    last = store.seen_events.get(event_id)
    if last is not None and now - last < window_s:
        return False
    store.seen_events[event_id] = now
    return True


def should_wake(event, watch):
    """Cheap binary gate: only a match spends a wake."""
    return (event.get("type") == watch.get("type")
            and event.get("thread") == watch.get("thread"))


if __name__ == "__main__":
    store = Store()
    now = 14 * 3600.0  # 2pm: briefing missed its 6h window, market task way past
    store.jobs = [
        Job("morning-briefing", fire_at=7.5 * 3600, lateness_budget_s=6 * 3600,
            on_missed="send_with_note"),
        Job("market-open", fire_at=8.5 * 3600, lateness_budget_s=300,
            on_missed="skip"),
    ]
    effects = []
    tick(store, now, "scheduler-1", effects)
    print("effects:", effects)
    print("outcomes:", [(j.name, j.state) for j in store.jobs])
    print("wake 1st delivery:", dedupe(store, "evt-1", now=now))
    print("wake 2nd delivery:", dedupe(store, "evt-1", now=now + 1))
