"""The crate's axis vertex sweep, emulated at one column in binary64 with its own rounding.

Usage: ``python3 -I sweep_emulation.py CANDIDATE.json FACTOR X Y [CRATE_BOUND]``

``X`` and ``Y`` are the exact rationals of the sweep's reported ``argmin``; ``FACTOR``
scales every mass (``1`` for the original, ``99/100`` for the census control's mutant).
The program rebuilds the event grid and the column of ``X`` as ``packing/sqverify_fast/
src/axis.rs`` does, with the directed steps of ``interval.rs`` (lemma I1: ``dn(x) = x -
(|x| 2^-52 + 2^-1074)``) written here in Python floats, and prints the enclosure the
sweep certifies at ``Y``, its width, the least lower end over the column, the exact
capture at the vertex recomputed in fractions, and the sum of the outward steps the
column took. A match with ``CRATE_BOUND`` to the last digit says the emulation walked the
crate's path; the width is what a tolerance on the axis row would have to cover. It
decides nothing.
"""

from __future__ import annotations

import bisect
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fine_net_exact as exact

GAP = 2.0**-52
TINY = 5e-324
#: The outward steps taken so far, summed exactly: part of where a width comes from.
STEPS = {"count": 0, "total": Fraction(0)}


def dn(x: float) -> float:
    step = abs(x) * GAP + TINY
    STEPS["count"] += 1
    STEPS["total"] += Fraction(step)
    return x - step


def up(x: float) -> float:
    step = abs(x) * GAP + TINY
    STEPS["count"] += 1
    STEPS["total"] += Fraction(step)
    return x + step


def fmin(a: float, b: float) -> float:
    return (min(b, a)) + a * 0.0


def fmax(a: float, b: float) -> float:
    return (max(b, a)) + a * 0.0


class Iv:
    """A closed interval of binary64 endpoints, as ``interval.rs`` keeps it."""

    __slots__ = ("hi", "lo")

    def __init__(self, lo: float, hi: float) -> None:
        self.lo, self.hi = lo, hi

    def plus(self, other: Iv) -> Iv:
        return Iv(dn(self.lo + other.lo), up(self.hi + other.hi))

    def minus(self, other: Iv) -> Iv:
        return Iv(dn(self.lo - other.hi), up(self.hi - other.lo))

    def times(self, other: Iv) -> Iv:
        a, b, c, d = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Iv(dn(fmin(fmin(a, b), fmin(c, d))), up(fmax(fmax(a, b), fmax(c, d))))

    def mul_nonneg(self, k: Iv) -> Iv:
        lo = self.lo * k.lo if self.lo >= 0.0 else self.lo * k.hi
        hi = self.hi * k.hi if self.hi >= 0.0 else self.hi * k.lo
        return Iv(dn(lo), up(hi))

    def min(self, other: Iv) -> Iv:
        return Iv(fmin(self.lo, other.lo), fmin(self.hi, other.hi))

    def max(self, other: Iv) -> Iv:
        return Iv(fmax(self.lo, other.lo), fmax(self.hi, other.hi))

    def pos(self) -> Iv:
        return Iv(fmax(self.lo, 0.0), fmax(self.hi, 0.0))


def enclose(q: Fraction) -> Iv:
    """The largest binary64 at most ``q`` and the smallest at least ``q`` (lemma I2)."""
    x = float(q)
    if Fraction(x) == q:
        return Iv(x, x)
    if Fraction(x) < q:
        return Iv(x, math.nextafter(x, math.inf))
    return Iv(math.nextafter(x, -math.inf), x)


def overlap(centre: Iv, a: Iv, b: Iv, h: Iv) -> Iv:
    right = centre.plus(h).min(b)
    left = centre.minus(h).max(a)
    return right.minus(left).pos()


