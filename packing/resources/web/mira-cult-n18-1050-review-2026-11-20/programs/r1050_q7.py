"""Exact arithmetic in Q(sqrt 7) and the unit-square geometry the r1050 checkers share.

Lane r1050's own code: it imports nothing from the source under review or from this
repository. A number a + b*sqrt(7) is held as two Fractions; its sign is decided by
comparing a*a with 7*b*b, so no comparison is ever approximate.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

SEVEN = 7


class Q7:
    """a + b*sqrt(7) with rational a, b."""

    __slots__ = ("a", "b")

    def __init__(self, a: Any = 0, b: Any = 0) -> None:
        self.a = Fraction(a)
        self.b = Fraction(b)

    @staticmethod
    def of(x: Any) -> Q7:
        return x if isinstance(x, Q7) else Q7(x, 0)

    def __add__(self, o: Any) -> Q7:
        o = Q7.of(o)
        return Q7(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self) -> Q7:
        return Q7(-self.a, -self.b)

    def __sub__(self, o: Any) -> Q7:
        o = Q7.of(o)
        return Q7(self.a - o.a, self.b - o.b)

    def __rsub__(self, o: Any) -> Q7:
        return Q7.of(o) - self

    def __mul__(self, o: Any) -> Q7:
        o = Q7.of(o)
        return Q7(self.a * o.a + SEVEN * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def scale(self, q: Fraction) -> Q7:
        return Q7(self.a * q, self.b * q)

    def sign(self) -> int:
        a, b = self.a, self.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        # Opposite signs: compare squares.
        d = a * a - SEVEN * b * b
        if a > 0:  # b < 0
            return 1 if d > 0 else (-1 if d < 0 else 0)
        return -1 if d > 0 else (1 if d < 0 else 0)  # a < 0 < b

    def __abs__(self) -> Q7:
        return -self if self.sign() < 0 else self

    def cmp(self, o: Any) -> int:
        return (self - Q7.of(o)).sign()

    def __lt__(self, o: Any) -> bool:
        return self.cmp(o) < 0

    def __le__(self, o: Any) -> bool:
        return self.cmp(o) <= 0

    def __gt__(self, o: Any) -> bool:
        return self.cmp(o) > 0

    def __ge__(self, o: Any) -> bool:
        return self.cmp(o) >= 0

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, (Q7, int, Fraction)):
            return NotImplemented
        return self.cmp(o) == 0

    def __hash__(self) -> int:
        return hash((self.a, self.b))

    def __float__(self) -> float:
        # Display only; never used in a decision.
        return float(self.a) + float(self.b) * 7**0.5

    def text(self) -> str:
        return f"{self.a} + ({self.b})*sqrt(7)"


def qmax(*xs: Q7) -> Q7:
    best = xs[0]
    for x in xs[1:]:
        if x > best:
            best = x
    return best


def qmin(*xs: Q7) -> Q7:
    best = xs[0]
    for x in xs[1:]:
        if x < best:
            best = x
    return best


Vec = tuple[Q7, Q7]


def dot(p: Vec, q: Vec) -> Q7:
    return p[0] * q[0] + p[1] * q[1]


def sub(p: Vec, q: Vec) -> Vec:
    return (p[0] - q[0], p[1] - q[1])


HALF = Fraction(1, 2)

# The source's tilted frame: u = ((1+sqrt7)/4, (sqrt7-1)/4), v = J u (quarter turn).
U_TILT: Vec = (Q7(Fraction(1, 4), Fraction(1, 4)), Q7(Fraction(-1, 4), Fraction(1, 4)))
V_TILT: Vec = (-U_TILT[1], U_TILT[0])
U_AXIS: Vec = (Q7(1), Q7(0))
V_AXIS: Vec = (Q7(0), Q7(1))


class Tile:
    """A closed unit square: centre c, orthonormal axes u, v (exact)."""

    __slots__ = ("c", "tid", "u", "v")

    def __init__(self, tid: int, c: Vec, u: Vec, v: Vec) -> None:
        self.tid = tid
        self.c = c
        self.u = u
        self.v = v

    def radius(self, n: Vec) -> Q7:
        """Half-length of the projection of the tile on direction n (unit or not)."""
        return (abs(dot(n, self.u)) + abs(dot(n, self.v))).scale(HALF)

    def norm(self, x: Vec) -> Q7:
        """The tile's rotated maximum norm of x - c."""
        d = sub(x, self.c)
        return qmax(abs(dot(d, self.u)), abs(dot(d, self.v)))

    def moved(self, dx: Q7, dy: Q7) -> Tile:
        return Tile(self.tid, (self.c[0] + dx, self.c[1] + dy), self.u, self.v)


