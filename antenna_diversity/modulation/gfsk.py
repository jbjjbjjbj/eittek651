import numpy as np
import typing as t
from scipy import signal
from scipy.signal import upfirdn, lfilter


class GFSK():
    """
        GFSK is a special case of GFSK where h = 0.5 -> h is calculated from the frequency peak difference.
    """

    def __init__(self, bitrate=1.152e6, BTb=0.5, deltaf=288e3*2, fc=1.88e9, L=32) -> None:
        """
            Default values originate from the DECT standard - ETSI EN 300175-2
        """
        # setup parameters for gfsk
        self.Fb = bitrate  # biterate
        self.Tb = 1/self.Fb  # bit time
        self.BTb = BTb  # bandwith bit product
        self.deltaf = deltaf  # peak frequency deviation
        self.fc = fc  # carrier frequency
        self.L = L  # oversampling factor
        self.h = deltaf*self.Tb  # modulation index
        self.fs = L*self.Fb  # sample frequency
        self.Ts = 1/self.fs  # sample period
        self.B = BTb/self.Tb  # bandwith from Bandwith bit time product.

    def print_parameters(self):
        """
           Prints all the GFSK parameteres             
        """
        print("Fb:", self.Fb, "TB:", self.Tb)
        print("BTb:", self.BTb)
        print("Delta peak frequency deltaf:", self.deltaf)
        print("fc:", self.fc)
        print("Modulation index h:", self.h)
        print("Bandwith B:", self.B)
        print("Oversampling:", self.L)
        print("Sampling frequency - fs:", self.fs, " Ts:", self.Ts)

    def gaussianLPF(self):
        """
            Gaussian low pass filter see page 100 in "digital modulations using python ebook" for explemnation
            return the 
        """
        # make time samples
        t = np.arange(start=-1*self.Tb, stop=1*self.Tb +
                      self.Tb/self.L, step=self.Tb/self.L)
        # make the filter coefficiens h
        h = self.B*np.sqrt(2*np.pi/(np.log(2))) * \
            np.exp(-2 * (t*np.pi*self.B)**2 / (np.log(2)))
        # normalize the filter coefficeins
        h_norm = h/np.sum(h)
        return h_norm

    def modulate(self, bit_sequence):
        """
            GFSK modulate a bit sequence
            Returns signal complex QI signal
        """
        # upsample the bit_sequence, and make et NRZ (i.e. {0,1}-> {-1,1})
        c_t = upfirdn(h=[1]*self.L, x=2*bit_sequence-1, up=self.L)
        h_t = self.gaussianLPF()
        # convolve the gaussian filter with the NRZ sequence
        b_t = np.convolve(h_t, c_t, 'full')
        # normalize the b_t sequence to be between -1 and 1
        bnorm_t = b_t/max(abs(b_t))
        # Integrate over the output of the gaussian filter to get phase information
        # using lfilter makes a low pass filter, corresponding to integrating
        phi_t = lfilter(b=[1], a=[1, -1], x=bnorm_t *
                        self.Ts)*self.h*np.pi/self.Tb
        # calculate inphase and quadrature for baseband signal
        I = np.cos(phi_t)
        Q = np.sin(phi_t)
        # make complex baseband signal
        s_bb = I-1j*Q
        return s_bb

    def demodulate(self, signal_sequence):
        """
            Demodulate GFSK modulated complex baseband signal
            See page 105-107 in "digital modulations using python ebook" for explemnation
        """
        I = np.real(signal_sequence)
        Q = -1*np.imag(signal_sequence)
        z1 = I * np.hstack((np.zeros(self.L), Q[0:len(Q)-self.L]))
        z2 = Q * np.hstack((np.zeros(self.L), I[0:len(I)-self.L]))
        z = z1 - z2
        a_hat = (z[2*self.L-1:-self.L:self.L] < 0).astype(int)
        return a_hat

    def __str__(self):
        return "Gausian Frequency Shift Keying"
