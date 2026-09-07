import unittest

from solution import Runtime, StateEntry, StateLeak, Store, audit, kill_and_resume


class TestStateAuditor(unittest.TestCase):
    def test_homeless_state_is_a_finding(self):
        entries = [StateEntry("recipient_list", None, owner="nobody")]
        with self.assertRaises(StateLeak):
            audit(entries)

    def test_each_home_enforces_its_contract(self):
        with self.assertRaises(StateLeak):
            audit([StateEntry("ctx", "context", rebuildable_from_stores=False)])
        with self.assertRaises(StateLeak):
            audit([StateEntry("sess", "session", has_rebuild_path=False)])
        with self.assertRaises(StateLeak):
            audit([StateEntry("ckpt", "stores", atomic_write=False)])
        self.assertTrue(audit([StateEntry("ok", "stores", atomic_write=True)]))

    def test_kill_between_any_two_lines(self):
        store = Store()
        Runtime(store).run_step("assemble")          # "process" dies here
        steps = kill_and_resume(store, ["call_model", "checkpoint"])
        self.assertEqual(steps, ["assemble", "call_model", "checkpoint"])


if __name__ == "__main__":
    unittest.main()
