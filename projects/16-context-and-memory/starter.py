from dataclasses import dataclass

@dataclass(frozen=True)
class Entry:
    kind: str        # profile | episodic | semantic | working
    text: str
    source: str
    verified: bool = False

def write(store, entry):
    """Append an entry. Provenance travels with the memory."""
    return store + (entry,)

def assemble(store, budget):
    """TODO: fill the budget (in characters) with verified entries first."""
    raise NotImplementedError

def compact(store, keep_kinds=("profile", "semantic")):
    """TODO: summarize episodic entries, keep constraints and open loops as data."""
    raise NotImplementedError
