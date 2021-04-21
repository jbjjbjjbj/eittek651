# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
from .noise import AWGN
from .fading import rayleigh, RayleighFader
import numpy as np
import typing as t

# This file is for the construced channel models
# The construced channel models (like the RayAWGNchannel function shown below)
# can be made in this file.
# Other channel models can be made below.


class RayleighAwgnChannel:
    """
    Create a channel applying Rayleigh and AWGN fading to the incoming signal

    Incoming signals are always assumed to be complex
    """

    def __init__(self,
                 SNR_db: float,
                 coherence_time: float,
                 symbol_period: float,
                 branches: int) -> None:
        self.SNR_db = SNR_db

        # Create a Rayleigh fader for each sample
        self.faders = []
        for _ in range(branches):
            self.faders.append(RayleighFader(coherence_time, symbol_period))

        self.branches = branches

    def attenuate(self, signal: np.ndarray) \
            -> t.Tuple[t.List[np.ndarray], t.List[np.ndarray]]:
        """
        Attenuate a signal through all brances

        Returns both the attenuated signals, and they reyleigh samples used.
        """
        n = len(signal)

        hs = []
        ys = []

        for i in range(self.branches):
            h = self.faders[i].get_samples(n)
            hs.append(h)
            ys.append(h*signal + AWGN(n, self.SNR_db))

        return ys, hs


def rayleigh_awgn(x, snr):
    n = len(x)
    alpha = rayleigh(n)
    W = AWGN(n, snr)
    y = alpha*x + W
    return y
