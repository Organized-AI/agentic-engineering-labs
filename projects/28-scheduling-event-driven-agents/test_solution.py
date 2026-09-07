import unittest

from solution import Job, Store, dedupe, should_wake, tick


class TestDurableScheduler(unittest.TestCase):
    def test_missed_fire_policy_belongs_to_the_job(self):
        store = Store()
        now = 14 * 3600.0
        store.jobs = [
            Job("briefing", fire_at=7.5 * 3600, lateness_budget_s=6 * 3600,
                on_missed="send_with_note"),
            Job("market-open", fire_at=8.5 * 3600, lateness_budget_s=300,
                on_missed="skip"),
        ]
        effects = []
        tick(store, now, "s1", effects)
        self.assertEqual(effects, [("briefing", "late-note")])
        self.assertEqual(store.jobs[1].state, "skipped")
        self.assertEqual(len(store.heartbeats), 1)

    def test_duplicate_events_wake_once(self):
        store = Store()
        self.assertTrue(dedupe(store, "evt-1", now=100.0))
        self.assertFalse(dedupe(store, "evt-1", now=101.0))
        self.assertTrue(dedupe(store, "evt-1", now=1000.0))  # outside window

    def test_trigger_gates_before_spending_a_wake(self):
        watch = {"type": "invite-change", "thread": "thread-42"}
        self.assertTrue(should_wake({"type": "invite-change", "thread": "thread-42"}, watch))
        self.assertFalse(should_wake({"type": "invite-change", "thread": "other"}, watch))
        self.assertFalse(should_wake({"type": "newsletter", "thread": "thread-42"}, watch))


if __name__ == "__main__":
    unittest.main()
