import ad_path
from antenna_diversity import channel
import numpy as np
import matplotlib.pyplot as plt
import math
ad_path.nop()


def calculate_db(input):
    return 10 * math.log10(input)


branches = 3
sampler = channel.RayleighAWGNChannel(branches, 10)

# Run a thausant of dect frames
runs = 100
frame_number = np.arange(runs)
res = np.empty((runs, branches))
resDb = np.empty((runs, branches))

signal = np.ones(1)
for i in frame_number:
    _, result = sampler.run(signal)
    res[i] = result
    for j, br in enumerate(result):
        resDb[i][j] = calculate_db(br)
    sampler.frame_sent()


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))


ax1.plot(frame_number, res, linewidth=0.75)
ax2.plot(frame_number, resDb, linewidth=0.75)
ax1.set_xlabel('Sample number [-]')
ax2.set_xlabel('Sample number [-]')


ax1.set_ylabel('Channel h factor [-]')
ax2.set_ylabel('Channel h factor [dB]')

plt.tight_layout()
plt.savefig("dect_frame_h_graphing.pdf")
plt.show()
