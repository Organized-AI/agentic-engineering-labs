import unittest
from solution import Trial, compare, decision

class ExperimentTests(unittest.TestCase):
    def test_paired_results_and_cost(self):
        rows = [
            Trial("1", "A", True, False, 1), Trial("1", "B", True, False, 2),
            Trial("2", "A", True, False, 1), Trial("2", "B", False, False, 2),
            Trial("3", "A", False, False, 1), Trial("3", "B", True, False, 2),
            Trial("4", "A", False, False, 1), Trial("4", "B", False, False, 2),
        ]
        report = compare(rows)
        self.assertEqual((report["both"], report["only_a"], report["only_b"], report["neither"]), (1, 1, 1, 1))
        self.assertEqual(report["a"]["cost_per_accepted"], 2)
        self.assertEqual(report["b"]["cost_per_accepted"], 4)
        self.assertEqual(decision(report), "inconclusive")

    def test_hard_gate_blocks_adoption(self):
        rows = [Trial("1", "A", False, False, 1), Trial("1", "B", True, True, 1)]
        self.assertEqual(decision(compare(rows)), "reject")

    def test_requires_complete_pairs(self):
        with self.assertRaises(ValueError):
            compare([Trial("1", "A", True, False, 1)])

if __name__ == "__main__": unittest.main()
