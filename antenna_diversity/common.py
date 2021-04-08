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
