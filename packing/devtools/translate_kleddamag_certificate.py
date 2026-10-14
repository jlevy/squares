#!/usr/bin/env python3
"""Translate Overbeck's external n = 17 measure into this repository's threshold schema.

The retained artifact under `packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/`
carries a weighted covering measure -- 1,134 point orbits and 253 two-of-three orbits over
the container ``L = 4613/1000`` -- stated in a *restricted parent-centre* language this
repository does not implement. Its catalogue assigns to every parent half-angle interval
``[a, b]`` a concentric core ``(t, B)`` and then quantifies only over centres a legal
side-``A`` parent could have, the square ``[r, L - r]^2`` with
``r = A min(c(a) + s(a), c(b) + s(b)) / 2``. Nothing in this repository registers that
statement, and the two-route gate cannot read it.

This tool restates the *same measure* in the unrestricted language of
`sqpack.fractional.threshold`: the point orbits expanded to their D4 sites as point atoms,
the two-of-three orbits expanded to their physical triples as ``2``-of-``3`` threshold
atoms, one shrink ``B`` for every direction, and a uniform half-tangent net. Nothing about
the parent survives the translation, so ``Condition 5'`` then quantifies over *every*
closed ``B``-square at a net direction inside the container -- a strict superset of the
artifact's centres, since ``B <= A`` and each row's own check
``B (c(t) + s(t)) / 2 <= r`` puts the core's envelope inside the parent's. A pass would
therefore hand the repository the external bound in its own gate, and that implication is
one-sided in the useful direction.

A *fail* is weaker than it looks, and the difference matters enough to state here. The
whole-net decision replaces the artifact's adaptive per-row selector -- a core angle within
``0.006`` degrees of its parent band, a per-row ``B`` anywhere in the measured band -- with
fixed net directions and one ``B``, so it varies the selector and the net alongside the
domain. Its least charge is an *upper bound* on what the parent-centre restriction costs
and never a measurement of it. The measurement is ``--charge-at`` below, which moves the
centre and nothing else. Neither reading is worth anything if the translation moved the
object, which is what the controls below are for.

Three choices in the translation, each of which could be made differently and none of
which is free:

* **``B`` is the smallest core side in the catalogue**, ``min`` over the 7,853 rows, because
  the schema carries one shrink and the row-wise guarantee is only as strong as its weakest
  core. Smaller ``B`` captures fewer sites, so this is the conservative reading of
  ``Condition 5'`` and simultaneously the sharper one for the dilation corollary, whose
  supremum ``L sqrt(1 + D^2) / (B (1 + D))`` falls as ``B`` rises.
* **``L`` is the artifact's own container side, unscaled.** The emitted record therefore
  claims ``s(17) >= 4613/1000``, which is *below* the registered ``T-032``; the external
  value is recovered only through `devtools.dilation_corollary`, exactly as ``A1``'s row in
  X-041 sets out. Scaling the sites by ``1 / A`` instead would put ``B / A`` past what
  ``Condition 4`` admits on any net this repository runs.
* **Zero-weight sites are not emitted as point atoms.** All 2,244 of them are triple sites,
  so every one of them still reaches the event grid through its threshold atom, and the
  charge function is unchanged site for site. The emitted atom list is the 6,744 sites of
  positive weight.

The controls, all exact, all decided before a byte is written:

``C1`` the expanded structure -- 8,988 sites, 6,744 of them positive, 852 positive orbits,
2,008 physical triples -- against the artifact's own retained `evidence/structure.json`;
``C2`` every site distinct and inside the container;
``C3`` every point orbit a full D4 orbit of one weight, and every threshold orbit a full D4
orbit of triples, re-derived here rather than read from the file;
``C4`` the point budget, the triple budget and their total against ``budget_units``;
``C5`` the artifact's own counting inequality ``17 * minimum_units > budget_units``;
``C6`` the emitted atoms closed under `sqpack.fractional.certificate.d4_images` at equal
weight, which is the gate's own ``Condition 1`` predicate, decided here so the gate is not
the first thing to see it;
``C7`` ``B (1 + D) < 1`` at the requested net, which is ``Condition 4``;
``C8`` -- the one that matters -- the artifact's own per-row minima, recomputed *from the
expanded sites* over the artifact's own restricted centre domain and required to match the
retained Python replay exactly, row by row, on the minimum, the slab count and the cell
count. The row attaining the global minimum is always in the sample, so ``C8`` reproduces
``minimum_units`` itself. A translation that cannot do that has moved the object and no
unrestricted verdict taken from it means anything; the tool refuses to emit.

``C8`` is a second implementation of the artifact's sweep, not a call into its checker: a
segment-free slab sweep over the same signed rectangle expansion
``1[i + j + k >= 2] = ij + ik + jk - 2ijk``, in ``int64`` under the artifact's own
``sum(w) + 5 sum(w_triple) < 2^50`` headroom, with the polygon crossings taken in exact
integer arithmetic. It agrees with the retained replay on the cell counts as well as the
minima, which a differently-partitioned sweep would not.

Three measurements ride on the same expansion, each behind its own flag because each
costs something:

``--charge-at`` (``C9``) charges one catalogue row's *own* core -- its own ``t``, its own
``B``, the artifact's own sites -- at one named centre, by membership counting in exact
rationals. It is the un-confounded reading of what the parent-centre restriction carries,
because it moves the centre and nothing else; the whole-net decision below moves the
domain, the selector and the net together and can only bound it.

``--point-only-rows`` is the ``H-235`` screen: the same restricted rows with every
two-of-three atom dropped, deciding whether the triples are load-bearing at these weights.

``--sweep-certificate`` with ``--sweep-directions`` decides ``Condition 5'`` at a sample of
an emitted record's own net directions, reading the bytes through
`devtools.decide_threshold_certificate`'s loader and running that gate's own exact sweep.
``Condition 5'`` is a conjunction over directions, so a sample refuses and never accepts;
it exists because the whole net is hours of gate at this support size and a lane that only
needs to refuse should not pay for them.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python \
        -m devtools.translate_kleddamag_certificate --output cert.json --control-rows 200
    uv run --frozen --all-extras --group dev python \
        -m devtools.translate_kleddamag_certificate --output cert.json \
        --direction-steps 288 --report report.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from bisect import bisect_left, bisect_right
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from math import lcm
from multiprocessing import get_context
from pathlib import Path
from typing import Any, cast

import numpy as np

from devtools.decide_threshold_certificate import load
from sqpack.fractional.certificate import d4_images
from sqpack.fractional.threshold import ThresholdCertificate, exact_charge, minimum_charge

PACKING = Path(__file__).resolve().parent.parent
ARTIFACT = (
    PACKING
    / "resources/web/n17-kleddamag-certified-bound-2026-09-21"
    / "kleddamag-17-squares-certified-bound"
)
SOURCE = ARTIFACT / "global-certificate.json"
STRUCTURE = ARTIFACT / "evidence/structure.json"
REPLAY = ARTIFACT / "evidence/average4-adaptive-r1.python-replay.json"

#: The repository's standard half-tangent ceiling: ``tan(pi/8)`` rounded down on the
#: 500000 scale, the same value the frozen n = 11 threshold certificate carries. The
#: artifact's catalogue ends at exactly this tangent, which is why the two nets can be
#: compared at all.
ANGLE_LIMIT = Fraction(207107, 500000)

#: The artifact's own overflow headroom: no accumulator can exceed the sum of the point
#: weights plus five times the sum of the triple weights, and it checks that against this.
INT64_HEADROOM = 2**50


class TranslationError(ValueError):
    """The source cannot be read, or a control refuses the translation."""


@dataclass(frozen=True, slots=True)
class Expansion:
    """The artifact's measure with every orbit expanded, in the artifact's own order.

    ``sites`` holds integer coordinates on the source's ``coordinate_denominator``, in the
    order the ``threshold_orbits`` indices refer to: orbit by orbit in file order, and
    inside an orbit the sorted set of its eight D4 images. ``weights`` is one point weight
    per site on the source's ``weight_denominator``; ``triples`` and ``triple_weights`` are
    the physical triples and their weights on the same scale.
    """

    outer_side: Fraction
    parent_side: Fraction
    coordinate_denominator: int
    weight_denominator: int
    point_orbits: int
    positive_point_orbits: int
    threshold_orbit_count: int
    sites: tuple[tuple[int, int], ...]
    weights: tuple[int, ...]
    triples: tuple[tuple[int, int, int], ...]
    triple_weights: tuple[int, ...]
    rows: tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]
    minimum_units: int
    budget_units: int

    @property
    def point_units(self) -> int:
        return sum(self.weights)

    @property
    def triple_units(self) -> int:
        return sum(self.triple_weights)

    @property
    def least_core_side(self) -> Fraction:
        return min(row[3] for row in self.rows)

    @property
    def greatest_core_side(self) -> Fraction:
        return max(row[3] for row in self.rows)

    def point(self, index: int) -> tuple[Fraction, Fraction]:
        x, y = self.sites[index]
        return Fraction(x, self.coordinate_denominator), Fraction(
            y, self.coordinate_denominator
        )


def _integer(value: object, field: str) -> int:
    if type(value) is not int:
        raise TranslationError(f"field {field!r} must be a JSON integer, got {value!r}")
    return cast(int, value)


def _exact(value: object, field: str) -> Fraction:
    """Parse a rational the way the source spells it: a string, never a float."""
    if not isinstance(value, str):
        raise TranslationError(
            f"field {field!r} must be an exact rational string, got {value!r}"
        )
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise TranslationError(f"field {field!r} is not an exact rational: {error}") from None


def _refuse_float(text: str) -> float:
    raise TranslationError(
        f"inexact JSON number {text!r} in the source; nothing here may be float"
    )


def read_source(path: Path) -> tuple[dict[str, Any], str]:
    """The source object and the SHA-256 of the bytes it was read from."""
    data = path.read_bytes()
    decoded = cast(
        object,
        json.loads(data, parse_float=_refuse_float, parse_constant=_refuse_float),
    )
    if not isinstance(decoded, dict):
        raise TranslationError("the source's top-level JSON value must be an object")
    return cast(dict[str, Any], decoded), hashlib.sha256(data).hexdigest()


def orbit(x: int, y: int, span: int) -> list[tuple[int, int]]:
    """The sorted D4 orbit of one integer site about the container's centre.

    The same eight images `sqpack.fractional.certificate.d4_images` takes, in the same
    sorted-set order the artifact's two independent expanders both use, which is what makes
    the ``threshold_orbits`` indices mean the same sites here as there.
    """
    return sorted(
        {(a, b) for u, v in ((x, y), (y, x)) for a in (u, span - u) for b in (v, span - v)}
    )


def expand(source: dict[str, Any]) -> Expansion:
    """Expand the orbits, deciding controls C2 to C5 as the structure is built."""
    outer_side = _exact(source.get("L"), "L")
    parent_side = _exact(source.get("A"), "A")
    coordinate_denominator = _integer(
        source.get("coordinate_denominator"), "coordinate_denominator"
    )
    weight_denominator = _integer(source.get("weight_denominator"), "weight_denominator")
    if not 0 < parent_side < outer_side:
        raise TranslationError(
            f"parent side {parent_side} is not inside container {outer_side}"
        )
    span = outer_side * coordinate_denominator
    if span.denominator != 1:
        raise TranslationError("the container side is not an integer on the coordinate scale")
    limit = int(span)

    sites: list[tuple[int, int]] = []
    weights: list[int] = []
    orbit_indices: list[range] = []
    for index, entry in enumerate(cast(list[Any], source["point_orbits"])):
        x, y, weight = (_integer(v, f"point_orbits[{index}][{c}]") for c, v in enumerate(entry))
        if weight < 0 or not (0 <= x <= limit and 0 <= y <= limit):
            raise TranslationError(f"point_orbits[{index}] leaves the container or is signed")
        images = orbit(x, y, limit)
        orbit_indices.append(range(len(sites), len(sites) + len(images)))
        sites.extend(images)
        weights.extend([weight] * len(images))
    if len(set(sites)) != len(sites):
        raise TranslationError(
            "two point orbits share a site; the expansion is not a partition"
        )
    lookup = {site: index for index, site in enumerate(sites)}

    triples: list[tuple[int, int, int]] = []
    triple_weights: list[int] = []
    for index, entry in enumerate(cast(list[Any], source["threshold_orbits"])):
        group = [tuple(cast(list[int], triple)) for triple in cast(list[Any], entry["triples"])]
        weight = _integer(entry.get("weight"), f"threshold_orbits[{index}].weight")
        if weight < 0:
            raise TranslationError(f"threshold_orbits[{index}] has a negative weight")
        for triple in group:
            if len(triple) != 3 or len(set(triple)) != 3:
                raise TranslationError(
                    f"threshold_orbits[{index}] is not a triple of distinct sites"
                )
            if not all(type(i) is int and 0 <= i < len(sites) for i in triple):
                raise TranslationError(
                    f"threshold_orbits[{index}] indexes a site that is not there"
                )
        expected = {
            tuple(
                sorted(
                    lookup[image]
                    for image in _triple_image(group[0], sites, limit, flip=flip, turn=turn)
                )
            )
            for flip in (False, True)
            for turn in range(4)
        }
        if expected != {tuple(sorted(t)) for t in group} or len(expected) != len(group):
            raise TranslationError(
                f"threshold_orbits[{index}] is not a full D4 orbit of triples"
            )
        triples.extend(cast(list[tuple[int, int, int]], group))
        triple_weights.extend([weight] * len(group))

    budget_units = _integer(source.get("budget_units"), "budget_units")
    minimum_units = _integer(source.get("minimum_units"), "minimum_units")
    expanded = sum(weights) + sum(triple_weights)
    if expanded != budget_units:
        raise TranslationError(
            f"C4 the expanded budget {expanded} != the declared {budget_units}"
        )
    if sum(weights) + 5 * sum(triple_weights) >= INT64_HEADROOM:
        raise TranslationError(
            "C4 the absolute charge leaves the artifact's own int64 headroom"
        )
    if 17 * minimum_units <= budget_units:
        raise TranslationError(
            f"C5 the counting inequality fails: 17 * {minimum_units} <= {budget_units}"
        )

    rows: list[tuple[Fraction, Fraction, Fraction, Fraction]] = []
    cursor = Fraction(0)
    for index, entry in enumerate(cast(list[Any], source["entries"])):
        a, b, t, side = (_exact(v, f"entries[{index}][{c}]") for c, v in enumerate(entry))
        if a != cursor or not 0 <= a < b < 1 or not 0 <= t < 1 or not 0 < side < parent_side:
            raise TranslationError(f"entries[{index}] does not continue the catalogue")
        rows.append((a, b, t, side))
        cursor = b
    if cursor * cursor + 2 * cursor <= 1:
        raise TranslationError("the catalogue stops short of pi/4")

    return Expansion(
        outer_side=outer_side,
        parent_side=parent_side,
        point_orbits=len(cast(list[Any], source["point_orbits"])),
        positive_point_orbits=sum(
            1 for entry in cast(list[Any], source["point_orbits"]) if entry[2]
        ),
        threshold_orbit_count=len(cast(list[Any], source["threshold_orbits"])),
        coordinate_denominator=coordinate_denominator,
        weight_denominator=weight_denominator,
        sites=tuple(sites),
        weights=tuple(weights),
        triples=tuple(triples),
        triple_weights=tuple(triple_weights),
        rows=tuple(rows),
        minimum_units=minimum_units,
        budget_units=budget_units,
    )


def _triple_image(
    triple: tuple[int, ...],
    sites: list[tuple[int, int]],
    span: int,
    *,
    flip: bool,
    turn: int,
) -> list[tuple[int, int]]:
    """One of the eight D4 images of a triple, as sites rather than indices."""
    shape = [sites[i] for i in triple]
    if flip:
        shape = [(y, x) for x, y in shape]
    for _ in range(turn):
        shape = [(span - y, x) for x, y in shape]
    return shape


def structure_control(expansion: Expansion, structure: dict[str, Any]) -> dict[str, Any]:
    """C1: the expanded counts against the artifact's own retained structure record."""
    measured = {
        "available_point_orbits": expansion.point_orbits,
        "positive_point_orbits": expansion.positive_point_orbits,
        "physical_sites": len(expansion.sites),
        "positive_sites": sum(1 for w in expansion.weights if w),
        "threshold_orbits": expansion.threshold_orbit_count,
        "physical_triples": len(expansion.triples),
        "point_budget_units": expansion.point_units,
        "threshold_budget_units": expansion.triple_units,
        "total_budget_units": expansion.point_units + expansion.triple_units,
    }
    mismatched = {
        key: (value, structure.get(key))
        for key, value in measured.items()
        if structure.get(key) != value
    }
    if mismatched:
        raise TranslationError(
            f"C1 the expansion disagrees with evidence/structure.json: {mismatched}"
        )
    return measured


