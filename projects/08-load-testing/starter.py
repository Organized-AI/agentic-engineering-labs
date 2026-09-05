from dataclasses import dataclass

@dataclass(frozen=True)
class Request:
    arrival: float
    service_time: float
    accepted_quality: bool = True

def percentile(values: list[float], p: float) -> float:
    """TODO: nearest-rank percentile for a non-empty list."""
    raise NotImplementedError

def simulate(requests: list[Request], workers=1, deadline=2.0) -> dict:
    """TODO: assign each arrival to earliest free worker and calculate goodput."""
    raise NotImplementedError
