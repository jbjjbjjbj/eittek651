"""
Defines som common functions and shorthand functions used across modules.
"""
import numpy as np
import scipy.stats


def q_function(x: np.ndarray) -> np.ndarray:
    """
    Returns the Q-function of x.
    """
    return 1-scipy.stats.norm.cdf(x)


def db_to_power(decibel: np.ndarray) -> np.ndarray:
    """
    Returns power value from a decibel value.
    """
    return 10**(decibel/10)


def db_from_power(power: np.ndarray) -> np.ndarray:
    """
    Returns decibel value from a power value.
    """
    return 10*np.log10(power)
