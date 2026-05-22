#!/usr/bin/env python3
"""fastfilegen – ultra‑quick batch file creator.

Author: TopherBot <topherbot@proton.me>
License: MIT (see LICENSE file)
"""

import argparse
import os
import sys
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate N files instantly with auto‑renamed, collision‑free names."
    )
    parser.add_argument("-n", "--number", type=int, required=True,
                        help="Number of files to generate")
    parser.add_argument("-p", "--prefix", default="file",
                        help="Filename prefix (default: 'file')")
    parser.add_argument("-s", "--suffix", default="",
                        help="Filename suffix (default: empty)")
    parser.add_argument("-e", "--ext", default=".txt",
                        help="File extension including the dot (default: .txt)")
    parser.add_argument("-c", "--content", default="",
                        help="One‑line text to write inside each file (default: empty)")
    parser.add_argument("-d", "--dir", default=".",
                        help="Destination directory (default: current working directory)")
    return parser.parse_args()

def ensure_dir(path: Path):
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[ERROR] Cannot create directory {path}: {e}", file=sys.stderr)
        sys.exit(1)

def generate_filename(base_dir: Path, prefix: str, suffix: str, ext: str, index: int) -> Path:
    """Return a filename that does not yet exist.
    The function will increment `index` until a free name is found.
    """
    while True:
        name = f"{prefix}_{index:03d}{suffix}{ext}"
        candidate = base_dir / name
        if not candidate.exists():
            return candidate
        index += 1

def main():
    args = parse_args()
    target_dir = Path(args.dir).expanduser().resolve()
    ensure_dir(target_dir)

    created = 0
    idx = 1
    while created < args.number:
        file_path = generate_filename(target_dir, args.prefix, args.suffix, args.ext, idx)
        try:
            with file_path.open("w", encoding="utf-8") as f:
                if args.content:
                    f.write(args.content + "\n")
            print(f"[+] Created: {file_path}")
            created += 1
            idx = int(file_path.stem.split('_')[-1]) + 1  # continue after the last used number
        except Exception as e:
            print(f"[ERROR] Failed to write {file_path}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
