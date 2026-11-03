"""The enclosure `sqverify-fast`'s axis vertex sweep holds at one vertex, recomputed here.

At direction `r = 0` the crate's vertex sweep (`sqverify_fast/src/axis.rs`, lemmas A1
and A2 of `SOUNDNESS.md`) keeps, at every vertex of its event grid, an interval
`[l, u]` around the exact capture `F` there, and reports only `min l` and the vertex
where it falls (`min_certified_lower_bound`, `argmin`). The census control
(`devtools.sqverify_fast_census`, `refusal_record`) checks the 99/100 mutant's axis
refusal against that report, and needs the interval: `F - l` is half its width, which
varies with the vertex's place in its column and the slopes summed there (2.5e-9 at
s(39)'s least vertex, 1.4e-10 at s(37)'s), so no constant allowance fits every
certificate (F-1 and section 5 of
docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md).

`column_enclosure` is that review's option 2: it walks the vertex's column as `axis.rs`
does, with the outward-rounded binary64 arithmetic of `interval.rs` written here in
Python floats, and returns `[l', u']` at the vertex. It transcribes the crate's
arithmetic, so it is not an evaluator written apart from the crate; the exact capture
it is compared with is (`check_sqverify_fast.mixed_exact`). Two facts make the pair
the test the control needs:

- `[l', u']` encloses the exact capture whether or not the walk is the crate's. Each
  step is one IEEE 754 binary64 operation rounded to nearest (CPython's float
  arithmetic, which contracts nothing into a fused multiply-add), moved outward by
  `|x| 2^-52 + 2^-1074`, at least the gap to the next binary64 value (lemma I1), on
  tight enclosures of exact rationals (lemma I2), along lemma A2's exact slope schedule.
- `l' = l` to the bit shows the walk is the crate's: the same events, the same
  rectangles in the same order, the same operations. Then `[l', u']` is the interval
  whose lower end the crate certified, and its width is the precision the sweep had at
  that vertex. A transcription that strayed from the crate's path fails that equality.

It decides nothing on its own: the census reads it to judge a refusal the crate made.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any

from devtools.check_sqverify_fast import mixed_rows

#: `interval.rs`'s GAP: no gap between adjacent binary64 values exceeds `2^-52 |x|`.
GAP = 2.0**-52
#: `interval.rs`'s TINY, the least positive subnormal: the gap at and below the normal
#: range.
TINY = 5e-324

#: A closed interval of binary64 endpoints, `(lo, hi)`, as `interval.rs`'s `Iv` holds it.
type Iv = tuple[float, float]

ZERO: Iv = (0.0, 0.0)


def dn(x: float) -> float:
    """A lower bound on the exact result whose rounding is `x` (lemma I1)."""
    return x - (abs(x) * GAP + TINY)


def up(x: float) -> float:
    """An upper bound on the exact result whose rounding is `x` (lemma I1)."""
    return x + (abs(x) * GAP + TINY)


def fmin(a: float, b: float) -> float:
    """`interval.rs`'s `fmin`, `if a < b { a } else { b }`, plus `a * 0` to carry a NaN or
    an infinite `a`. Python's `min(b, a)` keeps `b` unless `a < b`: the same select."""
    return min(b, a) + a * 0.0


def fmax(a: float, b: float) -> float:
    """`interval.rs`'s `fmax`, `if a > b { a } else { b }`, plus `a * 0` to carry a NaN or
    an infinite `a`. Python's `max(b, a)` keeps `b` unless `a > b`: the same select."""
    return max(b, a) + a * 0.0


def plus(a: Iv, b: Iv) -> Iv:
    return dn(a[0] + b[0]), up(a[1] + b[1])


def minus(a: Iv, b: Iv) -> Iv:
    return dn(a[0] - b[1]), up(a[1] - b[0])


def times(a: Iv, b: Iv) -> Iv:
    """The enclosure of a product by the four endpoint products, as `Iv::times`."""
    p, q, r, s = a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]
    return dn(fmin(fmin(p, q), fmin(r, s))), up(fmax(fmax(p, q), fmax(r, s)))


def mul_nonneg(a: Iv, k: Iv) -> Iv:
    """The product of `a` with a nonnegative `k`, as `Iv::mul_nonneg`."""
    lo = a[0] * k[0] if a[0] >= 0.0 else a[0] * k[1]
    hi = a[1] * k[1] if a[1] >= 0.0 else a[1] * k[0]
    return dn(lo), up(hi)


def lesser(a: Iv, b: Iv) -> Iv:
    """`Iv::min`, the pointwise minimum."""
    return fmin(a[0], b[0]), fmin(a[1], b[1])


def greater(a: Iv, b: Iv) -> Iv:
    """`Iv::max`, the pointwise maximum."""
    return fmax(a[0], b[0]), fmax(a[1], b[1])


def positive(a: Iv) -> Iv:
    """`Iv::pos`, the positive part."""
    return fmax(a[0], 0.0), fmax(a[1], 0.0)


