"""Read center-basis Witness/v2 files: rational exactly, algebraic as mpmath values (review L83).

A center-basis square is centre c and basis (cos, sin) = u; its corners are
c - u/2 - v/2, c + u/2 - v/2, c + u/2 + v/2, c - u/2 + v/2 with v = perp(u).
The rational reader insists that u.u = 1 exactly.
"""

from __future__ import annotations

import gzip
from fractions import Fraction
from pathlib import Path

import mpmath

import l83_reader as R


def _tree(path: Path):
    raw = path.read_bytes()
    if path.suffix == ".gz":
        raw = gzip.decompress(raw)
    return R.compose_yaml(raw.decode("utf-8"))


def _q(text) -> Fraction:
    return Fraction(*R.parse_scalar(text))


def read_rational(path: Path):
    """(n, side, ids, centres, bases) as Fractions; refuses anything but rational center-basis."""
    w = _tree(path)["witness"]
    if w["representation"] != "center-basis" or w["scalar"] != {"kind": "rational"}:
        raise R.Refused("not a rational center-basis witness")
    if w["coordinates"]["origin"] != "lower-left" or w["square_size"] != "1":
        raise R.Refused("origin or size")
    n = int(w["n"])
    side = _q(w["side"])
    ids, cs, us = [], [], []
    for sq in w["squares"]:
        c = (_q(sq["center"][0]), _q(sq["center"][1]))
        u = (_q(sq["basis"][0]), _q(sq["basis"][1]))
        if u[0] * u[0] + u[1] * u[1] != 1:
            raise R.Refused(f"basis of {sq['id']} not a unit vector")
        ids.append(sq["id"])
        cs.append(c)
        us.append(u)
    if len(ids) != n:
        raise R.Refused("count")
    return n, side, ids, cs, us


def corners(c, u):
    (cx, cy), (ux, uy) = c, u
    vx, vy = -uy, ux
    p0 = (cx - ux / 2 - vx / 2, cy - uy / 2 - vy / 2)
    return [p0, (p0[0] + ux, p0[1] + uy), (p0[0] + ux + vx, p0[1] + uy + vy), (p0[0] + vx, p0[1] + vy)]


def read_float(path: Path, dps: int = 40):
    """(n, side, centres, angles in degrees) as mpmath values, for rational or algebraic witnesses."""
    mpmath.mp.dps = dps
    w = _tree(path)["witness"]
    kind = w["scalar"]["kind"]
    if kind == "rational":
        val = lambda t: mpmath.mpf(_q(t).numerator) / _q(t).denominator  # noqa: E731
    elif kind == "algebraic-number-field":
        poly = [int(_q(c)) for c in w["scalar"]["minimal_polynomial"]]
        lo, hi = (_q(t) for t in w["scalar"]["isolating_interval"])
        a = mpmath.mpf(lo.numerator) / lo.denominator
        b = mpmath.mpf(hi.numerator) / hi.denominator
        # the polynomial is listed lowest degree first or highest first; take the one with a sign change
        def f(x, p):
            return sum(mpmath.mpf(c) * x**k for k, c in enumerate(p))
        p = poly if f(a, poly) * f(b, poly) < 0 else list(reversed(poly))
        if f(a, p) * f(b, p) >= 0:
            raise R.Refused("no sign change on the isolating interval")
        for _ in range(dps * 4):
            m = (a + b) / 2
            if f(a, p) * f(m, p) <= 0:
                b = m
            else:
                a = m
        alpha = (a + b) / 2

        def val(t):
            if isinstance(t, list):
                return sum((mpmath.mpf(_q(c).numerator) / _q(c).denominator) * alpha**k for k, c in enumerate(t))
            return mpmath.mpf(_q(t).numerator) / _q(t).denominator
    else:
        raise R.Refused(f"scalar kind {kind}")
    side = val(w["side"])
    cs, angs = [], []
    for sq in w["squares"]:
        cs.append((val(sq["center"][0]), val(sq["center"][1])))
        if "basis" in sq:
            ux, uy = val(sq["basis"][0]), val(sq["basis"][1])
            angs.append(mpmath.degrees(mpmath.atan2(uy, ux)))
        else:
            angs.append(val(sq["angle"]))
    return int(w["n"]), side, cs, angs
