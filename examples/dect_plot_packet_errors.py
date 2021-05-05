# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import antenna_diversity as ad
import numpy as np
import pandas as pd

import ad_path
ad_path.nop()


nr_packets = 75
snrs_db = np.arange(-5, 25, 1)
x_crc_error_ratios = []
z_crc_error_ratios = []
a_crc_error_ratios = []
bers = []
nr_undetected_errors = []
for snr in snrs_db:
    print(f"Starting run for SNR {snr}")
    packets = [ad.protocols.dect.Full.with_random_payload()
               for _ in range(nr_packets)]
    packets_bytes = [p.to_bytes() for p in packets]

    modulator = ad.modulation.GFSK()

    modem = ad.encoding.SymbolEncoder(2)

    symbols = [modem.encode_msb(pb) for pb in packets_bytes]

    modulated = [modulator.modulate(s) for s in symbols]

    some_channel = ad.channel.channel_models.RayleighAWGNChannel(2, snr)
    rs_and_hss = []
    for i, m in enumerate(modulated):
        rs_and_hss.append(some_channel.run(m))
        some_channel.frame_sent()

        # god forsaken return tuples
    demodulated = [
        modulator.demodulate(
            ad.diversity_technique.selection_from_h(
                r,
                hs)[0]) for r,
        hs in rs_and_hss]

    received_packets = [
        ad.protocols.dect.Full.from_bytes(
            modem.decode_msb(d)) for d in demodulated]
    received_packets_bytes = [rp.to_bytes() for rp in received_packets]

    a_crc_detecteds = [rp.a_field_crc_error_detected()
                       for rp in received_packets]
    a_crc_error_ratios.append(sum(a_crc_detecteds) / len(a_crc_detecteds))

    x_crc_detecteds = [rp.x_crc_error_detected() for rp in received_packets]
    x_crc_error_ratios.append(sum(x_crc_detecteds) / len(x_crc_detecteds))

    z_crc_error_detecteds = [rp.z_crc_error_detected()
                             for rp in received_packets]
    z_crc_error_ratios.append(
        sum(z_crc_error_detecteds) /
        len(z_crc_error_detecteds))

    nr_undetected_error = 0
    packet_bers = []
    for i in range(
        ad.common.shared_length(
            packets_bytes,
            received_packets_bytes)):

        faults, total = ad.common.count_bit_errors(packets_bytes[i],
                                                   received_packets_bytes[i])
        packet_bers.append(faults / total)

        if ((not received_packets[i].any_crc_error_detected()) and
                packets_bytes[i] != received_packets_bytes[i]):
            nr_undetected_error += 1

    nr_undetected_errors.append(nr_undetected_error / nr_packets)
    mean_ber = sum(packet_bers) / len(packet_bers)
    bers.append(mean_ber)


df = pd.DataFrame(
    index=snrs_db,
    data={"Ratio of Packets with X-CRC Error Detected": x_crc_error_ratios,
          "Ratio of Packets with R-CRC Error Detected": a_crc_error_ratios,
          f"Mean Bit Error Rate ({nr_packets} packets)": bers,
          "Ratio of Undetected Packet Errors": nr_undetected_errors,
          "Ratio of Packets with Z-CRC Error Detected": z_crc_error_ratios,
          }
)


df.plot(xlabel="SNR [dB]").get_figure().savefig("lol2.png")
