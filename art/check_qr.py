"""Check that QR PNGs decode with three independent decoders, also when shrunk, tilted, blurred and noisy.

Needs `pip install opencv-python-headless zxing-cpp` (use a throwaway venv, not the project .venv).
python art/check_qr.py <expected text> <png> [<png> ...]
"""
import itertools
import sys

import cv2
import numpy as np
import zxingcpp

GREY = (190, 190, 190)
# angle, scale, blur kernel, noise seed
GRID = list(itertools.product([-20, -12, -6, 0, 6, 12, 20], [0.7, 0.85, 1.0], [3, 5], [1, 2]))


def photo_like(im, angle, scale, blur, seed):
    pad = max(im.shape[:2]) // 2
    big = cv2.copyMakeBorder(im, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=GREY)
    h, w = big.shape[:2]
    out = cv2.warpAffine(big, cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale), (w, h), borderValue=GREY)
    out = cv2.GaussianBlur(out, (blur, blur), 0)
    noise = np.random.default_rng(seed).normal(0, 6, out.shape)
    return np.clip(out.astype(float) + noise, 0, 255).astype(np.uint8)


def zxing_decode(im):
    found = zxingcpp.read_barcodes(im)
    return found[0].text if found else ""


DECODERS = {
    "OpenCV": lambda im: cv2.QRCodeDetector().detectAndDecode(im)[0],
    "OpenCV-Aruco": lambda im: cv2.QRCodeDetectorAruco().detectAndDecode(im)[0],
    "ZXing": zxing_decode,
}


def main():
    expected, paths = sys.argv[1], sys.argv[2:]
    failed = False
    for path in paths:
        full = cv2.imread(path)
        h, w = full.shape[:2]
        small = cv2.resize(full, (700, int(700 * h / w)), interpolation=cv2.INTER_AREA)
        print(path.split("\\")[-1])
        for name, decode in DECODERS.items():
            clean = decode(full) == expected and decode(small) == expected
            hits = sum(decode(photo_like(small, *g)) == expected for g in GRID)
            ok = clean and hits >= 0.9 * len(GRID)
            failed |= not ok
            print(f"  {'OK  ' if ok else 'FAIL'} {name:12} clean and small: {'yes' if clean else 'NO'}; tilted/blurred/noisy: {hits}/{len(GRID)}")
    print("FAILED" if failed else "ALL OK")


if __name__ == "__main__":
    main()
