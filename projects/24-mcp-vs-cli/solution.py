"""Tool Door Router - reference solution."""
from dataclasses import dataclass


@dataclass
class Capability:
    name: str
    needs_session: bool = False
    has_complex_schema: bool = False
    already_installed: bool = True
    composes_with_pipes: bool = True
    repeated: bool = False
    exact: bool = False


@dataclass
class Measurement:
    door: str
    discovery_tokens: int = 0
    validation_catches: int = 0


class StatelessMcpServer:
    """A minimal MCP server with no session state. Each request stands alone."""

    def __init__(self, tools):
        self.tools = tools  # {name: schema}

    def handle(self, request):
        method = request.get("method")
        if method == "initialize":
            # Deliberately no Mcp-Session-Id: this server is stateless.
            return {"protocolVersion": "2025-06-18", "session": None}
        if method == "tools/list":
            return {"tools": [{"name": n, "schema": s} for n, s in self.tools.items()]}
        if method == "tools/call":
            name = request.get("name")
            if name not in self.tools:
                return {"error": "unknown tool"}
            return {"result": f"called {name}"}
        return {"error": "unknown method"}


def measure(capability, door, *, schema_tokens=0, help_tokens=0, bad_calls=0):
    """Measure discovery cost and validation strength for one door.

    MCP pays schema tokens once per `tools/list`; the CLI pays exploration
    tokens per capability. MCP schemas reject malformed calls before
    execution; the CLI discovers bad flags only at runtime.
    """
    if door == "mcp":
        return Measurement(door, discovery_tokens=schema_tokens,
                           validation_catches=bad_calls)
    if door == "cli":
        return Measurement(door, discovery_tokens=help_tokens,
                           validation_catches=0)
    raise ValueError(f"unknown door: {door}")


def route(capability):
    """The chapter's routing question, asked per capability."""
    if capability.repeated and capability.exact:
        return "script"
    if capability.needs_session or capability.has_complex_schema:
        return "mcp"
    if capability.already_installed and capability.composes_with_pipes:
        return "cli"
    return "cli_behind_a_wrapper"


def harden(capability):
    """Lift a repeated, exact capability out of the model into a script."""
    if not (capability.repeated and capability.exact):
        raise ValueError("only repeated, exact work leaves the model")
    return f"scripts/{capability.name}.sh"


if __name__ == "__main__":
    calendar = Capability("calendar", has_complex_schema=True)
    server = StatelessMcpServer({"list_events": {"type": "object"},
                                 "create_event": {"type": "object"}})
    print(server.handle({"method": "initialize"}))
    print(server.handle({"method": "tools/list"}))
    mcp = measure(calendar, "mcp", schema_tokens=400, bad_calls=2)
    cli = measure(calendar, "cli", help_tokens=3000, bad_calls=2)
    print(f"mcp: {mcp.discovery_tokens} discovery tokens, "
          f"{mcp.validation_catches} validation catches")
    print(f"cli: {cli.discovery_tokens} discovery tokens, "
          f"{cli.validation_catches} validation catches")
    brief = Capability("daily-brief", repeated=True, exact=True)
    print(f"{brief.name} routes to: {route(brief)} -> {harden(brief)}")
