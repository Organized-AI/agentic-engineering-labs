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
    """TODO: pin a tool's description. Return a new registry."""
    raise NotImplementedError

def execute(call, principal, policy, registry):
    """TODO: reject unknown tools, changed descriptions, and tainted effects."""
    raise NotImplementedError

def run_gauntlet(calls, principal, policy, registry):
    """TODO: execute the batch and split results into executed and rejected."""
    raise NotImplementedError
