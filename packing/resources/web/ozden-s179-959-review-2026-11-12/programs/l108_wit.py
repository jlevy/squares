"""Witness/v2 files as 60-digit poses, for the after-freeze measurements; decides nothing.

Lane L108, blind stage 4 review of jlevy/squares#959. Written after the findings were
frozen. Reads corners (rational), center-basis (rational or algebraic-number-field) and
center-angle (decimal) witnesses into poses: centre, angle modulo 90 degrees in
(-45, 45], and the half-extent along x and y. For a number field it isolates the
generator by exact bisection in the file's isolating interval.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath
import yaml

mpmath.mp.dps = 60


@dataclass(frozen=True)
class Pose:
    cx: Any
    cy: Any
    deg: Any  # angle modulo 90 degrees, in (-45, 45]
    ex: Any  # half-extent along x: (|cos| + |sin|) / 2


@dataclass(frozen=True)
class Packing:
    name: str
    n: int
    side: Any
    side_exact: Fraction | None
    poses: list[Pose]


def _frac(text: str) -> Fraction:
    return Fraction(text)


def _poly_value(coeffs: list[Fraction], x: Fraction) -> Fraction:
    """Coefficients in increasing degree."""
    total = Fraction(0)
    for c in reversed(coeffs):
        total = total * x + c
    return total


def _generator(field: dict[str, Any]) -> Any:
    coeffs = [_frac(c) for c in field["minimal_polynomial"]]
    lo, hi = (_frac(v) for v in field["isolating_interval"])
    # The file does not say the coefficient order; take the one with a sign change.
    for order in (coeffs, list(reversed(coeffs))):
        if _poly_value(order, lo) * _poly_value(order, hi) < 0:
            break
    else:
        raise ValueError("no sign change in the isolating interval in either order")
    flo = _poly_value(order, lo)
    for _ in range(260):
        mid = (lo + hi) / 2
        fm = _poly_value(order, mid)
        if fm == 0:
            lo = hi = mid
            break
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return mpmath.mpf(lo.numerator) / lo.denominator


def _scalar(v: Any, t: Any) -> Any:
    if isinstance(v, list):
        total = mpmath.mpf(0)
        power = mpmath.mpf(1)
        for c in v:
            f = _frac(c)
            total += power * mpmath.mpf(f.numerator) / f.denominator
            power *= t
        return total
    f = _frac(str(v))
    return mpmath.mpf(f.numerator) / f.denominator


def _pose(cx: Any, cy: Any, c: Any, s: Any) -> Pose:
    deg = mpmath.degrees(mpmath.atan2(s, c))
    while deg > 45:
        deg -= 90
    while deg <= -45:
        deg += 90
    rad = mpmath.radians(deg)
    return Pose(cx=cx, cy=cy, deg=deg, ex=(abs(mpmath.cos(rad)) + abs(mpmath.sin(rad))) / 2)


def load(path: Path, name: str) -> Packing:
    w = yaml.safe_load(path.read_text(encoding="utf-8"))["witness"]
    kind = w["scalar"]["kind"]
    rep = w["representation"]
    t = _generator(w["scalar"]) if kind == "algebraic-number-field" else None
    side = _scalar(w["side"], t)
    side_exact = _frac(w["side"]) if kind == "rational" else None
    poses: list[Pose] = []
    for sq in w["squares"]:
        if rep == "corners":
            p = [(_scalar(x, t), _scalar(y, t)) for x, y in sq["corners"]]
            cx, cy = (p[0][0] + p[2][0]) / 2, (p[0][1] + p[2][1]) / 2
            poses.append(_pose(cx, cy, p[1][0] - p[0][0], p[1][1] - p[0][1]))
        elif rep == "center-basis":
            cx, cy = (_scalar(v, t) for v in sq["center"])
            c, s = (_scalar(v, t) for v in sq["basis"])
            poses.append(_pose(cx, cy, c, s))
        elif rep == "center-angle":
            assert w["coordinates"]["angle_unit"] == "degrees"
            cx, cy = (mpmath.mpf(v) for v in sq["center"])
            a = mpmath.radians(mpmath.mpf(sq["angle"]))
            poses.append(_pose(cx, cy, mpmath.cos(a), mpmath.sin(a)))
        else:
            raise ValueError(rep)
    return Packing(name=name, n=int(w["n"]), side=side, side_exact=side_exact, poses=poses)


def num(x: Any, digits: int = 6) -> str:
    return mpmath.nstr(x, digits, min_fixed=-3, max_fixed=4)
