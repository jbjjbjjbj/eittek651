import unittest
from antenna_diversity.diversity_technique import selection
import numpy as np


class TestSelection(unittest.TestCase):
    def setUp(self):
        self.signals = np.array([[1, 2, 3], [4, 5, 2], [0, 0, 0]])

    def test_simple(self):
        hs = np.array([0, -100, 2])
        chosen = 2

        res, index = selection(self.signals, hs)
        self.assertEqual(chosen, index)
        np.testing.assert_array_equal(res, self.signals[chosen])
