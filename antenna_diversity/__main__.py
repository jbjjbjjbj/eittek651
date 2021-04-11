import numpy as np
from . import modulation

from .encoding import GrayEncoder

if __name__ == "__main__":
    my_pam = modulation.MSK()
    M = my_pam.M

    my_symbols = np.random.randint(0, M, size=1000)
    # my_symbols = np.array([1, 1, 0, 0, 1])
    print(my_symbols)

    my_gray = GrayEncoder(M)

    my_gray_symbols = my_gray.encode(my_symbols)

    my_modulated = my_pam.modulate(my_gray_symbols)
    # print("modulated", my_modulated)

    my_demodulated = my_pam.demodulate(my_modulated)
    my_demodulated = my_gray.decode(my_demodulated)

    # print(my_demodulated)

    if not np.array_equal(my_demodulated, my_symbols):
        print("THE ARRAYS DIFFER")

