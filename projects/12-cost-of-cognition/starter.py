from dataclasses import dataclass

@dataclass(frozen=True)
class Attempt:
    task: str
    automated_cost: float
    review_minutes: float
    accepted: bool

def outcome_cost(attempts: list[Attempt], reviewer_hourly_cost: float) -> dict:
    """TODO: include all attempts and review time; handle zero accepted."""
    raise NotImplementedError

def break_even(fixed_cost: float, managed_unit: float, self_variable_unit: float):
    """TODO: return None when self-hosting has no positive unit advantage."""
    raise NotImplementedError
