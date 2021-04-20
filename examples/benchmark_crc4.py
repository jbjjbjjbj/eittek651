#!/usr/bin/env python3
# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT

import os

import ad_path
from antenna_diversity.protocols.dect import dect_4bit_crc, dect_4bit_crc_old
from antenna_diversity.common import Timer

ad_path.nop()


values = [b'hej med dig', bytes.fromhex("deadbeef"), b'1', b'fdsfasdfds']
for val in values:
    print(val, dect_4bit_crc(val), dect_4bit_crc_old(val))

runs = 100
chunk = 1000


def run_crc(impl, name):
    with Timer() as t:
        for i in range(runs):
            payload = os.urandom(chunk)

            _ = impl(payload)

            if i % 10 == 0:
                print(i)

    print(f"{name}, duration:", t.get_duration() / runs)


run_crc(dect_4bit_crc, "new")
run_crc(dect_4bit_crc_old, "old")

