from dataclasses import dataclass

@dataclass(frozen=True)
class Attempt:
    task: str
    automated_cost: float
    review_minutes: float
    accepted: bool

def outcome_cost(attempts: list[Attempt], reviewer_hourly_cost: float) -> dict:
    if reviewer_hourly_cost < 0 or any(a.automated_cost < 0 or a.review_minutes < 0 for a in attempts): raise ValueError("costs cannot be negative")
    total=sum(a.automated_cost+a.review_minutes/60*reviewer_hourly_cost for a in attempts)
    accepted=sum(a.accepted for a in attempts)
    return {"attempts":len(attempts),"accepted":accepted,"total_cost":round(total,4),"cost_per_accepted":None if not accepted else round(total/accepted,4)}

def break_even(fixed_cost: float, managed_unit: float, self_variable_unit: float):
    if min(fixed_cost,managed_unit,self_variable_unit) < 0: raise ValueError("costs cannot be negative")
    advantage=managed_unit-self_variable_unit
    return None if advantage <= 0 else fixed_cost/advantage

if __name__ == "__main__":
    attempts=[Attempt("a",.20,1,True),Attempt("b",.10,3,False),Attempt("b-retry",.25,1,True)]
    print(outcome_cost(attempts,60)); print("break-even:",break_even(2000,.05,.01))
