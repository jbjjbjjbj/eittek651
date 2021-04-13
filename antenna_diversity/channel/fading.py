import numpy as np
import math

def rayleigh(sizeofinput):
    raysize = len(sizeofinput) #unsure if this is correct
    alpha = np.random.rayleigh(size = raysize,scale = 1/math.sqrt(2))
    return alpha