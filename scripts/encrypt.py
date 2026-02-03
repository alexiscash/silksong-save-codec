from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import json

CSHARP_HEADER = bytes([0, 1, 0, 0, 0, 255, 255, 255,
                       255, 1, 0, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0, 0])
AES_KEY_STRING = "UKu52ePUBwetZ9wNX88o54dnfKRu0T1l"


def encrypt(json_str: dict) -> bytes:
    json_bytes = json.dumps(json_str, ensure_ascii=False).encode()

    cipher = AES.new(AES_KEY_STRING.encode(), AES.MODE_ECB)

    encrypted = cipher.encrypt(pad(json_bytes, AES.block_size))

    b64_bytes = base64.b64encode(encrypted)

    out = bytearray()

    n = len(b64_bytes)
    while True:
        byte = n & 0x7f
        n >>= 7
        if n:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            break

    len_bytes = bytes(out)

    return (
        CSHARP_HEADER +
        len_bytes +
        b64_bytes +
        b"\x0B"
    )


def save_to_dat_file(final_bytes: bytes) -> None:
    Path("saves/user3.dat").write_bytes(final_bytes)
