from .constellmod import ConstellationModulator
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
    def generate_constellation(self, energy: float) -> np.ndarray:
        return np.array(generate_psk_constellation(self.M)) * math.sqrt(energy)