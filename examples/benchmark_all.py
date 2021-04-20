#!/usr/bin/env python3
# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT

"""
This runs the different parts of antenna_diversity to make profiling easy
"""

import os

import ad_path
from antenna_diversity import modulation, encoding, channel, protocols, common

ad_path.nop()


M = 2
dect = protocols.DECT(M)
enc = encoding.SymbolEncoder(M)
mod = modulation.PSK(M)


def run_sim() -> bool:
    # Create random dect packet
    payload = os.urandom(40)
    data = dect.create_full(payload).to_bytes()

    # Run through simulation chain
    symbols = enc.encode_msb(data)
    moded = mod.modulate(symbols)
    recv = channel.rayleigh_awgn(moded, 10)
    symbols_hat = mod.demodulate(recv)
    data_hat = enc.decode_msb(symbols_hat)

    # Check it
    return dect.unpack_full(data_hat).check_crc()


num_packets = 10000

wrong = 0
with common.Timer() as t:
    for i in range(num_packets):
        wrong += int(run_sim())

        if i % 1000 == 0:
            print(i)

print(f"runtime: {t.get_duration()}, total: {num_packets}, wrong: {wrong}")
