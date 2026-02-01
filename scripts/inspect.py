import base64
from pathlib import Path

save_path = Path("saves/user2.dat")

raw = save_path.read_bytes()

print("file size:", len(raw))
print("first 64 bytes:")
print(raw[:64])
print("\nprintable preview:")
print(raw[:200].decode(errors="replace"))


try:
    decoded = base64.b64decode(raw, validate=True)
    print("\nbase64 decode: SUCCESS")
    print("Decoded length:", len(decoded))
    print("Decoded first 16 bytes:", decoded[:16])
except Exception as e:
    print("\nbase64 decode: FAIL")
    print(e)
