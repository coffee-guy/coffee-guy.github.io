"""Generate the website QR code in ./qr: a plain code and a friendly "SCAN ME" poster, each as PNG and SVG."""

import argparse
import os
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import segno

OUT_DIR = Path(__file__).resolve().parent / "qr"
LOGO = Path(__file__).resolve().parent / "docs" / "images" / "logo.svg"

ESPRESSO, SAFFRON, CREAM, CORAL, CORAL_DARK = "#2b1810", "#f3b23c", "#fff4e3", "#ff6b5e", "#d94a3d"

# "SCAN ME" outlined from Lilita One (SIL OFL); 100 units tall.
SCAN_ME_WIDTH = 602.4
SCAN_ME_PATH = (
    "M10.8 65.2Q13.6 67.3 20.2 71Q26.8 74.8 32.9 74.8Q38.9 74.8 38.9 70Q38.9 67.9 37.2 66.3Q35.5 64.6 31 62.5Q26.4 60.3 24.1 59.1Q21.8 57.9 18 55.1Q14.3 52.4 12.3 49.4Q6.6 41.2 6.6 28.7Q6.6 16.1 15.9 7.5Q25.2 -1.1 40.4 -1.1Q50.6 -1.1 59.3 1.1Q68 3.3 68.3 6.8Q68.3 7.3 68.3 7.7Q68.3 12.7 65.2 20.3Q62.1 28 60.8 28.8Q51.6 24.1 44.4 24.1Q37.2 24.1 37.2 29.2Q37.2 32.4 42.5 34.8Q43.7 35.4 45.8 36.4Q47.9 37.4 50.7 38.7Q53.5 40.1 56.7 42.2Q59.9 44.2 63.6 47.6Q71.2 54.8 71.2 66.5Q71.2 81.7 62.8 91.4Q54.4 101.1 36.8 101.4Q28.2 101.4 21.3 100Q14.4 98.6 9.3 94.4Q4.1 90.3 4.1 84.5Q4.1 78.6 6.3 72.8Q8.4 67 10.8 65.2Z"
    "M145.5 29.4Q144.8 29.4 143.9 28.6Q142.9 27.8 139.6 26.9Q136.2 26 133.8 26Q125.5 26 120.5 31.8Q115.4 37.7 115.4 49.7Q115.4 61.8 120.6 67.6Q125.8 73.5 133.8 73.5Q137.1 73.5 141.2 72.5Q145.2 71.6 146.9 69.9Q147.2 69.6 148.1 69.6Q148.9 69.6 151.3 72.8Q153.6 76 155.6 81.2Q157.6 86.4 157.6 89.3Q157.6 94.9 149.1 98.1Q140.5 101.4 128.8 101.4Q110 101.4 97.9 88.2Q85.7 74.9 85.7 50.7Q85.7 26.5 98.2 12.7Q110.7 -1.1 129.4 -1.1Q139.8 -1.1 147.7 1.8Q155.6 4.7 155.6 9.7Q155.6 14.7 151.9 22Q148.1 29.4 145.5 29.4Z"
    "M241.4 100.3Q229 100.3 228 96.3L223.3 77.9H200.6L196.4 95.6Q195.6 100 182.7 100Q175.9 100 172.6 99.2Q169.3 98.4 169.3 98L194.6 1.4Q194.6 0.3 214.1 0.3Q233.7 0.3 233.7 1.4L258.3 98.1Q258.3 99.1 251.8 99.7Q245.2 100.3 241.4 100.3ZM204.1 59.8H219.1L212.7 30.2H211.8Z"
    "M351.6 96.9Q351.6 99.9 338.2 99.9Q324.8 99.9 323.7 97.7L299.9 53.2V97.6Q299.9 100.1 286.7 100.1Q273.5 100.1 273.5 97.6V2.1Q273.5 0 284.7 0Q289.2 0 295.1 0.8Q301 1.6 302.3 3.7L325.1 47.6V2.9Q325.1 0.1 338.4 0.1Q351.6 0.1 351.6 2.9Z"
    "M504 100.1Q491.3 100.1 491.3 97.3L488.3 40.1L470.9 98Q470.3 99.7 461.2 99.7Q452.1 99.7 451.8 98.1L433.8 39.5L431.8 96.4Q431.7 98.6 426.4 99.4Q421.1 100.1 417.6 100.1Q414.1 100.1 410.8 99.7Q404 98.7 404.1 96.1L407.4 3.4Q407.4 0 424.8 0Q430 0 437.4 0.8Q444.8 1.6 445.6 3.9L461.6 48.8L475.6 3.7Q476.9 0 495.3 0Q500.6 0 507.9 0.8Q515.3 1.6 515.3 3.6L519.4 97.1Q519.4 98.7 513.8 99.4Q508.3 100.1 504 100.1Z"
    "M585.6 39.8Q588.3 39.8 588.3 49.8Q588.3 52.8 587.7 56.8Q587 60.9 585.3 60.9H567.2V75.2H593.4Q595.9 75.2 596.7 81.5Q597.1 84.2 597.1 87.2Q597.1 90.3 596.3 95.1Q595.4 100 593.4 100H544.7Q539.2 100 539.2 95.6V3.9Q539.2 0.1 542.5 0.1H593.6Q596.6 0.1 596.6 12.8Q596.6 25.4 593.6 25.4H567.2V39.8Z"
)

