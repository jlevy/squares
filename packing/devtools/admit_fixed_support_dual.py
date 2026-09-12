"""Independently admit an exact dual over a D4-closed placement support.

The historical A6 receipt stores a sparse row matrix.  This reader does not use that
matrix to decide the certificate.  It partitions a retained, D4-closed placement
family into exact orbits, matches each declared column representative to one
reconstructed orbit, and recomputes the coefficient of every priced row with
``Placement.contains`` and ``Fraction`` arithmetic.

Supported priced rows are point-depth inequalities and threshold-atom orbit
inequalities.  This is the small row vocabulary needed by the retained A6 dual, while
the admission logic is independent of its particular counts and rational values.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from sqpack.fractional.ceiling import CeilingCertificate, Placement
from sqpack.fractional.threshold import ThresholdAtom

KIND = "fixed-support-dual-admission/v1"
DEPTH_ROW_KIND = "depth-at-site"
ATOM_ROW_KINDS = frozenset({"atom-orbit", "seeded-atom-orbit"})
DEPTH_BUDGET = Fraction(1)
RATIONAL_PATTERN = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")

PlacementKey = tuple[Fraction, Fraction, Fraction, Fraction]
Point = tuple[Fraction, Fraction]


class InputError(ValueError):
    """An input path cannot be decoded as strict JSON."""


class AdmissionError(ValueError):
    """A decoded record does not establish the claimed exact dual bound."""


@dataclass(frozen=True, slots=True)
class SupportOrbit:
    """One exact D4 orbit of support placements."""

    keys: tuple[PlacementKey, ...]
    placements: tuple[Placement, ...]


@dataclass(frozen=True, slots=True)
class CertificateColumn:
    """A certificate column matched to an independently reconstructed support orbit."""

    ordinal: int
    orbit: SupportOrbit
    representative: PlacementKey


@dataclass(frozen=True, slots=True)
class PricedRow:
    """One priced inequality with its exact, independently rebuilt coefficients."""

    ordinal: int
    kind: str
    multiplier: Fraction
    budget: Fraction
    coefficients: Mapping[int, int]


def _mapping(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise AdmissionError(f"{context} must be a JSON object")
    return value


def _array(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise AdmissionError(f"{context} must be a JSON array")
    return value


def _integer(value: Any, context: str, *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise AdmissionError(f"{context} must be a JSON integer at least {minimum}")
    return value


def _boolean(value: Any, context: str) -> bool:
    if not isinstance(value, bool):
        raise AdmissionError(f"{context} must be a JSON boolean")
    return value


def _fraction(value: Any, context: str) -> Fraction:
    if not isinstance(value, str) or RATIONAL_PATTERN.fullmatch(value) is None:
        raise AdmissionError(f"{context} must be an exact rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise AdmissionError(f"{context} is not a rational number: {value!r}") from error


def _point(value: Any, context: str, outer_side: Fraction) -> Point:
    raw = _array(value, context)
    if len(raw) != 2:
        raise AdmissionError(f"{context} must have two entries")
    point = (_fraction(raw[0], f"{context}[0]"), _fraction(raw[1], f"{context}[1]"))
    if not (0 <= point[0] <= outer_side and 0 <= point[1] <= outer_side):
        raise AdmissionError(f"{context} {point} lies outside [0, {outer_side}]^2")
    return point


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InputError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def load_record(path: Path, context: str) -> Mapping[str, Any]:
    """Read a JSON object while refusing duplicate keys.

    Decimal display fields are preserved as ``Decimal`` objects.  Every field used in
    an admission decision must still pass ``_fraction`` and therefore be a rational
    string.
    """

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise InputError(f"cannot read {context} {path}: {error}") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_float=Decimal,
        )
    except (json.JSONDecodeError, InputError) as error:
        raise InputError(f"cannot decode {context} {path}: {error}") from error
    if not isinstance(value, Mapping):
        raise InputError(f"{context} {path} must contain a JSON object")
    return value


def _placement_key(placement: Placement) -> PlacementKey:
    return (
        placement.half_tangent,
        placement.centre_x,
        placement.centre_y,
        placement.side,
    )


def _placement_images(key: PlacementKey, outer_side: Fraction) -> tuple[PlacementKey, ...]:
    tangent, centre_x, centre_y, side = key
    if tangent > 1:
        raise AdmissionError(
            f"support half-tangent {tangent} is outside the folded D4 range [0, 1]"
        )
    reflected = (1 - tangent) / (1 + tangent)
    images: set[PlacementKey] = set()
    for image_tangent, start_x, start_y in (
        (tangent, centre_x, centre_y),
        (reflected, outer_side - centre_x, centre_y),
    ):
        x, y = start_x, start_y
        for _quarter_turn in range(4):
            images.add((image_tangent, x, y, side))
            x, y = outer_side - y, x
    return tuple(sorted(images))


def _support_family(
    record: Mapping[str, Any],
) -> tuple[CeilingCertificate, tuple[PlacementKey, ...]]:
    n = _integer(record.get("n"), "support field 'n'", minimum=1)
    outer_side = _fraction(record.get("outer_side"), "support field 'outer_side'")
    square_side = _fraction(record.get("square_side"), "support field 'square_side'")
    raw_tangents = _array(record.get("half_tangents"), "support field 'half_tangents'")
    tangents = [
        _fraction(value, f"support field 'half_tangents[{index}]'")
        for index, value in enumerate(raw_tangents)
    ]
    raw_placements = _array(record.get("placements"), "support field 'placements'")
    for index, value in enumerate(raw_placements):
        placement = _array(value, f"support placement {index}")
        if len(placement) != 5:
            raise AdmissionError(f"support placement {index} must have five entries")
        for field, token in zip(
            ("half_tangent", "centre_x", "centre_y", "weight", "side"),
            placement,
            strict=True,
        ):
            _fraction(token, f"support placement {index} field '{field}'")
    declared_total = _fraction(record.get("total_weight"), "support field 'total_weight'")
    try:
        family = CeilingCertificate.from_record(
            {
                "n": n,
                "outer_side": str(outer_side),
                "square_side": str(square_side),
                "half_tangents": [str(value) for value in tangents],
                "placements": raw_placements,
            }
        )
    except (TypeError, ValueError, KeyError, ZeroDivisionError) as error:
        raise AdmissionError(f"invalid support family: {error}") from error
    if family.total_weight != declared_total:
        raise AdmissionError(
            "support total_weight does not match its placements: "
            f"declared {declared_total}, recomputed {family.total_weight}"
        )
    if not family.placements:
        raise AdmissionError("support family has no placements")
    for index, placement in enumerate(family.placements):
        if placement.weight <= 0:
            raise AdmissionError(f"support placement {index} must have positive weight")
        if placement.side != family.square_side:
            raise AdmissionError(
                f"support placement {index} has side {placement.side}, "
                f"expected {family.square_side}"
            )

    return family, tuple(_placement_key(placement) for placement in family.placements)


def _representative(
    value: Any, context: str, outer_side: Fraction, square_side: Fraction
) -> PlacementKey:
    record = _mapping(value, context)
    key = (
        _fraction(record.get("half_tangent"), f"{context} field 'half_tangent'"),
        _fraction(record.get("centre_x"), f"{context} field 'centre_x'"),
        _fraction(record.get("centre_y"), f"{context} field 'centre_y'"),
        _fraction(record.get("side"), f"{context} field 'side'"),
    )
    if key[3] != square_side:
        raise AdmissionError(
            f"{context} side {key[3]} does not match support side {square_side}"
        )
    if not (0 <= key[1] <= outer_side and 0 <= key[2] <= outer_side):
        raise AdmissionError(f"{context} centre lies outside [0, {outer_side}]^2")
    return key


def _support_orbits(
    placement_keys: tuple[PlacementKey, ...], outer_side: Fraction
) -> tuple[SupportOrbit, ...]:
    if len(set(placement_keys)) != len(placement_keys):
        raise AdmissionError("support family repeats a positive placement")
    support = set(placement_keys)
    remaining = set(placement_keys)
    orbits: list[SupportOrbit] = []
    while remaining:
        representative = min(remaining)
        keys = _placement_images(representative, outer_side)
        missing = set(keys) - support
        if missing:
            raise AdmissionError(
                "support family is not exactly D4-closed; the orbit of "
                f"{representative} is missing {min(missing)}"
            )
        orbits.append(
            SupportOrbit(
                keys,
                tuple(
                    Placement(tangent, x, y, Fraction(0), side) for tangent, x, y, side in keys
                ),
            )
        )
        remaining.difference_update(keys)
    return tuple(orbits)


def _columns(
    dual: Mapping[str, Any],
    support_orbits: tuple[SupportOrbit, ...],
    outer_side: Fraction,
    square_side: Fraction,
) -> tuple[CertificateColumn, ...]:
    raw_columns = _array(dual.get("columns"), "dual field 'columns'")
    if not raw_columns:
        raise AdmissionError("dual field 'columns' must be nonempty")
    support_by_key = {
        key: orbit_index
        for orbit_index, orbit in enumerate(support_orbits)
        for key in orbit.keys
    }
    by_ordinal: dict[int, CertificateColumn] = {}
    used_support_orbits: dict[int, int] = {}
    for index, raw_column in enumerate(raw_columns):
        context = f"dual column {index}"
        column = _mapping(raw_column, context)
        ordinal = _integer(column.get("orbit"), f"{context} field 'orbit'")
        if ordinal >= len(raw_columns):
            raise AdmissionError(f"{context} ordinal {ordinal} is outside the column range")
        if ordinal in by_ordinal:
            raise AdmissionError(f"duplicate dual column ordinal {ordinal}")
        representative = _representative(
            column.get("representative"),
            f"{context} representative",
            outer_side,
            square_side,
        )
        try:
            support_orbit_index = support_by_key[representative]
        except KeyError as error:
            raise AdmissionError(
                f"{context} representative is absent from the retained support"
            ) from error
        if support_orbit_index in used_support_orbits:
            raise AdmissionError(
                f"{context} repeats the support orbit used by column "
                f"{used_support_orbits[support_orbit_index]}"
            )
        orbit = support_orbits[support_orbit_index]
        if _placement_images(representative, outer_side) != orbit.keys:
            raise AdmissionError(f"{context} does not reconstruct its exact support orbit")
        used_support_orbits[support_orbit_index] = ordinal
        declared_size = _integer(
            column.get("orbit_size"), f"{context} field 'orbit_size'", minimum=1
        )
        if declared_size != len(orbit.keys):
            raise AdmissionError(
                f"{context} orbit_size is {declared_size}, exact D4 size is {len(orbit.keys)}"
            )
        declared_cost = _fraction(column.get("cost"), f"{context} field 'cost'")
        if declared_cost != len(orbit.keys):
            raise AdmissionError(
                f"{context} cost is {declared_cost}, expected orbit size {len(orbit.keys)}"
            )
        by_ordinal[ordinal] = CertificateColumn(ordinal, orbit, representative)
    columns = tuple(by_ordinal[index] for index in range(len(raw_columns)))
    if len(used_support_orbits) != len(support_orbits):
        missing_orbit = min(set(range(len(support_orbits))) - used_support_orbits.keys())
        raise AdmissionError(
            "certificate columns do not cover the retained support exactly; no "
            f"representative names support orbit {missing_orbit}"
        )
    return columns


def _declared_coefficients(value: Any, context: str, column_count: int) -> dict[int, int]:
    raw_pairs = _array(value, context)
    coefficients: dict[int, int] = {}
    for pair_index, value_pair in enumerate(raw_pairs):
        pair = _array(value_pair, f"{context}[{pair_index}]")
        if len(pair) != 2:
            raise AdmissionError(f"{context}[{pair_index}] must have two entries")
        column = _integer(pair[0], f"{context}[{pair_index}][0]")
        if column >= column_count:
            raise AdmissionError(f"{context}[{pair_index}] names missing column {column}")
        if column in coefficients:
            raise AdmissionError(f"{context} repeats column {column}")
        coefficient = _fraction(pair[1], f"{context}[{pair_index}][1]")
        if coefficient.denominator != 1 or coefficient <= 0:
            raise AdmissionError(
                f"{context}[{pair_index}] coefficient must be a positive integer"
            )
        coefficients[column] = int(coefficient)
    return coefficients


def _row_range(
    kind: str, ordinal: int, depth_rows: int, atom_rows: int, seeded_rows: int
) -> None:
    atom_start = depth_rows
    seed_start = atom_start + atom_rows
    row_end = seed_start + seeded_rows
    if kind == DEPTH_ROW_KIND and ordinal >= depth_rows:
        raise AdmissionError(f"depth row ordinal {ordinal} is outside 0..{depth_rows - 1}")
    if kind == "atom-orbit" and not (atom_start <= ordinal < seed_start):
        raise AdmissionError(
            f"atom row ordinal {ordinal} is outside {atom_start}..{seed_start - 1}"
        )
    if kind == "seeded-atom-orbit" and not (seed_start <= ordinal < row_end):
        raise AdmissionError(
            f"seeded atom row ordinal {ordinal} is outside {seed_start}..{row_end - 1}"
        )


def _depth_coefficients(point: Point, columns: tuple[CertificateColumn, ...]) -> dict[int, int]:
    return {
        column.ordinal: coefficient
        for column in columns
        if (
            coefficient := sum(
                placement.contains(*point) for placement in column.orbit.placements
            )
        )
    }


def _atom_coefficients(
    atom: ThresholdAtom,
    images: tuple[ThresholdAtom, ...],
    columns: tuple[CertificateColumn, ...],
) -> dict[int, int]:
    coefficients: dict[int, int] = {}
    for column in columns:
        coefficient = sum(
            atom_image.trace_count(placement.contains) >= atom.threshold
            for atom_image in images
            for placement in column.orbit.placements
        )
        if coefficient:
            coefficients[column.ordinal] = coefficient
    return coefficients


def _priced_row(
    value: Any,
    row_index: int,
    columns: tuple[CertificateColumn, ...],
    *,
    outer_side: Fraction,
    depth_rows: int,
    atom_rows: int,
    seeded_rows: int,
) -> PricedRow:
    context = f"priced row {row_index}"
    row = _mapping(value, context)
    ordinal = _integer(row.get("row"), f"{context} field 'row'")
    multiplier = _fraction(row.get("multiplier"), f"{context} field 'multiplier'")
    if multiplier <= 0:
        raise AdmissionError(f"{context} multiplier must be positive")
    identity = _mapping(row.get("identity"), f"{context} identity")
    kind = identity.get("kind")
    if kind != DEPTH_ROW_KIND and kind not in ATOM_ROW_KINDS:
        raise AdmissionError(f"{context} has unsupported identity kind {kind!r}")
    assert isinstance(kind, str)
    _row_range(kind, ordinal, depth_rows, atom_rows, seeded_rows)

    if kind == DEPTH_ROW_KIND:
        point = _point(identity.get("site"), f"{context} identity field 'site'", outer_side)
        budget = DEPTH_BUDGET
        coefficients = _depth_coefficients(point, columns)
    else:
        raw_points = _array(identity.get("points"), f"{context} identity field 'points'")
        points = tuple(
            _point(point, f"{context} atom point {index}", outer_side)
            for index, point in enumerate(raw_points)
        )
        threshold = _integer(
            identity.get("threshold"), f"{context} identity field 'threshold'", minimum=1
        )
        # This reader prices ordinary orbit columns. A weighted atom's budget is a token
        # budget and its orbit is keyed on the token counts, so reading one here without
        # them would price a different column; refuse instead of guessing. Outside the
        # `try`, because `AdmissionError` is a `ValueError` and would be relabelled.
        if identity.get("multiplicities") is not None or identity.get("variant") is not None:
            raise AdmissionError(
                f"{context} identity declares token counts, and this reader prices "
                "unweighted orbit columns only"
            )
        try:
            atom = ThresholdAtom(points, threshold, Fraction(1))
        except (TypeError, ValueError) as error:
            raise AdmissionError(f"{context} has an invalid threshold atom: {error}") from error
        images = atom.orbit(outer_side)
        declared_orbit_size = _integer(
            identity.get("orbit_size"),
            f"{context} identity field 'orbit_size'",
            minimum=1,
        )
        if declared_orbit_size != len(images):
            raise AdmissionError(
                f"{context} atom orbit_size is {declared_orbit_size}, "
                f"exact D4 size is {len(images)}"
            )
        # `token_count`, not `size`: see `ThresholdAtom.budget`.
        budget = Fraction(len(images) * (atom.token_count // atom.threshold))
        coefficients = _atom_coefficients(atom, images, columns)

    declared_budget = _fraction(row.get("budget"), f"{context} field 'budget'")
    if declared_budget != budget:
        raise AdmissionError(
            f"{context} budget is {declared_budget}, exact row budget is {budget}"
        )
    declared_coefficients = _declared_coefficients(
        row.get("bounds_support_orbits"),
        f"{context} field 'bounds_support_orbits'",
        len(columns),
    )
    if declared_coefficients != coefficients:
        raise AdmissionError(
            f"{context} stored coefficients differ from exact reconstruction: "
            f"stored {declared_coefficients}, recomputed {coefficients}"
        )
    declared_contribution = _fraction(
        row.get("contribution"), f"{context} field 'contribution'"
    )
    contribution = budget * multiplier
    if declared_contribution != contribution:
        raise AdmissionError(
            f"{context} contribution is {declared_contribution}, expected {contribution}"
        )
    return PricedRow(ordinal, kind, multiplier, budget, coefficients)


def _program_counts(record: Mapping[str, Any]) -> tuple[int, int, int, int]:
    program = _mapping(record.get("program"), "field 'program'")
    depth_rows = _integer(program.get("depth_rows"), "program field 'depth_rows'")
    atom_rows = _integer(program.get("atom_rows"), "program field 'atom_rows'")
    seeded_rows = _integer(program.get("seeded_atom_rows"), "program field 'seeded_atom_rows'")
    rows_total = _integer(program.get("rows_total"), "program field 'rows_total'")
    if rows_total != depth_rows + atom_rows + seeded_rows:
        raise AdmissionError(
            "program rows_total does not equal depth_rows + atom_rows + seeded_atom_rows"
        )
    return rows_total, depth_rows, atom_rows, seeded_rows


def admit_records(
    certificate_record: Mapping[str, Any],
    support_record: Mapping[str, Any],
    *,
    certificate_source: str | None = None,
    support_source: str | None = None,
) -> dict[str, Any]:
    """Rebuild a certificate's support and priced rows and return an exact receipt."""

    if certificate_record.get("kind") != "lane-a6/dual-bracket/v1":
        raise AdmissionError("certificate kind must be 'lane-a6/dual-bracket/v1'")
    family, family_seeds = _support_family(support_record)
    outer_side = _fraction(certificate_record.get("outer_side"), "field 'outer_side'")
    square_side = _fraction(certificate_record.get("square_side"), "field 'square_side'")
    if outer_side != family.outer_side:
        raise AdmissionError(
            f"certificate outer_side {outer_side} does not match support {family.outer_side}"
        )
    if square_side != family.square_side:
        raise AdmissionError(
            f"certificate square_side {square_side} does not match support {family.square_side}"
        )

    support = _mapping(certificate_record.get("support"), "field 'support'")
    declared_placements = _integer(
        support.get("placements"), "support field 'placements'", minimum=1
    )
    declared_orbits = _integer(support.get("d4_orbits"), "support field 'd4_orbits'", minimum=1)
    rows_total, depth_rows, atom_rows, seeded_rows = _program_counts(certificate_record)
    program = _mapping(certificate_record.get("program"), "field 'program'")
    declared_columns = _integer(program.get("columns"), "program field 'columns'", minimum=1)
    dual = _mapping(certificate_record.get("dual"), "field 'dual'")
    support_orbits = _support_orbits(family_seeds, outer_side)
    columns = _columns(dual, support_orbits, outer_side, square_side)
    support_count = sum(len(orbit.keys) for orbit in support_orbits)
    if declared_placements != support_count:
        raise AdmissionError(
            f"declared support has {declared_placements} placements, exact source has "
            f"{support_count}"
        )
    if declared_orbits != len(support_orbits):
        raise AdmissionError(
            f"declared support has {declared_orbits} D4 orbits, exact source has "
            f"{len(support_orbits)}"
        )
    if declared_columns != len(columns):
        raise AdmissionError(
            f"program has {declared_columns} columns, exact support has {len(columns)}"
        )
    raw_rows = _array(dual.get("priced_rows"), "dual field 'priced_rows'")
    declared_priced = _integer(
        dual.get("n_priced_rows"), "dual field 'n_priced_rows'", minimum=1
    )
    if declared_priced != len(raw_rows):
        raise AdmissionError(
            f"dual n_priced_rows is {declared_priced}, but {len(raw_rows)} rows are stored"
        )
    priced_rows = tuple(
        _priced_row(
            row,
            index,
            columns,
            outer_side=outer_side,
            depth_rows=depth_rows,
            atom_rows=atom_rows,
            seeded_rows=seeded_rows,
        )
        for index, row in enumerate(raw_rows)
    )
    ordinals = [row.ordinal for row in priced_rows]
    if len(set(ordinals)) != len(ordinals):
        raise AdmissionError("priced row ordinals must be distinct")
    if any(ordinal >= rows_total for ordinal in ordinals):
        raise AdmissionError("a priced row ordinal is outside program rows_total")

    declared_column_records = {
        _integer(
            _mapping(value, "dual column").get("orbit"), "dual column field 'orbit'"
        ): _mapping(value, "dual column")
        for value in _array(dual.get("columns"), "dual field 'columns'")
    }
    column_results: list[dict[str, Any]] = []
    for column in columns:
        exact_value = sum(
            (row.multiplier * row.coefficients.get(column.ordinal, 0) for row in priced_rows),
            start=Fraction(0),
        )
        cost = Fraction(len(column.orbit.keys))
        slack = exact_value - cost
        stored = declared_column_records[column.ordinal]
        declared_value = _fraction(
            stored.get("A_transpose_u"),
            f"dual column {column.ordinal} field 'A_transpose_u'",
        )
        declared_slack = _fraction(
            stored.get("slack"), f"dual column {column.ordinal} field 'slack'"
        )
        declared_holds = _boolean(
            stored.get("holds"), f"dual column {column.ordinal} field 'holds'"
        )
        if declared_value != exact_value or declared_slack != slack:
            raise AdmissionError(
                f"dual column {column.ordinal} stored A^T u or slack differs from exact "
                f"reconstruction ({exact_value}, {slack})"
            )
        if declared_holds != (slack >= 0):
            raise AdmissionError(f"dual column {column.ordinal} has a false holds flag")
        if slack < 0:
            raise AdmissionError(
                f"dual column {column.ordinal} fails A^T u >= cost by {-slack}"
            )
        column_results.append(
            {
                "orbit": column.ordinal,
                "orbit_size": len(column.orbit.keys),
                "cost": str(cost),
                "A_transpose_u": str(exact_value),
                "slack": str(slack),
            }
        )

    declared_all_hold = _boolean(
        dual.get("a_transpose_u_ge_cost"), "dual field 'a_transpose_u_ge_cost'"
    )
    if not declared_all_hold:
        raise AdmissionError("dual a_transpose_u_ge_cost is false")
    bound = sum((row.multiplier * row.budget for row in priced_rows), start=Fraction(0))
    declared_bound = _fraction(dual.get("bound"), "dual field 'bound'")
    if declared_bound != bound:
        raise AdmissionError(f"dual bound is {declared_bound}, recomputed bound is {bound}")
    bracket = _mapping(certificate_record.get("bracket"), "field 'bracket'")
    upper = _fraction(bracket.get("upper_exact"), "bracket field 'upper_exact'")
    if upper != bound:
        raise AdmissionError(f"bracket upper_exact is {upper}, recomputed bound is {bound}")
    lower = _fraction(bracket.get("lower_exact"), "bracket field 'lower_exact'")

    return {
        "kind": KIND,
        "admitted": True,
        "arithmetic": "exact rational",
        "inputs": {
            "certificate": certificate_source,
            "support_family": support_source,
        },
        "support": {
            "source_positive_placements": len(family_seeds),
            "source_d4_closure_placements": support_count,
            "source_d4_orbits": len(support_orbits),
            "orbit_sizes": sorted(len(column.orbit.keys) for column in columns),
            "source_is_exactly_d4_closed": True,
            "certificate_representatives_match_every_source_orbit_once": True,
            "objective_orbit_costs_match_sizes": True,
        },
        "priced_rows": {
            "count": len(priced_rows),
            "depth_rows": sum(row.kind == DEPTH_ROW_KIND for row in priced_rows),
            "threshold_atom_rows": sum(row.kind in ATOM_ROW_KINDS for row in priced_rows),
            "threshold_atom_rows_use_complete_exact_d4_orbits": True,
            "saved_coefficient_matrix_used_for_decision": False,
            "rows": [
                {
                    "row": row.ordinal,
                    "kind": row.kind,
                    "multiplier": str(row.multiplier),
                    "budget": str(row.budget),
                    "contribution": str(row.multiplier * row.budget),
                    "coefficients": [
                        [column, str(coefficient)]
                        for column, coefficient in sorted(row.coefficients.items())
                    ],
                }
                for row in priced_rows
            ],
        },
        "dual": {
            "bound": str(bound),
            "a_transpose_u_ge_cost": True,
            "minimum_column_slack": str(
                min(Fraction(result["slack"]) for result in column_results)
            ),
            "columns": column_results,
        },
        "scope": {
            "established": (
                "an upper bound for the nonnegative D4-tied program on the reconstructed "
                "fixed support using the seven admitted inequalities"
            ),
            "stronger_full_depth_same_support": {
                "upper_bound_also_applies": True,
                "condition": (
                    "retain the admitted inequalities and add every exact point-depth row; "
                    "adding constraints can only reduce the maximum"
                ),
            },
            "untied_extension": {
                "established_by_reader": False,
                "conditional_upper_bound": (
                    "if the stronger program keeps the admitted threshold-orbit row and "
                    "imposes depth at every point, the same bound applies to untied weights "
                    "by D4 averaging"
                ),
                "checked_premises": [
                    "the 280-placement support is exactly D4-closed",
                    (
                        "each objective orbit cost equals its eight placements, so the "
                        "objective is total placement mass"
                    ),
                    "the threshold inequality sums all eight exact D4 images with budget 8",
                ],
                "obligations": [
                    "the stronger program retains the admitted threshold-orbit inequality",
                    "its complete point-depth row family is D4-invariant",
                    "D4-averaging is invoked to transfer the tied bound to untied weights",
                ],
                "support_closure_obligation_checked": True,
            },
            "selected_row_lower": {
                "declared": str(lower),
                "checked": False,
                "note": (
                    "the reader did not check the candidate family or the other program rows; "
                    "the retained max-depth verdict is 105263157/100000000, above one"
                ),
            },
        },
        "unchecked": [
            "the other declared depth and atom rows",
            "the selected-row lower candidate's feasibility",
            "K0--K3 placement admissibility, containment, depth, and symmetry",
        ],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("support_family", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(argv)
    try:
        certificate = load_record(arguments.certificate, "dual certificate")
        support = load_record(arguments.support_family, "support family")
        receipt = admit_records(
            certificate,
            support,
            certificate_source=str(arguments.certificate),
            support_source=str(arguments.support_family),
        )
    except InputError as error:
        print(
            json.dumps({"kind": KIND, "admitted": False, "error": str(error)}), file=sys.stderr
        )
        return 2
    except AdmissionError as error:
        print(
            json.dumps({"kind": KIND, "admitted": False, "error": str(error)}), file=sys.stderr
        )
        return 1
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if arguments.output is not None:
        atomic_write_text(arguments.output, rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
