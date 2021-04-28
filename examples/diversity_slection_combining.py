import numpy as np
import ad_path
from antenna_diversity.channel import channel_models
from antenna_diversity import modulation, channel
import matplotlib.pyplot as plt


# Generate frame parameters
slots_per_frame = 12
bits_per_full_frame = 11520
#bits_per_frame = int(slots_per_frame / 24 * bits_per_full_frame)
bits_per_frame = 10000
gfsk = modulation.GFSK()

frame = np.random.randint(0, 2, size=bits_per_frame)

snr = np.arange(-10, 20, 2.5)

# branches = np.arange(1, 5, 1)

x = gfsk.modulate(frame)

prob_res = np.empty(len(snr))


def fram_sender(chan):
    frame = np.random.randint(2, size=bits_per_frame)
    signal = gfsk.modulate(frame)
    hat_signal, h = ch.run(signal)
    hat_signal[0] = hat_signal[0] * 1 / h[0]
    hat_frame = gfsk.demodulate(hat_signal[0])
    # ch.frame_sent()
    wrong, n = modulation.runner.Runner.count_symbol_errors(
        frame, hat_frame)
    return wrong, n


for i, gamma in enumerate(snr):
    ch = channel_models.RayleighAWGNChannel(N=1, snr=gamma)
    ch.print_parameters()
    total_wrong = 0
    total = 0
    while (total_wrong < 1000 and total < bits_per_frame * 1000):
        error, n = fram_sender(ch)
        total_wrong += error
        total += n
    prob_res[i] = total_wrong / total
    print(gamma, ': ', prob_res[i])

# res = np.empty(shape=(len(branches), len(snr)))


""" for i, branch in enumerate(branches):
    for j, gamma in enumerate(snr):
        ch = channel_models.RayleighAWGNChannel(N=branch, snr=gamma)
        errors = 0
        totalSent = 0
        while errors < 100:
            frame = np.random.randint(0, 2, size=bits_per_frame)
            x = gfsk.modulate(frame)  # modulate signal
            r, h = ch.run(x)  # run signal trought channel
            print(r[0])
            print(np.shape(r))
            hat_x = gfsk.demodulate(r[0])  # demodulate received signal
            errors = errors + np.sum(frame != hat_x)
            totalSent = totalSent + bits_per_frame
        res[i][j] = errors / totalSent
        print('Branch: ', branch, ' gamma: ', gamma, res[i][j]) """

plt.yscale("log")
plt.plot(snr, prob_res)
plt.show()
