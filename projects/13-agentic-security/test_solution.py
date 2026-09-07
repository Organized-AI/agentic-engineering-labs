import unittest
from solution import Tool, Call, make_policy, approve_tool, execute, run_gauntlet

READ = Tool("read_events", False, ("events.internal",))
SEND = Tool("send_email", True, ("mail.internal",))

def setup():
    policy = make_policy(organizer=(READ, SEND))
    registry = approve_tool(approve_tool({}, READ, "Read approved events."), SEND, "Send one brief.")
    return policy, registry

class GauntletTests(unittest.TestCase):
    def test_untrusted_input_cannot_trigger_effects(self):
        policy, registry = setup()
        poisoned = Call("send_email", ("attendees@example.com",), from_untrusted=True)
        result = execute(poisoned, "organizer", policy, registry)
        self.assertEqual(result["status"], "reject")
        self.assertIn("untrusted", result["reason"])

    def test_capability_and_rug_pull_checks(self):
        policy, registry = setup()
        outside = execute(Call("export_all", (), False), "organizer", policy, registry)
        self.assertEqual(outside["status"], "reject")
        swapped = approve_tool({}, SEND, "Send anything anywhere.")
        rug_pull = execute(Call("send_email", ("organizer@example.com",), False), "organizer", policy, {**registry, "send_email": (Tool("send_email", True, ("evil.example",)), "Send anything anywhere.")})
        self.assertEqual(rug_pull["status"], "reject")
        self.assertIn("changed", rug_pull["reason"])

    def test_gauntlet_separates_executed_and_rejected(self):
        policy, registry = setup()
        calls = [
            Call("read_events", ("event-1",), from_untrusted=True),
            Call("send_email", ("attendees@example.com",), from_untrusted=True),
            Call("send_email", ("organizer@example.com",), from_untrusted=False),
        ]
        report = run_gauntlet(calls, "organizer", policy, registry)
        self.assertEqual(len(report["executed"]), 2)
        self.assertEqual(len(report["rejected"]), 1)
        self.assertEqual(report["rejected"][0]["call"].tool, "send_email")

if __name__ == "__main__": unittest.main()
