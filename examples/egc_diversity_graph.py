import numpy as np
import ad_path
from antenna_diversity import modulation, channel, diversity_technique, common
import matplotlib.pyplot as plt
import h5py

bits_per_slot = 440
slot_per_frame = 1

gfsk = modulation.GFSK()

# Make a frame constructed of how many bits there is per slot, and how
# many slots there is per frame


def make_frame_array():
    frameArray = np.empty(shape=(slot_per_frame, bits_per_slot))
    for i in range(slot_per_frame):
        frameArray[i] = np.random.randint(2, size=bits_per_slot)
    return frameArray


snr = np.arange(-10, 22.5, 2.5)

branches = np.arange(1, 6, 1)
prob = np.empty(shape=(len(branches), len(snr)))
base_tries = 5000

for j, branch in enumerate(branches):
    # tries is the number of runs
    tries = base_tries
    for i, gamma in enumerate(snr):
        # create channel with the curretn branch and snr
        ch = channel.RayleighAWGNChannel(N=branch, snr=gamma)
        errors = 0
        numberOfTries = 0
        # make it run extra tries if the snr is bigger then zero
        if gamma > 0:
            tries += 1000
        for k in range(tries):
            fram = make_frame_array()
            for slot in fram:
                signal = gfsk.modulate(slot)
                recieved, h = ch.run(signal)
                hat_recieved = diversity_technique.combining.egc(recieved)
                hat_slot = gfsk.demodulate(hat_recieved)
                err, n = common.count_symbol_errors(slot, hat_slot)
                errors += err
                numberOfTries += n
            ch.frame_sent()
        prob[j][i] = errors / numberOfTries
        print('snr', gamma, 'branch', branch, 'Prob:', prob[j][i])


legends = []

for i, branch in enumerate(branches):
    plt.plot(snr, prob[i])
    s = 'N = '
    s += str(branch)
    legends.append(s)

with h5py.File("diversity_egc.h5", "w") as f:
    f.create_dataset("probs", data=prob)
    f.create_dataset("snrs", data=snr)

plt.legend(legends)
plt.yscale('log')
plt.xlabel('SNR [dB]')
plt.ylabel('Bit Error Rate')
plt.grid(True)
# format axis to bigger to bigger font
plt.rc('font', size=20)  # controls default text size
plt.rc('axes', titlesize=20)  # fontsize of the title
plt.rc('axes', labelsize=20)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)  # fontsize of the x tick labels
plt.rc('ytick', labelsize=20)  # fontsize of the y tick labels
plt.rc('legend', fontsize=20)  # fontsize of the legend

plt.yscale('log')
plt.savefig('diversity_egc.pdf')
