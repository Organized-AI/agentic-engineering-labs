import unittest
from solution import Request, percentile, simulate

class LoadTests(unittest.TestCase):
    def test_percentile_and_queueing(self):
        self.assertEqual(percentile([4,1,3,2],.5),2)
        report=simulate([Request(0,1),Request(.1,1)],workers=1,deadline=3)
        self.assertAlmostEqual(report["rows"][1]["queue"],.9)
        self.assertAlmostEqual(report["p95"],1.9)
    def test_deadline_and_quality_define_goodput(self):
        report=simulate([Request(0,1,True),Request(0,1,False),Request(0,3,True)],workers=3,deadline=2)
        self.assertEqual((report["attempted"],report["accepted"]),(3,1))
    def test_more_load_can_reduce_accepted_count(self):
        low=simulate([Request(i,1) for i in range(5)],workers=1,deadline=2)
        high=simulate([Request(i*.1,1) for i in range(10)],workers=1,deadline=2)
        self.assertGreater(low["accepted"],high["accepted"])

if __name__ == "__main__": unittest.main()
