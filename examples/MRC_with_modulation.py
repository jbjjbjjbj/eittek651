# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT

from antenna_diversity.channel import AWGN
from antenna_diversity.channel import rayleigh
from antenna_diversity.diversity_schemes import MRC
from antenna_diversity.encoding import SymbolEncoder
from antenna_diversity import modulation
import numpy as np
from antenna_diversity.protocols import DECT
import ad_path

ad_path.nop()

#Create DECT packet
payload = b'0123456789012345678901234567890123456789'
dect_packet = DECT(2).create_full(payload)

#Modulate DECT packet
my_pam = modulation.PSK(2)
my_symbols = SymbolEncoder(2).encode_msb(dect_packet.to_bytes())
modulated_symbols = my_pam.modulate(my_symbols)

#Constructing the diversity schemes recieved signals
x = modulated_symbols, modulated_symbols, modulated_symbols
x = np.transpose(x)
r,c = x.shape #r for row and c for colum. We use colums because here they equal antennas/diversity branches  
h = np.transpose(rayleigh(c))
n = np.transpose(AWGN(c,-8))
r = h*x + n
r = np.transpose(r)

#Using the diversity scheme and demodulate the signal
mrc=MRC(r,h)
my_demodulate=my_pam.demodulate(mrc)
print(my_demodulate)
