"""Independent interval certification of the green17 sixteen-point claim.

This is the second, code-independent formal verification of the claim behind
the green17 lower bound: it shares the *data* (the sixteen points and the side) with
`cases/green17/packing.py` but none of the proof architecture -- no lemma
encodings, no cell plan, no cover machinery. Where `verify_cover` discharges a
declared partition of the container through Bentz-style lemma preconditions,
this module proves the claim directly, by exhaustive interval branch-and-bound
over the full pose space, with every discharge decision an exact integer
comparison.

**The claim proved here.** Every closed unit square contained in `[0, t]^2`
(default `t = SIDE = 4426213/10^6`; any exactly-scaled rational via `--side`)
contains at least one of the sixteen points (closed
containment). This implies the certified open-box claim: an open square `B` of
side `b > 1` inside the container contains the concentric closed unit square
`Q` (in the square's own frame `Q = {|u| <= 1/2}` sits inside
`B = {|u| < b/2}`), and `Q` inherits `B`'s containment in the container; a
point of the set inside `Q` is inside `B`.

**Pose space and its reduction.** A closed unit square is a centre `(x, y)`
and an angle; quarter-turn symmetry reduces the angle to any interval of
length `pi/2`, and this module uses `theta in [-T, T]` with `T = 7854/10^4`.
`T >= pi/4` is not assumed: it is checked exactly at import time via
`2 * sin_lower(T)^2 > 1` (sine is increasing on `[0, pi/2]`, so this is
`T > pi/4`). A closed square fits in the container exactly when both centre
coordinates lie in `[m(theta), t - m(theta)]` with
`m(theta) = (|cos theta| + |sin theta|)/2 >= 1/2`, so the initial box
`[1/2, t - 1/2]^2 x [-T, T]` contains every fitting pose.

**Exact fixed-scale arithmetic.** Every centre coordinate in play -- the
sixteen points, the walls, the seeded split values, and every bisection
midpoint -- is an exact multiple of `1/(10^6 * 2^40)`, and every angle
endpoint an exact multiple of `1/(10^4 * 2^40)`, so pose intervals are stored
as plain integers at those scales with no rounding anywhere in pose
arithmetic. Sine and cosine are bounded by exact rational Taylor partial sums
(alternating with decreasing terms on `|z| <= 1`, so consecutive partial sums
bracket the value), rounded *outward* to the scale `2^60`; outward rounding
only loosens bounds, and the values the tight faces need -- `cos = 1` and
`sin = 0` at `theta = 0` -- are exact at that scale. All downstream products
and comparisons are integer, so a pose family that touches a point exactly on
the square boundary still discharges once a split lands on it. No float
enters any decision; floats appear only in progress reporting.

**Discharges.** A parameter box is discharged when any of these holds:

- *near point*: some point sits within distance `1/2` of every centre in the
  box (max of `dx^2 + dy^2 <= 1/4`, an angle-free test -- a point within the
  inscribed circle is in the closed square at every angle);
- *oriented cover*: some point satisfies `|u| <= 1/2` and `|v| <= 1/2` for
  every pose in the box, where `(u, v)` is the displacement rotated into the
  square's frame, evaluated in interval arithmetic;
- *pair handoff*: two points `p, q` with `|p - q| <= 1` (an exact rational
  comparison on the squared distance, decided once) such that, box-wide, `p`
  can fail only by `v_p < -1/2` (its other three constraints hold) and `q`
  only by `v_q > 1/2` -- or the analogous pattern in the other coordinate or
  sign. This is sound with no angle refinement at all: `v_p - v_q` is the
  fixed displacement `p - q` projected onto the square's unit normal, so
  `|v_p - v_q| <= |p - q| <= 1` for every pose (Cauchy-Schwarz); if `p`
  fails, `v_p < -1/2` strictly, hence `v_q <= v_p + 1 < 1/2` and `q`'s
  remaining constraints put `q` in the closed square. Without this rule the
  branch-and-bound provably cannot terminate: along the curve of poses where
  coverage hands off between two such points, both sit exactly on the square
  boundary in the side-one limit, so every single-point bound is tight with
  zero margin -- the measured stall that motivated the rule sat at depth 38
  near `(x, y, theta) = (3.008, 3.246, 0.570)`, between the row points
  `(3, 2.646)` and `(5/2, 3.512)` whose distance is `sqrt(249989/250000)`;
- *no fit*: no pose in the box fits in the container (centre coordinate
  provably outside `[m(theta), t - m(theta)]` for every `theta` in the
  box's range).

Otherwise the box is split -- preferentially at a seeded critical coordinate
(a point coordinate, a point coordinate `+- 1/2`, or `theta = 0`), because
the design's exactly-tight pose families are axis-aligned at rational
coordinates and an inclusive bound is exact only when a split face lands on
them. Before splitting, the box's centre pose is tested for *definite
escape* (every point provably outside the closed square, pose provably
fitting); a hit refutes the claim with an exact witness, which is what the
negative controls exercise.

**Soundness inventory.** The branch-and-bound is a covering argument: the
initial box contains every fitting pose, every leaf is discharged by one of
the sound rules above, and splitting preserves the union.

Usage, from `packing/`:
    uv run --frozen python -m cases.green17.interval_audit
    uv run --frozen python -m cases.green17.interval_audit --side 429/100
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from fractions import Fraction

from cases.green17.packing import SIDE, build

HALF = Fraction(1, 2)

#: Angle half-range; proved `> pi/4` at import by `_check_angle_range`.
THETA_MAX = Fraction(7854, 10_000)

#: Pose-coordinate scale: every centre coordinate in play is an exact
#: multiple of 1/PSCALE.
PSCALE = 1_000_000 << 40

#: Angle scale: every angle endpoint is an exact multiple of 1/TSCALE.
TSCALE = 10_000 << 40

#: Trigonometric bounds are rounded outward to this scale; cos = 1 and
#: sin = 0 stay exact.
TRIG_SCALE = 1 << 60

#: u/v components live at scale PSCALE * TRIG_SCALE; 1/2 is exact there.
HALF_UV = (PSCALE * TRIG_SCALE) // 2

#: Squared-distance quarter at pose scale, for the near-point test.
QUARTER_P2 = (PSCALE * PSCALE) // 4

#: A point can cover a pose only when |dx| and |dy| are at most
#: (|cos| + |sin|)/2 <= sqrt(2)/2; beyond that it is dead for the whole
#: subtree. Rounded up, which only weakens the filter.
REACH_P = (7072 * PSCALE) // 10_000 + 1


class IntervalAuditError(Exception):
    """The branch-and-bound refused to certify: refuted or out of budget."""


def _to_scale_floor(value: Fraction, scale: int) -> int:
    return value.numerator * scale // value.denominator


def _to_scale_ceil(value: Fraction, scale: int) -> int:
    return -((-value.numerator * scale) // value.denominator)


def _to_scale_exact(value: Fraction, scale: int) -> int:
    scaled = value * scale
    if scaled.denominator != 1:
        raise ValueError(f"{value} is not exact at scale {scale}")
    return scaled.numerator


def _sin_bounds_abs(z: Fraction) -> tuple[Fraction, Fraction]:
    """Exact rational bounds for sin on one nonnegative argument `z <= 1`."""
    if not Fraction(0) <= z <= 1:
        raise ValueError(f"sin bound argument out of range: {z}")
    # Alternating series with decreasing terms on |z| <= 1: consecutive
    # partial sums bracket the value, and the parity of the last term says
    # which side each sum is on.
    term = z
    total = z
    lower = upper = z
    for k in range(1, 9):
        term = -term * z * z / ((2 * k) * (2 * k + 1))
        total += term
        if term < 0:
            lower = total
        else:
            upper = total
    return lower, upper


def _cos_bounds_abs(z: Fraction) -> tuple[Fraction, Fraction]:
    """Exact rational bounds for cos on one nonnegative argument `z <= 1`."""
    if not Fraction(0) <= z <= 1:
        raise ValueError(f"cos bound argument out of range: {z}")
    term = Fraction(1)
    total = Fraction(1)
    lower = upper = Fraction(1)
    for k in range(1, 9):
        term = -term * z * z / ((2 * k - 1) * (2 * k))
        total += term
        if term < 0:
            lower = total
        else:
            upper = total
    return lower, upper


def sin_interval(lo: Fraction, hi: Fraction) -> tuple[Fraction, Fraction]:
    """Bounds for sin over `[lo, hi]` inside `[-THETA_MAX, THETA_MAX]`."""
    # Sine is odd and increasing on this range.
    if lo >= 0:
        return _sin_bounds_abs(lo)[0], _sin_bounds_abs(hi)[1]
    if hi <= 0:
        neg_lo, neg_hi = _sin_bounds_abs(-hi)[0], _sin_bounds_abs(-lo)[1]
        return -neg_hi, -neg_lo
    return -_sin_bounds_abs(-lo)[1], _sin_bounds_abs(hi)[1]


def cos_interval(lo: Fraction, hi: Fraction) -> tuple[Fraction, Fraction]:
    """Bounds for cos over `[lo, hi]` inside `[-THETA_MAX, THETA_MAX]`."""
    # Cosine is even and decreasing in |theta| on this range.
    far = max(-lo, hi)
    lower = _cos_bounds_abs(far)[0]
    if lo <= 0 <= hi:
        return lower, Fraction(1)
    near = min(abs(lo), abs(hi))
    return lower, _cos_bounds_abs(near)[1]


def _check_angle_range() -> None:
    sin_lower = _sin_bounds_abs(THETA_MAX)[0]
    if not 2 * sin_lower * sin_lower > 1:
        raise AssertionError("THETA_MAX is not provably above pi/4")


_check_angle_range()


#: Outward dyadic rounding denominator for angle endpoints entering Taylor
#: evaluations: power-of-two denominators keep the rational Taylor terms
#: cheap, the 2^-60 widening is far below every margin in play, and zero is
#: preserved exactly (the tight faces at theta = 0 keep cos = 1 / sin = 0).
_COARSE = 1 << 60


def _imul(a_lo: int, a_hi: int, b_lo: int, b_hi: int) -> tuple[int, int]:
    p1 = a_lo * b_lo
    p2 = a_lo * b_hi
    p3 = a_hi * b_lo
    p4 = a_hi * b_hi
    return min(p1, p2, p3, p4), max(p1, p2, p3, p4)


@dataclass(frozen=True)
class ThetaData:
    """Per-theta-interval facts, shared by every x/y descendant of a box."""

    lo: int
    hi: int
    cos_lo: int
    cos_hi: int
    sin_lo: int
    sin_hi: int
    margin_min: int

    @classmethod
    def of(cls, lo: int, hi: int) -> ThetaData:
        # Round the endpoints outward to the dyadic grid before the Taylor
        # evaluations: bounds over a superset interval are valid for the
        # subset, and the TSCALE denominators (a factor 10^4) would otherwise
        # churn every rational Taylor term through large gcds.
        lo_f = Fraction(lo * _COARSE // TSCALE, _COARSE)
        hi_f = Fraction(-((-hi * _COARSE) // TSCALE), _COARSE)
        cos = cos_interval(lo_f, hi_f)
        sin = sin_interval(lo_f, hi_f)
        # m(theta) = (|cos| + |sin|)/2 is minimized, over this interval, at
        # the endpoint of the |theta|-range closest to zero; both endpoint
        # evaluations are lower-bounded and the smaller taken.
        ends = {abs(lo_f), abs(hi_f)}
        if lo <= 0 <= hi:
            ends.add(Fraction(0))
        margin_min = min((_cos_bounds_abs(t)[0] + _sin_bounds_abs(t)[0]) / 2 for t in ends)
        return cls(
            lo=lo,
            hi=hi,
            cos_lo=_to_scale_floor(cos[0], TRIG_SCALE),
            cos_hi=_to_scale_ceil(cos[1], TRIG_SCALE),
            sin_lo=_to_scale_floor(sin[0], TRIG_SCALE),
            sin_hi=_to_scale_ceil(sin[1], TRIG_SCALE),
            margin_min=_to_scale_floor(margin_min, PSCALE),
        )


@dataclass
class Stats:
    boxes: int = 0
    near_point: int = 0
    oriented: int = 0
    pair: int = 0
    no_fit: int = 0
    max_depth: int = 0
    #: Float running total of discharged parameter volume -- progress
    #: reporting only, no soundness role.
    volume_done: float = 0.0


def _definite_escape(
    points: list[tuple[Fraction, Fraction]],
    side: Fraction,
    x: Fraction,
    y: Fraction,
    theta: Fraction,
) -> bool:
    """True when the centre pose provably fits and provably contains no point."""
    # Probe at a nearby dyadic angle instead of the exact midpoint: any pose
    # is an equally good refutation probe, and the coarse denominator keeps
    # the Taylor terms narrow.
    theta = Fraction(round(theta * _COARSE), _COARSE)
    cos = cos_interval(theta, theta)
    sin = sin_interval(theta, theta)
    # m(theta) = (|cos| + |sin|)/2, upper-bounded through the even/odd
    # reductions on |theta| -- the signed sine interval would understate it.
    margin_max = (_cos_bounds_abs(abs(theta))[1] + _sin_bounds_abs(abs(theta))[1]) / 2
    if not (margin_max <= x <= side - margin_max and margin_max <= y <= side - margin_max):
        return False
    for px, py in points:
        dx = px - x
        dy = py - y
        u_candidates = (
            dx * cos[0] + dy * sin[0],
            dx * cos[0] + dy * sin[1],
            dx * cos[1] + dy * sin[0],
            dx * cos[1] + dy * sin[1],
        )
        v_candidates = (
            dy * cos[0] - dx * sin[0],
            dy * cos[0] - dx * sin[1],
            dy * cos[1] - dx * sin[0],
            dy * cos[1] - dx * sin[1],
        )
        u_lo, u_hi = min(u_candidates), max(u_candidates)
        v_lo, v_hi = min(v_candidates), max(v_candidates)
        outside = u_lo > HALF or u_hi < -HALF or v_lo > HALF or v_hi < -HALF
        if not outside:
            return False
    return True


def _parabola_hi(p_i: int, c_lo: int, c_hi: int) -> int:
    """Upper bound of `p*c - c^2/2` (in UV units) over `c in [c_lo, c_hi]`.

    Concave in `c` with vertex at `c = p`; the sup is at an endpoint or the
    vertex, each evaluated with outward rounding.
    """

    def at(c: int) -> int:
        return p_i * c - (c * c * PSCALE) // (2 * TRIG_SCALE)

    best = max(at(c_lo), at(c_hi))
    if c_lo * PSCALE < p_i * TRIG_SCALE < c_hi * PSCALE:
        vertex = (p_i * p_i * TRIG_SCALE + 2 * PSCALE - 1) // (2 * PSCALE)
        best = max(best, vertex)
    return best


def _parabola_lo(p_i: int, side_i: int, c_lo: int, c_hi: int) -> int:
    """Lower bound of `(p - side)*c + c^2/2` (in UV units) over the c range.

    Convex in `c` with vertex at `c = side - p`; the inf is at an endpoint or
    the vertex, each evaluated with outward rounding.
    """
    gap = side_i - p_i

    def at(c: int) -> int:
        return (p_i - side_i) * c + (c * c * PSCALE) // (2 * TRIG_SCALE)

    best = min(at(c_lo), at(c_hi))
    if c_lo * PSCALE < gap * TRIG_SCALE < c_hi * PSCALE:
        vertex = -((gap * gap * TRIG_SCALE + 2 * PSCALE - 1) // (2 * PSCALE))
        best = min(best, vertex)
    return best


def _sin_mix_bounds(
    e_lo: int, e_hi: int, *, c_lo: int, c_hi: int, s_lo: int, s_hi: int
) -> tuple[int, int]:
    """Bounds of `e*s -+ |s|*c/2` over the box (in UV units).

    Returns `(mix_lo, mix_hi)` where `mix_hi` bounds `e*s - |s|*c/2` above
    and `mix_lo` bounds `e*s + |s|*c/2` below. Both are piecewise linear in
    `s` with a kink at zero, so the extremes sit at the `s` endpoints (with
    the matching `w = e -+ c/2` branch) or at `s = 0`.
    """
    c_half_lo = (c_lo * PSCALE) // (2 * TRIG_SCALE)
    c_half_hi = -((-c_hi * PSCALE) // (2 * TRIG_SCALE))
    w_minus_lo, w_minus_hi = e_lo - c_half_hi, e_hi - c_half_lo
    w_plus_lo, w_plus_hi = e_lo + c_half_lo, e_hi + c_half_hi
    hi_cands: list[int] = []
    lo_cands: list[int] = []
    for s_end in (s_lo, s_hi):
        if s_end >= 0:
            hi_cands.extend((s_end * w_minus_lo, s_end * w_minus_hi))
            lo_cands.extend((s_end * w_plus_lo, s_end * w_plus_hi))
        else:
            hi_cands.extend((s_end * w_plus_lo, s_end * w_plus_hi))
            lo_cands.extend((s_end * w_minus_lo, s_end * w_minus_hi))
    if s_lo < 0 < s_hi:
        hi_cands.append(0)
        lo_cands.append(0)
    return min(lo_cands), max(hi_cands)


def _pick_split(lo: int, hi: int, seeds: tuple[int, ...]) -> int:
    width = hi - lo
    inner_lo = lo + width // 4
    inner_hi = hi - width // 4
    for seed in seeds:
        if inner_lo <= seed <= inner_hi and lo < seed < hi:
            return seed
    return (lo + hi) // 2


def certify(
    side: Fraction | None = None,
    points: list[tuple[Fraction, Fraction]] | None = None,
    max_boxes: int = 400_000_000,
    progress_every: int = 0,
) -> Stats:
    """Certify the closed-unit-square claim, or raise `IntervalAuditError`.

    The default arguments are the green17 configuration; `side` and `points`
    exist for the negative controls, which must see the certifier refuse.
    """
    if side is None:
        side = SIDE
    if points is None:
        set_points, _vertices, _plan, _boundary = build()
        points = [(p[0].value, p[1].value) for p in set_points.values()]

    points_i = [(_to_scale_exact(px, PSCALE), _to_scale_exact(py, PSCALE)) for px, py in points]
    half_p = PSCALE // 2
    x_values = {px for px, _ in points_i}
    y_values = {py for _, py in points_i}
    x_seeds = tuple(
        sorted(x_values | {x + half_p for x in x_values} | {x - half_p for x in x_values})
    )
    y_seeds = tuple(
        sorted(y_values | {y + half_p for y in y_values} | {y - half_p for y in y_values})
    )
    theta_seeds = (0,)

    # Pairs eligible for the handoff rule: squared distance at most one, an
    # exact rational comparison decided once.
    close_pair = [
        [
            (points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2 <= 1
            for j in range(len(points))
        ]
        for i in range(len(points))
    ]

    stats = Stats()
    theta_top = _to_scale_exact(THETA_MAX, TSCALE)
    root_theta = ThetaData.of(-theta_top, theta_top)
    low = half_p
    high = _to_scale_exact(side, PSCALE) - half_p
    if high < low:
        raise IntervalAuditError("container too small for any fitting pose")
    side_i = _to_scale_exact(side, PSCALE)
    all_indices = tuple(range(len(points_i)))
    stack: list[tuple[int, int, int, int, ThetaData, tuple[int, ...], int]] = [
        (low, high, low, high, root_theta, all_indices, 0)
    ]

    # Progress bookkeeping only.
    pose_unit = 1.0 / float(PSCALE)
    theta_unit = 1.0 / float(TSCALE)
    total_volume = (float(high - low) * pose_unit) ** 2 * 2 * float(theta_top) * theta_unit

    while stack:
        x1, x2, y1, y2, theta, candidates, depth = stack.pop()
        stats.boxes += 1
        stats.max_depth = max(stats.max_depth, depth)
        if stats.boxes > max_boxes:
            raise IntervalAuditError(
                f"box budget {max_boxes} exhausted at depth {depth} on "
                f"x=[{Fraction(x1, PSCALE)},{Fraction(x2, PSCALE)}] "
                f"y=[{Fraction(y1, PSCALE)},{Fraction(y2, PSCALE)}] "
                f"theta=[{Fraction(theta.lo, TSCALE)},{Fraction(theta.hi, TSCALE)}]"
            )
        if progress_every and stats.boxes % progress_every == 0:
            done = stats.volume_done / total_volume
            print(
                f"progress: boxes {stats.boxes}  volume {done:.6f}  "
                f"stack {len(stack)}  depth {depth}",
                file=sys.stderr,
                flush=True,
            )

        # No pose in the box fits: a centre coordinate is provably outside
        # [m(theta), side - m(theta)] for every theta in range.
        margin = theta.margin_min
        if x2 < margin or x1 > side_i - margin or y2 < margin or y1 > side_i - margin:
            stats.no_fit += 1
            stats.volume_done += (
                (float(x2 - x1) * float(y2 - y1) * float(theta.hi - theta.lo))
                * pose_unit
                * pose_unit
                * theta_unit
            )
            continue

        c_lo, c_hi, s_lo, s_hi = theta.cos_lo, theta.cos_hi, theta.sin_lo, theta.sin_hi
        survivors: list[int] = []
        frames: list[tuple[int, int, int, int]] = []
        discharged = False
        for index in candidates:
            px, py = points_i[index]
            dx_lo, dx_hi = px - x2, px - x1
            dy_lo, dy_hi = py - y2, py - y1
            if dx_lo > REACH_P or dx_hi < -REACH_P or dy_lo > REACH_P or dy_hi < -REACH_P:
                continue
            dx_sq = max(dx_lo * dx_lo, dx_hi * dx_hi)
            dy_sq = max(dy_lo * dy_lo, dy_hi * dy_hi)
            if dx_sq + dy_sq <= QUARTER_P2:
                stats.near_point += 1
                discharged = True
                break
            u_a, u_b = _imul(dx_lo, dx_hi, c_lo, c_hi)
            u_c, u_d = _imul(dy_lo, dy_hi, s_lo, s_hi)
            u_lo, u_hi = u_a + u_c, u_b + u_d
            v_a, v_b = _imul(dy_lo, dy_hi, c_lo, c_hi)
            v_c, v_d = _imul(-dx_hi, -dx_lo, s_lo, s_hi)
            v_lo, v_hi = v_a + v_c, v_b + v_d
            if u_lo >= -HALF_UV and u_hi <= HALF_UV and v_lo >= -HALF_UV and v_hi <= HALF_UV:
                stats.oriented += 1
                discharged = True
                break
            # Wall-tightened second chance: the claim only quantifies over
            # fitting poses, and substituting the fit constraint
            # `coord >= m(theta)` (or `<= side - m(theta)`) into the rotated
            # component gives `u <= p*c - c^2/2 + [e*s - |s|*c/2]` and its
            # mirrors -- exactly what closes the triple-tight pockets where a
            # wall, a point on the square edge, and theta -> 0 meet.
            mix_lo_u, mix_hi_u = _sin_mix_bounds(
                dy_lo, dy_hi, c_lo=c_lo, c_hi=c_hi, s_lo=s_lo, s_hi=s_hi
            )
            u_lo2 = max(u_lo, _parabola_lo(px, side_i, c_lo, c_hi) + mix_lo_u)
            u_hi2 = min(u_hi, _parabola_hi(px, c_lo, c_hi) + mix_hi_u)
            mix_lo_v, mix_hi_v = _sin_mix_bounds(
                -dx_hi, -dx_lo, c_lo=c_lo, c_hi=c_hi, s_lo=s_lo, s_hi=s_hi
            )
            v_lo2 = max(v_lo, _parabola_lo(py, side_i, c_lo, c_hi) + mix_lo_v)
            v_hi2 = min(v_hi, _parabola_hi(py, c_lo, c_hi) + mix_hi_v)
            if (
                u_lo2 >= -HALF_UV
                and u_hi2 <= HALF_UV
                and v_lo2 >= -HALF_UV
                and v_hi2 <= HALF_UV
            ):
                stats.oriented += 1
                discharged = True
                break
            survivors.append(index)
            frames.append((u_lo2, u_hi2, v_lo2, v_hi2))
        if discharged:
            stats.volume_done += (
                (float(x2 - x1) * float(y2 - y1) * float(theta.hi - theta.lo))
                * pose_unit
                * pose_unit
                * theta_unit
            )
            continue

        # Pair handoff: p may fail only on one side of one coordinate, q only
        # on the opposite side of the same coordinate, and |p - q| <= 1.
        count = len(survivors)
        if count >= 2:
            u_solid = [f[2] >= -HALF_UV and f[3] <= HALF_UV for f in frames]
            v_solid = [f[0] >= -HALF_UV and f[1] <= HALF_UV for f in frames]
            u_low_only = [u_solid[k] and frames[k][1] <= HALF_UV for k in range(count)]
            u_high_only = [u_solid[k] and frames[k][0] >= -HALF_UV for k in range(count)]
            v_low_only = [v_solid[k] and frames[k][3] <= HALF_UV for k in range(count)]
            v_high_only = [v_solid[k] and frames[k][2] >= -HALF_UV for k in range(count)]
            for a in range(count):
                if discharged:
                    break
                for b in range(count):
                    if a == b or not close_pair[survivors[a]][survivors[b]]:
                        continue
                    if (u_low_only[a] and u_high_only[b]) or (v_low_only[a] and v_high_only[b]):
                        stats.pair += 1
                        discharged = True
                        break
        if discharged:
            stats.volume_done += (
                (float(x2 - x1) * float(y2 - y1) * float(theta.hi - theta.lo))
                * pose_unit
                * pose_unit
                * theta_unit
            )
            continue

        # The escape probe is a refutation heuristic, not a soundness step:
        # run it only once boxes are deep enough that a genuine escape region
        # would dominate the box, so its cost stays off the hot path.
        if (
            depth >= 8
            and depth % 4 == 0
            and _definite_escape(
                points,
                side,
                Fraction(x1 + x2, 2 * PSCALE),
                Fraction(y1 + y2, 2 * PSCALE),
                Fraction(theta.lo + theta.hi, 2 * TSCALE),
            )
        ):
            raise IntervalAuditError(
                f"refuted: the closed unit square at x={Fraction(x1 + x2, 2 * PSCALE)} "
                f"y={Fraction(y1 + y2, 2 * PSCALE)} "
                f"theta={Fraction(theta.lo + theta.hi, 2 * TSCALE)} "
                "fits and contains no point"
            )

        remaining = tuple(survivors)
        x_width = x2 - x1
        y_width = y2 - y1
        # Angle width is compared on the pose scale so the weighting between
        # dimensions is meaningful; the factor 2 reflects the lever arm.
        theta_width = ((theta.hi - theta.lo) * PSCALE // TSCALE) * 2
        if depth > 200:
            raise IntervalAuditError(
                f"stall: depth {depth} without discharge on "
                f"x=[{Fraction(x1, PSCALE)},{Fraction(x2, PSCALE)}] "
                f"y=[{Fraction(y1, PSCALE)},{Fraction(y2, PSCALE)}] "
                f"theta=[{Fraction(theta.lo, TSCALE)},{Fraction(theta.hi, TSCALE)}]"
            )
        widths = (x_width, y_width, theta_width)
        axis = widths.index(max(widths))
        if axis == 0:
            cut = _pick_split(x1, x2, x_seeds)
            if not x1 < cut < x2:
                raise IntervalAuditError(
                    f"resolution floor in x at depth {depth}: "
                    f"x=[{Fraction(x1, PSCALE)},{Fraction(x2, PSCALE)}] "
                    f"y=[{Fraction(y1, PSCALE)},{Fraction(y2, PSCALE)}] "
                    f"theta=[{Fraction(theta.lo, TSCALE)},{Fraction(theta.hi, TSCALE)}] "
                    f"survivors={remaining}"
                )
            stack.append((x1, cut, y1, y2, theta, remaining, depth + 1))
            stack.append((cut, x2, y1, y2, theta, remaining, depth + 1))
        elif axis == 1:
            cut = _pick_split(y1, y2, y_seeds)
            if not y1 < cut < y2:
                raise IntervalAuditError(
                    f"resolution floor in y at depth {depth}: "
                    f"x=[{Fraction(x1, PSCALE)},{Fraction(x2, PSCALE)}] "
                    f"y=[{Fraction(y1, PSCALE)},{Fraction(y2, PSCALE)}] "
                    f"theta=[{Fraction(theta.lo, TSCALE)},{Fraction(theta.hi, TSCALE)}] "
                    f"survivors={remaining}"
                )
            stack.append((x1, x2, y1, cut, theta, remaining, depth + 1))
            stack.append((x1, x2, cut, y2, theta, remaining, depth + 1))
        else:
            cut = _pick_split(theta.lo, theta.hi, theta_seeds)
            if not theta.lo < cut < theta.hi:
                raise IntervalAuditError(f"resolution floor in theta at depth {depth}")
            stack.append((x1, x2, y1, y2, ThetaData.of(theta.lo, cut), remaining, depth + 1))
            stack.append((x1, x2, y1, y2, ThetaData.of(cut, theta.hi), remaining, depth + 1))

    return stats


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--side",
        type=str,
        default=None,
        help="container side as an exact fraction (default: the module SIDE)",
    )
    parser.add_argument("--max-boxes", type=int, default=400_000_000)
    parser.add_argument("--progress-every", type=int, default=0)
    options = parser.parse_args(arguments)
    side = Fraction(options.side) if options.side is not None else SIDE
    started = time.monotonic()
    stats = certify(
        side=side, max_boxes=options.max_boxes, progress_every=options.progress_every
    )
    elapsed = time.monotonic() - started
    print(f"CERTIFIED: every closed unit square in [0, {side}]^2 contains one of the 16 points")
    print(
        f"boxes {stats.boxes}  near-point {stats.near_point}  oriented "
        f"{stats.oriented}  pair {stats.pair}  no-fit {stats.no_fit}  "
        f"max depth {stats.max_depth}  wall {elapsed:.1f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
