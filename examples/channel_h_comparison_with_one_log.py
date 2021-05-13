import ad_path
from antenna_diversity.channel import channel_models
from antenna_diversity import channel
import numpy as np
import matplotlib.pyplot as plt
import math


data_point_start = 200
data_point_between_start_and_end = 200
data_point_end = data_point_start+data_point_between_start_and_end

data_name = 'Library Novi'
file_name = 'Library_novi_zoomed.pdf'


def read_data():
    file = open('logs/Basestation_walk_niels_jernes_library.log', 'r')
    lines = file.read().splitlines()
    file.close()
    return lines


lines = read_data()

rssi_str = np.empty(shape=(len(lines) - 1))
time_from_zero = np.arange(0, len(lines) * 10 - 10, 10)
time_str = []
sync_str = []
a_crc_str = []
x_crc_str = []
z_crc_str = []
q1_str = []
q2_str = []
ant_str = []
pow_Str = []

for i, line in enumerate(lines):
    if(i == 0):
        print(line)
    else:
        line_splited = line.split()
        # print(line_splited)
        time_str.append(line_splited[0])
        rssi_str[i - 1] = float(line_splited[1])
        sync_str.append(line_splited[2])
        a_crc_str.append(line_splited[3])
        x_crc_str.append(line_splited[4])
        z_crc_str.append(line_splited[5])
        q1_str.append(line_splited[6])
        q2_str.append(line_splited[7])
        ant_str.append(line_splited[8])
        pow_Str.append(line_splited[9])

rssi_sixty_gns = np.empty_like(rssi_str)
diff_from_gns = np.empty_like(rssi_str)

counter = 0
sum_rssi = 0

for i, rssi in enumerate(rssi_str):
    diff_from_gns[i] = rssi_sixty_gns[i] - rssi

data_formodlling = rssi_str[data_point_start:data_point_end]
x_value_modeling = time_from_zero[data_point_start:data_point_end]
data_formodlling_gns = np.mean(data_formodlling)
data_formodling_mdian = np.median(data_formodlling)
data_formodlling_norm = data_formodlling - data_formodlling_gns
mean_line = np.ones(shape=len(data_formodlling)) * data_formodlling_gns
median_line = np.ones(shape=len(data_formodlling)) * data_formodling_mdian

print(data_formodlling_gns)


ch_1 = channel.channel_models.RayleighAWGNChannel(1, 0)
ch_2 = channel_models.RayleighAWGNChannel(
    1, 0, frame_per_block=3, intermediate_point=0)
ch_3 = channel_models.RayleighAWGNChannel(
    1, 0, frame_per_block=4)
ch_4 = channel_models.RayleighAWGNChannel(1,0, frame_per_block=4,intermediate_point=2)
ch_old = channel_models.RayleighAWGNChannelOld(1, 0)

h_1 = np.empty(shape=(len(data_formodlling)))
h_2 = np.empty(shape=(len(data_formodlling)))
h_3 = np.empty(shape=(len(data_formodlling)))
h_4 = np.empty(shape=(len(data_formodlling)))
h_old = np.empty(shape=(len(data_formodlling)))

signal = np.ones(1)
for i in range(len(data_formodlling)):
    _, h_from_ch1 = ch_1.run(signal)
    h_1[i] = 10 * math.log10(h_from_ch1)
    _, h_from_ch2 = ch_2.run(signal)
    h_2[i] = 10 * math.log10(h_from_ch2)
    _, h_from_h3 = ch_3.run(signal)
    h_3[i] = 10 * math.log10(h_from_h3)
    _, h_from_chold = ch_old.run(signal)
    h_old[i] = 10 * math.log10(h_from_chold)
    _, h_from_h4 = ch_4.run(signal)
    h_4[i] = 10 * math.log10(h_from_h4)
    ch_1.frame_sent()
    ch_2.frame_sent()
    ch_3.frame_sent()
    ch_4.frame_sent()
    ch_old.frame_sent()

#plt.plot(x_value_modeling[0:len(data_sigma_upsample)], data_sigma_upsample_db)
#plt.plot(x_value_modeling[0:len(data_sigma_upsample)], data_sqrt_db)


fig, axs = plt.subplots(5, sharex=True, sharey=True, figsize=(10,10), )

axs[0].plot(x_value_modeling, h_old,'.-', linewidth=1, color='#7E2F8E')

axs[0].plot(x_value_modeling, data_formodlling_norm, '.--', linewidth=1, color='#A2142F')

axs[1].plot(x_value_modeling, h_2,'.-', linewidth=1, color='#77AC30')

axs[1].plot(x_value_modeling, data_formodlling_norm,'.--', linewidth=1, color='#A2142F')

axs[2].plot(x_value_modeling, h_1,'.-', linewidth=1, color='#0072BD')

axs[2].plot(x_value_modeling, data_formodlling_norm,'.--', linewidth=1, color='#A2142F')

axs[3].plot(x_value_modeling, h_3,'.-', linewidth=1, color='#EDB120')

axs[3].plot(x_value_modeling, data_formodlling_norm,'.--', linewidth=1,
             color='#A2142F')


axs[4].plot(x_value_modeling, h_4, '.-' ,linewidth=1, color='#4DBEEE')

axs[4].plot(x_value_modeling, data_formodlling_norm,'.--' ,linewidth=1, color='#A2142F')
# print('sigma',sigam_square)

axs[0].legend(['Old channel h', data_name],fontsize='small', loc='lower right')

axs[2].legend(['Channel h with 1 intermediate and 3 frame Tc',
              data_name],fontsize='small', loc='lower right')

axs[1].legend(['Channel h with 0 intermediate and 3 frame Tc',
              data_name],fontsize='small', loc='lower right')

axs[3].legend(['Channel h with 1 intermediate and 4 frame Tc',
              data_name],fontsize='small', loc='lower right')

axs[4].legend(['channel h with 2 intermediate and 4 frame Tc', data_name],fontsize='small', loc='lower right')


for ax in axs:
    ax.set_ylabel('[dB]')

plt.tight_layout(pad = 0)
plt.xlabel('Time [ms]')
plt.savefig(file_name)
plt.show()
