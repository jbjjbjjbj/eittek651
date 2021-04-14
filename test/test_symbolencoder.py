import unittest
import numpy as np
from antenna_diversity.encoding import SymbolEncoder


class TestSymbolEncoder(unittest.TestCase):
    def setUp(self):
        self.inputs = bytes.fromhex("DEADBEEF")
        self.exp2 = np.array([
            1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1,
            1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1,
            ])
        self.exp4 = np.array([
            3, 1, 3, 2, 2, 2, 3, 1, 2, 3, 3, 2, 3, 2, 3, 3
            ])

    def assertNP(self, a, b):
        self.assertTrue(np.array_equal(a, b))

    def test_encode_m2(self):
        self.assertNP(SymbolEncoder(2).encode_msb(self.inputs), self.exp2)

    def test_m3(self):
        with self.assertRaisesRegex(Exception, "SymbolEncoder created with"):
            SymbolEncoder(3)

    def test_encode_m4(self):
        self.assertNP(SymbolEncoder(4).encode_msb(self.inputs), self.exp4)

    def test_decode_m2(self):
        self.assertNP(SymbolEncoder(2).decode_msb(self.exp2), self.inputs)

    def test_decode_m4(self):
        self.assertNP(SymbolEncoder(4).decode_msb(self.exp4), self.inputs)
