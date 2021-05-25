import matplotlib.pyplot as plt
import numpy as np
import h5py
from numpy.core.fromnumeric import shape

filename = 'diversity_mega.h5'

f = h5py.File(filename, 'r')

data = f['data']

sh = shape(data)
print(sh)
# algo_names = ["Selection", "MRC", "CRC", "EGC", "rene", "power_and_crc"]
# data[snr][branch][algorithm] = [error, total, payload_error, slots, pbes]

ber = np.empty((sh[1], sh[0]))
stops = np.array([25, 25, 25, 25, 25])
print(shape(ber))

for br in range(sh[1]):
    for snr in range(sh[0]):
        error, total, _, _, _ = data[snr][br][3]
        biterr = error / total
        ber[br][snr] = biterr
        if(biterr < (10**-5)):
            stops[br] = snr
            break

x = np.arange(-10, 2.5 * 25 - 10, 2.5)
plt.figure(figsize=(7, 4))
for i in range(5):
    plt.plot(x[0: stops[i]], ber[i][0: stops[i]])


plt.yscale('log')
plt.ylabel('Bit error rate (BER) [-]')
plt.xlabel('Signal noise ratio (SNR) [dB]')
plt.grid(True)
plt.legend(['1 branch', '2 branch', '3 branch', '4 branch',
            '5 branch'])

plt.savefig('egc_BER_over_SNR.pdf')
plt.show()
