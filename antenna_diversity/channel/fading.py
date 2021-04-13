from .noise import AWGN
import numpy as np
import math

def rayawgnchannel(x,snr):
    raysize = len(x) #unsure if this is correct
    alpha = np.random.rayleigh(size = raysize,scale = 1/math.sqrt(2))
    W = AWGN(x,snr)
    y = alpha*x + W
    return y