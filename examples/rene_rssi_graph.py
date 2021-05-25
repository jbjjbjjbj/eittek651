from crccheck import crc
import ad_path
import antenna_diversity
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

encoder = antenna_diversity.encoding.SymbolEncoder(2)
modulator = antenna_diversity.modulation.GFSK()
branches = 2
channel = antenna_diversity.channel.RayleighAWGNChannel(branches, 8)

#selector = ad.diversity_technique.selection.ReneDif()
selector = antenna_diversity.diversity_technique.selection.CRCSelection(
    branches)

frames = 1000
slots_to_plot = 150
bits_per_slot = 440
slots_per_frame = 1

diff_div = antenna_diversity.diversity_technique.ReneDif()


def make_frame_array():
    frame_array = []
    for i in range(slots_per_frame):
        data = antenna_diversity.protocols.dect.Full.with_random_payload().to_bytes()
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
rssi_sel_selected = []
rssi_diff_power_selected = []
CRC_sel = antenna_diversity.diversity_technique.selection.CRCSelection(2)

for frame_number in range(frames):
    # make dect packet
    packet = antenna_diversity.protocols.dect.Full.with_random_payload()
    # make packet to data bytes
    data = packet.to_bytes()
    # encode symbols
    symbols = encoder.encode_msb(data)
    # modulate symbols
    moded = modulator.modulate(symbols)
    # run channel
    recv, h = channel.run(moded)
    # save channel h
    fading_t.append(h)
    # run selection diversity
    selc, index = antenna_diversity.diversity_technique.selection.selection_from_power(
        recv)
    # save the rssi of each branch
    rssi_branch1.append(calculate_db(
        antenna_diversity.diversity_technique.selection.calculate_power(recv[0][0:32 * 4])))
    rssi_branch2.append(calculate_db(
        antenna_diversity.diversity_technique.selection.calculate_power(recv[1][0:32 * 4])))

    # run CRC_sel diversity
    selc, index2 = diff_div.select(recv)

    slots += 1
    selected.append(index)
    # save the selected branch for selected diversity
    if(index == 0):
        rssi_sel_selected.append(calculate_db(
            antenna_diversity.diversity_technique.selection.calculate_power(recv[0][0:32 * 4])))
    else:
        rssi_sel_selected.append(calculate_db(
            antenna_diversity.diversity_technique.selection.calculate_power(recv[1][0:32 * 4])))
    # save the selected branch for crc_sel diversity
    if(index2 == 0):
        rssi_diff_power_selected.append(calculate_db(
            antenna_diversity.diversity_technique.selection.calculate_power(recv[0][0:32 * 4])))
    else:
        rssi_diff_power_selected.append(calculate_db(
            antenna_diversity.diversity_technique.selection.calculate_power(recv[1][0:32 * 4])))

    #selector.report_crc_status(not error)

    channel.frame_sent()

    #print(f"frame_id: {frame_number}")

plt.figure(figsize=(8, 4))
plt.plot(rssi_branch1[50:150], '.--', color='#0072BD')
plt.plot(rssi_branch2[50:150], '.--', color='#D95319')
plt.plot(rssi_sel_selected[50:150], '-', color='#7E2F8E')
plt.plot(rssi_diff_power_selected[50:150], '-', color='#77AC30')
plt.ylabel('Power [dB]')
plt.xlabel('Packet number [-]')
plt.legend(['Power of branch 1', 'Power of branch 2',
           'Selection technique', 'Differential technique'], loc='lower left')
plt.savefig("rene_rssi_graph.pdf")
plt.show()
