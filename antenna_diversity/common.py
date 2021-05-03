# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
"""
Defines som common functions and shorthand functions used across modules.
"""
import numpy as np
import scipy.stats
import typing as t


def q_function(x):
    """
    Returns the Q-function of x.
    """
    return 1-scipy.stats.norm.cdf(x)


def db_to_power(decibel):
    """
    Returns power value from a decibel value.
    """
    return 10**(decibel/10)


def db_from_power(power):
    """
    Returns decibel value from a power value.
    """
    return 10*np.log10(power)


def shared_length(a, *args) -> int:
    """
    Returns the shared length between arguments if the length identical.
    >>> shared_length([1,1,1], [2,2,2], [3,3,3])
    3
    >>> shared_length(np.array([1]), np.array([2]))
    1
    >>> shared_length((1, 1), [2, 2])
    2
    >>> shared_length((1, 1), (2, 2))
    2
    >>> shared_length((1, 2), (1, 2, 3))
    Traceback (most recent call last):
    Exception: lengths of (1, 2) and (1, 2, 3) differ: 2 != 3
    """
    na = len(a)
    for arg in args:
        nb = len(arg)
        if na != nb:
            raise Exception(f"lengths of {a} and {arg} differ: {na} != {nb}")

    return na


def count_bits(val: int) -> int:
    """
    >>> count_bits(0b10101100)
    4
    >>> count_bits(0xFF)
    8
    >>> count_bits(432432043213)
    22
    >>> count_bits(0)
    0
    >>> count_bits(1)
    1
    """
    count = 0
    for _ in range(val.bit_length()):
        count += val & 1
        val = val >> 1

    return count


bit_count_lookup = np.empty(256, dtype=int)
for i in range(256):
    bit_count_lookup[i] = count_bits(i)


def count_bit_errors(a: bytes, b: bytes) -> t.Tuple[int, int]:
    a_np = np.frombuffer(a, dtype=np.ubyte)
    b_np = np.frombuffer(b, dtype=np.ubyte)

    n = shared_length(a_np, b_np)

    total_bits = n * 8

    difference = np.bitwise_xor(a_np, b_np)
    counts = bit_count_lookup[difference]
    wrong_bits = np.sum(counts)

    return wrong_bits, total_bits


def count_symbol_errors(a: np.ndarray, b: np.ndarray) -> t.Tuple[int, int]:

    n = shared_length(a, b)

    wrong = np.sum(a != b)

    return wrong, n
