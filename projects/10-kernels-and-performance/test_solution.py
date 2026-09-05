import unittest
from solution import vector_add, overall_speedup

class KernelTests(unittest.TestCase):
    def test_boundaries_and_empty_input(self):
        for size in (0,1,7,8,9,17):
            x=list(range(size)); y=[2]*size
            self.assertEqual(vector_add(x,y,8),[value+2 for value in x])
    def test_invalid_shapes(self):
        with self.assertRaises(ValueError): vector_add([1],[1,2])
        with self.assertRaises(ValueError): vector_add([],[],0)
    def test_amdahl_bound(self):
        self.assertAlmostEqual(overall_speedup(.2,4),1/0.85)
        self.assertEqual(overall_speedup(0,100),1)

if __name__ == "__main__": unittest.main()
