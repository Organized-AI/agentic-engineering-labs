import unittest
from solution import Option, cost_per_accepted, price, winner

OPTIONS = [
    Option("prompt-v2", accepted=24, attempted=30, variable_cost=0.04, fixed_cost=0, review_minutes=1.0),
    Option("rag-pack", accepted=27, attempted=30, variable_cost=0.09, fixed_cost=200, review_minutes=0.5),
    Option("fine-tune", accepted=29, attempted=30, variable_cost=0.02, fixed_cost=4000, review_minutes=0.25),
]

class PricingTests(unittest.TestCase):
    def test_fixed_cost_amortizes_and_review_counts(self):
        tune = OPTIONS[2]
        at_1000 = cost_per_accepted(tune, 1000)
        at_10000 = cost_per_accepted(tune, 10000)
        self.assertGreater(at_1000, at_10000)
        self.assertAlmostEqual(at_10000, 0.02 + 0.4 + 0.25, places=6)

    def test_winner_is_cheapest_above_the_bar(self):
        report = price(OPTIONS, volume=1000)
        self.assertEqual(winner(report), "rag-pack")
        report = price(OPTIONS, volume=100000)
        self.assertEqual(winner(report), "fine-tune")

    def test_nothing_above_the_bar_means_no_winner(self):
        weak = [Option("bad", accepted=5, attempted=30, variable_cost=0.01, fixed_cost=0, review_minutes=0)]
        report = price(weak, volume=1000)
        self.assertIsNone(winner(report))

if __name__ == "__main__": unittest.main()
