# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import unittest
from antenna_diversity import common
import numpy as np


class TestBitErrorMeasure(unittest.TestCase):
    def test(self):
        data = np.zeros(100, dtype=np.ubyte)
        data_before = np.copy(data)

        data[0] = 1
        data[50] = 0xFF

        faults, total = common.count_bit_errors(data, data_before)

        self.assertEqual(faults, 9)
        self.assertEqual(total, 100 * 8)

    def test_exception(self):
        d1 = b'adbe'
        d2 = b'adbeed'
        with self.assertRaisesRegex(Exception, "differ: 4 != 6"):
            common.count_bit_errors(d1, d2)


class TestSymErrorMeasure(unittest.TestCase):
    def test(self):
        data = np.arange(100) * 23
        data_before = np.copy(data)

        data[0] = 23
        data[23] = 12
        data[3] = 12
        data[99] = 12

        faults, total = common.count_symbol_errors(data, data_before)
        self.assertEqual(total, 100)
        self.assertEqual(faults, 4)
