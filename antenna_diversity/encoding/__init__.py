from .gray import GrayEncoder
from .symbolencoder import SymbolEncoder
import numpy.typing as npt


class NoEncoder:
    def encode(self, a: npt.ArrayLike) -> npt.ArrayLike:
        return a

    def decode(self, a: npt.ArrayLike) -> npt.ArrayLike:
        return a
