import os
import time
import ad_path

import antenna_diversity.modulation as modulation
import antenna_diversity.channel as channel
import numpy as np


np.random.seed(0)

channel = channel.TheChannel(N=2, snr=0)
channel.print_parameters()
# test_sequence = np.random.rand(10)*10+0j
test_sequence = np.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=complex)

print("test:", test_sequence)
hat_test_sequence = channel.run(test_sequence)
print("hat_test_seqeunce\n", hat_test_sequence)
print("hat_test_sequence[0]\n", hat_test_sequence[0])

print("hat_test_sequence[1]\n", hat_test_sequence[1])
channel.print_parameters()
for i in range(10):
    channel.frame_sendt()
    channel.print_parameters()
