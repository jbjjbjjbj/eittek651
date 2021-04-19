import unittest
from antenna_diversity.protocols import DECT

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