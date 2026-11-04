"""Independently audit a rectangular fine-net candidate and its saved control points.

This bounded review instrument imports only the standard library. It checks a format-M
rectangle-only candidate with a declared net, a complete maintained coverage receipt,
and a v2 control receipt whose 99/100 mutant refuses at every direction. Exact polygon
clipping recomputes every saved control capture. It neither runs the native verifier nor
proves coverage between points; PASS is not a universal coverage or registry verdict.

An axis refusal reports no capture, only the sweep's least certified lower bound. It is
judged against the enclosure the native vertex sweep held at its least vertex, which
`axis_enclosure` recomputes by walking that column as the crate's `axis.rs` does, in
`interval.rs`'s outward-rounded binary64 steps: the bound must be the recomputed lower
end to the bit, and the exact capture must lie in the enclosure (F-1 of the 14 October
review, as the census control judges it since #892). That walk is a transcription of the
crate's arithmetic, not an independent method; the capture it is compared with is this
instrument's own.

A candidate may carry a `derived_from` provenance string beside the format's fields; it
is admitted and not read. Run with --help for the required case parameters. Rational
strings have their literal values; numeric receipt coordinates denote binary64 values,
as in the maintained control writer. No commit or result number enters the verdict.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

type Point = tuple[Fraction, Fraction]
type Rectangle = tuple[Fraction, Fraction, Fraction, Fraction]  # x0, x1, y0, y1


class AuditError(ValueError):
    """An input or exact comparison fails this instrument's stated scope."""


def require(condition: object, message: str) -> None:
    """Checks remain active under python -O."""
    if not condition:
        raise AuditError(message)


def rational(value: Any) -> Fraction:
    require(type(value) in (str, int, float), "expected a rational string or JSON number")
    return Fraction(value)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> Any:
    raise AuditError(f"non-finite JSON number: {value}")


def read_json(data: str | bytes) -> Any:
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=reject_constant)


@dataclass(frozen=True)
class Measure:
    n: int
    side: Fraction
    core: Fraction
    step: Fraction
    count: int
    mass: Fraction
    source_count: int
    rectangles: dict[Rectangle, Fraction]
    #: The expanded rectangles in the order the crate's admission first sees them
    #: (`certificate.rs`, `d4_images`), which is the order its axis sweep sums in.
    axis_order: tuple[Rectangle, ...] = ()

    @property
    def last_tangent(self) -> Fraction:
        return (self.count - 1) * self.step


#: The fields of the narrow rectangle-only format M this audit admits.
CANDIDATE_FIELDS = frozenset({"n", "L", "B", "proof_net", "total_mass", "points", "rectangles"})
#: Provenance a candidate may carry beside them, as a string, which nothing here reads:
#: `derived_from`, the note a regenerated certificate states its origin in (#890's
#: s(94) dilation), and which the crate's admission ignores too.
PROVENANCE_FIELDS = frozenset({"derived_from"})


