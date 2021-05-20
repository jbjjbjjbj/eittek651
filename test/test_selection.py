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

    def test_from_h_simple(self):
        hs = np.array([-100, 0, 2])
        chosen = 2
        res, index = selection.selection_from_h(self.signals, hs)
        self.assertEqual(chosen, index)
        np.testing.assert_array_equal(res, self.signals[chosen])

    def test_from_power_simple(self):
        chosen = 2
        res, index = selection.selection_from_power(self.signals_from_power)
        self.assertEqual(chosen, index)
        np.testing.assert_array_equal(res, self.signals_from_power[chosen])

    def test_from_crc(self):
        selector = selection.CRCSelection(2)

        for _ in range(10):
            _, sel = selector.select(self.signals)
            self.assertEqual(sel, 0)

        selector.report_crc_status(True)
        _, sel = selector.select(self.signals)
        self.assertEqual(sel, 0)

        selector.report_crc_status(False)
        _, sel = selector.select(self.signals)
        self.assertEqual(sel, 1)

        selector.report_crc_status(True)
        _, sel = selector.select(self.signals)
        self.assertEqual(sel, 1)

        selector.report_crc_status(False)
        _, sel = selector.select(self.signals)
        self.assertEqual(sel, 0)

    def test_selection_from_power_and_crc(self):
        chosen = 1
        crc_errors = [True, False, True]
        res, index = selection.selection_from_power_and_crc(self.signals_from_power,
                                                            crc_errors)
        self.assertEqual(chosen, index)
        np.testing.assert_array_equal(res, self.signals_from_power[chosen])


        chosen = 2
        crc_errors = [True, False, True]
        res, index = selection.selection_from_power_and_crc(self.signals_from_power,
                                                            crc_errors)
        self.assertFalse(chosen == index)

        chosen = 2
        crc_errors = [True, True, True]  # cover "else" in "for else"
        res, index = selection.selection_from_power_and_crc(self.signals_from_power,
                                                            crc_errors)
        self.assertTrue(chosen == index)

        # Catch a bug where the first non error crc branch was chosen, even
        # if it had worse snr
        chosen = 2
        crc_errors = [False, False, False]  # cover "else" in "for else"
        res, index = selection.selection_from_power_and_crc(self.signals_from_power,
                                                            crc_errors)
        self.assertEqual(chosen, index)

