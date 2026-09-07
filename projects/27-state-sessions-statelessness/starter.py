"""State Auditor - implement audit() and kill_and_resume()."""
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
    raise NotImplementedError


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
    raise NotImplementedError


