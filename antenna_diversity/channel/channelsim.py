from .noise import AWGN
from .fading import rayleigh

#This file is for the construced channel models(maybe the name of the file should be changed)
#The construced channel models (like the RayAWGNchannel function shown below) can be made in this file.
#Other channel models can be made below.

def rayawgnchannel(x,snr):
    alpha = rayleigh(x)
    W = AWGN(x,snr)
    y = alpha*x + W
    return y