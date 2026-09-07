import unittest

from solution import FaultyEndpoint, Signals, diagnose, probe_full_loop


class TestAttributionBench(unittest.TestCase):
    def test_null_result_names_the_serving_stack(self):
        # McNamara's case: decode +43%, KV pool 3.75x, prefill flat.
        s = Signals(6266, 6249, 112.0, 160.0, True, True, "model-a", "model-a")
        self.assertEqual(diagnose(s), "serving stack")
        both_moved = Signals(6266, 6900, 112.0, 160.0, True, True, "model-a", "model-a")
        self.assertNotEqual(diagnose(both_moved), "serving stack")

    def test_silent_swap_and_harness_fault(self):
        swap = Signals(6266, 6260, 112.0, 113.0, True, True, "model-b", "model-a")
        self.assertEqual(diagnose(swap), "silent model swap")
        harness = Signals(6266, 6260, 112.0, 113.0, True, False, "model-a", "model-a")
        self.assertEqual(diagnose(harness), "harness")

    def test_endpoint_lies_full_loop_tells(self):
        ep = FaultyEndpoint(plant_fault=True)
        self.assertEqual(ep.health()["status"], "ok")       # cheap check passes
        probe = probe_full_loop(ep, [{"name": "read_prompt"}, {"name": "tool_calendar"}])
        self.assertFalse(probe["ok"])
        self.assertEqual(probe["failed_at"], "tool_calendar")


if __name__ == "__main__":
    unittest.main()
