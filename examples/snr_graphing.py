import ad_path
import typing as t
import numpy as np
import os
from antenna_diversity import encoding, common, channel, diversity, modulation
import matplotlib.pyplot as plt
import multiprocessing as mp


ad_path.nop()

class SimContext:
    def __init__(self, branches):
        self.modulator = modulation.PSK(2)
        self.symbolenc = encoding.SymbolEncoder(2)
        self.branches = branches

    def gen_with_snr(self, snr) -> t.Generator[t.Tuple[int, int], None, None]:
        chnl = channel.RayleighAWGNChannel(self.branches, snr)

        while True:
            yield self.run(chnl)

    def run(self, chnl) -> t.Tuple[int, int]:
        # TODO 10000 bits is arround 1 frame
        chunk = int(11520 / 8)

        data = os.urandom(chunk)

        symbols = self.symbolenc.encode_msb(data)
        moded = self.modulator.modulate(symbols)

        recv, h = chnl.run(moded)
        # recv = moded * self.channel.h[0] + channel.AWGN(len(moded), self.channel.snr)

        recv = diversity.selection(recv, h)

        symbols_hat = self.modulator.demodulate(recv[0])
        data_hat = self.symbolenc.decode_msb(symbols_hat)

        chnl.frame_sent()

        return common.count_bit_errors(data_hat, data)

    def run_until_faults(self, snr: float) -> float:
        sim_gen = self.gen_with_snr(snr)
        # wrong, total
        bit_stats = np.zeros(2)

        run = 0
        while run < 1:
            bit_stats += np.array(next(sim_gen))
            run += 1

        prob = bit_stats[0] / bit_stats[1]
        print(f"branches: {self.branches}, snr: {snr}, prob={prob}")
        return prob


def run_through_snrs(ctx: SimContext, snrs: np.ndarray, worker_pool) \
        -> np.ndarray:
    res = worker_pool.map_async(ctx.run_until_faults, snrs).get()
    print(res)

    return res


if __name__ == "__main__":
    worker_pool = mp.Pool(processes=mp.cpu_count())

    snrs = np.arange(-10, 10+1)
    for branches in [1, 2]:
        ctx = SimContext(branches)

        probs = run_through_snrs(ctx, snrs, worker_pool)

        plt.plot(snrs, probs, label=f"{branches} branches")

    plt.yscale("log")
    plt.ylabel("BER")
    plt.xlabel("Symbol SNR [dB]")
    plt.legend()
    plt.savefig("out.png")
