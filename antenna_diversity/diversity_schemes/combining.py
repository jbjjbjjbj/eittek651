import numpy as np
from numpy.core.fromnumeric import transpose
from .. import channel 

#Assumptions:
#   slow or flat fading channel.
#   Rayleigh fading.
#   Signal x(t) has unit average power
#   SNR is instantaneous

def MRC(input, ray):
    r = input
    h = ray
    #Cauchy-Schwarz inequality dictates when the SNR is defined as:
    # ((w hermitian h)^2)/σ2 the weight (w) has a maximum when it's
    # linearly proportional to h (https://www.comm.utoronto.ca/~rsadve/Notes/DiversityReceive.pdf)
    W = np.transpose(h)
    #We can because W=h and both being hermitian w H h = w^2
    #(https://www.gaussianwaves.com/2020/01/receiver-diversity-maximum-ratio-combining-mrc/)
    #final result: y = w H y = w H h*x + w H n
    y = W.dot(r)
    return(y)
