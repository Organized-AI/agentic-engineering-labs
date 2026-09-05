import unittest
from solution import GIB, weight_bytes, kv_cache_bytes, fits

class InferenceTests(unittest.TestCase):
    def test_weight_and_cache_estimates(self):
        self.assertEqual(weight_bytes(8_000_000_000,2),16_000_000_000)
        self.assertEqual(kv_cache_bytes(32,8,128,8192,2),GIB)
        self.assertEqual(kv_cache_bytes(32,8,128,8192,2,sequences=10),10*GIB)
    def test_headroom_changes_fit(self):
        self.assertTrue(fits(10*GIB,8*GIB,.15))
        self.assertFalse(fits(10*GIB,9*GIB,.15))
    def test_invalid_inputs_fail(self):
        with self.assertRaises(ValueError): weight_bytes(-1,2)
        with self.assertRaises(ValueError): fits(10,5,1)

if __name__ == "__main__": unittest.main()
