"""Clean-room exact check of the #763 certificates at 268 and 303.

Stage 4 review of 24 October 2026 (bead think-zjus). Written from the mathematics
alone: its author read no checker of the source and no checker of this repository,
and it imports nothing from either. It reads each certificate as data.

The certificate format, as the certificates' own comment line states it: comment
lines start with '#'; a header line 'n side'; then n lines 'x y t', each field an
integer or a rational p/q, where (x, y) is the centre of a unit square and
t = tan(theta/2) its rotation. The square is

    { c + a*u + b*v : |a| <= 1/2, |b| <= 1/2 },
    u = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)),  v = (-u_y, u_x),

and u, v are exact rational unit vectors, so every quantity below is exact.

The statement decided: the n squares lie in the closed box [0, side]^2 and their
interiors are pairwise disjoint. That is the upper bound s(n) <= side.

Two routes decide every pair, in Python's exact Fraction arithmetic:

* Route A, separating axes. Two convex polygons have disjoint interiors if and only
  if, along the normal of some edge of one of them, their projections meet in at
  most one point (if the interiors are disjoint, the origin is not interior to the
  Minkowski difference P - Q, a convex polygon whose edge normals are those of P
  and Q, so one of its edges' supporting lines separates). For two squares the
  normals are u_i, v_i, u_j, v_j, and the projection of square k on a unit axis w
  is w.c_k +- half_k * (|w.u_k| + |w.v_k|). Route A runs over every pair, with no
  filter.
* Route B, clipping. Two convex polygons have disjoint interiors if and only if
  their intersection has zero area. Route B clips one square by the other's four
  edge half-planes (Sutherland-Hodgman, exact) and takes the shoelace area. It runs
  over the pairs whose centres are closer than sqrt(2)*(half_i + half_j); every
  other pair is disjoint because each square lies in the closed disc of radius
  sqrt(2)*half about its centre and its interior in the open disc. The distance
  test is exact (squared distances against 2*(half_i + half_j)^2).

Containment: route A checks the four corners of every square against the walls;
route B checks each square's support half*(|u_x| + |u_y|) against each wall.

The controls build modified packings in memory, each from a pair or a square
chosen by an exact rule, and decide them on both routes:

* refused: a duplicate square; a square moved halfway to its nearest neighbour; a
  square moved 1e-30 past exact contact with a neighbour (sharp); a square
  enlarged by its pair gap plus 1e-30 (pair); a square enlarged by its wall
  clearance plus 1e-30 (wall); the box 1e-30 below the packing's extent (sharp);
* accepted: the same square moved to exact contact (sharp); the box at the
  packing's exact extent (sharp);
* reported, not required: every rotation mirrored (t -> -t), and two malformed
  texts, which the parser must refuse.

Run from packing/ with the project interpreter, for example:

    uv run --frozen --all-extras --group dev python -I \\
      resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/check_certificates.py \\
      --out resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/out/check-certificates.json

It prints one line per decision and writes the JSON receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent.parent
SOURCE = PACKET / "source" / "certificates" / "best"

# The record's claims (T-240's `claim` field, frontier/results.yaml at #789's head
# 0329f73d6, and the source's certified_bounds.json `rounded_up` field).
CLAIMS = {
    268: {
        "file": SOURCE / "n268.cert",
        "sha256": "e9833bf26e1bf7e4719ee983c91979ba51f7319d6caa8dd1911fce820903e07e",
        "side": "78645658458105249171306580101/4660659750118000000000000000",
        "print": "16.874361715874",
    },
    303: {
        "file": SOURCE / "n303.cert",
        "sha256": "39a150f4cce7e435b0b7d6d82dbf15d172611e07c413e1abe9d61cf90822791a",
        "side": (
            "55035101387261868285958438488216555614454417144023299/"
            "3073388523105741896887024831655729584500000000000000"
        ),
        "print": "17.906978233799",
    },
}

RATIONAL = re.compile(r"^[+-]?[0-9]+(/[0-9]+)?$")
HALF = Fraction(1, 2)
TINY = Fraction(1, 10**30)


class CertificateError(ValueError):
    """The text is not a certificate in the stated format."""


@dataclass(frozen=True)
class Square:
    """A square with centre (x, y), unit edge directions u = (c, s), v = (-s, c)."""

    x: Fraction
    y: Fraction
    c: Fraction
    s: Fraction
    half: Fraction = HALF

    def corners(self) -> list[tuple[Fraction, Fraction]]:
        """The four corners, counter-clockwise."""
        h = self.half
        ux, uy = h * self.c, h * self.s
        vx, vy = -h * self.s, h * self.c
        return [
            (self.x + ux + vx, self.y + uy + vy),
            (self.x - ux + vx, self.y - uy + vy),
            (self.x - ux - vx, self.y - uy - vy),
            (self.x + ux - vx, self.y + uy - vy),
        ]


@dataclass(frozen=True)
class Packing:
    n: int
    side: Fraction
    squares: tuple[Square, ...]
    comments: tuple[str, ...] = ()


def parse_rational(token: str) -> Fraction:
    if not RATIONAL.match(token):
        msg = f"not an integer or p/q rational: {token!r}"
        raise CertificateError(msg)
    if "/" in token:
        num, den = token.split("/")
        if int(den) == 0:
            msg = f"zero denominator: {token!r}"
            raise CertificateError(msg)
        return Fraction(int(num), int(den))
    return Fraction(int(token))


def square_from_tangent(x: Fraction, y: Fraction, t: Fraction) -> Square:
    d = 1 + t * t
    c, s = (1 - t * t) / d, 2 * t / d
    if c * c + s * s != 1:  # an identity; kept as a guard on the arithmetic
        msg = "rotation is not a unit vector"
        raise CertificateError(msg)
    return Square(x, y, c, s)


def parse_certificate(text: str) -> Packing:
    comments: list[str] = []
    rows: list[list[str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            comments.append(line)
            continue
        rows.append(line.split())
    if not rows:
        msg = "no header line"
        raise CertificateError(msg)
    header = rows[0]
    if len(header) != 2 or not header[0].isdigit():
        msg = f"header is not 'n side': {header!r}"
        raise CertificateError(msg)
    n = int(header[0])
    side = parse_rational(header[1])
    if n <= 0 or side <= 0:
        msg = "n and side must be positive"
        raise CertificateError(msg)
    body = rows[1:]
    if len(body) != n:
        msg = f"header says {n} squares, the text has {len(body)} square lines"
        raise CertificateError(msg)
    squares = []
    for k, row in enumerate(body, start=1):
        if len(row) != 3:
            msg = f"square line {k} has {len(row)} fields, not 3"
            raise CertificateError(msg)
        x, y, t = (parse_rational(tok) for tok in row)
        squares.append(square_from_tangent(x, y, t))
    return Packing(n, side, tuple(squares), tuple(comments))


# ---------------------------------------------------------------- route A


def projection_radius(sq: Square, wx: Fraction, wy: Fraction) -> Fraction:
    return sq.half * (abs(wx * sq.c + wy * sq.s) + abs(-wx * sq.s + wy * sq.c))


def axes(a: Square, b: Square) -> list[tuple[Fraction, Fraction]]:
    return [(a.c, a.s), (-a.s, a.c), (b.c, b.s), (-b.s, b.c)]


def sat_gap(a: Square, b: Square, *, full: bool) -> Fraction | None:
    """Largest projected gap over the four edge normals (>= 0 iff separated).

    With full=False it returns the first non-negative gap it meets, or None when no
    axis separates; with full=True it returns the maximum over the four axes.
    """
    dx, dy = b.x - a.x, b.y - a.y
    best: Fraction | None = None
    for wx, wy in axes(a, b):
        gap = (
            abs(wx * dx + wy * dy)
            - projection_radius(a, wx, wy)
            - projection_radius(b, wx, wy)
        )
        if not full and gap >= 0:
            return gap
        if best is None or gap > best:
            best = gap
    if not full:
        return None
    return best


def corners_inside(sq: Square, side: Fraction) -> bool:
    return all(0 <= px <= side and 0 <= py <= side for px, py in sq.corners())


# ---------------------------------------------------------------- route B


def cross(ox: Fraction, oy: Fraction, ax: Fraction, ay: Fraction, px: Fraction,
          py: Fraction) -> Fraction:
    return (ax - ox) * (py - oy) - (ay - oy) * (px - ox)


def clip_area(a: Square, b: Square) -> Fraction:
    """Exact area of the intersection of two squares (Sutherland-Hodgman)."""
    poly = a.corners()
    clip = b.corners()
    for k in range(4):
        (ex, ey), (fx, fy) = clip[k], clip[(k + 1) % 4]
        out: list[tuple[Fraction, Fraction]] = []
        m = len(poly)
        for idx in range(m):
            px, py = poly[idx - 1]
            qx, qy = poly[idx]
            dp = cross(ex, ey, fx, fy, px, py)
            dq = cross(ex, ey, fx, fy, qx, qy)
            if dq >= 0:
                if dp < 0:
                    lam = dp / (dp - dq)
                    out.append((px + (qx - px) * lam, py + (qy - py) * lam))
                out.append((qx, qy))
            elif dp >= 0:
                lam = dp / (dp - dq)
                out.append((px + (qx - px) * lam, py + (qy - py) * lam))
        poly = out
        if not poly:
            return Fraction(0)
    twice = Fraction(0)
    for idx in range(len(poly)):
        (px, py), (qx, qy) = poly[idx - 1], poly[idx]
        twice += px * qy - qx * py
    return abs(twice) / 2


def support_clearance(sq: Square, side: Fraction) -> Fraction:
    h = sq.half * (abs(sq.c) + abs(sq.s))
    return min(sq.x - h, side - sq.x - h, sq.y - h, side - sq.y - h)


def near(a: Square, b: Square) -> bool:
    dx, dy = b.x - a.x, b.y - a.y
    reach = a.half + b.half
    return dx * dx + dy * dy < 2 * reach * reach


# ---------------------------------------------------------------- decisions


@dataclass
class Decision:
    accepted: bool
    pairs: int
    pairs_decided: int
    overlaps: list[tuple[int, int]]
    outside: list[int]
    cpu_seconds: float
    least_gap: Fraction | None = None
    least_gap_pair: tuple[int, int] | None = None
    least_clearance: Fraction | None = None
    least_clearance_square: int | None = None
    zero_gap_pairs: int = 0

    def summary(self) -> dict[str, object]:
        return {
            "accepted": self.accepted,
            "pairs": self.pairs,
            "pairs_decided": self.pairs_decided,
            "overlapping_pairs": [[i + 1, j + 1] for i, j in self.overlaps[:20]],
            "overlapping_pair_count": len(self.overlaps),
            "squares_outside": [k + 1 for k in self.outside[:20]],
            "squares_outside_count": len(self.outside),
            "least_pair_gap": None if self.least_gap is None else str(self.least_gap),
            "least_pair_gap_float": None if self.least_gap is None else float(self.least_gap),
            "least_pair_gap_squares": None if self.least_gap_pair is None else [
                self.least_gap_pair[0] + 1, self.least_gap_pair[1] + 1],
            "pairs_at_zero_gap": self.zero_gap_pairs,
            "least_wall_clearance": None if self.least_clearance is None else str(
                self.least_clearance),
            "least_wall_clearance_float": None if self.least_clearance is None else float(
                self.least_clearance),
            "least_wall_clearance_square": None if self.least_clearance_square is None
            else self.least_clearance_square + 1,
            "cpu_seconds": round(self.cpu_seconds, 3),
        }


def route_a(p: Packing, *, exhaustive: bool) -> Decision:
    """Separating axes over every pair; corners against the walls."""
    t0 = time.process_time()
    sq = p.squares
    outside = [k for k, s in enumerate(sq) if not corners_inside(s, p.side)]
    overlaps: list[tuple[int, int]] = []
    least: Fraction | None = None
    least_pair: tuple[int, int] | None = None
    zero = 0
    pairs = decided = 0
    for i in range(len(sq)):
        for j in range(i + 1, len(sq)):
            pairs += 1
            is_near = near(sq[i], sq[j])
            if not exhaustive and not is_near:
                continue
            decided += 1
            gap = sat_gap(sq[i], sq[j], full=is_near)
            if gap is None or gap < 0:
                overlaps.append((i, j))
                continue
            if is_near:
                if gap == 0:
                    zero += 1
                if least is None or gap < least:
                    least, least_pair = gap, (i, j)
    clear = [min(min(px, p.side - px, py, p.side - py) for px, py in s.corners()) for s in sq]
    k_min = min(range(len(sq)), key=clear.__getitem__)
    return Decision(not overlaps and not outside, pairs, decided, overlaps, outside,
                    time.process_time() - t0, least, least_pair, clear[k_min], k_min, zero)


def route_b(p: Packing) -> Decision:
    """Exact clipped area over the pairs closer than the circumscribed discs."""
    t0 = time.process_time()
    sq = p.squares
    clear = [support_clearance(s, p.side) for s in sq]
    outside = [k for k, c in enumerate(clear) if c < 0]
    overlaps: list[tuple[int, int]] = []
    pairs = decided = 0
    for i in range(len(sq)):
        for j in range(i + 1, len(sq)):
            pairs += 1
            if not near(sq[i], sq[j]):
                continue
            decided += 1
            if clip_area(sq[i], sq[j]) > 0:
                overlaps.append((i, j))
    k_min = min(range(len(sq)), key=clear.__getitem__)
    return Decision(not overlaps and not outside, pairs, decided, overlaps, outside,
                    time.process_time() - t0, None, None, clear[k_min], k_min)


def decide(p: Packing, *, exhaustive: bool = False) -> dict[str, object]:
    a = route_a(p, exhaustive=exhaustive)
    b = route_b(p)
    same = (a.accepted == b.accepted and sorted(a.overlaps) == sorted(b.overlaps)
            and sorted(a.outside) == sorted(b.outside))
    return {
        "accepted": a.accepted and b.accepted,
        "routes_agree": same,
        "route_a": a.summary(),
        "route_b": b.summary(),
    }


# ---------------------------------------------------------------- side and print


def ceil_print(x: Fraction, places: int = 12) -> str:
    scaled = x * 10**places
    up = -((-scaled.numerator) // scaled.denominator)
    whole, frac = divmod(up, 10**places)
    return f"{whole}.{frac:0{places}d}"


def decimal(x: Fraction, places: int = 40) -> str:
    scaled = x * 10**places
    down = scaled.numerator // scaled.denominator
    whole, frac = divmod(down, 10**places)
    return f"{whole}.{frac:0{places}d}"


def extent(p: Packing) -> dict[str, object]:
    xs = [px for s in p.squares for px, _ in s.corners()]
    ys = [py for s in p.squares for _, py in s.corners()]
    lo_x, hi_x, lo_y, hi_y = min(xs), max(xs), min(ys), max(ys)
    tight = max(hi_x - lo_x, hi_y - lo_y)
    return {
        "min_x": float(lo_x), "max_x_slack": float(p.side - hi_x),
        "min_y": float(lo_y), "max_y_slack": float(p.side - hi_y),
        "tight_side_after_translation": decimal(tight, 30),
        "side_minus_tight": float(p.side - tight),
        "box_at_extent": str(max(hi_x, hi_y)),
        "extent_from_origin_is_inside_box": bool(lo_x >= 0 and lo_y >= 0),
    }


# ---------------------------------------------------------------- controls


def nearest_pairs(p: Packing) -> list[tuple[Fraction, int, int]]:
    out = []
    sq = p.squares
    for i in range(len(sq)):
        for j in range(i + 1, len(sq)):
            if near(sq[i], sq[j]):
                gap = sat_gap(sq[i], sq[j], full=True)
                assert gap is not None
                out.append((gap, i, j))
    out.sort()
    return out


def with_square(p: Packing, k: int, sq: Square) -> Packing:
    squares = list(p.squares)
    squares[k] = sq
    return replace(p, squares=tuple(squares))


def locally_valid(p: Packing, k: int, sq: Square) -> bool:
    """Whether square k, replaced by sq, is inside the box and overlaps no other.

    Used only to choose a control; every control is then decided in full.
    """
    if not corners_inside(sq, p.side):
        return False
    for m, other in enumerate(p.squares):
        if m == k or not near(sq, other):
            continue
        gap = sat_gap(sq, other, full=False)
        if gap is None or gap < 0:
            return False
    return True


def contact_parameter(a: Square, b: Square) -> Fraction:
    """Least lam >= 0 at which b moved by lam*(a.c - b.c) touches a.

    Along each axis w the gap of the moved pair is max(A + lam*r, B - lam*r), so
    the overlap set {lam : every gap < 0} is the intersection of open intervals
    (L_w, U_w); lam = 1 (centres coincide) lies in it, and its lower end is the
    contact. Exact.
    """
    dx, dy = a.x - b.x, a.y - b.y
    lower = Fraction(0)
    for wx, wy in axes(a, b):
        ra = projection_radius(a, wx, wy)
        rb = projection_radius(b, wx, wy)
        proj_a = wx * a.x + wy * a.y
        proj_b = wx * b.x + wy * b.y
        rate = wx * dx + wy * dy
        # b's projection centre at lam: proj_b + lam*rate; gaps:
        # g1 = (proj_b + lam*rate) - rb - (proj_a + ra)  (b beyond a)
        # g2 = (proj_a - ra) - (proj_b + lam*rate + rb)  (b before a)
        reach = ra + rb
        if rate == 0:
            continue  # this axis never closes: |proj_a - proj_b| stays; handled at lam = 1
        # both gaps negative iff |proj_b + lam*rate - proj_a| < reach
        lo = (proj_a - reach - proj_b) / rate
        hi = (proj_a + reach - proj_b) / rate
        lower = max(lower, min(lo, hi))
    return lower


def controls(p: Packing) -> list[dict[str, object]]:
    pairs = nearest_pairs(p)
    out: list[dict[str, object]] = []

    def run(name: str, q: Packing, expect: bool, rule: str) -> dict[str, object]:
        d = decide(q)
        ok = d["accepted"] is expect and d["routes_agree"]
        row = {"control": name, "rule": rule, "expected_accepted": expect,
               "met": ok, **d}
        print(f"  control {name}: accepted={d['accepted']} routes_agree="
              f"{d['routes_agree']} expected={expect} -> {'MET' if ok else 'NOT MET'}")
        out.append(row)
        return row

    gap0, i0, j0 = pairs[0]
    a, b = p.squares[i0], p.squares[j0]
    run("duplicate-square", with_square(p, j0, replace(a)), expect=False,
        rule=f"square {j0 + 1} replaced by a copy of square {i0 + 1}, the closest pair")
    mid = replace(b, x=(a.x + b.x) / 2, y=(a.y + b.y) / 2)
    run("moved-halfway", with_square(p, j0, mid), expect=False,
        rule=f"square {j0 + 1} moved halfway to square {i0 + 1}'s centre")

    # Sharp contact: the closest pair whose moved square stays valid at contact.
    chosen = None
    for gap, i, j in pairs[:40]:
        for mover, other in ((j, i), (i, j)):
            sa, sb = p.squares[other], p.squares[mover]
            lam = contact_parameter(sa, sb)
            touch = replace(sb, x=sb.x + lam * (sa.x - sb.x), y=sb.y + lam * (sa.y - sb.y))
            gap_touch = sat_gap(sa, touch, full=True)
            if gap_touch != 0:
                continue
            if locally_valid(p, mover, touch):
                chosen = (gap, mover, other, lam, sa, sb)
                break
        if chosen:
            break
    if chosen is None:
        out.append({"control": "sharp-contact", "met": False,
                    "rule": "no closest pair of the first 40 gave a valid contact"})
    else:
        gap, mover, other, lam, sa, sb = chosen
        dist2 = (sa.x - sb.x) ** 2 + (sa.y - sb.y) ** 2
        touch = replace(sb, x=sb.x + lam * (sa.x - sb.x), y=sb.y + lam * (sa.y - sb.y))
        rule = (f"square {mover + 1} moved toward square {other + 1}'s centre by "
                f"lam = {float(lam):.6e} of the centre distance (move "
                f"{float(lam) * float(dist2) ** 0.5:.3e}), to exact contact")
        run("sharp-contact-touching", with_square(p, mover, touch), expect=True, rule=rule)
        lam2 = lam + TINY
        past = replace(sb, x=sb.x + lam2 * (sa.x - sb.x), y=sb.y + lam2 * (sa.y - sb.y))
        run("sharp-contact-past", with_square(p, mover, past), expect=False,
            rule=rule.replace("to exact contact", "plus 1e-30 of it, past contact"))

    big = replace(b, half=b.half + gap0 + TINY)
    run("enlarged-square-pair", with_square(p, j0, big), expect=False,
        rule=f"square {j0 + 1}'s half-edge enlarged by the closest pair's gap "
             f"({float(gap0):.3e}) plus 1e-30")
    clear = [support_clearance(s, p.side) for s in p.squares]
    k = min(range(p.n), key=clear.__getitem__)
    wide = replace(p.squares[k], half=p.squares[k].half + clear[k] + TINY)
    run("enlarged-square-wall", with_square(p, k, wide), expect=False,
        rule=f"square {k + 1}'s half-edge enlarged by its wall clearance "
             f"({float(clear[k]):.3e}) plus 1e-30")

    ext = extent(p)
    if ext["extent_from_origin_is_inside_box"]:
        at = Fraction(str(ext["box_at_extent"]))
        run("box-at-extent", replace(p, side=at), expect=True,
            rule="box side set to the largest corner coordinate, exactly")
        run("box-below-extent", replace(p, side=at - TINY), expect=False,
            rule="box side 1e-30 below the largest corner coordinate")

    mirrored = tuple(replace(s, s=-s.s) for s in p.squares)
    d = decide(replace(p, squares=mirrored))
    out.append({"control": "mirrored-rotations (reported)", "expected_accepted": None,
                "rule": "every t replaced by -t (the opposite rotation sense)", **d})
    print(f"  control mirrored-rotations (reported): accepted={d['accepted']} "
          f"overlapping pairs A={d['route_a']['overlapping_pair_count']} "
          f"B={d['route_b']['overlapping_pair_count']}")
    return out


def parse_controls(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    header_at = next(k for k, ln in enumerate(lines) if ln.strip() and not ln.startswith("#"))
    n, side = lines[header_at].split()
    bad_count = [*lines[:header_at], f"{int(n) + 1} {side}", *lines[header_at + 1:]]
    bad_token = list(lines)
    first = header_at + 1
    x, y, t = bad_token[first].split()
    bad_token[first] = f"{float(Fraction(x))!r} {y} {t}"
    rows = []
    for name, body in (("header-count-plus-one", bad_count),
                       ("decimal-token", bad_token)):
        try:
            parse_certificate("\n".join(body))
        except CertificateError as exc:
            rows.append({"control": name, "refused": True, "reason": str(exc)})
            print(f"  parse control {name}: refused ({exc})")
        else:
            rows.append({"control": name, "refused": False})
            print(f"  parse control {name}: NOT refused")
    return rows


def check(n: int) -> dict[str, object]:
    claim = CLAIMS[n]
    path = claim["file"]
    assert isinstance(path, Path)
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    text = raw.decode("ascii")
    p = parse_certificate(text)
    side_claim = parse_rational(str(claim["side"]))
    print(f"n = {n}: {path.name} sha256 {digest[:16]}... (expected "
          f"{str(claim['sha256'])[:16]}...: {'match' if digest == claim['sha256'] else 'DIFFER'})")
    print(f"  header n = {p.n}, squares parsed = {len(p.squares)}")
    print(f"  header side == claimed exact side: {p.side == side_claim}")
    up = ceil_print(p.side)
    print(f"  side = {decimal(p.side)}...; rounded up at 12 places {up}; "
          f"claimed print {claim['print']}: {'match' if up == claim['print'] else 'DIFFER'}")
    exhaustive = decide(p, exhaustive=True)
    a, b = exhaustive["route_a"], exhaustive["route_b"]
    assert isinstance(a, dict)
    assert isinstance(b, dict)
    print(f"  route A (every pair): accepted={a['accepted']} pairs={a['pairs_decided']}"
          f"/{a['pairs']} least gap {a['least_pair_gap_float']:.4e} at squares "
          f"{a['least_pair_gap_squares']}, least wall clearance "
          f"{a['least_wall_clearance_float']:.4e} (square "
          f"{a['least_wall_clearance_square']}), cpu {a['cpu_seconds']} s")
    print(f"  route B (pairs within the discs): accepted={b['accepted']} "
          f"pairs={b['pairs_decided']}/{b['pairs']}, least wall clearance "
          f"{b['least_wall_clearance_float']:.4e}, cpu {b['cpu_seconds']} s")
    ext = extent(p)
    print(f"  extent: side - tight side = {ext['side_minus_tight']:.4e}; "
          f"min x {ext['min_x']:.3e}, min y {ext['min_y']:.3e}")
    rows = controls(p)
    parse_rows = parse_controls(text)
    return {
        "n": n,
        "file": str(path.relative_to(PACKET)),
        "sha256": digest,
        "sha256_matches_manifest": digest == claim["sha256"],
        "comments": list(p.comments),
        "header_n": p.n,
        "squares": len(p.squares),
        "side": str(p.side),
        "side_decimal_40": decimal(p.side),
        "side_equals_claim": p.side == side_claim,
        "print_rounded_up_12": up,
        "print_claimed": claim["print"],
        "print_matches": up == claim["print"],
        "side_times_1e12_is_integer": (p.side * 10**12).denominator == 1,
        "extent": ext,
        "positive": exhaustive,
        "controls": rows,
        "parse_controls": parse_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--n", type=int, nargs="*", default=[268, 303])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    t0 = time.process_time()
    results = [check(n) for n in args.n]
    ok = all(
        r["sha256_matches_manifest"] and r["side_equals_claim"] and r["print_matches"]
        and r["positive"]["accepted"] and r["positive"]["routes_agree"]  # type: ignore[index]
        and all(c.get("met", True) for c in r["controls"])  # type: ignore[union-attr]
        and all(c["refused"] for c in r["parse_controls"])  # type: ignore[index]
        for r in results
    )
    receipt = {
        "program": "check_certificates.py",
        "python": sys.version.split()[0],
        "verdict": "all positives accepted and all controls met" if ok else "FAILED",
        "cpu_seconds_total": round(time.process_time() - t0, 2),
        "results": results,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(f"verdict: {receipt['verdict']}; cpu {receipt['cpu_seconds_total']} s; "
          f"receipt {args.out}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
