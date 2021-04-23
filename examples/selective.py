import os
import time
import numpy as np
from numpy.core.fromnumeric import size
import alation, encoding, channel, protocols, diversity_schemes
import matplotlib.pyplot as pltd_path
from antenna_diversity import modu

gfsk = modulation.GFSK()
gfsk.print_parameters()

chunkSize = 600

u = np.random.randint(2, size=chunkSize)
s = gfsk.modulate(u)


ch1 = []
ch2 = []
ch_choice = []
bedst_ch = []
for i in range(100):
    y, h, bedst_h = diversity_schemes.SEL.selective(s, 0, 2)
    ch1.append(h[0])
    ch2.append(h[1])
    ch_choice.append(bedst_h)
    if bedst_h == 0:
        bedst_ch.append(h[0])
    else:
        bedst_ch.append(h[1])
    hat_u = gfsk.demodulate(y)










plt.plot(ch1)
plt.plot(ch2)
plt.plot(bedst_ch)
plt.show()
