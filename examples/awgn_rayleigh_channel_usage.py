# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT

from antenna_diversity import channel
import numpy as np
import matplotlib.pyplot as plt

N = 1000
# We create a channel with snr=10,
#   coherence_time=0.066,
#   bit_period=0.000868
#   and two diversity brances
# The coherence time and bit period were calculated from DECT
# and a indoor walking speed of 2.5 m/s
chnl = channel.RayleighAwgnChannel(10, 0.066, 0.000868, 2)

# Lets create a constant signal
stuff = np.repeat(1 + 2j, N)
recv, hs = chnl.attenuate(stuff)

# Lets just plot all the branches h values
# The h's are sampled with a T=0.000868
t = np.arange(N) * 0.000868
for h in hs:
    plt.plot(t, h)
