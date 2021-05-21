import unittest

from antenna_diversity.diversity_technique import combining
import numpy as np


class TestCombining(unittest.TestCase):
    def setUp(self):
        self.signals = np.array([[1, 2, 3], [4, 5, 6], [9, 8, 7]])
        self.expected = [
                1 + 4 + 9,
                2 + 5 + 8,
                3 + 6 + 7
                ]

    def test_egc(self):
        comb = combining.egc(self.signals)

        np.testing.assert_array_equal(self.expected, comb)

    def test_mrc_simple(self):
        comb = combining.mrc(self.signals, np.ones(len(self.signals)))

        np.testing.assert_array_equal(self.expected, comb)

    def test_mrc(self):
        h = [2, 0.5, 1]
        comb = combining.mrc(self.signals, h)

        exp = [
                2 * 1 + 0.5 * 4 + 1 * 9,
                2 * 2 + 0.5 * 5 + 1 * 8,
                2 * 3 + 0.5 * 6 + 1 * 7
              ]

        np.testing.assert_array_equal(exp, comb)
