import ad_path
import antenna_diversity as ad
import numpy as np
import matplotlib.pyplot as plt

"""
This file will show the insights of a chosen selection algorithm.
Very nice for seing what is actually done.

It will output the following data:
- A plot showing CRC error and the selected branch
- A plot showing fading values for each plot
- A printout of all branches with usage statistics

To make the plot readable only 100 frames are sent through, but this can be
adjusted.

To make comparison between algorithms easy, the generator is seeded before.
Therefore each run will have CRC errors etc. in the same place each time.
"""

ad_path.nop()
np.random.seed(2)

encoder = ad.encoding.SymbolEncoder(2)
modulator = ad.modulation.GFSK()
branches = 2
channel = ad.channel.RayleighAWGNChannel(branches, 10)

selector = ad.diversity_technique.selection.ReneDif()

frames = 1000
slots_to_plot = 300
bits_per_slot = 440
slots_per_frame = 1


def make_frame_array():
    frame_array = []
    for i in range(slots_per_frame):
        data = ad.protocols.dect.Full.with_random_payload().to_bytes()
        frame_array.append(data)
    return frame_array


slots = frames
selected = np.empty(frames)
selected_old = np.empty(frames)
errors = np.empty(frames)
fading_t = np.empty((frames, branches))

fade_select_old = np.empty(slots_to_plot)
fade_select = np.empty(slots_to_plot)

for frame_number in range(frames):
    frame = make_frame_array()
    for slot in frame:
        symbols = encoder.encode_msb(slot)
        moded = modulator.modulate(symbols)

        recv, h = channel.run(moded)

        fading_t[frame_number] = (h)

        _, selected_old[frame_number] = ad.diversity_technique.selection_from_power(recv)
        selc, selected[frame_number] = selector.select(recv)
        demod = modulator.demodulate(selc)

        unpacked = ad.protocols.dect.Full.from_bytes(encoder.decode_msb(demod))
        error = unpacked.any_crc_error_detected()

        errors[frame_number] = (error)

        if frame_number < slots_to_plot:
            fade_select_old[frame_number] = h[int(selected_old[frame_number])]
            fade_select[frame_number] = h[int(selected[frame_number])]

        #selector.report_crc_status(not error)

    channel.frame_sent()

    print(f"frame_id: {frame_number}")

print(f"Sent {slots} slots")
total_errors = sum(errors)
print(f"Had {total_errors} errors ({100 * total_errors / slots} %)")
for branch in range(branches):
    selected_at = np.where(selected == branch)[0]

    had_slots = len(selected_at)
    had_errors = sum(errors[selected_at])
    if had_slots != 0:
        print(f"Branch {branch}:")
        print(f"  slots: {had_slots} ({100 * had_slots / slots} % of total)")
        print(f"  errors: {had_errors} ({100 * had_errors / had_slots} %)")
    else:
        print(f"Branch {branch} was not selected at all")

fading = np.transpose(fading_t)  # type: ignore

style = ".--"

slots = np.arange(slots_to_plot)
for i, fade in enumerate(fading):
    plt.plot(slots, fade[slots], style, label=f"N = {i}")

plt.plot(slots, fade_select, style, label="Diff select")
plt.plot(slots, fade_select_old, style, label="Normal select")

plt.legend()
plt.show()

"""
fig, ax = plt.subplots(2)
slots = np.arange(slots_to_plot)
ax[0].plot(slots, errors[slots])
ax[0].plot(slots, selected[slots])
for fade in fading:
    ax[1].plot(slots, fade[slots])

fig.savefig("out.png")
"""
