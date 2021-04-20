# Copyright 2021 Christian Schneider Pedersen, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
from .noise import AWGN
from .fading import rayleigh

#This file is for the construced channel models
#The construced channel models (like the RayAWGNchannel function shown below) can be made in this file.
#Other channel models can be made below.

def rayleigh_awgn(x,snr):
    n = len(x)
    alpha = rayleigh(n)
    W = AWGN(n,snr)
    y = alpha*x + W
    return y
