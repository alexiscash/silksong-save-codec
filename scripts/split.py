from pathlib import Path

raw = Path("saves/user2.dat").read_bytes()

newline_index = raw.find(b"\n")

print("newline at byte:", newline_index)
print("header bytes:", newline_index)
print("payload starts with:", raw[newline_index+1:newline_index+9])

header = raw[:newline_index+1]
payload = raw[newline_index+1:]

Path("saves/header.bin").write_bytes(header)
Path("saves/payload.b64").write_bytes(payload)

print("header size:", len(header))
print("payload size:", len(payload))
