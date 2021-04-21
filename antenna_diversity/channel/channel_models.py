# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
from .noise import AWGN
from .fading import rayleigh, RayleighFader
import numpy as np
import typing as t

# This file is for the constructed channel models
# The constructed channel models (like the RayAWGNchannel function shown below)
# can be made in this file.
# Other channel models can be made below.


class RayleighAwgnChannel:
    """
    Create a channel applying Rayleigh and AWGN fading to the incoming signal

    Incoming signals are always assumed to be complex
    """

    def __init__(self,
                 snr_db: float,
                 coherence_time: float,
                 sample_period: float,
                 branches: int) -> None:
        self.snr_db = snr_db

        # Create a Rayleigh fader for each sample
        self.faders = []
        for _ in range(branches):
            self.faders.append(RayleighFader(coherence_time, sample_period))

        self.branches = branches

    def attenuate(self, signal: np.ndarray) \
            -> t.Tuple[t.List[np.ndarray], t.List[np.ndarray]]:
        """
        Attenuate a signal through all branches

        Returns both the attenuated signals, and the Rayleigh samples.
        """
        n = len(signal)

        hs = []
        ys = []

        for i in range(self.branches):
            h = self.faders[i].get_samples(n)
            hs.append(h)
            ys.append(h*signal + AWGN(n, self.snr_db))

        return ys, hs


def rayleigh_awgn(x, snr):
    n = len(x)
    alpha = rayleigh(n)
    W = AWGN(n, snr)
    y = alpha*x + W
    return y
