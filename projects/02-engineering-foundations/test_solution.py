import unittest
from solution import Event, EventService

class FoundationsTests(unittest.TestCase):
    def setUp(self):
        self.service = EventService([Event("a", "org-a", "Hall A"), Event("b", "org-b", "Hall B")])

    def test_authorized_vertical_slice(self):
        brief = self.service.make_brief(self.service.read("org-a", "a"))
        self.assertEqual(self.service.save("org-a", brief)["venue"], "Hall A")

    def test_cross_tenant_read_and_write_fail(self):
        with self.assertRaises(PermissionError): self.service.read("org-a", "b")
        forged = {"event_id":"b","tenant":"org-a","venue":"Hall B","source_version":1,"status":"draft"}
        with self.assertRaises(PermissionError): self.service.save("org-a", forged)

    def test_stale_and_false_results_fail(self):
        brief = self.service.make_brief(self.service.read("org-a", "a"))
        self.service.events["a"].version += 1
        with self.assertRaises(RuntimeError): self.service.save("org-a", brief)
        brief["source_version"] = 2; brief["venue"] = "Invented"
        with self.assertRaises(ValueError): self.service.save("org-a", brief)

if __name__ == "__main__": unittest.main()