def candidate_measure(data: dict[str, Any], n: int, side: Fraction) -> Measure:
    """Admit the narrow rectangle-only form needed by this audit, then expand D4."""
    require(
        CANDIDATE_FIELDS <= set(data) <= CANDIDATE_FIELDS | PROVENANCE_FIELDS,
        "candidate must have the rectangle-only format-M audit fields",
    )
    require(
        all(type(data[key]) is str for key in PROVENANCE_FIELDS & set(data)),
        "a provenance field must be a string",
    )
    require(type(data["n"]) is int and data["n"] == n and n > 0, "candidate count differs")
    require(rational(data["L"]) == side and side > 0, "candidate side differs")
    require(data["points"] == [], "point masses are outside this audit")
    net = data["proof_net"]
    require(set(net) == {"step", "last"}, "unexpected net fields")
    require(type(net["last"]) is int, "net last must be a JSON integer")
    core, step = rational(data["B"]), rational(net["step"])
    count = net["last"] + 1
    require(0 < core < 1 and step > 0 and 2 <= count <= 2**16, "invalid core or net size")
    last = (count - 1) * step
    require(last <= Fraction(1, 2) and last * last + 2 * last - 1 > 0, "net misses endpoint")
    lower = last - step / 2
    require(lower * lower + 2 * lower - 1 < 0, "last bin starts beyond the folded range")
    require(core * (1 + step) < 1, "strict core shrink fails")
    require(core * (1 + step / (1 - step * step / 4)) < 1, "tangent shrink fails")
    require(side * side >= 2 * core * core and side >= 2 * rho(lower), "empty centre domain")
    rectangles: dict[Rectangle, Fraction] = {}
    order: dict[Rectangle, None] = {}
    mass = Fraction(0)
    for row in data["rectangles"]:
        require(set(row) == {"rectangle", "mass"}, "unexpected rectangle fields")
        x0, y0, x1, y1 = map(rational, row["rectangle"])
        weight = rational(row["mass"])
        require(weight >= 0, "negative rectangle mass")
        mass += weight
        if weight == 0:
            continue
        require(0 <= x0 < x1 <= side and 0 <= y0 < y1 <= side, "rectangle outside container")
        density = weight / (8 * (x1 - x0) * (y1 - y0))
        require(64 * density <= 2**32, "source-row density guard exceeded")
        for swap in (False, True):
            ax, bx, ay, by = (y0, y1, x0, x1) if swap else (x0, x1, y0, y1)
            for flip_x in (False, True):
                for flip_y in (False, True):
                    left, right = (side - bx, side - ax) if flip_x else (ax, bx)
                    bottom, top = (side - by, side - ay) if flip_y else (ay, by)
                    image = (left, right, bottom, top)
                    rectangles[image] = rectangles.get(image, Fraction(0)) + density
        order.update(dict.fromkeys(crate_images(side, x0, y0, x1, y1)))
    require(0 < mass < n and mass == rational(data["total_mass"]), "total mass is invalid")
    require(all(d <= 2**96 for d in rectangles.values()), "expanded density guard exceeded")
    integrated = sum(
        ((b - a) * (d - c) * q for (a, b, c, d), q in rectangles.items()), Fraction(0)
    )
    require(integrated == mass, "D4 expansion changed the mass")
    require(set(order) == set(rectangles), "D4 expansion orders differ")
    return Measure(
        n, side, core, step, count, mass, len(data["rectangles"]), rectangles, tuple(order)
    )


def crate_images(
    side: Fraction, x0: Fraction, y0: Fraction, x1: Fraction, y1: Fraction
) -> list[Rectangle]:
    """The eight images of a row in the crate's `d4_images` order, written as this
    instrument writes a rectangle: the identity, the reflections in x = L/2 and y = L/2,
    the half turn, then the same four after the diagonal swap."""
    rx0, rx1, ry0, ry1 = side - x1, side - x0, side - y1, side - y0
    return [
        (x0, x1, y0, y1),
        (rx0, rx1, y0, y1),
        (x0, x1, ry0, ry1),
        (rx0, rx1, ry0, ry1),
        (y0, y1, x0, x1),
        (ry0, ry1, x0, x1),
        (y0, y1, rx0, rx1),
        (ry0, ry1, rx0, rx1),
    ]


def rho(tangent: Fraction) -> Fraction:
    return (1 + 2 * tangent - tangent * tangent) / (2 * (1 + tangent * tangent))


def in_domain(measure: Measure, pose: Sequence[Any], index: int) -> bool:
    if type(index) is not int or not 0 <= index < measure.count or len(pose) != 2:
        return False
    high = measure.side - rho(max(Fraction(0), index * measure.step - measure.step / 2))
    return all(measure.side / 2 <= rational(value) <= high for value in pose)


