import ad_path
from antenna_diversity import channel
import numpy as np
import matplotlib.pyplot as plt

ad_path.nop()

branches = 3
sampler = channel.RayleighAWGNChannel(branches, 10)

# Run a thausant of dect frames
runs = 100
frame_number = np.arange(runs)
res = np.empty((runs, branches))

signal = np.ones(1)
for i in frame_number:
    _, res[i] = sampler.run(signal)
    sampler.frame_sent()

plt.plot(frame_number, res)
plt.xlabel("Frame number")
plt.ylabel("Attenuation")
plt.title("Rayleigh samples")
plt.savefig("out2.png")
