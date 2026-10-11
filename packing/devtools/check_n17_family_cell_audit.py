"""Force free square 6 into side-S2 for a restricted exact endpoint skeleton.

The other sixteen unit squares have their exact endpoint-family poses, with sliders
a in [0, 3/25], b in [0, 3/40], z in [-1/20, 1/40], embedded concentrically at
U = 1169/250. Eleven closed polygon pieces cover the seven alternative vacant cells.
On each piece, the squared distance to a blocking square's centre is strictly below
one throughout the slider box; the open radius-1/2 incircles then overlap at every
orientation of square 6. Capacity one rules out the sixteen occupied cells.

This reuses the maintained root, endpoint and cover helpers. It proves no capture of
perturbed cores, no wider slider box, and no exclusion of a global packing state.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from typing import Any

from devtools import check_n17_capacity_one_cover as cover
from devtools.check_n17_endpoint_feasibility import FROZEN_ROOT_REF, Box
from devtools.check_n17_root_certificate import SOURCE_PATH
from devtools.check_n17_root_certificate import check as check_root

SCHEMA = "n17-restricted-family-cell-audit/v1"
ROUNDING_GRID = 1000
FORCED_CELL = "side-S2"
BLOCKERS = (3, 9, 10, 11, 12, 13, 14, 16, 17)
OCCUPIED = {
    1: "corner-SW",
    2: "side-S0",
    3: "side-W0",
    4: "corner-NW",
    5: "corner-SE",
    7: "side-E0",
    8: "corner-NE",
    9: "side-W2",
    10: "side-N0",
    11: "interior-W",
    12: "interior-N",
    13: "side-S1",
    14: "interior-E",
    15: "side-N1",
    16: "side-N2",
    17: "side-E1",
}
PUBLISHED_BOUNDS = {
    "interior-SW:11": Q(58298837, 84640000),
    "interior-NW:10": Q(592493086513, 673921600000),
    "interior-S:13": Q(11737, 12500),
    "interior-SE:14": Q(1294731481, 2116000000),
    "interior-NE:12": Q(409960561, 423200000),
    "interior-NE:16": Q(151533961, 264500000),
    "side-W1:9": Q(893101, 1000000),
    "side-W1:3": Q(61, 100),
    "side-W1:11": Q(3420961, 9000000),
    "side-E2:16": Q(3088577, 4500000),
    "side-E2:17": Q(164821, 200000),
}
LIMITATIONS = (
    "Restricted exact sixteen-square family only; no perturbed-core capture, wider "
    "slider claim, or global state exclusion. Shared geometry helpers; no independent "
    "checker or downstream certificate admission is claimed."
)
CentreBox = tuple[tuple[Q, Q], tuple[Q, Q]]


@dataclass(frozen=True)
class Split:
    """Complementary closed cuts: low keeps coordinate <= value, high keeps >=."""

    axis: int
    value: Q
    low: int | Split
    high: int | Split


# At every internal node {coordinate <= value} union {coordinate >= value} is the
# whole parent, including the seam. Recursing therefore proves closed coverage.
PARTITIONS: dict[str, int | Split] = {
    "interior-SW": 11,
    "interior-NW": 10,
    "interior-S": 13,
    "interior-SE": 14,
    "interior-NE": Split(1, Q(29, 10), 12, 16),
    "side-W1": Split(1, Q(21, 10), Split(0, Q(1), 3, 11), 9),
    "side-E2": Split(0, Q(37, 10), 16, 17),
}


@dataclass(frozen=True)
class Piece:
    """A closed convex leaf of a cell's complete partition, with its blocker label."""

    cell: str
    blocker: int
    vertices: tuple[cover.Point, ...]


def _require_domain(domain: cover.SliderDomain) -> None:
    if (domain.a, domain.b, domain.z) != (
        (Q(0), Q(3, 25)),
        (Q(0), Q(3, 40)),
        (Q(-1, 20), Q(1, 40)),
    ):
        raise ValueError("slider domain must be the full stated restricted box")


def round_outward(interval: Box) -> tuple[Q, Q]:
    """Round an exact centre interval outward to the table's 1/1000 lattice."""
    return (
        Q(math.floor(interval.lo * ROUNDING_GRID), ROUNDING_GRID),
        Q(math.ceil(interval.hi * ROUNDING_GRID), ROUNDING_GRID),
    )


def blocker_boxes(point: cover.Endpoint, domain: cover.SliderDomain) -> dict[int, CentreBox]:
    """Enclose blocker centres for all slider values, retaining root uncertainty."""
    _require_domain(domain)
    result: dict[int, CentreBox] = {}
    for label in BLOCKERS:
        x, y = point.centres[label - 1]
        if label == 11:
            slide = Box(*domain.b)
            x, y = x - point.v[0] * slide, y - point.v[1] * slide
        elif label == 13:
            slide = Box(*domain.z)
            x, y = x + point.v[0] * slide, y + point.v[1] * slide
        result[label] = round_outward(x), round_outward(y)
    return result


def closed_pieces(cells: list[cover.Cell]) -> list[Piece]:
    """Construct eleven leaves by closed complementary cuts, never seam priority."""
    result: list[Piece] = []
    by_name = {cell.name: cell for cell in cells}
    if len(by_name) != len(cells) or not set(PARTITIONS) <= set(by_name):
        raise ValueError("missing or duplicate audit cell")

    def descend(name: str, polygon: list[cover.Point], node: int | Split) -> None:
        if not polygon:
            raise ValueError(f"empty audit piece in {name}")
        if isinstance(node, int):
            result.append(Piece(name, node, tuple(polygon)))
            return
        if node.axis not in (0, 1):
            raise ValueError("partition needs a coordinate axis")
        nx, ny = (Q(1), Q(0)) if node.axis == 0 else (Q(0), Q(1))
        descend(name, cover.clip(polygon, nx, ny, node.value), node.low)
        descend(name, cover.clip(polygon, -nx, -ny, -node.value), node.high)

    for name, node in PARTITIONS.items():
        descend(name, list(by_name[name].vertices), node)
    return result


