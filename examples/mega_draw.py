import numpy as np
import ad_path
import antenna_diversity as ad
import matplotlib.pyplot as plt
import h5py
import typing as t
import time
import os

ad_path.nop()


bits_per_slot = 440
slots_per_frame = 1
give_up_value = 1e-6
# How many bits to aim for at give_up_value
certainty = 20
# Stop early at x number of errors. Make sure to scale together with
# slots_per_frame, as this number number must include several different
# h values.
stop_at_errors = 100000
snr_stop = 50
snr_step = 2.5
branches = 5
crc_fail_penalty = 320  # Payload len
savefile = "diversity_mega.h5"

bit_goal = np.ceil(1/give_up_value) * certainty
max_tries = int(np.ceil(bit_goal / (bits_per_slot * slots_per_frame)))
print(bit_goal, max_tries)

snr_values = np.arange(-10, snr_stop+snr_step, snr_step)
snr_todo = list(range(len(snr_values)))
snr_channels = []
for snr in snr_values:
    snr_channels.append(ad.channel.RayleighAWGNChannel(branches, snr))

gfsk = ad.modulation.GFSK()
encoder = ad.encoding.SymbolEncoder(2)

# Keep track of class instances used at the innermost loop
selector_dictionary = {}


def rest(hat_recv: np.ndarray, symbols: np.ndarray, slot) -> t.Tuple[int, int, bool, int]:
    hat_symbols = gfsk.demodulate(hat_recv)

    hat_data = encoder.decode_msb(hat_symbols)
    unpacked = ad.protocols.dect.Full.from_bytes(hat_data)

    err, n = ad.common.count_symbol_errors(symbols, hat_symbols)

    crc_fail = unpacked.any_crc_error_detected()
    if crc_fail:
        pbes = crc_fail_penalty
    else:
        pbes, _ = ad.common.count_bit_errors(slot.b_field, unpacked.b_field)

    return err, n, crc_fail, pbes


# Must return (errors, total, crc, pbes)
def selection_recv_h(recv: np.ndarray, h: np.ndarray, symbols: np.ndarray, slot, _) \
        -> t.Tuple[int, int, bool, int]:
    hat_recv, _ = ad.diversity_technique.selection_from_h(recv, h)
    return rest(hat_recv, symbols, slot)


def mrc_recv_h(recv: np.ndarray, h: np.ndarray, symbols: np.ndarray, slot, _) \
        -> t.Tuple[int, int, bool, int]:
    hat_recv = ad.diversity_technique.combining.mrc(recv, h)
    return rest(hat_recv, symbols, slot)


def egc_recv_h(recv: np.ndarray, h: np.ndarray, symbols: np.ndarray, slot, _) \
        -> t.Tuple[int, int, bool, int]:
    hat_recv = ad.diversity_technique.combining.egc(recv)
    return rest(hat_recv, symbols, slot)


def crc_recv_h(recv: np.ndarray, h: np.ndarray, symbols: np.ndarray, slot, state_id)\
        -> t.Tuple[int, int, bool, int]:
    if state_id not in selector_dictionary:
        selector = ad.diversity_technique.CRCSelection(len(recv))
        selector_dictionary[state_id] = selector
    else:
        selector = selector_dictionary[state_id]

    hat_recv, _ = selector.select(recv)
    err, n, crc_fail, pbes = rest(hat_recv, symbols, slot)

    selector.report_crc_status(not crc_fail)

    return err, n, crc_fail, pbes


def renedif_recv_h(recv: np.ndarray, h: np.ndarray, symbols: np.ndarray, slot, state_id)\
        -> t.Tuple[int, int, bool, int]:
    if state_id not in selector_dictionary:
        selector = ad.diversity_technique.ReneDif()
        selector_dictionary[state_id] = selector
    else:
        selector = selector_dictionary[state_id]

    hat_recv, _ = selector.select(recv)
    return rest(hat_recv, symbols, slot)


