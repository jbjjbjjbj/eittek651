import unittest
from antenna_diversity.channel import RayleighAWGNChannel
import numpy as np


class TestChannelModels(unittest.TestCase):
    def test_output_size(self):
        chnl = RayleighAWGNChannel(3, 10)

        signal = np.ones(100)

        recv, h = chnl.run(signal)
        self.assertTupleEqual(recv.shape, (3, 100))
        self.assertEqual(len(h), 3)

    def test_frame_per_block(self):
        chnl = RayleighAWGNChannel(3, 10)
        h = chnl.h

        for _ in range(5):
            chnl.frame_sent()

        equal = np.array_equal(h, chnl.h)
        self.assertTrue(equal)

        chnl.frame_sent()

        equal = np.array_equal(h, chnl.h)
        self.assertFalse(equal)
