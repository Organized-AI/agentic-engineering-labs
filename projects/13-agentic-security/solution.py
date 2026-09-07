from dataclasses import dataclass

@dataclass(frozen=True)
class Tool:
    name: str
    has_effect: bool
    hosts: tuple = ()

@dataclass(frozen=True)
class Call:
    tool: str
    args: tuple = ()
    from_untrusted: bool = False

def make_policy(**capabilities):
    """make_policy(org_a=(Tool(...), ...)) -> {principal: {tool_name: Tool}}"""
    return {principal: {tool.name: tool for tool in tools} for principal, tools in capabilities.items()}

def approve_tool(registry, tool, description):
    """Pin a tool's description. Returns a new registry."""
    return {**registry, tool.name: (tool, description)}

def execute(call, principal, policy, registry):
    tools = policy.get(principal, {})
    if call.tool not in tools:
        return {"status": "reject", "reason": "outside granted capability", "call": call}
    tool = tools[call.tool]
    approved = registry.get(call.tool)
    if approved is None or approved[0] != tool:
        return {"status": "reject", "reason": "tool description changed since approval", "call": call}
    if call.from_untrusted and tool.has_effect:
        return {"status": "reject", "reason": "untrusted input cannot trigger effects", "call": call}
    return {"status": "executed", "tool": tool.name, "call": call}

def run_gauntlet(calls, principal, policy, registry):
    results = [execute(call, principal, policy, registry) for call in calls]
    return {
        "executed": [r for r in results if r["status"] == "executed"],
        "rejected": [r for r in results if r["status"] == "reject"],
    }

if __name__ == "__main__":
    read_events = Tool("read_events", False, ("events.internal",))
    send_email = Tool("send_email", True, ("mail.internal",))
    policy = make_policy(organizer=(read_events, send_email))
    registry = approve_tool(approve_tool({}, read_events, "Read approved events."), send_email, "Send one brief.")
    calls = [
        Call("read_events", ("event-1",), from_untrusted=True),
        Call("send_email", ("attendees@example.com",), from_untrusted=True),
        Call("send_email", ("organizer@example.com",), from_untrusted=False),
    ]
    report = run_gauntlet(calls, "organizer", policy, registry)
    for r in report["executed"]:
        print("EXECUTED", r["tool"], r["call"].args)
    for r in report["rejected"]:
        print("REJECTED", r["call"].tool, "-", r["reason"])