def clip_polygon(
    polygon: list[Point], a: Fraction, b: Fraction, limit: Fraction
) -> list[Point]:
    """Intersect a convex polygon with ax + by <= limit, using exact fractions."""
    if not polygon:
        return []
    result: list[Point] = []
    old = polygon[-1]
    old_value = a * old[0] + b * old[1] - limit
    for current in polygon:
        value = a * current[0] + b * current[1] - limit
        if (old_value <= 0) != (value <= 0):
            part = old_value / (old_value - value)
            result.append(
                (old[0] + part * (current[0] - old[0]), old[1] + part * (current[1] - old[1]))
            )
        if value <= 0:
            result.append(current)
        old, old_value = current, value
    return result


def polygon_area(polygon: list[Point]) -> Fraction:
    return (
        abs(
            sum(
                (
                    x * v - u * y
                    for (x, y), (u, v) in zip(polygon, polygon[1:] + polygon[:1], strict=True)
                ),
                Fraction(0),
            )
        )
        / 2
    )


def check_deadline(deadline: float) -> None:
    require(time.monotonic() <= deadline, "audit time budget exceeded")


def capture_at(
    measure: Measure, pose: Sequence[Any], index: int, deadline: float = float("inf")
) -> Fraction:
    """Integrate the measure on one closed core; this is not a coverage search."""
    cx, cy = map(rational, pose)
    tangent = index * measure.step
    cosine = (1 - tangent * tangent) / (1 + tangent * tangent)
    sine = 2 * tangent / (1 + tangent * tangent)
    half = measure.core / 2
    extent = half * (cosine + sine)
    planes = (
        (cosine, sine, half + cosine * cx + sine * cy),
        (-cosine, -sine, half - cosine * cx - sine * cy),
        (-sine, cosine, half - sine * cx + cosine * cy),
        (sine, -cosine, half + sine * cx - cosine * cy),
    )
    total = Fraction(0)
    for (x0, x1, y0, y1), density in measure.rectangles.items():
        check_deadline(deadline)
        if x1 <= cx - extent or x0 >= cx + extent or y1 <= cy - extent or y0 >= cy + extent:
            continue
        polygon = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for a, b, limit in planes:
            polygon = clip_polygon(polygon, a, b, limit)
        total += density * polygon_area(polygon)
    return total


type Interval = tuple[float, float]

#: `interval.rs`'s step constants: no gap between adjacent binary64 values exceeds
#: `2^-52 |x|`, and the least positive subnormal is the gap at and below the normal range.
GAP, TINY = 2.0**-52, 5e-324


def step_down(x: float) -> float:
    return x - (abs(x) * GAP + TINY)


def step_up(x: float) -> float:
    return x + (abs(x) * GAP + TINY)


def select_min(a: float, b: float) -> float:
    """`interval.rs`'s `fmin`: `a` when `a < b`, else `b`, carrying a NaN in `a`."""
    return min(b, a) + a * 0.0


def select_max(a: float, b: float) -> float:
    """`interval.rs`'s `fmax`: `a` when `a > b`, else `b`, carrying a NaN in `a`."""
    return max(b, a) + a * 0.0


def iv_plus(a: Interval, b: Interval) -> Interval:
    return step_down(a[0] + b[0]), step_up(a[1] + b[1])


def iv_minus(a: Interval, b: Interval) -> Interval:
    return step_down(a[0] - b[1]), step_up(a[1] - b[0])


def iv_times(a: Interval, b: Interval) -> Interval:
    p, q, r, s = a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]
    low = select_min(select_min(p, q), select_min(r, s))
    return step_down(low), step_up(select_max(select_max(p, q), select_max(r, s)))


def iv_scale(a: Interval, k: Interval) -> Interval:
    """`Iv::mul_nonneg`: the product with a nonnegative `k`, sign-selected on `a`."""
    low = a[0] * k[0] if a[0] >= 0.0 else a[0] * k[1]
    high = a[1] * k[1] if a[1] >= 0.0 else a[1] * k[0]
    return step_down(low), step_up(high)


