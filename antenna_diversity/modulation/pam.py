"""
Simulates M-PAM modulation
"""

from .. import common
from .. import encoding
import numpy as np
import math
from typing import List
from numpy.typing import ArrayLike


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


class PAM:
    def __init__(self, M: int, energy: float = 1) -> None:
        self.__M = M
        self.gray = encoding.GrayEncoder(M)
        d = math.sqrt(3 * energy / (self.__M**2 - 1))
        self.constellation = np.array(generate_lookup(M)) * d

    def modulate(self, symbols: ArrayLike) -> ArrayLike:
        # make d scale mean symbol energy
        gray = self.gray.encode(symbols)
        return self.constellation[gray]

    def demodulate(self, received: ArrayLike) -> ArrayLike:
        """
        Something is wrong
        """
        # There is a column for each constellation element and a row for each "received".
        # This is important since it is best for C-style memory layout to
        # compare elements in a row as opposed to in a column.
        distances = np.abs(np.subtract.outer(received, self.constellation))
        estimated_symbols = np.argmin(distances, 1)
        return self.gray.decode(estimated_symbols)
