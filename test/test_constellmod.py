# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import unittest
import antenna_diversity.modulation as modulation
import numpy as np


class TestConstellationModulator(unittest.TestCase):
    def test_overall(self):
        m = modulation.PSK(4)
        syms = np.random.randint(0, 4, size=10)
        modulated = m.modulate(syms)
        demodulated = m.demodulate(modulated)
        self.assertTrue(np.array_equal(syms, demodulated))
        self.assertTrue(demodulated.dtype == syms.dtype)

    def test_floating_input(self):
        m = modulation.PSK(4)
        syms = np.random.randint(0, 4, size=10).astype(float)

        try:
            m.modulate(syms)
        except IndexError:
            self.fail("IndexError on symbol modulation, could not handle \
floating point")