# Her instilles listen af algorithmer der skal køres
algorithms = [selection_recv_h, mrc_recv_h, crc_recv_h, egc_recv_h, renedif_recv_h]
algo_names = ["Selection", "MRC", "CRC", "EGC", "rene"]
# algorithms = [renedif_recv_h, crc_recv_h]
# algo_names = ["rene", "crc"]

# Thing with structure [snr_index][branch][algorithm] = [errors, total, payload_errors, slots, pbes]
data = np.zeros((len(snr_values), branches, len(algorithms), 5))

if os.path.isfile(savefile):
    with h5py.File(savefile, "r") as f:
        data = f["data"][:]
        print("Loaded existing data from file")


def make_frame_array():
    frame_array = []
    for i in range(slots_per_frame):
        data = ad.protocols.dect.Full.with_random_payload()
        frame_array.append(data)
    return frame_array


run = 0

start = time.time()
while len(snr_todo) > 0:
    frame = make_frame_array()
    for slot in frame:
        symbols = encoder.encode_msb(slot.to_bytes())
        signal = gfsk.modulate(symbols)

        for i, snr_index in enumerate(snr_todo):
            ch = snr_channels[snr_index]
            recv, h = ch.run(signal)

            done = True

            for branch in range(branches):
                for ai, algorithm in enumerate(algorithms):
                    state_id = f"{snr_index}.{branch}.{ai}"
                    errors, total, _, _, _ = data[snr_index][branch][ai]
                    prob = errors / total
                    # print(f"snr_index: {snr_index}, branch: {branch}, snr: {snr_values[snr_index]}, total: {total}, prob: {prob}")
                    if total > bit_goal or errors > stop_at_errors:
                        break

                    done = False

                    err, n, crc_fault, pbes = algorithm(recv[:branch+1], h[:branch+1], symbols, slot, state_id)

                    data[snr_index][branch][ai][0] += err
                    data[snr_index][branch][ai][1] += n
                    data[snr_index][branch][ai][2] += int(crc_fault)
                    data[snr_index][branch][ai][3] += 1
                    data[snr_index][branch][ai][4] += pbes

            ch.frame_sent()

            if done:
                del snr_todo[i]

    run += 1
    if run % 10 == 0:
        end = time.time()
        duration = (end - start) / 10
        print(f"Run: {run}, time: {duration}s, snr_todo: ({len(snr_todo)}) {snr_values[snr_todo]}")
        start = end


print(data)

with h5py.File("diversity_mega.h5", "w") as f:
    f.create_dataset("data", data=data)

for i, algo_name in enumerate(algo_names):
    # Draw BER over SNR plots
    plt.figure()
    for branch in range(branches):
        probs = np.empty(len(snr_values))
        for snr_i, _ in enumerate(snr_values):
            errors, total, _, _, _ = data[snr_i][branch][i]
            probs[snr_i] = errors / total

        plt.title(algo_name)
        plt.plot(snr_values, probs, label=f"N = {branch+1}")

    plt.xlabel('SNR [dB]')
    plt.ylabel('Bit Error Rate')
    plt.yscale("log")
    plt.legend()
    plt.grid(True)

    # Draw payload_error graph
    plt.figure()
    for branch in range(branches):
        probs = np.empty(len(snr_values))
        for snr_i, _ in enumerate(snr_values):
            _, _, payload_fail, slots, _ = data[snr_i][branch][i]
            probs[snr_i] = payload_fail / slots

        plt.plot(snr_values, probs, label=f"N = {branch+1}")

    plt.title(algo_name + " payload_error")
    plt.xlabel("SNR [dB]")
    plt.ylabel("Ratio of packets CRC errors")
    plt.legend()
    plt.grid(True)

    # Draw pbes graph
    plt.figure()
    for branch in range(branches):
        probs = np.empty(len(snr_values))
        for snr_i, _ in enumerate(snr_values):
            _, _, _, slots, pbes = data[snr_i][branch][i]
            probs[snr_i] = pbes / slots

        plt.plot(snr_values, probs, label=f"N = {branch+1}")

    plt.title(algo_name + " payload_score")
    plt.xlabel("SNR [dB]")
    plt.ylabel("Payload Bit Error Score")
    plt.legend()
    plt.grid(True)


plt.show()

