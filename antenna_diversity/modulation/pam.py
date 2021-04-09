"""
Simulates M-PAM modulation
"""

from typing import List

from .constellmod import ConstellationModulator


def generate_lookup(M: int) -> List[int]:
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
    def generate_constellation(self) -> List[int]:
        return generate_lookup(self.M)
