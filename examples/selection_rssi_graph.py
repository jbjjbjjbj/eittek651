import ad_path
import antenna_diversity as ad
import numpy as np
import matplotlib.pyplot as plt
import math
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

encoder = ad.encoding.SymbolEncoder(2)
modulator = ad.modulation.GFSK()
branches = 3
channel = ad.channel.RayleighAWGNChannel(branches, 10)

# selector = ad.diversity_technique.selection.ReneDif()
selector = ad.diversity_technique.selection.CRCSelection(branches)

frames = 1000
slots_to_plot = 150
bits_per_slot = 440
slots_per_frame = 1


def make_frame_array():
    frame_array = []
    for i in range(slots_per_frame):
        data = ad.protocols.dect.Full.with_random_payload().to_bytes()
        frame_array.append(data)
    return frame_array


def calculate_db(input):
    return 10 * math.log10(input)


slots = 0
selected = []
errors = []
fading_t = []
rssi_branch1 = []
rssi_branch2 = []
rssi_branch3 = []
rssi_selected = []

for frame_number in range(frames):
    frame = make_frame_array()
    for slot in frame:
        symbols = encoder.encode_msb(slot)
        moded = modulator.modulate(symbols)
        recv, h = channel.run(moded)
        fading_t.append(h)
        selc, index = ad.diversity_technique.selection.selection_from_power(
            recv)
        rssi_branch1.append(calculate_db(
            ad.diversity_technique.selection.calculate_power(recv[0][0:32 * 4])))
        rssi_branch2.append(calculate_db(
            ad.diversity_technique.selection.calculate_power(recv[1][0:32 * 4])))
        rssi_branch3.append(calculate_db(
            ad.diversity_technique.selection.calculate_power(recv[2][0:32 * 4])))
        slots += 1
        selected.append(index)
        if(index == 0):
            rssi_selected.append(calculate_db(
                ad.diversity_technique.selection.calculate_power(recv[0][0:32 * 4])))
        elif(index == 1):
            rssi_selected.append(calculate_db(
                ad.diversity_technique.selection.calculate_power(recv[1][0:32 * 4])))
        else:
            rssi_selected.append(calculate_db(
                ad.diversity_technique.selection.calculate_power(recv[2][0:32 * 4])))

        # selector.report_crc_status(not error)

    channel.frame_sent()

    # print(f"frame_id: {frame_number}")

plt.figure(figsize=(8, 5))
plt.plot(rssi_branch1[50:150], '.--')
plt.plot(rssi_branch2[50:150], '.--')
plt.plot(rssi_branch3[50:150], '.--')
plt.plot(rssi_selected[50:150], '-')
plt.legend(['Branch 1', 'Branch 2', 'Branch 3', 'Selected branch'])
plt.xlabel('Packet number [-]')
plt.ylabel('Power [dB]')
plt.savefig("selection_rssi_plot.pdf")
plt.show()
