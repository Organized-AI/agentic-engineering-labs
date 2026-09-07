import unittest
from solution import Token, issue_service_token, exchange, call

USER = Token("jordan", "auth", "user:full", "user-session")

class IdentityTests(unittest.TestCase):
    def test_exchange_preserves_subject_and_narrows_audience(self):
        token = exchange(USER, "calendar", "event:write", "agent-worker-1")
        self.assertEqual(token.subject, "jordan")
        self.assertEqual(token.audience, "calendar")
        result = call("calendar", "event:write", token)
        self.assertEqual(result["status"], "executed")
        self.assertEqual(result["actor"], "agent-worker-1")

    def test_wrong_audience_is_rejected(self):
        token = exchange(USER, "calendar", "event:write", "agent-worker-1")
        result = call("billing", "billing:charge", token)
        self.assertEqual(result["status"], "reject")
        self.assertIn("audience", result["reason"])

    def test_service_account_cannot_stand_in_for_a_user(self):
        result = call("calendar", "event:write", issue_service_token("agent-worker-1"))
        self.assertEqual(result["status"], "reject")
        self.assertIn("subject", result["reason"])

if __name__ == "__main__": unittest.main()
