"""Containment Matrix - implement check_reach(), mirror_check(), and enforce_budget()."""
from dataclasses import dataclass, field


class Denied(Exception):
    pass


@dataclass
class Resource:
    name: str
    policy: dict          # tenant -> set of allowed capabilities


@dataclass
class Agent:
    tenant: str
    scopes: set
    token_budget: int
    tokens_used: int = 0


def check_reach(agent, resource, capability, log):
    """The agent's reach must stay within its tenant's policy."""
    raise NotImplementedError


def mirror_check(agents, resources):
    """The mirror: what reaches INTO each tenant from outside?"""
    raise NotImplementedError


def enforce_budget(agent, tokens):
    """Costly is a failure mode: budgets bind at the runtime, not the agent."""
    raise NotImplementedError


