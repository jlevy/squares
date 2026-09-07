"""Conditional combinatorial replay of Stromquist's 1984 six-square argument.

Run from packing/ with the project Python: python -m cases.stromquist.memo1.
The geometric premises remain explicit inputs to the finite argument; this
does not independently verify Lemmas 6--8 or prove a new packing bound.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from sqpack.cover import write_text_atomic
from sqpack.incidence import (
    Allocation,
    IncidenceProblem,
    allocations,
    convexly_closed_masks,
    occupancy_bound,
)

LABELS = tuple("ABCDEFGHI")
GRID = tuple((index % 3, index // 3) for index in range(9))
POINTS = tuple((1 + Fraction(x, 2), 1 + Fraction(y, 2)) for x, y in GRID)
CENTER = 1 << LABELS.index("E")
PERIMETER = ((1 << len(LABELS)) - 1) ^ CENTER
PREMISES = (
    "perimeter_hit",
    "convexity",
    "two_point_adjacency",
    "adjacent_singletons",
)
SOURCE_ALLOCATION = ("AD", "B", "CF", "EH", "G", "I")
FINAL_LABELS = ("E", "G", "H", "I", "J", "K", "L", "M")
FINAL_POINTS = (
    (Fraction(3, 2), Fraction(3, 2)),
    (Fraction(1), Fraction(2)),
    (Fraction(3, 2), Fraction(2)),
    (Fraction(2), Fraction(2)),
    (Fraction(1), Fraction(17, 10)),
    (Fraction(2), Fraction(17, 10)),
    (Fraction(1), Fraction(9, 10)),
    (Fraction(2), Fraction(9, 10)),
)


def _adjacent(left: int, right: int) -> bool:
    x1, y1 = GRID[left]
    x2, y2 = GRID[right]
    return abs(x1 - x2) + abs(y1 - y2) == 1


def make_problem(*, omit_premise: str | None = None) -> IncidenceProblem:
    """Retain all masks satisfying the named necessary conditions, with no size cap."""
    if omit_premise is not None and omit_premise not in PREMISES:
        raise ValueError(f"unknown geometric premise: {omit_premise}")
    masks = (
        tuple(range(1, 1 << len(LABELS)))
        if omit_premise == "convexity"
        else convexly_closed_masks(POINTS)
    )
    allowed: list[int] = []
    for mask in masks:
        if omit_premise != "perimeter_hit" and not mask & PERIMETER:
            continue
        indices = tuple(index for index in range(len(LABELS)) if mask & (1 << index))
        if (
            omit_premise != "two_point_adjacency"
            and len(indices) == 2
            and not _adjacent(*indices)
        ):
            continue
        allowed.append(mask)
    conflicts = (
        ()
        if omit_premise == "adjacent_singletons"
        else tuple(
            (1 << left, 1 << right)
            for left in range(len(LABELS))
            for right in range(left + 1, len(LABELS))
            if _adjacent(left, right)
            and (1 << left) & PERIMETER
            and (1 << right) & PERIMETER
            and (1 << left) in allowed
            and (1 << right) in allowed
        )
    )
    return IncidenceProblem(LABELS, tuple(allowed), conflicts)


def mask_names(mask: int, labels: tuple[str, ...] = LABELS) -> str:
    """Human-readable labels for one mask, ordered by the supplied site inventory."""
    return "".join(label for index, label in enumerate(labels) if mask & (1 << index))


def d4_images(allocation: Allocation) -> tuple[Allocation, ...]:
    """All distinct images under global square symmetries of the nine-site grid."""
    images: set[Allocation] = set()
    for reflected in (False, True):
        for turns in range(4):
            permutation: list[int] = []
            for original_x, original_y in GRID:
                x = 2 - original_x if reflected else original_x
                y = original_y
                for _ in range(turns):
                    x, y = 2 - y, x
                permutation.append(3 * y + x)
            images.add(
                tuple(
                    sorted(
                        sum(
                            1 << permutation[index] for index in range(9) if mask & (1 << index)
                        )
                        for mask in allocation
                    )
                )
            )
    return tuple(sorted(images))


def conditional_record() -> dict[str, object]:
    """Rebuild the full finite answer and controls without accepting stored outcomes."""
    problem = make_problem()
    found = allocations(problem, 6)
    canonical = {min(d4_images(allocation)) for allocation in found}
    expected = tuple(
        sorted(sum(1 << LABELS.index(label) for label in group) for group in SOURCE_ALLOCATION)
    )
    expected_images = set(d4_images(expected))
    if set(found) != expected_images or len(canonical) != 1:
        raise ValueError("finite allocations do not reproduce the source's single D4 orbit")
    controls: dict[str, object] = {}
    for omitted in PREMISES:
        alternative = allocations(make_problem(omit_premise=omitted), 6)
        extras = sorted(set(alternative) - set(found))
        if not set(found) < set(alternative):
            raise ValueError(f"removing {omitted} did not expose additional allocations")
        controls[omitted] = {
            "allocation_count": len(alternative),
            "extra_count": len(extras),
            "example_extra": [mask_names(mask) for mask in extras[0]],
        }
    forced = sum(1 << FINAL_LABELS.index(label) for label in "EHJK")
    capacity = occupancy_bound((Fraction(1),) * len(FINAL_LABELS), (forced,))
    weakened = occupancy_bound(
        (Fraction(1),) * len(FINAL_LABELS), (forced ^ (1 << FINAL_LABELS.index("K")),)
    )
    if capacity != 5 or weakened != 6:
        raise ValueError("forced-point capacity control failed")
    return {
        "schema_version": 1,
        "scope": "conditional-combinatorial-control",
        "full_geometric_proof_verified": False,
        "new_packing_bound": False,
        "source": {
            "pdf": (
                "packing/resources/papers/"
                "stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares.pdf"
            ),
            "pages": [11, 12, 13, 18, 19],
            "figure": 14,
        },
        "assumed_geometry": {
            "perimeter_hit": (
                "Every open square of side >1 in [0,3]^2 contains a perimeter mark (Lemma 6)."
            ),
            "convexity": (
                "A block contains every mark in the closed convex hull of its incidences."
            ),
            "two_point_adjacency": (
                "A block with exactly two grid marks has marks at distance 1/2 (p. 18)."
            ),
            "adjacent_singletons": (
                "Adjacent perimeter marks cannot both be isolated in disjoint blocks (Lemma 8)."
            ),
            "final_cover": "Every block contains one of E,G,H,I,J,K,L,M (Lemma 7).",
            "forced_four": (
                "In the normalized allocation, the EH block also contains J and K (p. 18)."
            ),
        },
        "grid": {name: [str(x), str(y)] for name, (x, y) in zip(LABELS, POINTS, strict=True)},
        "allowed_masks": [mask_names(mask) for mask in problem.allowed_masks],
        "incompatible_masks": [
            [mask_names(left), mask_names(right)] for left, right in problem.incompatible_masks
        ],
        "allocation_count": len(found),
        "d4_orbit_count": len(canonical),
        "allocations": [[mask_names(mask) for mask in allocation] for allocation in found],
        "all_grid_sites_used": all(
            sum(allocation) == (1 << len(LABELS)) - 1 for allocation in found
        ),
        "source_representative": list(SOURCE_ALLOCATION),
        "final_count": {
            "sites": {
                name: [str(x), str(y)]
                for name, (x, y) in zip(FINAL_LABELS, FINAL_POINTS, strict=True)
            },
            "forced_together": list("EHJK"),
            "capacity": str(capacity),
            "calculation": "1 + (8 - 4) = 5",
            "three_forced_points_capacity": str(weakened),
        },
        "premise_removal_controls": controls,
        "unrestricted_n11_arithmetic_control": {
            "site_count": 12,
            "forced_together_count": 3,
            "capacity": str(occupancy_bound((Fraction(1),) * 12, (7,))),
            "geometric_certificate": "packing/cases/stromquist/repaired_cover.py",
        },
    }


def main() -> int:
    """Emit the conditional control as JSON, optionally retaining the same bytes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="retain the full rebuilt JSON record")
    args = parser.parse_args()
    text = json.dumps(conditional_record(), indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        write_text_atomic(args.output, text)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
