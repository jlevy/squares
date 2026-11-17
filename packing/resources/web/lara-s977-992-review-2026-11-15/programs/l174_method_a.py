"""Lane L174 method A: separating axes in Z[sqrt 2] with Python integers.

Every square is turned 0 or 45 degrees, so the edge normals of every square, and of
every pair, lie among four directions: e1 = (1, 0), e2 = (0, 1), e3 = (1, 1),
e4 = (1, -1).  For each square and direction the projection is an interval
``[p - h, p + h]``: ``p`` the centre's projection, ``h`` the half-width

* upright square of side s:  h = s/2 on e1, e2 and h = s on e3, e4;
* 45-degree square of side s: h = s/sqrt 2 = (s/2) sqrt 2 on all four.

All values are scaled by one common integer D so that every coordinate is
``a + b sqrt 2`` with integers a, b.  The sign of ``a + b sqrt 2`` is decided exactly
by comparing ``a^2`` with ``2 b^2`` when a and b differ in sign.

A pair's class is the largest sign over the four directions of
``max(lo_j - hi_i, lo_i - hi_j)``: +1 apart (strictly separated), 0 touching (weakly
separated, closed squares meet), -1 overlapping (no direction separates; the four
directions contain both squares' edge normals, so by the separating axis theorem their
interiors meet).  Walls: the clearances ``lo_e1``, ``lo_e2``, ``W - hi_e1``,
``W - hi_e2``.  A square is a unit square when its side field is exactly 1.

No pair is skipped: every one of the n(n-1)/2 pairs is decided.
"""

from __future__ import annotations

import hashlib
import math
from fractions import Fraction

from l174_reader import Construction

Z2 = tuple[int, int]


def zsign(a: int, b: int) -> int:
    """Exact sign of a + b sqrt 2 for integers a, b."""
    if a >= 0 and b >= 0:
        return 1 if (a or b) else 0
    if a <= 0 and b <= 0:
        return -1
    if a > 0:  # b < 0
        d = a * a - 2 * b * b
    else:  # a < 0 < b
        d = 2 * b * b - a * a
    return (d > 0) - (d < 0)  # d == 0 is impossible for (a, b) != (0, 0)


def _lcm_denominators(values: list[Fraction]) -> int:
    d = 1
    for v in values:
        d = math.lcm(d, v.denominator)
    return d


class Prepared:
    """Integer intervals of every square on the four directions, scaled by D."""

    def __init__(self, con: Construction) -> None:
        raw: list[Fraction] = [con.container[0], con.container[1]]
        for s in con.squares:
            raw.extend((s.cx[0], s.cx[1], s.cy[0], s.cy[1], s.size / 2))
        scale = _lcm_denominators(raw)
        self.scale = scale

        def z(p: tuple[Fraction, Fraction]) -> Z2:
            a, b = p[0] * scale, p[1] * scale
            assert a.denominator == 1 and b.denominator == 1
            return (int(a), int(b))

        self.width = z(con.container)
        # lo[k][i], hi[k][i] as integer pairs
        self.lo: list[list[Z2]] = [[] for _ in range(4)]
        self.hi: list[list[Z2]] = [[] for _ in range(4)]
        for s in con.squares:
            cx, cy = z(s.cx), z(s.cy)
            proj = (cx, cy, (cx[0] + cy[0], cx[1] + cy[1]), (cx[0] - cy[0], cx[1] - cy[1]))
            if s.angle == 0:
                h_half = z((s.size / 2, Fraction(0)))
                h_full = z((s.size, Fraction(0)))
                halves = (h_half, h_half, h_full, h_full)
            else:
                h = z((Fraction(0), s.size / 2))
                halves = (h, h, h, h)
            for k in range(4):
                p, h = proj[k], halves[k]
                self.lo[k].append((p[0] - h[0], p[1] - h[1]))
                self.hi[k].append((p[0] + h[0], p[1] + h[1]))
        self.unit = [s.size == 1 for s in con.squares]


def pair_class(prep: Prepared, i: int, j: int) -> int:
    best = -1
    for k in range(4):
        lo, hi = prep.lo[k], prep.hi[k]
        a = lo[j]
        b = hi[i]
        s1 = zsign(a[0] - b[0], a[1] - b[1])
        if s1 > 0:
            return 1
        a = lo[i]
        b = hi[j]
        s2 = zsign(a[0] - b[0], a[1] - b[1])
        if s2 > 0:
            return 1
        best = max(best, s1, s2)
    return best


def wall_classes(prep: Prepared, i: int) -> tuple[int, int, int, int]:
    """Signs of the clearances to the left, bottom, right and top walls."""
    w = prep.width
    lx, ly = prep.lo[0][i], prep.lo[1][i]
    hx, hy = prep.hi[0][i], prep.hi[1][i]
    return (
        zsign(*lx),
        zsign(*ly),
        zsign(w[0] - hx[0], w[1] - hx[1]),
        zsign(w[0] - hy[0], w[1] - hy[1]),
    )


def decide(con: Construction) -> dict[str, object]:
    prep = Prepared(con)
    n = len(con.squares)
    digest = hashlib.sha256()
    counts = {1: 0, 0: 0, -1: 0}
    touching: list[tuple[int, int]] = []
    overlapping: list[tuple[int, int]] = []
    for i in range(n):
        row = bytearray()
        for j in range(i + 1, n):
            c = pair_class(prep, i, j)
            counts[c] += 1
            row.append(c + 1)
            if c == 0:
                touching.append((i, j))
            elif c < 0:
                overlapping.append((i, j))
        digest.update(bytes(row))
    walls = [wall_classes(prep, i) for i in range(n)]
    wall_digest = hashlib.sha256(bytes(c + 1 for w in walls for c in w)).hexdigest()
    return {
        "method": "A: separating axes on e1..e4 in Z[sqrt 2], exact integer signs",
        "scale": prep.scale,
        "n": n,
        "pairs": n * (n - 1) // 2,
        "apart": counts[1],
        "touching": counts[0],
        "overlapping": counts[-1],
        "touching_pairs": touching,
        "overlapping_pairs": overlapping,
        "pair_class_sha256": digest.hexdigest(),
        "walls": walls,
        "wall_class_sha256": wall_digest,
        "unit": prep.unit,
    }
