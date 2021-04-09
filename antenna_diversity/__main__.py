import numpy as np
from . import common
from . import modulation

if __name__ == "__main__":
    my_pam = modulation.PAM(4)

    my_symbols = np.random.randint(0, 4, size=100)
    print(my_symbols)

    my_modulated = my_pam.modulate(my_symbols)
    print("modulated", my_modulated)

    my_demodulated = my_pam.demodulate(my_modulated)
    print(my_demodulated)
