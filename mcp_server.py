import sys
import json
import base64
from client import ProtobufWire

def main():
    pb = ProtobufWire()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "encode":
            b = pb.encode_field(params.get("field_number", 1), params.get("wire_type", 0), params.get("payload"))
            res = {"bytes_b64": base64.b64encode(b).decode()}
        elif method == "decode_varint":
            raw = base64.b64decode(params.get("bytes_b64", "").encode())
            val, _ = pb.decode_varint(raw, params.get("offset", 0))
            res = {"value": val}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
