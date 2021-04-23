# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
from .noise import AWGN, AWGN_Matrix
from .fading import rayleigh, RayleighFader
import numpy as np
import typing as t
import math
# This file is for the constructed channel models
# The constructed channel models (like the RayAWGNchannel function shown below)
# can be made in this file.
# Other channel models can be made below.


class TheChannel:
    def __init__(self, N, snr, frame_per_block=6) -> None:
        """
            N: number of branches for the channel
            snr: the starting snr of the channel in dB
            frame_per_block: Number of frames per channel block,
                standard is 6 frames per block, equal to sending
                at a coherence time of 60ms

            The channel is based on DECT frames, i.e. the channel
            should be updated with frame_sendt()
            after each frame have been passed through the channel.
        """
        self.N = N
        self.snr = snr
        self.number_of_send_frame = 0
        self.frame_per_channel_block = frame_per_block
        self.update_h()

    def run(self, signal):
        """
            signal: array of complex signal points
            returns: matrix that is N x len(signal) where
            N is number of branches
            The channel is a rayleight distributed and AWGN i.e.
            y = h*x+n
        """
        noise = AWGN_Matrix(self.N, len(signal), self.snr)
        
        # makes the outer product between the h vector and the signal vector
        hTimesSignal = np.outer(self.h, signal)
        return hTimesSignal + noise

    def frame_sendt(self):
        """
            Method to be called after a frame have been sendt
            Must be called by the user, updates the number of frames sendt
            and updates the channel h if the number of frames sendt
            is bigger then or equal to the frames per block
        """
        self.number_of_send_frame += 1
        if self.number_of_send_frame >= self.frame_per_channel_block:
            self.update_h()
            self.number_of_send_frame = 0

    def update_h(self):
        """
            Method for updating the h array i.e. channel parameter
        """
        self.h = np.transpose(np.random.rayleigh(
            size=self.N, scale=1 / math.sqrt(2)))

    def print_parameters(self):
        print(self.__dict__)


def rayleigh_awgn(x, snr):
    n = len(x)
    alpha = rayleigh(n)
    W = AWGN(n, snr)
    y = alpha * x + W
    return y
