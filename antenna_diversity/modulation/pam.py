"""
Simulates M-PAM modulation
"""

import numpy as np
import typing as t
import math

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
