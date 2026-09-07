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
    """Record a live approval or rejection. Expired requests can only be rejected."""
    req = queue.requests[rid]
    if rid in queue.decisions:
        raise ValueError("request already decided")
    approved = approve and now <= req["expires"]
    queue.decisions[rid] = {"approved": approved, "by": by, "consumed": False}
    return queue.decisions[rid]

def execute(queue, rid, context_hash, effect):
    """Require a live exact approval, audit first, then consume the approval."""
    decision = queue.decisions.get(rid)
    if decision is None or not decision["approved"]:
        raise PermissionError("no approval on record")
    if decision["consumed"]:
        raise PermissionError("approval already consumed")
    req = queue.requests[rid]
    if context_hash != req["hash"]:
        raise PermissionError("context changed since approval")
    queue.audit.append({"rid": rid, "action": req["action"], "by": decision["by"]})
    decision["consumed"] = True
    return effect()

if __name__ == "__main__":
    queue = Queue()
    rid = submit(queue, "send_brief", "hash:brief-v7", now=0)
    decide(queue, rid, approve=True, by="organizer", now=10)
    print("EXECUTED", execute(queue, rid, "hash:brief-v7", lambda: "brief sent"))
    for label, fn in [
        ("replay", lambda: execute(queue, rid, "hash:brief-v7", lambda: "brief sent again")),
        ("doctored", lambda: execute(queue, submit(queue, "send_brief", "hash:brief-v8", now=20), "hash:brief-DOCTORED", lambda: "doctored sent")),
    ]:
        try:
            fn()
            print("FAIL", label, "executed")
        except PermissionError as e:
            print("REJECTED", label, "-", e)
    print("AUDIT", queue.audit)
