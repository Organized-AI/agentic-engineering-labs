"""State Auditor - reference solution."""
from dataclasses import dataclass, field


@dataclass
class StateEntry:
    name: str
    home: str | None          # "context" | "session" | "stores" | None
    owner: str = ""
    lifetime: str = ""
    rebuildable_from_stores: bool = False
    has_rebuild_path: bool = False
    atomic_write: bool = False


class StateLeak(Exception):
    pass


def audit(entries):
    """Every entry must name a home with the properties that home requires."""
    leaks = []
    for e in entries:
        if e.home is None:
            leaks.append(e.name)
        elif e.home == "context" and not e.rebuildable_from_stores:
            leaks.append(f"{e.name}: context not rebuildable")
        elif e.home == "session" and not e.has_rebuild_path:
            leaks.append(f"{e.name}: session has no rebuild path")
        elif e.home == "stores" and not e.atomic_write:
            leaks.append(f"{e.name}: store writes not atomic")
    if leaks:
        raise StateLeak(", ".join(leaks))
    return True


class Store:
    def __init__(self):
        self.data = {}

    def write(self, key, value):
        self.data[key] = value


class Runtime:
    """A runtime whose turn state lives in stores, not in process memory."""

    def __init__(self, store):
        self.store = store

    def run_step(self, step):
        steps = self.store.data.get("steps", [])
        steps.append(step)
        self.store.write("steps", steps)
        return len(steps)


def kill_and_resume(store, remaining_steps):
    """Fresh 'process': reconstruct from stores and finish the turn."""
    runtime = Runtime(store)          # new process, same store
    for step in remaining_steps:
        runtime.run_step(step)
    return runtime.store.data["steps"]


if __name__ == "__main__":
    good = [
        StateEntry("transcript", "context", owner="runtime", lifetime="turn",
                   rebuildable_from_stores=True),
        StateEntry("calendar_session", "session", owner="calendar-supervisor",
                   lifetime="connection", has_rebuild_path=True),
        StateEntry("checkpoints", "stores", owner="runtime", lifetime="forever",
                   atomic_write=True),
    ]
    print("audit clean:", audit(good))
    store = Store()
    Runtime(store).run_step("assemble")
    print("resumed:", kill_and_resume(store, ["call_model", "checkpoint"]))
