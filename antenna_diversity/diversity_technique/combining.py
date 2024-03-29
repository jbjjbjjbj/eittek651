# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT

import numpy as np

# Assumptions:
#    slow or flat fading channel.
#    Rayleigh fading.
#    Signal x(t) has unit average power
#    SNR is instantaneous


def mrc(signals: np.ndarray, ray: np.ndarray) -> np.ndarray:
    # signals in this context is the recieved signals from n antennas/branches
    # with fading and noise: r=h*x+n.
    # Ray is the fading used to give MRC its weight.
    # The expected output y is the sum of all recieved signals weighted by w.
    r = signals
    h = ray

    # Cauchy-Schwarz inequality dictates when the SNR is defined as:
    # > ((w hermitian h)^2)/σ2 the weight (w) has a maximum when it's
    # > linearly proportional to h
    # (https://www.comm.utoronto.ca/~rsadve/Notes/DiversityReceive.pdf)
    W = np.transpose(h)

    # We can because W=h and both being hermitian w H h = w^2
    #   (https://www.gaussianwaves.com/2020/01/receiver-diversity-maximum-ratio-combining-mrc/)
    # Final result: y = w H y = w H h*x + w H n
    # We ignore the type as there are issues with the unkdown dimension of
    # signal and ray
    y = np.matmul(W, r)
    return y


def egc(signals: np.ndarray) -> np.ndarray:
    # signals in this context is the recieved signals from n antennas/branches
    # with fading and noise: r=h*x+n.
    # The expected output y is the sum of all recieved signals weighted by w.
    r = signals
    l = len(r)                       # Here we generate a r long vector
    w = np.ones(l)  # which get filled with 1s since e^j0=1
    w = np.transpose(w)
    # returned result: y = w H y = w H h*x + w H n
    y = np.matmul(w, r)
    return y
