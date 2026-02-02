from pathlib import Path
import base64
import zlib

payload = Path("saves/payload.b64").read_bytes()
decoded = base64.b64decode(payload)

try:
    decompressed = zlib.decompress(decoded, wbits=-15)
    print("Raw DEFLATE decompression succeeded!")
    print("Decompressed size:", len(decompressed))
    print("Preview:")
    print(decompressed[:300].decode(errors="replace"))

    Path("saves/decompressed.bin").write_bytes(decompressed)
except Exception as e:
    print("Raw DEFLATE decompression failed:")
    print(e)
