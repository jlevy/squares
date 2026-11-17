#!/usr/bin/env python3
"""sqcheck: decide whether n unit squares fit, with disjoint interiors, in the square [0, s]^2.

Written from scratch for Doğa's lab (2026-11-02); it shares no code with the Squares Project's checkers.

Arithmetic, chosen by the witness:
  exact-rational   every coordinate is a rational; every sign is decided exactly (touching = allowed).
  exact-algebraic  coordinates live in Q(alpha), alpha a root of an irreducible polynomial isolated by a
                   rational interval; zero is decided symbolically, nonzero signs by exact rational
                   interval refinement.
  interval         some angle is a decimal (cos/sin are not rational); mpmath interval arithmetic with
                   outward rounding. A tight packing cannot be decided at its own side, so the verdict is a
                   CERTIFIED UPPER BOUND s*(1+lambda): the centres are dilated by (1+lambda) about the
                   origin, which turns every tight contact strict (pair margins grow by >= lambda*R >= lambda,
                   wall margins by >= lambda/2) while leaving the squares unit and their angles unchanged.

Geometry: square i has centre c_i and orthonormal frame (u_i, v_i). Containment: c_x - (|u_x|+|v_x|)/2 >= 0 and
c_x + (|u_x|+|v_x|)/2 <= s, same for y. Disjoint interiors of two convex polygons <=> some edge normal of either
(u_i, v_i, u_j, v_j) separates them (closed half-planes): |dc.a| >= 1/2 + (|u_k.a|+|v_k.a|)/2 for a from square
i's frame and k = j (and symmetrically). If all four margins are strictly negative, the interiors overlap.

Input: a witness file in the Squares Project's Witness/v2 layout (YAML or JSON): representation corners |
center-angle | center-basis; scalar kind rational | decimal | algebraic-number-field. Our own finders write the
same layout (center-angle with angle_unit radians or degrees, decimal or rational strings).

Exit code 0 = VALID (exact) or CERTIFIED (interval, bound printed); 1 = INVALID (a violation was proved);
2 = UNDECIDED; 3 = malformed input.
"""
from __future__ import annotations

import argparse
import json
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import mpmath
import yaml
from mpmath import iv

sys.set_int_max_str_digits(0)

HALF = Fraction(1, 2)


class Malformed(Exception):
    pass


@contextmanager
def iv_digits(digits: int):
    saved = iv.prec
    iv.dps = digits
    try:
        yield
    finally:
        iv.prec = saved


# ---------------------------------------------------------------- algebraic number field Q(alpha)

class NumberField:
    def __init__(self, minpoly_desc: list[str], interval: list[str]):
        import sympy

        coeffs = [Fraction(c) for c in minpoly_desc]  # highest degree first
        if coeffs[0] == 0:
            raise Malformed("minimal polynomial has zero leading coefficient")
        self.monic = [c / coeffs[0] for c in coeffs]  # x^d + m[1] x^{d-1} + ... + m[d]
        self.d = len(coeffs) - 1
        x = sympy.symbols("x")
        poly = sympy.Poly([sympy.Rational(c.numerator, c.denominator) for c in coeffs], x, domain="QQ")
        if not poly.is_irreducible:
            raise Malformed("minimal polynomial is reducible over Q; exact zero test would be unsound")
        self.lo, self.hi = Fraction(interval[0]), Fraction(interval[1])
        nroots = poly.count_roots(sympy.Rational(self.lo.numerator, self.lo.denominator),
                                  sympy.Rational(self.hi.numerator, self.hi.denominator))
        if nroots != 1:
            raise Malformed(f"isolating interval holds {nroots} roots of the minimal polynomial, not 1")
        if self._p(self.lo) == 0 or self._p(self.hi) == 0:
            raise Malformed("isolating interval endpoint is a root")
        self.sign_lo = self._p(self.lo) > 0

    def _p(self, t: Fraction) -> Fraction:
        acc = Fraction(0)
        for c in self.monic:
            acc = acc * t + c
        return acc

    def refine(self):
        mid = (self.lo + self.hi) / 2
        pm = self._p(mid)
        if pm == 0:
            self.lo = self.hi = mid
        elif (pm > 0) == self.sign_lo:
            self.lo = mid
        else:
            self.hi = mid

    def elem(self, raw) -> "FieldElem":
        if isinstance(raw, list):
            cs = [Fraction(c) for c in raw]
            if len(cs) > self.d:
                raise Malformed("field element has more coefficients than the field degree")
        else:
            cs = [Fraction(raw)]
        return FieldElem(self, tuple(cs + [Fraction(0)] * (self.d - len(cs))))


