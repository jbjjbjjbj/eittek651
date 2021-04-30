import numpy as np
import ad_path
from antenna_diversity import modulation, channel, diversity_technique
import matplotlib.pyplot as plt
import h5py

bits_per_slot = 440
slot_per_frame = 1

gfsk = modulation.GFSK()

# Make a frame constructed of how many bits there is per slot, and how
# many slots there is per frame


def makeFrameArray():
    frameArray = np.empty(shape=(slot_per_frame, bits_per_slot))
    for i in range(slot_per_frame):
        frameArray[i] = np.random.randint(2, size=bits_per_slot)
    return frameArray


snr = np.arange(-10, 17.5, 2.5)

branches = np.arange(1, 6, 1)
prob = np.empty(shape=(len(branches), len(snr)))
base_tries = 1000

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
            tries += 100
        for k in range(tries):
            fram = make_frame_array()
            for slot in fram:
                signal = gfsk.modulate(slot)
                recieved, h = ch.run(signal)
                hat_recieved = diversity_technique.combining.egc(recieved)
                hat_slot = gfsk.demodulate(hat_recieved)
                err, n = modulation.Runner.count_symbol_errors(slot, hat_slot)
                errors += err
                numberOfTries += n
            ch.frame_sent()
        prob[j][i] = errors / numberOfTries
        print('snr', gamma, 'branch', branch, 'Prob:', prob[j][i])


for i, branch in enumerate(branches):
    plt.plot(snr, prob[i])

with h5py.File("diversity_egc.h5", "w") as f:
    f.create_dataset("probs", data=prob)
    f.create_dataset("snrs", data=snr)


plt.yscale('log')
plt.savefig('diversity_egc.pdf')
