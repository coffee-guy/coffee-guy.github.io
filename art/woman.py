from chars import OL, SKIN_W, HAIR_W, cup, eye, hand, leaf, peony
from lib import *  # noqa: F401,F403
from side import FACE_F, ear, face_skin, limb

HEAD = (232, 290)  # she sits on the left and looks right
DX = -10  # body shifted away from the dog


def _head(parts, tilt=2):
    return f'<g transform="translate({HEAD[0]} {HEAD[1]}) rotate({tilt} 0 100)">{"".join(parts)}</g>'


def woman():
    back, front = [], []
    sk, sh = SKIN_W
    hc, hs, hl = HAIR_W

    # long hair hanging behind her back
    bh = [(176, 236), (158, 292), (146, 362), (138, 442), (136, 522), (144, 570), (166, 586), (186, 568), (196, 522), (198, 470), (204, 420), (212, 372), (208, 322), (198, 262)]
    bh_lines = "".join(f'<path d="{p}" fill="none" stroke="#0e080a" stroke-width="1.8" stroke-linecap="round" opacity=".7"/>' for p in (
        "M164 300C156 380 152 470 156 570", "M178 270C170 360 168 450 172 560"))
    back.append(shaded(D(bh, t=0.9), hc, hs, (-8, -6), OL, 3.5, extra_clip=bh_lines))

    # neck, shoulders and chest in side view
    torso = [(214, 344), (258, 354), (252, 380), (260, 398), (273, 414), (281, 441), (275, 468), (265, 496), (261, 530), (263, 580), (168, 580), (165, 520), (166, 460), (176, 420),
             (194, 396), (206, 372)]
    chin_sh = f'<ellipse cx="240" cy="362" rx="32" ry="20" fill="{sh}" opacity=".85"/>'
    back.append(shaded(D(torso), sk, sh, (-6, -5), OL, 3.5, extra_clip=chin_sh))

    # dress with peony print
    dress = [(180, 418, "c"), (206, 426), (234, 434), (254, 430), (268, 422, "c"), (280, 442), (274, 468), (264, 496), (260, 530), (263, 584), (166, 584), (164, 520), (166, 470),
             (172, 438)]
    art = "".join([
        leaf(176, 520, 30, -20), leaf(268, 520, 24, 200), leaf(240, 566, 26, 80), leaf(176, 468, 22, 190),
        peony(262, 452, 19, 40), peony(256, 500, 23, 10), peony(182, 470, 19, 20), peony(178, 540, 22, 70), peony(236, 560, 25, 0), peony(270, 548, 16, 0),
    ])
    back.append(shaded(D(dress, t=0.9), "#fffaf2", "#d9d0d6", (-9, -4), OL, 3.5, extra_clip=art))

    # head in profile
    h = []
    cheek = '<ellipse cx="20" cy="32" rx="12" ry="6.5" fill="#f38c8c" opacity=".38"/>'
    h.append(face_skin(SKIN_W, FACE_F, extra=cheek + '<path d="M44 30Q50 27 64 31V47Q52 49 44 42Z" fill="#c9505f"/>'))
    h.append(ear(SKIN_W))
    h.append(f'<g transform="translate(29 -3) scale(.62 .95)">{eye(True)}</g>')
    h.append('<path d="M14 -21Q28 -31 43 -25" fill="none" stroke="#2a1b1c" stroke-width="3.2" stroke-linecap="round"/>')
    h.append('<path d="M50 17Q55 21 52 25" fill="none" stroke="#c58a68" stroke-width="2" stroke-linecap="round"/>')
    h.append('<path d="M52 38Q44 41 37 40" fill="none" stroke="#8c2e3c" stroke-width="1.6" stroke-linecap="round"/>')
    cap = [(52, -26, "c"), (52, -42), (46, -64), (28, -82), (4, -90), (-24, -88), (-48, -72), (-62, -44), (-66, -10), (-64, 26), (-58, 56),
           (-40, 44), (-30, 22), (-22, -4), (-14, -26), (2, -34), (20, -40), (36, -36), (46, -30)]
    sheen = (f'<path d="M-40 -70C-16 -86 24 -84 48 -64" fill="none" stroke="{hl}" stroke-width="6" stroke-linecap="round" opacity=".75"/>'
             f'<path d="M-58 -30C-60 0 -56 30 -52 50" fill="none" stroke="{hl}" stroke-width="4" stroke-linecap="round" opacity=".5"/>')
    lines = "".join(f'<path d="{p}" fill="none" stroke="#0e080a" stroke-width="1.8" stroke-linecap="round" opacity=".7"/>' for p in (
        "M-30 -80C-6 -88 30 -76 52 -48", "M-52 -56C-60 -20 -58 20 -52 50", "M0 -88C20 -74 36 -56 44 -40"))
    h.append(shaded(D(cap, t=0.9), hc, hs, (-6, -4), OL, 3.5, extra_clip=sheen + lines))
    for p in ("M-4 -88C-10 -100 0 -108 14 -104", "M16 -86C24 -100 38 -100 44 -92"):
        h.append(f'<path d="{p}" fill="none" stroke="{hc}" stroke-width="2.4" stroke-linecap="round"/>')
    h.append(f'<circle cx="-10" cy="29" r="3.4" fill="#f4d58a" stroke="{OL}" stroke-width="1.4"/><circle cx="-10" cy="39" r="4.4" fill="#fffaf0" stroke="{OL}" stroke-width="1.4"/>')
    back.append(_head(h))
    back = [f'<g transform="translate({DX} 0)">{"".join(back)}</g>']

    # drawn after the table: arms, strap, cup, hands
    far_fore = [(266, 590), (284, 598), (304, 608), (304, 626), (280, 620), (266, 606)]
    front.append(shaded(D(far_fore, t=0.9), sk, sh, (-5, -4), OL, 3.5))
    arm = limb([(212 + DX, 404), (212 + DX, 468), (214 + DX / 2, 526), (222, 566), (230, 600)], [38, 36, 33, 27, 22])
    front.append(shaded(D(arm, t=0.9), sk, sh, (-6, -4), OL, 3.5))
    strap = "M256 431Q238 388 214 386Q192 388 184 418"
    front.append(f'<g transform="translate({DX} 0)"><path d="{strap}" fill="none" stroke="{OL}" stroke-width="10" stroke-linecap="round"/>'
                 f'<path d="{strap}" fill="none" stroke="#fffaf2" stroke-width="5.5" stroke-linecap="round"/></g>')
    front.append(cup(262, 598, 56, None, True, "#fff"))
    front.append(hand(230, 614, 1))
    front.append(hand(296, 614, -1))
    return "".join(back), "".join(front)
