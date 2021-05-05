import unittest
from unittest import signals
from numpy.core.fromnumeric import shape

from scipy.signal.signaltools import resample
from antenna_diversity.diversity_technique import selection
import numpy as np


class TestSelection(unittest.TestCase):
    def setUp(self):
        self.signals = np.array([[1, 2, 3], [4, 5, 2], [0, 0, 0]])
        self.signals_from_power = np.array(
            [np.ones(shape=32 * 4), np.ones(shape=32 * 4) * 0.5, np.ones(shape=32 * 4) * 2])

    def test_simple(self):
        hs = np.array([0, -100, 2])
        chosen = 2
        res, index = selection.selection_from_h(self.signals, hs)
        self.assertEqual(chosen, index)
        np.testing.assert_array_equal(res, self.signals[chosen])

    def test_simple_from_power(self):
        chosen = 2
        res, index = selection.selection_from_power(self.signals_from_power)
        self.assertEqual(chosen, index)
        np.testing.assert_array_equal(res, self.signals_from_power[chosen])
