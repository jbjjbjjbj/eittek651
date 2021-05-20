import unittest
from antenna_diversity.protocols import dect
import copy
import os
from pathlib import Path
from antenna_diversity import common


class TestFull(unittest.TestCase):
    """
    Test full slot
    """
    def setUp(self):
        self.payload = b'0123456789012345678901234567890123456789'
        self.packet_bytes = b'\xaa\xaa\xff\xff\xff\xff\xff\xaa\xaa\xaa\xaa' + \
            b'\xaa_=0123456789012345678901234567890123456789\x11'
        self.packet = dect.Full(self.payload)

        self.mutable_bytes = bytearray(self.packet_bytes)
        self.mutated_bytes = copy.copy(self.mutable_bytes)
        self.mutated_bytes[-1] = 0
        self.mutated_bytes[7] = 0
        self.mutated_packet = dect.Full.from_bytes(self.mutated_bytes)

    def test_from_payload(self):
        self.assertEqual(self.packet.xz_field, 17)
        self.assertEqual(self.packet.b_field, self.payload)
        self.assertEqual(self.packet.to_bytes(), self.packet_bytes)

    def test_from_bytes(self):
        packet_from_bytes = dect.Full.from_bytes(self.packet_bytes)
        self.assertEqual(self.packet.to_bytes(), packet_from_bytes.to_bytes())

    def test_check_xz_crc(self):
        self.assertFalse(self.packet.xz_crc_error_detected())
        self.assertTrue(self.mutated_packet.xz_crc_error_detected())

    def test_x_and_z_crc_mutated_z(self):
        mutated_xz = self.packet.xz_field ^ 0x05  # 0000 0101
        self.packet.xz_field = mutated_xz
        self.assertTrue(self.packet.z_crc_error_detected())
        self.assertFalse(self.packet.x_crc_error_detected())

    def test_x_and_z_crc_mutated_x(self):
        mutated_xz = self.packet.xz_field ^ 0x50  # 0101 0000
        self.packet.xz_field = mutated_xz
        self.assertTrue(self.packet.z_crc_error_detected())
        self.assertTrue(self.packet.x_crc_error_detected())

    def test_x_and_z_crc_mutated_payload(self):
        mutated_payload = [0x00] * 40
        self.packet.b_field = bytes(mutated_payload)
        self.assertTrue(self.packet.x_crc_error_detected())
        self.assertFalse(self.packet.z_crc_error_detected())

    def test_check_a_crc(self):
        self.assertFalse(self.packet.a_field_crc_error_detected())
        self.assertTrue(self.mutated_packet.a_field_crc_error_detected())

    def test_crc_drops_packet(self):
        self.assertFalse(self.packet.crc_drops_packet())
        self.assertTrue(self.mutated_packet.crc_drops_packet())

    def test_any_crc(self):
        self.assertFalse(self.packet.any_crc_error_detected())
        self.assertTrue(self.mutated_packet.any_crc_error_detected())

    def test_check_payload_len(self):
        with self.assertRaisesRegex(Exception, "payload is not 40 long"):
            dect.Full(b'hej')

    def test_invalid_bytes(self):
        byts = self.mutable_bytes[:20]
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

        for i in range(common.shared_length(data, expected)):
            self.assertEqual(expected[i], self.packet.x_crc_4_bit(data[i]))

    def test_get_random(self):
        dect.Full.with_random_payload()  # We have no known good so this is just run
