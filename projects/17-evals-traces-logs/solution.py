from dataclasses import dataclass, field

@dataclass
class Telemetry:
    logs: list = field(default_factory=list)
    spans: list = field(default_factory=list)
    scores: list = field(default_factory=list)

def log_event(tel, task_id, event, **fields):
    """Append a structured event. Events without a task id cannot join, so they fail."""
    if not task_id:
        raise ValueError("log event without a task id cannot join the three signals")
    tel.logs.append({"task_id": task_id, "event": event, **fields})

def add_span(tel, task_id, name, **fields):
    """Append a trace span keyed by task id."""
    if not task_id:
        raise ValueError("span without a task id cannot join the three signals")
    tel.spans.append({"task_id": task_id, "span": name, **fields})

def score(tel, task_id, grader, value):
    """Attach an eval score to the task."""
    if not task_id:
        raise ValueError("score without a task id cannot join the three signals")
    tel.scores.append({"task_id": task_id, "grader": grader, "value": value})

def why(tel, task_id):
    """Join the three signals for one task: what happened, why, and whether it went well."""
    return {
        "task_id": task_id,
        "logs": [e for e in tel.logs if e["task_id"] == task_id],
        "spans": [s for s in tel.spans if s["task_id"] == task_id],
        "scores": [s for s in tel.scores if s["task_id"] == task_id],
    }

if __name__ == "__main__":
    tel = Telemetry()
    log_event(tel, "task-7", "tool.call", tool="send_brief", outcome="ok")
    add_span(tel, "task-7", "model.call", record_version=7, tokens=1180)
    score(tel, "task-7", "brief_correctness", 0.0)
    report = why(tel, "task-7")
    print("WHAT", [e["event"] for e in report["logs"]])
    print("WHY", [(s["span"], s.get("record_version")) for s in report["spans"]])
    print("GOOD", [(s["grader"], s["value"]) for s in report["scores"]])
    try:
        log_event(tel, "", "orphan.event")
    except ValueError as e:
        print("REJECTED orphan log -", e)