@dataclass(frozen=True)
class FieldElem:
    K: NumberField
    c: tuple  # ascending powers of alpha

    def _lift(self, o):
        if isinstance(o, FieldElem):
            return o
        return FieldElem(self.K, (Fraction(o),) + (Fraction(0),) * (self.K.d - 1))

    def __add__(self, o):
        o = self._lift(o)
        return FieldElem(self.K, tuple(a + b for a, b in zip(self.c, o.c)))

    __radd__ = __add__

    def __neg__(self):
        return FieldElem(self.K, tuple(-a for a in self.c))

    def __sub__(self, o):
        return self + (-self._lift(o))

    def __rsub__(self, o):
        return self._lift(o) - self

    def __mul__(self, o):
        o = self._lift(o)
        d = self.K.d
        prod = [Fraction(0)] * (2 * d - 1)
        for i, a in enumerate(self.c):
            if a:
                for j, b in enumerate(o.c):
                    if b:
                        prod[i + j] += a * b
        m = self.K.monic  # alpha^d = -(m[1] alpha^{d-1} + ... + m[d])
        for k in range(2 * d - 2, d - 1, -1):
            t = prod[k]
            if t:
                prod[k] = Fraction(0)
                for r in range(1, d + 1):
                    prod[k - r] -= t * m[r]
        return FieldElem(self.K, tuple(prod[:d]))

    __rmul__ = __mul__

    def _bounds(self):
        lo, hi = self.K.lo, self.K.hi
        acc_lo = acc_hi = Fraction(0)
        for c in reversed(self.c):  # Horner over the rational interval [lo, hi]
            cands = [acc_lo * lo, acc_lo * hi, acc_hi * lo, acc_hi * hi]
            acc_lo, acc_hi = min(cands) + c, max(cands) + c
        return acc_lo, acc_hi

    def sign(self) -> int:
        if not any(self.c):
            return 0
        for _ in range(4000):
            a, b = self._bounds()
            if a > 0:
                return 1
            if b < 0:
                return -1
            self.K.refine()
        raise RuntimeError("sign refinement did not converge")

    def approx(self) -> float:
        a, b = self._bounds()
        while b - a > Fraction(1, 10 ** 18) * (1 + abs(a)):
            self.K.refine()
            a, b = self._bounds()
        return float((a + b) / 2)


# ---------------------------------------------------------------- arithmetic-agnostic helpers

def sign(x):
    """+1, -1, 0, or None (interval straddling zero)."""
    if isinstance(x, Fraction) or isinstance(x, int):
        return (x > 0) - (x < 0)
    if isinstance(x, FieldElem):
        return x.sign()
    if x.a > 0:
        return 1
    if x.b < 0:
        return -1
    if x.a == 0 and x.b == 0:
        return 0
    return None


def absval(x):
    if isinstance(x, (Fraction, int, FieldElem)):
        return x if sign(x) >= 0 else -x
    return abs(x)


def approx(x) -> float:
    if isinstance(x, FieldElem):
        return x.approx()
    if isinstance(x, (Fraction, int)):
        return float(x)
    return float(x.mid)


@dataclass
class Sq:
    cx: object
    cy: object
    ux: object
    uy: object  # u = (ux, uy) unit; v = (-uy, ux)


# ---------------------------------------------------------------- witness parsing

def load(path: Path):
    text = path.read_text()
    doc = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    w = doc.get("witness", doc)
    for key in ("n", "side", "representation", "scalar", "squares"):
        if key not in w:
            raise Malformed(f"witness lacks '{key}'")
    if str(w.get("square_size", "1")) != "1":
        raise Malformed("square_size must be 1")
    return w


