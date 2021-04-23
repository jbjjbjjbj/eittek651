import os
import time
import ad_path

import antenna_diversity.modulation as modulation
import antenna_diversity.channel as channel
import numpy as np

"""
    This files demonstrates how to use
    the TheChannel class for simulating and rayleight + AWGN channel


"""
# set random seed for getting same random returns
np.random.seed(0)

# construct a channel object called the channel, with N = 2 branches, snr
# 0 [dB]
channel = channel.RayleighAWGNChannel(N=2, snr=0)

# print parameters just to see the other deafault values
# the class instantly creates the first channel h parameters
channel.print_parameters()

# make a test sequence, this will normally be the modulate signal.
test_sequence = np.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=complex)
print("test:", test_sequence)

# run the test sequence throught the channel
hat_test_sequence = channel.run(test_sequence)

# as there are two branches hat_test_sequence will return a 2 x
# len(test_sequence) array (a matrix)
print("hat_test_seqeunce\n", hat_test_sequence)

# prints the samples of each branch independ
print("hat_test_sequence[0]\n", hat_test_sequence[0])
print("hat_test_sequence[1]\n", hat_test_sequence[1])

# After the whole frame have been throught the channel, ,
# call frame_sendt() to update the channel
# The channel will automatically update to the next block
# after 6 frames have been sendt
channel.print_parameters()
for i in range(10):
    channel.frame_sendt()
    channel.print_parameters()
