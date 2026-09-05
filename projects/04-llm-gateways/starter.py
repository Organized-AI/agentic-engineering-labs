from dataclasses import dataclass

@dataclass
class Endpoint:
    name: str
    data_classes: set[str]
    estimated_cost: float
    behavior: str = "ok"
    calls: int = 0

    def call(self, prompt: str) -> dict:
        self.calls += 1
        if self.behavior == "timeout": raise TimeoutError(self.name)
        if self.behavior == "malformed": return {"wrong": True}
        return {"brief": prompt.upper(), "endpoint": self.name}

class Budget:
    def __init__(self, available: float): self.available=available
    def reserve(self, amount: float):
        """TODO: reject an amount greater than the remaining budget."""
        raise NotImplementedError

def route(prompt: str, data_class: str, endpoints: list[Endpoint], budget: Budget) -> dict:
    """TODO: filter by policy, reserve before calls, and use bounded fallback."""
    raise NotImplementedError