def tight(q: Fraction) -> Interval:
    """The nearest binary64 values at most and at least `q` (`exact.rs`'s `enclose`)."""
    x = float(q)
    if Fraction(x) == q:
        return x, x
    if Fraction(x) < q:
        return x, math.nextafter(x, math.inf)
    return math.nextafter(x, -math.inf), x


def axis_enclosure(measure: Measure, factor: Fraction, pose: Sequence[Any]) -> Interval | None:
    """The enclosure the crate's axis sweep holds at the vertex `pose` of the measure
    with every density scaled by `factor`, on `[L/2, L - 1/2]^2`: its column walked as
    `axis.rs`'s `verify_axis` walks it, in `interval.rs`'s steps. Each step rounds to
    nearest and then moves outward by at least one gap, so the result encloses the exact
    capture whatever path it takes; summing in the crate's order with the crate's
    operations reproduces the crate's interval. None off the event grid, without the
    crate's order, or where the enclosure is not finite."""
    x, y = map(rational, pose)
    h, lower = measure.core / 2, measure.side / 2
    upper = measure.side - rho(Fraction(0))
    rects = [(key, factor * measure.rectangles[key]) for key in measure.axis_order]
    if not rects:
        return None
    xs, ys = {lower, upper}, {lower, upper}
    for (x0, x1, y0, y1), _density in rects:
        xs.update(p for e in (x0, x1) for p in (e - h, e + h) if lower <= p <= upper)
        ys.update(p for e in (y0, y1) for p in (e - h, e + h) if lower <= p <= upper)
    events = sorted(ys)
    where = {value: position for position, value in enumerate(events)}
    if x not in xs or y not in where:
        return None
    grid = [tight(value) for value in events]
    half, centre = tight(h), tight(x)

    def overlap(c: Interval, a: Interval, b: Interval) -> Interval:
        right = iv_plus(c, half)
        right = (select_min(right[0], b[0]), select_min(right[1], b[1]))
        left = iv_minus(c, half)
        left = (select_max(left[0], a[0]), select_max(left[1], a[1]))
        width = iv_minus(right, left)
        return select_max(width[0], 0.0), select_max(width[1], 0.0)

    zero: Interval = (0.0, 0.0)
    delta = [zero] * len(events)
    value, slope = zero, zero
    for (x0, x1, y0, y1), density in rects:
        across = overlap(centre, tight(x0), tight(x1))
        if across[1] <= 0.0:
            continue
        weight = iv_scale(across, tight(density))
        value = iv_plus(value, iv_scale(weight, overlap(grid[0], tight(y0), tight(y1))))
        for point, sign in ((y0 - h, 1), (y1 - h, -1), (y0 + h, -1), (y1 + h, 1)):
            signed = weight if sign > 0 else (-weight[1], -weight[0])
            if point < lower:
                slope = iv_plus(slope, signed)
            elif point <= upper:
                delta[where[point]] = iv_plus(delta[where[point]], signed)
    slope = iv_plus(slope, delta[0])
    for j in range(where[y]):
        value = iv_plus(value, iv_times(slope, iv_minus(grid[j + 1], grid[j])))
        slope = iv_plus(slope, delta[j + 1])
    return value if math.isfinite(value[0]) and math.isfinite(value[1]) else None


def require_complete_indices(rows: list[dict[str, Any]], count: int) -> None:
    indices = [row["r"] for row in rows]
    require(all(type(index) is int for index in indices), "direction index must be an integer")
    require(
        sorted(indices) == list(range(count)), "directions missing, duplicated or out of range"
    )


def check_direction_log(rows: list[dict[str, Any]], count: int) -> dict[str, Any]:
    require(bool(rows), "empty direction log")
    directions, summary = rows[:-1], rows[-1]
    require_complete_indices(directions, count)
    for row in directions:
        require(row["verdict"] == "verified", "direction was not verified")
        require(
            rational(row["threshold"]) == 1 and rational(row["min_certified_lower_bound"]) >= 1,
            "direction threshold or bound invalid",
        )
    require(
        summary["status"] == "VERIFIED" and summary["directions"] == count,
        "invalid coverage summary",
    )
    require(
        summary["refused_directions"] == [] and summary["fault_injected_at_box"] is None,
        "coverage refusal or injected fault",
    )
    return summary


