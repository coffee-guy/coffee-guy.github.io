"""Generate the website QR code in ./qr: a plain code and a "SCAN ME" poster, each as PNG and SVG."""

import argparse
import os
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import segno

OUT_DIR = Path(__file__).resolve().parent / "qr"

ESPRESSO, ROAST, SAFFRON, MILK = "#2b1810", "#5b3420", "#f3b23c", "#fffaf1"

# "SCAN ME" outlined from Lilita One (SIL OFL); 100 units tall.
TEXT_WIDTH = 602.4
TEXT_PATH = (
    "M10.8 65.2Q13.6 67.3 20.2 71Q26.8 74.8 32.9 74.8Q38.9 74.8 38.9 70Q38.9 67.9 37.2 66.3Q35.5 64.6 31 62.5Q26.4 60.3 24.1 59.1Q21.8 57.9 18 55.1Q14.3 52.4 12.3 49.4Q6.6 41.2 6.6 28.7Q6.6 16.1 15.9 7.5Q25.2 -1.1 40.4 -1.1Q50.6 -1.1 59.3 1.1Q68 3.3 68.3 6.8Q68.3 7.3 68.3 7.7Q68.3 12.7 65.2 20.3Q62.1 28 60.8 28.8Q51.6 24.1 44.4 24.1Q37.2 24.1 37.2 29.2Q37.2 32.4 42.5 34.8Q43.7 35.4 45.8 36.4Q47.9 37.4 50.7 38.7Q53.5 40.1 56.7 42.2Q59.9 44.2 63.6 47.6Q71.2 54.8 71.2 66.5Q71.2 81.7 62.8 91.4Q54.4 101.1 36.8 101.4Q28.2 101.4 21.3 100Q14.4 98.6 9.3 94.4Q4.1 90.3 4.1 84.5Q4.1 78.6 6.3 72.8Q8.4 67 10.8 65.2Z"
    "M145.5 29.4Q144.8 29.4 143.9 28.6Q142.9 27.8 139.6 26.9Q136.2 26 133.8 26Q125.5 26 120.5 31.8Q115.4 37.7 115.4 49.7Q115.4 61.8 120.6 67.6Q125.8 73.5 133.8 73.5Q137.1 73.5 141.2 72.5Q145.2 71.6 146.9 69.9Q147.2 69.6 148.1 69.6Q148.9 69.6 151.3 72.8Q153.6 76 155.6 81.2Q157.6 86.4 157.6 89.3Q157.6 94.9 149.1 98.1Q140.5 101.4 128.8 101.4Q110 101.4 97.9 88.2Q85.7 74.9 85.7 50.7Q85.7 26.5 98.2 12.7Q110.7 -1.1 129.4 -1.1Q139.8 -1.1 147.7 1.8Q155.6 4.7 155.6 9.7Q155.6 14.7 151.9 22Q148.1 29.4 145.5 29.4Z"
    "M241.4 100.3Q229 100.3 228 96.3L223.3 77.9H200.6L196.4 95.6Q195.6 100 182.7 100Q175.9 100 172.6 99.2Q169.3 98.4 169.3 98L194.6 1.4Q194.6 0.3 214.1 0.3Q233.7 0.3 233.7 1.4L258.3 98.1Q258.3 99.1 251.8 99.7Q245.2 100.3 241.4 100.3ZM204.1 59.8H219.1L212.7 30.2H211.8Z"
    "M351.6 96.9Q351.6 99.9 338.2 99.9Q324.8 99.9 323.7 97.7L299.9 53.2V97.6Q299.9 100.1 286.7 100.1Q273.5 100.1 273.5 97.6V2.1Q273.5 0 284.7 0Q289.2 0 295.1 0.8Q301 1.6 302.3 3.7L325.1 47.6V2.9Q325.1 0.1 338.4 0.1Q351.6 0.1 351.6 2.9Z"
    "M504 100.1Q491.3 100.1 491.3 97.3L488.3 40.1L470.9 98Q470.3 99.7 461.2 99.7Q452.1 99.7 451.8 98.1L433.8 39.5L431.8 96.4Q431.7 98.6 426.4 99.4Q421.1 100.1 417.6 100.1Q414.1 100.1 410.8 99.7Q404 98.7 404.1 96.1L407.4 3.4Q407.4 0 424.8 0Q430 0 437.4 0.8Q444.8 1.6 445.6 3.9L461.6 48.8L475.6 3.7Q476.9 0 495.3 0Q500.6 0 507.9 0.8Q515.3 1.6 515.3 3.6L519.4 97.1Q519.4 98.7 513.8 99.4Q508.3 100.1 504 100.1Z"
    "M585.6 39.8Q588.3 39.8 588.3 49.8Q588.3 52.8 587.7 56.8Q587 60.9 585.3 60.9H567.2V75.2H593.4Q595.9 75.2 596.7 81.5Q597.1 84.2 597.1 87.2Q597.1 90.3 596.3 95.1Q595.4 100 593.4 100H544.7Q539.2 100 539.2 95.6V3.9Q539.2 0.1 542.5 0.1H593.6Q596.6 0.1 596.6 12.8Q596.6 25.4 593.6 25.4H567.2V39.8Z"
)


