import struct

def encode(value) -> bytes:
    """
    - https://protobuf.dev/programming-guides/encoding/#varints
    """
    if value == 0:
        return bytes([0])
    
    result = bytearray()
    while value > 0:
        #print("Value: " + bin(value))
        byte = value & 0x7F # Nimmt die 7 niedrigwertigsten Bits
        #print("Byte: " + bin(byte))
        value >>= 7         # Schiebe 7 Bits nach rechts.
        #print(value)
        if value > 0:       # Wenn noch Bits übrig sind
            byte |= 0x80    # Setze das MSB(Forsetzungsbit)
        #    print(byte)
        result.append(byte)
    return bytes(result)


with open('150.uint64', 'rb') as file:
    #8 Bytes einlesen
    data = file.read(8)
    #als Big Endian interpretieren
    decimal = struct.unpack('>Q', data)[0]
    print(encode(decimal))
    assert encode(150) == b'\x96\x01'


"""
Bitweise Operatoren
& 	AND	Sets each bit to 1 if both bits are 1	x & y	
|	OR	Sets each bit to 1 if one of two bits is 1	x | y	
^	XOR	Sets each bit to 1 if only one of two bits is 1	x ^ y	
~	NOT	Inverts all the bits	~x	
<<	Zero fill left shift	Shift left by pushing zeros in from the right and let the leftmost bits fall off	x << 2	
>>	Signed right shift	Shift right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off	x >> 2
"""