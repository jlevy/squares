"""Lane L105's method B: exact clipped areas in `gmpy2.mpq`.

A square (x, y, c, s) is built as four corners in the order
p0 = C - u/2 - v/2, p1 = C + u/2 - v/2, p2 = C + u/2 + v/2, p3 = C - u/2 + v/2,
with u = (c, s), v = (-s, c), and accepted as a unit square when its four edges
have squared length 1, its four turns have one strict sign, and its shoelace area
is +-1 (a rhombus of side 1 and area 1 has a right angle).

- A pair: the first square clipped by the other's four closed inner half-planes
  (Sutherland-Hodgman, keeping points on the line). Empty: the closed squares are
  apart; non-empty with area 0: contact; positive area: their interiors meet.
- A wall: the square clipped by the wall's closed outer half-plane (x <= 0,
  y <= 0, x >= L, y >= L), read the same three ways, plus the least corner
  distance to the wall as an exact clearance. Containment: clipped to the box,
  the area stays 1.

Written for this review alone; it imports nothing from this repository or the
source, and shares nothing with method A but the integers the reader hands it.
"""

from __future__ import annotations

from gmpy2 import mpq

Rat = tuple[int, int]
Pt = tuple[mpq, mpq]
HALF = mpq(1, 2)


def q(r: Rat) -> mpq:
    return mpq(r[0], r[1])


def corners(sq: tuple[Rat, Rat, Rat, Rat]) -> list[Pt]:
    x, y, c, s = (q(t) for t in sq)
    ux, uy = c * HALF, s * HALF
    vx, vy = -s * HALF, c * HALF
    return [
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
    ]


def area2(poly: list[Pt]) -> mpq:
    """Twice the signed shoelace area."""
    tot = mpq(0)
    m = len(poly)
    for i in range(m):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % m]
        tot += x0 * y1 - x1 * y0
    return tot


def is_unit_square(p: list[Pt]) -> bool:
    if len(p) != 4:
        return False
    edges = [(p[(i + 1) % 4][0] - p[i][0], p[(i + 1) % 4][1] - p[i][1]) for i in range(4)]
    if any(ex * ex + ey * ey != 1 for ex, ey in edges):
        return False
    turns = [edges[i][0] * edges[(i + 1) % 4][1] - edges[i][1] * edges[(i + 1) % 4][0] for i in range(4)]
    if not (all(t > 0 for t in turns) or all(t < 0 for t in turns)):
        return False
    return abs(area2(p)) == 2


def ccw(p: list[Pt]) -> list[Pt]:
    return p if area2(p) > 0 else list(reversed(p))


def clip_halfplane(poly: list[Pt], a: mpq, b: mpq, c0: mpq) -> list[Pt]:
    """Keep the points with a*x + b*y + c0 >= 0 (closed half-plane)."""
    out: list[Pt] = []
    m = len(poly)
    if m == 0:
        return out
    vals = [a * px + b * py + c0 for px, py in poly]
    for i in range(m):
        p, vp = poly[i], vals[i]
        nq, vq = poly[(i + 1) % m], vals[(i + 1) % m]
        if vp >= 0:
            out.append(p)
        if (vp > 0 and vq < 0) or (vp < 0 and vq > 0):
            t = vp / (vp - vq)
            out.append((p[0] + t * (nq[0] - p[0]), p[1] + t * (nq[1] - p[1])))
    return out


def clip_by_square(poly: list[Pt], other_ccw: list[Pt]) -> list[Pt]:
    """Clip `poly` by the four closed inner half-planes of a CCW square."""
    out = poly
    for i in range(4):
        sx, sy = other_ccw[i]
        ex, ey = other_ccw[(i + 1) % 4]
        # inside: cross(e - s, p - s) >= 0  ->  a*x + b*y + c0 >= 0
        a = -(ey - sy)
        b = ex - sx
        c0 = (ey - sy) * sx - (ex - sx) * sy
        out = clip_halfplane(out, a, b, c0)
        if not out:
            return out
    return out


def pair_class(p_ccw: list[Pt], o_ccw: list[Pt]) -> tuple[str, mpq]:
    """('apart' | 'contact' | 'overlap', clipped area)."""
    inter = clip_by_square(p_ccw, o_ccw)
    if not inter:
        return "apart", mpq(0)
    ar = abs(area2(inter)) / 2
    return ("contact" if ar == 0 else "overlap"), ar


WALLS = ("left", "bottom", "right", "top")


def wall_facts(p: list[Pt], side: mpq) -> list[tuple[str, mpq, mpq]]:
    """Per wall: (class, exact clearance by least corner distance, outside area)."""
    out = []
    for w in WALLS:
        if w == "left":
            hp = (mpq(-1), mpq(0), mpq(0))
            clr = min(px for px, _ in p)
        elif w == "bottom":
            hp = (mpq(0), mpq(-1), mpq(0))
            clr = min(py for _, py in p)
        elif w == "right":
            hp = (mpq(1), mpq(0), -side)
            clr = side - max(px for px, _ in p)
        else:
            hp = (mpq(0), mpq(1), -side)
            clr = side - max(py for _, py in p)
        piece = clip_halfplane(p, *hp)
        if not piece:
            cls, ar = "inside", mpq(0)
        else:
            ar = abs(area2(piece)) / 2
            cls = "contact" if ar == 0 else "outside"
        out.append((cls, clr, ar))
    return out


def contained(p: list[Pt], side: mpq) -> bool:
    box = [(mpq(0), mpq(0)), (side, mpq(0)), (side, side), (mpq(0), side)]
    inter = clip_by_square(p, box)
    return bool(inter) and abs(area2(inter)) == 2
