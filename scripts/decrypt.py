from pathlib import Path
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json

CSHARP_HEADER = [0, 1, 0, 0, 0, 255, 255, 255,
                 255, 1, 0, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0, 0]
AES_KEY_STRING = "UKu52ePUBwetZ9wNX88o54dnfKRu0T1l"

raw = Path('saves/user2.dat').read_bytes()

without_header = raw[len(CSHARP_HEADER):len(raw)-1]

len_count = 0
for i in range(5):
    len_count += 1
    if (without_header[i] & 0x80) == 0:
        break

payload = without_header[len_count:]

b64_encrypted = base64.b64decode(payload)
mode = AES.MODE_ECB
cipher = AES.new(AES_KEY_STRING.encode(), mode)

decoded = cipher.decrypt(b64_encrypted)
unpadded = unpad(decoded, AES.block_size)

pretty = json.loads(unpadded)

with open('saves/user2.json', 'w') as f:
    json.dump(pretty, f, ensure_ascii=False)
