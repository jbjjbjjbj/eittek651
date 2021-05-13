import unittest
from antenna_diversity.channel import RayleighAWGNChannel
import numpy as np


class TestChannelModels(unittest.TestCase):
    def setUp(self):
        np.random.seed(2)

    def test_output_size(self):
        chnl = RayleighAWGNChannel(3, 10)

        signal = np.ones(100)

        recv, h = chnl.run(signal)
        self.assertTupleEqual(recv.shape, (3, 100))
        self.assertEqual(len(h), 3)

    def test_frame_per_block(self):
        chnl = RayleighAWGNChannel(3, 10, 3, 0)
        h = chnl.h

        for _ in range(2):
            chnl.frame_sent()

        equal = np.array_equal(h, chnl.h)
        self.assertTrue(equal)

        chnl.frame_sent()

        equal = np.array_equal(h, chnl.h)
        self.assertFalse(equal)

    def test_frame_per_block_interpolate(self):
        chnl = RayleighAWGNChannel(3, 10, 3, 1)
        h = np.copy(chnl.h)

        chnl.frame_sent()

        equal = np.array_equal(h, chnl.h)
        self.assertTrue(equal)

        chnl.frame_sent()
        h_inter = np.copy(chnl.h)
        chnl.frame_sent()

        equal = np.array_equal(h, chnl.h)
        self.assertFalse(equal)

        equal1 = np.array_equal(h_inter, chnl.h)
        equal2 = np.array_equal(h_inter, h)
        self.assertFalse(equal1 or equal2)
