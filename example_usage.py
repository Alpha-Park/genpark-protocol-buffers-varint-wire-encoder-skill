from client import ProtobufWire

def main():
    print("=== Testing Protocol Buffers Wire Encoder ===")
    pb = ProtobufWire()
    enc = pb.encode_field(field_number=1, wire_type=0, payload=300)
    print("Encoded bytes:", list(enc))

    tag, off = pb.decode_varint(enc, 0)
    assert tag == (1 << 3) | 0
    val, _ = pb.decode_varint(enc, off)
    print(f"Decoded tag: {tag >> 3}, value: {val}")
    assert val == 300
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
