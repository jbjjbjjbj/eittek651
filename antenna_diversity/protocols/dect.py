# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
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


class DECT():

    def __init__(self, M) -> None:
        self.M = M

    def create_full(self, payload: bytes):
        full = Full(self.M)
        full.create_packet(payload)
        return full

    def unpack_full(self, dect_packet: bytes):
        full = Full(self.M)
        full.from_bytes(dect_packet)
        return full

    def check_crc_full(self, dect_packet: bytes):
        return self.unpack_full(dect_packet).check_crc()


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

    def __init__(self, M=2) -> None:
        if M != 2:
            raise Exception("Only M=2 is supported")
        self.a_field_format = '=B5sH'
        self.packet_format = '=HL8s40sB'

    def create_packet(self, payload: bytes):
        self.a_header = int('1'*8, 2)
        self.a_tail = bytes.fromhex('AA' * int(40/8))
        crc_fields = struct.pack('B5s', self.a_header, self.a_tail)
        self.a_crc = crc.Crc16DectR().calc(crc_fields)

        self.preamble = int('10' * 8, 2)
        self.sync = int('1'*32, 2)
        if len(payload) != int(320/8):
            raise Exception(f"payload is not {int(320/8)} long")
        self.b_field = bytes(payload)

        self.xz_field = self.calculate_xz_field()

    def calculate_xz_field(self):
        test_bytes = prepare_test_bytes(self.b_field)

        x_field = dect_4bit_crc(test_bytes)
        if x_field.bit_length() > 4:
            raise Exception("x_field bit length is not 4")

        return x_field | (x_field << 4)

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

    def from_bytes(self, bytes):
        self.preamble, self.sync, a_field, self.b_field, self.xz_field = \
            struct.unpack(self.packet_format, bytes)

        self.a_header, self.a_tail, self.a_crc = \
            struct.unpack(self.a_field_format, a_field)

    def check_crc(self) -> bool:
        return self.calculate_xz_field() == self.xz_field


def dect_4bit_crc(data: bytes):
    a = bitarray()
    a.frombytes(data)
    a.extend([0, 0, 0, 0])
    poly = 1
    register = 0

    while len(a) > 0:
        desicion = register & 8
        register = (register << 1) & 0xF
        register |= a.pop(0)

        if(desicion > 0):
            register = register ^ poly

    return register


def prepare_test_bytes(b_field: bytes) -> bytes:
    """
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
