import unittest
from antenna_diversity.protocols import dect
import struct
import os
from pathlib import Path
from antenna_diversity import common


class TestFull(unittest.TestCase):
    """
    Test full slot
    """
    def setUp(self):
        self.input = b'0123456789012345678901234567890123456789'
        self.dect_packet = b'\xaa\xaa\xff\xff\xff\xff\xff\xaa\xaa\xaa\xaa' + \
            b'\xaa_=0123456789012345678901234567890123456789\x11'

    def test_payload_presence(self):
        a = dect.Full(self.input)
        self.assertEqual(a.payload, a.b_field, self.input)

    def test_create_full(self):
        a = dect.Full(self.input)

        self.assertEqual(a.xz_field, 17)
        self.assertEqual(a.b_field, self.input)

        self.assertEqual(a.to_bytes(), self.dect_packet)

    def test_from_bytes(self):
        a = dect.Full.from_bytes(self.dect_packet)
        self.assertEqual(a.xz_field, 17)
        self.assertEqual(a.b_field, self.input)

    def test_check_xz_crc(self):
        self.assertFalse(dect.Full.from_bytes(self.dect_packet).xz_crc_error_detected())

        b = bytearray(self.dect_packet)
        b[-1] = 0
        self.assertTrue(dect.Full.from_bytes(bytes(b)).xz_crc_error_detected())

    def test_x_crc(self):
        self.assertFalse(dect.Full.from_bytes(self.dect_packet).x_crc_error_detected())

        b = bytearray(self.dect_packet)
        b[-1] = 0
        self.assertTrue(dect.Full.from_bytes(bytes(b)).x_crc_error_detected())

    def test_z_crc(self):
        self.assertFalse(dect.Full.from_bytes(self.dect_packet).z_crc_error_detected())

        b = bytearray(self.dect_packet)
        b[-1] = 0
        self.assertTrue(dect.Full.from_bytes(bytes(b)).z_crc_error_detected())

    def test_check_a_crc(self):
        self.assertFalse(dect.Full(self.input).a_crc_error_detected())

        b = bytearray(self.dect_packet)
        b[7] = 0
        self.assertTrue(dect.Full.from_bytes(bytes(b)).a_crc_error_detected())

    def test_check_payload_len(self):
        with self.assertRaisesRegex(Exception, "payload is not 40 long"):
            dect.Full(b'hej')

    def test_invalid_bytes(self):
        byts = bytearray(self.dect_packet)[:20]
        with self.assertRaisesRegex(Exception,
                                    "bytes are not 55 long"):
            dect.Full.from_bytes(byts)

    def test_4_bit_x_crc(self):
        # ensure it doesn't matter which dir this is run from
        p = os.path.join(Path(os.path.realpath(__file__)).parent,
                         'known_good_4_bit_x_crcs.txt')
        data = []
        expected = []
        with open(p) as lines:
            for line in lines:
                dat, val = line.split()
                data.append(bytes.fromhex(dat))
                expected.append(int(val))

        a = dect.Full(self.input)
        for i in range(common.shared_length(data, expected)):
            self.assertEqual(expected[i], a.x_crc_4_bit(data[i]))

    def test_get_random(self):
        dect.Full.with_random_payload()  # We have no known good so this is just run
