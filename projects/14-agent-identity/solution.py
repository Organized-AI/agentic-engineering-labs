from dataclasses import dataclass

@dataclass(frozen=True)
class Token:
    subject: str       # the user the agent acts for; "" means machine-only
    audience: str      # the one tool this token may call
    scope: str         # e.g. "event:write"
    actor: str         # the workload identity of the agent itself

def issue_service_token(actor):
    """A machine credential with no subject. Never sufficient alone."""
    return Token("", "service", "service:run", actor)

def exchange(user_token, audience, scope, actor):
    """Trade a user token for an audience-scoped token, keeping the subject."""
    if not user_token.subject:
        raise ValueError("cannot delegate a token with no subject")
    return Token(user_token.subject, audience, scope, actor)

def call(tool, required_scope, token):
    if not token.actor:
        return {"status": "reject", "reason": "no workload identity on the call"}
    if not token.subject:
        return {"status": "reject", "reason": "user-scoped effect needs a subject"}
    if token.audience != tool:
        return {"status": "reject", "reason": f"token audience is {token.audience}, not {tool}"}
    if token.scope != required_scope:
        return {"status": "reject", "reason": f"missing scope {required_scope}"}
    return {"status": "executed", "tool": tool, "subject": token.subject, "actor": token.actor}

if __name__ == "__main__":
    user = Token("jordan", "auth", "user:full", "user-session")
    calendar = exchange(user, "calendar", "event:write", "agent-worker-1")
    service = issue_service_token("agent-worker-1")
    for label, tool, scope, token in [
        ("scoped call", "calendar", "event:write", calendar),
        ("wrong audience", "billing", "billing:charge", calendar),
        ("service account", "calendar", "event:write", service),
    ]:
        result = call(tool, scope, token)
        if result["status"] == "executed":
            print("EXECUTED", result["tool"], "as", result["subject"], "via", result["actor"])
        else:
            print("REJECTED", label, "-", result["reason"])
