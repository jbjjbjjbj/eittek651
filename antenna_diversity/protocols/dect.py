import struct
# R-CRC
# Used for:
#   - All A-fields
#   - All B-subfields in multisubfield protected format (every 64-bits)



# X-CRC is used for:
#   - X-field (and is a of the B-field)


# B-CRC
# Used for:
#  - The whole B-field in singlesubfield proteced format (in the end of the B-field, before X-field)



# struct {
# unsigned char header
# char[] tail
# unsigned short CRC
# };

a_field_format = 'BsH'

class DECT:

    def __init__(self) -> None:
        pass

    def full(payload):
        """
        16 bit preamble
        32 bit sync field
        64 bit A-field
        320 bit B-field
        4 bit X-field
        4 bit Z-field (copy of X)
        """
        # struct {
        # unsigned short preamble
        # unsigned long long sync
        # char[] A-field
        # char[] B-field
        # unsigned char XandZ
        # };
        struct_format = 'HQssB'

        


    def long(payload):
        raise "long is not implemented yet"

    def double(payload):
        raise "double is not implemented yet"




