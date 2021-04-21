import numpy as np
from . import modulation
from . import channel
from . import diversity_schemes
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

    nodiversity = channel.rayleigh_awgn(my_modulated, 22)
    mrcdiversity = diversity_schemes.MRC(my_modulated,-10,2)

    nodiv_demodulated = my_pam.demodulate(nodiversity)
    print(nodiv_demodulated)
    mrcdiv_demodulated = my_pam.demodulate(mrcdiversity) 
    print(mrcdiv_demodulated) #The MRC diversity schemes seems to be semi-stable with two antennas with a -5 dB SNR and -8 with three

    if not np.array_equal(my_symbols, nodiv_demodulated):
        print("No diversity: not same")
    if not np.array_equal(my_symbols, mrcdiv_demodulated):
        print("MRC diversity: not same")
