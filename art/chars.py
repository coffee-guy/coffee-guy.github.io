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


def woman(cx=205):
    back, front = [], []
    # ---- hair behind the body
    bh = [(205, 196), (240, 200), (268, 216), (284, 244), (290, 290), (290, 350), (286, 420), (284, 490), (284, 560), (205, 582),
          (126, 560), (126, 490), (124, 420), (120, 350), (120, 290), (128, 244), (144, 216), (172, 200)]
    back.append(shaded(D(bh), HAIR_W[0], HAIR_W[1], (-8, -6), OL, 3.5))

    # ---- neck + shoulders + chest (skin)
    bust = [(188, 326), (222, 326), (226, 362), (250, 380), (280, 392), (290, 414), (290, 450), (250, 452), (205, 458), (160, 452), (120, 450), (120, 414), (130, 392),
            (160, 380), (184, 362)]
    d = D(bust)
    chin_sh = f'<ellipse cx="206" cy="344" rx="40" ry="24" fill="{SKIN_W[1]}" opacity=".85"/>'
    back.append(shaded(d, SKIN_W[0], SKIN_W[1], (-6, -5), OL, 3.5, extra_clip=chin_sh))

    # ---- dress (bodice + skirt) with peony print
    dress = [(160, 438, "c"), (182, 431), (205, 447), (228, 431), (250, 438, "c"), (253, 472), (249, 506), (262, 542), (274, 584), (205, 596), (136, 584), (148, 542),
             (161, 506), (157, 472)]
    dd = D(dress, t=0.9)
    print_ = "".join([
        leaf(150, 520, 34, -30), leaf(262, 512, 30, 200), leaf(214, 562, 30, 80), leaf(150, 468, 26, 190),
        peony(178, 470, 27, 10), peony(238, 462, 21, 40), peony(206, 524, 31, 0), peony(158, 560, 21, 20), peony(254, 556, 25, 70), peony(224, 586, 18, 0),
    ])
    folds = "".join(
        f'<path d="M{x} {y}Q{x + 4} {y + 30} {x + dx} {y + 56}" stroke="#cfc3cb" stroke-width="2.2" fill="none" opacity=".7"/>' for x, y, dx in ((176, 512, -8), (232, 514, 10)))
    back.append(shaded(dd, "#fffaf2", "#d9d0d6", (-9, -4), OL, 3.5, extra_clip=print_ + folds))
    # straps
    for x0, x1 in ((166, 158), (244, 252)):
        back.append(f'<path d="M{x0} 436L{x1} 384" stroke="{OL}" stroke-width="10" stroke-linecap="round"/>')
        back.append(f'<path d="M{x0} 436L{x1} 384" stroke="#fffaf2" stroke-width="5.5" stroke-linecap="round"/>')

    # ---- head
    h = []
    face = [(0, -58), (30, -54), (50, -36), (56, -8), (55, 18), (49, 42), (36, 62), (18, 75), (0, 79), (-18, 75), (-36, 62), (-49, 42), (-55, 18), (-56, -8), (-50, -36), (-30, -54)]
    fd = D(face)
    fringe_sh = '<path d="M-60 -56H60V-14C40 -22 20 -26 0 -24C-20 -26 -40 -22 -60 -14Z" fill="#c98f72" opacity=".35"/>'
    cheeks = '<ellipse cx="-35" cy="41" rx="12" ry="6.5" fill="#f38c8c" opacity=".38"/><ellipse cx="35" cy="41" rx="12" ry="6.5" fill="#f38c8c" opacity=".38"/>'
    h.append(shaded(fd, SKIN_W[0], SKIN_W[1], (-5, -4), OL, 3.5, extra_clip=fringe_sh + cheeks))
    h.append(f'<g transform="translate(24 12)">{eye(False)}</g>')
    h.append(f'<g transform="translate(-24 12)">{eye(True)}</g>')
    h.append('<path d="M12 -22C20 -29 33 -29 42 -22M-12 -22C-20 -29 -33 -29 -42 -22" fill="none" stroke="#2a1b1c" stroke-width="3.4" stroke-linecap="round"/>')
    h.append('<path d="M-2.5 40Q0 43.5 3 40" fill="none" stroke="#c58a68" stroke-width="2" stroke-linecap="round"/>')
    h.append('<path d="M-11 55C-6 54 -2 52 0 53C2 52 6 54 11 55C6 64 -6 64 -11 55Z" fill="#c9505f" stroke="#8c2e3c" stroke-width="1.4" stroke-linejoin="round"/>')
    h.append('<path d="M-11 55C-4 58 4 58 11 55" fill="none" stroke="#8c2e3c" stroke-width="1.6" stroke-linecap="round"/>')
    h.append('<ellipse cx="-3" cy="60" rx="3.5" ry="1.4" fill="#ffd2d6" opacity=".7"/>')
    # front hair
    hr = [(3, -70, "c"), (32, -66), (58, -50), (74, -22), (80, 14), (84, 54), (94, 96), (92, 136), (86, 172), (96, 208, "c"), (80, 188), (72, 152), (66, 114), (60, 80), (56, 56),
          (54, 30), (52, 4), (46, -22), (32, -42), (14, -52), (3, -57, "c")]
    hl = [(-3, -70, "c"), (-32, -67), (-58, -51), (-75, -22), (-82, 14), (-82, 54), (-88, 98), (-96, 138), (-100, 176), (-92, 206, "c"), (-82, 186), (-74, 150), (-68, 112), (-60, 80),
          (-56, 56), (-54, 30), (-52, 4), (-46, -22), (-32, -42), (-14, -52), (-3, -57, "c")]
    for pts, sgn in ((hr, 1), (hl, -1)):
        dd_ = D(pts, t=0.9)
        sheen = (f'<path d="M{sgn * 24} -63C{sgn * 48} -58 {sgn * 66} -40 {sgn * 74} -12" fill="none" stroke="{HAIR_W[2]}" stroke-width="6" stroke-linecap="round" opacity=".75"/>'
                 f'<path d="M{sgn * 70} 60C{sgn * 76} 100 {sgn * 82} 140 {sgn * 84} 176" fill="none" stroke="{HAIR_W[2]}" stroke-width="4" stroke-linecap="round" opacity=".5"/>')
        lines = "".join(f'<path d="{p}" fill="none" stroke="#0e080a" stroke-width="1.8" stroke-linecap="round" opacity=".7"/>' for p in (
            f"M{sgn * 40} -50C{sgn * 62} -26 {sgn * 70} 30 {sgn * 80} 120",
            f"M{sgn * 28} -56C{sgn * 52} -38 {sgn * 62} 20 {sgn * 72} 100",
            f"M{sgn * 62} 60C{sgn * 68} 110 {sgn * 76} 160 {sgn * 88} 196"))
        h.append(shaded(dd_, HAIR_W[0], HAIR_W[1], (sgn * -6, -4), OL, 3.5, extra_clip=sheen + lines))
    h.append(f'<path d="M0 -70V-56" stroke="{OL}" stroke-width="2.5" stroke-linecap="round"/>')
    for p in ("M-6 -70C-14 -84 -4 -95 10 -92", "M8 -70C16 -86 32 -88 38 -80", "M-22 -68C-30 -78 -26 -90 -14 -92"):
        h.append(f'<path d="{p}" fill="none" stroke="{HAIR_W[0]}" stroke-width="2.4" stroke-linecap="round"/>')
    # earrings
    for sx in (-1, 1):
        h.append(f'<circle cx="{sx * 57}" cy="56" r="3.4" fill="#f4d58a" stroke="{OL}" stroke-width="1.4"/><circle cx="{sx * 57}" cy="66" r="4.4" fill="#fffaf0" stroke="{OL}" stroke-width="1.4"/>')
    back.append(f'<g transform="translate({cx} 280) rotate(5 0 100)">{"".join(h)}</g>')

    # ---- arms, cup and hands (drawn after the table)
    arm_l = [(123, 404), (121, 450), (121, 500), (124, 552), (130, 590), (146, 607), (170, 616), (190, 619), (192, 600), (168, 592), (156, 582), (152, 550), (150, 500), (152, 450),
             (150, 420), (146, 396)]
    for pts in (arm_l, mirror(arm_l, 205)):
        front.append(shaded(D(pts, t=0.9), SKIN_W[0], SKIN_W[1], (-6, -4), OL, 3.5))
    front.append(cup(205, 598, 60, None, True, "#fff"))
    front.append(hand(172, 614, 1))
    front.append(hand(238, 614, -1))
    return "".join(back), "".join(front)


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
