import unittest
from antenna_diversity.protocols import DECT
import struct
import os
from pathlib import Path
from antenna_diversity import common


class TestDECT(unittest.TestCase):
    def setUp(self):
        self.input = b'0123456789012345678901234567890123456789'
        self.dect_packet = b'\xaa\xaa\xff\xff\xff\xff\xff\xaa\xaa\xaa\xaa' + \
            b'\xaa_=0123456789012345678901234567890123456789\x11'

    def test_create_full(self):
        a = DECT(2).create_full(self.input)

        self.assertEqual(a.xz_field, 17)
        self.assertEqual(a.b_field, self.input)

        self.assertEqual(a.to_bytes(), self.dect_packet)

    def test_unpack_full(self):
        a = DECT(2).unpack_full(self.dect_packet)
        self.assertEqual(a.xz_field, 17)
        self.assertEqual(a.b_field, self.input)

    def test_check_crc_full(self):
        self.assertTrue(DECT(2).check_crc_full(self.dect_packet))

        b = bytearray(self.dect_packet)
        b[-1] = 0
        self.assertFalse(DECT(2).check_crc_full(bytes(b)))

    def test_check_payload_len(self):
        with self.assertRaisesRegex(Exception, "payload is not 40 long"):
            DECT(2).create_full(b'hej')

    def test_invalid_bytes(self):
        byts = bytearray(self.dect_packet)[:20]
        with self.assertRaisesRegex(struct.error,
                                    "unpack requires a buffer of 55 bytes"):
            DECT(2).unpack_full(byts)

    def test_400_cases(self):
        # ensure it doesn't matter which dir this is run from
        p = os.path.join(Path(os.path.realpath(__file__)).parent,
                         'known_good_four_bit_x_crcs.txt')
        data = []
        expected = []
        with open(p) as f:
            for line in f:
                dat, value = line.split()
                data.append(bytes.fromhex(dat))
                expected.append(int(value))

        a = DECT(2).create_full(self.input)
        for i in range(common.shared_length(data, expected)):
            self.assertEqual(expected[i], a.dect_4bit_crc(data[i]))


