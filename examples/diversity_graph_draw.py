from pathlib import Path
import numpy as np
import re
import h5py
import matplotlib.pyplot as plt
import typing as t

diversity_file_re = re.compile("diversity_(.*)\\.h5$")
output_default = "diversity_all.pdf"

# Find diversity files in current dir
data_files = []
for fname in Path.cwd().iterdir():
    match = diversity_file_re.search(str(fname))
    if match is not None:
        name = match.group(1)
        data_files.append((fname, name))

# Get user settings
print("Found data files:")
for i, (_, name) in enumerate(data_files):
    print(f"  {i}: {name}")

choise_str = input("Select dataset by number: ")
choise = int(choise_str)

sel_branches_str = input("Select the wanted branches \
(use space for seperation, nothing for all): ")
sel_branches: t.Optional[t.List[int]] = None
if sel_branches_str != "":
    sel_branches = [int(s) for s in sel_branches_str.split(" ")]

title = input("Write a nice title for the graph(leave empty if unwanted): ")

output = input(f"Where to save (leave empty for {output_default}): ")
if output == "":
    output = output_default

# Load each data thing and plot it
fname, name = data_files[choise]
print(f"Loading file {fname}")
with h5py.File(fname, "r") as f:
    snr = f["snrs"][:]
    prob = f["probs"][:]

branches = len(prob)
print(f"Found {branches} branches")

if sel_branches is None:
    sel_branches = list(range(branches))

legends = []

min_snr = np.inf
max_snr = -np.inf
# TODO hmm we are limited by the number of line styles, that is stupid
for i, b in enumerate(sel_branches):
    plt.plot(snr[b], prob[b])
    legends.append(f"N = {b+1}")

    min_snr = min(min(snr[b]), min_snr)
    max_snr = max(max(snr[b]), max_snr)

print(legends)

plt.legend(legends)
plt.yscale("log")
plt.ylabel("Symbol Error Rate")
plt.xlabel("SNR [dB]")
plt.grid(True)
plt.xticks(np.arange(min_snr, max_snr + 1, 5.0))
plt.yticks([1e0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5])
plt.ylim(1e-5, 1e0)
# format axis to bigger to bigger font
plt.rc('font', size=20)  # controls default text size
plt.rc('axes', titlesize=20)  # fontsize of the title
plt.rc('axes', labelsize=20)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)  # fontsize of the x tick labels
plt.rc('ytick', labelsize=20)  # fontsize of the y tick labels
plt.rc('legend', fontsize=20)  # fontsize of the legend
if title != "":
    print(f"Setting title '{title}'")
    plt.title(title)

print(f"Saving to {output}")
plt.savefig(output)
print("bye")
