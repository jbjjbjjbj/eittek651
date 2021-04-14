import unittest
import numpy as np
from antenna_diversity.encoding import GrayEncoder


class TestGrayEncoder(unittest.TestCase):
    def setUp(self):
        self.inputs = np.array([1, 3, 2, 1, 0, 0])
        self.exp = np.array([1, 2, 3, 1, 0, 0])
        pass

    def test_encode(self):
        encoded = GrayEncoder(4).encode(self.inputs)
        self.assertTrue(np.array_equal(encoded, self.exp))

    def test_decode(self):
        decoded = GrayEncoder(4).encode(self.exp)
        self.assertTrue(np.array_equal(decoded, self.inputs))

    def test_invalid_m(self):
        with self.assertRaisesRegex(AssertionError, "M should be a power o"):
            GrayEncoder(3)
