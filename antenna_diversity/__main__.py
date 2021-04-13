import numpy as np
from . import modulation
from .rayleigh_fading import rayleigh

if __name__ == "__main__":
    my_pam = modulation.PSK(4)
    my_pam.save_constellation("constellation.png")

    my_symbols = np.random.randint(0, 4, size=100)
    print(my_symbols)

    my_modulated = my_pam.modulate(my_symbols)
    print("modulated", my_modulated)
    my_modulated = rayleigh(my_modulated,21)

    my_demodulated = my_pam.demodulate(my_modulated)
    print(my_demodulated)
    if not np.array_equal(my_symbols,my_demodulated):
        print("not same")