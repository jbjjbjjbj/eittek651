import struct
from crccheck import crc
from bitarray import bitarray


# R-CRC
# Used for:
#   - All A-fields
#   - All B-subfields in multisubfield protected format (every 64-bits)


# X-CRC is used for:
#   - X-field (and is of the a selected number of scrambled B-field bits)


# B-CRC
# Used for:
#  - The whole B-field in singlesubfield proteced format (in the end of the
# B-field, before X-field)


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

    def __init__(self,
                 payload_or_bytes: bytes,
                 m: int = 2,
                 from_payload: bool = True) -> None:
        """
        Contructs a packet from 40 bytes / 320 bits payload.
        Various headers and the tail in the A-field are filled with garbage
        and CRCs are calculated by default.
        If you want to set from_payload=True, preferably use the from_bytes class method instead.
        """
        if m != 2:
            raise Exception("Only m=2 is supported")
        self.a_field_format = '=B5sH'
        self.packet_format = '=HL8s40sB'

        if from_payload:
            self.a_header = int('1'*8, 2)
            self.a_tail = bytes([0xAA] * int(40 / 8))
            self.a_crc = self.calculate_a_crc_field()

            self.preamble = int('10' * 8, 2)
            self.sync = int('1'*32, 2)
            if len(payload_or_bytes) != int(320/8):
                raise Exception(f"payload is not {int(320/8)} long")
            self.b_field = bytes(payload_or_bytes)

            self.xz_field = self.calculate_xz_crc_field()
        else:
            if len(payload_or_bytes) != int(440/8):
                raise Exception(f"bytes are not {int(440/8)} long")

            self.preamble, self.sync, a_field, self.b_field, self.xz_field = \
                struct.unpack(self.packet_format, payload_or_bytes)

            self.a_header, self.a_tail, self.a_crc = \
                struct.unpack(self.a_field_format, a_field)

    @classmethod
    def from_bytes(cls, raw_packet: bytes):  # Not sure about return type
        """
        Constructs a packet from 55 bytes / 440 bits which consists exclusively of those bytes.
        No sanity check is made, anything goes, and chances are if you check CRCs afterwards
        that they will detect an error.
        """
        return cls(raw_packet, from_payload=False)

    def calculate_a_crc_field(self) -> int:
        """
        Calculates the 2 byte CRC for the A-header
        """

        fields_to_crc = struct.pack('B5s', self.a_header, self.a_tail)
        return crc.Crc16DectR().calc(fields_to_crc)

    def calculate_xz_crc_field(self) -> int:
        """
        Calculates the X and Z field which in total is 8 bits where each nibble
        are identical 4 bit CRCs.
        """
        test_bytes = prepare_test_bytes(self.b_field)

        x_field = self.x_crc_4_bit(test_bytes)
        if x_field.bit_length() > 4:
            raise Exception("x_field bit length is not 4")

        return x_field | (x_field << 4)

    def to_bytes(self) -> bytes:
        """
        Returns the packet as 55 bytes.
        """
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

    def check_a_crc_field(self) -> bool:
        """
        Checks if the CRC in the A-field in the packet is equivalent to a new CRC calculation.
        """
        return self.calculate_a_crc_field() == self.a_crc

    def check_xz_crc_field(self) -> bool:
        """
        Checks if the X-CRC and Z-CRC (copies) in the packet is equivalent to a new CRC calculation.
        """
        return self.calculate_xz_crc_field() == self.xz_field

    @staticmethod
    def x_crc_4_bit(data: bytes) -> int:
        """
        Returns the result of the 4-bit X-CRC as described in DECT.
        It CRCs everything it gets as input and does NOT pick out m number of test bits.
        The N in N-bit X-CRC should depend on the modulation level.
        See https://www.zlib.net/crc_v3.txt for implementation details.
        """
        a = bitarray()
        a.frombytes(data)
        a.extend([0, 0, 0, 0])
        poly = 1
        register = 0

        while len(a) > 0:
            desicion = register & 8
            register = (register << 1) & 0xF
            register |= a.pop(0)

            if desicion > 0:
                register = register ^ poly

        return register


def prepare_test_bytes(b_field: bytes) -> bytes:
    """
    Returns the bytes of the B-field which are to be CRCed.
    It can be thought of as "2 on 6 off cont.".

    >>> prepare_test_bytes(bytes.fromhex('0b 0b 0c 0d 0e 0f aa bb cc'))
    b'\\x0b\\x0b\\xcc'
    """
    # bytes be CRCed
    test_bytes = bytearray()
    i = 1
    for e in b_field:
        i = i % 8

        if i == 1 or i == 2:
            test_bytes.append(e)
        i += 1
    return bytes(test_bytes)
