from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True)
class Trial:
    case: str
    config: str
    accepted: bool
    hard_gate_violation: bool
    cost: float

def compare(trials: list[Trial]) -> dict:
    paired = defaultdict(dict)
    for trial in trials:
        if trial.config not in {"A", "B"}:
            raise ValueError("config must be A or B")
        if trial.config in paired[trial.case]:
            raise ValueError("duplicate config for case")
        paired[trial.case][trial.config] = trial
    if not paired or any(set(pair) != {"A", "B"} for pair in paired.values()):
        raise ValueError("every case needs exactly one A and one B trial")
    counts = {"both": 0, "only_a": 0, "only_b": 0, "neither": 0}
    for pair in paired.values():
        a, b = pair["A"].accepted, pair["B"].accepted
        counts["both" if a and b else "only_a" if a else "only_b" if b else "neither"] += 1
    result = {"cases": len(paired), **counts}
    for config in ("A", "B"):
        rows = [p[config] for p in paired.values()]
        accepted = sum(r.accepted for r in rows)
        result[config.lower()] = {
            "accepted": accepted,
            "hard_gate_violations": sum(r.hard_gate_violation for r in rows),
            "total_cost": round(sum(r.cost for r in rows), 4),
            "cost_per_accepted": None if not accepted else round(sum(r.cost for r in rows) / accepted, 4),
        }
    return result

def decision(report: dict) -> str:
    if report["b"]["hard_gate_violations"]:
        return "reject"
    if report["only_b"] > report["only_a"]:
        return "adopt"
    return "inconclusive"

if __name__ == "__main__":
    sample = [
        Trial("complete", "A", True, False, .04), Trial("complete", "B", True, False, .06),
        Trial("conflict", "A", False, False, .04), Trial("conflict", "B", True, False, .07),
        Trial("private", "A", False, False, .03), Trial("private", "B", False, False, .03),
    ]
    report = compare(sample)
    print(report)
    print("decision:", decision(report))
