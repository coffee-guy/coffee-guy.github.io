import lib
from chars import OL, SKIN_W, cup, hand
from lib import *  # noqa: F401,F403
from side import FACE_M, ear, face_skin, limb

SKIN_M = SKIN_W  # same skin tone as the woman
SKIN_LINE = "#c58a68"  # the woman's nose-line colour
HAIR_M = ("#2b1e1a", "#150d0b", "#6b5851")
DEN = ("#94a8be", "#6d8199", "#bccbdc")
STITCH = "#d6e0ea"
HEAD = (232, 286)  # drawn facing right like the woman, then mirrored across the middle of the picture
DX = -10  # body shifted away from the dog


def stitched(d, w=1.8):
    return f'<path d="{d}" fill="none" stroke="{STITCH}" stroke-width="{w}" stroke-dasharray="5 4" stroke-linecap="round" opacity=".9"/>'


def _head(parts, tilt=-2):
    return f'<g transform="translate({HEAD[0]} {HEAD[1]}) rotate({tilt} 0 100)">{"".join(parts)}</g>'


def _draw():
    back, front = [], []
    sk, sh = SKIN_M

    # hair behind the neck
    bh = [(182, 268), (174, 320), (180, 348), (198, 352), (212, 346), (212, 320), (204, 278)]
    back.append(shaded(D(bh, t=0.9), HAIR_M[0], HAIR_M[1], (-6, -5), OL, 3.5))

    # neck
    neck = [(212, 338), (264, 346), (262, 384), (270, 406), (240, 416), (204, 404), (206, 374)]
    back.append(shaded(D(neck), sk, sh, (-6, -4), OL, 3.5, extra_clip=f'<ellipse cx="238" cy="358" rx="36" ry="22" fill="{sh}" opacity=".85"/>'))
    # T-shirt, seen at the front of the open jacket
    tee = [(236, 392), (268, 396), (281, 424), (285, 470), (283, 530), (285, 586), (232, 586), (234, 500), (236, 440)]
    back.append(shaded(D(tee), "#2b2b33", "#17171d", (-5, -4), OL, 3.5))
    back.append('<path d="M244 398Q264 410 276 404" fill="none" stroke="#3d3d47" stroke-width="3" stroke-linecap="round"/>')
    # denim jacket body
    jk = [(196, 384, "c"), (242, 398, "c"), (252, 440), (256, 490), (256, 540), (258, 586), (146, 586), (144, 526), (148, 460), (162, 418), (180, 396)]
    back.append(shaded(D(jk, t=0.8), DEN[0], DEN[1], (-7, -5), OL, 3.5))
    back.append(stitched("M248 404Q256 450 254 580", 1.6))
    back.append(stitched("M160 430Q148 500 152 580", 1.6))
    pocket = "M222 446H248V478L235 488L222 478Z"
    back.append(shaded(pocket, DEN[2], DEN[0], (-3, -3), "#40566e", 2.4))
    back.append('<circle cx="235" cy="460" r="3.4" fill="#cfd9e4" stroke="#40566e" stroke-width="1.5"/>')
    # collar
    col = [(198, 380, "c"), (226, 372), (256, 396, "c"), (250, 432), (232, 418), (214, 402)]
    back.append(shaded(D(col, t=0.7), DEN[2], DEN[0], (-3, -3), OL, 3.2))
    back.append(stitched("M206 386Q232 382 250 398", 1.5))

    # head in profile
    h = []
    beard = D([(-40, 26), (-40, 92), (70, 92), (70, 26)], t=0.0)
    extra = (f'<path d="{beard}" fill="url(#lg-stub)"/>'
             '<path d="M40 31Q50 27 62 32V37Q50 36 40 36Z" fill="#3a251c" opacity=".35"/>'
             '<ellipse cx="22" cy="40" rx="11" ry="6" fill="#f38c8c" opacity=".34"/>')
    h.append(face_skin(SKIN_M, FACE_M, extra=extra))
    h.append(ear(SKIN_M, line=SKIN_LINE))
    h.append(f'<path d="M55 24Q59 27 56 30" fill="none" stroke="{SKIN_LINE}" stroke-width="2.2" stroke-linecap="round"/>')
    h.append('<path d="M55 43Q46 46 38 45" fill="none" stroke="#6b3526" stroke-width="2.6" stroke-linecap="round"/>')
    # sunglasses
    lens = "M19 -14H46Q53 -14 53 -7V6Q53 15 44 15H27Q19 15 19 6Z"
    cid = nid()
    h.append(f'<clipPath id="{cid}"><path d="{lens}"/></clipPath>')
    h.append(f'<path d="{lens}" fill="#17161c"/>')
    h.append(f'<g clip-path="url(#{cid})"><rect x="19" y="-15" width="35" height="31" fill="#34333f" opacity=".7"/>'
             '<path d="M30 -15L40 -15L28 16L18 16Z" fill="#fff" opacity=".22"/><path d="M43 -15L47 -15L37 16L33 16Z" fill="#fff" opacity=".14"/></g>')
    h.append(f'<path d="{lens}" fill="none" stroke="#0d0c10" stroke-width="5" stroke-linejoin="round"/>')
    h.append('<path d="M19 -6L-14 -8" stroke="#0d0c10" stroke-width="4" stroke-linecap="round"/>')
    h.append('<path d="M18 -23Q34 -31 50 -25" fill="none" stroke="#2a1a14" stroke-width="5" stroke-linecap="round"/>')
    # hair: medium length, loose and natural; the locks sit behind the main mass so only their tips show
    cap = [(54, -24, "c"), (58, -40), (54, -62), (40, -84), (18, -98), (-8, -102), (-36, -96), (-58, -82), (-72, -56), (-78, -22), (-76, 8), (-74, 30), (-70, 48),
            (-64, 62), (-56, 68, "c"), (-50, 60), (-44, 44), (-38, 24), (-30, 4), (-22, -16), (-10, -32), (8, -40), (28, -42), (44, -36), (50, -30)]
    sheen = ('<path d="M-46 -76C-20 -96 22 -96 48 -70" fill="none" stroke="#6b5851" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
             '<path d="M-68 -44C-72 -14 -70 22 -64 52" fill="none" stroke="#6b5851" stroke-width="4" stroke-linecap="round" opacity=".6"/>')
    flow = "".join(f'<path d="{p}" fill="none" stroke="#0f0908" stroke-width="2" stroke-linecap="round" opacity=".7"/>' for p in (
        "M10 -98C-14 -96 -44 -82 -62 -52", "M-20 -100C-48 -90 -68 -60 -72 -26", "M-54 -50C-66 -20 -66 20 -58 56", "M-40 -10C-46 20 -46 40 -42 56", "M24 -96C42 -84 54 -62 54 -42"))
    h.append(shaded(D(cap, t=0.9), HAIR_M[0], HAIR_M[1], (-6, -5), OL, 3.5, extra_clip=sheen + flow))
    back.append(_head(h))
    back = [f'<g transform="translate({DX} 0)">{"".join(back)}</g>']

    # drawn after the table: far arm, sleeve, cuff, cup, hands
    far_fore = [(266, 590), (284, 598), (304, 608), (304, 626), (280, 620), (266, 606)]
    front.append(shaded(D(far_fore, t=0.9), sk, sh, (-5, -4), OL, 3.5))
    sleeve = limb([(206 + DX, 408), (204 + DX, 470), (206 + DX / 2, 530), (220, 572), (234, 598)], [56, 52, 46, 40, 36])
    front.append(shaded(D(sleeve, t=0.9), DEN[0], DEN[1], (-7, -5), OL, 3.5))
    front.append(stitched(f"M{218 + DX} 420Q{214 + DX} 500 220 556", 1.6))
    front.append(shaded(D([(214, 590, "c"), (244, 600), (252, 618, "c"), (222, 614)], t=0.7), DEN[2], DEN[0], (-3, -3), OL, 3))
    front.append(cup(262, 598, 56, None, True, "#fff"))
    front.append(hand(230, 616, 1, SKIN_M))
    front.append(hand(296, 614, -1, SKIN_M))
    return back, front


def man():
    lib.MIRROR = True
    try:
        back, front = _draw()
    finally:
        lib.MIRROR = False
    flip = 'transform="translate(800 0) scale(-1 1)"'
    return f"<g {flip}>{''.join(back)}</g>", f"<g {flip}>{''.join(front)}</g>"
