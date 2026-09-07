"""History-free, positive-inclusion ceiling checker for a fixed D4 support.

The scientific entry point is explicit and lazy. It shares the accepted Trump seed,
NumberField arithmetic and packing verifier with the existing independent source reader.
It does not import the archived executable, call a solver, or invent screening history.
The generic core verifies necessary lower-incidence rows, not exclusion signs or a
candidate's global depth. A complete-child timeout must be supplied externally.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from devtools.check_full_size_density_support_ceiling import reconstruct_source
from sqpack.field import FieldElement, NumberField
from sqpack.full_size_density.support_ceiling import Point, Square, SquareKey, Support
from sqpack.verify import exact_sign, verify_packing

MAX_BITS = 4096
MAX_OUTPUT_BYTES = 2 * 1024 * 1024
SCOPE = "Exact D4 closure of the declared source only; no global packing or density claim."


class AdoptionError(ValueError):
    """A source, inclusion, or upper-certificate obligation was not established."""


@dataclass(frozen=True)
class BoxRow:
    """A positive-area box and necessary lower counts in representative order."""

    point: tuple[Fraction, Fraction]
    radius: Fraction
    counts: tuple[int, ...]


@dataclass(frozen=True)
class Specification:
    """Caller-frozen exact data; no arbitrary packet or field is constructed."""

    source: str
    representatives: tuple[int, ...]
    sizes: tuple[int, ...]
    original_counts: tuple[int, ...]
    rows: tuple[BoxRow, ...]
    multipliers: tuple[Fraction, ...]
    bound: Fraction


def _rational(value: object) -> Fraction:
    if type(value) is not Fraction:
        raise AdoptionError("an exact Fraction is required")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_BITS:
        raise AdoptionError("rational exceeds its bit cap")
    return value


def _key(square: Square) -> SquareKey:
    return tuple(sorted((tuple(x.coeffs), tuple(y.coeffs)) for x, y in square))


def _images(square: Square, side: FieldElement) -> tuple[Square, ...]:
    images: list[Square] = []
    for reflected in (False, True):
        current = tuple((side - x if reflected else x, y) for x, y in square)
        for _turn in range(4):
            images.append(current)
            current = tuple((side - y, x) for x, y in current)
    return tuple(images)


def _encode_key(key: SquareKey) -> list[list[list[str]]]:
    return [[[str(value) for value in coordinate] for coordinate in point] for point in key]


def _square(square: Square, side: FieldElement) -> int:
    if len(square) != 4 or any(len(point) != 2 for point in square):
        raise AdoptionError("square requires four cyclic corners")
    for point in square:
        for value in point:
            if not isinstance(value, FieldElement) or value.field is not side.field:
                raise AdoptionError("source geometry uses another field")
            for coefficient in value.coeffs:
                _rational(coefficient)
            if value.sign() < 0 or (side - value).sign() < 0:
                raise AdoptionError("source square escapes the container")
    p, q, r, s = square
    e, f = (q[0] - p[0], q[1] - p[1]), (s[0] - p[0], s[1] - p[1])
    if (
        e[0] * e[0] + e[1] * e[1] != 1
        or f[0] * f[0] + f[1] * f[1] != 1
        or not (e[0] * f[0] + e[1] * f[1]).is_zero()
        or r != (p[0] + e[0] + f[0], p[1] + e[1] + f[1])
    ):
        raise AdoptionError("source corners are not an ordered unit square")
    orientation = (e[0] * f[1] - e[1] * f[0]).sign()
    if orientation == 0:
        raise AdoptionError("degenerate source square")
    return orientation


def _binding(seeds: Sequence[Square], support: Support, metadata: dict[str, Any]):
    side = support.side
    if not isinstance(side, FieldElement) or type(side.field) is not NumberField:
        raise AdoptionError("source requires an exact NumberField")
    if not 1 <= side.field.degree <= 8 or side.sign() <= 0 or not 1 <= len(seeds) <= 11:
        raise AdoptionError("source field, side or seed count exceeds admission")
    for value in side.coeffs:
        _rational(value)
    for seed in seeds:
        _square(seed, side)
    if not verify_packing(seeds, side, sign=exact_sign).valid:
        raise AdoptionError("source is not an exact packing")
    labels: dict[SquareKey, list[list[int]]] = {}
    seed_orbits: list[tuple[SquareKey, ...]] = []
    for index, seed in enumerate(seeds):
        images = _images(seed, side)
        seed_orbits.append(tuple(sorted({_key(square) for square in images})))
        for image_index, square in enumerate(images):
            labels.setdefault(_key(square), []).append(
                [index, image_index // 4, image_index % 4]
            )
    expected = sorted(set(seed_orbits))
    if not 1 <= len(support.orbits) <= 8 or any(
        not 1 <= len(orbit) <= 8 for orbit in support.orbits
    ):
        raise AdoptionError("support orbit inventory exceeds admission")
    for orbit in support.orbits:
        for square in orbit:
            _square(square, side)
    actual = [tuple(_key(square) for square in orbit) for orbit in support.orbits]
    if actual != expected:
        raise AdoptionError("support differs from the complete source D4 closure")
    counts = [sum(_key(seed) in orbit for seed in seeds) for orbit in expected]
    baseline = [
        Fraction(count, len(orbit)) for count, orbit in zip(counts, expected, strict=True)
    ]
    for orbit, weight in zip(expected, baseline, strict=True):
        if weight <= 0 or any(Fraction(len(labels[key]), 8) != weight for key in orbit):
            raise AdoptionError("source preimages do not establish the positive baseline")
    expected_metadata = {
        "side": [str(value) for value in side.coeffs],
        "orbits": [[_encode_key(key) for key in orbit] for orbit in expected],
        "preimages": [
            {"square": _encode_key(key), "labels": labels[key]} for key in sorted(labels)
        ],
        "sizes": list(support.sizes),
        "original_counts": counts,
        "uniform_weights": [str(value) for value in baseline],
    }
    if json.dumps(metadata, sort_keys=True) != json.dumps(expected_metadata, sort_keys=True):
        raise AdoptionError("source metadata differs from complete labelled reconstruction")
    return seed_orbits, expected, baseline


def _specification(spec: Specification, seed_count: int) -> None:
    count = len(spec.representatives)
    if (
        type(spec.source) is not str
        or not 1 <= len(spec.source) <= 64
        or not 1 <= count <= 8
        or len(set(spec.representatives)) != count
        or any(
            type(index) is not int or not 0 <= index < seed_count
            for index in spec.representatives
        )
        or len(spec.sizes) != count
        or len(spec.original_counts) != count
        or any(type(size) is not int or not 1 <= size <= 8 for size in spec.sizes)
        or any(type(value) is not int or not 1 <= value <= 11 for value in spec.original_counts)
        or not 1 <= len(spec.rows) <= 7
        or len(spec.rows) != len(spec.multipliers)
    ):
        raise AdoptionError("invalid frozen source or certificate inventory")
    if _rational(spec.bound) != seed_count:
        raise AdoptionError("bound must match the original packing's mass")
    for row in spec.rows:
        if len(row.point) != 2 or _rational(row.radius) <= 0:
            raise AdoptionError("box requires a positive radius and two coordinates")
        for value in row.point:
            _rational(value)
        if len(row.counts) != count or any(
            type(value) is not int or not 0 <= value <= size
            for value, size in zip(row.counts, spec.sizes, strict=True)
        ):
            raise AdoptionError("row counts exceed distinct orbit members")
    if any(_rational(value) < 0 for value in spec.multipliers):
        raise AdoptionError("negative upper multiplier")
    combined = tuple(
        sum(
            (
                weight * row.counts[column]
                for weight, row in zip(spec.multipliers, spec.rows, strict=True)
            ),
            Fraction(),
        )
        for column in range(count)
    )
    if combined != spec.sizes or sum(spec.multipliers, Fraction()) != spec.bound:
        raise AdoptionError("multiplier identity does not give the exact frozen ceiling")


def _box(row: BoxRow, side: FieldElement) -> tuple[Point, ...]:
    bounds = [
        (side.field.rational(value - row.radius), side.field.rational(value + row.radius))
        for value in row.point
    ]
    if any(low.sign() <= 0 or (side - high).sign() <= 0 for low, high in bounds):
        raise AdoptionError("closed box is not strictly inside the container")
    return tuple((x, y) for x in bounds[0] for y in bounds[1])


def contains_box(square: Square, corners: tuple[Point, ...], side: FieldElement) -> bool:
    """Certify every point of a closed box strictly inside either cyclic orientation."""
    orientation = _square(square, side)
    if len(corners) != 4 or any(len(point) != 2 for point in corners):
        raise AdoptionError("box requires four corners")
    if any(value.field is not side.field for point in corners for value in point):
        raise AdoptionError("box field mismatch")
    for index, (x, y) in enumerate(square):
        nx, ny = square[(index + 1) % 4]
        for px, py in corners:
            if (orientation * ((nx - x) * (py - y) - (ny - y) * (px - x))).sign() <= 0:
                return False
    return True


def check_certificate(
    source: str,
    seeds: Sequence[Square],
    support: Support,
    metadata: dict[str, Any],
    spec: Specification,
) -> dict[str, Any]:
    """Check a caller-bound source and frozen rows, without loading scientific data.

    Returned member IDs are [current_orbit, member_index] in full source metadata.
    This in-process API has finite inventory guards but no hard wall-time guarantee.
    Exceptions or interrupted output never establish a ceiling.
    """
    if source != spec.source:
        raise AdoptionError("source identity mismatch")
    _specification(spec, len(seeds))
    seed_orbits, orbit_keys, baseline = _binding(seeds, support, metadata)
    permutation = [orbit_keys.index(seed_orbits[index]) for index in spec.representatives]
    if sorted(permutation) != list(range(len(orbit_keys))):
        raise AdoptionError("representatives do not bijectively bind every source orbit")
    if (
        tuple(support.sizes[index] for index in permutation) != spec.sizes
        or tuple(metadata["original_counts"][index] for index in permutation)
        != spec.original_counts
    ):
        raise AdoptionError("representative counts or orbit permutation mismatch")
    mass = sum(
        (weight * size for weight, size in zip(baseline, support.sizes, strict=True)),
        Fraction(),
    )
    if mass != spec.bound:
        raise AdoptionError("source baseline mass differs from the ceiling")
    results: list[dict[str, Any]] = []
    for row in spec.rows:
        corners = _box(row, support.side)
        selected: list[list[int]] = []
        for column, quota in enumerate(row.counts):
            orbit_index = permutation[column]
            found = 0
            for member_index, square in enumerate(support.orbits[orbit_index]):
                if found == quota:
                    break
                if contains_box(square, corners, support.side):
                    selected.append([orbit_index, member_index])
                    found += 1
            if found != quota:
                raise AdoptionError(
                    f"strict inclusion quota unmet in row {len(results)}, column {column}"
                )
        if len({tuple(member) for member in selected}) != sum(row.counts):
            raise AdoptionError("selected member identities are duplicated")
        results.append(
            {
                "point": [str(value) for value in row.point],
                "radius": str(row.radius),
                "counts": list(row.counts),
                "selected_members": selected,
                "strict_inclusions_verified": True,
            }
        )
    result = {
        "version": 1,
        "kind": "d4-positive-inclusion-support-ceiling",
        "source": source,
        "status": "verified_support_ceiling",
        "ceiling_proved": True,
        "predicate": "necessary-lower-incidence",
        "scope": SCOPE,
        "field": support.side.field.precondition_certificate(),
        "support": metadata,
        "archive_representatives": list(spec.representatives),
        "archive_to_current": permutation,
        "rows": results,
        "multipliers": [str(value) for value in spec.multipliers],
        "combined_coefficients": list(spec.sizes),
        "upper_bound": str(spec.bound),
        "baseline_mass": str(mass),
        "baseline_verified": True,
        "labelled_images": 8 * len(seeds),
        "distinct_placements": sum(support.sizes),
        "selected_incidences": sum(sum(row.counts) for row in spec.rows),
        "shared_components": ["accepted source seed", "NumberField", "exact packing verifier"],
    }
    if len(json.dumps(result, sort_keys=True).encode()) > MAX_OUTPUT_BYTES:
        raise AdoptionError("result exceeds the output byte cap")
    return result


def trump_specification() -> Specification:
    """The seven contributed constants; no archive import or source construction."""
    rows = (
        ((961, 752), (1, 1, 0, 0, 1, 0, 0, 0)),
        ((922, 922), (1, 2, 0, 0, 0, 0, 0, 0)),
        ((2621, 3017), (0, 1, 1, 0, 1, 0, 2, 2)),
        ((1887, 2893), (0, 0, 2, 2, 1, 0, 0, 1)),
        ((1939, 3154), (0, 0, 2, 2, 2, 0, 0, 0)),
        ((2025, 1308), (0, 0, 0, 1, 0, 2, 3, 2)),
        ((1939, 1489), (0, 0, 0, 0, 0, 4, 2, 2)),
    )
    return Specification(
        "trump11-v1",
        (0, 2, 4, 7, 10, 8, 6, 9),
        (4, 8, 8, 8, 8, 8, 8, 8),
        (3, 1, 2, 1, 1, 1, 1, 1),
        tuple(
            BoxRow((Fraction(x, 1000), Fraction(y, 1000)), Fraction(1, 100000), counts)
            for (x, y), counts in rows
        ),
        tuple(Fraction(value) for value in (1, 3, 1, 1, "5/2", 1, "3/2")),
        Fraction(11),
    )


def check_trump() -> dict[str, Any]:
    """Explicit scientific entry point; requires separately authorized invocation."""
    seeds, support, metadata = reconstruct_source("trump11-v1")
    field = support.side.field.precondition_certificate()
    polynomial = [str(Fraction(value, 5)) for value in (5, -10, -2, 14, 12, -6, 2, 2, -1)]
    if (
        field["normalized_minimal_polynomial"] != polynomial
        or field["declared_isolating_interval"] != ["9/25", "37/100"]
        or len(seeds) != 11
        or sum(support.sizes) != 60
        or len(support.orbits) != 8
    ):
        raise AdoptionError("fixed Trump field, real embedding or 88/60/8 source mismatch")
    return check_certificate("trump11-v1", seeds, support, metadata, trump_specification())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-trump", action="store_true", required=True)
    parser.parse_args(argv)
    try:
        result = check_trump()
    except (ValueError, ArithmeticError, RuntimeError) as error:
        print(
            json.dumps(
                {
                    "status": "unresolved",
                    "ceiling_proved": False,
                    "reason": str(error)[:512],
                    "scope": SCOPE,
                },
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
