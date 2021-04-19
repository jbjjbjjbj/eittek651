import numpy as np
from . import modulation
from . import channel
from . import encoding, protocols

if __name__ == "__main__":
    my_pam = modulation.PSK(2)
    my_pam.save_constellation("constellation.png")

    #          | pS | S | A |    B | X| Z|
    # np.array([1, 0, 0, 1, 1, 1, 1, 1, 1])
    
    payload = b'0123456789012345678901234567890123456789'

    dect_packet = protocols.DECT(2).create_full(payload)

    my_symbols = encoding.SymbolEncoder(2).encode_msb(dect_packet.to_bytes())

    print(my_symbols)

    my_modulated = my_pam.modulate(my_symbols)
    print("modulated", my_modulated)
    my_modulated = channel.rayleigh_awgn(my_modulated,22) #med rayleigh er det mindste vi kan komme ned på 22 snr

    my_demodulated = my_pam.demodulate(my_modulated)
    print(my_demodulated)

    if not np.array_equal(my_symbols,my_demodulated):
        print("not same")

