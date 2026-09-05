import unittest
from solution import Store, audit

class RetentionTests(unittest.TestCase):
    def test_ttl_and_retained_store(self):
        marker="SYNTHETIC-X"
        short=Store("short",10); retained=Store("retained",None)
        short.write(0,marker); retained.write(0,marker)
        short.expire(10); retained.expire(100)
        self.assertEqual(audit([short,retained],marker),{"short":False,"retained":True})
    def test_failure_copy_is_detected(self):
        marker="SYNTHETIC-FAIL"
        log=Store("error-log",30); log.write(0,"exception payload "+marker)
        self.assertTrue(audit([log],marker)["error-log"])
    def test_realistic_secret_marker_is_rejected(self):
        with self.assertRaises(ValueError): audit([],"customer@example.com")

if __name__ == "__main__": unittest.main()
