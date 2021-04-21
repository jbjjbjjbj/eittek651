# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
from .noise import AWGN
from .fading import rayleigh
import numpy as np
from scipy import signal
import typing as t

# This file is for the construced channel models
# The construced channel models (like the RayAWGNchannel function shown below)
# can be made in this file.
# Other channel models can be made below.


class RayleighAwgnChannel:
    """
    Create a channel applying rayleigh and awgn fading to the incomming signal

    The constructor should be given the noise_floor relative to the signal,
    and should not be given as a snr value.

    Incomming signals are always assumed to be complex
    """

    def __init__(self,
                 noise_floor_db: float,
                 coherence_time: float,
                 symbol_period: float) -> None:
        self.noise_floor = noise_floor_db

        # TODO is this an okay approximation
        self.samples_per_fade = int(coherence_time // symbol_period)

        # Keep track of fading samples accross multiple calls to `process_data`
        self.last_fading_value = 0
        self.last_fading_left = 0

    def get_fading_samples(self, n: int) -> np.ndarray:
        h = np.empty(n)

        # Fill out the first values with the fading value from last
        from_last = min(self.last_fading_left, n)
        if from_last != 0:
            h[:from_last] = np.repeat(self.last_fading_value, from_last)
            n -= from_last

            self.last_fading_left -= from_last

        if n <= 0:
            return h

        # Create fading samples
        alpha = rayleigh(int(np.ceil(n / self.samples_per_fade)))
        upsampled = signal.upfirdn(h=np.ones(self.samples_per_fade),
                                   x=alpha,
                                   up=self.samples_per_fade)

        h[from_last:] = upsampled[:n]

        # Check for leftovers
        leftover = len(upsampled) - n
        if leftover > 0:
            self.last_fading_left = leftover
            self.last_fading_value = alpha[-1]

        return h

    def attenuate(self, signal: np.ndarray) \
            -> t.Tuple[np.ndarray, np.ndarray]:
        """
        Attenuate a signal through the channel

        Returns both the attenuated signal, and they reyleigh samples used.
        """
        n = len(signal)

        h = self.get_fading_samples(n)
        y = h*signal + AWGN(n, self.noise_floor)

        return y, h


def rayleigh_awgn(x, snr):
    n = len(x)
    alpha = rayleigh(n)
    W = AWGN(n, snr)
    y = alpha*x + W
    return y
