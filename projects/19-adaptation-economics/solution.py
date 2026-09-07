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
    """Total dollars per accepted outcome: variable + amortized fixed + review time."""
    review_cost = (option.review_minutes / 60) * reviewer_hourly
    return option.variable_cost + option.fixed_cost / volume + review_cost

def price(options, volume=1000, reviewer_hourly=60):
    """Score every option and return a dated, rerunnable comparison."""
    return {
        "volume": volume,
        "reviewer_hourly": reviewer_hourly,
        "options": [{
            "name": o.name,
            "accept_rate": o.accepted / o.attempted,
            "cost_per_accepted": cost_per_accepted(o, volume, reviewer_hourly),
        } for o in options],
    }

def winner(report, minimum_accept_rate=0.80):
    """Cheapest option that clears the quality bar; None if nothing does."""
    eligible = [o for o in report["options"] if o["accept_rate"] >= minimum_accept_rate]
    if not eligible:
        return None
    return min(eligible, key=lambda o: o["cost_per_accepted"])["name"]

if __name__ == "__main__":
    options = [
        Option("prompt-v2", accepted=24, attempted=30, variable_cost=0.04, fixed_cost=0, review_minutes=1.0),
        Option("rag-pack", accepted=27, attempted=30, variable_cost=0.09, fixed_cost=200, review_minutes=0.5),
        Option("fine-tune", accepted=29, attempted=30, variable_cost=0.02, fixed_cost=4000, review_minutes=0.25),
    ]
    report = price(options, volume=1000)
    for row in report["options"]:
        print(f"{row['name']:10s} accept={row['accept_rate']:.2f} cost/accepted=${row['cost_per_accepted']:.3f}")
    print("WINNER", winner(report))
