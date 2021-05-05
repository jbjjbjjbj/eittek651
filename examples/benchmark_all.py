#!/usr/bin/env python3
# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT

"""
This runs the different parts of antenna_diversity to make profiling easy
"""

import os
import time

import ad_path
from antenna_diversity import modulation, encoding, channel, \
        diversity_technique
from antenna_diversity.protocols import dect

ad_path.nop()


M = 2
enc = encoding.SymbolEncoder(M)
mod = modulation.PSK(M)

# Nice shorthand /s
chnl = channel.RayleighAWGNChannel(2, 10)


def run_sim() -> bool:
    # Create random dect packet
    payload = os.urandom(40)
    data = dect.Full(payload).to_bytes()

    # Run through simulation chain
    symbols = enc.encode_msb(data)
    moded = mod.modulate(symbols)
    recv, h = chnl.run(moded)
    combined, _ = diversity_technique.selection(recv, h)

    symbols_hat = mod.demodulate(combined)
    data_hat = enc.decode_msb(symbols_hat)

    chnl.frame_sent()

    # Check it
    return dect.Full.from_bytes(data_hat).a_field_crc_error_detected()


num_packets = 10000

wrong = 0
start = time.time()

for i in range(num_packets):
    wrong += int(run_sim())

    if i % 1000 == 0:
        print(i)

duration = time.time() - start

print(f"runtime: {duration}, total: {num_packets}, wrong: {wrong}")
