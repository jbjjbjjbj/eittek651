from antenna_diversity import common
from antenna_diversity.channel.fading import rayleigh
from antenna_diversity.channel import channel_models
import numpy as np
from numpy.core.fromnumeric import size, transpose
from .. import channel

# Assumptions:
#   slow or flat fading channel.
#   Rayleigh fading.
#   Signal x(t) has unit average power
#   SNR is instantaneous


class SEL:
    def __init__(self) -> None:
        pass

    @staticmethod
    def selective(signal, snr, nr_antenna):
        """
            Function only operate on one package with each indepent channel being coherrent.

            nr_antenna: number of branches
            SNR: signal to noise ration [db]
            signal: unit input signal 
        """
        # Make h for each channel
        h = channel.fading.rayleigh(nr_antenna)
        print(h)
        # multiply snr of each channel
        new_snr = common.db_from_power(h) + snr
        print(new_snr)
        # get the argument for the highest snr
        bedst_h = np.argmax(new_snr)
        print(bedst_h)
        # get the snr at that argument
        bedst_snr = h[bedst_h]
        print(bedst_snr)
        # make awgn component from the bedst snr
        w = channel.noise.AWGN(len(signal), bedst_snr)
        out_signal = signal+w
        return out_signal, h, bedst_h
