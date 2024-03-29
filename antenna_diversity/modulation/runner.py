# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
from antenna_diversity import encoding, common, channel

import numpy as np
import matplotlib.pyplot as plt
import os
import math
import typing as t
import time
import pandas as pd



class Runner:
    """
    Runs the selected instantiated modulator for different snr's.

    Tests are run until a satisfactory number of errors are found.
    Main functionality should happen through the static `plot` and
    `simulate_snrs` methods.
    """

    def __init__(self, modulator):
        self.modulator = modulator
        self.M = modulator.M

        self.symbolenc = encoding.SymbolEncoder(self.M)

        self.reset_counts()

    def reset_counts(self):
        # [faults, total]
        self.sym_stats = np.zeros(2)
        self.bit_stats = np.zeros(2)

    def feed_data(self, data, snr) -> None:
        symbols = self.symbolenc.encode_msb(data)
        moded = self.modulator.modulate(symbols)

        received = moded + channel.awgn(len(moded), snr)

        symbols_hat = self.modulator.demodulate(received)
        data_hat = self.symbolenc.decode_msb(symbols_hat)

        self.bit_stats += np.array(
                common.count_symbol_errors(symbols, symbols_hat)
                )
        self.sym_stats += np.array(
                common.count_bit_errors(data, data_hat)
                )

    def run_until_faults(self, target: int, snr: float) -> None:
        chunk_size = 10000
        while self.sym_stats[0] < target:
            start_time = time.time()

            data = os.urandom(chunk_size)
            self.feed_data(data, snr)

            duration = time.time() - start_time
            # Increase chunk_size if calculation was fast
            if duration < 0.5:
                chunk_size = chunk_size*2

            print(f"\racc_sym[faults, total]:{self.sym_stats} ", end="")

    def get_probabilities(self) -> t.Tuple[float, float]:
        return self.sym_stats[0] / self.sym_stats[1], \
            self.bit_stats[0] / self.bit_stats[1]

    @staticmethod
    def simulate_snrs(modulator, snrs: np.ndarray, target: int):
        runner = Runner(modulator)

        N = len(snrs)
        bit_probs = np.empty(N)
        sym_probs = np.empty(N)
        for i, snr in enumerate(snrs):
            try:
                runner.run_until_faults(target, snr)
            except KeyboardInterrupt:
                print(f"\nInterrupted simulation of snr={snr}")

            sym_probs[i], bit_probs[i] = runner.get_probabilities()
            runner.reset_counts()
            print(f"snr={snr}, sym_prob={sym_probs[i]}, \
                    bit_probs={bit_probs[i]}")

        return sym_probs, bit_probs

    @staticmethod
    def plot(modulator, snrs_db: np.ndarray, target: int):
        # Setup vars
        M = modulator.M

        # Setup X axises
        snrs_symbol = common.db_to_power(snrs_db)
        snrs_bit = snrs_symbol / math.log2(M)

        # Calculate probabilities
        theo_bit = modulator.theoretical_bitprob(snrs_bit)
        theo_sym = modulator.theoretical_symprob(snrs_symbol)

        sim_sym, sim_bit = Runner.simulate_snrs(
                modulator, snrs_db, target)

        # Plot probabilities
        df_bit = pd.DataFrame(
                index=snrs_db,
                data={"Theoretical": theo_bit, "Simulated": sim_bit}
                )
        df_sym = pd.DataFrame(
                index=snrs_db,
                data={"Theoretical": theo_sym, "Simulated": sim_sym}
                )
        fig, ax = plt.subplots(2)
        df_bit.plot(ax=ax[0], logy=True, xlabel="Symbol SNR [dB]",
                    ylabel="Bit Error Rate")
        df_sym.plot(ax=ax[1], logy=True, xlabel="Symbol SNR [dB]",
                    ylabel="Symbol Error Rate")
        fig.tight_layout()
        return fig
