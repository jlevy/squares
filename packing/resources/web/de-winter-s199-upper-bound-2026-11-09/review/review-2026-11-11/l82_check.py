"""L82 clean-room exact checker for unit-square packings (stage 4 review, 2026-11-11).

Written for this review before any producer code, or this repository's witness,
verifier or promotion code, was read. It imports nothing from either.

Two methods that share only the reader, which returns Python integers:

- method A: separating axes in fractions.Fraction, over the four edge normals of the
  pair, projecting all eight corners; the pair margin is the largest projected gap.
  margin > 0 clear, == 0 contact, < 0 interiors overlap.
- method B: exact clipping in gmpy2.mpq (Sutherland-Hodgman against the closed
  half-planes of the other square) and the shoelace area of the clipped polygon.
  empty -> clear, nonempty with area 0 -> contact, area > 0 -> overlap.

Every square, every wall and every pair is decided; there is no distance filter.

MUTANT (module global) deliberately breaks one method for the mutant run only.
"""

from __future__ import annotations

import json
import math
import re
from fractions import Fraction

import gmpy2
import yaml

MUTANT = ""

_RAT = re.compile(r"^(-?)(0|[1-9][0-9]*)(?:/([1-9][0-9]*))?$")


class ReadError(ValueError):
    pass


# ---------------------------------------------------------------- reader


def parse_rat(x: object) -> tuple[int, int]:
    """Exact rational as (p, q), q > 0, in lowest terms. Fails closed."""
    if isinstance(x, bool):
        raise ReadError(f"boolean scalar {x!r}")
    if isinstance(x, int):
        return (x, 1)
    if not isinstance(x, str):
        raise ReadError(f"scalar of type {type(x).__name__}: {x!r}")
    m = _RAT.match(x.strip())
    if not m or x != x.strip():
        raise ReadError(f"not a rational literal: {x[:60]!r}")
    sign, p, q = m.group(1), int(m.group(2)), int(m.group(3) or 1)
    if sign and p == 0:
        raise ReadError("negative zero")
    if math.gcd(p, q) != 1:
        raise ReadError(f"not in lowest terms: {x[:60]!r}")
    return (-p if sign else p, q)


def _square_from_corners(cs: list) -> tuple:
    """Convert four exact corners to (cx, cy, c, s); refuse unless a unit square."""
    if not isinstance(cs, list) or len(cs) != 4:
        raise ReadError("corners must be a list of four points")
    pts = []
    for p in cs:
        if not isinstance(p, list) or len(p) != 2:
            raise ReadError("corner must be [x, y]")
        pts.append(tuple(Fraction(*parse_rat(v)) for v in p))
    e = [(pts[(k + 1) % 4][0] - pts[k][0], pts[(k + 1) % 4][1] - pts[k][1]) for k in range(4)]
    for k in range(4):
        if e[k][0] ** 2 + e[k][1] ** 2 != 1:
            raise ReadError("corner edge not of unit length")
        if e[k][0] * e[(k + 1) % 4][0] + e[k][1] * e[(k + 1) % 4][1] != 0:
            raise ReadError("corner edges not perpendicular")
    cx = (pts[0][0] + pts[2][0]) / 2
    cy = (pts[0][1] + pts[2][1]) / 2
    c, s = e[0]
    return tuple((v.numerator, v.denominator) for v in (cx, cy, c, s))


def _pack(n: int, side: tuple, squares: list) -> dict:
    if len(squares) != n:
        raise ReadError(f"{len(squares)} squares, n = {n}")
    if side[0] <= 0:
        raise ReadError("side not positive")
    return {"n": n, "side": side, "squares": squares}


def read_witness_yaml(path: str) -> dict:
    """Witness/v2 rational file, center-basis or corners. Fails closed."""
    with open(path, encoding="utf-8") as fh:
        doc = yaml.load(fh, Loader=yaml.CSafeLoader)
    if not isinstance(doc, dict) or "witness" not in doc:
        raise ReadError("no top-level witness")
    w = doc["witness"]
    n = w.get("n")
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ReadError("bad n")
    if str(w.get("square_size")) != "1":
        raise ReadError("square_size is not 1")
    if (w.get("scalar") or {}).get("kind") != "rational":
        raise ReadError("scalar kind is not rational")
    rep = w.get("representation")
    if rep not in ("center-basis", "corners"):
        raise ReadError(f"representation {rep!r} not handled")
    side = parse_rat(w.get("side"))
    sq = w.get("squares")
    if not isinstance(sq, list):
        raise ReadError("squares not a list")
    out = []
    for k, e in enumerate(sq, start=1):
        if not isinstance(e, dict) or e.get("id") != k:
            raise ReadError(f"square {k}: id out of order or missing")
        if rep == "center-basis":
            if set(e) != {"id", "center", "basis"}:
                raise ReadError(f"square {k}: keys {sorted(e)}")
            c, b = e["center"], e["basis"]
            if not (isinstance(c, list) and isinstance(b, list) and len(c) == 2 and len(b) == 2):
                raise ReadError(f"square {k}: center/basis shape")
            out.append(tuple(parse_rat(v) for v in (*c, *b)))
        else:
            if set(e) != {"id", "corners"}:
                raise ReadError(f"square {k}: keys {sorted(e)}")
            out.append(_square_from_corners(e["corners"]))
    return _pack(n, side, out)


