import struct
import math
import crccheck.crc as crc
import typing as t


# R-CRC
# Used for:
#   - All A-fields
#   - All B-subfields in multisubfield protected format (every 64-bits)



# X-CRC is used for:
#   - X-field (and is of the a selected number of scrambled B-field bits)



# B-CRC
# Used for:
#  - The whole B-field in singlesubfield proteced format (in the end of the B-field, before X-field)



class DECT():

    def __init__(self, M) -> None:
        self.M = M

    def full(self, payload):
        return Full(payload, self.M)


class Full():
    """
    16 bit preamble
    32 bit sync field
    64 bit A-field
        8 bit header
        40 bit tail
        16 bit crc
    320 bit B-field (payload)
    4 bit X-field
    4 bit Z-field (copy of X)
    """

    def __init__(self, payload: bytes, M=2) -> None:
        if M != 2:
            raise Exception("Only M=2 is supported")
        self.a_field_format = '=B5sH'
        self.a_header = int('1'*8, 2)
        self.a_tail = bytes.fromhex('AA' * int(40/8))
        self.crc_fields = struct.pack('B5s', self.a_header, self.a_tail)
        self.a_crc = crc.Crc16DectR().calc(self.crc_fields)

        self.packet_format = '=HL8s40sB'
        self.preamble = int('10' * 8, 2)
        self.sync = int('1'*32, 2)
        if len(payload) != int(320/8):
            raise Exception(f"payload is not {int(320/8)} long")
        self.b_field = bytes(payload)

        # bytes be CRCed
        self.test_bytes = bytearray()
        for e in test_byte_indices(M):
            self.test_bytes.append(self.b_field[e])

        x_field = (crc.Crc16DectX.calc(self.test_bytes) >> 12) | 0x000f  # Not sure if correct
        if x_field.bit_length() != 4:
            raise Exception("x_field bit length is not 4")

        self.xz_field = x_field | (x_field << 4)

    def to_bytes(self) -> bytes:
        a_field = struct.pack(self.a_field_format,
                              self.a_header,
                              self.a_tail,
                              self.a_crc,
                              )
        return struct.pack(self.packet_format,
                           self.preamble,
                           self.sync,
                           a_field,
                           self.b_field,
                           self.xz_field,
                           )



def test_byte_indices(M: int) -> t.List:
    # etsi dect standard p. 87
    o = int(math.log2(M)) - 1

    nr_test_bit_table = [84, 168, 252, 336, 496]
    m = nr_test_bit_table[o]

    x_crc_size_table = [4, 8, 12, 16, 16]
    x = x_crc_size_table[o]

    delta_i_table = [240, 480, 720, 960, 1440]
    delta_i = delta_i_table[o]

    bit_indices = [i + 48 * (1 + math.floor(i/16)) for i in range(0, m-x)]
    bit_indices += [i + delta_i for i in range(m-x, m-4)]  # VI VED IKKE OM VI MÅ MINUS HER
    # Assumes there is always 8 bits in a row
    byte_indices = [int(bit_indices[i]/8) for i in range(0, len(bit_indices), 8)]
    return byte_indices
