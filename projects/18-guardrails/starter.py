def rail(name, fn):
    """A named guardrail. fn(call_text) returns True to allow, False to deny."""
    return {"name": name, "fn": fn}

def run(call_text, rails, clock=lambda: 0.0):
    """TODO: pass the call through each rail in order.

    Return {"decision": "allow"|"deny", "reasons": [...], "latency_ms": N}.
    A rail that returns False denies with its name as the reason.
    A rail that raises denies too: fail closed, never skip.
    """
    raise NotImplementedError