def read_author_json(path: str) -> dict:
    """The author's [cx, cy, cos, sin] JSON twin. Fails closed."""
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    n = doc.get("n")
    if not isinstance(n, int) or isinstance(n, bool):
        raise ReadError("bad n")
    if doc.get("square_size") != "1":
        raise ReadError("square_size is not 1")
    side = parse_rat(doc.get("side"))
    out = []
    for k, e in enumerate(doc.get("squares") or [], start=1):
        if not isinstance(e, list) or len(e) != 4:
            raise ReadError(f"square {k}: not four scalars")
        out.append(tuple(parse_rat(v) for v in e))
    return _pack(n, side, out)


# ---------------------------------------------------------------- method A


def _corners_a(sq):
    cx, cy, c, s = (Fraction(*v) for v in sq)
    h = Fraction(1, 2)
    return [
        (cx + h * (c - s), cy + h * (s + c)),
        (cx + h * (-c - s), cy + h * (-s + c)),
        (cx + h * (-c + s), cy + h * (-s - c)),
        (cx + h * (c + s), cy + h * (s - c)),
    ]


def unit_a(sq) -> bool:
    if MUTANT == "no_unit_check":
        return True
    c, s = Fraction(*sq[2]), Fraction(*sq[3])
    return c * c + s * s == 1


def pair_margin_a(sqi, sqj, ci=None, cj=None) -> Fraction:
    ci = ci or _corners_a(sqi)
    cj = cj or _corners_a(sqj)
    axes = []
    for sq in (sqi, sqj) if MUTANT != "one_axes" else (sqi,):
        c, s = Fraction(*sq[2]), Fraction(*sq[3])
        axes += [(c, s), (-s, c)]
    best = None
    for wx, wy in axes:
        pi = [wx * x + wy * y for x, y in ci]
        pj = [wx * x + wy * y for x, y in cj]
        g = max(min(pj) - max(pi), min(pi) - max(pj))
        if best is None or g > best:
            best = g
    return best


def wall_clearances_a(sq, side: Fraction, cs=None) -> tuple:
    cs = cs or _corners_a(sq)
    xs = [p[0] for p in cs]
    ys = [p[1] for p in cs]
    return (min(xs), min(ys), side - max(xs), side - max(ys))  # left, bottom, right, top


# ---------------------------------------------------------------- method B


def _q(v):
    return gmpy2.mpq(v[0], v[1])


def _corners_b(sq):
    cx, cy, c, s = (_q(v) for v in sq)
    h = gmpy2.mpq(1, 2)
    out = []
    for a, b in ((h, h), (-h, h), (-h, -h), (h, -h)):
        out.append((cx + a * c - b * s, cy + a * s + b * c))
    return out


def _area2(poly) -> gmpy2.mpq:
    n = len(poly)
    acc = gmpy2.mpq(0)
    for k in range(n):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % n]
        acc += x0 * y1 - x1 * y0
    return acc


def _clip(poly, a, b):
    ex, ey = b[0] - a[0], b[1] - a[1]
    out = []
    n = len(poly)
    for k in range(n):
        p, q = poly[k], poly[(k + 1) % n]
        fp = ex * (p[1] - a[1]) - ey * (p[0] - a[0])
        fq = ex * (q[1] - a[1]) - ey * (q[0] - a[0])
        keep = fp > 0 if MUTANT == "open_halfplanes" else fp >= 0
        if keep:
            out.append(p)
        if (fp > 0 > fq) or (fp < 0 < fq):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def clip_convex(poly, conv):
    """poly clipped by the closed CCW convex polygon conv."""
    out = list(poly)
    m = len(conv)
    for k in range(m):
        if not out:
            break
        out = _clip(out, conv[k], conv[(k + 1) % m])
    return out


def unit_b(sq) -> bool:
    if MUTANT == "no_unit_check":
        return True
    p = _corners_b(sq)
    e = [(p[(k + 1) % 4][0] - p[k][0], p[(k + 1) % 4][1] - p[k][1]) for k in range(4)]
    ok = all(x * x + y * y == 1 for x, y in e)
    ok = ok and all(e[k][0] * e[(k + 1) % 4][0] + e[k][1] * e[(k + 1) % 4][1] == 0 for k in range(4))
    return ok and _area2(p) == 2


def pair_class_b(pi, pj) -> tuple[str, gmpy2.mpq]:
    inter = clip_convex(pi, pj)
    if not inter:
        return ("clear", gmpy2.mpq(0))
    area = abs(_area2(inter)) / 2
    if area == 0:
        return ("overlap" if MUTANT == "gap0_overlap" else "contact", area)
    return ("overlap", area)