def check_bindings(
    measure: Measure,
    summary: dict[str, Any],
    entry: dict[str, Any],
    control: dict[str, Any],
    *,
    candidate_sha: str,
) -> None:
    # Bind downloaded candidate bytes to the retained runtime inputs, not Git source.
    require(
        candidate_sha
        == entry["candidate_sha256"]
        == control["candidate_sha256"]
        == summary["premises"]["input_sha256"],
        "candidate digest mismatch",
    )
    require(entry["status"] == "VERIFIED" and entry["returncode"] == 0, "census did not verify")
    require(
        entry["directions_verified"] == measure.count and entry["refused_directions"] == [],
        "census directions differ",
    )
    require(entry["premises"] == summary["premises"], "census premises differ")
    require(
        rational(entry["threshold"]) == rational(summary["threshold"]) == 1,
        "summary threshold differs",
    )
    # The build product has no Git identity; coverage and controls must name one binary.
    require(
        entry["binary_sha256"] == control["binary_sha256"], "control binary identity differs"
    )
    premises = summary["premises"]
    exact = {
        "B": measure.core,
        "D": measure.step,
        "L": measure.side,
        "mass_exact": measure.mass,
        "mass_below_n": measure.n - measure.mass,
        "net_last_tangent": measure.last_tangent,
        "shrink_bound": measure.core * (1 + measure.step),
    }
    for key, value in exact.items():
        require(rational(premises[key]) == value, f"premise differs: {key}")
    fields = {
        "format": "M",
        "centre_domain": "per-bin",
        "net_origin": "proof_net",
        "expanded_points": 0,
        "expanded_segments": 0,
        "expanded_rectangles": len(measure.rectangles),
        "n": measure.n,
        "angle_count": measure.count,
        "source_rectangles": measure.source_count,
    }
    for key, value in fields.items():
        require(premises[key] == value, f"premise differs: {key}")
    require(summary["build"] == entry["build"] == control["build"], "build identities differ")
    require(summary["build"]["profile"] == "release", "receipt is not from a release build")
    require(
        control["n"] == measure.n and rational(control["L"]) == measure.side,
        "control claim differs",
    )


def check_refusal(
    measure: Measure, row: dict[str, Any], factor: Fraction, deadline: float
) -> Fraction:
    index = row["r"]
    require(in_domain(measure, row["pose"], index), f"refusal pose outside domain: {index}")
    flags = (
        "coverage_refusal",
        "in_domain",
        "capture_below_1",
        "captures_agree",
        "original_at_least_1",
    )
    require(all(row[key] is True for key in flags), f"invalid refusal flags: {index}")
    value = capture_at(measure, row["pose"], index, deadline)
    require(
        value >= 1 and factor * value < 1,
        f"control does not separate original and mutant: {index}",
    )
    require(factor * value == rational(row["capture"]), f"control capture differs: {index}")
    if row["verdict"] == "refused":
        require(
            index == 0 and row["method"] == "axis-vertex-sweep",
            f"invalid axis refusal: {index}",
        )
        bound = rational(row["crate_lower_bound"])
        # The axis sweep certifies the lower end of the enclosure it held at its least
        # vertex. The bound must be the recomputed lower end, to the bit, and the exact
        # capture must lie in that enclosure: no allowance beyond the sweep's own width.
        enclosure = axis_enclosure(measure, factor, row["pose"])
        require(enclosure is not None, f"axis refusal vertex has no sweep enclosure: {index}")
        low, high = map(Fraction, enclosure or (0.0, 0.0))
        require(low == bound, "axis refusal bound is not the sweep's recomputed lower end")
        require(
            low <= factor * value <= high,
            "axis refusal capture lies outside the sweep's enclosure",
        )
        stored = row.get("sweep_enclosure")
        require(
            stored is None or [rational(end) for end in stored] == [low, high],
            "receipt's sweep enclosure differs from the recomputed one",
        )
    elif row["verdict"] == "counterexample-candidate":
        require(row["crate_exact_below_threshold"] is True, f"missing exact refusal: {index}")
    else:
        raise AuditError(f"invalid refusal verdict: {index}")
    return value


