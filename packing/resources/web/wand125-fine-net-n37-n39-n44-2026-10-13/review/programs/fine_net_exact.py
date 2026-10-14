"""Exact arithmetic for a format M rectangle measure on a declared net.

Written for the mathematical review of 14 October 2026
(``docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md``)
from the claim and lemmas N0 to N4, D and C1 of ``packing/sqverify_fast/SOUNDNESS.md``
and the candidate format of the check2 bundles. It imports nothing from the crate, from
``devtools`` or from the source: the eight images, the rotated core, the clipping and the
areas are written here, in Python fractions, and every function is exact.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

Rectangle = tuple[Fraction, Fraction, Fraction, Fraction]
Point = tuple[Fraction, Fraction]

#: The gap every certificate of this kind leaves below its count.
GAP = Fraction(1, 100000)
#: Half the diagonal of a square of side at most one, with a margin: a core of side
#: ``B < 1`` lies within this distance of its centre on each axis.
REACH = Fraction(71, 100)


def refuse_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """A JSON object whose keys are distinct, or a refusal."""
    found: dict[str, Any] = {}
    for key, value in pairs:
        if key in found:
            msg = f"duplicate JSON key {key!r}"
            raise ValueError(msg)
        found[key] = value
    return found


def load_json(data: bytes) -> Any:
    """JSON with every decimal kept as its text, so that it reads as an exact rational."""
    return json.loads(data, parse_float=str, object_pairs_hook=refuse_duplicates)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class Measure:
    """A candidate read exactly: its rows and its merged D4 expansion."""

    n: int
    side: Fraction
    core: Fraction
    step: Fraction
    count: int
    rows: list[tuple[Rectangle, Fraction]]
    images: list[tuple[Rectangle, Fraction]]
    total: Fraction


def images_of(side: Fraction, rect: Rectangle) -> list[Rectangle]:
    """The eight images of ``[x1, x2] x [y1, y2]`` under the symmetries of ``[0, L]^2``.

    The order is the group's elements: the identity, the reflection in ``x = L/2``, in
    ``y = L/2``, the half turn, then the four with the diagonal swap first.
    """
    x1, y1, x2, y2 = rect
    rx1, rx2, ry1, ry2 = side - x2, side - x1, side - y2, side - y1
    return [
        (x1, y1, x2, y2),
        (rx1, y1, rx2, y2),
        (x1, ry1, x2, ry2),
        (rx1, ry1, rx2, ry2),
        (y1, x1, y2, x2),
        (ry1, x1, ry2, x2),
        (y1, rx1, y2, rx2),
        (ry1, rx1, ry2, rx2),
    ]


def expand(
    side: Fraction, rows: list[tuple[Rectangle, Fraction]], factor: Fraction = Fraction(1)
) -> list[tuple[Rectangle, Fraction]]:
    """Every positive row's eight images with density ``factor * mass / (8 area)``,
    coincident images merged by exact key, in first-seen order."""
    merged: dict[Rectangle, Fraction] = {}
    for (x1, y1, x2, y2), mass in rows:
        if mass == 0:
            continue
        density = factor * mass / 8 / ((x2 - x1) * (y2 - y1))
        for image in images_of(side, (x1, y1, x2, y2)):
            merged[image] = merged.get(image, Fraction(0)) + density
    return list(merged.items())


def read_measure(candidate: dict[str, Any]) -> Measure:
    """Read a candidate exactly, refusing what the format refuses."""
    n = candidate["n"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        msg = "n is not a positive integer"
        raise ValueError(msg)
    side, core = Fraction(candidate["L"]), Fraction(candidate["B"])
    net = candidate["proof_net"]
    if set(net) != {"step", "last"} or isinstance(net["last"], bool):
        msg = "proof_net is not exactly {step, last}"
        raise ValueError(msg)
    if not isinstance(net["last"], int) or net["last"] < 1:
        msg = "proof_net.last is not a positive integer"
        raise ValueError(msg)
    step, count = Fraction(net["step"]), int(net["last"]) + 1
    rows: list[tuple[Rectangle, Fraction]] = []
    total = Fraction(0)
    for index, row in enumerate(candidate["rectangles"]):
        if set(row) != {"rectangle", "mass"}:
            msg = f"row {index} has other fields"
            raise ValueError(msg)
        x1, y1, x2, y2 = (Fraction(value) for value in row["rectangle"])
        mass = Fraction(row["mass"])
        if mass < 0:
            msg = f"row {index} has a negative mass"
            raise ValueError(msg)
        if mass > 0 and not (0 <= x1 < x2 <= side and 0 <= y1 < y2 <= side):
            msg = f"row {index} is degenerate or outside [0, L]^2"
            raise ValueError(msg)
        rows.append(((x1, y1, x2, y2), mass))
        total += mass
    return Measure(n, side, core, step, count, rows, expand(side, rows), total)


def direction(step: Fraction, index: int) -> tuple[Fraction, Fraction]:
    """The exact cosine and sine of net angle ``index``, half-angle tangent ``index * step``."""
    t = index * step
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def rho(a: Fraction) -> Fraction:
    """Half the width ``(cos phi + sin phi) / 2`` of a unit square at half-angle tangent a."""
    return (1 + 2 * a - a * a) / (2 * (1 + a * a))


def bin_floor(step: Fraction, index: int) -> Fraction:
    """Lemma D's ``a_r = max(0, r D - D/2)``."""
    return max(Fraction(0), index * step - step / 2)


