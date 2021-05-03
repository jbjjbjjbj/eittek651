from pathlib import Path
import re
import h5py
import matplotlib.pyplot as plt
import matplotlib

diversity_file_re = re.compile("diversity_(.*)\\.h5$")
output_default = "diversity_all.pdf"

styles = [":", "-.", "--", "-"]
# https://matplotlib.org/stable/gallery/color/named_colors.html
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple",
          "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]

# Find diversity files in current dir
data_files = []
for fname in Path.cwd().iterdir():
    match = diversity_file_re.search(str(fname))
    if match is not None:
        name = match.groups(0)[0]
        data_files.append((fname, name))

# Get user settings
print("Found data files:")
for i, (_, name) in enumerate(data_files):
    print(f"  {i}: {name}")

choise_str = input("Select by numbers (use space for seperation): ")
choises = [int(s) for s in choise_str.split(" ")]

sel_branches_str = input("Select the wanted branches \
(use space for seperation): ")
sel_branches = [int(s) for s in sel_branches_str.split(" ")]

title = input("Write a nice title for the graph(leave empty if unwanted): ")

output = input(f"Where to save (leave empty for {output_default}): ")
if output == "":
    output = output_default


# Load each data thing and plot it
for color_i, choise in enumerate(choises):
    fname, name = data_files[choise]
    print(f"Loading file {fname}")
    with h5py.File(fname, "r") as f:
        snr = f["snrs"][:]
        prob = f["probs"][:]

    branches = len(prob)
    print(f"Found {branches} branches")

    # If there are no branches we should only include the name in the legend
    if len(sel_branches) == 1:
        label = [name]
    else:
        label = [f"Branch {i+1}({name})" for i in sel_branches]

    # TODO hmm we are limited by the number of line styles, that is stupid
    for i, b in enumerate(sel_branches):
        plt.plot(snr, prob[b], label=label[i], linestyle=styles[i],
                 color=colors[color_i], lw=1)

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
