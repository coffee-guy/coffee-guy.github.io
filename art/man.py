from chars import cup, hand, OL
from lib import *  # noqa: F401,F403

SKIN_M = ("#e9b58b", "#c98b62")
HAIR_M = ("#2b1e1a", "#150d0b", "#6b5851")
DEN = ("#94a8be", "#6d8199", "#bccbdc")
STITCH = "#d6e0ea"


def stitched(d, w=1.8):
    return f'<path d="{d}" fill="none" stroke="{STITCH}" stroke-width="{w}" stroke-dasharray="5 4" stroke-linecap="round" opacity=".9"/>'


def man(cx=595):
    back, front = [], []
    m = 2 * cx  # mirror helper: x' = m - x

    def mir(points):
        return mirror(points, cx)

    # ---- neck
    neck = [(572, 326), (618, 326), (620, 372), (630, 400), (595, 410), (560, 400), (570, 372)]
    back.append(shaded(D(neck), SKIN_M[0], SKIN_M[1], (-6, -4), OL, 3.5,
                       extra_clip=f'<ellipse cx="{cx + 1}" cy="344" rx="40" ry="24" fill="{SKIN_M[1]}" opacity=".85"/>'))
    # ---- T-shirt
    tee = [(556, 390), (595, 412), (634, 390), (650, 412), (654, 470), (650, 574), (540, 574), (536, 470), (540, 412)]
    back.append(shaded(D(tee), "#2b2b33", "#17171d", (-5, -4), OL, 3.5))
    back.append(f'<path d="M566 394Q595 414 624 394" fill="none" stroke="#3d3d47" stroke-width="3" stroke-linecap="round"/>')
    # ---- denim jacket (two halves)
    jl = [(576, 372, "c"), (548, 380), (514, 394), (498, 416), (494, 470), (494, 574), (554, 580), (556, 520), (557, 470), (563, 434), (576, 406), (584, 384, "c")]
    for pts in (jl, mir(jl)):
        back.append(shaded(D(pts, t=0.8), DEN[0], DEN[1], (-7, -5), OL, 3.5))
    # pockets, seams
    for sgn in (1, -1):
        px = lambda x: cx + sgn * (cx - x)  # noqa: E731  (mirror helper for the left side coords)
        pocket = f"M{px(506)} 438H{px(546)}V472L{px(526)} 484L{px(506)} 472Z"
        back.append(shaded(pocket, DEN[2], DEN[0], (-3, -3), "#40566e", 2.4))
        back.append(f'<circle cx="{px(526)}" cy="454" r="3.4" fill="#cfd9e4" stroke="#40566e" stroke-width="1.5"/>')
        back.append(stitched(f"M{px(509)} 442H{px(543)}V468L{px(526)} 478L{px(509)} 468Z", 1.4))
        back.append(stitched(f"M{px(512)} 398Q{px(504)} 430 {px(500)} 470", 1.6))
        back.append(stitched(f"M{px(552)} 574Q{px(551)} 520 {px(553)} 470Q{px(556)} 436 {px(568)} 410", 1.6))
    # collars
    col = [(584, 368, "c"), (554, 378), (532, 404, "c"), (556, 416), (574, 406), (588, 388)]
    for pts in (col, mir(col)):
        back.append(shaded(D(pts, t=0.7), DEN[2], DEN[0], (-3, -3), OL, 3.2))
    back.append(stitched("M580 374Q560 384 542 402", 1.5))
    back.append(stitched(f"M{m - 580} 374Q{m - 560} 384 {m - 542} 402", 1.5))

    # ---- head (local coords, origin = head centre)
    h = []
    ears = "".join(
        f'<ellipse cx="{sx * 60}" cy="8" rx="9" ry="14" fill="{SKIN_M[0]}" stroke="{OL}" stroke-width="3"/>'
        f'<path d="M{sx * 59} 1Q{sx * 64} 8 {sx * 59} 16" fill="none" stroke="#b27652" stroke-width="2" stroke-linecap="round"/>' for sx in (-1, 1))
    h.append(ears)
    face = [(0, -58), (32, -55), (54, -38), (60, -8), (59, 20), (53, 46), (40, 66), (20, 80), (0, 84), (-20, 80), (-40, 66), (-53, 46), (-59, 20), (-60, -8), (-54, -38), (-32, -55)]
    fd = D(face)
    beard = D([(-62, 16), (-62, 92), (62, 92), (62, 16)], t=0.0)
    stub = (f'<path d="{beard}" fill="url(#lg-stub)"/>'
            '<path d="M-17 52Q-8 45 0 48Q8 45 17 52Q9 54 0 53Q-9 54 -17 52Z" fill="#3a251c" opacity=".55"/>'
            '<ellipse cx="-36" cy="42" rx="11" ry="6" fill="#e07a6a" opacity=".3"/><ellipse cx="36" cy="42" rx="11" ry="6" fill="#e07a6a" opacity=".3"/>')
    h.append(shaded(fd, SKIN_M[0], SKIN_M[1], (-5, -4), OL, 3.5, extra_clip=stub))
    h.append('<path d="M-3 28Q0 36 6 31" fill="none" stroke="#b27652" stroke-width="2.2" stroke-linecap="round"/>')
    h.append('<path d="M-14 62Q0 73 14 62" fill="none" stroke="#6b3526" stroke-width="2.8" stroke-linecap="round"/>')
    h.append('<path d="M-9 64Q0 71 9 64Q0 66 -9 64Z" fill="#fff6ee" opacity=".9"/>')
    # sunglasses
    lens_r = "M6 -3Q6 -10 14 -10H42Q50 -10 50 -3V9Q50 22 38 22H18Q6 22 6 9Z"
    lens_l = "M-6 -3Q-6 -10 -14 -10H-42Q-50 -10 -50 -3V9Q-50 22 -38 22H-18Q-6 22 -6 9Z"
    for d_, sg in ((lens_l, -1), (lens_r, 1)):
        cid = nid()
        h.append(f'<clipPath id="{cid}"><path d="{d_}"/></clipPath>')
        h.append(f'<path d="{d_}" fill="#17161c"/>')
        h.append(f'<g clip-path="url(#{cid})"><rect x="{-52 if sg < 0 else 4}" y="-12" width="50" height="36" fill="#34333f" opacity=".7"/>'
                 f'<path d="M{sg * 18} -12L{sg * 30} -12L{sg * 14} 24L{sg * 2} 24Z" fill="#fff" opacity=".22"/>'
                 f'<path d="M{sg * 34} -12L{sg * 38} -12L{sg * 22} 24L{sg * 18} 24Z" fill="#fff" opacity=".14"/></g>')
        h.append(f'<path d="{d_}" fill="none" stroke="#0d0c10" stroke-width="5" stroke-linejoin="round"/>')
    h.append('<path d="M-6 2Q0 -3 6 2" fill="none" stroke="#0d0c10" stroke-width="5" stroke-linecap="round"/>')
    h.append('<path d="M-50 0L-62 -2M50 0L62 -2" stroke="#0d0c10" stroke-width="4" stroke-linecap="round"/>')
    h.append('<path d="M-46 -17Q-28 -27 -8 -18M46 -17Q28 -27 8 -18" fill="none" stroke="#2a1a14" stroke-width="5.2" stroke-linecap="round"/>')
    # hair: big wavy quiff
    hair = [(-64, 26, "c"), (-72, 4), (-80, -26), (-78, -58), (-60, -88), (-30, -108), (6, -116), (42, -108), (68, -86), (80, -54), (78, -22), (72, 6), (66, 26, "c"),
            (60, 8), (57, -18), (46, -34), (26, -42), (6, -38), (-12, -44), (-32, -42), (-48, -30), (-57, -12), (-60, 8)]
    sheen = ('<path d="M-52 -80C-26 -104 16 -108 52 -88" fill="none" stroke="#6b5851" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
             '<path d="M-70 -44C-72 -20 -68 -4 -64 14" fill="none" stroke="#6b5851" stroke-width="4" stroke-linecap="round" opacity=".6"/>'
             '<path d="M68 -62C74 -40 72 -20 68 -6" fill="none" stroke="#6b5851" stroke-width="3.5" stroke-linecap="round" opacity=".5"/>')
    wav = "".join(f'<path d="{p}" fill="none" stroke="#0f0908" stroke-width="2" stroke-linecap="round" opacity=".7"/>' for p in (
        "M-40 -96C-30 -80 -34 -64 -44 -50", "M-8 -106C0 -90 -4 -72 -14 -58", "M26 -104C34 -88 30 -70 22 -56", "M52 -90C58 -76 56 -62 50 -50",
        "M-62 -30C-52 -22 -56 -10 -66 0", "M66 -30C58 -22 62 -10 70 0"))
    hair_d, _ = fur(hair, step=15, length=(3, 6.5), seed=4, kind="cloud", t=0.9, skip=lambda a, b: abs(a[0]) < 63 and a[1] > -50, lean=0.1)
    h.append(shaded(hair_d, HAIR_M[0], HAIR_M[1], (-6, -5), OL, 3.5, extra_clip=sheen + wav))
    # fringe locks over the forehead
    for lock in (
        [(-40, -44, "c"), (-20, -50), (4, -46), (20, -36, "c"), (-4, -30), (-26, -32)],
        [(6, -46, "c"), (26, -48), (48, -40), (56, -22, "c"), (40, -26), (22, -34)],
    ):
        h.append(shaded(D(lock, t=0.9), HAIR_M[0], HAIR_M[1], (-3, -3), OL, 3))
    # locks curling by the ears
    for sx in (-1, 1):
        lock = [(sx * 62, 8, "c"), (sx * 74, 18), (sx * 70, 34, "c"), (sx * 62, 26), (sx * 58, 14)]
        h.append(shaded(D(lock, t=0.9), HAIR_M[0], HAIR_M[1], (-3, -3), OL, 3))
    back.append(f'<g transform="translate({cx} 276) rotate(-5 0 100)">{"".join(h)}</g>')

    # ---- arms (after the table)
    sl_r = [(688, 396), (704, 418), (710, 470), (712, 530), (710, 586), (698, 612), (672, 626), (648, 630), (642, 606), (662, 596), (676, 584), (676, 530), (674, 470), (668, 424),
            (658, 400)]
    sl_l = [(502, 396), (486, 418), (480, 470), (478, 530), (478, 590), (480, 612), (514, 612), (514, 530), (514, 470), (508, 424), (500, 400)]
    back.append(shaded(D(sl_l, t=0.9), DEN[0], DEN[1], (-7, -5), OL, 3.5))
    back.append(stitched("M490 420Q486 500 488 570", 1.6))
    front.append(shaded(D(sl_r, t=0.9), DEN[0], DEN[1], (-7, -5), OL, 3.5))
    front.append(stitched("M700 420Q704 500 702 580", 1.6))
    # cuff
    front.append(shaded(D([(636, 604, "c"), (650, 636), (664, 632, "c"), (654, 598)], t=0.7), DEN[2], DEN[0], (-3, -3), OL, 3))
    # cup and hand
    front.append(cup(585, 598, 56, None, True, "#fff"))
    front.append(hand(624, 614, -1, SKIN_M))
    return "".join(back), "".join(front)
