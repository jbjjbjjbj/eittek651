from crccheck import crc
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

encoder = ad.encoding.SymbolEncoder(2)
modulator = ad.modulation.GFSK()
branches = 3
channel = ad.channel.RayleighAWGNChannel(branches, 10)

#selector = ad.diversity_technique.selection.ReneDif()
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


slots = 0
selected = []
errors = []
fading_t = []
rssi_branch1 = []
rssi_branch2 = []
rssi_sel_selected = []
rssi_crc_power_selected = []
crc_error_1 = []
crc_error_2 = []
selected_crc = []
CRC_sel = ad.diversity_technique.selection.CRCSelection(2)

for frame_number in range(frames):
    # make dect packet
    packet = ad.protocols.dect.Full.with_random_payload()
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
    selc, index = ad.diversity_technique.selection.selection_from_power(recv)
    # save the rssi of each branch
    rssi_branch1.append(
        ad.diversity_technique.selection.calculate_power(recv[0][0:32 * 4]))
    rssi_branch2.append(
        ad.diversity_technique.selection.calculate_power(recv[1][0:32 * 4]))

    # run CRC_sel diversity
    selc, index2 = CRC_sel.select(recv)

    # demodulate signals
    rc_demodulated = modulator.demodulate(selc)

    # decoded signals
    rc_decoded = encoder.decode_msb(rc_demodulated)

    # DECT packet
    rc_packet = ad.protocols.dect.Full.from_bytes(rc_decoded)

    if (rc_packet.a_field_crc_error_detected(
    ) or rc_packet.x_crc_error_detected() or rc_packet.z_crc_error_detected()):
        CRC_sel.report_crc_status(good=False)
        selected_crc.append(1)
    else:
        CRC_sel.report_crc_status(good=True)
        selected_crc.append(0)

    recieved = []
    recieved.append(modulator.demodulate(recv[0]))
    recieved.append(modulator.demodulate(recv[1]))

    # decode signal i.e. make it to bytes
    decoded = []
    decoded.append(encoder.decode_msb(recieved[0]))
    decoded.append(encoder.decode_msb(recieved[1]))

    # make dect packet from decoded signal
    received_packet = []
    received_packet.append(ad.protocols.dect.Full.from_bytes(decoded[0]))
    received_packet.append(ad.protocols.dect.Full.from_bytes(decoded[1]))

    for i, packet in enumerate(received_packet):
        if (packet.a_field_crc_error_detected(
        ) or packet.x_crc_error_detected() or packet.z_crc_error_detected()):
            if(i == 0):
                crc_error_1.append(1)
            else:
                crc_error_2.append(1)
        else:
            if(i == 0):
                crc_error_1.append(0)
            else:
                crc_error_2.append(0)

    slots += 1
    selected.append(index)
    # save the selected branch for selected diversity
    if(index == 0):
        rssi_sel_selected.append(
            ad.diversity_technique.selection.calculate_power(recv[0][0:32 * 4]))
    else:
        rssi_sel_selected.append(
            ad.diversity_technique.selection.calculate_power(recv[1][0:32 * 4]))
    # save the selected branch for crc_sel diversity
    if(index2 == 0):
        rssi_crc_power_selected.append(
            ad.diversity_technique.selection.calculate_power(recv[0][0:32 * 4]))
    else:
        rssi_crc_power_selected.append(
            ad.diversity_technique.selection.calculate_power(recv[1][0:32 * 4]))

    #selector.report_crc_status(not error)

    channel.frame_sent()

    #print(f"frame_id: {frame_number}")

fig, (ax1, ax2) = plt.subplots(2)

#fig, ax1 = plt.subplots()

ax1.plot(rssi_branch1[50:150], '.--', color='#0072BD')
ax1.plot(rssi_branch2[50:150], '.--', color='#D95319')
ax1.plot(rssi_sel_selected[50:150], '-', color='#7E2F8E')
ax1.plot(rssi_crc_power_selected[50:150], '-', color='#77AC30')
ax1.set_xlabel('# sample')
ax1.set_ylabel('Power')
ax1.legend(['Power branch 1', 'Power branch 2',
           'Normal selection', 'Power and CRC'], loc='lower left')


#ax2 = plt.twinx(ax1)

x = np.arange(0, 150 - 50)

ax2.scatter(x, crc_error_1[50:150], color='#0072BD', alpha=0.3)
ax2.scatter(x, crc_error_2[50:150], color='#D95319', alpha=0.3)
# markerline1, stemlines1, baseline1 = ax2.stem(crc_error_1[50:150])
# stemlines1.set_color('#0072BD')
# markerline1.set_color('#0072BD')

# markerline2, stemlines2, baseline2 = ax2.stem(crc_error_2[50:150])
# stemlines1.set_color('#D95319')
# markerline2.set_color('#D95319')

ax2.plot(selected_crc[50:150], color='#77AC30', alpha=0.3)

ax2.set_ylabel('CRC error')
ax2.set_alpha(0.5)
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['No', 'Yes'])

ax2.legend(['Power and CRC selected ', 'CRC error branch 1',
            'CRC error branch 2',
            ], loc='lower right')

plt.show()
plt.savefig("selection_rssi_plot.pdf")
