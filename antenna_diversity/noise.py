import numpy as np
import math
from .common import db_to_power

def AWGN(x,snr):
    normsize=len(x)
    variance=(1/db_to_power(snr))/2
    W=np.random.normal(size=normsize)*math.sqrt(variance) + 1j*np.random.normal(size=normsize)*math.sqrt(variance)
    y=x+W
    return y