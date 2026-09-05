from dataclasses import dataclass

@dataclass(frozen=True)
class Trial:
    case: str
    config: str
    accepted: bool
    hard_gate_violation: bool
    cost: float

def compare(trials: list[Trial]) -> dict:
    """TODO: produce paired counts and cost per accepted result."""
    raise NotImplementedError

def decision(report: dict) -> str:
    """TODO: reject hard-gate failures; otherwise adopt only with net wins."""
    raise NotImplementedError
