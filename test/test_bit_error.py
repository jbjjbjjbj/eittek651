import unittest
from antenna_diversity import BitErrorMeasure
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