def inside_b(p, side) -> bool:
    z = gmpy2.mpq(0)
    box = [(z, z), (side, z), (side, side), (z, side)]
    clipped = clip_convex(p, box)
    return bool(clipped) and abs(_area2(clipped)) == abs(_area2(p))


# ---------------------------------------------------------------- decide


def classify_margin(m: Fraction) -> str:
    if m > 0:
        return "clear"
    if m == 0:
        return "overlap" if MUTANT == "gap0_overlap" else "contact"
    return "overlap"


def decide(pk: dict, side=None, thresholds=(Fraction(1, 10**12), Fraction(1, 10**90), Fraction(1, 10**300))) -> dict:
    """Decide a packing exactly by both methods. Returns a JSON-able receipt."""
    sqs = pk["squares"]
    n = len(sqs)
    S = Fraction(*pk["side"]) if side is None else Fraction(side)
    Sq = gmpy2.mpq(S.numerator, S.denominator)
    ca = [_corners_a(s) for s in sqs]
    cb = [_corners_b(s) for s in sqs]
    r: dict = {"n": n, "side": f"{S.numerator}/{S.denominator}"}
    r["not_unit_a"] = [k + 1 for k in range(n) if not unit_a(sqs[k])]
    r["not_unit_b"] = [k + 1 for k in range(n) if not unit_b(sqs[k])]
    outside_a, walls, least_wall = [], [], None
    for k in range(n):
        cl = wall_clearances_a(sqs[k], S, ca[k])
        if min(cl) < 0:
            outside_a.append(k + 1)
        for name, v in zip(("left", "bottom", "right", "top"), cl):
            if v == 0:
                walls.append([k + 1, name])
            elif v > 0 and (least_wall is None or v < least_wall[0]):
                least_wall = (v, k + 1, name)
    r["outside_a"] = outside_a
    r["outside_b"] = [k + 1 for k in range(n) if not inside_b(cb[k], Sq)]
    r["wall_contacts"] = walls
    r["least_positive_wall_clearance"] = (
        None if least_wall is None else [f"{float(least_wall[0]):.6e}", least_wall[1], least_wall[2]]
    )
    touch, over, disagree = [], [], []
    least = None
    below = [0] * len(thresholds)
    for i in range(n):
        for j in range(i + 1, n):
            m = pair_margin_a(sqs[i], sqs[j], ca[i], ca[j])
            ka = classify_margin(m)
            kb, area = pair_class_b(cb[i], cb[j])
            if ka != kb:
                disagree.append([i + 1, j + 1, ka, kb])
            if ka == "contact":
                touch.append([i + 1, j + 1])
            elif ka == "overlap":
                over.append([i + 1, j + 1, f"{float(m):.6e}", f"{float(area):.6e}"])
            else:
                if least is None or m < least[0]:
                    least = (m, i + 1, j + 1)
                for t, th in enumerate(thresholds):
                    if m < th:
                        below[t] += 1
    r["pairs"] = n * (n - 1) // 2
    r["touching_pairs"] = touch
    r["overlapping_pairs"] = over
    r["method_disagreements"] = disagree
    r["least_positive_margin"] = None if least is None else [_sci(least[0]), least[1], least[2]]
    r["least_positive_margin_exact"] = None if least is None else f"{least[0].numerator}/{least[0].denominator}"
    r["positive_margins_below"] = {f"1e-{_exp(th)}": c for th, c in zip(thresholds, below)}
    ok = not (
        r["not_unit_a"] or r["not_unit_b"] or outside_a or r["outside_b"] or over or disagree
    )
    r["verdict"] = "ACCEPT" if ok else "REFUSE"
    return r


def _exp(th: Fraction) -> int:
    return len(str(th.denominator)) - 1


def _sci(x: Fraction, digits: int = 12) -> str:
    """Decimal scientific print of an exact rational, correct at any magnitude."""
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    x = abs(x)
    e = len(str(x.numerator)) - len(str(x.denominator))
    while x >= Fraction(10) ** e:
        e += 1
    while x < Fraction(10) ** (e - 1):
        e -= 1
    mant = x / Fraction(10) ** (e - 1)
    m = mant * 10 ** (digits - 1)
    q = m.numerator // m.denominator
    s = str(q)
    return f"{sign}{s[0]}.{s[1:]}e{e - 1:+d}"


def sci(x, digits: int = 12) -> str:
    return _sci(Fraction(x), digits)


def decimal_floor(x: Fraction, places: int) -> str:
    q = (x.numerator * 10**places) // x.denominator
    s = str(abs(q)).rjust(places + 1, "0")
    return ("-" if q < 0 else "") + s[:-places] + "." + s[-places:]


def decimal_ceil(x: Fraction, places: int) -> str:
    q = -((-x.numerator * 10**places) // x.denominator)
    s = str(abs(q)).rjust(places + 1, "0")
    return ("-" if q < 0 else "") + s[:-places] + "." + s[-places:]
