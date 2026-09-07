import unittest
from solution import BLOCKS, audit

STRONG = {
    "prompt_in_git": True, "tests_run_in_ci": True, "rollback_documented": True,
    "reviewed_commits_pct": 95, "adr_count": 4, "alerts_have_owners": True,
    "secrets_in_manager": True,
}

class FoundationTests(unittest.TestCase):
    def test_strong_repo_passes_with_no_fix_list(self):
        result = audit(STRONG)
        self.assertTrue(result["passes"])
        self.assertEqual(result["fix_first"], [])
        self.assertIsNone(result["weakest"])

    def test_gaps_land_on_the_fix_first_list_in_order(self):
        report = {**STRONG, "rollback_documented": False, "alerts_have_owners": False}
        result = audit(report)
        self.assertEqual(result["weakest"], "reversible_deploys")
        self.assertEqual(result["fix_first"], ["reversible_deploys", "telemetry"])

    def test_every_score_carries_evidence(self):
        result = audit({})
        self.assertEqual(len(result["results"]), len(BLOCKS))
        for r in result["results"]:
            self.assertIn(r["block"], r["evidence"])

if __name__ == "__main__": unittest.main()
