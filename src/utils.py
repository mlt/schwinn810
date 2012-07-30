import struct

def unpack_bcd(x0):
    x00 = x0
    x = 0
    m = 0
    while x0:
        digit = x0 & 0x000f
        if digit>9:
            raise Exception("Non-BCD argument {:X} in {:X}".format(digit, x00))
        x = x + digit * 10**m
        m = m + 1
        x0 = x0 >> 4
    return x

def pack_coord(c0, hemi):
    c1 = struct.unpack(">HBHs", c0)
    c2=[unpack_bcd(x) for x in c1[0:3]]
    c = c2[0] + (c2[1]+c2[2]/10000.)/60.
    if (c1[3] == hemi) : c = -c
    return c
