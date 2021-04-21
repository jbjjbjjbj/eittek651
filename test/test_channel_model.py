import unittest
from antenna_diversity.channel import RayleighAwgnChannel
import numpy as np
from scipy.signal import upfirdn


class TestRayleightAwgnChannel(unittest.TestCase):
    def setUp(self):
        self.channel = RayleighAwgnChannel(10, 10, 1)
        self.seed()

    def assertNPEqual(self, a: np.ndarray, b: np.ndarray, round=None) -> bool:
        if round is not None:
            a = np.around(a, round)
            b = np.around(b, round)
        self.assertTrue(np.array_equal(a, b))

    def seed(self):
        np.random.seed(0)

    def test_fading_samples_exact(self):
        h = self.channel.get_fading_samples(10)

        self.assertNPEqual(h, [0.89211799]*10, 3)

    def test_fading_samples_smaller(self):
        h1 = self.channel.get_fading_samples(5)
        h2 = self.channel.get_fading_samples(5)

        expect = np.repeat(0.89211799, 5)
        self.assertNPEqual(h1, expect, 3)
        self.assertNPEqual(h2, expect, 3)

    def test_fading_samples_larger(self):
        h = self.channel.get_fading_samples(20)

        expect = upfirdn(h=np.ones(10), x=[0.89211799, 1.12068317], up=10)

        self.assertNPEqual(h, expect, 3)

    def test_fading_samples_wierd(self):
        h1 = self.channel.get_fading_samples(7)
        h2 = self.channel.get_fading_samples(7)
        h3 = self.channel.get_fading_samples(10)

        expect1 = [0.89211799]*7
        expect2 = [0.89211799]*3 + [1.12068317]*4
        expect3 = [1.12068317]*6 + [0.96084502]*4

        self.assertNPEqual(h1, expect1, 3)
        self.assertNPEqual(h2, expect2, 3)
        self.assertNPEqual(h3, expect3, 3)
