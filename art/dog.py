from chars import OL
from lib import *  # noqa: F401,F403

WHITE = ("#fffaf1", "#e9dfcf", "#d4c6b0")
TAN = ("#cf9456", "#a76a38", "#e8b87c", "#8d5529")
DOL = "#5b3a26"  # softer outline for fur
BOW = ("#e5534f", "#b63a3a")


def strands(tips, color, depth=1.0, w=1.5, op=0.55):
    out = []
    for tip, mid in tips:
        e = (mid[0] + (mid[0] - tip[0]) * depth * 0.9, mid[1] + (mid[1] - tip[1]) * depth * 0.9)
        out.append(f"M{pt(tip)}L{pt(e)}")
    return f'<path d="{"".join(out)}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'


def dog(cx=400, cy=452):
    back, front = [], []
    h = []

    # ---- ears (tan, long, feathered), behind the head
    ear_r = [(50, -54), (76, -50), (94, -26), (102, 12), (106, 54), (100, 94), (88, 118, "c"), (74, 100), (68, 66), (62, 30), (54, 0)]
    for pts in (ear_r, mirror(ear_r, 0)):
        d, tips = fur(pts, step=13, length=(5, 11), seed=3, grav=0.9, kind="flame", skip=lambda a, b: abs(a[0]) < 62 and a[1] < 10, lean=0.4)
        lines = strands(tips, TAN[3], 1.6, 1.8, 0.6)
        ear_hi = (f'<path d="M{pts[0][0] * 1.4:.0f} -40C{pts[3][0] * 1.0:.0f} -10 {pts[4][0] * .95:.0f} 40 {pts[5][0] * .8:.0f} 90" fill="none" stroke="{TAN[2]}" stroke-width="7" stroke-linecap="round" opacity=".55"/>'
                  if pts[0][0] > 0 else
                  f'<path d="M{pts[0][0] * 1.4:.0f} -40C{pts[3][0] * 1.0:.0f} -10 {pts[4][0] * .95:.0f} 40 {pts[5][0] * .8:.0f} 90" fill="none" stroke="{TAN[2]}" stroke-width="7" stroke-linecap="round" opacity=".55"/>')
        dark_tip = f'<path d="M-120 70H120V140H-120Z" fill="{TAN[3]}" opacity=".35"/>'
        h.append(shaded(d, TAN[0], TAN[1], (-6, -4), DOL, 3, extra_clip=ear_hi + lines + dark_tip))

    # ---- chest bib
    chest = [(-50, 40), (-62, 74), (-72, 112), (-68, 146), (-40, 162), (0, 166), (40, 162), (68, 146), (72, 112), (62, 74), (50, 40)]
    d, tips = fur(chest, step=13, length=(6, 12), seed=8, grav=0.8, kind="flame", skip=lambda a, b: a[1] < 52 or a[1] > 150, lean=0.4)
    h.append(shaded(d, WHITE[0], WHITE[1], (-7, -4), DOL, 3, extra_clip=strands(tips, WHITE[2], 1.7, 1.8, 0.7)))
    # collar
    h.append(f'<path d="M-50 56Q0 80 50 56L47 70Q0 96 -47 70Z" fill="#2f8f8b" stroke="{DOL}" stroke-width="3" stroke-linejoin="round"/>')
    h.append(f'<circle cx="2" cy="90" r="8" fill="#f4c64a" stroke="{DOL}" stroke-width="2.6"/><circle cx="0" cy="88" r="2.5" fill="#fff3c0"/>')

    # ---- head
    head = [(0, -64), (30, -62), (56, -48), (72, -22), (78, 8), (72, 36), (56, 58), (32, 72), (0, 78), (-32, 72), (-56, 58), (-72, 36), (-78, 8), (-72, -22), (-56, -48), (-30, -62)]
    d, tips = fur(head, step=11, length=(7, 15), seed=5, grav=1.0, kind="flame", lean=0.15)
    patch_r = [(80, -6), (70, -44), (44, -62), (16, -64), (8, -40), (14, -12), (12, 14), (30, 26), (54, 22), (74, 10)]
    patches = "".join(f'<path d="{D(p, t=0.9)}" fill="{TAN[0]}"/>' for p in (patch_r, mirror(patch_r, 0)))
    patch_hi = "".join(f'<path d="{D(p, t=0.9)}" fill="{TAN[2]}" opacity=".45" transform="translate(-8 -6) scale(.9)"/>' for p in (patch_r,))
    face_lines = strands(tips, "#a98b66", 1.9, 1.3, 0.3)
    cheeks = '<ellipse cx="-50" cy="38" rx="13" ry="7" fill="#f4a1a8" opacity=".4"/><ellipse cx="50" cy="38" rx="13" ry="7" fill="#f4a1a8" opacity=".4"/>'
    h.append(shaded(d, WHITE[0], WHITE[1], (-8, -5), DOL, 3.2, extra_clip=patches + patch_hi + face_lines + cheeks))
    # beard fluff round the muzzle
    beard = [(-42, 36), (-44, 56), (-32, 72), (-12, 80), (0, 82), (12, 80), (32, 72), (44, 56), (42, 36)]
    d, tips = fur(beard, step=11, length=(6, 12), seed=2, grav=0.9, kind="flame", closed=False, lean=0.2)
    h.append(f'<path d="{d}Z" fill="{WHITE[0]}"/>')
    h.append(f'<path d="{d}" fill="none" stroke="{DOL}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round"/>')
    # eyes
    for sx in (-1, 1):
        ex = sx * 29
        h.append(f'<ellipse cx="{ex}" cy="6" rx="11.5" ry="12.5" fill="#1f130c" stroke="{DOL}" stroke-width="2"/>')
        h.append(f'<ellipse cx="{ex}" cy="9" rx="8.5" ry="8.5" fill="#4a2a18" opacity=".6"/>')
        h.append(f'<circle cx="{ex - 3.2}" cy="0.5" r="4.2" fill="#fff"/><circle cx="{ex + 3.8}" cy="10.5" r="1.9" fill="#fff" opacity=".85"/>')
        h.append(f'<path d="M{ex - 13} -13Q{ex} -21 {ex + 13} -13" fill="none" stroke="{TAN[3]}" stroke-width="4" stroke-linecap="round" opacity=".8"/>')
    # nose and mouth
    h.append('<path d="M-12 32C-12 25 12 25 12 32C12 40 5 45 0 45C-5 45 -12 40 -12 32Z" fill="#1f1511" stroke="#0f0a08" stroke-width="2"/>')
    h.append('<ellipse cx="-4" cy="30" rx="4.5" ry="2.2" fill="#fff" opacity=".6"/>')
    h.append(f'<path d="M0 45V52M0 52C-4 60 -13 60 -17 53M0 52C4 60 13 60 17 53" fill="none" stroke="{OL}" stroke-width="2.6" stroke-linecap="round"/>')
    h.append('<path d="M-7 56C-8 70 8 70 7 56Z" fill="#f08a9a" stroke="#b9485c" stroke-width="2" stroke-linejoin="round"/><path d="M0 58V66" stroke="#b9485c" stroke-width="1.6" stroke-linecap="round"/>')
    # topknot with bow
    tk = [(-16, -58), (-28, -78), (-26, -98), (-10, -112), (8, -112), (24, -98), (26, -78), (14, -58)]
    d, tips = fur(tk, step=11, length=(5, 9), seed=11, grav=-0.2, kind="flame", skip=lambda a, b: a[1] > -66, lean=0.4)
    h.append(shaded(d, TAN[0], TAN[1], (-5, -4), DOL, 3, extra_clip=f'<path d="M-4 -112C-10 -90 -6 -72 -4 -60M8 -110C12 -90 10 -72 6 -60" stroke="{WHITE[0]}" stroke-width="5" fill="none" opacity=".85" stroke-linecap="round"/>' + strands(tips, TAN[3], 1.5, 1.6, 0.5)))
    loop = "M0 -66C-16 -88 -40 -82 -36 -66C-34 -54 -14 -54 0 -66Z"
    for sx in (1, -1):
        h.append(f'<g transform="scale({sx} 1)">{shaded(loop, BOW[0], BOW[1], (-4, -3), DOL, 2.8)}</g>')
    h.append(f'<circle cx="0" cy="-66" r="6.5" fill="{BOW[0]}" stroke="{DOL}" stroke-width="2.8"/>')
    back.append(f'<g transform="translate({cx} {cy}) rotate(4) scale(.94)">{"".join(h)}</g>')

    # ---- legs and paws on the table (after the table)
    for sx, jitter in ((-1, 0), (1, 3)):
        px = cx + sx * 34
        leg = [(px - 19, 534), (px + 19, 534), (px + 16, 566), (px + 14, 586), (px + 22, 602), (px + 14, 613), (px, 615), (px - 14, 613), (px - 22, 602), (px - 14, 586), (px - 16, 566)]
        d, tips = fur(leg, step=9, length=(3, 6), seed=20 + jitter, grav=0.8, kind="flame", skip=lambda a, b: a[1] < 590, lean=0.1)
        toes = "".join(f'<path d="M{px + k * 8} 603V612" stroke="{WHITE[2]}" stroke-width="2.2" stroke-linecap="round"/>' for k in (-1, 1))
        hair = f'<path d="M{px - 8} 540Q{px - 9} 566 {px - 9} 590M{px + 6} 540Q{px + 7} 566 {px + 8} 590" fill="none" stroke="{WHITE[2]}" stroke-width="1.8" stroke-linecap="round" opacity=".6"/>'
        front.append(shaded(d, WHITE[0], WHITE[1], (-5, -4), DOL, 3, extra_clip=toes + hair))
    return "".join(back), "".join(front)
