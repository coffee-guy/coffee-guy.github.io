"""Generate the website QR code as PNG and SVG files in ./qr."""

import argparse
from pathlib import Path
from urllib.parse import urlparse

import segno

OUT_DIR = Path(__file__).resolve().parent / "qr"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Final public https:// address of the website")
    parser.add_argument("--name", default="rio-cafe-qr", help="Output file name without extension")
    args = parser.parse_args()

    parsed = urlparse(args.url)
    if parsed.scheme != "https" or not parsed.netloc:
        parser.error("url must be a full https:// address")

    OUT_DIR.mkdir(exist_ok=True)
    qr = segno.make(args.url, error="q")
    for ext, scale in (("png", 20), ("svg", 10)):
        path = OUT_DIR / f"{args.name}.{ext}"
        qr.save(path, scale=scale, border=4)
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
