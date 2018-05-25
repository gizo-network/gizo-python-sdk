import binascii

def to_hex(bytes):
    return binascii.hexlify(bytearray(bytes)).decode("utf-8")

def to_bytes(hex):
    return list(binascii.unhexlify(hex))