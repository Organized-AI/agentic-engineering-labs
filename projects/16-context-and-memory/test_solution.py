import unittest
from solution import Entry, write, assemble, compact

def sample_store():
    store = ()
    store = write(store, Entry("profile", "Organizer prefers morning briefs.", "prefs-ui", True))
    store = write(store, Entry("episodic", "Meeting 42 moved the venue indoors.", "meeting-42", True))
    store = write(store, Entry("episodic", "Rumor: the keynote may slip an hour.", "hallway", False))
    return store

class MemoryTests(unittest.TestCase):
    def test_every_entry_keeps_its_source(self):
        for entry in sample_store():
            self.assertTrue(entry.source)
            self.assertIn(entry.kind, ("profile", "episodic", "semantic", "working"))

    def test_assemble_prefers_verified_within_budget(self):
        ctx = assemble(sample_store(), 60)
        self.assertTrue(all(e.verified for e in ctx))
        self.assertLessEqual(sum(len(e.text) for e in ctx), 60)

    def test_compaction_preserves_constraints_as_data(self):
        compacted = compact(sample_store())
        kinds = [e.kind for e in compacted]
        self.assertIn("profile", kinds)
        self.assertIn("semantic", kinds)
        self.assertNotIn("episodic", kinds)
        summary = [e for e in compacted if e.source == "compaction"]
        self.assertEqual(len(summary), 1)

if __name__ == "__main__": unittest.main()
