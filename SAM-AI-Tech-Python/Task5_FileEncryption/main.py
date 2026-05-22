import argparse
from pathlib import Path

import encryption


def encrypt_file(source: Path, password: str, output: Path):
    try:
        plaintext = source.read_text(encoding="utf-8")
        encrypted_data = encryption.encrypt_text(plaintext, password)
        encryption.save_encrypted_file(output, encrypted_data)
        print(f"Encrypted file saved to: {output}")
    except FileNotFoundError:
        print("Error: Source file not found.")
    except Exception as exc:
        print(f"Encryption failed: {exc}")


def decrypt_file(source: Path, password: str, output: Path):
    try:
        encrypted_data = encryption.load_encrypted_file(source)
        plaintext = encryption.decrypt_text(encrypted_data, password)
        output.write_text(plaintext, encoding="utf-8")
        print(f"Decrypted file saved to: {output}")
    except FileNotFoundError:
        print("Error: Encrypted file not found.")
    except ValueError as exc:
        print(f"Decryption failed: {exc}")
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="File encryption and decryption utility")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Operation mode")
    parser.add_argument("source", help="Source file path")
    parser.add_argument("password", help="Password for encryption or decryption")
    parser.add_argument("--output", help="Destination file path")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    source = Path(args.source)
    output = Path(args.output) if args.output else None

    if args.mode == "encrypt":
        output = output or source.with_suffix(source.suffix + ".enc")
        encrypt_file(source, args.password, output)
    else:
        output = output or source.with_suffix(".dec.txt")
        decrypt_file(source, args.password, output)


if __name__ == "__main__":
    main()
