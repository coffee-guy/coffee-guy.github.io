"""Build docs/images/logo.svg (run with the repo's .venv): python art/gen.py [out.svg] [bg,woman,man,dog,table,petals]"""
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
from make_qr import text_group  # noqa: E402

from lib import *  # noqa: E402,F401,F403

OL = "#2b1810"
CREAM = "#fff4e3"
SAFF = "#f3b23c"
SAFF_D = "#d9951f"
GREEN_D = "#2f6b5e"
CX, CY, R = 400, 400, 372

DEFS = []
LAYERS = {}


def defs():
    return """
<clipPath id="lg-clip"><circle cx="400" cy="400" r="372"/></clipPath>
<linearGradient id="lg-wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d2e8cf"/><stop offset="1" stop-color="#a2ccaa"/></linearGradient>
<linearGradient id="lg-glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffecb8"/><stop offset="1" stop-color="#ffc471"/></linearGradient>
<linearGradient id="lg-awn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a3d00" stop-opacity=".30"/><stop offset="1" stop-color="#7a3d00" stop-opacity="0"/></linearGradient>
<linearGradient id="lg-shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f6b5e" stop-opacity=".55"/><stop offset="1" stop-color="#2f6b5e" stop-opacity="0"/></linearGradient>
<linearGradient id="lg-ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cdb99a"/><stop offset="1" stop-color="#e6d6ba"/></linearGradient>
<radialGradient id="lg-bulb"><stop offset="0" stop-color="#fff6c8" stop-opacity=".95"/><stop offset=".4" stop-color="#ffe08a" stop-opacity=".5"/><stop offset="1" stop-color="#ffd36a" stop-opacity="0"/></radialGradient>
<radialGradient id="lg-sun" cx=".18" cy=".1" r=".75"><stop offset="0" stop-color="#fff7d6" stop-opacity=".75"/><stop offset=".5" stop-color="#ffeab0" stop-opacity=".18"/><stop offset="1" stop-color="#ffeab0" stop-opacity="0"/></radialGradient>
<radialGradient id="lg-vig" cx=".5" cy=".5" r=".5"><stop offset=".72" stop-color="#3a1d10" stop-opacity="0"/><stop offset="1" stop-color="#3a1d10" stop-opacity=".2"/></radialGradient>
<linearGradient id="lg-stub" gradientUnits="userSpaceOnUse" x1="0" y1="18" x2="0" y2="86"><stop offset="0" stop-color="#4a3026" stop-opacity="0"/><stop offset=".55" stop-color="#4a3026" stop-opacity=".12"/><stop offset="1" stop-color="#4a3026" stop-opacity=".2"/></linearGradient>
<g id="lg-fl"><g fill="#fcd3df" stroke="#e98aa8" stroke-width="1.1" stroke-linejoin="round">
<path d="M0 -1.5C-6 -4 -7 -11 -3.4 -13.6C-1.8 -14.8 -.6 -13.4 0 -12.2C.6 -13.4 1.8 -14.8 3.4 -13.6C7 -11 6 -4 0 -1.5Z" transform="rotate(0)"/>
<path d="M0 -1.5C-6 -4 -7 -11 -3.4 -13.6C-1.8 -14.8 -.6 -13.4 0 -12.2C.6 -13.4 1.8 -14.8 3.4 -13.6C7 -11 6 -4 0 -1.5Z" transform="rotate(72)"/>
<path d="M0 -1.5C-6 -4 -7 -11 -3.4 -13.6C-1.8 -14.8 -.6 -13.4 0 -12.2C.6 -13.4 1.8 -14.8 3.4 -13.6C7 -11 6 -4 0 -1.5Z" transform="rotate(144)"/>
<path d="M0 -1.5C-6 -4 -7 -11 -3.4 -13.6C-1.8 -14.8 -.6 -13.4 0 -12.2C.6 -13.4 1.8 -14.8 3.4 -13.6C7 -11 6 -4 0 -1.5Z" transform="rotate(216)"/>
<path d="M0 -1.5C-6 -4 -7 -11 -3.4 -13.6C-1.8 -14.8 -.6 -13.4 0 -12.2C.6 -13.4 1.8 -14.8 3.4 -13.6C7 -11 6 -4 0 -1.5Z" transform="rotate(288)"/></g>
<circle r="2.6" fill="#f2a9bf"/><circle r="1" fill="#fff1b0"/></g>
<g id="lg-pt"><path d="M0 -4C3 -3.5 5.5 -1 5.5 1C5.5 3 3 4.5 0 4C-.6 2 -.6 -2 0 -4Z" fill="#fcc9d7"/><path d="M0 -3.2C.4 -1 .4 1.6 0 3.4" stroke="#f08aa8" stroke-width=".8" fill="none"/></g>
"""


