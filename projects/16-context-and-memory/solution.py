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
    """Fill the budget (in characters) with verified entries first."""
    ordered = sorted(store, key=lambda e: (not e.verified, e.kind != "profile"))
    picked, used = [], 0
    for entry in ordered:
        if used + len(entry.text) > budget:
            continue
        picked.append(entry)
        used += len(entry.text)
    return picked

def compact(store, keep_kinds=("profile", "semantic")):
    """Summarize episodic entries; constraints and open loops survive as data."""
    kept = [e for e in store if e.kind in keep_kinds]
    episodes = [e for e in store if e.kind == "episodic"]
    if episodes:
        summary = Entry("semantic",
                        f"Summary of {len(episodes)} episodes: " + "; ".join(e.text[:40] for e in episodes),
                        "compaction", verified=True)
        kept.append(summary)
    return tuple(kept)

if __name__ == "__main__":
    store = ()
    store = write(store, Entry("profile", "Organizer prefers morning briefs.", "prefs-ui", True))
    store = write(store, Entry("episodic", "Meeting 42 moved the venue indoors.", "meeting-42", True))
    store = write(store, Entry("semantic", "Catering never confirmed by email alone.", "postmortem-3", True))
    store = write(store, Entry("episodic", "Rumor: the keynote may slip an hour.", "hallway", False))
    ctx = assemble(store, 60)
    print("CONTEXT", [e.kind for e in ctx])
    smaller = compact(store)
    print("COMPACTED", [(e.kind, e.source) for e in smaller])
