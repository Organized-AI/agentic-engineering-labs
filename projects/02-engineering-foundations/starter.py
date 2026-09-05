from dataclasses import dataclass

@dataclass
class Event:
    id: str
    tenant: str
    venue: str
    version: int = 1

class EventService:
    def __init__(self, events: list[Event]):
        self.events = {e.id: e for e in events}

    def read(self, principal_tenant: str, event_id: str) -> dict:
        """TODO: return only an event in the principal's tenant."""
        raise NotImplementedError

    def make_brief(self, snapshot: dict) -> dict:
        """TODO: produce a source-backed deterministic brief."""
        raise NotImplementedError

    def save(self, principal_tenant: str, brief: dict) -> dict:
        """TODO: validate shape, tenant, fact, and source version."""
        raise NotImplementedError