def rect_arch(cx, top, w, bottom):
    r = w / 2
    return f"M{fmt(cx - r)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + r)} {fmt(top + r)}V{fmt(bottom)}Z"


def background():
    s = ['<rect width="800" height="800" fill="url(#lg-wall)"/>']
    # clapboard siding
    for y in range(110, 700, 26):
        s.append(f'<path d="M0 {y}H800" stroke="#82b190" stroke-width="2" opacity=".4"/>')
        s.append(f'<path d="M0 {y + 3}H800" stroke="#eaf6e6" stroke-width="1.6" opacity=".45"/>')

    # windows and door (behind the people)
    for cx in (205, 595):
        d = rect_arch(cx, 292, 230, 540)
        s.append(P(d, "url(#lg-glass)"))
        # interior hints: pendant lamps and shelves
        for lx, ly, lr in ((cx - 52, 372, 15), (cx + 56, 358, 13)):
            s.append(f'<path d="M{lx} 300V{ly - lr}" stroke="#b9772a" stroke-width="2.4" opacity=".7"/>')
            s.append(f'<path d="M{lx - lr} {ly}Q{lx} {ly - lr * 1.5} {lx + lr} {ly}Z" fill="#e48f3a" opacity=".8"/>')
            s.append(f'<circle cx="{lx}" cy="{ly + 4}" r="{lr * 2}" fill="url(#lg-bulb)"/>')
        for sy in (452, 500):
            s.append(f'<path d="M{cx - 108} {sy}H{cx + 108}" stroke="#d58a3c" stroke-width="5" opacity=".55"/>')
            jx = cx - 96
            rnd = random.Random(int(cx) + sy)
            while jx < cx + 92:
                jw, jh = rnd.uniform(10, 20), rnd.uniform(18, 32)
                s.append(f'<rect x="{fmt(jx)}" y="{fmt(sy - 3 - jh)}" width="{fmt(jw)}" height="{fmt(jh)}" rx="3" fill="#e0933f" opacity=".45"/>')
                jx += jw + rnd.uniform(5, 12)
        s.append(P(d, "none", OL, 20))
        s.append(P(d, "none", CREAM, 14))
        s.append(P(d, "none", OL, 2))
        s.append(f'<rect x="{cx - 130}" y="536" width="260" height="14" rx="3" fill="{CREAM}" stroke="{OL}" stroke-width="3"/>')

    # door
    d = rect_arch(400, 300, 112, 640)
    s.append(P(d, GREEN_D, OL, 20))
    s.append(P(d, GREEN_D, CREAM, 13))
    s.append(P(d, GREEN_D, OL, 2))
    g = rect_arch(400, 316, 80, 372)
    s.append(P(g, "url(#lg-glass)", OL, 3))
    s.append(f'<path d="M400 316V372M360 372H440" stroke="{OL}" stroke-width="3"/>')
    s.append('<path d="M366 404H434V470H366Z M366 494H434V572H366Z" fill="#25574c" stroke="#1a3f37" stroke-width="3"/>')

    # awning shadow on the wall
    s.append('<rect x="0" y="232" width="800" height="110" fill="url(#lg-shade)"/>')

    # awning
    top_y, front_y = 100, 196
    tx0, tx1, bx0, bx1, N = 215, 585, 60, 740, 14
    for i in range(N):
        a0, a1 = tx0 + (tx1 - tx0) * i / N, tx0 + (tx1 - tx0) * (i + 1) / N
        b0, b1 = bx0 + (bx1 - bx0) * i / N, bx0 + (bx1 - bx0) * (i + 1) / N
        col = SAFF if i % 2 == 0 else CREAM
        s.append(f'<path d="M{fmt(a0)} {top_y}L{fmt(a1)} {top_y}L{fmt(b1)} {front_y}L{fmt(b0)} {front_y}Z" fill="{col}"/>')
    s.append(f'<path d="M{tx0} {top_y}L{tx1} {top_y}L{bx1} {front_y}L{bx0} {front_y}Z" fill="url(#lg-awn)"/>')
    for i in range(N + 1):
        a = tx0 + (tx1 - tx0) * i / N
        b = bx0 + (bx1 - bx0) * i / N
        s.append(f'<path d="M{fmt(a)} {top_y}L{fmt(b)} {front_y}" stroke="{OL}" stroke-width="1.6" opacity=".55"/>')
    s.append(f'<path d="M{tx0} {top_y}L{tx1} {top_y}L{bx1} {front_y}L{bx0} {front_y}Z" fill="none" stroke="{OL}" stroke-width="4" stroke-linejoin="round"/>')
    # valance with scalloped hem
    vy, vh = front_y, 36
    sw_ = (bx1 - bx0) / N
    d = f"M{bx0} {vy}H{bx1}V{vy + vh}"
    for i in range(N):
        d += f"A{fmt(sw_ / 2)} {fmt(sw_ / 2)} 0 0 1 {fmt(bx1 - sw_ * (i + 1))} {vy + vh}"
    d += "Z"
    s.append(shaded(d, SAFF, SAFF_D, (0, -5), OL, 4))
    s.append(f'<path d="M{bx0 + 6} {vy + 7}H{bx1 - 6}" stroke="#fff0c2" stroke-width="2" opacity=".6"/>')
    txt, tw = text_group("COFFEE GUY", 24, OL, 400, vy + 6, "middle", 6)
    s.append(txt)
    # bulbs under the scallops
    for i in range(N):
        bx = bx0 + sw_ * (i + 0.5)
        by = vy + vh + sw_ / 2 + 9
        s.append(f'<circle cx="{fmt(bx)}" cy="{fmt(by)}" r="17" fill="url(#lg-bulb)"/>')
        s.append(f'<path d="M{fmt(bx)} {fmt(by - 12)}V{fmt(by - 5)}" stroke="{OL}" stroke-width="2"/>')
        s.append(f'<ellipse cx="{fmt(bx)}" cy="{fmt(by)}" rx="4.6" ry="5.6" fill="#fff3b8" stroke="#b97a22" stroke-width="1.4"/>')
    return "".join(s)


