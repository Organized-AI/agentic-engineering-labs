from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Request:
    arrival: float
    service_time: float
    accepted_quality: bool = True

def percentile(values: list[float], p: float) -> float:
    if not values or not 0 < p <= 1: raise ValueError("non-empty values and p in (0,1]")
    values=sorted(values); return values[math.ceil(p*len(values))-1]

def simulate(requests: list[Request], workers=1, deadline=2.0) -> dict:
    if workers < 1 or deadline <= 0: raise ValueError("invalid capacity")
    free=[0.0]*workers; rows=[]
    for request in sorted(requests,key=lambda r:r.arrival):
        index=min(range(workers),key=free.__getitem__)
        start=max(request.arrival,free[index]); finish=start+request.service_time; free[index]=finish
        latency=finish-request.arrival; accepted=request.accepted_quality and latency <= deadline
        rows.append({"arrival":request.arrival,"queue":start-request.arrival,"latency":latency,"accepted":accepted})
    duration=max((r["arrival"]+r["latency"] for r in rows),default=0)
    accepted=sum(r["accepted"] for r in rows)
    return {"attempted":len(rows),"accepted":accepted,"duration":duration,"goodput":0 if not duration else accepted/duration,"p50":percentile([r["latency"] for r in rows],.5) if rows else 0,"p95":percentile([r["latency"] for r in rows],.95) if rows else 0,"rows":rows}

if __name__ == "__main__":
    for gap in (.8,.4,.2):
        requests=[Request(i*gap,.5) for i in range(20)]
        report=simulate(requests,workers=2,deadline=1.5)
        print({"gap":gap,"goodput":round(report["goodput"],2),"p95":round(report["p95"],2)})
