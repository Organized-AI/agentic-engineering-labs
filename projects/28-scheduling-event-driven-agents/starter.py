"""Durable Scheduler - implement tick(), dedupe(), and should_wake()."""
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
    raise NotImplementedError


def dedupe(store, event_id, window_s=300, now=None):
    raise NotImplementedError


def should_wake(event, watch):
    """Cheap binary gate: only a match spends a wake."""
    raise NotImplementedError


