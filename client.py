class ProtobufWire:
    """
    Protocol Buffers Wire Format Encoder and Decoder.
    Encodes field tags, wire types, and varint payloads.
    """
    def encode_varint(self, value):
        out = bytearray()
        while value > 0x7F:
            out.append((value & 0x7F) | 0x80)
            value >>= 7
        out.append(value & 0x7F)
        return bytes(out)

    def decode_varint(self, data, offset=0):
        res = 0
        shift = 0
        while offset < len(data):
            b = data[offset]
            offset += 1
            res |= (b & 0x7F) << shift
            if (b & 0x80) == 0:
                break
            shift += 7
        return res, offset

    def encode_field(self, field_number, wire_type, payload):
        tag = (field_number << 3) | wire_type
        header = self.encode_varint(tag)
        if wire_type == 0:
            return header + self.encode_varint(payload)
        elif wire_type == 2:
            return header + self.encode_varint(len(payload)) + payload
        return header + payload
