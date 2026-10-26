"""Drawing helpers: smooth splines, cel shading, fur edges."""
import math
import random

_n = 0


def nid():
    global _n
    _n += 1
    return f"lg-{_n}"


def fmt(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def pt(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def _split(points):
    return [(p[0], p[1]) for p in points], [len(p) > 2 and p[2] == "c" for p in points]


def segments(points, closed=True, t=1.0):
    """Catmull-Rom through the points as cubic Beziers; a third item 'c' makes a sharp corner."""
    P, C = _split(points)
    n = len(P)

    def at(i):
        return P[i % n] if closed else P[min(max(i, 0), n - 1)]

    out = []
    for i in range(n if closed else n - 1):
        p0, p1, pm, p2 = at(i), at(i + 1), at(i - 1), at(i + 2)
        c1 = p0 if C[i % n] else (p0[0] + (p1[0] - pm[0]) * t / 6, p0[1] + (p1[1] - pm[1]) * t / 6)
        c2 = p1 if C[(i + 1) % n] else (p1[0] - (p2[0] - p0[0]) * t / 6, p1[1] - (p2[1] - p0[1]) * t / 6)
        out.append((p0, c1, c2, p1))
    return out


def D(points, closed=True, t=1.0):
    segs = segments(points, closed, t)
    d = "M" + pt(segs[0][0])
    for _, c1, c2, p in segs:
        d += "C" + pt(c1) + " " + pt(c2) + " " + pt(p)
    return d + ("Z" if closed else "")


def bez(p0, c1, c2, p1, t):
    u = 1 - t
    return (
        u**3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * p1[0],
        u**3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * p1[1],
    )


def polyline(points, closed=True, t=1.0, per=14):
    segs = segments(points, closed, t)
    out = []
    for p0, c1, c2, p1 in segs:
        for j in range(per):
            out.append(bez(p0, c1, c2, p1, j / per))
    if not closed:
        out.append(segs[-1][3])
    return out


def resample(poly, step, closed=True):
    pts = poly + ([poly[0]] if closed else [])
    out = [pts[0]]
    remain = step
    cur = pts[0]
    for b in pts[1:]:
        a = cur
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        while L >= remain and L > 0:
            f = remain / L
            a = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
            out.append(a)
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            remain = step
        remain -= L
        cur = b
    if closed and len(out) > 2 and math.hypot(out[-1][0] - out[0][0], out[-1][1] - out[0][1]) < step * 0.5:
        out.pop()
    return out


def mirror(points, ax=0.0):
    return [(2 * ax - p[0], p[1]) + tuple(p[2:]) for p in points]


def xf(points, dx=0.0, dy=0.0, s=1.0, rot=0.0, c=(0.0, 0.0)):
    """Scale about c, rotate about c, then translate."""
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for p in points:
        x, y = (p[0] - c[0]) * s, (p[1] - c[1]) * s
        out.append((c[0] + x * ca - y * sa + dx, c[1] + x * sa + y * ca + dy) + tuple(p[2:]))
    return out


def ell(cx, cy, rx, ry, rot=0.0):
    a = math.radians(rot)
    ux, uy = rx * math.cos(a), rx * math.sin(a)
    return (
        f"M{fmt(cx - ux)} {fmt(cy - uy)}A{fmt(rx)} {fmt(ry)} {fmt(rot)} 1 0 {fmt(cx + ux)} {fmt(cy + uy)}"
        f"A{fmt(rx)} {fmt(ry)} {fmt(rot)} 1 0 {fmt(cx - ux)} {fmt(cy - uy)}Z"
    )


def style(fill=None, stroke=None, sw=None, op=None, extra=""):
    s = ""
    if fill is not None:
        s += f' fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}"'
        if sw:
            s += f' stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'
    if op is not None:
        s += f' opacity="{op}"'
    return s + extra


def P(d, fill="none", stroke=None, sw=3, op=None, extra=""):
    return f'<path d="{d}"{style(fill, stroke, sw, op, extra)}/>'


def shaded(d, base, shade, off=(-6, -5), stroke="#2b1810", sw=3, extra_clip=""):
    """Flat form with a crescent of shade on the lower-right (light comes from the upper left)."""
    cid = nid()
    s = f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
    s += f'<path d="{d}" fill="{shade}"/>'
    s += f'<g clip-path="url(#{cid})"><path d="{d}" fill="{base}" transform="translate({fmt(off[0])} {fmt(off[1])})"/>{extra_clip}</g>'
    if stroke:
        s += f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'
    return s


def clipped(d, inner, ):
    cid = nid()
    return f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{inner}</g>'


def _area(poly):
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def fur(points, step=10.0, length=(6, 12), seed=0, closed=True, t=1.0, grav=0.0, kind="flame", skip=None, lean=0.25):
    """Outline of a closed shape with fur tufts pointing outwards; returns (path d, tips list)."""
    rnd = random.Random(seed)
    poly = resample(polyline(points, closed, t), step, closed)
    n = len(poly)
    sgn = 1 if _area(poly) > 0 else -1

    def normal(i):
        a, b = poly[(i - 1) % n], poly[(i + 1) % n]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1
        return (sgn * ty / L, -sgn * tx / L)

    d = "M" + pt(poly[0])
    tips = []
    for i in range(n if closed else n - 1):
        a, b = poly[i], poly[(i + 1) % n]
        if skip and skip(a, b):
            d += "L" + pt(b)
            continue
        na, nb = normal(i), normal((i + 1) % n)
        L = rnd.uniform(*length)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nm = ((na[0] + nb[0]) / 2, (na[1] + nb[1]) / 2)
        sh = rnd.uniform(-lean, lean)
        tip = (mx + nm[0] * L + (b[0] - a[0]) * sh, my + nm[1] * L + grav * L)
        tips.append((tip, (mx, my)))
        if kind == "cloud":
            c = (mx + nm[0] * L * 1.9, my + nm[1] * L * 1.9 + grav * L)
            d += "Q" + pt(c) + " " + pt(b)
        else:
            c1 = (a[0] + na[0] * L * 0.85, a[1] + na[1] * L * 0.85 + grav * L * 0.3)
            c2 = (b[0] + nb[0] * L * 0.2, b[1] + nb[1] * L * 0.2)
            d += "Q" + pt(c1) + " " + pt(tip) + "Q" + pt(c2) + " " + pt(b)
    return d + ("Z" if closed else ""), tips