def blossoms():
    s = []
    rnd = random.Random(7)

    def mass(cx, cy, rx, ry, n, seed):
        r_ = random.Random(seed)
        out = []
        cols = ["#f7b9cb", "#fbcfdb", "#f4a6bd", "#fddbe4"]
        for _ in range(n):
            a, rr = r_.uniform(0, 6.283), math.sqrt(r_.random())
            x, y = cx + math.cos(a) * rx * rr, cy + math.sin(a) * ry * rr
            out.append((x, y, r_.uniform(13, 25), r_.choice(cols)))
        out.sort(key=lambda o: o[1])
        g = []
        for x, y, r, c in out:
            g.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{c}"/>')
        for x, y, r, c in out[::2]:
            g.append(f'<circle cx="{fmt(x - r * .3)}" cy="{fmt(y - r * .35)}" r="{fmt(r * .45)}" fill="#fff0f4" opacity=".7"/>')
        for _ in range(int(n * 0.55)):
            a, rr = r_.uniform(0, 6.283), math.sqrt(r_.random())
            x, y = cx + math.cos(a) * rx * rr, cy + math.sin(a) * ry * rr
            g.append(f'<use href="#lg-fl" transform="translate({fmt(x)} {fmt(y)}) rotate({fmt(r_.uniform(0, 72))}) scale({fmt(r_.uniform(.8, 1.25))})"/>')
        return "".join(g)

    # branches
    s.append(f'<path d="M-10 330C40 300 60 240 110 190S190 120 250 100" fill="none" stroke="#5e3a2a" stroke-width="12" stroke-linecap="round"/>')
    s.append(f'<path d="M810 330C760 300 740 240 690 190S610 120 550 100" fill="none" stroke="#5e3a2a" stroke-width="12" stroke-linecap="round"/>')
    s.append(mass(95, 190, 90, 80, 38, 1))
    s.append(mass(215, 112, 80, 30, 22, 2))
    s.append(mass(705, 190, 90, 80, 38, 3))
    s.append(mass(585, 112, 80, 30, 22, 4))
    return "".join(s)


