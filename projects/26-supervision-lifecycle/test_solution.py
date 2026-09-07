import unittest

from solution import (CircuitOpen, FlakyServer, Supervisor, WedgedServer,
                      health_check)


class TestSupervisorTree(unittest.TestCase):
    def test_health_definition_catches_wedge(self):
        self.assertFalse(health_check(WedgedServer()))
        self.assertTrue(health_check(FlakyServer()))

    def test_bounded_restart_then_breaker(self):
        sup = Supervisor()
        wedged = WedgedServer()
        for _ in range(12):  # 12 failures = 4 restart attempts > limit
            try:
                sup.call("calendar", wedged, {"op": "read"})
            except (TimeoutError, CircuitOpen):
                pass
        self.assertIn("calendar", sup.breakers)
        with self.assertRaises(CircuitOpen):
            sup.call("calendar", wedged, {"op": "read"})

    def test_healthy_server_passes_through(self):
        sup = Supervisor()
        out = sup.call("calendar", FlakyServer(), {"op": "read"})
        self.assertEqual(out["events"], ["standup at 9"])


if __name__ == "__main__":
    unittest.main()
