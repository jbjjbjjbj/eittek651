from .psk import PSK
import numpy as np


class MSK:
    def __init__(self, energy: float = 1):
        sqrte = np.sqrt(energy)
        self.constellation = np.array([
            sqrte, -sqrte, 1j * sqrte, -1j * sqrte
        ])

        self.M = 2

    def modulate(self, symbols: np.ndarray) -> np.ndarray:
        # Do vector encoding as described in lecture nodes
        # TODO Ohh wow this is terrible, fix it

        # Last bit in u does not carry information
        ubit = symbols
        n = len(ubit) + 1

        res = np.empty(n, dtype=np.ubyte)
        vbit = np.empty(n, dtype=np.ubyte)
        vbit[0] = 0
        for i in range(1, n):
            vbit[i] = vbit[i-1] ^ ubit[i-1]
            res[i-1] = (ubit[i-1] << 1) | vbit[i-1]
            pass

        res[n-1] = 0 if vbit[n-1] == 0 else 1

        return self.constellation[res]

    def demodulate(self, symbols: np.ndarray) -> np.ndarray:
        # First find the vbit
        def calc_z(y, n_scale):
            shifted = np.insert(y, 0, 0)[:-1]
            return y * n_scale + shifted

        z = calc_z(np.real(symbols), 1) - calc_z(np.imag(symbols), -1)

        vbit = (z < 0).astype(int)

        # Now run the reverse state machine thing
        vbit_shift = np.roll(vbit, -1)
        vbit_shift[-1] = 0

        ubit = np.bitwise_xor(vbit_shift, vbit)
        return ubit[:-1]
