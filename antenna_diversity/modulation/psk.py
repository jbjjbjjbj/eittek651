# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
from .constellmod import ConstellationModulator
from .. import common
import typing as t
import math
import numpy as np


def generate_psk_constellation(M: int) -> t.List[complex]:
    """
    Generate M-ary PSK constellation

    Example:
    >>> [np.round(x) for x in generate_psk_constellation(4)]
    [(1+0j), 1j, (-1+0j), (-0-1j)]
    """
    # Cite Fleury and Land p. 89
    precalc = 2 * math.pi / M
    def phi_m_g(m): return (m-1) * precalc

    res: t.List[complex] = []

    for i in range(M):
        m = i+1
        phi_m = phi_m_g(m)

        point = math.cos(phi_m) + 1j * math.sin(phi_m)

        res.append(point)

    return res


class PSK(ConstellationModulator):
    name = "Phase Shift Keying"

    def generate_constellation(self, energy: float) -> np.ndarray:
        return np.array(generate_psk_constellation(self.M)) * math.sqrt(energy)

    def theoretical_symprob(self, snr: np.ndarray) -> np.ndarray:
        """
        Calculates the theoretical symbol probability with symbol SNR's.

        Cite: Fleury and Land, page 95
        """
        M = self.M
        if M != 4:
            raise Exception(f"theoretical_symprob only implemented \
                    for M=4, not M={M}")

        sqrt_snr = np.sqrt(snr)
        return 2 * common.q_function(sqrt_snr) - common.q_function(sqrt_snr)**2

    def theoretical_bitprob(self, snr: np.ndarray) -> np.ndarray:
        """
        Calculates the theoretical bit probabilities with bit SNR's

        Cite: Fleury and Land, page 98
        """
        M = self.M
        if M != 4:
            raise Exception(f"theoretical_bitprob only implemented \
                    for M=4, not M={M}")

        return common.q_function(np.sqrt(snr * 2))
