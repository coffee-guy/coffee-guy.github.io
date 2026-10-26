"""Side-view helpers: right-facing profile heads and tube-shaped limbs.

Head coordinates: origin = head centre, x points forward (the way the face looks)."""
from chars import OL
from lib import *  # noqa: F401,F403

# skin silhouettes, clockwise from the forehead; the nose tip and the point under it are sharp corners
FACE_F = [(14, -60), (36, -51), (47, -35), (49, -21), (46, -10), (49, 1), (55, 12), (61, 20, "c"), (51, 25, "c"), (52, 30), (56, 35), (51, 39), (53, 44), (48, 50),
          (50, 58), (45, 68), (34, 74), (14, 73), (2, 64), (-8, 44), (-22, 18), (-38, -14), (-34, -44), (-14, -58)]
FACE_M = [(14, -62), (36, -52), (48, -36), (51, -22), (47, -11), (50, 0), (58, 12), (63, 21, "c"), (53, 27, "c"), (54, 32), (57, 37), (53, 41), (55, 46), (50, 52),
          (53, 61), (50, 72), (38, 80), (16, 80), (-4, 70), (-16, 48), (-28, 20), (-40, -12), (-36, -44), (-16, -58)]


def face_skin(skin, pts, extra=""):
    return shaded(D(pts, t=0.95), skin[0], skin[1], (-5, -4), OL, 3.5, extra_clip=extra)


def ear(skin, x=-10, y=12, line="#c58a68"):
    s = f'<ellipse cx="{x}" cy="{y}" rx="8" ry="13" fill="{skin[0]}" stroke="{OL}" stroke-width="3"/>'
    s += f'<path d="M{x - 2} {y - 6}Q{x + 4} {y} {x - 2} {y + 7}" fill="none" stroke="{line}" stroke-width="2" stroke-linecap="round"/>'
    return s


def limb(path, widths, cap=True):
    """Outline points of a tube along a centre-line; the far end is cut square (hidden by a hand), the near end can be rounded."""
    pts = polyline(path, closed=False, per=5)
    n, m = len(pts), len(path)

    def width(i):
        f = i / (n - 1) * (m - 1)
        k = min(int(f), m - 2)
        return widths[k] + (widths[k + 1] - widths[k]) * (f - k)

    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny, w = -dy / L, dx / L, width(i) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    out = left + right[::-1]
    out = [(p[0], p[1], "c") if k in (len(left) - 1, len(left)) else p for k, p in enumerate(out)]
    if cap:
        x0, y0 = pts[0]
        dx, dy = pts[1][0] - x0, pts[1][1] - y0
        L = math.hypot(dx, dy) or 1
        out.append((x0 - dx / L * widths[0] * 0.5, y0 - dy / L * widths[0] * 0.5))
    return out
