"""
Simulates M-PAM modulation
"""

from .. import common
import numpy as np
import math


def generate_lookup(M):
    """
    Generates a lookup table.
    Example:
    >>> generate_lookup(4)
    [-3, -1, 1, 3]
    """
    res = np.empty(M)
    for i in range(M):
        m = i+1
        # Fleury and Land p. 59
        res[i] = 2 * m - M - 1
    return res


class PAM:
    def __init__(self, M):
        self.__M = M
        self.lol = M
        self.gray = common.GrayEncoder(M)
        self.constellation = generate_lookup(M)

    def modulate(self, symbol, energy=1):
        # make d scale mean symbol energy
        d = math.sqrt(3 * energy / (self.__M**2 - 1))
        gray = self.gray.encode(symbol)
        return self.constellation[gray] * d

    def demodulate(self, received):
        """
        Something is wrong
        """
        res = None
        prev_distance = +math.inf
        for i, symbol in enumerate(self.constellation):
            distance = np.abs(received - symbol)
            if distance <= prev_distance:
                res = i
                prev_distance = distance
        return self.gray.decode(res)
