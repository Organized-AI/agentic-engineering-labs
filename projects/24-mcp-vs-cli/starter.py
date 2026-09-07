"""Tool Door Router - implement measure(), route(), and harden()."""
from dataclasses import dataclass, field


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
    """Return a Measurement for driving the capability through the given door."""
    raise NotImplementedError


def route(capability):
    """Return 'script', 'mcp', 'cli', or 'cli_behind_a_wrapper'."""
    raise NotImplementedError


def harden(capability):
    """Lift a repeated, exact capability out of the model into a script."""
    raise NotImplementedError
