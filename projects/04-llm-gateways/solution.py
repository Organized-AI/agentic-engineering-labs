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
        if amount < 0 or amount > self.available: raise RuntimeError("budget exceeded")
        self.available = round(self.available-amount, 10)

def route(prompt: str, data_class: str, endpoints: list[Endpoint], budget: Budget) -> dict:
    eligible=[e for e in endpoints if data_class in e.data_classes]
    if not eligible: raise PermissionError("no policy-eligible endpoint")
    errors=[]
    for endpoint in eligible[:2]:
        try:
            budget.reserve(endpoint.estimated_cost)
            response=endpoint.call(prompt)
            if set(response) != {"brief","endpoint"}: raise ValueError("schema violation")
            return {**response,"attempts":len(errors)+1}
        except (TimeoutError, ValueError) as error:
            errors.append(type(error).__name__)
    raise RuntimeError("all eligible routes failed: "+", ".join(errors))

if __name__ == "__main__":
    endpoints=[Endpoint("primary",{"internal"},.04,"timeout"),Endpoint("fallback",{"internal"},.06)]
    print(route("event brief", "internal", endpoints, Budget(.20)))
