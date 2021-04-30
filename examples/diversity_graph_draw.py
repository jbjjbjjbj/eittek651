from pathlib import Path
import re
import h5py
import matplotlib.pyplot as plt

diversity_file_re = re.compile("diversity_(.*)\\.h5$")
output_default = "diversity_all.pdf"

# Find diversity files in current dir
data_files = []
for fname in Path.cwd().iterdir():
    match = diversity_file_re.search(str(fname))
    if match is not None:
        name = match.groups(0)[0]
        data_files.append((fname, name))

print("Found data files:")
for i, (_, name) in enumerate(data_files):
    print(f"  {i}: {name}")

choise_str = input("Select by numbers (use space for seperation): ")
choises = [int(s) for s in choise_str.split(" ")]

title = input("Write a nice title for the graph(leave empty if unwanted): ")

output = input(f"Where to save (leave empty for {output_default}): ")
if output == "":
    output = output_default

for choise in choises:
    fname, name = data_files[choise]
    print(f"Loading file {fname}")
    with h5py.File(fname, "r") as f:
        snr = f["snrs"][:]
        prob = f["probs"][:]

    branches = len(prob)
    print(f"Found {branches} branches")
    if branches == 1:
        label = [name]
    else:
        label = [f"Branch {i}({name})" for i in range(branches)]

    for i in range(branches):
        plt.plot(snr, prob[i], label=label[i])

plt.yscale("log")
plt.ylabel("Symbol Error Probability")
plt.xlabel("SNR [dB]")
plt.legend()
if title != "":
    print(f"Setting title '{title}'")
    plt.title(title)

print(f"Saving to {output}")
plt.savefig(output)
print("bye")
