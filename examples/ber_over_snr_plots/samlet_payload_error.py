import matplotlib.pyplot as plt
import numpy as np
import h5py
from numpy.core.fromnumeric import shape

filename = 'diversity_mega.h5'

f = h5py.File(filename, 'r')

data = f['data']

print(data[0][0][0])

sh = shape(data)

# algo_names = ["Selection", "MRC", "CRC", "EGC", "rene", "power_and_crc"]
# data[snr][branch][algorithm] = [error, total, payload_error, slots, pbes]

one_branch_ber = []
one_branch_snr_stop = 0
one_branch_pbe = []
one_branch_payload_error = []

# selection
selection_ber_stop = 0
selection_ber = []
selection_pbe = []
selection_payload_error = []

for snr_i in range(25):
    err, total, payload_error, slots, pbes = data[snr_i][0][0]
    if (err / total) > (10**-4 * 1 / 2):
        one_branch_ber.append(err / total)
        one_branch_snr_stop = snr_i
        print(one_branch_snr_stop)
    one_branch_pbe.append(pbes / slots)
    one_branch_payload_error.append(payload_error / slots)

for snr_i in range(25):
    err, total, payload_error, slots, pbes = data[snr_i][1][0]
    if err / total > 10**-5:
        selection_ber.append(err / total)
        selection_ber_stop = snr_i
    selection_pbe.append(pbes / slots)
    selection_payload_error.append(payload_error / slots)

# MRC
mrc_ber_stop = 0
mrc_ber = []
mrc_pbe = []
mrc_payload_error = []

for snr_i in range(25):
    err, total, payload_error, slots, pbes = data[snr_i][1][1]
    if err / total > 10**-5:
        mrc_ber.append(err / total)
        mrc_ber_stop = snr_i
    mrc_pbe.append(pbes / slots)
    mrc_payload_error.append(payload_error / slots)

# crc
crc_ber_stop = 0
crc_ber = []
crc_pbe = []
crc_payload_error = []

for snr_i in range(25):
    err, total, payload_error, slots, pbes = data[snr_i][1][2]
    if err / total > 10**-4 * 1 / 2:
        crc_ber.append(err / total)
        crc_ber_stop = snr_i
    crc_pbe.append(pbes / slots)
    crc_payload_error.append(payload_error / slots)

# egc
egc_ber_stop = 0
egc_ber = []
egc_pbe = []
egc_payload_error = []

for snr_i in range(25):
    err, total, payload_error, slots, pbes = data[snr_i][1][3]
    if err / total > (10**-5):
        egc_ber.append(err / total)
        egc_ber_stop = snr_i
    egc_pbe.append(pbes / slots)
    egc_payload_error.append(payload_error / slots)


# Rene
rene_ber_stop = 0
rene_ber = []
rene_pbe = []
rene_payload_error = []

for snr_i in range(25):
    err, total, payload_error, slots, pbes = data[snr_i][1][4]
    if err / total > 10**-5:
        rene_ber.append(err / total)
        rene_ber_stop = snr_i
    rene_pbe.append(pbes / slots)
    rene_payload_error.append(payload_error / slots)


# power_and_crc
power_and_crc_ber_stop = 0
power_and_crc_ber = []
power_and_crc_pbe = []
power_and_crc_payload_error = []

for snr_i in range(25):
    err, total, payload_error, slots, pbes = data[snr_i][1][5]
    if err / total > 10**-5:
        power_and_crc_ber.append(err / total)
        power_and_crc_ber_stop = snr_i
    power_and_crc_pbe.append(pbes / slots)
    power_and_crc_payload_error.append(payload_error / slots)


x = np.arange(-10, 2.5 * 25 - 10, 2.5)
lw = 0.75

plt.figure(figsize=(7, 4))
plt.plot(x[2:len(one_branch_payload_error) - 8],
         one_branch_payload_error[2:len(one_branch_payload_error) - 8],
         '--',
         color='#A2142F',
         linewidth=lw)
plt.plot(x[2:len(selection_payload_error) - 8],
         selection_payload_error[2:len(selection_payload_error) - 8],
         color='#0072BD',
         linewidth=lw)
plt.plot(x[2:len(mrc_payload_error) - 8],
         mrc_payload_error[2:len(mrc_payload_error) - 8],
         color='#D95319',
         linewidth=lw)
plt.plot(x[2:len(crc_payload_error) - 8],
         crc_payload_error[2:len(crc_payload_error) - 8],
         color='#4DBEEE',
         linewidth=lw)
plt.plot(x[2:len(egc_payload_error) - 8],
         egc_payload_error[2:len(egc_payload_error) - 8],
         color='#EDB120',
         linewidth=lw)
plt.plot(x[2:len(rene_payload_error) - 8],
         rene_payload_error[2:len(rene_payload_error) - 8],
         color='#7E2F8E',
         linewidth=lw)
plt.plot(x[2:len(power_and_crc_payload_error) - 8],
         power_and_crc_payload_error[2:len(power_and_crc_payload_error) - 8],
         color='#77AC30',
         linewidth=lw)

plt.ylabel('Packet loss ratio [-]')
plt.xlabel('Signal noise ratio (SNR) [dB]')
plt.grid(True)
plt.legend(['1 branch', 'Selection', 'MRC', 'CRC',
            'EGC', 'Differential', 'Power and CRC'])

plt.savefig('Payload_error_over_snr.pdf')
plt.show()
