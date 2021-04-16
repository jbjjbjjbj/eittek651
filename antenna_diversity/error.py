import numpy as np
import typing as t


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
    for i in range(val.bit_length()):
        count += val & 1
        val = val >> 1

    return count


# Create bit count lookup table
bit_count_lookup = np.empty(256, dtype=int)
for i in range(256):
    bit_count_lookup[i] = count_bits(i)


def count_bit_errors(a: bytes, b: bytes) -> t.Tuple[int, int]:
    a_np = np.frombuffer(a, dtype=np.ubyte)
    b_np = np.frombuffer(b, dtype=np.ubyte)

    n = len(a_np)
    if n != len(b_np):
        raise Exception("array to be checked is not the original size")

    total_bits = n * 8

    difference = np.bitwise_xor(a_np, b_np)
    counts = bit_count_lookup[difference]
    wrong_bits = np.sum(counts)

    return wrong_bits, total_bits


def count_symbol_errors(a: np.ndarray, b: np.ndarray) \
        -> t.Tuple[float, int, int]:

    if len(a) != len(b):
        raise Exception("array to be checked is not the original size")

    wrong = np.sum(a != b)

    return wrong, len(a)
