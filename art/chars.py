"""Pieces shared by the characters: colours, print flowers, an eye, a hand and a cup."""
from lib import *  # noqa: F401,F403

OL = "#2b1810"
SAFF = "#f3b23c"
SKIN_W = ("#f6cfaa", "#e0a07c")
HAIR_W = ("#2c2024", "#150d10", "#745f6c")


def peony(x, y, r, rot=0):
    g = [f'<g transform="translate({fmt(x)} {fmt(y)}) rotate({fmt(rot)})">']
    for i in range(6):
        a = math.radians(i * 60)
        g.append(f'<circle cx="{fmt(math.cos(a) * r * .5)}" cy="{fmt(math.sin(a) * r * .5)}" r="{fmt(r * .52)}" fill="#2a1a2e"/>')
    g.append(f'<circle r="{fmt(r * .55)}" fill="#2a1a2e"/>')
    for i in range(3):
        a = math.radians(i * 120 + 20)
        g.append(
            f'<path d="M{fmt(math.cos(a) * r * .15)} {fmt(math.sin(a) * r * .15)}Q{fmt(math.cos(a + .7) * r * .6)} {fmt(math.sin(a + .7) * r * .6)} {fmt(math.cos(a + .2) * r * .85)} {fmt(math.sin(a + .2) * r * .85)}"'
            f' fill="none" stroke="#e9dbe6" stroke-width="{fmt(max(1.2, r * .07))}" stroke-linecap="round" opacity=".75"/>'
        )
    g.append("</g>")
    return "".join(g)


def leaf(x, y, L, rot):
    return (
        f'<path d="M0 0C{fmt(L * .3)} {fmt(-L * .22)} {fmt(L * .75)} {fmt(-L * .2)} {fmt(L)} 0C{fmt(L * .75)} {fmt(L * .2)} {fmt(L * .3)} {fmt(L * .22)} 0 0Z"'
        f' transform="translate({fmt(x)} {fmt(y)}) rotate({fmt(rot)})" fill="#23302b"/>'
    )


def eye(flip=False):
    """Right-hand eye in local coords (origin at the eye centre); flip mirrors it."""
    cid = nid()
    upper = "M-12 5C-11 -8 -1 -14 7 -13C12 -12 14 -6 14 -1"
    shape = upper + "C13 8 5 16 -3 15C-9 14 -12 10 -12 5Z"
    g = f'<clipPath id="{cid}"><path d="{shape}"/></clipPath>'
    g += f'<path d="{shape}" fill="#fffdf8"/>'
    g += f'<g clip-path="url(#{cid})">'
    g += '<ellipse cx="1" cy="1" rx="10" ry="14" fill="#6b3a24"/>'
    g += '<ellipse cx="1" cy="5" rx="9" ry="9.5" fill="#8a5232" opacity=".8"/>'
    g += '<ellipse cx="1" cy="2" rx="5.2" ry="8" fill="#1a0e0a"/>'
    g += '<path d="M-12 -14H14V-5C8 -9 -4 -9 -12 -3Z" fill="#000" opacity=".28"/>'
    g += '<circle cx="-2.6" cy="-5.2" r="3.8" fill="#fff"/><circle cx="5.2" cy="7.6" r="1.7" fill="#fff" opacity=".85"/>'
    g += "</g>"
    g += f'<path d="{upper}" fill="none" stroke="#1d100d" stroke-width="4.4" stroke-linecap="round"/>'
    g += '<path d="M14 -1L19.5 -5.5" stroke="#1d100d" stroke-width="3" stroke-linecap="round"/>'
    g += '<path d="M-9 14C-2 18 7 16 11 9" fill="none" stroke="#7a4a3a" stroke-width="1.4" stroke-linecap="round" opacity=".6"/>'
    g += '<path d="M-8 -16C0 -21 10 -20 16 -12" fill="none" stroke="#b97a5c" stroke-width="1.6" stroke-linecap="round" opacity=".55"/>'
    return f'<g transform="scale(-1 1)">{g}</g>' if flip else g


