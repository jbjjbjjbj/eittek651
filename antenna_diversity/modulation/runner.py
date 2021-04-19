from antenna_diversity import encoding, common, channel

import numpy as np
import matplotlib.pyplot as plt
import os
import math
import typing as t
import time
import pandas as pd



class Runner:
    def __init__(self, modulator, snrs: np.ndarray):
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

        received = moded + channel.AWGN(len(moded), snr)

        symbols_hat = self.modulator.demodulate(received)
        data_hat = self.symbolenc.decode_msb(symbols_hat)

        self.bit_stats += np.array(
                self.count_symbol_errors(symbols, symbols_hat)
                )
        self.sym_stats += np.array(
                self.count_bit_errors(data, data_hat)
                )

    def run_until_faults(self, target: int, snr: float) -> None:
        chunk = 10000
        while self.sym_stats[0] < target:
            start_time = time.time()

            data = os.urandom(chunk)
            self.feed_data(data, snr)

            duration = time.time() - start_time
            # Increase chunk if calculation was fast
            if duration < 0.5:
                chunk = chunk*2

            print(f"\racc_sym[faults, total]:{self.sym_stats} ", end="")

    def get_probabilities(self) -> t.Tuple[float, float]:
        return self.sym_stats[0] / self.sym_stats[1], \
            self.bit_stats[0] / self.bit_stats[1]

    @staticmethod
    def simulate_snrs(modulator, snrs: np.ndarray, target: int):
        runner = Runner(modulator, snrs)

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
            print(f"snr={snr}, sym_prob={sym_probs[i]}, bit_probs={bit_probs[i]}")

        return sym_probs, bit_probs

    @staticmethod
    def plot(modulator, snr_range: t.Tuple[int, int], target: int):
        # Setup vars
        M = modulator.M

        # Setup X axises
        snrs_db = np.arange(snr_range[0], snr_range[1]+1)
        # We devide by four to get the SNR per bit, instead of per sumbol
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
        df_bit.plot(ax=ax[0], logy=True, xlabel="Symbol SNR [dB]", ylabel="Bit Error Rate")
        df_sym.plot(ax=ax[1], logy=True, xlabel="Symbol SNR [dB]", ylabel="Symbol Error Rate")
        fig.tight_layout()
        fig.savefig("out.png")

    @staticmethod
    def count_bit_errors( a: bytes, b: bytes) -> t.Tuple[int, int]:
        a_np = np.frombuffer(a, dtype=np.ubyte)
        b_np = np.frombuffer(b, dtype=np.ubyte)

        n = common.shared_length(a_np, b_np)

        total_bits = n * 8

        difference = np.bitwise_xor(a_np, b_np)
        counts = bit_count_lookup[difference]
        wrong_bits = np.sum(counts)

        return wrong_bits, total_bits

    @staticmethod
    def count_symbol_errors(a: np.ndarray, b: np.ndarray) \
            -> t.Tuple[int, int]:

        n = common.shared_length(a, b)

        wrong = np.sum(a != b)

        return wrong, n


bit_count_lookup = np.empty(256, dtype=int)
for i in range(256):
    bit_count_lookup[i] = common.count_bits(i)
