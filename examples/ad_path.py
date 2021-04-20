# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT

# This pretends as if it were the antenna_diversity module
import os
import sys
from pathlib import Path

filepath = Path(os.path.realpath(__file__))
sys.path.append(str(filepath.parent.parent))


def nop():
    pass