def d4_closure_control(
    points: list[tuple[Fraction, Fraction]], weights: list[Fraction], outer_side: Fraction
) -> int:
    """C6: the gate's own ``Condition 1`` predicate, decided before the gate sees the bytes."""
    table = dict(zip(points, weights, strict=True))
    if len(table) != len(points):
        raise TranslationError("C6 two emitted atoms share a site")
    for point, weight in table.items():
        for image in d4_images(point[0], point[1], outer_side):
            if table.get(image) != weight:
                raise TranslationError(
                    f"C6 the site {point} has no D4 image of equal weight at {image}"
                )
    return len(table)


def _row_rectangles(
    expansion: Expansion,
    row: tuple[Fraction, Fraction, Fraction, Fraction],
    *,
    point_only: bool = False,
) -> tuple[dict[tuple[int, int, int, int], int], list[tuple[int, int]]]:
    """The signed capture rectangles of one catalogue row, and its legal-centre polygon.

    Everything is an integer on the row's own common scale: the rotation is applied as the
    integer pair ``(C, S) = (q^2 - p^2, 2pq)`` for ``t = p / q``, and the half-side carries
    the matching factor ``R = q^2 + p^2``, so no rational survives into the sweep.
    """
    a, b, t, side = row
    p, q = t.numerator, t.denominator
    cosine, sine, norm = q * q - p * p, 2 * p * q, q * q + p * p
    denominator = expansion.coordinate_denominator
    span = int(expansion.outer_side * denominator)

    def width(u: Fraction) -> Fraction:
        return (1 + 2 * u - u * u) / (1 + u * u)

    reach = expansion.parent_side * min(width(a), width(b)) / 2
    half_domain = expansion.outer_side / 2 - reach
    scale = lcm(2 * denominator, (side / 2).denominator, half_domain.denominator)
    factor = scale // (2 * denominator)
    domain = int(half_domain * scale)
    half = int(side * scale / 2) * norm
    frame = [
        (
            cosine * (2 * x - span) * factor + sine * (2 * y - span) * factor,
            -sine * (2 * x - span) * factor + cosine * (2 * y - span) * factor,
        )
        for x, y in expansion.sites
    ]
    rectangles: dict[tuple[int, int, int, int], int] = {}

    def insert(indices: tuple[int, ...], weight: int) -> None:
        if not weight:
            return
        us = [frame[i][0] for i in indices]
        vs = [frame[i][1] for i in indices]
        box = (max(us) - half, min(us) + half, max(vs) - half, min(vs) + half)
        if box[0] < box[1] and box[2] < box[3]:
            rectangles[box] = rectangles.get(box, 0) + weight

    for index, weight in enumerate(expansion.weights):
        insert((index,), weight)
    if not point_only:
        for (i, j, k), weight in zip(expansion.triples, expansion.triple_weights, strict=True):
            insert((i, j), weight)
            insert((i, k), weight)
            insert((j, k), weight)
            insert((i, j, k), -2 * weight)
    polygon = [
        (cosine * x + sine * y, -sine * x + cosine * y)
        for x, y in ((-domain, -domain), (domain, -domain), (domain, domain), (-domain, domain))
    ]
    return {box: weight for box, weight in rectangles.items() if weight}, polygon


