import unittest

from solution import StubModel, assemble, policy_check, run_turn


class TestTurnLoop(unittest.TestCase):
    def test_assemble_enforces_budget(self):
        messages = ["x" * 3000, "y" * 3000, "z" * 100]
        ctx = assemble(messages, budget=4096)
        self.assertEqual(sum(len(m) for m in ctx), 3100)
        self.assertEqual(ctx[-1], "z" * 100)  # newest survives eviction

    def test_policy_choke_point(self):
        with self.assertRaises(PermissionError):
            policy_check({"name": "send_brief", "to": "ops-tean"})
        self.assertTrue(policy_check({"name": "send_brief", "to": "ops-team"}))

    def test_turn_with_stub_model(self):
        model = StubModel([{"calls": [{"name": "read_calendar"}], "final_text": "ok"}])
        runtime = {"model": model, "tools": ["read_calendar"],
                   "history": ["old"], "log": [], "checkpoints": 0}
        out = run_turn(runtime, "hi")
        self.assertEqual(out["results"], [("read_calendar", "ok")])
        self.assertEqual(runtime["checkpoints"], 1)


if __name__ == "__main__":
    unittest.main()
