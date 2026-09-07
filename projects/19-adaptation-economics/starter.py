from dataclasses import dataclass

@dataclass(frozen=True)
class Option:
    name: str
    accepted: int        # accepted outcomes in the trial
    attempted: int       # total trial tasks
    variable_cost: float # dollars per accepted outcome (tokens, retrieval)
    fixed_cost: float    # one-time cost (training, setup), amortized over volume
    review_minutes: float # human review minutes per accepted outcome

def cost_per_accepted(option, volume, reviewer_hourly=60):
    """TODO: total dollars per accepted outcome at the given monthly volume."""
    raise NotImplementedError

def price(options, volume=1000, reviewer_hourly=60):
    """TODO: score every option and return a dated comparison report."""
    raise NotImplementedError

def winner(report, minimum_accept_rate=0.80):
    """TODO: cheapest option that clears the quality bar. None may be the answer."""
    raise NotImplementedError
