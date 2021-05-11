import numpy as np
import ad_path
from antenna_diversity import modulation, channel, diversity_technique, common
import matplotlib.pyplot as plt
import h5py
from config import ber_over_snr as cfg

ad_path.nop()

gfsk = modulation.GFSK()

# Make a frame constructed of how many bits there is per slot, and how
# many slots there is per frame


def make_frame_array():
    frameArray = np.empty(shape=(cfg.slot_per_frame, cfg.bits_per_slot))
    for i in range(cfg.slot_per_frame):
        frameArray[i] = np.random.randint(2, size=cfg.bits_per_slot)
    return frameArray


snr_todo = np.arange(-10, cfg.snr_stop+cfg.snr_step, cfg.snr_step)

bit_goal = np.ceil(1/cfg.give_up_value) * cfg.certainty
max_tries = int(np.ceil(bit_goal / (cfg.bits_per_slot * cfg.slot_per_frame)))

branches = np.arange(1, cfg.branches+1, 1)

shape = (len(branches), len(snr_todo))
# nan or "not a number" values are ignored when plotting
probs = np.full(shape, np.nan)
snrs = np.full(shape, np.nan)

for j, branch in enumerate(branches):
    branch_probs = []
    branch_snrs = []
    for i, gamma in enumerate(snr_todo):
        # create channel with the curretn branch and snr
        ch = channel.RayleighAWGNChannel(N=branch, snr=gamma)
        errors = 0
        numberOfBits = 0

        for k in range(max_tries):
            fram = make_frame_array()
            for slot in fram:
                signal = gfsk.modulate(slot)
                recieved, h = ch.run(signal)
                hat_recieved, _ = diversity_technique.selection_from_power(
                    recieved)
                hat_slot = gfsk.demodulate(hat_recieved)
                err, n = common.count_symbol_errors(slot, hat_slot)
                errors += err
                numberOfBits += n
            ch.frame_sent()

            if errors >= cfg.stop_at_errors:
                print(f"Stopping early at {k} runs")
                break

        ber = errors / numberOfBits
        print('snr', gamma, 'branch', branch, 'Prob:', ber)

        snrs[j][i] = gamma
        probs[j][i] = ber

        # Stop when below give_up_value
        if ber < cfg.give_up_value:
            print(f"Under {cfg.give_up_value}, stopping here")
            break

legends = []

for i, branch in enumerate(branches):
    plt.plot(snrs[i], probs[i])
    s = 'N = '
    s += str(branch)
    legends.append(s)

with h5py.File("diversity_selection.h5", "w") as f:
    f.create_dataset("probs", data=probs)
    f.create_dataset("snrs", data=snrs)

plt.legend(legends)
plt.yscale('log')
plt.xlabel('SNR [dB]')
plt.ylabel('Bit Error Rate')
plt.grid(True)
# format axis to bigger to bigger font
plt.rc('font', size=20)  # controls default text size
plt.rc('axes', titlesize=20)  # fontsize of the title
plt.rc('axes', labelsize=20)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)  # fontsize of the x tick labels
plt.rc('ytick', labelsize=20)  # fontsize of the y tick labels
plt.rc('legend', fontsize=20)  # fontsize of the legend

plt.savefig('diversity_selection.pdf')
