from dataclasses import dataclass

@dataclass(frozen=True)
class Fact:
    subject: str
    predicate: str
    value: str
    source: str
    approved: bool
    valid_from: int
    valid_to: int | None = None

def _current(fact: Fact, at_time: int) -> bool:
    return fact.approved and fact.valid_from <= at_time and (fact.valid_to is None or at_time < fact.valid_to)

def resolve_venue(event_id: str, tenant: str, event_tenants: dict, facts: list[Fact], at_time: int) -> dict:
    if event_tenants.get(event_id) != tenant: raise PermissionError("event unavailable")
    links=[f for f in facts if f.subject==event_id and f.predicate=="takesPlaceAt" and _current(f,at_time)]
    if len(links) != 1: raise ValueError("event needs one current approved venue link")
    venue_id=links[0].value
    labels=[f for f in facts if f.subject==venue_id and f.predicate=="label" and _current(f,at_time)]
    if len(labels) != 1: raise ValueError("venue needs one current approved label")
    return {"venue_id":venue_id,"label":labels[0].value,"link_source":links[0].source,"label_source":labels[0].source}

if __name__ == "__main__":
    facts=[Fact("event-a","takesPlaceAt","venue-1","event-record",True,0),Fact("venue-1","label","Hall A","venue-record",True,0)]
    print(resolve_venue("event-a","org-a",{"event-a":"org-a"},facts,10))