def contains(vertices: tuple[cover.Point, ...], point: cover.Point) -> bool:
    """Closed containment in a counterclockwise convex polygon."""
    return all(
        cover.cross(start, end, point) >= 0
        for start, end in zip(vertices, (*vertices[1:], vertices[0]), strict=True)
    )


def replay(
    point: cover.Endpoint,
    cells: list[cover.Cell],
    *,
    domain: cover.SliderDomain = cover.TRIANGLE,
    published_bounds: dict[str, Q] | None = None,
) -> dict[str, Any]:
    """Check the geometric deduction on supplied exact inputs; refuse a broken premise.

    Root existence is a prerequisite supplied by `check`, rather than implied by this
    geometric replay. Squared distance is convex on polygon x centre rectangle, so
    polygon vertices and centre-box corners bound every pair in that product.
    """
    _require_domain(domain)
    claimed = PUBLISHED_BOUNDS if published_bounds is None else published_bounds
    pieces = closed_pieces(cells)
    boxes = blocker_boxes(point, domain)
    keys = {f"{piece.cell}:{piece.blocker}" for piece in pieces}
    if set(claimed) != keys or any(
        type(bound) is not Q or not 0 <= bound < 1 for bound in claimed.values()
    ):
        raise ValueError("invalid published bound roster or non-strict bound")
    records: list[dict[str, Any]] = []
    for piece in pieces:
        bound = max(
            (x - cx) ** 2 + (y - cy) ** 2
            for (x, y), (cx, cy) in product(piece.vertices, product(*boxes[piece.blocker]))
        )
        key = f"{piece.cell}:{piece.blocker}"
        if bound > claimed[key]:
            raise ValueError(f"published bound exceeded for {key}: {bound} > {claimed[key]}")
        records.append(
            {
                "cell": piece.cell,
                "blocker": piece.blocker,
                "squared_distance_upper_bound": str(bound),
            }
        )
    by_name = {cell.name: cell for cell in cells}
    occupied_names = set(OCCUPIED.values())
    if set(by_name) != occupied_names | set(PARTITIONS) | {FORCED_CELL}:
        raise ValueError("occupied, alternative and forced cells do not cover the cell roster")
    for label, name in OCCUPIED.items():
        for x, y in cover.family_points(point, label, domain):
            if not all(
                contains(by_name[name].vertices, corner)
                for corner in product((x.lo, x.hi), (y.lo, y.hi))
            ):
                raise ValueError(f"square {label} not contained in occupied cell {name}")
    capacity_cache: dict[tuple[Q, Q], dict[str, Any]] = {}
    if not all(cover.capacity_proof(cell, capacity_cache)["passed"] for cell in cells):
        raise ValueError("capacity-one premise failed")
    if not cover.coverage(cells)["passed"]:
        raise ValueError("closed cover premise failed")
    worst = max(Q(record["squared_distance_upper_bound"]) for record in records)
    return {
        "schema": SCHEMA,
        "passed": True,
        "scope": {
            "cap": str(cover.U),
            "design": cover.UNIQUE_24.name,
            "core": "exact endpoint family; all labels except 6",
            "slider_box": {
                "a": [str(value) for value in domain.a],
                "b": [str(value) for value in domain.b],
                "z": [str(value) for value in domain.z],
            },
            "square_6": "any unit-square orientation and any centre allowed by the container",
        },
        "blocker_centre_boxes": {
            str(label): [[str(low), str(high)] for low, high in box]
            for label, box in boxes.items()
        },
        "occupied_cells": {str(label): name for label, name in OCCUPIED.items()},
        "pieces": records,
        "worst_squared_distance": str(worst),
        "squared_distance_margin": str(1 - worst),
        "forced_cell": FORCED_CELL,
        "limitations": LIMITATIONS,
    }


def check() -> dict[str, Any]:
    """Replay the retained root and join its enclosure to the audited cover geometry."""
    root_path = cover.REPO / FROZEN_ROOT_REF.split(":", 1)[1]
    root_document = json.loads(root_path.read_bytes())
    root_result = check_root(root_document, (cover.REPO / SOURCE_PATH).read_bytes())
    midpoint = [Q(value) for value in root_document["box"]["midpoint"]]
    radii = [Q(value) for value in root_result["inclusion_bounds"]]
    expected = tuple(
        Box(*cover.outward(Box(m - radius, m + radius)))
        for m, radius in zip(midpoint, radii, strict=True)
    )
    t, beta, provenance = cover.load_root_box(cover.CERTIFICATE)
    if (t, beta) != expected or not provenance["criterion_passed"]:
        raise ValueError("endpoint enclosure does not match the verified root")
    result = replay(cover.endpoint(t, beta), cover.build_cover(cover.UNIQUE_24))
    result["root_verified"] = root_result["verification_passed"]
    result["root_box"] = {"t": [str(t.lo), str(t.hi)], "beta": [str(beta.lo), str(beta.hi)]}
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.parse_args(argv)
    try:
        result = check()
    except (OSError, ValueError) as error:
        print(
            json.dumps(
                {
                    "schema": SCHEMA,
                    "passed": False,
                    "error": str(error),
                    "limitations": LIMITATIONS,
                },
                indent=1,
                sort_keys=True,
            )
        )
        return 1
    print(json.dumps(result, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
