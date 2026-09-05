import unittest
from solution import Jobs

class JobTests(unittest.TestCase):
    def setUp(self): self.jobs=Jobs()
    def test_idempotent_submit(self):
        self.assertEqual(self.jobs.submit("k","p"), self.jobs.submit("k","p"))
        with self.assertRaises(ValueError): self.jobs.submit("k","different")
    def test_active_lease_and_stale_fencing(self):
        job=self.jobs.submit("k","p"); old=self.jobs.claim(job,0)
        self.assertIsNone(self.jobs.claim(job,1))
        new=self.jobs.claim(job,11)
        with self.assertRaises(RuntimeError): self.jobs.complete(job,old,"old",12)
        self.assertEqual(self.jobs.complete(job,new,"new",12),"new")
    def test_atomic_idempotent_completion(self):
        job=self.jobs.submit("k","p"); token=self.jobs.claim(job,0)
        self.assertEqual(self.jobs.complete(job,token,"value",1),"value")
        self.assertEqual(self.jobs.complete(job,token,"value",2),"value")
        self.assertEqual(self.jobs.db.execute("SELECT COUNT(*) FROM results").fetchone()[0],1)
        self.assertEqual(self.jobs.db.execute("SELECT COUNT(*) FROM outbox").fetchone()[0],1)

if __name__ == "__main__": unittest.main()
