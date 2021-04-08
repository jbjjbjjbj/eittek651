"""
Defines som common functions and shorthand functions used across modules.
"""
import math
import scipy.stats


def q_function(x: float) -> float:
    """
    Returns the Q-function of x.
    """
    return 1-scipy.stats.norm.cdf(x)


def db_to_power(decibel: float) -> float:
    """
    Returns power value from a decibel value.
    """
    return 10**(decibel/10)


def db_from_power(power: float) -> float:
    """
    Returns decibel value from a power value.
    """
    return 10*math.log(power, 10)


class GrayEncoder:

    def __init__(self, M):
        if M == 4:
            self.lookup = [0, 1, 3, 2]
        elif M == 16:
            self.lookup = [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8]
        else:
            raise f"Can't Gray Encode for {M} bits"

    def encode(self, a):
        return self.lookup[a]

    def decode(self, a):
        return self.lookup.index(a)
