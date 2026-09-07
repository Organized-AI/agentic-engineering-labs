import unittest
from solution import Ledger

def seeded():
    return Ledger(bet="RAG beats fine-tuning at our scale", date="2026-09-06")

class SprintTests(unittest.TestCase):
    def test_gates_are_ordered_and_required(self):
        ledger = seeded()
        with self.assertRaises(ValueError):
            ledger.ship(30, "build")
        ledger.ship(7, "map")
        ledger.ship(30, "build")
        self.assertEqual(list(ledger.artifacts), [7, 30])

    def test_no_artifact_no_level_up(self):
        ledger = seeded()
        with self.assertRaises(ValueError):
            ledger.ship(7, "")
        with self.assertRaises(ValueError):
            ledger.ship(14, "not a gate day")

    def test_grade_reports_bet_state(self):
        ledger = seeded()
        self.assertEqual(ledger.grade(7)["open"], [(7, "fluency")])
        for day, artifact in [(7, "map"), (30, "build"), (60, "review"), (90, "benchmark")]:
            ledger.ship(day, artifact)
        final = ledger.grade(90)
        self.assertTrue(final["complete"])
        self.assertEqual(final["verdict"], "bet ready to grade")
        self.assertEqual(final["bet_date"], "2026-09-06")

if __name__ == "__main__": unittest.main()
