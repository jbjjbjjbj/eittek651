import math


def gen_bits(nbits):
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

    def __init__(self, M):
        nbits = math.log2(M)
        assert nbits.is_integer(), f"M should be a power of 2, {M} is not"
        self.lookup = gen_bits(int(nbits))

    def encode(self, a):
        return self.lookup[a]

    def decode(self, a):
        return self.lookup.index(a)


