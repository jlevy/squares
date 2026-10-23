"""Adversarial probe of the continuous mode's box bounds against an exact oracle.

``slab.rs`` decides each box ``u in [ul, uh]``, ``v in [vl, vh]``, ``t in [ta, tb]`` by a
binary64 lower bound (lemmas C2 to C5). This program transcribes that bound from the
reviewer's reading of ``slab.rs`` and ``interval.rs`` (Python's floats are IEEE 754
binary64 with round-to-nearest and no fused operations, so each step computes what the
Rust computes), and holds every quantity it derives to exact rational truth computed by
an oracle written here: the area of a rectangle clipped by a rotated square, by exact
Sutherland--Hodgman clipping of the square against the rectangle's four half-planes.
Nothing of the source runs, and the oracle is not the source's ``oracle.rs``.

At poses sampled in each box, the corners and edges of the box included, it checks:

- C2: ``c(t)``, ``s(t)``, ``W(t)`` and ``E(t)`` lie in their enclosures; the centre lies
  in ``X x Y``, the path centre in ``Xm x Ym``, and ``|x - x_m(t)| <= dx`` (and for y);
- C4: a rectangle classified inside has its full area captured, one classified outside
  none, at every sampled pose;
- C3: the area lower bound is at most the exact area at the path centre, at every sampled
  angle;
- C5: one-sided difference quotients of each rectangle's capture, along x and along y
  (the crate's tests check x only), lie in its gradient enclosure;
- the whole box: ``base + f - dx |Gx| - dy |Gy|`` is at most the exact capture of every
  rectangle of the box at every sampled pose.

Instances are adversarial: rectangles placed at the edges and corners of the box's middle
square, thin ones, tiny ones, ones containing the square, ones on the container's edge
with the square pushed against it (``u`` or ``v`` near 1), boxes straddling
``t = sqrt 2 - 1``, boxes at ``t`` near ``10^-7`` and near ``83/200``, and deep boxes;
and, in a second family, the D4-expanded c6715 density itself. It prints one JSON receipt
with the counts of checks and of violations, and exits 1 if any check fails.

Usage::

    python -I bounds_probe.py --seed 1 --boxes 600 [--density c6715.json] > probe.json
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path

INF = math.inf
NAN = math.nan
GAP = 2.0**-52
TINY = 5e-324
SQRT_2 = 1.4142135623730951
# One deliberate error at a time, to show the probe detects it (see MUTATIONS).
MUTATION: str | None = None
MUTATIONS = (
    "area x 1.0005", "section term x 1.001", "gradient halved", "dx halved",
    "inside test loosened 1%", "outside test loosened 2%", "W upper bound at tb only",
    "midpoint rule for the trapezoid", "inner rectangle from the wrong end",
    "wrong branch of kx_up",
)

# --------------------------------------------------------------------- binary64 steps


def dn(x: float) -> float:
    return x - (abs(x) * GAP + TINY)


def up(x: float) -> float:
    return x + (abs(x) * GAP + TINY)


def fdiv(a: float, b: float) -> float:
    """IEEE division, which Python refuses at zero."""
    if b == 0.0:
        if a == 0.0 or math.isnan(a):
            return NAN
        return math.copysign(INF, a) * math.copysign(1.0, b)
    return a / b


def add_dn(a: float, b: float) -> float:
    return dn(a + b)


def add_up(a: float, b: float) -> float:
    return up(a + b)


def sub_dn(a: float, b: float) -> float:
    return dn(a - b)


def sub_up(a: float, b: float) -> float:
    return up(a - b)


def mul_dn(a: float, b: float) -> float:
    return dn(a * b)


def mul_up(a: float, b: float) -> float:
    return up(a * b)


def div_dn(a: float, b: float) -> float:
    return dn(fdiv(a, b))


def div_up(a: float, b: float) -> float:
    return up(fdiv(a, b))


def fmin(a: float, b: float) -> float:
    return (a if a < b else b) + a * 0.0


def fmax(a: float, b: float) -> float:
    return (a if a > b else b) + a * 0.0


def midpoint(a: float, b: float) -> float:
    return (a + b) / 2.0


@dataclass(frozen=True)
class Iv:
    lo: float
    hi: float

    def plus(self, o: Iv) -> Iv:
        return Iv(add_dn(self.lo, o.lo), add_up(self.hi, o.hi))

    def minus(self, o: Iv) -> Iv:
        return Iv(sub_dn(self.lo, o.hi), sub_up(self.hi, o.lo))

    def times(self, o: Iv) -> Iv:
        a, b, c, d = self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi
        return Iv(dn(fmin(fmin(a, b), fmin(c, d))), up(fmax(fmax(a, b), fmax(c, d))))

    def mul_nonneg(self, k: Iv) -> Iv:
        lo = self.lo * k.lo if self.lo >= 0.0 else self.lo * k.hi
        hi = self.hi * k.hi if self.hi >= 0.0 else self.hi * k.lo
        return Iv(dn(lo), up(hi))

    def min(self, o: Iv) -> Iv:
        return Iv(fmin(self.lo, o.lo), fmin(self.hi, o.hi))

    def max(self, o: Iv) -> Iv:
        return Iv(fmax(self.lo, o.lo), fmax(self.hi, o.hi))

    def pos(self) -> Iv:
        return Iv(fmax(self.lo, 0.0), fmax(self.hi, 0.0))

    def mag(self) -> float:
        return fmax(abs(self.lo), abs(self.hi))


def enclose(q: F) -> Iv:
    x = float(q)
    if F(x) == q:
        return Iv(x, x)
    if F(x) < q:
        return Iv(x, math.nextafter(x, INF))
    return Iv(math.nextafter(x, -INF), x)


# ------------------------------------------------------------ the transcribed bound


@dataclass(frozen=True)
class Rect:
    x1: Iv
    x2: Iv
    y1: Iv
    y2: Iv
    rho: Iv
    mass: Iv


@dataclass(frozen=True)
class Angles:
    c: Iv
    s: Iv
    w: Iv


@dataclass(frozen=True)
class Pose:
    an: Angles
    h: Iv
    ext: float
    x: Iv
    y: Iv
    xm: Iv
    ym: Iv
    dx: float
    dy: float
    e_lo: float
    e_hi: float
    u0: float
    v0: float


def angles(ta: float, tb: float) -> Angles:
    def sq_dn(t: float) -> float:
        return mul_dn(t, t)

    def sq_up(t: float) -> float:
        return mul_up(t, t)

    c_lo = div_dn(sub_dn(1.0, sq_up(tb)), add_up(1.0, sq_up(tb)))
    c_hi = div_up(sub_up(1.0, sq_dn(ta)), add_dn(1.0, sq_dn(ta)))
    s_lo = div_dn(2.0 * ta, add_up(1.0, sq_up(ta)))
    s_hi = div_up(2.0 * tb, add_dn(1.0, sq_dn(tb)))

    def w_dn(t: float) -> float:
        return div_dn(sub_dn(add_dn(1.0, 2.0 * t), sq_up(t)), add_up(1.0, sq_up(t)))

    def w_up(t: float) -> float:
        return div_up(sub_up(add_up(1.0, 2.0 * t), sq_dn(t)), add_dn(1.0, sq_dn(t)))

    w_lo = fmin(w_dn(ta), w_dn(tb))
    if MUTATION == "W upper bound at tb only":
        w_hi = w_up(tb)
    elif add_up(add_up(sq_up(tb), 2.0 * tb), 0.0) < 1.0:
        w_hi = w_up(tb)
    elif add_dn(sq_dn(ta), 2.0 * ta) > 1.0:
        w_hi = w_up(ta)
    else:
        w_hi = up(SQRT_2)
    return Angles(Iv(fmax(c_lo, 0.0), c_hi), Iv(fmax(s_lo, 0.0), s_hi), Iv(w_lo, w_hi))


def pose(ul: float, uh: float, vl: float, vh: float, ta: float, tb: float, half_l: Iv, h: Iv) -> Pose | None:
    an = angles(ta, tb)
    e_lo = sub_dn(half_l.lo, mul_up(h.hi, an.w.hi))
    e_hi = sub_up(half_l.hi, mul_dn(h.lo, an.w.lo))
    if not e_lo > 0.0:
        return None

    def rng(a: float, b: float) -> Iv:
        return Iv(add_dn(half_l.lo, mul_dn(a, e_lo)), add_up(half_l.hi, mul_up(b, e_hi)))

    u0, v0 = midpoint(ul, uh), midpoint(vl, vh)
    du = fmax(sub_up(uh, u0), sub_up(u0, ul))
    dv = fmax(sub_up(vh, v0), sub_up(v0, vl))
    return Pose(an, h, mul_up(h.hi, an.w.hi), rng(ul, uh), rng(vl, vh), rng(u0, u0), rng(v0, v0),
                mul_up(du, e_hi) * (0.5 if MUTATION == "dx halved" else 1.0),
                mul_up(dv, e_hi) * (0.5 if MUTATION == "dx halved" else 1.0), e_lo, e_hi, u0, v0)


def absmin(a: Iv) -> float:
    if a.lo > 0.0:
        return a.lo
    if a.hi < 0.0:
        return -a.hi
    return 0.0


def classify(p: Pose, r: Rect) -> str:
    if (r.x2.hi <= sub_dn(p.x.lo, p.ext) or r.x1.lo >= add_up(p.x.hi, p.ext)
            or r.y2.hi <= sub_dn(p.y.lo, p.ext) or r.y1.lo >= add_up(p.y.hi, p.ext)):
        return "outside"
    half = Iv(0.5, 0.5)
    mx = r.x1.plus(r.x2).mul_nonneg(half)
    my = r.y1.plus(r.y2).mul_nonneg(half)
    hx = r.x2.minus(r.x1).mul_nonneg(half).pos()
    hy = r.y2.minus(r.y1).mul_nonneg(half).pos()
    ddx, ddy = mx.minus(p.x), my.minus(p.y)
    c, s = p.an.c, p.an.s
    pu = c.times(ddx).plus(s.times(ddy))
    pv = c.times(ddy).minus(s.times(ddx))
    eu = hx.mul_nonneg(c).plus(hy.mul_nonneg(s))
    ev = hx.mul_nonneg(s).plus(hy.mul_nonneg(c))
    h_in = p.h.lo * (1.01 if MUTATION == "inside test loosened 1%" else 1.0)
    h_out = p.h.hi * (0.98 if MUTATION == "outside test loosened 2%" else 1.0)
    if add_up(pu.mag(), eu.hi) <= h_in and add_up(pv.mag(), ev.hi) <= h_in:
        return "inside"
    if sub_dn(absmin(pu), eu.hi) >= h_out or sub_dn(absmin(pv), ev.hi) >= h_out:
        return "outside"
    return "boundary"


def quot_lo(num_lo: float, k: Iv) -> float:
    return div_dn(num_lo, k.hi) if num_lo >= 0.0 else div_dn(num_lo, k.lo)


def quot_hi(num_hi: float, k: Iv) -> float:
    return div_up(num_hi, k.lo) if num_hi >= 0.0 else div_up(num_hi, k.hi)


def kx_up(k: Iv, xi: float) -> float:
    if MUTATION == "wrong branch of kx_up":
        return mul_up(k.hi, xi)
    return mul_up(k.hi, xi) if xi >= 0.0 else mul_up(k.lo, xi)


def kx_dn(k: Iv, xi: float) -> float:
    return mul_dn(k.lo, xi) if xi >= 0.0 else mul_dn(k.hi, xi)


def section_lo(c: Iv, s: Iv, hl: float, xi: float, e: float, b: float) -> float:
    f1 = quot_lo(sub_dn(hl, kx_up(c, xi)), s)
    if MUTATION == "section term x 1.001":
        f1 *= 1.001
    f2 = quot_lo(add_dn(hl, kx_dn(s, xi)), c)
    g1 = quot_hi(sub_up(-hl, kx_dn(c, xi)), s)
    g2 = quot_hi(sub_up(kx_up(s, xi), hl), c)
    return sub_dn(fmin(fmin(e, f1), f2), fmax(fmax(b, g1), g2))


def knots_at(c: float, s: float, h: float, e: float, b: float) -> list[float]:
    return [h * (c - s), h * (s - c), fdiv(h - s * e, c), fdiv(c * e - h, s), fdiv(-h - s * b, c),
            fdiv(c * b + h, s), h * (c + s), -h * (c + s), fdiv(-h - s * e, c), fdiv(c * e + h, s),
            fdiv(h - s * b, c), fdiv(c * b - h, s)]


def area_lo(p: Pose, r: Rect) -> float:
    xi1 = sub_up(r.x1.hi, p.xm.hi if MUTATION == "inner rectangle from the wrong end" else p.xm.lo)
    xi2 = sub_dn(r.x2.lo, p.xm.hi)
    e = sub_dn(r.y2.lo, p.ym.hi)
    b = sub_up(r.y1.hi, p.ym.lo)
    if not (xi1 < xi2 and b < e):
        return 0.0
    c, s, hl = p.an.c, p.an.s, p.h.lo
    extra = knots_at(c.lo, s.hi, hl, e, b) + knots_at(c.hi, s.lo, hl, e, b)
    knots = sorted([xi1, xi2] + [x for x in extra if x > xi1 and x < xi2])
    total = 0.0
    px = knots[0]
    pv = section_lo(c, s, hl, px, e, b)
    for x in knots[1:]:
        v = section_lo(c, s, hl, x, e, b)
        total_sum = add_dn(pv, v)
        width = sub_dn(x, px)
        if MUTATION == "midpoint rule for the trapezoid":
            mid = section_lo(c, s, hl, midpoint(px, x), e, b)
            if mid > 0.0 and width > 0.0:
                total = add_dn(total, mul_dn(mid, width))
        elif (total_sum > 0.0 or math.isnan(total_sum)) and width > 0.0:
            total = add_dn(total, dn(mul_dn(total_sum, width) * 0.5))
        px, pv = x, v
    if MUTATION == "area x 1.0005":
        total *= 1.0005
    return total


def over(a: Iv, k: Iv) -> Iv:
    return a.times(Iv(div_dn(1.0, k.hi), div_up(1.0, k.lo)))


def chord(z: Iv, centre: Iv, along: Iv, lo: Iv, hi: Iv, c: Iv, s: Iv, h: Iv) -> Iv:
    w = z.minus(centre)
    top = over(h.minus(c.times(w)), s).min(over(h.plus(s.times(w)), c))
    bottom = over(Iv(-h.hi, -h.lo).minus(c.times(w)), s).max(over(s.times(w).minus(h), c))
    upper = hi.minus(along).min(top)
    lower = lo.minus(along).max(bottom)
    return upper.minus(lower).pos()


def gradient(p: Pose, r: Rect) -> tuple[Iv, Iv]:
    c, s, h = p.an.c, p.an.s, p.h

    def reach_x(z: Iv) -> bool:
        return z.hi >= sub_dn(p.x.lo, p.ext) and z.lo <= add_up(p.x.hi, p.ext)

    def reach_y(z: Iv) -> bool:
        return z.hi >= sub_dn(p.y.lo, p.ext) and z.lo <= add_up(p.y.hi, p.ext)

    zero = Iv(0.0, 0.0)
    left = chord(r.x1, p.x, p.y, r.y1, r.y2, c, s, h) if reach_x(r.x1) else zero
    right = chord(r.x2, p.x, p.y, r.y1, r.y2, c, s, h) if reach_x(r.x2) else zero
    bottom = chord(r.y1, p.y, p.x, r.x1, r.x2, s, c, h) if reach_y(r.y1) else zero
    top = chord(r.y2, p.y, p.x, r.x1, r.x2, s, c, h) if reach_y(r.y2) else zero
    gx, gy = left.minus(right).mul_nonneg(r.rho), bottom.minus(top).mul_nonneg(r.rho)
    if MUTATION == "gradient halved":
        gx, gy = Iv(gx.lo * 0.5, gx.hi * 0.5), Iv(gy.lo * 0.5, gy.hi * 0.5)
    return gx, gy


def box_lower(p: Pose, rects: list[Rect]) -> tuple[float, list[str], float, float, float]:
    base, f = 0.0, 0.0
    gx, gy = Iv(0.0, 0.0), Iv(0.0, 0.0)
    classes = []
    for r in rects:
        k = classify(p, r)
        classes.append(k)
        if k == "inside":
            base = add_dn(base, r.mass.lo)
        elif k == "boundary":
            a = area_lo(p, r)
            if a > 0.0:
                f = add_dn(f, mul_dn(r.rho.lo, a))
            rx, ry = gradient(p, r)
            gx, gy = gx.plus(rx), gy.plus(ry)
    lx, ly = mul_up(p.dx, gx.mag()), mul_up(p.dy, gy.mag())
    return sub_dn(sub_dn(add_dn(base, f), lx), ly), classes, f, lx, ly


# ------------------------------------------------------------------- exact oracle


def clip(poly: list[tuple[F, F]], axis: int, edge: F, keep_ge: bool) -> list[tuple[F, F]]:
    out: list[tuple[F, F]] = []
    n = len(poly)
    for i in range(n):
        cur, nxt = poly[i], poly[(i + 1) % n]
        ci = cur[axis] >= edge if keep_ge else cur[axis] <= edge
        ni = nxt[axis] >= edge if keep_ge else nxt[axis] <= edge
        if ci:
            out.append(cur)
        if ci != ni:
            lam = (edge - cur[axis]) / (nxt[axis] - cur[axis])
            out.append((cur[0] + lam * (nxt[0] - cur[0]), cur[1] + lam * (nxt[1] - cur[1])))
    return out


def exact_area(rect: tuple[F, F, F, F], x: F, y: F, c: F, s: F, h: F) -> F:
    """|R intersect Q|, Q the square of half-side h centred at (x, y) with axes (c, s), (-s, c)."""
    x1, y1, x2, y2 = rect
    corners = [(x + c * a - s * b, y + s * a + c * b) for a, b in ((-h, -h), (h, -h), (h, h), (-h, h))]
    if (max(p[0] for p in corners) <= x1 or min(p[0] for p in corners) >= x2
            or max(p[1] for p in corners) <= y1 or min(p[1] for p in corners) >= y2):
        return F(0)
    poly = corners
    for axis, edge, keep in ((0, x1, True), (0, x2, False), (1, y1, True), (1, y2, False)):
        poly = clip(poly, axis, edge, keep)
        if len(poly) < 3:
            return F(0)
    twice = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[i][1] * poly[(i + 1) % len(poly)][0]
                for i in range(len(poly)))
    return abs(twice) / 2


def rotation(t: F) -> tuple[F, F]:
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


# ------------------------------------------------------------------ instances


@dataclass
class Exact:
    rect: tuple[F, F, F, F]
    density: F


def make_rect(e: Exact) -> Rect:
    x1, y1, x2, y2 = e.rect
    return Rect(enclose(x1), enclose(x2), enclose(y1), enclose(y2), enclose(e.density),
                enclose(e.density * (x2 - x1) * (y2 - y1)))


def q(x: float) -> F:
    return F(x)


def random_box(rng: random.Random) -> tuple[float, float, float, float, float, float]:
    kind = rng.random()
    if kind < 0.15:  # straddle sqrt 2 - 1
        centre = SQRT_2 - 1.0
        half = 10 ** rng.uniform(-9, -2)
        ta, tb = max(1e-7, centre - half * rng.random()), min(0.4150001, centre + half * rng.random())
    elif kind < 0.30:  # near eps
        ta = 1e-7 * (1 + rng.random() * 10)
        tb = ta + 10 ** rng.uniform(-12, -5)
    elif kind < 0.40:  # near T
        tb = 0.415 + rng.random() * 1e-9
        ta = tb - 10 ** rng.uniform(-12, -2)
    else:
        ta = 1e-7 + rng.random() * 0.414
        tb = min(0.4150001, ta + 10 ** rng.uniform(-12, -1.5))
    widths = [10 ** rng.uniform(-11, 0) for _ in range(2)]
    lows = []
    for w in widths:
        place = rng.random()
        if place < 0.3:  # pushed against the container's edge
            lows.append(max(0.0, 1.0 - w))
        elif place < 0.4:
            lows.append(0.0)
        else:
            lows.append(rng.random() * max(0.0, 1.0 - w))
    ul, vl = lows
    uh, vh = min(1.0, ul + widths[0]), min(1.0, vl + widths[1])
    return ul, uh, vl, vh, ta, tb


def adversarial_rects(rng: random.Random, x0: F, y0: F, c: F, s: F, h: F, side: F, count: int) -> list[Exact]:
    """Rectangles at the middle square's edges and corners, thin, tiny, large, or on K's edge."""
    out = []
    quantum = F(1, 10**12)

    def snap(v: F) -> F:
        v = min(max(v, F(0)), side)
        return F(round(v / quantum)) * quantum

    for _ in range(count):
        a = F(rng.choice((-1, 1))) * h * F(rng.uniform(0.9, 1.1))
        b = h * F(rng.uniform(-1.2, 1.2))
        if rng.random() < 0.5:
            a, b = b, a
        px, py = x0 + c * a - s * b, y0 + s * a + c * b
        kind = rng.random()
        if kind < 0.25:
            w, hh = F(10 ** rng.uniform(-9, -6)), F(10 ** rng.uniform(-3, 0))
        elif kind < 0.4:
            w, hh = F(10 ** rng.uniform(-3, 0)), F(10 ** rng.uniform(-9, -6))
        elif kind < 0.55:
            w = hh = F(10 ** rng.uniform(-8, -3))
        elif kind < 0.7:
            w, hh = F(rng.uniform(1.5, 3)), F(rng.uniform(1.5, 3))
        else:
            w, hh = F(10 ** rng.uniform(-3, 0.2)), F(10 ** rng.uniform(-3, 0.2))
        x1 = snap(px - w * F(rng.random()))
        y1 = snap(py - hh * F(rng.random()))
        x2, y2 = snap(x1 + w), snap(y1 + hh)
        if rng.random() < 0.15:
            x2 = side
        if rng.random() < 0.15:
            y2 = side
        if x1 < x2 and y1 < y2:
            density = F(rng.randint(1, 4000), rng.choice((7, 100, 1000)))
            out.append(Exact((x1, y1, x2, y2), density))
    return out


def rows_of(doc: dict) -> list[tuple[list, object]]:
    """Orbit rows and weights of a format T (rectangles, weights) or M ({rectangle, mass}) file."""
    rows = doc["rectangles"]
    if rows and isinstance(rows[0], dict):
        if doc.get("points"):
            raise SystemExit("a format M candidate with points is outside this reader")
        return [(row["rectangle"], row["mass"]) for row in rows]
    return list(zip(rows, doc["weights"], strict=True))


def load_density(path: Path) -> tuple[F, list[Exact]]:
    doc = json.loads(path.read_text())
    side = F(str(doc["L"]))
    merged: dict[tuple[F, F, F, F], F] = {}
    order: list[tuple[F, F, F, F]] = []
    for row, weight in rows_of(doc):
        if F(str(weight)) == 0:
            continue
        x1, y1, x2, y2 = (F(str(v)) for v in row)
        share = F(str(weight)) / 8
        density = share / ((x2 - x1) * (y2 - y1))
        rx1, rx2, ry1, ry2 = side - x2, side - x1, side - y2, side - y1
        images = [(x1, y1, x2, y2), (rx1, y1, rx2, y2), (x1, ry1, x2, ry2), (rx1, ry1, rx2, ry2),
                  (y1, x1, y2, x2), (ry1, x1, ry2, x2), (y1, rx1, y2, rx2), (ry1, rx1, ry2, rx2)]
        for image in images:
            if image in merged:
                merged[image] += density
            else:
                merged[image] = density
                order.append(image)
    return side, [Exact(k, merged[k]) for k in order]


# ---------------------------------------------------------------------- the probe


class Tally:
    def __init__(self) -> None:
        self.checks: dict[str, int] = {}
        self.failures: dict[str, int] = {}
        self.violations: dict[str, list] = {}

    def check(self, name: str, ok: bool, detail: object) -> None:
        self.checks[name] = self.checks.get(name, 0) + 1
        if not ok:
            self.failures[name] = self.failures.get(name, 0) + 1
            self.violations.setdefault(name, [])
            if len(self.violations[name]) < 5:
                self.violations[name].append(detail)


def sample_points(lo: float, hi: float, rng: random.Random) -> list[float]:
    pts = [lo, hi, midpoint(lo, hi), lo + (hi - lo) * rng.random()]
    return [min(max(p, lo), hi) for p in pts]


def probe_box(tally: Tally, rng: random.Random, side: F, core: F, box, exacts: list[Exact], label: str,
              poses: int) -> None:
    ul, uh, vl, vh, ta, tb = box
    half_l, h = enclose(side / 2), enclose(core / 2)
    p = pose(ul, uh, vl, vh, ta, tb, half_l, h)
    if p is None:
        return
    rects = [make_rect(e) for e in exacts]
    lower, classes, _f, lx, ly = box_lower(p, rects)
    hh = core / 2
    u0, v0 = q(p.u0), q(p.v0)
    for k in range(poses):
        t = q(sample_points(ta, tb, rng)[k % 4] if k < 4 else ta + (tb - ta) * rng.random())
        t = min(max(t, q(ta)), q(tb))
        c, s = rotation(t)
        w = c + s
        e_t = side / 2 - hh * w
        tally.check("C2 angle enclosures", q(p.an.c.lo) <= c <= q(p.an.c.hi) and q(p.an.s.lo) <= s <= q(p.an.s.hi)
                    and q(p.an.w.lo) <= w <= q(p.an.w.hi), (label, box, str(t)))
        tally.check("C2 E(t) enclosure", q(p.e_lo) <= e_t <= q(p.e_hi), (label, box, str(t)))
        us = sample_points(ul, uh, rng)
        vs = sample_points(vl, vh, rng)
        u, v = q(us[k % 4]), q(vs[(k + 1) % 4])
        x, y = side / 2 + u * e_t, side / 2 + v * e_t
        xm, ym = side / 2 + u0 * e_t, side / 2 + v0 * e_t
        tally.check("C2 centre ranges", q(p.x.lo) <= x <= q(p.x.hi) and q(p.y.lo) <= y <= q(p.y.hi)
                    and q(p.xm.lo) <= xm <= q(p.xm.hi) and q(p.ym.lo) <= ym <= q(p.ym.hi), (label, box))
        tally.check("C5 dx, dy", abs(x - xm) <= q(p.dx) and abs(y - ym) <= q(p.dy), (label, box))
        total = F(0)
        for i, (ex, r) in enumerate(zip(exacts, rects, strict=True)):
            area = exact_area(ex.rect, x, y, c, s, hh)
            total += ex.density * area
            full = (ex.rect[2] - ex.rect[0]) * (ex.rect[3] - ex.rect[1])
            if classes[i] == "inside":
                tally.check("C4 inside", area == full, (label, box, i))
            elif classes[i] == "outside":
                tally.check("C4 outside", area == 0, (label, box, i))
            else:
                am = exact_area(ex.rect, xm, ym, c, s, hh)
                lo = area_lo(p, r)
                tally.check("C3 area at the path centre", (not lo > 0.0) or q(lo) <= am,
                            (label, box, i, lo, float(am)))
                gx, gy = gradient(p, r)
                step = F(1, 10**10)
                for axis, g, coord_ok in (
                    ("x", gx, lambda d: q(p.x.lo) <= x + d <= q(p.x.hi)),
                    ("y", gy, lambda d: q(p.y.lo) <= y + d <= q(p.y.hi)),
                ):
                    for d in (step, -step):
                        if not coord_ok(d):
                            continue
                        if axis == "x":
                            moved = exact_area(ex.rect, x + d, y, c, s, hh)
                        else:
                            moved = exact_area(ex.rect, x, y + d, c, s, hh)
                        quotient = (moved - area) / d * ex.density
                        tally.check(f"C5 gradient along {axis}", q(g.lo) <= quotient <= q(g.hi),
                                    (label, box, i, axis, float(quotient), g.lo, g.hi))
        tally.check("whole box bound", (not math.isfinite(lower)) or q(lower) <= total,
                    (label, box, lower, float(total), lx, ly))


def run_probe(seed: int, boxes: int, rects: int, poses: int, density: Path | None,
              density_boxes: int, mutation: str | None) -> dict:
    """One probe: adversarial families, then (optionally) a real density; a receipt."""
    global MUTATION
    MUTATION = mutation
    rng = random.Random(seed)
    tally = Tally()
    started = time.monotonic()
    families = {"adversarial, L = 67/10, B = 199529/200000": (F(67, 10), F(199529, 200000)),
                "adversarial, L = 3/2, B = 1 (tiny centre domain near pi/4)": (F(3, 2), F(1)),
                "adversarial, L = 573351/100000, B = 499/500": (F(573351, 100000), F(499, 500))}
    per_family = max(1, boxes // len(families))
    boxes_done = 0
    for label, (side, core) in families.items():
        for _ in range(per_family):
            box = random_box(rng)
            ul, uh, vl, vh, ta, tb = box
            tm = q(midpoint(ta, tb))
            c, s = rotation(tm)
            e_t = side / 2 - core / 2 * (c + s)
            if e_t <= 0:
                continue
            x0 = side / 2 + q(midpoint(ul, uh)) * e_t
            y0 = side / 2 + q(midpoint(vl, vh)) * e_t
            exacts = adversarial_rects(rng, x0, y0, c, s, core / 2, side, rects)
            probe_box(tally, rng, side, core, box, exacts, label, poses)
            boxes_done += 1
    if density is not None:
        side, exacts = load_density(density)
        core = F(199529, 200000)
        for _ in range(density_boxes):
            box = random_box(rng)
            ul, uh, vl, vh, ta, tb = box
            tm = q(midpoint(ta, tb))
            c, s = rotation(tm)
            e_t = side / 2 - core / 2 * (c + s)
            x0 = side / 2 + q(midpoint(ul, uh)) * e_t
            y0 = side / 2 + q(midpoint(vl, vh)) * e_t
            reach = core + F(3, 2)
            near = [ex for ex in exacts
                    if ex.rect[2] >= x0 - reach and ex.rect[0] <= x0 + reach
                    and ex.rect[3] >= y0 - reach and ex.rect[1] <= y0 + reach]
            probe_box(tally, rng, side, core, box, near, f"density {density.name}", 3)
            boxes_done += 1
    MUTATION = None
    return {
        "seed": seed,
        "mutation": mutation,
        "boxes": boxes_done,
        "checks": tally.checks,
        "failures": tally.failures,
        "violation_examples": tally.violations,
        "failure_count": sum(tally.failures.values()),
        "seconds": round(time.monotonic() - started, 1),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--boxes", type=int, default=600)
    parser.add_argument("--rects", type=int, default=24)
    parser.add_argument("--poses", type=int, default=6)
    parser.add_argument("--density", type=Path, default=None)
    parser.add_argument("--density-boxes", type=int, default=60)
    parser.add_argument("--mutate", choices=MUTATIONS, default=None)
    args = parser.parse_args()
    receipt = run_probe(args.seed, args.boxes, args.rects, args.poses, args.density,
                        args.density_boxes, args.mutate)
    json.dump(receipt, sys.stdout, indent=2, default=str)
    print()
    return 1 if receipt["failure_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