def build(w, prec_digits: int):
    kind = w["scalar"]["kind"]
    rep = w["representation"]
    unit = (w.get("coordinates") or {}).get("angle_unit", "degrees")
    if kind == "rational":
        num, mode = (lambda r: Fraction(str(r))), "exact-rational"
    elif kind == "algebraic-number-field":
        K = NumberField([str(c) for c in w["scalar"]["minimal_polynomial"]],
                        [str(c) for c in w["scalar"]["isolating_interval"]])
        num, mode = K.elem, "exact-algebraic"
    elif kind == "decimal":
        if rep == "center-angle":
            num, mode = (lambda r: Fraction(str(r))), "interval"
        else:
            raise Malformed("decimal coordinates are only accepted with center-angle")
    else:
        raise Malformed(f"unsupported scalar kind {kind}")
    side = num(w["side"])
    squares: list[Sq] = []
    problems: list[str] = []
    for k, s in enumerate(w["squares"]):
        if rep == "center-angle":
            cx, cy = (num(v) for v in s["center"])
            ang = Fraction(str(s["angle"]))
            quarter = Fraction(90) if unit == "degrees" else None
            if ang == 0 or (quarter and ang % quarter == 0):
                ux, uy = Fraction(1), Fraction(0)  # frame of a square is invariant under quarter turns
            else:
                mode = "interval"
                with iv_digits(prec_digits + 10):
                    a = iv.mpf(ang.numerator) / iv.mpf(ang.denominator)
                    if unit == "degrees":
                        a = a * iv.pi / 180
                    elif unit != "radians":
                        raise Malformed(f"angle_unit {unit}")
                    ux, uy = iv.cos(a), iv.sin(a)
            squares.append(Sq(cx, cy, ux, uy))
        elif rep == "center-basis":
            cx, cy = (num(v) for v in s["center"])
            ux, uy = (num(v) for v in s["basis"])
            norm = ux * ux + uy * uy - 1
            if sign(norm) != 0:
                problems.append(f"square {k + 1}: basis is not unit length")
            squares.append(Sq(cx, cy, ux, uy))
        elif rep == "corners":
            p = [(num(a), num(b)) for a, b in s["corners"]]
            ex, ey = p[1][0] - p[0][0], p[1][1] - p[0][1]
            fx, fy = p[3][0] - p[0][0], p[3][1] - p[0][1]
            ok = (sign(ex * ex + ey * ey - 1) == 0 and sign(fx * fx + fy * fy - 1) == 0
                  and sign(ex * fx + ey * fy) == 0
                  and sign(p[2][0] - (p[0][0] + ex + fx)) == 0 and sign(p[2][1] - (p[0][1] + ey + fy)) == 0)
            if not ok:
                problems.append(f"square {k + 1}: corners are not a unit square")
            squares.append(Sq(p[0][0] + (ex + fx) * HALF, p[0][1] + (ey + fy) * HALF, ex, ey))
        else:
            raise Malformed(f"unsupported representation {rep}")
    if len(squares) != int(w["n"]):
        problems.append(f"witness lists {len(squares)} squares, claims n = {w['n']}")
    return side, squares, mode, problems


# ---------------------------------------------------------------- the check

def to_iv(x):
    if isinstance(x, Fraction):
        return iv.mpf(x.numerator) / iv.mpf(x.denominator)
    return x


def check(side, squares: list[Sq], interval: bool, dilation: Fraction = Fraction(0)):
    """Returns (violations, undecided, min_wall_margin, min_pair_margin)."""
    conv = to_iv if interval else (lambda x: x)
    f = conv(1 + dilation)
    s = conv(side) * f
    sq = [Sq(conv(q.cx) * f, conv(q.cy) * f, conv(q.ux), conv(q.uy)) for q in squares]
    half = conv(HALF)
    violations, undecided = [], []
    min_wall, min_pair = float("inf"), float("inf")
    hw = []
    for k, q in enumerate(sq):
        hx = (absval(q.ux) + absval(q.uy)) * half  # |u_x| + |v_x| with v = (-u_y, u_x)
        hw.append(hx)
        for name, m in (("left", q.cx - hx), ("right", s - q.cx - hx), ("bottom", q.cy - hx), ("top", s - q.cy - hx)):
            g = sign(m)
            min_wall = min(min_wall, approx(m))
            if g is None:
                undecided.append(f"square {k + 1} {name} wall")
            elif g < 0:
                violations.append(f"square {k + 1} crosses the {name} wall by {-approx(m):.3e}")
    two = conv(Fraction(2))
    for i in range(len(sq)):
        a = sq[i]
        for j in range(i + 1, len(sq)):
            b = sq[j]
            dx, dy = b.cx - a.cx, b.cy - a.cy
            far = sign(dx * dx + dy * dy - two)
            if far is not None and far > 0:
                continue  # centres farther than sqrt(2) = sum of circumradii
            margins = []
            for own, other in ((a, b), (b, a)):
                for ax, ay in ((own.ux, own.uy), (-own.uy, own.ux)):
                    proj = absval(dx * ax + dy * ay)
                    ext = (absval(other.ux * ax + other.uy * ay) + absval(-other.uy * ax + other.ux * ay)) * half
                    margins.append(proj - half - ext)
            signs = [sign(m) for m in margins]
            best = max(approx(m) for m in margins)
            min_pair = min(min_pair, best)
            if any(g is not None and g >= 0 for g in signs):
                continue
            if all(g is not None and g < 0 for g in signs):
                violations.append(f"squares {i + 1} and {j + 1} overlap (best separating margin {best:.3e})")
            else:
                undecided.append(f"squares {i + 1} and {j + 1}")
    return violations, undecided, min_wall, min_pair


