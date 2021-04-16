import numpy as np
import math
from ..common import db_to_power

# This file is for housing our noise models (like the AWGN function below).
# Other fuctions could be added later if needed.


def AWGN(sizeofinput, snr):
    sigma = math.sqrt((1/db_to_power(snr))/2)
    W = np.random.normal(size=sizeofinput)*sigma + 1j * \
        np.random.normal(size=sizeofinput)*sigma
    return W


# Implementation of AWGN for GMSK, might be connected with the normal AWGN - was in doubt about how it worked..... - Mikkel
def AWGN_GMSK(nrElementOut, snr):
    sigma = math.sqrt((1/db_to_power(snr))*1/2)
    W = np.random.standard_normal(
        size=nrElementOut)*sigma+1j*np.random.standard_normal(size=nrElementOut)*sigma
    return W
