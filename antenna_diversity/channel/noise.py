# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import numpy as np
import math
from ..common import db_to_power

# This file is for housing our noise models (like the AWGN function below).
# Other fuctions could be added later if needed.

# Implementation of AWGN for GMSK, might be connected with the normal AWGN
# - was in doubt about how it worked..... - Mikkel


def AWGN(nrElementOut, snr: float) -> np.ndarray:
    sigma = math.sqrt((1 / db_to_power(snr)) * 1 / 2)
    W = np.random.standard_normal(size=nrElementOut) * sigma + \
        1j * np.random.standard_normal(size=nrElementOut) * sigma
    return W


def AWGN_Matrix(rows: int, columns: int, snr: float) -> np.ndarray:
    """
        Takes in number of rows and columns
        returns a matrix with size: rows x columns with complex normal
        distributed variables
    """
    W = np.empty(shape=(rows, columns), dtype=complex)
    sigma = math.sqrt((1 / db_to_power(snr)) * 1 / 2)
    for row in range(rows):
        W[row] = np.random.standard_normal(size=columns) * sigma + \
            1j * np.random.standard_normal(size=columns) * sigma
    return W
