from antenna_diversity import modulation, encoding, error, common, channel

import numpy as np
import matplotlib.pyplot as plt
import os
import math
import typing as t
import copy
import argparse


class Simulation:
    def __init__(self, modulator):
        self.modulator = modulator
        self.M = modulator.M

        self.symbolenc = encoding.SymbolEncoder(self.M)

        # Set in the future by methods
        self.snr: float = None
        self.data: bytes = None
        self.symbols: np.ndarray = None
        self.moded: np.ndarray = None
        self.symbols_hat: np.ndarray = None
        self.data_hat: bytes = None

    def fork(self) -> "Simulation":
        # Do a shallow copy
        return copy.copy(self)

    # TODO extend with Rayleigh
    def with_channel(self, symbol_snr: float) -> "Simulation":
        fork = self.fork()
        fork.snr = symbol_snr
        return fork

    def with_input_random(self, n) -> "Simulation":
        fork = self.fork()
        fork.data = os.urandom(n)
        fork.__input_hook()

        return fork

    def __input_hook(self):
        self.symbols = self.symbolenc.encode_msb(self.data)
        self.moded = self.modulator.modulate(self.symbols)

    def run(self):
        with_noise = self.moded + channel.AWGN(len(self.moded), self.snr)

        self.symbols_hat = self.modulator.demodulate(with_noise)
        self.data_hat = self.symbolenc.decode_msb(self.symbols_hat)

    def measure_biterror(self):
        return error.BitErrorMeasure(self.data).check_against(self.data_hat)

    def measure_symerror(self):
        return error.SymErrorMeasure(self.symbols) \
                .check_against(self.symbols_hat)


def run_simulation_til_faults(sim: Simulation, target_faults: int, chunk: int)\
        -> t.Tuple[float, float]:
    # [faults, total]
    sym_stats = np.zeros(2)
    bit_stats = np.zeros(2)
    while sym_stats[0] < target_faults:
        s = sim.with_input_random(chunk)
        s.run()

        # Only save the counts, and not prob
        sym_stats += np.array(s.measure_symerror()[1:3])
        bit_stats += np.array(s.measure_biterror()[1:3])

        print(f"\racc_sym[faults, total]:{sym_stats} ", end="")

    return sym_stats[0] / sym_stats[1], sym_stats[0] / sym_stats[1]


def run_for_snrs(sim: Simulation,
                 snrs: np.ndarray,
                 target_faults: int,
                 chunk: int):
    N = len(snrs)
    bit_probs = np.empty(N)
    sym_probs = np.empty(N)
    for i, snr in enumerate(snrs):
        with_snr = sim.with_channel(snr)
        res = run_simulation_til_faults(with_snr, target_faults, chunk)

        sym_probs[i], bit_probs[i] = res

        print(f"snr={snr}, bit_prob={res[1]}, sym_probs={res[0]}")

    return sym_probs, bit_probs


modulators = {
        "pam": modulation.PAM,
        "psk": modulation.PSK,
        }

parser = argparse.ArgumentParser()
parser.add_argument("-M", default=2, type=int,
                    help="which M to use for modulation")
parser.add_argument("-o", "--output", default="out.png",
                    help="where to save plot")
parser.add_argument("--until", default=100, type=int,
                    help="how many symbol faults for each snr")
parser.add_argument("-r", "--snr_range", nargs=2, default=[-10, 10],
                    type=int, help="range of symbol snr [db]")
parser.add_argument("-m", "--modulator", default="pam",
                    choices=modulators.keys(),
                    help="which modulation to use")

args = parser.parse_args()
print(args)

# ==============
# Setup vars
# ==============
M = args.M
snr_range = args.snr_range
mod = modulators[args.modulator](M, use_gray=True)

# ==============
# Setup X axises
# ==============
theo_snrs_db = np.linspace(snr_range[0], snr_range[1], 1000)
# We devide by four to get the SNR per bit, instead of per sumbol
theo_snrs_symbol = common.db_to_power(theo_snrs_db)
theo_snrs_bit = theo_snrs_symbol / math.log2(M)

sim_snrs_db = np.arange(snr_range[0], snr_range[1]+1)

# ==============
# Calculate probabilities
# ==============
theo_bit = mod.theo_bitprob(theo_snrs_bit)
theo_sym = mod.theo_symprob(theo_snrs_symbol)

simulator = Simulation(mod)

sim_sym, sim_bit = run_for_snrs(simulator, sim_snrs_db, args.until, 10000)

# ==============
# Plot probabilities
# ==============
fig, ax = plt.subplots(2)
ax[0].plot(theo_snrs_db, theo_sym, label="Theoretical")
ax[0].plot(sim_snrs_db, sim_sym, label="Simulated")
ax[0].set_xlabel("Symbol SNR [db]")
ax[0].set_ylabel("Symbol error probability")
ax[0].set_yscale("log")
ax[0].legend()

ax[1].plot(theo_snrs_db, theo_bit, label="Theoretical")
ax[1].plot(sim_snrs_db, sim_bit, label="Simulated")
ax[1].set_xlabel("Symbol SNR [db]")
ax[1].set_ylabel("Bit error probability")
ax[1].set_yscale("log")
ax[1].legend()

fig.tight_layout()
fig.savefig(args.output)
