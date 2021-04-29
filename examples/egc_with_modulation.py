# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import ad_path
from antenna_diversity.channel import channel_models
from antenna_diversity.diversity_technique import egc
from antenna_diversity.encoding import SymbolEncoder
from antenna_diversity import modulation
import numpy as np
from antenna_diversity.protocols import dect

ad_path.nop()

# Create DECT packet
payload = b'0123456789012345678901234567890123456789'
dect_packet = dect.Full(payload)

# Modulate DECT packet
my_pam = modulation.PSK(2)
my_symbols = SymbolEncoder(2).encode_msb(dect_packet.to_bytes())
modulated_symbols = my_pam.modulate(my_symbols)
N = 3

# Creating the channel with N antennas and 10 snr
chnl = channel_models.RayleighAWGNChannel(N, 10)
r, h = chnl.run(modulated_symbols)

# Using the diversity scheme and demodulate the signal
recv = egc(r)
my_demodulate = my_pam.demodulate(recv)
print(my_demodulate)

if np.array_equal(my_demodulate, my_symbols):
    print("it good")
else:
    print("it not good")
