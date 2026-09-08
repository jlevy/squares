"""BC-303 independent reader for Theorem E.4 (lane E, session-104).

Promoted from the e4_reader.py appendix at Git commit c89c7646. Geometry and
exact bounds are retained; the CLI is portable, bounded, and fails on incomplete
covers. Run from packing/ with uv run --frozen --all-extras --group dev python
-m devtools.segment_cover_replay --output RESULT.json.

Claim replayed: every closed unit square contained in S = [0, 96/25]^2, at any angle, is
within delta = 3/500 (Euclidean) of one of the ten closed horizontal segments of length
1/10 centred on Stromquist's Figure-13 points at 96/25.

Design (fixed before reading the lane's cover_reader.py):
  * pose (t, cx, cy), t = tan(theta/2); domain t in [0, 27/64] (covers theta in [0, pi/4]
    by the reflection x -> q - x, which keeps the segment set and maps theta -> pi/2 - theta),
    cx in [1/2, 7/2], cy in [1/2, 2] (covers cy <= q/2 by the half-turn, which keeps theta);
    dyadic bounds so every bisection box is an exact float and an exact Fraction;
  * signed Euclidean distance g(P, m) from the square to segment m (negative = penetration
    depth); over a box with half-widths (ht, hx, hy) about the centre pose P0,
    g(P, m) <= g(P0, m) + sqrt(hx^2 + hy^2) + (sqrt 2 / 2) * |theta - theta0|,
    |theta - theta0| <= 2 ht / (1 + t1 t0); certified iff min_m g(P0, m) + h <= delta;
  * g(P0, seg) = min over the segment of a convex function; the float stage evaluates the
    analytic candidate minimisers, the exact stage re-evaluates g at the recorded rational
    minimiser (an upper bound on the minimum whatever the float stage did);
  * a box is discarded only if it holds no contained pose; an undecided floor box is
    a failure. The exact polygon falsifier supplies the retained negative control.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from fractions import Fraction
from math import isqrt
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from strif import atomic_write_text

from devtools.rounded_measure_audit import source_identity

type FloatArray = NDArray[np.float64]

Q = Fraction(96, 25)
DELTA = Fraction(3, 500)
HALF_LEN = Fraction(1, 20)
SQRT2_UP = Fraction(665857, 470832)  # convergent from above: 665857^2 - 2*470832^2 = 1 > 0
assert SQRT2_UP * SQRT2_UP > 2
SQRT2F = float(SQRT2_UP)
P10 = [
    (Fraction(1), Fraction(1)),
    (Fraction(48, 25), Fraction(1)),
    (Fraction(71, 25), Fraction(1)),
    (Fraction(27, 50), Fraction(48, 25)),
    (Fraction(73, 50), Fraction(48, 25)),
    (Fraction(119, 50), Fraction(48, 25)),
    (Fraction(33, 10), Fraction(48, 25)),
    (Fraction(1), Fraction(71, 25)),
    (Fraction(48, 25), Fraction(71, 25)),
    (Fraction(71, 25), Fraction(71, 25)),
]
ALLOW = 1e-9

# ----------------------------------------------------------------------------- exact helpers


def sqrt_upper(fr: Fraction, bits: int = 40) -> Fraction:
    """segment_start rational rho with rho^2 >= fr, within 2^-bits of sqrt(fr)."""
    if fr <= 0:
        return Fraction(0)
    n, d = fr.numerator, fr.denominator
    scale = 1 << bits
    return Fraction(isqrt(n * d * scale * scale) + 1, d * scale)


def frame(t: Fraction) -> tuple[Fraction, Fraction]:
    den = 1 + t * t
    return (1 - t * t) / den, 2 * t / den


def half_width(t: Fraction) -> Fraction:
    c, s = frame(t)
    return (c + s) / 2


def exact_signed(
    t0: Fraction, x0: Fraction, y0: Fraction, px: Fraction, py: Fraction
) -> tuple[bool, Fraction]:
    """Signed distance of point p from the closed unit square at pose (t0, x0, y0).

    Returns (inside, value): inside -> value is the signed distance (<= 0, exact);
    outside -> value is the squared distance (> 0, exact).
    """
    c, s = frame(t0)
    rx, ry = px - x0, py - y0
    u = rx * c + ry * s
    v = -rx * s + ry * c
    a = abs(u) - Fraction(1, 2)
    b = abs(v) - Fraction(1, 2)
    if a <= 0 and b <= 0:
        return True, max(a, b)
    a = max(a, Fraction(0))
    b = max(b, Fraction(0))
    return False, a * a + b * b


def square_vertices(
    t0: Fraction, x0: Fraction, y0: Fraction
) -> list[tuple[Fraction, Fraction]]:
    c, s = frame(t0)
    out = []
    for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        out.append((x0 + (a * c - b * s) / 2, y0 + (a * s + b * c) / 2))
    return out


def _cross(ax, ay, bx, by) -> Fraction:
    return ax * by - ay * bx


def _point_seg_dist2(point, start, end) -> Fraction:
    px, py = point
    ax, ay = start
    bx, by = end
    dx, dy = bx - ax, by - ay
    l2 = dx * dx + dy * dy
    tt = ((px - ax) * dx + (py - ay) * dy) / l2
    tt = min(max(tt, Fraction(0)), Fraction(1))
    cx, cy = ax + tt * dx, ay + tt * dy
    return (px - cx) ** 2 + (py - cy) ** 2


def _segments_cross(p1, p2, p3, p4) -> bool:
    """Closed segments p1p2 and p3p4 intersect (exact, with collinear cases)."""

    def orient(a, b, c):
        return _cross(b[0] - a[0], b[1] - a[1], c[0] - a[0], c[1] - a[1])

    def on_seg(a, b, c):
        return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(
            a[1], b[1]
        )

    o1, o2, o3, o4 = (
        orient(p1, p2, p3),
        orient(p1, p2, p4),
        orient(p3, p4, p1),
        orient(p3, p4, p2),
    )
    if (
        ((o1 > 0) != (o2 > 0))
        and ((o3 > 0) != (o4 > 0))
        and o1 != 0
        and o2 != 0
        and o3 != 0
        and o4 != 0
    ):
        return True
    if o1 == 0 and on_seg(p1, p2, p3):
        return True
    if o2 == 0 and on_seg(p1, p2, p4):
        return True
    if o3 == 0 and on_seg(p3, p4, p1):
        return True
    return bool(o4 == 0 and on_seg(p3, p4, p2))


def exact_square_segment_dist2(
    t0: Fraction,
    x0: Fraction,
    y0: Fraction,
    seg_index: int,
    *,
    half_length: Fraction = HALF_LEN,
) -> Fraction:
    """Exact square-to-segment distance squared, including edge crossings."""
    xm, ym = P10[seg_index]
    segment_start = (xm - half_length, ym)
    box = (xm + half_length, ym)
    verts = square_vertices(t0, x0, y0)
    # endpoints inside the closed square?
    for px, py in (segment_start, box):
        inside, _ = exact_signed(t0, x0, y0, px, py)
        if inside:
            return Fraction(0)
    edges = [(verts[i], verts[(i + 1) % 4]) for i in range(4)]
    for e0, e1 in edges:
        if _segments_cross(e0, e1, segment_start, box):
            return Fraction(0)
    best = min(_point_seg_dist2((vx, vy), segment_start, box) for vx, vy in verts)
    for px, py in (segment_start, box):
        for e0, e1 in edges:
            d2 = _point_seg_dist2((px, py), e0, e1)
            best = min(best, d2)
    return best


def exact_contained(t0: Fraction, x0: Fraction, y0: Fraction) -> bool:
    return all(0 <= vx <= Q and 0 <= vy <= Q for vx, vy in square_vertices(t0, x0, y0))


def exact_escape(
    t0: Fraction,
    x0: Fraction,
    y0: Fraction,
    delta: Fraction = DELTA,
    *,
    half_length: Fraction = HALF_LEN,
) -> tuple[bool, Fraction]:
    """Return strict escape status and exact least squared segment distance."""
    if not exact_contained(t0, x0, y0):
        return False, Fraction(-1)
    least = min(
        exact_square_segment_dist2(t0, x0, y0, k, half_length=half_length)
        for k in range(len(P10))
    )
    return least > delta * delta, least


# ----------------------------------------------------------------------------- float stage

SEG_X = np.array([float(p[0]) for p in P10])
SEG_Y = np.array([float(p[1]) for p in P10])
HL = float(HALF_LEN)


def float_g_min(t0: FloatArray, x0: FloatArray, y0: FloatArray):
    """min over segments of the signed distance at the centre poses; returns (g, seg, s*)."""
    n = t0.shape[0]
    den = 1.0 + t0 * t0
    cosine = (1.0 - t0 * t0) / den
    sine = 2.0 * t0 / den
    rx = SEG_X[None, :] - x0[:, None]  # (n, 10) at s = 0
    ry = SEG_Y[None, :] - y0[:, None]
    u0 = rx * cosine[:, None] + ry * sine[:, None]
    v0 = -rx * sine[:, None] + ry * cosine[:, None]
    cosine_column = cosine[:, None]
    sine_column = sine[:, None]
    with np.errstate(divide="ignore", invalid="ignore"):
        cands = [
            np.full_like(u0, -HL),
            np.full_like(u0, HL),
            -u0 / cosine_column,  # u = 0
            v0 / sine_column,  # v = 0
            (0.5 - u0) / cosine_column,
            (-0.5 - u0) / cosine_column,  # u = +-1/2
            (v0 - 0.5) / sine_column,
            (v0 + 0.5) / sine_column,  # v = +-1/2
            (v0 - u0) / (cosine_column + sine_column),  # u = v
            (-v0 - u0) / (cosine_column - sine_column),  # u = -v
        ]
        cands.extend(
            -u0 * cosine_column
            + v0 * sine_column
            + (su * cosine_column - sv * sine_column) / 2.0
            for su in (1.0, -1.0)
            for sv in (1.0, -1.0)
        )
    s = np.stack(cands, axis=2)  # (n, 10, 14)
    s = np.where(np.isfinite(s), s, HL)
    s = np.clip(s, -HL, HL)
    u = u0[:, :, None] + cosine_column[:, :, None] * s
    v = v0[:, :, None] - sine_column[:, :, None] * s
    a = np.abs(u) - 0.5
    b = np.abs(v) - 0.5
    inside = (a <= 0) & (b <= 0)
    val = np.where(inside, np.maximum(a, b), np.hypot(np.maximum(a, 0.0), np.maximum(b, 0.0)))
    flat = val.reshape(n, -1)
    idx = np.argmin(flat, axis=1)
    g = flat[np.arange(n), idx]
    seg = idx // s.shape[2]
    cand = idx % s.shape[2]
    sstar = s.reshape(n, -1)[np.arange(n), idx]
    return g, seg, sstar, cand


def float_half_width(t):
    den = 1.0 + t * t
    return ((1.0 - t * t) / den + 2.0 * t / den) / 2.0


def run_cover(
    delta: float,
    floor: float,
    node_budget: int,
    chunk: int = 4000,
    log: Callable[[str], None] | None = None,
):
    dom = np.array([[0.0, 27 / 64, 0.5, 3.5, 0.5, 2.0]])  # t1 t2 x1 x2 y1 y2 (all dyadic)
    frontier = dom
    leaves = []  # certified: rows [t1 t2 x1 x2 y1 y2 seg sstar g h]
    discards = []  # rows [t1 t2 x1 x2 y1 y2]
    failures = []  # rows [t1 t2 x1 x2 y1 y2 g h]
    nodes = 0
    level = 0
    qf = float(Q)
    t_start = time.perf_counter()
    while frontier.shape[0] > 0:
        if nodes + frontier.shape[0] > node_budget:
            failures.append(
                np.column_stack(
                    [
                        frontier,
                        np.full(frontier.shape[0], np.nan),
                        np.full(frontier.shape[0], np.nan),
                    ]
                )
            )
            break
        level += 1
        next_parts = []
        n_cert = n_disc = n_fail = 0
        for start in range(0, frontier.shape[0], chunk):
            box = frontier[start : start + chunk]
            nodes += box.shape[0]
            t1, t2, x1, x2, y1, y2 = (box[:, i] for i in range(6))
            t0 = (t1 + t2) / 2.0
            x0 = (x1 + x2) / 2.0
            y0 = (y1 + y2) / 2.0
            ht = (t2 - t1) / 2.0
            hx = (x2 - x1) / 2.0
            hy = (y2 - y1) / 2.0
            # discard test: no contained pose in the box
            wmin = np.minimum(float_half_width(t1), float_half_width(t2))
            disc = (
                (x2 < wmin - ALLOW)
                | (x1 > qf - wmin + ALLOW)
                | (y2 < wmin - ALLOW)
                | (y1 > qf - wmin + ALLOW)
            )
            # certification
            g, seg, sstar, _ = float_g_min(t0, x0, y0)
            h = np.hypot(hx, hy) + SQRT2F * ht / (1.0 + t1 * t0)
            cert = (~disc) & (g + h <= delta - ALLOW)
            rest = ~(disc | cert)
            if disc.any():
                discards.append(box[disc])
                n_disc += int(disc.sum())
            if cert.any():
                leaves.append(
                    np.column_stack(
                        [box[cert], seg[cert].astype(float), sstar[cert], g[cert], h[cert]]
                    )
                )
                n_cert += int(cert.sum())
            if rest.any():
                remaining = box[rest]
                sw = np.stack([hx[rest], hy[rest], SQRT2F * ht[rest]], axis=1)
                atfloor = sw.max(axis=1) <= floor
                if atfloor.any():
                    failures.append(
                        np.column_stack(
                            [remaining[atfloor], g[rest][atfloor], h[rest][atfloor]]
                        )
                    )
                    n_fail += int(atfloor.sum())
                    remaining = remaining[~atfloor]
                    sw = sw[~atfloor]
                if remaining.shape[0]:
                    dim = np.argmax(sw, axis=1)  # 0 -> x, 1 -> y, 2 -> t
                    left = remaining.copy()
                    right = remaining.copy()
                    for d, (lo, hi) in ((0, (2, 3)), (1, (4, 5)), (2, (0, 1))):
                        m = dim == d
                        mid = (remaining[m, lo] + remaining[m, hi]) / 2.0
                        left[m, hi] = mid
                        right[m, lo] = mid
                    next_parts.append(left)
                    next_parts.append(right)
        frontier = np.concatenate(next_parts) if next_parts else np.zeros((0, 6))
        if log is not None:
            log(
                f"level {level:2d}: nodes {nodes:9d} cert +{n_cert:8d} "
                f"disc +{n_disc:7d} fail +{n_fail:6d} "
                f"open {frontier.shape[0]:8d}  {time.perf_counter() - t_start:7.1f}s"
            )
    leaf_rows = np.concatenate(leaves) if leaves else np.zeros((0, 10))
    discard_rows = np.concatenate(discards) if discards else np.zeros((0, 6))
    failure_rows = np.concatenate(failures) if failures else np.zeros((0, 8))
    return nodes, leaf_rows, discard_rows, failure_rows


# ----------------------------------------------------------------------------- exact stage


def exact_certify_leaf(
    row: FloatArray, delta: Fraction, delta2_override: Fraction | None = None
) -> bool:
    t1, t2, x1, x2, y1, y2 = (Fraction(float(v)) for v in row[:6])
    seg = int(row[6])
    sstar = Fraction(float(row[7]))
    sstar = min(max(sstar, -HALF_LEN), HALF_LEN)
    t0, x0, y0 = (t1 + t2) / 2, (x1 + x2) / 2, (y1 + y2) / 2
    ht, hx, hy = (t2 - t1) / 2, (x2 - x1) / 2, (y2 - y1) / 2
    h = sqrt_upper(hx * hx + hy * hy) + SQRT2_UP * ht / (1 + t1 * t0)
    xm, ym = P10[seg]
    inside, val = exact_signed(t0, x0, y0, xm + sstar, ym)
    if delta2_override is None:
        # The signed value retains useful penetration slack inside the square.
        if inside:
            return val + h <= delta
        room = delta - h
        return room >= 0 and val <= room * room
    # Inside, the target inequality compares the signed value plus motion with sqrt(D2).
    if inside:
        lhs = val + h  # may be negative
        return lhs <= 0 or lhs * lhs <= delta2_override
    # sqrt(val) + h <= sqrt(D2)  <=> sqrt(val) <= sqrt(D2) - h ; need sqrt(D2) >= h: h^2 <= D2
    if h * h > delta2_override:
        return False
    # A rational lower bound on sqrt(D2) leaves a conservative radius after motion.
    r = sqrt_lower(delta2_override)
    if r < h:
        return False
    return val <= (r - h) * (r - h)


def sqrt_lower(fr: Fraction, bits: int = 40) -> Fraction:
    n, d = fr.numerator, fr.denominator
    scale = 1 << bits
    return Fraction(isqrt(n * d * scale * scale), d * scale)


def exact_discard_box(row: FloatArray) -> bool:
    t1, t2, x1, x2, y1, y2 = (Fraction(float(v)) for v in row[:6])
    wmin = min(half_width(t1), half_width(t2))
    return x2 < wmin or x1 > Q - wmin or y2 < wmin or y1 > Q - wmin


def volume(rows: FloatArray) -> Fraction:
    tot = Fraction(0)
    for r in rows:
        t1, t2, x1, x2, y1, y2 = (Fraction(float(v)) for v in r[:6])
        tot += (t2 - t1) * (x2 - x1) * (y2 - y1)
    return tot


HISTORICAL_PATH = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/"
    "bc-303-first-wave-selection.md"
)


def replay(
    *,
    floor: float = 2.0**-14,
    node_budget: int = 100_000,
    sharper: bool = False,
    log: Callable[[str], None] | None = None,
) -> dict[str, object]:
    """Re-decide the retained length-1/10 theorem; unresolved boxes cannot pass.

    The fixed dyadic domain and Figure-13 segments are part of this claim. The
    bounded CLI intentionally does not expose a new mark/side search.
    """
    if not math.isfinite(floor) or not 0 < floor <= 1:
        raise ValueError("floor must be finite, positive and at most one")
    if not 1 <= node_budget <= 12_000_000:
        raise ValueError("node budget must be between 1 and 12000000")
    delta2 = 2 * Fraction(2121, 500000) ** 2 if sharper else None
    delta_float = math.sqrt(float(delta2)) if delta2 is not None else float(DELTA)
    started = time.perf_counter()
    nodes, leaves, discards, failures = run_cover(delta_float, floor, node_budget, log=log)
    float_seconds = time.perf_counter() - started
    started = time.perf_counter()
    rejected_leaves = sum(not exact_certify_leaf(row, DELTA, delta2) for row in leaves)
    rejected_discards = sum(not exact_discard_box(row) for row in discards)
    measured_volume = volume(leaves) + volume(discards) + volume(failures)
    domain_volume = Fraction(243, 128)
    volume_ok = measured_volume == domain_volume
    invalid = rejected_leaves > 0 or rejected_discards > 0 or not volume_ok
    proved = not invalid and len(failures) == 0 and len(leaves) > 0
    return {
        "status": "invalid" if invalid else "certified" if proved else "unresolved",
        "proved": proved,
        "outer_side": str(Q),
        "segment_length": str(2 * HALF_LEN),
        "delta": str(DELTA) if delta2 is None else f"sqrt({delta2})",
        "floor": floor,
        "node_budget": node_budget,
        "nodes": nodes,
        "certified": len(leaves),
        "discarded": len(discards),
        "failures": len(failures),
        "exact_rejected_leaves": rejected_leaves,
        "exact_rejected_discards": rejected_discards,
        "volume": str(measured_volume),
        "domain_volume": str(domain_volume),
        "volume_ok": volume_ok,
        "float_seconds": round(float_seconds, 3),
        "exact_seconds": round(time.perf_counter() - started, 3),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--floor", type=float, default=2.0**-14)
    parser.add_argument("--node-budget", type=int, default=100_000)
    parser.add_argument(
        "--sharper",
        action="store_true",
        help="replay the retained sqrt(2)*2121/500000 constant",
    )
    args = parser.parse_args(argv)
    try:
        result = replay(floor=args.floor, node_budget=args.node_budget, sharper=args.sharper)
        result["source"] = source_identity(Path(__file__), HISTORICAL_PATH)
        code = 0 if result["proved"] else 1
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        result = {"status": "error", "proved": False, "error": str(error)}
        code = 2
    text = json.dumps(result, indent=2) + "\n"
    if args.output is not None:
        atomic_write_text(args.output, text)
    print(text, end="")
    return code


if __name__ == "__main__":
    sys.exit(main())
