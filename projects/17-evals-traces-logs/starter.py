from dataclasses import dataclass, field

@dataclass
class Telemetry:
    logs: list = field(default_factory=list)
    spans: list = field(default_factory=list)
    scores: list = field(default_factory=list)

def log_event(tel, task_id, event, **fields):
    """TODO: append a structured event. Reject events without a task id."""
    raise NotImplementedError

def add_span(tel, task_id, name, **fields):
    """TODO: append a trace span keyed by task id."""
    raise NotImplementedError

def score(tel, task_id, grader, value):
    """TODO: attach an eval score to the task."""
    raise NotImplementedError

def why(tel, task_id):
    """TODO: join the three signals for one task into a single report."""
    raise NotImplementedError
