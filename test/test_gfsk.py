# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import unittest
import antenna_diversity as ad
import numpy as np

class TestGFSK(unittest.TestCase):
    def setUp(self):
        np.random.seed(0)
        self.data = np.random.bytes(10)
        self.symbols = ad.encoding.SymbolEncoder(2).encode_msb(self.data)
        self.mod = ad.modulation.GFSK()

    def test_mod_demod_signed(self):
        symbols = self.symbols.astype(int)
        moded = self.mod.modulate(symbols)

        demod = self.mod.demodulate(moded)

        np.testing.assert_equal(self.symbols, demod)

    def test_mod_demod_unsigned(self):
        symbols = self.symbols.astype(np.uint8)
        moded = self.mod.modulate(symbols)

        demod = self.mod.demodulate(moded)

        np.testing.assert_equal(self.symbols, demod)