# "COFFEE GUY" outlined the same way.
BRAND_WIDTH = 824.4
BRAND_PATH = (
    "M64.1 29.4Q63.3 29.4 62.4 28.6Q61.5 27.8 58.1 26.9Q54.8 26 52.4 26Q44.1 26 39 31.8Q34 37.7 34 49.7Q34 61.8 39.2 67.6Q44.4 73.5 52.4 73.5Q55.6 73.5 59.7 72.5Q63.8 71.6 65.5 69.9Q65.8 69.6 66.6 69.6Q67.5 69.6 69.8 72.8Q72.2 76 74.2 81.2Q76.2 86.4 76.2 89.3Q76.2 94.9 67.6 98.1Q59.1 101.4 47.4 101.4Q28.5 101.4 16.4 88.2Q4.3 74.9 4.3 50.7Q4.3 26.5 16.8 12.7Q29.2 -1.1 47.9 -1.1Q58.3 -1.1 66.3 1.8Q74.2 4.7 74.2 9.7Q74.2 14.7 70.4 22Q66.6 29.4 64.1 29.4Z"
    "M138.2 101.4Q118.1 101.4 105.5 88.3Q92.9 75.2 92.9 50Q92.9 24.8 105.6 11.8Q118.4 -1.1 138.6 -1.1Q158.8 -1.1 171.2 11.6Q183.6 24.4 183.6 50.3Q183.6 76.2 170.9 88.8Q158.2 101.4 138.2 101.4ZM138.2 26.2Q131.4 26.2 126.7 32.5Q122.1 38.8 122.1 50.1Q122.1 61.5 126.5 67.5Q131 73.6 138.2 73.6Q145.4 73.6 149.9 67.5Q154.4 61.3 154.4 49.9Q154.4 38.5 149.7 32.4Q145.1 26.2 138.2 26.2Z"
    "M256.9 0.1Q259.3 0.1 259.3 12.8Q259.3 25.4 256.9 25.4H230.8V41.7H248.2Q250.6 41.7 250.6 52.7Q250.6 63.8 248.4 63.8H230.8V98.1Q230.8 100.1 225.5 100.8Q220.1 101.4 216.5 101.4L209.8 101.1Q202.9 100.3 202.9 98.3V3.9Q202.9 1.6 203.8 0.9Q204.7 0.1 206.6 0.1Z"
    "M332.8 0.1Q335.2 0.1 335.2 12.8Q335.2 25.4 332.8 25.4H306.7V41.7H324.1Q326.5 41.7 326.5 52.7Q326.5 63.8 324.3 63.8H306.7V98.1Q306.7 100.1 301.4 100.8Q296 101.4 292.4 101.4L285.7 101.1Q278.7 100.3 278.7 98.3V3.9Q278.7 1.6 279.7 0.9Q280.6 0.1 282.5 0.1Z"
    "M401.7 39.8Q404.4 39.8 404.4 49.8Q404.4 52.8 403.8 56.8Q403.1 60.9 401.4 60.9H383.3V75.2H409.6Q412 75.2 412.8 81.5Q413.3 84.2 413.3 87.2Q413.3 90.3 412.4 95.1Q411.6 100 409.6 100H360.8Q355.3 100 355.3 95.6V3.9Q355.3 0.1 358.6 0.1H409.7Q412.7 0.1 412.7 12.8Q412.7 25.4 409.7 25.4H383.3V39.8Z"
    "M480.6 39.8Q483.3 39.8 483.3 49.8Q483.3 52.8 482.7 56.8Q482 60.9 480.3 60.9H462.2V75.2H488.4Q490.9 75.2 491.7 81.5Q492.2 84.2 492.2 87.2Q492.2 90.3 491.3 95.1Q490.4 100 488.4 100H439.7Q434.2 100 434.2 95.6V3.9Q434.2 0.1 437.5 0.1H488.6Q491.6 0.1 491.6 12.8Q491.6 25.4 488.6 25.4H462.2V39.8Z"
    "M601.3 70.2L601.6 50.8Q601.6 48.8 605.7 48.1Q609.8 47.5 612.6 47.5L618.1 47.9Q623.5 48.8 623.5 50.9L623 95.6Q620.1 97.6 611.5 99.5Q602.9 101.4 591.7 101.4Q571 101.4 558.3 88Q545.6 74.6 545.6 48.6Q545.6 26.5 558.1 12.7Q570.5 -1.1 592.4 -1.1Q602.4 -1.1 610.5 0.8Q618.5 2.7 621.5 6Q621.7 7.1 621.7 10.3Q621.7 13.4 619.5 19.2Q617.4 25 614.7 27.8Q612 30.7 610.8 30.7Q609.6 30.7 608.2 29.6Q606.8 28.5 602.9 27.3Q598.9 26.1 595.1 26.1Q586.3 26.1 580.8 31.8Q575.3 37.5 575.3 49.5Q575.3 61.5 581 67.7Q586.6 73.9 593.9 73.9Q601.3 73.9 601.3 70.2Z"
    "M692.3 3Q692.3 0.1 707.8 0.1Q723.3 0.1 723.3 3V68.5Q723.3 83 712.8 92.2Q702.4 101.4 684.1 101.4Q665.8 101.4 654.3 91.9Q642.8 82.5 642.8 66.3V3.1Q642.8 0.3 658.3 0.3Q673.8 0.3 673.8 3.1V67.5Q673.8 70.3 676.7 72Q679.9 73.8 683.3 73.8Q686.7 73.8 689.5 72.2Q692.3 70.6 692.3 67.5Z"
    "M793.4 4.9Q795.3 -0.1 811.7 -0.1Q815.8 -0.1 821.5 0.4Q827.1 1 826.7 1.9L797 61.5V96.3Q797 98.7 789.2 99.7Q785.2 100.3 781.3 100.3Q777.5 100.3 773.6 99.9Q765.8 98.9 765.8 96.3V62.3L735.1 2.1Q734.5 1.3 740.9 0.5Q747.4 -0.3 751.8 -0.3Q769.3 -0.3 771 4.9L781.5 34Z"
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


def heart(x, y, s, fill):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0,8C-18,-4 -10,-16 0,-8C10,-16 18,-4 0,8Z" fill="{fill}"/>'


def paw(x, y, s, fill):
    toes = "".join(
        f'<ellipse cx="{dx}" cy="{dy}" rx="4.6" ry="6.4" transform="rotate({rot} {dx} {dy})"/>'
        for dx, dy, rot in ((-13, -3, -25), (-5, -13, -8), (5, -13, 8), (13, -3, 25))
    )
    pad = '<path d="M0,-2C8,-2 14,6 14,11C14,16 9,17 0,17C-9,17 -14,16 -14,11C-14,6 -8,-2 0,-2Z"/>'
    return f'<g transform="translate({x} {y}) scale({s})" fill="{fill}">{toes}{pad}</g>'


def logo_group(x, y, size):
    markup = LOGO.read_text(encoding="utf-8")
    inner = markup[markup.index(">", markup.index("<svg")) + 1 : markup.rindex("</svg>")]
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 400 400">{inner}</svg>'


def poster_svg(qr):
    n = len(qr.matrix)
    m = 440 // (n + 8)  # whole-pixel modules keep the edges crisp
    panel = (n + 8) * m
    w, border, pad, top_pad, badge, badge_y = 600, 8, 14, 62, 272, 22
    card_w, card_h = panel + 2 * (pad + border), panel + top_pad + pad + 2 * border
    card_x, card_y = (w - card_w) / 2, 232
    qx, qy = card_x + border + pad, card_y + border + top_pad
    ribbon_w, ribbon_h = 440, 92
    ribbon_x, ribbon_y = (w - ribbon_w) / 2, qy + panel + 14
    s, t = 0.5, 0.36
    scan_x, scan_y = w / 2 - SCAN_ME_WIDTH * s / 2, ribbon_y + (ribbon_h - 100 * s) / 2 - 2
    brand_x, brand_y = w / 2 - BRAND_WIDTH * t / 2, ribbon_y + ribbon_h + 26
    h = round(brand_y + 100 * t + 30)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#8fd0f2"/>
      <stop offset=".55" stop-color="#d9f1fc"/>
      <stop offset="1" stop-color="{CREAM}"/>
    </linearGradient>
    <pattern id="dots" width="36" height="36" patternUnits="userSpaceOnUse"><circle cx="18" cy="18" r="3" fill="#fff" opacity=".45"/></pattern>
    <filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="10"/></filter>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#sky)"/>
  <rect width="{w}" height="{h}" fill="url(#dots)"/>
  <g fill="#fff">
    <ellipse cx="84" cy="96" rx="34" ry="13"/><ellipse cx="64" cy="104" rx="20" ry="10"/><ellipse cx="108" cy="104" rx="22" ry="10"/>
    <ellipse cx="520" cy="62" rx="30" ry="12"/><ellipse cx="540" cy="70" rx="18" ry="9"/><ellipse cx="500" cy="70" rx="18" ry="9"/>
  </g>
  <path d="M0,{h - 118}C100,{h - 138} 200,{h - 132} 300,{h - 112}S500,{h - 120} 600,{h - 130}V{h + 10}H0Z" fill="#8fd07f" stroke="#3b2418" stroke-width="3"/>
  <path d="M0,{h - 92}C120,{h - 108} 240,{h - 100} 330,{h - 94}S520,{h - 110} 600,{h - 98}V{h + 10}H0Z" fill="#a3dd93" stroke="#3b2418" stroke-width="3"/>
  <g>
    <circle cx="40" cy="{h - 62}" r="5.5" fill="#ff9db1"/><circle cx="40" cy="{h - 62}" r="2" fill="#ffe27a"/>
    <circle cx="96" cy="{h - 34}" r="5" fill="#fff"/><circle cx="96" cy="{h - 34}" r="1.8" fill="#ffd45a"/>
    <circle cx="560" cy="{h - 60}" r="5" fill="#fff"/><circle cx="560" cy="{h - 60}" r="1.8" fill="#ffd45a"/>
    <circle cx="506" cy="{h - 32}" r="5.5" fill="#ff9db1"/><circle cx="506" cy="{h - 32}" r="2" fill="#ffe27a"/>
  </g>
  <rect x="{card_x}" y="{card_y + 14}" width="{card_w}" height="{card_h}" rx="40" fill="{ESPRESSO}" opacity=".25" filter="url(#blur)"/>
  <rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="40" fill="{SAFFRON}" stroke="{ESPRESSO}" stroke-width="4"/>
  <rect x="{card_x + border}" y="{card_y + border}" width="{card_w - 2 * border}" height="{card_h - 2 * border}" rx="32" fill="#fff"/>
  <g transform="translate({qx + 4 * m} {qy + 4 * m}) scale({m})">
    <path d="{dark_runs(qr)}" fill="{ESPRESSO}" shape-rendering="crispEdges"/>
  </g>
  <circle cx="{w / 2}" cy="{badge_y + badge / 2 + 8}" r="{badge / 2}" fill="{ESPRESSO}" opacity=".25" filter="url(#blur)"/>
  {logo_group((w - badge) / 2, badge_y, badge)}
  <rect x="{ribbon_x}" y="{ribbon_y + 8}" width="{ribbon_w}" height="{ribbon_h}" rx="46" fill="{CORAL_DARK}" stroke="{ESPRESSO}" stroke-width="4"/>
  <rect x="{ribbon_x}" y="{ribbon_y}" width="{ribbon_w}" height="{ribbon_h}" rx="46" fill="{CORAL}" stroke="{ESPRESSO}" stroke-width="4"/>
  <path d="M{ribbon_x + 44} {ribbon_y + 14}H{ribbon_x + ribbon_w - 44}" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".4"/>
  {paw(ribbon_x + 46, ribbon_y + 50, 0.9, "#fff")}
  {paw(ribbon_x + ribbon_w - 46, ribbon_y + 50, 0.9, "#fff")}
  <g transform="translate({scan_x} {scan_y}) scale({s})" stroke-linejoin="round">
    <path d="{SCAN_ME_PATH}" transform="translate(0 8)" fill="{ESPRESSO}" stroke="{ESPRESSO}" stroke-width="18"/>
    <path d="{SCAN_ME_PATH}" fill="{ESPRESSO}" stroke="{ESPRESSO}" stroke-width="18"/>
    <path d="{SCAN_ME_PATH}" fill="#fff"/>
  </g>
  <path d="{sparkle(58, 200, 15)}" fill="#fff"/>
  <path d="{sparkle(548, 176, 11)}" fill="#fff"/>
  <path d="{sparkle(556, 300, 9)}" fill="{SAFFRON}"/>
  {heart(40, ribbon_y + 40, 1.1, CORAL)}
  {heart(560, ribbon_y + 54, 0.9, CORAL)}
  <g transform="translate({brand_x} {brand_y}) scale({t})" stroke-linejoin="round">
    <path d="{BRAND_PATH}" fill="#fff" stroke="#fff" stroke-width="16"/>
    <path d="{BRAND_PATH}" fill="{ESPRESSO}"/>
  </g>
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