def main(argv: list[str]) -> int:
    path, factor = Path(argv[1]), Fraction(argv[2])
    x_arg, y_arg = Fraction(argv[3]), Fraction(argv[4])
    crate_bound = float(argv[5]) if len(argv) > 5 else None
    candidate = exact.load_json(path.read_bytes())
    measure = exact.read_measure(candidate)
    images = exact.expand(measure.side, measure.rows, factor)
    h = measure.core / 2
    lower = measure.side / 2
    upper = measure.side - exact.rho(exact.bin_floor(measure.step, 0))
    xs = {lower, upper}
    ys = {lower, upper}
    for (x1, y1, x2, y2), _ in images:
        for edge in (x1, x2):
            xs.update(p for p in (edge - h, edge + h) if lower <= p <= upper)
        for edge in (y1, y2):
            ys.update(p for p in (edge - h, edge + h) if lower <= p <= upper)
    xs_sorted, ys_sorted = sorted(xs), sorted(ys)
    if x_arg not in xs or y_arg not in ys:
        msg = "the given vertex is not on the event grid"
        raise SystemExit(msg)
    k, j_target = xs_sorted.index(x_arg), ys_sorted.index(y_arg)
    y_iv = [enclose(p) for p in ys_sorted]
    x = enclose(xs_sorted[k])
    h_iv = enclose(h)
    rects = [
        (enclose(x1), enclose(x2), enclose(y1), enclose(y2), enclose(rho))
        for (x1, y1, x2, y2), rho in images
    ]
    steps = []
    for (_, y1, _, y2), _ in images:
        row = []
        for p, sign in ((y1 - h, 1.0), (y2 - h, -1.0), (y1 + h, -1.0), (y2 + h, 1.0)):
            if p < lower:
                row.append(("initial", 0, sign))
            elif p > upper:
                row.append(("never", 0, sign))
            else:
                index = bisect.bisect_left(ys_sorted, p)
                if ys_sorted[index] != p:
                    msg = "an in-range breakpoint is missing from the events"
                    raise SystemExit(msg)
                row.append(("at", index, sign))
        steps.append(row)
    m = len(ys_sorted)
    delta = [Iv(0.0, 0.0) for _ in range(m)]
    value, slope = Iv(0.0, 0.0), Iv(0.0, 0.0)
    STEPS["count"], STEPS["total"] = 0, Fraction(0)
    active = 0
    for (rx1, rx2, ry1, ry2, rho), row in zip(rects, steps, strict=True):
        ox = overlap(x, rx1, rx2, h_iv)
        if ox.hi <= 0.0:
            continue
        active += 1
        weight = ox.mul_nonneg(rho)
        value = value.plus(weight.mul_nonneg(overlap(y_iv[0], ry1, ry2, h_iv)))
        for kind, index, sign in row:
            signed = weight if sign > 0.0 else Iv(-weight.hi, -weight.lo)
            if kind == "initial":
                slope = slope.plus(signed)
            elif kind == "at":
                delta[index] = delta[index].plus(signed)
    initial_steps = STEPS["count"]
    slope = slope.plus(delta[0])
    min_lower, argmin, at_target = math.inf, -1, Iv(math.nan, math.nan)
    max_slope, max_value = 0.0, 0.0
    for j in range(m):
        if value.lo < min_lower:
            min_lower, argmin = value.lo, j
        if j == j_target:
            at_target = Iv(value.lo, value.hi)
        max_slope = max(max_slope, abs(slope.lo), abs(slope.hi))
        max_value = max(max_value, abs(value.hi))
        if j + 1 < m:
            width = y_iv[j + 1].minus(y_iv[j])
            value = value.plus(slope.times(width))
            slope = slope.plus(delta[j + 1])
    exact_value = exact.capture(
        exact.Measure(
            measure.n,
            measure.side,
            measure.core,
            measure.step,
            measure.count,
            measure.rows,
            images,
            measure.total,
        ),
        x_arg,
        y_arg,
        0,
    )
    report = {
        "factor": str(factor),
        "x_events": len(xs_sorted),
        "y_events": m,
        "column_index": k,
        "vertex_index": j_target,
        "rectangles_active_in_column": active,
        "enclosure_at_vertex": [at_target.lo, at_target.hi],
        "enclosure_width_at_vertex": at_target.hi - at_target.lo,
        "least_lower_end_in_column": min_lower,
        "least_lower_end_at_vertex_index": argmin,
        "least_is_at_given_vertex": argmin == j_target,
        "crate_bound": crate_bound,
        "lower_end_equals_crate_bound": crate_bound is not None and at_target.lo == crate_bound,
        "exact_capture_at_vertex": float(exact_value),
        "exact_capture_rational": str(exact_value),
        "exact_minus_lower_end": float(exact_value - Fraction(at_target.lo)),
        "upper_end_minus_exact": float(Fraction(at_target.hi) - exact_value),
        "exact_inside_enclosure": Fraction(at_target.lo)
        <= exact_value
        <= Fraction(at_target.hi),
        "max_abs_slope_in_column": max_slope,
        "max_abs_value_in_column": max_value,
        "outward_steps_initial_sum": initial_steps,
        "outward_steps_total": STEPS["count"],
        "outward_steps_sum": float(STEPS["total"]),
    }
    sys.stdout.write(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
