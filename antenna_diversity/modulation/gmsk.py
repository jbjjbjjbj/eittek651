import numpy as np
import typing as t
import matplotlib.pyplot as plt
import matplotlib
import math
from scipy import signal
from scipy.signal import upfirdn, lfilter


# Fb = 1.152e6  # bit frequence (bit rate) of 1.152Mbps
# Tb = 1/Fb  # bit time 1/Fb
# print("real", Tb)
# BTb = 0.5  # bandwith bit period product of BTb = 0.5
# deltaf = 288e3*2  # Nominal peak peak frequency deviation of 288 kHz
# h = deltaf*Tb
# print("h", h)
# fc = 1.8e9  # carrier frequency
# L = 32  # oversampling factor must satisfy nyquist sampling theorem


class SymErrorMeasure:
    def __init__(self, original: np.ndarray, copy=False) -> None:
        self.original = original
        if copy:
            self.original = np.copy(self.original)

    def check_against(self, other: np.ndarray) -> t.Tuple[float, int, int]:
        total = len(other)
        wrong = np.sum(self.original != other)

        return wrong / total, wrong, total


class GMSK():
    def __init__(self, bitrate=1.152e6, BTb=0.5, deltaf=288e3*2, fc=1.88e9, L=32) -> None:
        # setup parameters for gmsk
        self.Fb = bitrate
        self.Tb = 1/self.Fb  # bit time
        self.BTb = BTb  # bandwith bit product
        self.deltaf = deltaf  # peak frequency deviation
        self.fc = fc  # carrier frequency
        self.L = L  # oversampling factor
        self.h = deltaf*self.Tb  # modulation index
        self.fs = L*self.Fb  # sample frequency
        self.Ts = 1/self.fs  # sample period
        self.B = BTb/self.Tb

    def print_parameters(self):
        """
           Prints all the GMSK parameteres             
        """
        print("Fb:", self.Fb, "TB:", self.Tb)
        print("BTb:", self.BTb)
        print("Delta peak frequency deltaf:", self.deltaf)
        print("fc:", self.fc)
        print("Modulation index h:", self.h)
        print("Bandwith B:", self.B)
        print("Oversampling:", self.L)
        print("Samplin - fs:", self.fs, " Ts:")

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
            GMFSK modulate a bit sequence
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
            Demodulate GMSK modulated complex baseband signal
            See page 105-107 in "digital modulations using python ebook" for explemnation
        """
        I = np.real(signal_sequence)
        Q = -1*np.imag(signal_sequence)
        z1 = I * np.hstack((np.zeros(self.L), Q[0:len(Q)-self.L]))
        z2 = Q * np.hstack((np.zeros(self.L), I[0:len(I)-self.L]))
        z = z1 - z2
        a_hat = (z[2*self.L-1:-self.L:self.L] < 0).astype(int)
        return a_hat


# def modulate_gmsk_signal(bit_sequence):
#     fs = L*Fb
#     Ts = 1/fs
#     #Tb = L*Ts
#     # Ts = Tb*L  # set sample time to L times bit time Tb
#     # convert to from bit sequence 1 and 0 to NRZ sequence -1 and 1
#     c_t = upfirdn(h=[1]*L, x=2*bit_sequence-1, up=L)
#     # plt.plot(c_t)
#     k = 1  # truncation lenght for Gaussian LPF
#     h_t = gaussianLPF(BTb, Tb, L, k)  # get gaussian Low Pass filter
#     # convolve the -1,1 sequence with the gaussian filter to get the waveform of the phase
#     b_t = np.convolve(h_t, c_t, 'full')

#     # normalise such that the output is limited between -1 and 1
#     bnorm_t = b_t/max(abs(b_t))
#     # plt.plot(bnorm_t)

#     # integrate over the output of the gaussian filter to get phase information
#     phi_t = lfilter(b=[1], a=[1, -1], x=bnorm_t*Ts)*h*np.pi/Tb
#     I = np.cos(phi_t)  # calculate the inphase
#     Q = np.sin(phi_t)  # calculate the quadrature
#     return I, Q


# def demodulate_gmsk_signal(baseband_signal_I, baseband_signal_Q):
#     z1 = baseband_signal_I * \
#         np.hstack((np.zeros(L), baseband_signal_Q[0:len(baseband_signal_Q)-L]))
#     z2 = baseband_signal_Q * \
#         np.hstack((np.zeros(L), baseband_signal_I[0:len(baseband_signal_I)-L]))
#     z = z1 - z2
#     a_hat = (z[2*L-1:-L:L] < 0).astype(int)
#     return a_hat


# def gmsk_awgn(baseband_signal_I, baseband_signal_Q, snr):
#     noise = AWGN(len(baseband_signal_Q), snr)
#     w_real = np.real(noise)
#     w_imag = np.imag(noise)
#     I = baseband_signal_I+w_real
#     Q = baseband_signal_Q+w_imag
#     return I, Q


# test = np.array([0.0, 1.0, 2, 3, 2, 1, 0, -1, -2, -
#                  3, 2, 1, 3, 2, -4, -5, 6, -4, -5])
# lfilter_res = lfilter(b=[1], a=[1, -1], x=test)
# print('lfilter:', lfilter_res)
# integrated = integrator(test)
# print('integrator', integrated)
# plt.plot(test)
# plt.plot(integrated, '.')
# plt.plot(lfilter_res, '-.')

# bit_error_prob = []

# test_bits = np.array([1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0])
# I, Q = modulate_gmsk_signal(test_bits)
# I, Q = gmsk_awgn(I, Q, 0.0001)

# hat_test_bits = demodulate_gmsk_signal(I, Q)

# plt.plot(test_bits)
# plt.plot(hat_test_bits)
# plt.plot(I)
# plt.plot(Q)
# ax.plot(I_Q


# def gaussianLPF(BTb, Tb, L, k):  # craete gaussian low pass filter
#     B = BTb/Tb  # bandwidth of the filter
#     print(B, L)
#     print("Tb", Tb)
#     t = np.arange(start=-k*Tb, stop=k*Tb + Tb/L, step=Tb/L)
#     h = B*np.sqrt(2*np.pi/(np.log(2))) * \
#         np.exp(-2 * (t*np.pi*B)**2 / (np.log(2)))
#     h_norm = h/np.sum(h)
#     # bit_sequence = np
#     # delta = np.array([1])
#     # test = np.convolve(delta, h_norm)
#     # plt.plot(test)
#     return h_norm
