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
    """TODO: trade a user token for an audience-scoped token, keeping the subject."""
    raise NotImplementedError

def call(tool, required_scope, token):
    """TODO: reject missing subjects, wrong audiences, and missing scopes."""
    raise NotImplementedError