def dark_runs(qr):
    """Dark modules as horizontal runs in one SVG path, in module units."""
    parts = []
    for y, row in enumerate(qr.matrix):
        x = 0
        while x < len(row):
            if not row[x]:
                x += 1
                continue
            start = x
            while x < len(row) and row[x]:
                x += 1
            parts.append(f"M{start} {y}h{x - start}v1h{start - x}z")
    return "".join(parts)


def sparkle(x, y, r):
    return f"M{x} {y - r}Q{x} {y} {x + r} {y}Q{x} {y} {x} {y + r}Q{x} {y} {x - r} {y}Q{x} {y} {x} {y - r}Z"


def poster_svg(qr):
    n = len(qr.matrix)
    m = 440 // (n + 8)  # whole-pixel modules keep the edges crisp
    panel = (n + 8) * m
    w, top, gap, banner_w, banner_h = 600, 72, 40, 400, 110
    h = top + panel + gap + banner_h + 72
    left, cx, by = (w - panel) / 2, w / 2, top + panel + gap
    s = 0.56
    tx, ty = cx - TEXT_WIDTH * s / 2, by + (banner_h - 100 * s) / 2
    o, arm = 22, 62
    x0, y0, x1, y1 = left - o, top - o, left + panel + o, top + panel + o
    brackets = (
        f"M{x0} {y0 + arm}V{y0}H{x0 + arm}"
        f"M{x1 - arm} {y0}H{x1}V{y0 + arm}"
        f"M{x1} {y1 - arm}V{y1}H{x1 - arm}"
        f"M{x0 + arm} {y1}H{x0}V{y1 - arm}"
    )
    sparkles = "".join(
        sparkle(cx + dx, by + dy, r) for dx, dy, r in ((236, 4, 17), (266, -20, 9), (-238, 100, 14), (-266, 74, 8))
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <radialGradient id="bg" cx=".5" cy=".28" r=".9">
      <stop offset="0" stop-color="{ROAST}"/>
      <stop offset="1" stop-color="{ESPRESSO}"/>
    </radialGradient>
    <filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <rect x="{left}" y="{top + 14}" width="{panel}" height="{panel}" rx="30" fill="#000" opacity=".4" filter="url(#blur)"/>
  <rect x="{left}" y="{top}" width="{panel}" height="{panel}" rx="30" fill="{MILK}"/>
  <g transform="translate({left + 4 * m} {top + 4 * m}) scale({m})">
    <path d="{dark_runs(qr)}" fill="{ESPRESSO}" shape-rendering="crispEdges"/>
  </g>
  <path d="{brackets}" fill="none" stroke="{SAFFRON}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M{cx - 26} {by + 4}L{cx} {by - 30}L{cx + 26} {by + 4}Z" fill="{SAFFRON}" stroke="{SAFFRON}" stroke-width="6" stroke-linejoin="round"/>
  <rect x="{cx - banner_w / 2}" y="{by + 8}" width="{banner_w}" height="{banner_h}" rx="55" fill="#b9770e"/>
  <rect x="{cx - banner_w / 2}" y="{by}" width="{banner_w}" height="{banner_h}" rx="55" fill="{SAFFRON}"/>
  <path transform="translate({tx} {ty}) scale({s})" d="{TEXT_PATH}" fill="{ESPRESSO}"/>
  <path d="{sparkles}" fill="{MILK}"/>
</svg>"""
    return svg, w, h


def find_edge():
    for var in ("ProgramFiles(x86)", "ProgramFiles"):
        exe = Path(os.environ.get(var, "")) / "Microsoft/Edge/Application/msedge.exe"
        if exe.exists():
            return exe
    return None


def render_png(svg, png, width, height):
    """Rasterise the poster with headless Edge; returns False when Edge is missing."""
    edge = find_edge()
    if not edge:
        return False
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "poster.html"
        page.write_text(
            f"<!doctype html><style>body{{margin:0}}svg{{display:block;width:{width}px;height:{height}px}}</style>{svg}",
            encoding="utf-8",
        )
        subprocess.run(
            [
                str(edge), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                f"--user-data-dir={Path(tmp) / 'profile'}", f"--window-size={width},{height}",
                f"--screenshot={png}", page.as_uri(),
            ],
            check=True, capture_output=True, timeout=120,
        )
    return png.exists()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Final public https:// address of the website")
    parser.add_argument("--name", default="coffeeguy", help="File name prefix")
    parser.add_argument("--out", type=Path, default=OUT_DIR, help="Output folder (default: ./qr)")
    args = parser.parse_args()

    parsed = urlparse(args.url)
    if parsed.scheme != "https" or not parsed.netloc:
        parser.error("url must be a full https:// address")

    args.out.mkdir(parents=True, exist_ok=True)
    qr = segno.make(args.url, error="q")
    for ext, scale in (("png", 20), ("svg", 10)):
        path = args.out / f"{args.name}-qr.{ext}"
        qr.save(path, scale=scale, border=4)
        print(f"Saved {path}")

    svg, w, h = poster_svg(qr)
    svg_path = args.out / f"{args.name}-scan-me.svg"
    svg_path.write_text(svg, encoding="utf-8")
    print(f"Saved {svg_path}")
    png_path = args.out / f"{args.name}-scan-me.png"
    if render_png(svg, png_path, 2 * w, 2 * h):
        print(f"Saved {png_path}")
    else:
        print("Poster PNG skipped: Microsoft Edge not found (the SVG is complete)")


if __name__ == "__main__":
    main()