def hand(x, y, d, skin=None):
    """Palm at (x, y) with three fingers wrapping towards +d (1 or -1) along x."""
    skin = skin or SKIN_W
    s = []
    for k, dy in enumerate((-9, 0, 9)):
        x0, y0 = x + d * 4, y + dy
        x1, y1 = x + d * (22 - k % 2), y + dy + (1 if k == 0 else 0)
        s.append(f'<path d="M{x0} {y0}L{x1} {y1}" stroke="{OL}" stroke-width="10.5" stroke-linecap="round"/>')
        s.append(f'<path d="M{x0} {y0}L{x1} {y1}" stroke="{skin[0]}" stroke-width="6.6" stroke-linecap="round"/>')
    s.append(shaded(ell(x, y, 11, 15), skin[0], skin[1], (-3, -3), OL, 3))
    s.append(f'<path d="M{x + d * 1} {y - 13}L{x + d * 17} {y - 17}" stroke="{OL}" stroke-width="10.5" stroke-linecap="round"/>')
    s.append(f'<path d="M{x + d * 1} {y - 13}L{x + d * 17} {y - 17}" stroke="{skin[0]}" stroke-width="6.6" stroke-linecap="round"/>')
    return "".join(s)


def cup(cx, cy, w=56, handle="right", steam=True, steam_col="#fff", lw=1.0, band_color=SAFF):
    """Ceramic cup on a saucer; (cx, cy) is the middle of the rim; lw scales every stroke."""
    s = []
    sau = ell(cx, cy + 30, w * .9, 10.5)
    s.append(shaded(sau, "#fffaf0", "#ddd0bf", (-4, -3), OL, 3 * lw))
    s.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy + 29)}" rx="{fmt(w * .5)}" ry="5.5" fill="#d9cbb8" opacity=".7"/>')
    if handle:
        sx = 1 if handle == "right" else -1
        hx = cx + sx * w / 2
        hd = f"M{fmt(hx - sx * 3)} {fmt(cy + 2)}C{fmt(hx + sx * 20)} {fmt(cy - 4)} {fmt(hx + sx * 20)} {fmt(cy + 22)} {fmt(hx - sx * 8)} {fmt(cy + 21)}"
        s.append(f'<path d="{hd}" fill="none" stroke="{OL}" stroke-width="{fmt(5 + 5.5 * lw)}" stroke-linecap="round"/>')
        s.append(f'<path d="{hd}" fill="none" stroke="#fffaf0" stroke-width="5" stroke-linecap="round"/>')
    body = f"M{fmt(cx - w / 2)} {fmt(cy)}C{fmt(cx - w / 2)} {fmt(cy + 26)} {fmt(cx - w / 4)} {fmt(cy + 33)} {fmt(cx)} {fmt(cy + 33)}C{fmt(cx + w / 4)} {fmt(cy + 33)} {fmt(cx + w / 2)} {fmt(cy + 26)} {fmt(cx + w / 2)} {fmt(cy)}Z"
    band = f'<path d="M{fmt(cx - w / 2)} {fmt(cy + 11)}Q{fmt(cx)} {fmt(cy + 21)} {fmt(cx + w / 2)} {fmt(cy + 11)}" fill="none" stroke="{band_color}" stroke-width="5"/>'
    s.append(shaded(body, "#fffaf0", "#dccfbd", (-7, -3), OL, 3 * lw, extra_clip=band))
    s.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy)}" rx="{fmt(w / 2)}" ry="8" fill="#fffaf0" stroke="{OL}" stroke-width="{fmt(3 * lw)}"/>')
    s.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy + 1)}" rx="{fmt(w / 2 - 4.5)}" ry="5.4" fill="#6a3a1f"/>')
    s.append(f'<ellipse cx="{fmt(cx - 6)}" cy="{fmt(cy - 0.5)}" rx="{fmt(w / 4)}" ry="2" fill="#a56a3a" opacity=".8"/>')
    if steam:
        for k, dx in enumerate((-9, 2, 13)):
            x0, y0 = cx + dx, cy - 8
            s.append(f'<path d="M{fmt(x0)} {fmt(y0)}C{fmt(x0 - 9)} {fmt(y0 - 12)} {fmt(x0 + 9)} {fmt(y0 - 20)} {fmt(x0)} {fmt(y0 - 34 - k * 3)}" fill="none" stroke="#7a4f2e" stroke-width="7" stroke-linecap="round" opacity=".16"/>')
            s.append(f'<path d="M{fmt(x0)} {fmt(y0)}C{fmt(x0 - 9)} {fmt(y0 - 12)} {fmt(x0 + 9)} {fmt(y0 - 20)} {fmt(x0)} {fmt(y0 - 34 - k * 3)}" fill="none" stroke="{steam_col}" stroke-width="4" stroke-linecap="round" opacity=".92"/>')
    return "".join(s)
