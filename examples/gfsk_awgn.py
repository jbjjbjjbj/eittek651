import numpy as np
import ad_path
from antenna_diversity import modulation, channel
import matplotlib.pyplot as plt
import h5py

ad_path.nop()

gfsk = modulation.GFSK()
gfsk.print_parameters()
chunkSize = 10000
errorBar = 100


def run_gfsk_simulation(snr):
    u = np.random.randint(2, size=chunkSize)
    s = gfsk.modulate(u)
    w = channel.noise.AWGN(len(s), snr=snr)
    r = s + w
    hat_U = gfsk.demodulate(r)
    wrong, n = modulation.runner.Runner.count_symbol_errors(u, hat_U)
    return wrong, n


snr = np.arange(-5, 16, 2)

prob = np.empty(len(snr))
for i, gamma in enumerate(snr):
    print(gamma)
    w_t, n = run_gfsk_simulation(snr=gamma)
    num_wrong = w_t
    number = n
    while(num_wrong < 1000 and number < chunkSize * 1000):
        w_t, n = run_gfsk_simulation(snr=gamma)
        num_wrong += w_t
        number += n
    prob[i] = (num_wrong / number)


book_snr = np.array([0, 2, 4, 6, 8, 10, 12])
book_prob = np.array([0.2, 0.1, 0.08, 0.03, 0.007, 0.0009, 0.00002])

with h5py.File("gfsk_awgn.h5", "w") as f:
    f.create_dataset("probs", data=prob)
    f.create_dataset("snrs", data=snr)

plt.plot(snr, prob)
plt.scatter(book_snr, book_prob, color='r')
plt.xlabel("snr [dB]")
plt.ylabel("Error probability")
plt.legend(["Simulation", "Viswanathan"])
plt.semilogy()
plt.savefig("out.png")
