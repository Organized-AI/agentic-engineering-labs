import unittest
from solution import Attempt, outcome_cost, break_even

class CostTests(unittest.TestCase):
    def test_failures_and_review_are_included(self):
        attempts=[Attempt("a",1,0,True),Attempt("b",2,60,False),Attempt("b-retry",3,0,True)]
        report=outcome_cost(attempts,60)
        self.assertEqual(report,{"attempts":3,"accepted":2,"total_cost":66,"cost_per_accepted":33})
    def test_zero_accepted_is_explicit(self):
        self.assertIsNone(outcome_cost([Attempt("a",1,0,False)],0)["cost_per_accepted"])
    def test_break_even(self):
        self.assertEqual(break_even(2000,.05,.01),50000)
        self.assertIsNone(break_even(2000,.01,.02))

if __name__ == "__main__": unittest.main()
