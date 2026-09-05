import unittest
from solution import Task, evaluate, release_gate

class EvaluationTests(unittest.TestCase):
    def test_outcome_beats_claim(self):
        def liar(task, env, trial): return "saved correctly"
        report=evaluate([Task("a","Hall A")],liar)
        self.assertFalse(report["attempts"][0]["accepted"])
    def test_forbidden_effect_is_hard_gate(self):
        def unsafe(task, env, trial):
            env["saved"]={"event_id":task.id,"venue":task.expected_venue}; env["effects"].append("email_sent")
        report=evaluate([Task("a","Hall A","email_sent")],unsafe)
        self.assertFalse(release_gate(report,0))
    def test_all_trials_remain_in_denominator(self):
        def variable(task, env, trial):
            if trial == 0: env["saved"]={"event_id":task.id,"venue":task.expected_venue}
        report=evaluate([Task("a","Hall A")],variable,trials=2)
        self.assertEqual((report["accepted"],len(report["attempts"])),(1,2))
        self.assertFalse(release_gate(report,.75))

if __name__ == "__main__": unittest.main()
