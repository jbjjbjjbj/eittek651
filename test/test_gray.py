import unittest
import numpy as np
from antenna_diversity.encoding import GrayEncoder           

class TestGrayEncoder(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_encoded(self):
        inputArr = np.array([0, 1, 2, 3])
        encoded = GrayEncoder(4).encode(inputArr)
        output = np.array([0, 1, 3, 2])
        self.assertTrue(np.array_equal(encoded, output))
        
    