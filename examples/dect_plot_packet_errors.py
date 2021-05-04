# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import numpy as np
import pandas as pd

import ad_path
ad_path.nop()
import antenna_diversity as ad

nr_packets = 1000
snrs_db = np.arange(-5, 11, 1)
xz_crc_error_ratios = []
a_crc_error_ratios = []
bers = []
nr_overlooked_errors = []
for snr in snrs_db:
    print(f"Starting run for SNR {snr}")
    packets = [ad.protocols.dect.Full.get_random() for _ in range(nr_packets)]
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
    demodulated = [modulator.demodulate(ad.diversity_technique.selection(r, hs)[0]) \
                   for r, hs in rs_and_hss]

    received_packets = [ad.protocols.dect.Full.from_bytes(modem.decode_msb(d)) for d in demodulated]
    received_packets_bytes = [rp.to_bytes() for rp in received_packets]

    a_crc_checks = [rp.a_crc_no_error_detected() for rp in received_packets]
    a_crc_error_ratios.append(1-sum(a_crc_checks)/len(a_crc_checks))


    xz_crc_checks = [rp.xz_crc_no_error_detected() for rp in received_packets]
    xz_crc_error_ratios.append(1-sum(xz_crc_checks)/len(xz_crc_checks))

    nr_overlooked_error = 0
    packet_bers = []
    for i in range(ad.common.shared_length(packets_bytes, received_packets_bytes)):

        faults, total = ad.modulation.Runner.count_bit_errors(packets_bytes[i],
                                                              received_packets_bytes[i])
        packet_bers.append(faults/total)

        if (xz_crc_checks[i] is True and a_crc_checks[i] is True and
                                         packets_bytes[i] != received_packets_bytes[i]):
            nr_overlooked_error += 1

    nr_overlooked_errors.append(nr_overlooked_error/nr_packets)
    mean_ber = sum(packet_bers)/len(packet_bers)
    bers.append(mean_ber)


df = pd.DataFrame(
        index=snrs_db,
        data={"XZ-CRC Packet Error Detection Ratio": xz_crc_error_ratios,
              "R-CRC Packet Error Detection Ratio": a_crc_error_ratios,
              f"Mean Bit Error Rate ({nr_packets} packets)": bers,
              "Ratio of Overlooked Packet Errors by CRCs": nr_overlooked_errors,
              }
        )


df.plot(xlabel="SNR [dB]").get_figure().savefig("lol2.png")

