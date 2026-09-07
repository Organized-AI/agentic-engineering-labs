"""Turn Loop Harness - reference solution."""

BUDGET = 4096
APPROVED_RECIPIENTS = {"ops-team", "organizer"}


class StubModel:
    def __init__(self, proposals):
        self.proposals = list(proposals)
        self.seen_contexts = []

    def complete(self, context, tools):
        self.seen_contexts.append(context)
        return self.proposals.pop(0) if self.proposals else {"calls": [], "final_text": "done"}


def assemble(messages, budget=BUDGET):
    """Pack messages newest-first until the budget (in chars) is full."""
    packed, total = [], 0
    for msg in reversed(messages):
        if total + len(msg) > budget:
            break
        packed.insert(0, msg)
        total += len(msg)
    return packed


def policy_check(call):
    """The single choke point: every effect passes here."""
    if call.get("name") == "send_brief" and call.get("to") not in APPROVED_RECIPIENTS:
        raise PermissionError(f"unapproved recipient: {call.get('to')}")
    return True


def run_turn(runtime, user_message):
    runtime["log"].append(("turn.start",))
    ctx = assemble(runtime["history"] + [user_message])
    proposal = runtime["model"].complete(ctx, tools=runtime["tools"])
    results = []
    for call in proposal.get("calls", []):
        policy_check(call)
        results.append((call["name"], "ok"))
    runtime["history"].append(user_message)
    runtime["checkpoints"] += 1
    return {"text": proposal.get("final_text", ""), "results": results}


if __name__ == "__main__":
    runtime = {
        "model": StubModel([{"calls": [{"name": "read_calendar"},
                                       {"name": "send_brief", "to": "ops-team"}],
                             "final_text": "Briefing sent."}]),
        "tools": ["read_calendar", "send_brief"],
        "history": ["Earlier context."],
        "log": [],
        "checkpoints": 0,
    }
    print(run_turn(runtime, "Send the morning briefing."))
    print(f"checkpoints: {runtime['checkpoints']}")
