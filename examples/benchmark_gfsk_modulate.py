import numpy as np

import ad_path
ad_path.nop()
import antenna_diversity as ad

import timeit

modem = ad.modulation.GFSK()

def run_the_thing():
    modem.modulate(np.random.randint(2, size=10000))

time = timeit.timeit(run_the_thing, number=100)
print(time)
