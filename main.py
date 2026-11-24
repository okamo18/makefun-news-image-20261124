#!/usr/bin/env python3
"""Entrypoint for the 24 November 2026 world-news image.

Copies the front page drawn by draw_news.py to the output directory
as entry.png, byte for byte.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    # Verify the source is a real PNG of the expected size before copying.
    with open(SRC, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG file", file=sys.stderr)
        sys.exit(1)
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    if (width, height) != (1024, 1024):
        print(f"error: entry.png is {width}x{height}, expected 1024x1024",
              file=sys.stderr)
        sys.exit(1)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