def table():
    s = []
    # ground
    s.append('<rect x="0" y="640" width="800" height="200" fill="url(#lg-ground)"/>')
    s.append(f'<path d="M0 640H800" stroke="{OL}" stroke-width="3" opacity=".5"/>')
    rnd = random.Random(11)
    for row in range(5):
        y = 656 + row * 30
        x = -20 + (row % 2) * 30
        while x < 820:
            w = rnd.uniform(46, 70)
            s.append(f'<rect x="{fmt(x)}" y="{y}" width="{fmt(w - 4)}" height="24" rx="8" fill="#d8c5a5" opacity=".6"/>')
            x += w
    s.append('<ellipse cx="400" cy="722" rx="330" ry="46" fill="#4a2e1c" opacity=".2"/>')
    # pedestal
    s.append(f'<path d="M386 680H414V742H386Z" fill="#3a3430" stroke="{OL}" stroke-width="3"/>')
    s.append(f'<ellipse cx="400" cy="748" rx="76" ry="13" fill="#3a3430" stroke="{OL}" stroke-width="3"/>')
    # top
    cx, cy, rx, ry, th = 400, 612, 285, 60, 18
    rim = f"M{cx - rx} {cy}A{rx} {ry} 0 0 0 {cx + rx} {cy}V{cy + th}A{rx} {ry} 0 0 1 {cx - rx} {cy + th}Z"
    s.append(shaded(rim, "#b9763a", "#8f5426", (0, -6), OL, 4))
    top = ell(cx, cy, rx, ry)
    s.append(shaded(top, "#e3b077", "#cf9a5e", (-10, -7), OL, 4))
    s.append(f'<path d="M{cx - rx + 34} {cy - 4}A{rx - 34} {ry - 12} 0 0 1 {cx - 60} {cy - ry + 14}" fill="none" stroke="#f8e0b6" stroke-width="4.5" stroke-linecap="round" opacity=".6"/>')
    s.append(f'<path d="M{cx + rx - 40} {cy + 12}A{rx - 40} {ry - 14} 0 0 1 {cx + 70} {cy + ry - 16}" fill="none" stroke="#b27a42" stroke-width="3.5" stroke-linecap="round" opacity=".35"/>')
    return "".join(s)


def petals(seed, n, box, z=None):
    r_ = random.Random(seed)
    x0, y0, x1, y1 = box
    avoid = ((140, 205, 270, 360), (525, 195, 665, 360), (300, 335, 500, 560))
    out = []
    while len(out) < n:
        x, y = r_.uniform(x0, x1), r_.uniform(y0, y1)
        if any(a <= x <= c and b <= y <= d for a, b, c, d in avoid):
            continue
        out.append(f'<use href="#lg-pt" transform="translate({fmt(x)} {fmt(y)}) rotate({fmt(r_.uniform(0, 360))}) scale({fmt(r_.uniform(.9, 1.6))})"/>')
    return "".join(out)


def build(parts):
    import chars
    import dog as dog_mod
    import man as man_mod

    body, backs, fronts = [], [], []
    if "woman" in parts:
        b, f = chars.woman(205)
        backs.append(b)
        fronts.append(f)
    if "man" in parts:
        b, f = man_mod.man(595)
        backs.append(b)
        fronts.append(f)
    if "dog" in parts:
        b, f = dog_mod.dog(400)
        backs.append(b)
        fronts.append(f)
    if "bg" in parts:
        body.append(background())
        body.append(blossoms())
        body.append('<rect width="800" height="800" fill="url(#lg-sun)"/>')
    body.extend(backs)
    if "table" in parts:
        body.append(table())
    body.extend(fronts)
    if "petals" in parts:
        body.append(petals(5, 26, (80, 120, 720, 700)))
    return body


def assemble(body):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">'
        f"<defs>{defs()}</defs>"
        '<g transform="scale(.5)">'
        f'<circle cx="400" cy="400" r="394" fill="{OL}"/><circle cx="400" cy="400" r="384" fill="{SAFF}"/><circle cx="400" cy="400" r="376" fill="{OL}"/>'
        f'<g clip-path="url(#lg-clip)">{"".join(body)}'
        '<rect width="800" height="800" fill="url(#lg-vig)"/></g>'
        "</g></svg>"
    )


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "images" / "logo.svg"
    parts = (sys.argv[2] if len(sys.argv) > 2 else "bg,woman,man,dog,table,petals").split(",")
    out.write_text(assemble(build(parts)), encoding="utf-8")
    print("wrote", out, out.stat().st_size, "bytes")
