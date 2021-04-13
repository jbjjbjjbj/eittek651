import numpy as np
import math

#This file is for housing different fading methods (like the rayleigh function below).
#Other fading function can be added later if needed

def rayleigh(sizeofinput):
    raysize = len(sizeofinput) #unsure if this is correct
    alpha = np.random.rayleigh(size = raysize,scale = 1/math.sqrt(2))
    return alpha