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
