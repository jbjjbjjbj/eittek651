# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
"""
Simulates M-PAM modulation
"""

import numpy as np
import typing as t
import math

from .. import common

from .constellmod import ConstellationModulator


def generate_lookup(M: int) -> t.List[int]:
    """
    Generates a lookup table.
    Example:
    >>> generate_lookup(4)
    [-3, -1, 1, 3]
    """
    res = []
    for i in range(M):
        m = i+1
        # Fleury and Land p. 59
        res.append(2 * m - M - 1)
    return res


class PAM(ConstellationModulator):
    def generate_constellation(self, energy: float) -> np.ndarray:
        d = math.sqrt(3 * energy / (self.M**2 - 1))
        return np.array(generate_lookup(self.M)) * d

    def theoretical_bitprob(self, snr: np.ndarray) -> np.ndarray:
        """
        Calculates the theoretical bit probabilities with bit SNR's

        Cite: Fleury and Land, page 66
        """
        M = self.M
        log2M = np.log2(M)
        return 2 * (M - 1) / (M * log2M) * \
            common.q_function(np.sqrt(snr * (6 * log2M) / (M*M - 1)))

    def theoretical_symprob(self, snr: np.ndarray) -> np.ndarray:
        """
        Calculates the theoretical symbol probability with symbol SNR's.

        Cite: Fleury and Land, page 65
        """
        M = self.M
        return 2 * (1 - 1/M) * common.q_function(np.sqrt(snr * 6 / (M*M - 1)))
