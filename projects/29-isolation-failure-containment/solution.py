"""Containment Matrix - reference solution."""
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
    allowed = resource.policy.get(agent.tenant, set())
    if capability not in allowed or capability not in agent.scopes:
        log.append(("deny", agent.tenant, resource.name, capability))
        raise Denied(f"{agent.tenant} cannot {capability} on {resource.name}")
    log.append(("allow", agent.tenant, resource.name, capability))
    return True


def mirror_check(agents, resources):
    """The mirror: what reaches INTO each tenant from outside?"""
    violations = []
    for agent in agents:
        for resource in resources:
            if resource.policy.get(agent.tenant) is None:
                violations.append((agent.tenant, resource.name))
    return violations


def enforce_budget(agent, tokens):
    """Costly is a failure mode: budgets bind at the runtime, not the agent."""
    if agent.tokens_used + tokens > agent.token_budget:
        raise Denied(f"{agent.tenant}: token budget exceeded")
    agent.tokens_used += tokens
    return agent.tokens_used


if __name__ == "__main__":
    store_b = Resource("store-b", policy={"tenant-b": {"read", "write"}})
    tools = Resource("calendar", policy={"tenant-a": {"read"}, "tenant-b": {"read", "write"}})
    agent_a = Agent("tenant-a", scopes={"read"}, token_budget=1000)
    log = []
    for cap, res in [("read", store_b), ("write", tools)]:
        try:
            check_reach(agent_a, res, cap, log)
        except Denied as e:
            print("denied:", e)
    try:
        enforce_budget(agent_a, 1500)
    except Denied as e:
        print("denied:", e)
    print("log:", log)
