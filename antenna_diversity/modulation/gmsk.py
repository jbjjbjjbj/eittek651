
import numpy as np
import typing as t
import matplotlib.pyplot as plt
import matplotlib
import math
from numpy.core.defchararray import array
from scipy.signal import upfirdn, lfilter


Tb = 1.152e6  # bit period of 1.152Mbps
BTb = 0.5  # bandwith bit period product of BTb = 0.5
deltaf = 288e3  # Nominal peak peak frequency deviation of 288 kHz
h = 2*deltaf/Tb
fc = 1.8e9  # carrier frequency
L = 16  # oversampling factor must satisfy nyquist sampling theorem


class SymErrorMeasure:
    def __init__(self, original: np.ndarray, copy=False) -> None:
        self.original = original
        if copy:
            self.original = np.copy(self.original)

    def check_against(self, other: np.ndarray) -> t.Tuple[float, int, int]:
        total = len(other)
        wrong = np.sum(self.original != other)

        return wrong / total, wrong, total


def gaussianLPF(BTb, Tb, L, k):  # craete gaussian low pass filter
    B = BTb/Tb  # bandwidth of the filter
    t = np.arange(start=-k*Tb, stop=k*Tb + Tb/L, step=Tb/L)
    h = B*np.sqrt(2*np.pi/(np.log(2)) *
                  np.exp(-2 * (t*np.pi*B)**2 / (np.log(2))))
    h_norm = h/np.sum(h)
    return h_norm


def modulate_gmsk_signal(bit_sequence):
    Ts = Tb/L
    fs = 1/Ts
    c_t = upfirdn(h=[1]*L, x=2*bit_sequence-1, up=L)

    k = 1  # truncation lenght for Gaussian LPF
    h_t = gaussianLPF(BTb, Tb, L, k)  # get gaussian Low Pass filter
    # convolve the -1,1 sequence with the gaussian filter to get the waveform of the phase
    b_t = np.convolve(h_t, c_t, 'full')
    # normalise such that the output is limited between -1 and 1
    bnorm_t = b_t/max(abs(b_t))

    # integrate over the output of the gaussian filter to get phase information
    phi_t = lfilter(b=[1], a=[1, -1], x=bnorm_t*Ts)*h*np.pi/Tb

    I = np.cos(phi_t)  # calculate the inphase
    Q = np.sin(phi_t)  # calculate the quadrature
    return I, Q


def demodulate_gmsk_signal(baseband_signal_I, baseband_signal_Q):
    Ts = Tb/L
    fs = 1/Ts

    z1 = baseband_signal_I * \
        np.hstack((np.zeros(L), baseband_signal_Q[0:len(baseband_signal_Q)-L]))
    z2 = baseband_signal_Q * \
        np.hstack((np.zeros(L), baseband_signal_I[0:len(baseband_signal_I)-L]))
    z = z1 - z2
    a_hat = (z[2*L-1:-L:L] < 0).astype(int)
    return a_hat


def gmsk_awgn(baseband_signal_I, baseband_signal_Q, snr):
    noiseI = np.random.normal(0, 1/snr*1/2)
    noiseQ = np.random.normal(0, 1/snr*1/2)
    I = baseband_signal_I+noiseI
    Q = baseband_signal_Q+noiseQ
    return I, Q


snr = np.arange(start=-25, stop=25+1, step=2.5)

bits_per_snr = 1000000

bit_error_prob = []

for i, gamma in enumerate(snr):
    print(gamma)
    gamma = 10**(gamma/10)
    test_bits = np.random.randint(0, 2, size=bits_per_snr)
    I, Q = modulate_gmsk_signal(test_bits)
    I, Q = gmsk_awgn(I, Q, gamma)
    hat_test_bits = demodulate_gmsk_signal(I, Q)
    SEM = SymErrorMeasure(test_bits)
    frac, errors, total = SEM.check_against(hat_test_bits)
    bit_error_prob.append(frac)

#plt.plot(snr, bit_error_prob)
plt.plot(snr, bit_error_prob, label="sim")
plt.legend()
plt.xlabel("snr (db)")
plt.yscale("log")
plt.savefig("hej.png")


test_bits = np.array([1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0])
I, Q = modulate_gmsk_signal(test_bits)
I, Q = gmsk_awgn(I, Q, 0.0001)

hat_test_bits = demodulate_gmsk_signal(I, Q)

# plt.plot(test_bits)
# plt.plot(hat_test_bits)
# plt.plot(I)
# plt.plot(Q)
# ax.plot(I_Q)
plt.show()
