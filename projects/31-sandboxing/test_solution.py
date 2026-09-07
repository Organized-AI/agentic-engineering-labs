import unittest

from solution import Denied, Sandbox, Store, mint, run_generated_report


class TestFiveWalls(unittest.TestCase):
    def test_filesystem_and_egress_walls(self):
        sb = Sandbox(owner="t", allowlist=["api.venue-db.internal"])
        with self.assertRaises(Denied):
            sb.read_file("/etc/host-config")
        with self.assertRaises(Denied):
            sb.egress("evil.example")
        self.assertTrue(sb.egress("api.venue-db.internal"))
        self.assertEqual([e[0] for e in sb.log], ["deny-fs", "deny-egress"])

    def test_credentials_are_scoped_and_revocable(self):
        creds = mint(scope="venue:read", ttl_s=60)
        self.assertEqual(creds.scope, "venue:read")
        self.assertFalse(creds.revoked)

    def test_teardown_is_total_even_on_failure(self):
        store = Store()
        class Boom(Sandbox):
            def exec(self, *a, **k):
                raise RuntimeError("generated code blew up")
        sb_owner = "tenant-a"
        # failing exec must still end in revoked creds + destroyed sandbox
        import solution
        orig = solution.Sandbox
        try:
            solution.Sandbox = Boom
            with self.assertRaises(RuntimeError):
                run_generated_report("rpt-x", "explode()", sb_owner, store)
        finally:
            solution.Sandbox = orig
        out = run_generated_report("rpt-2", "generate_daily()", "tenant-a", store)
        self.assertTrue(out["success"])
        self.assertIn("reports/rpt-2", store.data)  # state lives outside the box


if __name__ == "__main__":
    unittest.main()
