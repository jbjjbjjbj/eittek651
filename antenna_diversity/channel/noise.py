import numpy as np
import math
from ..common import db_to_power

def AWGN(sizeofinput,snr):
    normsize = len(sizeofinput)
    sigma = math.sqrt((1/db_to_power(snr))/2)
    W = np.random.normal(size=normsize)*sigma + 1j*np.random.normal(size=normsize)*sigma
    return W