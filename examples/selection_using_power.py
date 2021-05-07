"""
    This files main purpose is to test the selection diversity technique.

    We want to test wheter the simplification of just using the h for selection correspon to acctuarrly choosing the power of the signal
"""
import numpy as np
from numpy.core.defchararray import index
import ad_path
from antenna_diversity import modulation, channel, diversity_technique
import matplotlib.pyplot as plt
import h5py

bits_per_slot = 440
slot_per_frame = 1

gfsk = modulation.GFSK()
# get the oversampling factor from the gfsk module as it is used for the
# signal power calculations
points_per_bit = gfsk.L


def calculate_signal_power(signal):
    # check the power of the first 4 bits:
    signal_part = signal
    # Calculation is from page 160 in wireless communication systems in matlab
    signal_abs_squared = np.square(np.abs(signal_part))
    signal_power = 1 / len(signal_part) * np.sum(signal_abs_squared)
    # return the sum of the signal part squared.
    return signal_power


def real_selection(signal):
    sh = np.shape(signal)
    signal_powers = np.empty(shape=(sh[0]))
    for i, rows in enumerate(signal):
        signal_powers[i] = calculate_signal_power(rows)

    index = np.argmax(signal_powers)
    return signal[index], int(index)

# Make a frame constructed of how many bits there is per slot, and how
# many slots there is per frame


def make_frame_array():
    frameArray = np.empty(shape=(slot_per_frame, bits_per_slot))
    for i in range(slot_per_frame):
        frameArray[i] = np.random.randint(2, size=bits_per_slot)
    return frameArray


snr = np.arange(10, 17.5, 2.5)

branches = np.arange(1, 6, 1)
prob = np.empty(shape=(len(branches), len(snr)))
base_tries = 5000

errors = 0
numberOfTries = 0
ch = channel.RayleighAWGNChannel(N=2, snr=10)

tries = 1000
ind_1_arr = np.empty(shape=(tries))
ind_2_arr = np.empty(shape=(tries))

for ty in range(tries):
    fram = make_frame_array()
    for slot in fram:
        signal = gfsk.modulate(slot)
        recieved, h = ch.run(signal)
        hat_real_recieved, ind1 = real_selection(recieved)
        hat_recieved, ind2 = diversity_technique.selection_from_power(recieved)
        ind_1_arr[ty] = ind1
        ind_2_arr[ty] = ind2
        hat_slot = gfsk.demodulate(hat_recieved)
    ch.frame_sent()

plt.plot(ind_1_arr)
plt.plot(ind_2_arr)
plt.show()
