from . import common


from . import common
from . import modulation
import numpy as np

if __name__ == "__main__":

    my_pam = modulation.PAM(4)

    my_symbols = np.random.randint(0, 4, size=100)
    print(my_symbols)

    my_modulated = np.empty(len(my_symbols))
    for i, my_symbol in enumerate(my_symbols):
        my_modulated[i] = my_pam.modulate(my_symbol)

    print("modulated", my_modulated)


    my_demodulated = np.empty(len(my_symbols))
    for i, my_modulat in enumerate(my_modulated):
        my_demodulated[i] = my_pam.demodulate(my_modulat)

    print(my_demodulated)
