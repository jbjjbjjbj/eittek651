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
    def __init__(self, coherence_time: float, symbol_period: float) -> None:
        # TODO is this an okay approximation
        self.samples_per_fade = int(coherence_time // symbol_period)

        # Keep track of fading samples accross multiple calls to `process_data`
        self.last_fading_value = 0
        self.last_fading_left = 0

    def get_samples(self, n: int) -> np.ndarray:
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


def rayleigh(sizeofinput):
    alpha = np.random.rayleigh(size=sizeofinput, scale=1/math.sqrt(2))
    return alpha
