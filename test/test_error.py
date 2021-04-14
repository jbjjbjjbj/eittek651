import unittest
from antenna_diversity.error import BitErrorMeasure, SymErrorMeasure
import numpy as np


class TestBitErrorMeasure(unittest.TestCase):
    def test(self):
        data = np.zeros(100, dtype=np.ubyte)

        meas = BitErrorMeasure(data.tobytes())

        data[0] = 1
        data[50] = 0xFF

        frac, faults, _ = meas.check_against(data)

        self.assertEqual(frac, 0.01125)
        self.assertEqual(faults, 9)


class TestSymErrorMeasure(unittest.TestCase):
    def test(self):
        data = np.arange(100) * 23

        meas = SymErrorMeasure(data, copy=True)

        data[0] = 23
        data[23] = 12
        data[3] = 12
        data[99] = 12

        frac, faults, _ = meas.check_against(data)
        self.assertEqual(frac, 0.04)
        self.assertEqual(faults, 4)
