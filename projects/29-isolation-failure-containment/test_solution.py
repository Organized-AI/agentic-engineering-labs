import unittest

from solution import Agent, Denied, Resource, check_reach, enforce_budget, mirror_check


class TestContainmentMatrix(unittest.TestCase):
    def setUp(self):
        self.store_b = Resource("store-b", policy={"tenant-b": {"read", "write"}})
        self.tools = Resource("calendar", policy={"tenant-a": {"read"}})
        self.agent_a = Agent("tenant-a", scopes={"read", "write"}, token_budget=100)
        self.log = []

    def test_compromised_agent_hits_the_wall(self):
        with self.assertRaises(Denied):  # read tenant B's store
            check_reach(self.agent_a, self.store_b, "read", self.log)
        with self.assertRaises(Denied):  # tool outside tenant policy
            check_reach(self.agent_a, self.tools, "write", self.log)
        self.assertEqual([e[0] for e in self.log], ["deny", "deny"])

    def test_costly_agent_hits_the_budget(self):
        enforce_budget(self.agent_a, 60)
        with self.assertRaises(Denied):
            enforce_budget(self.agent_a, 60)
        self.assertEqual(self.agent_a.tokens_used, 60)

    def test_mirror_check_finds_inbound_gaps(self):
        orphan = Resource("orphan-store", policy={})  # no tenant policy at all
        violations = mirror_check([self.agent_a], [self.tools, orphan])
        self.assertEqual(violations, [(self.agent_a.tenant, "orphan-store")])
        self.assertEqual(mirror_check([self.agent_a], [self.tools]), [])


if __name__ == "__main__":
    unittest.main()
