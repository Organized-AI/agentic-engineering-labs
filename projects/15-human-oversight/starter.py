from dataclasses import dataclass, field

@dataclass
class Queue:
    requests: dict = field(default_factory=dict)
    decisions: dict = field(default_factory=dict)
    audit: list = field(default_factory=list)
    _next: int = 0

def submit(queue, action, context_hash, now=0, ttl=300):
    """Register a consequential action awaiting approval."""
    queue._next += 1
    rid = f"req-{queue._next}"
    queue.requests[rid] = {"action": action, "hash": context_hash, "expires": now + ttl}
    return rid

def decide(queue, rid, approve, by, now=0):
    """TODO: record a live approval or rejection. Reject expired requests."""
    raise NotImplementedError

def execute(queue, rid, context_hash, effect):
    """TODO: require a live exact approval, audit first, consume the approval."""
    raise NotImplementedError
