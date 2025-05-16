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

def decode(bytes_seq):
    """
    Dekodiert eine Varint-kodierte Byte-Sequenz.
    
    Args:
        bytes_seq (bytes): Varint-kodierte Bytes
        
    Returns:
        int: Dekodierter Wert
    """
    result = 0
    shift = 0

    for byte in bytes_seq:
        #Extrahiere die 7 Datenbits
        result |= (byte & 0x7f) << shift

        #Prüfe Forsetzungsbit
        if not (byte & 0x80):
            break
        shift += 7
    return result

if __name__ == '__main__':
    cases = {
        ('1.uint64', b'\x01'),
        ('150.uint64', b'\x96\x01'),
        ('maxint.uint64', b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01'),
    }
    for fname, expectation in cases:
        with open(fname, 'rb') as file:
            #8 Bytes einlesen
            data = file.read(8)
            #als Big Endian interpretieren
            decimal = struct.unpack('>Q', data)[0]
            encoded = encode(decimal)
            print(encoded)
            assert encoded == expectation
            print(decode(encoded))
            #assert decode(b'\x96\x01') == 150
            assert decode(encoded) == decimal
    print('ok')


"""
Bitweise Operatoren
& 	AND	Sets each bit to 1 if both bits are 1	x & y	
|	OR	Sets each bit to 1 if one of two bits is 1	x | y	
^	XOR	Sets each bit to 1 if only one of two bits is 1	x ^ y	
~	NOT	Inverts all the bits	~x	
<<	Zero fill left shift	Shift left by pushing zeros in from the right and let the leftmost bits fall off	x << 2	
>>	Signed right shift	Shift right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off	x >> 2
"""