def enclose(q: Fraction) -> Iv:
    """The largest binary64 value at most `q` and the smallest at least `q` (lemma I2,
    `exact.rs`'s `enclose`). `float` of a fraction is correctly rounded, so one step
    outward from it is the other end when it is not `q` itself."""
    x = float(q)
    if Fraction(x) == q:
        return x, x
    if Fraction(x) < q:
        return x, math.nextafter(x, math.inf)
    return math.nextafter(x, -math.inf), x


def images(
    raw: dict[str, Any], factor: Fraction
) -> list[tuple[tuple[Fraction, ...], Fraction]]:
    """Every rectangle image `(x1, y1, x2, y2)` with its density, as admission expands a
    format M file whose masses are `factor` times `raw`'s (`certificate.rs`, `admit`): a
    row of zero mass is skipped, each other row's eight images carry an eighth of its mass
    in `d4_images`'s order, and coincident images are merged by exact key in first-seen
    order. That order is the order the column walk sums in, so it must be the crate's."""
    side = Fraction(raw["L"])
    merged: dict[tuple[Fraction, ...], Fraction] = {}
    for _kind, (x1, y1, x2, y2), mass in mixed_rows(raw):
        if mass == 0:
            continue
        density = factor * mass / 8 / ((x2 - x1) * (y2 - y1))
        rx1, rx2, ry1, ry2 = side - x2, side - x1, side - y2, side - y1
        for image in (
            (x1, y1, x2, y2),
            (rx1, y1, rx2, y2),
            (x1, ry1, x2, ry2),
            (rx1, ry1, rx2, ry2),
            (y1, x1, y2, x2),
            (ry1, x1, ry2, x2),
            (y1, rx1, y2, rx2),
            (ry1, rx1, ry2, rx2),
        ):
            merged[image] = merged.get(image, Fraction(0)) + density
    return list(merged.items())


def column_enclosure(
    raw: dict[str, Any], factor: Fraction, x: Fraction, y: Fraction, upper: Fraction
) -> Iv | None:
    """The enclosure `[l', u']` the axis sweep holds at the vertex `(x, y)` of the
    measure with every mass of `raw` scaled by `factor`, on the quadrant `[L/2, upper]^2`
    (`upper` is the domain's end at node 0, `L - 1/2` for format M's per-bin domain).

    It walks `x`'s column from `L/2` to `y` exactly as `verify_axis` does. None where the
    sweep would not run (a point or segment mass, lemma B5), where `y` is not an ordinate
    event, or where the enclosure is not finite; the census reads None as a refusal it
    cannot tie to the crate's report, so it fails closed."""
    if any(kind != "rectangle" and mass != 0 for kind, _, mass in mixed_rows(raw)):
        return None
    h = Fraction(raw["B"]) / 2
    lower = Fraction(raw["L"]) / 2
    rects = images(raw, factor)
    events = {lower, upper}
    for (_, y1, _, y2), _density in rects:
        for edge in (y1, y2):
            events.update(p for p in (edge - h, edge + h) if lower <= p <= upper)
    ys = sorted(events)
    index = {value: position for position, value in enumerate(ys)}
    if y not in index:
        return None
    target = index[y]
    y_iv = [enclose(value) for value in ys]
    h_iv = enclose(h)
    x_iv = enclose(x)

    def overlap(centre: Iv, a: Iv, b: Iv) -> Iv:
        # |[c - h, c + h] intersect [a, b]| = (min(c + h, b) - max(c - h, a))^+
        right = lesser(plus(centre, h_iv), b)
        left = greater(minus(centre, h_iv), a)
        return positive(minus(right, left))

    delta: list[Iv] = [ZERO] * len(ys)
    value, slope = ZERO, ZERO
    for (x1, y1, x2, y2), density in rects:
        ox = overlap(x_iv, enclose(x1), enclose(x2))
        if ox[1] <= 0.0:
            continue
        weight = mul_nonneg(ox, enclose(density))
        ry1, ry2 = enclose(y1), enclose(y2)
        value = plus(value, mul_nonneg(weight, overlap(y_iv[0], ry1, ry2)))
        # The ordinate overlap's slope steps by +1, -1, -1, +1 at y1 - h, y2 - h, y1 + h
        # and y2 + h: below the domain into the initial slope, above it never.
        for point, sign in ((y1 - h, 1), (y2 - h, -1), (y1 + h, -1), (y2 + h, 1)):
            signed = weight if sign > 0 else (-weight[1], -weight[0])
            if point < lower:
                slope = plus(slope, signed)
            elif point <= upper:
                delta[index[point]] = plus(delta[index[point]], signed)
    slope = plus(slope, delta[0])
    for j in range(target):
        value = plus(value, times(slope, minus(y_iv[j + 1], y_iv[j])))
        slope = plus(slope, delta[j + 1])
    if not (math.isfinite(value[0]) and math.isfinite(value[1])):
        return None
    return value
