from pathlib import Path
import argparse
from src.silksong.codec import decrypt, encrypt, save_dat_file, save_json


def main():
    parser = argparse.ArgumentParser(
        prog="silksong",
        description="Silksong save file encoder/decoder"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    decode = sub.add_parser("decode", help="Decode .dat to JSON")
    decode.add_argument("input", help="Input .dat file")
    decode.add_argument("-o", "--output", help="Output JSON file")

    encode = sub.add_parser("encode", help="Encode JSON to .dat")
    encode.add_argument("input", help="Input JSON file")
    encode.add_argument("-o", "--output", help="Output .dat file")

    args = parser.parse_args()

    if args.command == "decode":
        raw = Path(args.input).read_bytes()
        data = decrypt(raw)
        out = args.output or Path(args.input).with_suffix('.json')
        save_json(data, out)

    elif args.command == "encode":
        import json
        data = json.loads(Path(args.input).read_text())
        out = args.output or Path(args.input).with_suffix(".dat")
        save_dat_file(encrypt(data), out)


if __name__ == "__main__":
    main()
