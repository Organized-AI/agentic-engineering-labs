from dataclasses import dataclass

@dataclass(frozen=True)
class Proposal:
    kind: str
    tool: str | None = None
    args: dict | None = None
    answer: str | None = None

def run_agent(model, tools: dict, principal: str, max_steps=4) -> dict:
    """TODO: execute only authorized tools in a bounded, progress-making loop."""
    raise NotImplementedError
