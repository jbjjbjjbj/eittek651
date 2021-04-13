import numpy as np
import math
import typing as t

# M = 2, 4, 16, 256
M_allowlist: t.List[int] = [2, 4, 16, 256]


def gen_mask(n: int) -> int:
    """
    >>> bin(gen_mask(3))
    '0b111'
    >>> bin(gen_mask(2))
    '0b11'
    >>> bin(gen_mask(8))
    '0b11111111'
    """
    return (1 << n) - 1


def mask_msb_first(byts: np.ndarray, n: int, index: int) -> np.ndarray:
    """
    Will mask out the index'th n bit from byts.
    Undefined behavior if 8 is not divisible by n

    >>> bin(mask_msb_first(0xDE, 2, 3))
    '0b10'
    >>> mask_msb_first(np.array([0xDE, 0xAD]), 2, 0)
    array([3, 2])
    >>> bin(mask_msb_first(0xDE, 2, 1))
    '0b1'
    >>> bin(mask_msb_first(0xDE, 4, 0))
    '0b1101'
    """
    max_index = int(8 // n)-1

    # Create a mask for index 0
    mask = gen_mask(n) << (8 - n)

    # Shift it in index times
    mask = mask >> (n * index)

    # Now extract result
    res = np.bitwise_and(byts, mask)

    # Move the res to LSB and return
    return res >> ((max_index - index) * n)


class SymbolEncoder:
    """
    Encodes a numpy list of bytes and returns them as symbols.
    Symbols can go from [0, M[, where a larger M will encode more bits in
    each symbol.

    Because of the underlying implementation M can only take
    the values 2,4,16,256

    Explanation:

    The encoder encodes using vectorized operations.
    This works by extracting bits from each element one bit at the time.

    ```python
    bits = np.bitwise_and(input, 1)
    ```

    This will extract the first bit of each byte.
    When working LSB first, we want these bits to map to each index `(i % 8)`.
    This is done by utilizing numpy matrixes, where we write each bit sequence
    to the row in a matrix corrosponding to the bit index.

    For example if we pull the first bit from each byte in input=[0xF5, 3] and
    save it to `bits`, we can place it in the first row of matrix:

    ```python
    [[1, 1],
     [0, 0],
     [0, 0],
     [0, 0],
     [0, 0],
     [0, 0],
     [0, 0],
     [0, 0]]
    ```

    If we do this for every bit we get:

    ```python
    dest = [[1, 1],
            [0, 1],
            [1, 0],
            [0, 0],
            [1, 0],
            [1, 0],
            [1, 0],
            [1, 0]]
    ```

    We can see that if we concat each column we get the correct bit sequence.
    This concatination is done with `dest.transpose().flatten()`.
    """

    def __init__(self, M: int) -> None:

        if M not in M_allowlist:
            raise Exception(f"SymbolEncoder created with unsupported M={M}")

        self.nbits = int(math.log2(M))

        self.syms_per_byte = int(8 // self.nbits)
        print(self.syms_per_byte)

    def encode(self, byts: np.ndarray) -> np.ndarray:
        dest = np.zeros([self.syms_per_byte, len(byts)])

        for i in range(self.syms_per_byte):
            # Take the nbits MSB, which forms symbols
            symbols = mask_msb_first(byts, self.nbits, i)

            # Save it to dest
            dest[i] = symbols

        # Now we extract the symbols
        symbols = dest.transpose().flatten()
        return symbols
