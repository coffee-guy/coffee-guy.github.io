from chars import cup, hand, OL, SKIN_W
from lib import *  # noqa: F401,F403

SKIN_M = SKIN_W  # same skin tone as the woman
SKIN_LINE = "#c58a68"  # the woman's nose-line colour
HAIR_M = ("#2b1e1a", "#150d0b", "#6b5851")
DEN = ("#94a8be", "#6d8199", "#bccbdc")
STITCH = "#d6e0ea"


def stitched(d, w=1.8):
    return f'<path d="{d}" fill="none" stroke="{STITCH}" stroke-width="{w}" stroke-dasharray="5 4" stroke-linecap="round" opacity=".9"/>'


def blade(ra, rb, tip, bend=8):
    """Pointed lock tapering from the hidden base ra-rb to the tip; both edges bow the same way."""
    def ctrl(a):
        dx, dy = tip[0] - a[0], tip[1] - a[1]
        L = math.hypot(dx, dy) or 1
        return ((a[0] + tip[0]) / 2 - dy / L * bend, (a[1] + tip[1]) / 2 + dx / L * bend)
    return f"M{pt(ra)}Q{pt(ctrl(ra))} {pt(tip)}Q{pt(ctrl(rb))} {pt(rb)}Z"


def man(cx=595):
    back, front = [], []
    m = 2 * cx  # mirror helper: x' = m - x
    head_t = f"translate({cx} 276) rotate(-5 0 100)"

    def mir(points):
        return mirror(points, cx)

    # ---- hair hanging behind the neck
    bh = [(-60, 8, "c"), (-68, 30), (-65, 54), (-52, 70, "c"), (-30, 62), (0, 66), (30, 62), (52, 70, "c"), (65, 54), (68, 30), (60, 8, "c")]
    back_strands = "".join(f'<path d="{p}" fill="none" stroke="#0f0908" stroke-width="2" stroke-linecap="round" opacity=".7"/>' for p in (
        "M-62 34C-63 46 -60 58 -54 66", "M62 34C63 46 60 58 54 66"))
    back.append(f'<g transform="{head_t}">{shaded(D(bh, t=0.9), HAIR_M[0], HAIR_M[1], (-6, -5), OL, 3.5, extra_clip=back_strands)}</g>')

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
        f'<path d="M{sx * 59} 1Q{sx * 64} 8 {sx * 59} 16" fill="none" stroke="{SKIN_LINE}" stroke-width="2" stroke-linecap="round"/>' for sx in (-1, 1))
    h.append(ears)
    face = [(0, -58), (32, -55), (54, -38), (60, -8), (59, 20), (53, 46), (40, 66), (20, 80), (0, 84), (-20, 80), (-40, 66), (-53, 46), (-59, 20), (-60, -8), (-54, -38), (-32, -55)]
    fd = D(face)
    beard = D([(-62, 16), (-62, 92), (62, 92), (62, 16)], t=0.0)
    stub = (f'<path d="{beard}" fill="url(#lg-stub)"/>'
            '<path d="M-17 52Q-8 45 0 48Q8 45 17 52Q9 54 0 53Q-9 54 -17 52Z" fill="#3a251c" opacity=".35"/>'
            '<ellipse cx="-36" cy="42" rx="11" ry="6" fill="#f38c8c" opacity=".34"/><ellipse cx="36" cy="42" rx="11" ry="6" fill="#f38c8c" opacity=".34"/>')
    h.append(shaded(fd, SKIN_M[0], SKIN_M[1], (-5, -4), OL, 3.5, extra_clip=stub))
    h.append(f'<path d="M-3 28Q0 36 6 31" fill="none" stroke="{SKIN_LINE}" stroke-width="2.2" stroke-linecap="round"/>')
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
    # hair: medium length, loose and layered, falling over the ears; the locks sit behind the crown so only their tips show
    outer = [(-58, 36, "c"), (-68, 14), (-74, -14), (-74, -46), (-63, -74), (-40, -96), (-8, -107), (22, -106), (50, -95), (67, -72), (75, -44), (76, -14), (72, 14), (63, 40, "c")]
    inner = [(52, 30), (55, 8), (56, -14), (52, -28), (42, -36), (26, -44), (8, -52), (-14, -58, "c"), (-30, -48), (-44, -38), (-54, -22), (-57, -2), (-55, 22), (-51, 30)]
    sheen = ('<path d="M-50 -78C-26 -100 16 -104 50 -86" fill="none" stroke="#6b5851" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
             '<path d="M-67 -44C-71 -22 -69 8 -62 32" fill="none" stroke="#6b5851" stroke-width="4" stroke-linecap="round" opacity=".6"/>'
             '<path d="M68 -50C72 -30 71 0 64 30" fill="none" stroke="#6b5851" stroke-width="3.5" stroke-linecap="round" opacity=".5"/>')
    flow = "".join(f'<path d="{p}" fill="none" stroke="#0f0908" stroke-width="2" stroke-linecap="round" opacity=".7"/>' for p in (
        "M-10 -104C14 -100 38 -88 50 -62", "M4 -106C34 -100 60 -82 68 -50", "M-16 -102C-32 -96 -50 -80 -60 -52",
        "M-66 -12C-68 8 -64 22 -57 34", "M66 -10C68 10 64 24 58 36"))
    locks = (
        ((62, -20), (76, 4), (73, 54), 3),
        ((-62, -20), (-76, 4), (-71, 48), -3),
        ((-34, -64), (-8, -58), (6, -32), -6),
        ((-16, -66), (16, -60), (54, -32), -8),
        ((-56, -52), (-34, -48), (-42, -30), 5),
    )
    for ra, rb, tip, bend in locks:
        h.append(shaded(blade(ra, rb, tip, bend), HAIR_M[0], HAIR_M[1], (-3, -3), OL, 3))
    h.append(shaded(D(outer + inner, t=0.9), HAIR_M[0], HAIR_M[1], (-6, -5), OL, 3.5, extra_clip=sheen + flow))
    back.append(f'<g transform="{head_t}">{"".join(h)}</g>')

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
