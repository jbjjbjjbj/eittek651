import numpy as np
from .. import channel 

#Assumptions:
#   slow or flat fading channel.
#   Rayleigh fading.
#   Signal x(t) has unit average power
#   SNR is instantaneous
#   I worry we have a problem with our SNR.

def MRC(input,SNR,antenna):
    x = input
    alpha = channel.rayleigh(antenna)
    n = channel.AWGN(antenna,SNR)
    #Cauchy-Schwarz inequality dictates when the SNR is defined as:
    # ((w hermitian alpha)^2)/σ2 the weight (w) has a maximum when it's
    # linearly proportional to alpha (https://www.comm.utoronto.ca/~rsadve/Notes/DiversityReceive.pdf)
    w=alpha
    #We can because W=alpha and both being hermitian w H alpha = w^2
    #(https://www.gaussianwaves.com/2020/01/receiver-diversity-maximum-ratio-combining-mrc/)
    w2=alpha*alpha
    #final result: y = w H y = w H alpha*x + w H n
    y = w2*x+np.conjugate(np.transpose(w))*n
    #Unfortunately it seems like my my complex conjugated and transpose method doesn't seem to work so
    #the noise here is wrong but im unsure how to fix it.
    
    return(y)


def EGC(input):
    x=input