def check_controls(
    measure: Measure, entry: dict[str, Any], control: dict[str, Any], deadline: float
) -> dict[str, Any]:
    require(
        control["kind"] == "sqverify-fast-control/v2"
        and control["status"] == "CONTROLS_REFUSED",
        "invalid control receipt",
    )
    original, scaled, near = control["runs"]
    require(
        original["name"] == "original"
        and original["returncode"] == 0
        and original["verdict"] == "verified",
        "original control did not verify",
    )
    require(
        scaled["name"] == "scaled-99-100" and near["name"] == "near-threshold",
        "unexpected control names",
    )
    sweep, factor = scaled["sweep"], rational(scaled["mutation"]["factor"])
    require(factor == Fraction(99, 100), "unexpected whole-net mutation")
    refusals = sweep["refused"]
    require_complete_indices(refusals, measure.count)
    require(
        sweep["directions"] == sweep["net_directions"] == measure.count,
        "control direction count differs",
    )
    require(
        sweep["indices_complete"] is True and sweep["premises_agree"] is True,
        "control premises incomplete",
    )
    require(
        sweep["returncode"] == 1 and sweep["summary_status"] == "REFUSED",
        "mutant did not refuse",
    )
    require(
        sweep["verified_directions"] == []
        and sweep["summary_refused_directions"] == list(range(measure.count)),
        "mutant direction summary differs",
    )
    require(sweep["fault_injected_at_box"] is None, "mutant fault injected")
    values = [check_refusal(measure, row, factor, deadline) for row in refusals]
    leaf, index = entry["least_bound_leaf_exact"], control["index"]
    require(
        leaf["r"] == index and leaf["centre"] == control["centre"], "least-bound leaf differs"
    )
    require(
        control["captures_agree"] is True and in_domain(measure, control["centre"], index),
        "invalid selected centre",
    )
    exact = capture_at(measure, control["centre"], index, deadline)
    require(
        exact
        == rational(leaf["exact_coverage"])
        == rational(control["exact_capture_crate"])
        == rational(control["exact_capture_independent"])
        and exact >= 1,
        "selected-centre capture differs",
    )
    near_factor, near_pose = rational(near["mutation"]["factor"]), near["witness"]["exact_pose"]
    require(0 < near_factor < 1, "invalid near-threshold factor")
    require(
        near["returncode"] == 1
        and near["verdict"] == "counterexample-candidate"
        and near["exact_below_threshold"] is True,
        "near-threshold mutant did not refuse",
    )
    require(in_domain(measure, near_pose, index), "near-threshold witness outside domain")
    require(
        exact * near_factor == rational(near["mutation"]["capture_at_centre"]) < 1,
        "near-threshold selected capture differs",
    )
    near_capture = capture_at(measure, near_pose, index, deadline) * near_factor
    require(
        near_capture
        == rational(near["witness"]["exact_coverage"])
        == rational(near["mutation"]["capture_at_witness"])
        < 1,
        "near-threshold witness capture differs",
    )
    return {
        "independent_refusal_points": len(values),
        "original_at_control_min": float(min(values)),
        "original_at_control_max": float(max(values)),
        "least_leaf_index": index,
        "least_leaf_original_capture": float(exact),
        "near_factor": str(near_factor),
        "near_capture": float(near_capture),
    }