def domain(side: Fraction, step: Fraction, index: int) -> tuple[Fraction, Fraction]:
    """Lemma D's per-bin centre domain on either axis, ``[rho(a_r), L - rho(a_r)]``."""
    width = rho(bin_floor(step, index))
    return width, side - width


def core_polygon(
    x: Fraction, y: Fraction, c: Fraction, s: Fraction, core: Fraction
) -> list[Point]:
    """The closed square of side ``core`` centred at ``(x, y)`` at angle ``(c, s)``."""
    h = core / 2
    ux, uy, vx, vy = c * h, s * h, -s * h, c * h
    return [
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
    ]


def clip(polygon: list[Point], axis: int, bound: Fraction, *, keep_above: bool) -> list[Point]:
    """Sutherland-Hodgman: the part of a convex polygon on one side of an axis-parallel line."""
    kept: list[Point] = []
    count = len(polygon)
    for k in range(count):
        current, following = polygon[k], polygon[(k + 1) % count]
        inside_current = (current[axis] >= bound) if keep_above else (current[axis] <= bound)
        inside_following = (
            (following[axis] >= bound) if keep_above else (following[axis] <= bound)
        )
        if inside_current:
            kept.append(current)
        if inside_current != inside_following:
            t = (bound - current[axis]) / (following[axis] - current[axis])
            kept.append(
                (
                    current[0] + t * (following[0] - current[0]),
                    current[1] + t * (following[1] - current[1]),
                )
            )
    return kept


def area(polygon: list[Point]) -> Fraction:
    """The area of a simple polygon by the shoelace formula."""
    total = Fraction(0)
    count = len(polygon)
    for k in range(count):
        (x0, y0), (x1, y1) = polygon[k], polygon[(k + 1) % count]
        total += x0 * y1 - x1 * y0
    return abs(total) / 2


def capture(measure: Measure, x: Fraction, y: Fraction, index: int) -> Fraction:
    """The exact mass the closed core at centre ``(x, y)`` and net angle ``index`` captures."""
    c, s = direction(measure.step, index)
    polygon = core_polygon(x, y, c, s, measure.core)
    total = Fraction(0)
    for (x1, y1, x2, y2), density in measure.images:
        if x1 > x + REACH or x2 < x - REACH or y1 > y + REACH or y2 < y - REACH:
            continue
        piece = clip(polygon, 0, x1, keep_above=True)
        piece = clip(piece, 0, x2, keep_above=False)
        piece = clip(piece, 1, y1, keep_above=True)
        piece = clip(piece, 1, y2, keep_above=False)
        if len(piece) >= 3:
            total += density * area(piece)
    return total


def net_facts(core: Fraction, step: Fraction, count: int) -> dict[str, Fraction]:
    """The containment facts of a declared net, exactly."""
    last = step * (count - 1)
    shrink = core * (1 + step)
    return {
        "step": step,
        "count": Fraction(count),
        "endpoint": last,
        "endpoint_check": last * last + 2 * last - 1,
        "rotated_side_upper": shrink,
        "side_margin": 1 - shrink,
        "per_edge_margin": (1 - shrink) / 2,
        "tangent_form": core * (1 + step / (1 - step * step / 4)),
    }


def premises_n0(facts: dict[str, Fraction], count: int) -> dict[str, bool]:
    """Lemma N0's premises (a) to (e) on the declared net, and (f): the last bin holds an
    orientation of ``[0, pi/4]``, that is ``(count - 3/2) D < tan(pi/8)``."""
    floor = (count - Fraction(3, 2)) * facts["step"]
    return {
        "a_positive_step_and_count": facts["step"] > 0 and 2 <= count <= 1 << 16,
        "b_core_fits": facts["rotated_side_upper"] < 1,
        "c_reaches_past_pi_over_4": facts["endpoint_check"] > 0,
        "d_last_tangent_at_most_half": facts["endpoint"] <= Fraction(1, 2),
        "e_tangent_form": facts["tangent_form"] < 1,
        "f_last_bin_holds_an_orientation": floor * floor + 2 * floor - 1 < 0,
    }


def semantic_digest(candidate: dict[str, Any]) -> str:
    """The source's candidate digest: SHA-256 of the compact, key-sorted JSON of the
    fields that define the certificate, ``proof_net`` among them where declared."""
    keys = ["n", "L", "B", "rectangles", "points", "total_mass"]
    keys += ["proof_net"] if "proof_net" in candidate else []
    text = json.dumps(
        {key: candidate[key] for key in keys}, sort_keys=True, separators=(",", ":")
    )
    return sha256(text.encode())
