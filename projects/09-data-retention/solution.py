from dataclasses import dataclass, field

@dataclass
class Store:
    name: str
    ttl: int | None
    records: list[tuple[int,str]] = field(default_factory=list)

    def write(self, now: int, value: str): self.records.append((now,value))
    def expire(self, now: int):
        if self.ttl is not None:
            self.records=[record for record in self.records if now-record[0] < self.ttl]
    def contains(self, marker: str) -> bool:
        return any(marker in value for _,value in self.records)

def audit(stores: list[Store], marker: str) -> dict:
    if not marker.startswith("SYNTHETIC-"): raise ValueError("use an obvious synthetic marker")
    return {store.name:store.contains(marker) for store in stores}

if __name__ == "__main__":
    marker="SYNTHETIC-CANARY-001"
    stores=[Store("app-log",10),Store("job-store",60),Store("business-record",None)]
    for store in stores: store.write(0,f"request {marker}")
    print("before:",audit(stores,marker))
    for store in stores: store.expire(30)
    print("after 30:",audit(stores,marker))
