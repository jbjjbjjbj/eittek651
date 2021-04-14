import numpy as np
import typing as t


def count_bits(byte: int) -> int:
    """
    >>> count_bits(0b10101100)
    4
    >>> count_bits(0xFF)
    8
    >>> count_bits(0)
    0
    >>> count_bits(1)
    1
    """
    count = 0
    for i in range(8):
        count += byte & 1
        byte = byte >> 1

    return count


class BitErrorMeasure:
    def __init__(self, original: bytes, copy=False) -> None:
        self.original = np.frombuffer(original, dtype=np.ubyte)
        if copy:
            self.original = np.copy(self.original)

        self.n = len(self.original)

        # Create bit count lookup table
        self.bit_count_lookup = np.empty(256, dtype=int)
        for i in range(256):
            self.bit_count_lookup[i] = count_bits(i)

    def check_against(self, other_raw: bytes) -> t.Tuple[float, int, int]:
        other = np.frombuffer(other_raw, dtype=np.ubyte)

        n = len(other)
        if n != self.n:
            raise Exception("array to be checked is not the original size")

        total_bits = n * 8

        difference = np.bitwise_xor(other, self.original)
        counts = self.bit_count_lookup[difference]
        wrong_bits = np.sum(counts)

        return wrong_bits / total_bits, wrong_bits, total_bits


class SymErrorMeasure:
    def __init__(self, original: np.ndarray, copy=False) -> None:
        self.original = original
        if copy:
            self.original = np.copy(self.original)

    def check_against(self, other: np.ndarray) -> t.Tuple[float, int, int]:
        total = len(other)
        wrong = np.sum(self.original != other)

        return wrong / total, wrong, total
