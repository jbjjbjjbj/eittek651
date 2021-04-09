from .. import encoding

import math
import numpy as np
import numpy.typing as npt

import typing as t

class ConstellationModulator:
    """
    The baseclass for all modulations utilizing constellations and minimum
    distance for modulation

    When extending, one must implement the "generate_constellation()" method
    """

    def __init__(self, M: int, use_gray: bool = True, energy: float = 1) -> None:
        # Set members
        self.M = M

        # Use gray encoder if user wants it
        self.encoder: t.Any = None
        if use_gray:
            self.encoder = encoding.GrayEncoder(M)
        else:
            self.encoder = encoding.NoEncoder()

        # Calculate the constellation
        d = math.sqrt(3 * energy / (self.M**2 - 1))
        self.constellation = np.array(self.generate_constellation()) * d

    def modulate(self, symbols: npt.ArrayLike) -> npt.ArrayLike:
        # make d scale mean symbol energy
        encoded = self.encoder.encode(symbols)
        return self.constellation[encoded]

    def demodulate(self, received: np.ndarray) -> np.ndarray:
        # There is a column for each constellation element and a row for each
        # "received".
        # This is important since it is best for C-style memory layout to
        # compare elements in a row as opposed to in a column.
        distances = np.abs(np.subtract.outer(received, self.constellation))
        estimated_symbols = np.argmin(distances, 1)
        return self.encoder.decode(estimated_symbols)

    def generate_constellation(self) -> t.List[int]:
        # Just create a dummy constellation
        raise Exception(f"Dummy constellation generator not overwritten by {self.__class__.__name__}")
        return np.zeros(self.M)
