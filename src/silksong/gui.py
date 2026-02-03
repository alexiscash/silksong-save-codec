from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from src.silksong.codec import decrypt, encrypt, save_dat_file, save_json


def decode_file():
    path = filedialog.askopenfilename(
        title="Select Silksong .dat save",
        filetypes=[("Silksong save", "*.dat")]
    )
    if not path:
        return

    try:
        raw = Path(path).read_bytes()
        data = decrypt(raw)

        out = Path(path).with_suffix(".json")
        save_json(data, out)

        status.set(f"Decoded -> {out.name}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def encode_file():
    path = filedialog.askopenfilename(
        title="Select JSON save",
        filetypes=[("JSON", "*.json")]
    )
    if not path:
        return

    try:
        import json
        data = json.loads(Path(path).read_text())

        out = Path(path).with_suffix(".dat")
        save_dat_file(encrypt(data), out)

        status.set(f"Encoded -> {out.name}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Silksong Save Editor")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Button(frame, text="Decode .dat -> JSON",
          width=30, command=decode_file).pack(pady=5)
tk.Button(frame, text="Encode JSON -> .dat",
          width=30, command=encode_file).pack(pady=5)

status = tk.StringVar(value="Ready")
tk.Label(frame, textvariable=status).pack(pady=(10, 0))

root.mainloop()
