# Copyright 2021 Christian Schneider Pedersen, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import math
from typing import List
import numpy as np
from numpy.typing import ArrayLike


def gen_bits(nbits: int) -> List[int]:
    """
    example:
    >>> gen_bits(2)
    [0, 1, 3, 2]
    """
    if nbits == 1:
        return [0, 1]
    previous = gen_bits(nbits - 1)
    reverse = reversed(previous)
    # prefix bytes with 1, e.g. 01 becomes 101
    reverse = map(lambda v: (1 << (nbits - 1)) | v, reverse)
    return previous + list(reverse)


class GrayEncoder:

    def __init__(self, M: int) -> None:
        nbits = math.log2(M)
        assert nbits.is_integer(), f"M should be a power of 2, {M} is not"
        self.lookup_encode = np.array(gen_bits(int(nbits)))

        self.lookup_decode = np.empty(len(self.lookup_encode))
        for i, element in enumerate(self.lookup_encode):
            self.lookup_decode[element] = i

    def encode(self, a: ArrayLike) -> ArrayLike:
        return self.lookup_encode[a]

    def decode(self, a: ArrayLike) -> ArrayLike:
        return self.lookup_decode[a]