def audit(
    root: Path,
    packet: str,
    certificate: str,
    n: int,
    side: Fraction,
    *,
    seconds: float,
    candidate_path: str | None = None,
) -> dict[str, Any]:
    """Audit one case. The candidate is `release/certificates/CERTIFICATE/candidate.json.gz`
    in the packet, as the wand125 release packets keep it, or `candidate_path`, a relative
    path inside the packet for one kept as its source published it (#890's
    `source/certificate/n94_L9965.json.gz`); the receipts bind it by digest either way."""
    started = time.monotonic()
    require(0 < seconds <= 300, "time budget must be between 0 and 300 seconds")
    for name in (packet, certificate):
        require(
            name not in ("", ".", "..") and Path(name).name == name,
            "case names must be single path components",
        )
    inside = (
        Path(candidate_path)
        if candidate_path is not None
        else Path("release/certificates") / certificate / "candidate.json.gz"
    )
    require(
        not inside.is_absolute()
        and inside.parts
        and all(part not in ("", ".", "..") for part in inside.parts),
        "the candidate path must be a relative path inside the packet",
    )
    candidate = root / "packing/resources/web" / packet / inside
    raw = candidate.read_bytes()
    measure = candidate_measure(read_json(gzip.decompress(raw)), n, side)
    base = root / "packing/benchmarks/measure-verifier/census-mixed"
    rows = [
        read_json(line)
        for line in gzip.decompress(
            (base / packet / f"{certificate}.jsonl.gz").read_bytes()
        ).splitlines()
    ]
    summary = check_direction_log(rows, measure.count)
    entries = [
        row
        for row in read_json((base / "census.json").read_bytes())["cases"].values()
        if row["packet"] == packet and row["certificate"] == certificate
    ]
    require(len(entries) == 1, "expected exactly one census case")
    entry = entries[0]
    control = read_json((base / packet / f"{certificate}.control.json").read_bytes())
    require(
        control["packet"] == packet and control["certificate"] == certificate,
        "control case differs",
    )
    candidate_sha = hashlib.sha256(raw).hexdigest()
    check_bindings(measure, summary, entry, control, candidate_sha=candidate_sha)
    results = check_controls(measure, entry, control, started + seconds)
    check_deadline(started + seconds)
    return {
        "status": "PASS",
        "packet": packet,
        "certificate": certificate,
        "n": n,
        "L": str(side),
        "B": str(measure.core),
        "D": str(measure.step),
        "rectangles": measure.source_count,
        "expanded_rectangles": len(measure.rectangles),
        "mass": str(measure.mass),
        "mass_gap": str(n - measure.mass),
        "shrink_product": str(measure.core * (1 + measure.step)),
        "shrink_gap": str(1 - measure.core * (1 + measure.step)),
        "endpoint_polynomial": str(measure.last_tangent**2 + 2 * measure.last_tangent - 1),
        "tangent_shrink_product": str(
            measure.core * (1 + measure.step / (1 - measure.step**2 / 4))
        ),
        "candidate_gzip_sha256": candidate_sha,
        "recorded_native_source_sha256": summary["build"]["source_sha256"],
        "source_identity_scope": "historical receipt metadata; current crate source not read",
        **results,
        "coverage_replay": "not run; retained complete native receipt inspected",
        "seconds": round(time.monotonic() - started, 3),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, required=True, help="checkout or exported evidence tree"
    )
    parser.add_argument("--packet", required=True)
    parser.add_argument("--certificate", required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--side", type=Fraction, required=True)
    parser.add_argument(
        "--candidate",
        default=None,
        help="the candidate's path inside the packet "
        "(default: release/certificates/CERTIFICATE/candidate.json.gz)",
    )
    parser.add_argument(
        "--seconds",
        type=float,
        default=300,
        help="cooperative budget, checked during point evaluation (maximum 300)",
    )
    args = parser.parse_args(argv)
    try:
        result = audit(
            args.root,
            args.packet,
            args.certificate,
            args.n,
            args.side,
            seconds=args.seconds,
            candidate_path=args.candidate,
        )
    except (
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        OSError,
        EOFError,
        OverflowError,
        ZeroDivisionError,
    ) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