def restricted_row_minimum(
    expansion: Expansion, index: int, *, point_only: bool = False
) -> tuple[int, int, int]:
    """The artifact's own minimum charge on one catalogue row: units, slabs, cells.

    A slab sweep over the event grid of the signed rectangles, taking the minimum only over
    the cells of the *restricted* legal-centre polygon. This is control ``C8``: an
    independent second implementation whose number the retained replay must confirm.

    ``point_only`` drops every two-of-three atom and sweeps the point weights alone, which
    is the ``H-235`` screen: the measure's triples are decoration at these weights exactly
    when the least point-only charge stays at or above the point budget over ``n``.
    """
    rectangles, polygon = _row_rectangles(
        expansion, expansion.rows[index], point_only=point_only
    )
    boxes = list(rectangles)
    weights = [rectangles[box] for box in boxes]
    us = sorted({point[0] for point in polygon} | {v for box in boxes for v in box[:2]})
    vs = sorted({point[1] for point in polygon} | {v for box in boxes for v in box[2:]})
    u_index = {value: i for i, value in enumerate(us)}
    v_index = {value: i for i, value in enumerate(vs)}
    low = np.array([v_index[box[2]] for box in boxes], np.int64)
    high = np.array([v_index[box[3]] for box in boxes], np.int64)
    events = sorted(
        [(u_index[box[0]], i, 1) for i, box in enumerate(boxes)]
        + [(u_index[box[1]], i, -1) for i, box in enumerate(boxes)]
    )
    edges: list[tuple[int, int, int, int, int]] = []
    for corner, start in enumerate(polygon):
        end = polygon[(corner + 1) % 4]
        if end[0] == start[0]:
            continue
        (u0, v0), (u1, v1) = (start, end) if start[0] < end[0] else (end, start)
        edges.append((u0, u1, v1 - v0, v0 * (u1 - u0) - u0 * (v1 - v0), u1 - u0))
    left = min(point[0] for point in polygon)
    right = max(point[0] for point in polygon)

    masses = np.zeros(len(vs) - 1, np.int64)
    least: int | None = None
    slabs = cells = cursor = 0
    for slab, (u0, u1) in enumerate(pairwise(us)):
        while cursor < len(events) and events[cursor][0] == slab:
            _, box, sign = events[cursor]
            masses[low[box] : high[box]] += sign * weights[box]
            cursor += 1
        if u0 < left or u1 > right:
            continue
        crossings = [
            (slope * u + offset, length)
            for start, end, slope, offset, length in edges
            if start <= u0 and u1 <= end
            for u in (u0, u1)
        ]
        if len(crossings) != 4:
            raise TranslationError(
                f"C8 row {index} slab {slab} met {len(crossings)} polygon edges"
            )
        bottom, bottom_scale = crossings[0]
        top, top_scale = crossings[0]
        for value, length in crossings[1:]:
            if value * bottom_scale < bottom * length:
                bottom, bottom_scale = value, length
            if value * top_scale > top * length:
                top, top_scale = value, length
        first = bisect_right(vs, bottom // bottom_scale) - 1
        last = bisect_left(vs, -((-top) // top_scale))
        if not 0 <= first < last <= len(vs) - 1:
            raise TranslationError(f"C8 row {index} slab {slab} left the event grid")
        value = int(masses[first:last].min())
        slabs += 1
        cells += last - first
        if least is None or value < least:
            least = value
    if least is None:
        raise TranslationError(f"C8 row {index} has no cell in its legal-centre polygon")
    return least, slabs, cells


def point_only_screen(
    expansion: Expansion, sample: list[int], *, workers: int, verbose: bool
) -> dict[str, Any]:
    """``H-235``: is the two-of-three apparatus load-bearing at the measure's own weights?

    The artifact's charge is a point part plus a triple part. Strip the triples, leave every
    point weight where it is, and sweep the same restricted rows: what is left is a point
    measure of budget ``M_p = 14.640116080``, and by the homogeneity argument of
    `devtools.measure_threshold_net_refinement` it rescales to a point certificate at the
    same ``(L, B, catalogue)`` exactly when its least charge exceeds ``M_p / 17``. Below
    that threshold the triples are doing real work at these weights; at or above it they are
    decoration and the artifact is, after rescaling, a point certificate.

    The screen is about *these* weights and no others: a point-only linear program with the
    triples' budget returned to the sites could do better or worse, and this says nothing
    about it. It runs restricted, on the artifact's own rows, so the parent-centre question
    does not enter.
    """
    started = time.perf_counter()
    threshold = Fraction(expansion.point_units, expansion.weight_denominator) / 17
    least: int | None = None
    at = -1
    results = _sweep_rows(expansion, sample, workers=workers, verbose=verbose, started=started)
    for index, units in results:
        if least is None or units < least:
            least, at = units, index
    if least is None:
        raise TranslationError("H-235 swept no row")
    charge = Fraction(least, expansion.weight_denominator)
    return {
        "rows_swept": len(sample),
        "rows_available": len(expansion.rows),
        "least_point_charge_units": least,
        "least_point_charge": str(charge),
        "least_point_charge_float": float(charge),
        "attained_at_row": at,
        "point_budget_over_n": str(threshold),
        "point_budget_over_n_float": float(threshold),
        "margin": str(charge - threshold),
        "triples_load_bearing": charge < threshold,
        "seconds": round(time.perf_counter() - started, 1),
    }


def _point_only_row(argument: tuple[Expansion, int]) -> tuple[int, int]:
    expansion, index = argument
    return index, restricted_row_minimum(expansion, index, point_only=True)[0]


def _sweep_rows(
    expansion: Expansion, sample: list[int], *, workers: int, verbose: bool, started: float
) -> list[tuple[int, int]]:
    """Every row's point-only minimum, forked over ``workers`` processes when asked."""
    arguments = [(expansion, index) for index in sample]
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("fork")) as pool:
            pairs = list(pool.map(_point_only_row, arguments, chunksize=8))
    else:
        pairs = []
        for position, argument in enumerate(arguments):
            pairs.append(_point_only_row(argument))
            if verbose and position % 200 == 0:
                running = min(units for _, units in pairs)
                print(
                    f"  H-235 {position + 1}/{len(sample)} row {argument[1]}: least so far "
                    f"{running} ({time.perf_counter() - started:.1f}s)",
                    flush=True,
                )
    return pairs


def direction_sweep(path: Path, count: int, *, workers: int, verbose: bool) -> dict[str, Any]:
    """The emitted certificate's least charge at a sample of its own net directions.

    `devtools.decide_threshold_certificate` decides ``Condition 5'`` at every direction of
    the net and prints one number; at this size that is hours of sweep, and a lane that
    only needs to *refuse* does not need all of them. ``Condition 5'`` is a conjunction
    over directions, so one direction whose least charge falls below 1 refuses the
    certificate, and refuses every finer net containing that direction as well. This reads
    the bytes through the gate's own loader, so the object swept is the gate's object, and
    then runs the gate's own exact sweep at a stratified sample of directions -- index 0
    always among them -- re-evaluating each least charge at its witness by membership
    counting, which is the sweep's own independent check.

    A sample decides a weaker statement than the net does. It can refuse and it can never
    accept, and the report says so in ``refuted``; the least charge it reports is an upper
    bound on the net's own least charge, never a measurement of it.
    """
    certificate, _ = load(path.read_bytes())
    total = len(certificate.half_tangents)
    stride = max(1, total // max(1, count))
    sample = sorted({*range(0, total, stride), total - 1})
    started = time.perf_counter()
    results = _sweep_directions(
        certificate, sample, workers=workers, verbose=verbose, started=started
    )
    least, at, witness = min(results, key=lambda row: row[0])
    return {
        "certificate": str(path),
        "directions_swept": len(sample),
        "directions_in_net": total,
        "least_charge": str(least),
        "least_charge_float": float(least),
        "binding_direction": at,
        "binding_half_tangent": str(certificate.half_tangents[at]),
        "binding_witness_rotated_frame": [str(value) for value in witness],
        "refuted": least < 1,
        "per_direction": [
            {"direction": index, "least_charge": str(value), "least_charge_float": float(value)}
            for value, index, _ in sorted(results, key=lambda row: row[1])
        ],
        "seconds": round(time.perf_counter() - started, 1),
    }


def _one_direction(
    argument: tuple[ThresholdCertificate, int],
) -> tuple[Fraction, int, tuple[Fraction, Fraction]]:
    certificate, index = argument
    least, witness = minimum_charge(
        certificate.atoms,
        certificate.threshold_atoms,
        certificate.directions[index],
        certificate.outer_side,
        certificate.square_side,
        dense_cell_limit=0,
    )
    membership = _membership(certificate, index, witness)
    recount = exact_charge(certificate.atoms, certificate.threshold_atoms, membership)
    if recount != least:
        raise TranslationError(
            f"direction {index}: the sweep says {least} and membership counting {recount}"
        )
    return least, index, witness


def _membership(
    certificate: ThresholdCertificate, index: int, witness: tuple[Fraction, Fraction]
) -> Callable[[Fraction, Fraction], bool]:
    """Is a point inside the core the sweep's witness centre names? Exactly, by counting."""
    direction = certificate.directions[index]
    half = certificate.square_side / 2
    centre_u, centre_v = witness

    def contains(x: Fraction, y: Fraction) -> bool:
        return (
            abs(direction.ux * x + direction.uy * y - centre_u) <= half
            and abs(direction.vx * x + direction.vy * y - centre_v) <= half
        )

    return contains


def _sweep_directions(
    certificate: ThresholdCertificate,
    sample: list[int],
    *,
    workers: int,
    verbose: bool,
    started: float,
) -> list[tuple[Fraction, int, tuple[Fraction, Fraction]]]:
    arguments = [(certificate, index) for index in sample]
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("fork")) as pool:
            return list(pool.map(_one_direction, arguments))
    results: list[tuple[Fraction, int, tuple[Fraction, Fraction]]] = []
    for argument in arguments:
        results.append(_one_direction(argument))
        if verbose:
            value, index, _ = results[-1]
            print(
                f"  direction {index}: least charge {float(value):.9f} "
                f"({time.perf_counter() - started:.1f}s)",
                flush=True,
            )
    return results


def control_rows(expansion: Expansion, replay: dict[str, Any], count: int) -> list[int]:
    """A deterministic sample: the two ends, the tight row, and an even stride between."""
    rows = cast(list[dict[str, int]], replay["rows"])
    if len(rows) != len(expansion.rows):
        raise TranslationError(
            f"C8 the replay holds {len(rows)} rows, the catalogue {len(expansion.rows)}"
        )
    tight = min(rows, key=lambda row: row["minimum_units"])["row"]
    last = len(rows) - 1
    if count >= len(rows):
        return list(range(len(rows)))
    stride = max(1, len(rows) // max(1, count - 3))
    return sorted({0, last, tight, *range(0, len(rows), stride)})


def replay_control(
    expansion: Expansion, replay: dict[str, Any], sample: list[int], *, verbose: bool
) -> dict[str, Any]:
    """C8: recompute each sampled row and require the retained replay to confirm it."""
    rows = cast(list[dict[str, int]], replay["rows"])
    started = time.perf_counter()
    least = None
    for position, index in enumerate(sample):
        units, slabs, cells = restricted_row_minimum(expansion, index)
        recorded = rows[index]
        if (units, slabs, cells) != (
            recorded["minimum_units"],
            recorded["slabs"],
            recorded["cells"],
        ):
            raise TranslationError(
                f"C8 row {index}: recomputed (units, slabs, cells) = {(units, slabs, cells)} "
                f"against the retained replay's "
                f"{(recorded['minimum_units'], recorded['slabs'], recorded['cells'])}"
            )
        least = units if least is None else min(least, units)
        if verbose and position % 20 == 0:
            print(
                f"  C8 {position + 1}/{len(sample)} row {index}: {units} units, {slabs} slabs, "
                f"{cells} cells ({time.perf_counter() - started:.1f}s)",
                flush=True,
            )
    declared = expansion.minimum_units
    if least != declared:
        raise TranslationError(f"C8 the sampled minimum {least} != the declared {declared}")
    return {
        "rows_recomputed": len(sample),
        "rows_available": len(rows),
        "sampled_minimum_units": least,
        "declared_minimum_units": expansion.minimum_units,
        "seconds": round(time.perf_counter() - started, 1),
    }


def witness_charge(
    expansion: Expansion, index: int, abscissa: str, ordinate: str
) -> dict[str, Any]:
    """``C9``: the exact charge of one catalogue row's own core at one named centre.

    This is the un-confounded reading of what the parent-centre restriction carries. It
    holds the row's own core fixed -- its own half-tangent ``t``, its own side ``B``, the
    artifact's own sites and triples -- and moves only the centre, to a placement the
    container admits and a legal parent does not. The charge is counted by membership in
    exact rationals, atom by atom, with no sweep and no event grid between the sites and
    the number, so it shares nothing with ``C8`` but the expansion.

    A coordinate of ``wall`` means ``B (c(t) + s(t)) / 2``, the least abscissa at which the
    rotated core still lies inside the container: the placement whose vertex touches the
    wall. The report says how far outside the row's own envelope ``[r, L - r]`` the centre
    falls, and compares the charge to ``M / 17`` rather than to 1, because a measure that
    charges below ``M / n`` somewhere is one no rescaling can turn into a certificate.
    """
    a, b, tangent, side = expansion.rows[index]
    norm = 1 + tangent * tangent
    cosine, sine = (1 - tangent * tangent) / norm, 2 * tangent / norm

    def envelope(u: Fraction) -> Fraction:
        return (1 + 2 * u - u * u) / (1 + u * u)

    reach = side * envelope(tangent) / 2
    centre = tuple(
        reach if text == "wall" else _exact(text, f"--charge-at centre[{axis}]")
        for axis, text in enumerate((abscissa, ordinate))
    )
    admissible = all(reach <= value <= expansion.outer_side - reach for value in centre)
    legal = expansion.parent_side * min(envelope(a), envelope(b)) / 2
    half = side / 2
    frame = (
        cosine * centre[0] + sine * centre[1],
        -sine * centre[0] + cosine * centre[1],
    )
    captured = {
        i
        for i, point in enumerate(expansion.point(j) for j in range(len(expansion.sites)))
        if abs(cosine * point[0] + sine * point[1] - frame[0]) <= half
        and abs(-sine * point[0] + cosine * point[1] - frame[1]) <= half
    }
    point_units = sum(expansion.weights[i] for i in captured)
    triple_units = sum(
        weight
        for triple, weight in zip(expansion.triples, expansion.triple_weights, strict=True)
        if sum(1 for i in triple if i in captured) >= 2
    )
    charge = Fraction(point_units + triple_units, expansion.weight_denominator)
    required = Fraction(expansion.budget_units, expansion.weight_denominator) / 17
    return {
        "row": index,
        "half_tangent": str(tangent),
        "core_side": str(side),
        "centre": [str(value) for value in centre],
        "centre_float": [float(value) for value in centre],
        "core_admissible_in_container": admissible,
        "parent_centre_envelope": str(legal),
        "outside_envelope_by": float(legal - centre[0]),
        "captured_sites": len(captured),
        "point_units": point_units,
        "triple_units": triple_units,
        "charge": str(charge),
        "charge_float": float(charge),
        "budget_over_n": str(required),
        "budget_over_n_float": float(required),
        "shortfall_against_budget_over_n": str(required - charge),
        "no_rescaling_saves_it": charge < required,
    }


def build(
    expansion: Expansion, steps: int, *, angle_limit: Fraction = ANGLE_LIMIT
) -> dict[str, Any]:
    """The threshold-certificate record, with C6 and C7 decided on the way out."""
    if steps < 2:
        raise TranslationError("the direction net needs at least two directions")
    side = expansion.least_core_side
    net = [angle_limit * k / steps for k in range(steps + 1)]
    gap = max((right - left) / (1 + left * right) for left, right in pairwise(net))
    if side * (1 + gap) >= 1:
        raise TranslationError(
            f"C7 Condition 4 refuses this net: B = {float(side):.9f}, D = {float(gap):.9f}, "
            f"B(1 + D) = {float(side * (1 + gap)):.9f} is not below 1; the net needs at "
            f"least {-int(-angle_limit / (1 / side - 1))} steps at this shrink"
        )
    points = [expansion.point(index) for index in range(len(expansion.sites))]
    positive = [index for index, weight in enumerate(expansion.weights) if weight]
    emitted = [points[index] for index in positive]
    emitted_weights = [
        Fraction(expansion.weights[index], expansion.weight_denominator) for index in positive
    ]
    d4_closure_control(emitted, emitted_weights, expansion.outer_side)
    point_mass = sum(emitted_weights, start=Fraction(0))
    threshold_budget = sum(
        (Fraction(weight, expansion.weight_denominator) for weight in expansion.triple_weights),
        start=Fraction(0),
    )
    return {
        "id": f"C-n017-kleddamag-unrestricted-net{steps}",
        "variant": "threshold",
        "n": 17,
        "claim": f"s(17) >= {expansion.outer_side}",
        "outer_side": str(expansion.outer_side),
        "square_side": str(side),
        "angle_limit": str(angle_limit),
        "direction_steps": steps,
        "symmetry": "D4",
        "point_mass": str(point_mass),
        "threshold_budget": str(threshold_budget),
        "total_budget": str(point_mass + threshold_budget),
        "atoms": [
            [str(x), str(y), str(w)] for (x, y), w in zip(emitted, emitted_weights, strict=True)
        ],
        "threshold_atoms": [
            {
                "points": [[str(points[i][0]), str(points[i][1])] for i in triple],
                "threshold": 2,
                "weight": str(Fraction(weight, expansion.weight_denominator)),
            }
            for triple, weight in zip(expansion.triples, expansion.triple_weights, strict=True)
        ],
        "provenance": {
            "tool": "devtools.translate_kleddamag_certificate",
            "source": str(SOURCE.relative_to(PACKING.parent)),
            "source_parent_side": str(expansion.parent_side),
            "core_side_band": [
                str(expansion.least_core_side),
                str(expansion.greatest_core_side),
            ],
            "restriction": "dropped: the source's parent-centre catalogue is not translated",
            "largest_half_gap_tangent": str(gap),
            "containment_product": str(side * (1 + gap)),
        },
    }


def translate(
    source_path: Path,
    *,
    steps: int,
    rows: int,
    structure_path: Path,
    replay_path: Path,
    centres: list[list[str]] | None,
    point_rows: int,
    workers: int,
    verbose: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Read, control and build; every control decides before the record is returned."""
    source, digest = read_source(source_path)
    expansion = expand(source)
    counts = structure_control(expansion, json.loads(structure_path.read_text()))
    record = build(expansion, steps)
    replay = json.loads(replay_path.read_text())
    sample = control_rows(expansion, replay, rows) if rows else []
    report = {
        "source": str(source_path),
        "source_sha256": digest,
        "structure": counts,
        "core_side_band": [str(expansion.least_core_side), str(expansion.greatest_core_side)],
        "catalogue_rows": len(expansion.rows),
        "direction_steps": steps,
        "square_side": record["square_side"],
        "total_budget": record["total_budget"],
        "containment_product": record["provenance"]["containment_product"],
        "emitted_atoms": len(cast(list[Any], record["atoms"])),
        "emitted_threshold_atoms": len(cast(list[Any], record["threshold_atoms"])),
        "restricted_replay_control": (
            replay_control(expansion, replay, sample, verbose=verbose) if sample else "skipped"
        ),
        "point_only_screen": (
            point_only_screen(
                expansion,
                (
                    list(range(len(expansion.rows)))
                    if point_rows >= len(expansion.rows)
                    else sorted(
                        {
                            *range(
                                0,
                                len(expansion.rows),
                                max(1, len(expansion.rows) // point_rows),
                            ),
                            len(expansion.rows) - 1,
                        }
                    )
                ),
                workers=workers,
                verbose=verbose,
            )
            if point_rows
            else "skipped"
        ),
        "unrestricted_witness_control": [
            witness_charge(expansion, int(row), x, y) for row, x, y in centres or []
        ]
        or "skipped",
    }
    return record, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--structure", type=Path, default=STRUCTURE)
    parser.add_argument("--replay", type=Path, default=REPLAY)
    parser.add_argument("--output", type=Path, help="where to write the threshold certificate")
    parser.add_argument("--report", type=Path, help="where to write the control report")
    parser.add_argument("--direction-steps", type=int, default=1440)
    parser.add_argument(
        "--control-rows",
        type=int,
        default=0,
        help="rows to recompute for C8; 0 skips it and no output may then be trusted",
    )
    parser.add_argument(
        "--charge-at",
        nargs=3,
        action="append",
        metavar=("ROW", "X", "Y"),
        help=(
            "C9: the exact charge of that catalogue row's own core at that centre, in "
            "container coordinates; 'wall' means the least admissible coordinate "
            "B (c(t) + s(t)) / 2. May be repeated."
        ),
    )
    parser.add_argument(
        "--point-only-rows",
        type=int,
        default=0,
        help=(
            "H-235: sweep this many catalogue rows with every two-of-three atom dropped; "
            "pass 7853 or more for the whole catalogue, 0 to skip"
        ),
    )
    parser.add_argument(
        "--workers", type=int, default=1, help="forked processes for the sweeps"
    )
    parser.add_argument(
        "--sweep-certificate", type=Path, help="an emitted record to sweep unrestricted"
    )
    parser.add_argument(
        "--sweep-directions",
        type=int,
        default=0,
        help=(
            "net directions of --sweep-certificate to decide Condition 5' at; a sample can "
            "refuse and can never accept"
        ),
    )
    parser.add_argument("--quiet", action="store_true", help="no per-row C8 progress")
    args = parser.parse_args(argv)
    try:
        record, report = translate(
            args.source,
            steps=args.direction_steps,
            rows=args.control_rows,
            structure_path=args.structure,
            replay_path=args.replay,
            centres=args.charge_at,
            point_rows=args.point_only_rows,
            workers=max(1, args.workers),
            verbose=not args.quiet,
        )
    except (TranslationError, OSError, KeyError, ValueError) as error:
        print(f"REFUSED: {error}", flush=True)
        return 1
    if args.sweep_certificate is not None and args.sweep_directions:
        try:
            report["unrestricted_direction_sweep"] = direction_sweep(
                args.sweep_certificate,
                args.sweep_directions,
                workers=max(1, args.workers),
                verbose=not args.quiet,
            )
        except (TranslationError, OSError, ValueError) as error:
            print(f"REFUSED: {error}", flush=True)
            return 1
    print(json.dumps(report, indent=2), flush=True)
    if args.control_rows == 0:
        print(
            "WARNING: C8 did not run; the translation is unconfirmed and no verdict taken "
            "from these bytes means anything. Pass --control-rows.",
            flush=True,
        )
    if args.output is not None:
        args.output.write_text(json.dumps(record, indent=1) + "\n")
        digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
        print(
            f"wrote {args.output} ({args.output.stat().st_size} bytes); sha256 {digest}",
            flush=True,
        )
    if args.report is not None:
        args.report.write_text(json.dumps(report, indent=2) + "\n")
        print(f"wrote {args.report}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
