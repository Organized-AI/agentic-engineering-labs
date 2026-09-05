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

def resolve_venue(event_id: str, tenant: str, event_tenants: dict, facts: list[Fact], at_time: int) -> dict:
    """TODO: authorize, follow takesPlaceAt, and return current approved provenance."""
    raise NotImplementedError
