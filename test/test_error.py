import unittest
from antenna_diversity import error
import numpy as np


class TestBitErrorMeasure(unittest.TestCase):
    def test(self):
        data = np.zeros(100, dtype=np.ubyte)
        data_before = np.copy(data)

        data[0] = 1
        data[50] = 0xFF

        faults, total = error.count_bit_errors(data, data_before)

        self.assertEqual(faults, 9)
        self.assertEqual(total, 100 * 8)


class TestSymErrorMeasure(unittest.TestCase):
    def test(self):
        data = np.arange(100) * 23
        data_before = np.copy(data)

        data[0] = 23
        data[23] = 12
        data[3] = 12
        data[99] = 12

        faults, total = error.count_symbol_errors(data, data_before)
        self.assertEqual(total, 100)
        self.assertEqual(faults, 4)
