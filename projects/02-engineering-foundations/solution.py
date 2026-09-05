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
        self.briefs = {}

    def read(self, principal_tenant: str, event_id: str) -> dict:
        event = self.events.get(event_id)
        if event is None or event.tenant != principal_tenant:
            raise PermissionError("event unavailable")
        return {"id": event.id, "tenant": event.tenant, "venue": event.venue, "version": event.version}

    def make_brief(self, snapshot: dict) -> dict:
        required = {"id", "tenant", "venue", "version"}
        if set(snapshot) != required or type(snapshot["version"]) is not int:
            raise ValueError("invalid snapshot")
        return {
            "event_id": snapshot["id"], "tenant": snapshot["tenant"],
            "venue": snapshot["venue"], "source_version": snapshot["version"],
            "status": "draft",
        }

    def save(self, principal_tenant: str, brief: dict) -> dict:
        required = {"event_id", "tenant", "venue", "source_version", "status"}
        if set(brief) != required or brief["status"] != "draft" or type(brief["source_version"]) is not int:
            raise ValueError("invalid brief")
        event = self.events.get(brief["event_id"])
        if event is None or event.tenant != principal_tenant or brief["tenant"] != principal_tenant:
            raise PermissionError("event unavailable")
        if event.version != brief["source_version"]:
            raise RuntimeError("source version changed")
        if event.venue != brief["venue"]:
            raise ValueError("brief contradicts authoritative venue")
        self.briefs[event.id] = dict(brief)
        return dict(brief)

if __name__ == "__main__":
    service = EventService([Event("event-a", "org-a", "Hall A")])
    snapshot = service.read("org-a", "event-a")
    print(service.save("org-a", service.make_brief(snapshot)))
