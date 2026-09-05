from dataclasses import dataclass, field

@dataclass
class Store:
    name: str
    ttl: int | None
    records: list[tuple[int,str]] = field(default_factory=list)

    def write(self, now: int, value: str): self.records.append((now,value))
    def expire(self, now: int):
        """TODO: remove records older than the TTL; None means retained."""
        raise NotImplementedError
    def contains(self, marker: str) -> bool:
        """TODO: search the store without changing it."""
        raise NotImplementedError

def audit(stores: list[Store], marker: str) -> dict:
    """TODO: return names that contain the synthetic marker."""
    raise NotImplementedError