def frame_ok(u: Vec, v: Vec) -> bool:
    return dot(u, u) == 1 and dot(v, v) == 1 and dot(u, v) == 0


def pair_slack(a: Tile, b: Tile) -> Q7:
    """max over the four edge normals of |d.n| - (r_a(n) + r_b(n)).

    By the separating-axis theorem for convex polygons, the interiors are disjoint iff
    this is >= 0 (every normal here is a unit vector, so the slack is a distance).
    """
    d = sub(b.c, a.c)
    best: Q7 | None = None
    for n in (a.u, a.v, b.u, b.v):
        s = abs(dot(d, n)) - a.radius(n) - b.radius(n)
        if best is None or s > best:
            best = s
    assert best is not None
    return best


def wall_slacks(t: Tile, side: Q7) -> list[Q7]:
    """The four wall slacks (left, right, bottom, top); each must be >= 0."""
    rx = t.radius((Q7(1), Q7(0)))
    ry = t.radius((Q7(0), Q7(1)))
    return [t.c[0] - rx, side - t.c[0] - rx, t.c[1] - ry, side - t.c[1] - ry]


def strict_q(s: str) -> Fraction:
    if not isinstance(s, str) or "." in s or "e" in s.lower():
        raise ValueError(f"not an exact rational string: {s!r}")
    return Fraction(s)


def load_construction(path: Path) -> tuple[Q7, list[Tile]]:
    """Strict reader for six-tilt18.json."""
    raw = json.loads(path.read_text())
    if set(raw) != {"field", "side", "centers"} or raw["field"] != "sqrt(7)":
        raise ValueError("unexpected construction keys or field")
    side = Q7(strict_q(raw["side"][0]), strict_q(raw["side"][1]))
    tiles: list[Tile] = []
    seen: set[int] = set()
    for row in raw["centers"]:
        tid, bit, cx, cy = row
        if not isinstance(tid, int) or tid in seen or bit not in (0, 1):
            raise ValueError(f"bad row {row!r}")
        seen.add(tid)
        c = (Q7(strict_q(cx[0]), strict_q(cx[1])), Q7(strict_q(cy[0]), strict_q(cy[1])))
        u, v = (U_TILT, V_TILT) if bit == 1 else (U_AXIS, V_AXIS)
        tiles.append(Tile(tid, c, u, v))
    return side, tiles


def check_packing(side: Q7, tiles: list[Tile]) -> dict[str, Any]:
    """Every wall and every pair, exactly. Returns counts, failures and contacts."""
    wall_fail: list[list[int]] = []
    wall_touch: list[list[int]] = []
    min_wall: Q7 | None = None
    for t in tiles:
        for k, s in enumerate(wall_slacks(t, side)):
            if s < 0:
                wall_fail.append([t.tid, k])
            elif s == 0:
                wall_touch.append([t.tid, k])
            if min_wall is None or s < min_wall:
                min_wall = s
    pair_fail: list[list[int]] = []
    pair_touch: list[list[int]] = []
    min_pair: Q7 | None = None
    npairs = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            npairs += 1
            s = pair_slack(tiles[i], tiles[j])
            if s < 0:
                pair_fail.append([tiles[i].tid, tiles[j].tid])
            elif s == 0:
                pair_touch.append([tiles[i].tid, tiles[j].tid])
            if min_pair is None or s < min_pair:
                min_pair = s
    assert min_wall is not None and min_pair is not None
    return {
        "walls_checked": 4 * len(tiles),
        "pairs_checked": npairs,
        "wall_failures": wall_fail,
        "pair_failures": pair_fail,
        "wall_contacts": wall_touch,
        "pair_contacts": pair_touch,
        "min_wall_slack": min_wall.text(),
        "min_pair_slack": min_pair.text(),
        "valid": not wall_fail and not pair_fail,
    }
