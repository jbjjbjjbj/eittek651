# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import numpy as np
import pandas as pd

import ad_path
ad_path.nop()
import antenna_diversity as ad


class NoDiversity():
   def  __init__():
        pass

crc_fail_penalty = 320  # Payload len
nr_packets = 1000
snrs_db = np.arange(-2, 18, 1)
dates = {}
for dt in [NoDiversity, ad.diversity_technique.mrc, ad.diversity_technique.egc, ad.diversity_technique.selection]:
    all_payload_bit_errors = []
    for snr in snrs_db:
        print(f"Starting run for SNR {snr}")
        packets = [ad.protocols.dect.Full.with_random_payload() for _ in range(nr_packets)]
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

        demodulated = None
        if dt == ad.diversity_technique.selection:
                                                              # god forsaken return tuples
            demodulated = [modulator.demodulate(dt(r, hs)[0]) \
                           for r, hs in rs_and_hss]
        elif dt == ad.diversity_technique.mrc:
            demodulated = [modulator.demodulate(dt(r, hs)) \
                           for r, hs in rs_and_hss]
        elif dt == ad.diversity_technique.egc:
            demodulated = [modulator.demodulate(dt(r)) \
                           for r, _ in rs_and_hss]
        elif dt == NoDiversity:
            demodulated = [modulator.demodulate(r[0]) for r, _ in rs_and_hss]
        else:
            raise Exception(f"Unknown diversity technique, {dt}, can't used")


        received_packets = [ad.protocols.dect.Full.from_bytes(modem.decode_msb(d)) for d in demodulated]


        received_packets_bytes = [rp.to_bytes() for rp in received_packets]


        payload_bit_errors = 0
        for i in range(ad.common.shared_length(received_packets, packets)):
            if received_packets[i].any_crc_error_detected():
                payload_bit_errors += crc_fail_penalty
            else:
                # b_field is payload for now, but see
                # https://github.com/jbjjbjjbj/eittek651/issues/39
                payload_bit_errors += ad.common.count_bit_errors(received_packets[i].b_field,
                                                                 packets[i].b_field)[0]
        # TODO: rename stuff to mean or avg, since it is divided by nr_packets
        all_payload_bit_errors.append(payload_bit_errors / nr_packets)
    dates[f'{dt.__name__} (2 branches)'] = all_payload_bit_errors


df = pd.DataFrame(
        index=snrs_db,
        data=dates,
        )


df.plot(ylabel=f"Payload Bit Error Score ({nr_packets} packets, lower is better)",
        xlabel="SNR [dB]",
        title="DECT Full, GFSK, RayleighAWGNChannel").get_figure().savefig("lol2.png")

