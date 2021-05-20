# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import numpy as np
import math
from scipy import signal

# This file is for housing different fading methods (like the Rayleigh
# function below).
# Other fading function can be added later if needed


class RayleighFader:
    """
    Stretches Rayleigh values from `Rayleigh` over multiple samples in
    accordance to the coherence time.

    The coherence time determines the amount of time where the channel stays
    constant.
    To account for this the Rayleigh distribution should be up sampled by some
    constant.

    Because this works in time, the sampling period must be given.
    """

    def __init__(self, coherence_time: float, sample_period: float) -> None:
        # TODO is this an okay approximation
        self.samples_per_realization = int(coherence_time // sample_period)

        # Keep track of fading samples across multiple calls to `process_data`
        self.prev_alpha: float = 0
        self.prev_left: int = 0

    def get_samples(self, n: int) -> np.ndarray:
        h = np.empty(n)
        # Fill out the first values with the fading value from last call to
        # `get_samples`
        number_from_last = min(self.prev_left, n)
        if number_from_last != 0:
            h[:number_from_last] = np.repeat(self.prev_alpha, number_from_last)
            n -= number_from_last

            self.prev_left -= number_from_last

        if n <= 0:
            return h

        # Pull out enough values from Rayleigh to satisfy n samples
        alpha = rayleigh(int(np.ceil(n / self.samples_per_realization)))

        # Upsample alpha so that each value is repeated samples_per_realization
        # times
        upsampled = signal.upfirdn(h=np.ones(self.samples_per_realization),
                                   x=alpha,
                                   up=self.samples_per_realization)

        # Copy the needed samples into h
        h[number_from_last:] = upsampled[:n]

        # Check that some values from up sampled should be added to the next
        # `get_sampled` call
        nr_leftover = len(upsampled) - n
        if nr_leftover > 0:
            self.prev_left = nr_leftover
            self.prev_alpha = alpha[-1]

        return h


def rayleigh(sizeofinput):
    alpha = np.random.rayleigh(size=sizeofinput, scale=1/math.sqrt(2))
    return alpha
