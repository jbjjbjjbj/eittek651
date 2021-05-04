from pathlib import Path
import re
import h5py
import matplotlib.pyplot as plt
import numpy as np

threshold = 0.1

# Find data files
diversity_file_re = re.compile("diversity_(.*)\\.h5$")
data_files = []
for fname in Path.cwd().iterdir():
    match = diversity_file_re.search(str(fname))
    if match is not None:
        name = match.group(1)
        data_files.append((fname, name))

legends = []
for fname, name in data_files:
    print(f"Loading {name} data from {fname}")
    with h5py.File(fname, "r") as f:
        snr = f["snrs"][:]
        prob = f["probs"][:]

    branches = []
    snr_good_enough = []
    for branch in range(len(prob)):
        where_okay = np.where(prob[branch] < threshold)[0]
        if len(where_okay) == 0:
            continue
        branches.append(branch+1)
        snr_good_enough.append(snr[where_okay[0]])

    print("branches:", branches)
    print("snrs:", snr_good_enough)
    plt.plot(branches, snr_good_enough)
    legends.append(name)

plt.legend(legends)
plt.ylabel("SNR [dB]")
plt.xlabel("Branch")
plt.savefig("out.png")
