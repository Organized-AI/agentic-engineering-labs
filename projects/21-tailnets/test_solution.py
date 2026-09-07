import unittest
from solution import load_policy, allows, audit

POLICY = load_policy([
    ("tag:dev-macs", "tag:services", (11434, 22)),
    ("tag:mobile", "tag:services", (8123,)),
])

class MeshTests(unittest.TestCase):
    def test_intended_path_is_allowed(self):
        self.assertTrue(allows(POLICY, ("tag:dev-macs",), "tag:services", 11434))
        self.assertTrue(allows(POLICY, ("tag:mobile",), "tag:services", 8123))

    def test_everything_else_denies_by_default(self):
        self.assertFalse(allows(POLICY, ("tag:mobile",), "tag:services", 22))
        self.assertFalse(allows(POLICY, ("tag:dev-macs",), "tag:services", 8123))
        self.assertFalse(allows(POLICY, ("tag:unknown",), "tag:services", 11434))

    def test_audit_covers_every_path(self):
        devices = {"macbook": ("tag:dev-macs",), "stranger": ("tag:unknown",)}
        services = {"tag:services": (11434, 22)}
        report = audit(POLICY, devices, services)
        self.assertEqual(len(report), 4)
        stranger = [r for r in report if r["device"] == "stranger"]
        self.assertTrue(all(not r["allowed"] for r in stranger))

if __name__ == "__main__": unittest.main()
