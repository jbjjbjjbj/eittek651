
# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import unittest
import antenna_diversity.modulation as modulation
import antenna_diversity.channel as channel

import numpy as np


class TestTheChannel(unittest.TestCase):
    def setUp(self) -> None:
        np.random.seed(0)

    def test_overall(self):
        channel = channel.TheChannel(N=3, snr=0)
        channel.print_parameters()
        test_sequence = np.random.randint(10, size=10)
        print("test:", test_sequence)
        hat_test_sequence = channel.run(test_sequence)
        print(hat_test_sequence)
        channel.frame_sendt()
        channel.print_parameters()
