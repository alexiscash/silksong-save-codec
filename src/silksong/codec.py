from pathlib import Path
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import json

CSHARP_HEADER = bytes([0, 1, 0, 0, 0, 255, 255, 255,
                       255, 1, 0, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0, 0])
AES_KEY_STRING = "UKu52ePUBwetZ9wNX88o54dnfKRu0T1l"


def decrypt(payload: bytes) -> str:  # JSON

    without_header = payload[len(CSHARP_HEADER):-1]

    len_count = 0
    for i in range(5):
        len_count += 1
        if (without_header[i] & 0x80) == 0:
            break

    no_header = without_header[len_count:]

    b64_encrypted = base64.b64decode(no_header)
    cipher = AES.new(AES_KEY_STRING.encode(), AES.MODE_ECB)

    decoded = cipher.decrypt(b64_encrypted)
    unpadded = unpad(decoded, AES.block_size)

    return json.loads(unpadded)


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


def save_json(obj: str, path: Path | str = 'saves/user2.json') -> None:
    with open(path, 'w') as f:
        json.dump(obj, f, ensure_ascii=False)


def save_dat_file(final_bytes: bytes, path: Path | str) -> None:
    Path(path).write_bytes(final_bytes)


if __name__ == "__main__":
    raw = Path('saves/user2.dat').read_bytes()
    save_json(decrypt(raw))
