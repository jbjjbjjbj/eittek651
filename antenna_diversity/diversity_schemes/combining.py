import numpy as np
from numpy.core.fromnumeric import transpose
from .. import channel 

#Assumptions:
#   slow or flat fading channel.
#   Rayleigh fading.
#   Signal x(t) has unit average power
#   SNR is instantaneous

def MRC(input, SNR, nr_antenna):
    x = input
    alpha = channel.rayleigh(nr_antenna)
    n = channel.AWGN(nr_antenna,SNR)
    #Cauchy-Schwarz inequality dictates when the SNR is defined as:
    # ((w hermitian alpha)^2)/σ2 the weight (w) has a maximum when it's
    # linearly proportional to alpha (https://www.comm.utoronto.ca/~rsadve/Notes/DiversityReceive.pdf)
    W = alpha
    #We can because W=alpha and both being hermitian w H alpha = w^2
    #(https://www.gaussianwaves.com/2020/01/receiver-diversity-maximum-ratio-combining-mrc/)
    #final result: y = w H y = w H alpha*x + w H n
    h = np.transpose(W)
    Wh = W.dot(h)
    n = np.transpose(np.array([n]))
    Wn = W.dot(n)

    y = Wh*x+Wn
    #Unfortunately it seems like my my complex conjugated and transpose method doesn't seem to work so
    #the noise here is wrong but im unsure how to fix it.
    return(y)


def EGC(input):
    x=input