def verify(path: Path, prec_digits: int = 60, quiet: bool = False):
    w = load(path)
    with iv_digits(prec_digits):
        side, squares, mode, problems = build(w, prec_digits)
        result = {"file": str(path), "n": int(w["n"]), "mode": mode, "side": approx(side)}
        if problems:
            result.update(verdict="INVALID", reasons=problems)
            return result, 1
        return decide(side, squares, mode, result)


def ceil_decimal(x, places=15):
    """Decimal string of x rounded UP at `places` decimals, or None when x is not an exact Fraction."""
    if not isinstance(x, Fraction):
        return None
    scale = 10 ** places
    q = -((-x.numerator * scale) // x.denominator)
    sign = "-" if q < 0 else ""
    q = abs(q)
    return f"{sign}{q // scale}.{q % scale:0{places}d}"


def decide(side, squares, mode, result):
    """Exact modes: VALID/INVALID. Interval mode: CERTIFIED (possibly via dilation)/INVALID/UNDECIDED."""
    if True:
        interval = mode == "interval"
        v, u, mw, mp = check(side, squares, interval)
        result.update(min_wall_margin=mw, min_pair_margin=mp)
        if v and not interval:
            result.update(verdict="INVALID", reasons=v[:20], violations=len(v))
            return result, 1
        if not u and not v:
            result.update(verdict="VALID" if not interval else "CERTIFIED", certified_side=approx(side), certified_side_upper=ceil_decimal(side),
                          certified_side_exact=str(side) if isinstance(side, Fraction) and len(str(side)) < 200 else None)
            return result, 0
        for exp in (24, 20, 16, 13, 10):
            lam = Fraction(1, 10 ** exp)
            v2, u2, _, _ = check(side, squares, True, lam)
            if not v2 and not u2:
                bound = side * (1 + lam)
                result.update(verdict="CERTIFIED", dilation=f"1e-{exp}", undecided_at_own_side=len(u) + len(v),
                              worst_violation_at_own_side=-min(mw, mp, 0.0),
                              certified_side=approx(bound), certified_side_upper=ceil_decimal(bound),
                              certified_side_exact=str(bound) if isinstance(bound, Fraction) and len(str(bound)) < 200 else None)
                return result, 0
        if v:
            result.update(verdict="INVALID", reasons=v[:20], violations=len(v),
                          note="interval mode: violations persist under every dilation up to 1e-10")
            return result, 1
        result.update(verdict="UNDECIDED", undecided=u[:20])
        return result, 2


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("witness", nargs="+", type=Path)
    ap.add_argument("--dps", type=int, default=60, help="interval working precision in decimal digits")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    worst = 0
    for p in args.witness:
        try:
            res, code = verify(p, args.dps)
        except (Malformed, KeyError, ValueError, ZeroDivisionError) as e:
            res, code = {"file": str(p), "verdict": "MALFORMED", "reasons": [f"{type(e).__name__}: {e}"]}, 3
        worst = max(worst, code)
        if args.json:
            print(json.dumps(res))
        else:
            extra = ((f" s<={res['certified_side_upper']} (exact side rounded up)" if res.get("certified_side_upper")
                      else f" s~{res['certified_side']:.15f} (binary64 approximation)") if "certified_side" in res else "")
            dil = (f" (dilation {res['dilation']}; at own side {res['undecided_at_own_side']} tight constraints,"
                   f" worst {res['worst_violation_at_own_side']:.1e})") if "dilation" in res else ""
            print(f"{res['verdict']:9} n={res.get('n', '?'):<4} {res.get('mode', ''):15}{extra}{dil}  {p.name}")
            for r in res.get("reasons", [])[:5]:
                print(f"           {r}")
    sys.exit(worst)


if __name__ == "__main__":
    main()
