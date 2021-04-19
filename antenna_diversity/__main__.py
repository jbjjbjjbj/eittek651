import numpy as np
from . import common
from . import modulation

if __name__ == "__main__":
    
    pass


"""
    my_pam = modulation.PAM(4)

    #          | pS | S | A |    B | X| Z|
    # np.array([1, 0, 0, 1, 1, 1, 1, 1, 1])

    dect_packet = protocols.DECT().full(payload)

    my_symbols = encode(dect_packet)

    print(my_symbols)

    my_modulated = my_pam.modulate(my_symbols)
    print("modulated", my_modulated)

    my_demodulated = my_pam.demodulate(my_modulated)
    print(my_demodulated)
"""