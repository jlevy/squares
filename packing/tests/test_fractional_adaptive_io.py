"""BC-230 parsing and cover controls; loading is not a retention decision."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import cast

import pytest

from devtools.decide_certificate import load as load_scalar
from sqpack.fractional import adaptive_io
from sqpack.fractional.adaptive import AdaptiveCertificate, specialize_scalar, sweep_minima
from sqpack.fractional.adaptive_interval import interval_minima
from sqpack.fractional.adaptive_io import (
    AdaptiveFormatError,
    load,
    load_bytes,
    validate_closed_cover,
    validate_endpoints,
)
from sqpack.fractional.certificate import Certificate, d4_images


def _record() -> dict[str, object]:
    """Serialized form of the unchanged slice-01 P4 control, not a target."""
    cells = []
    for index, (tangent, lower, upper, mismatch, side) in enumerate(
        (
            ("0", "0", "1/4", "1/4", "7/10"),
            ("1/4", "1/4", "56/71", "1/4", "3/4"),
            ("9/20", "56/71", "1", "16/89", "4/5"),
        )
    ):
        cells.append(
            {
                "index": index,
                "half_tangent": tangent,
                "lower_boundary_tangent": lower,
                "upper_boundary_tangent": upper,
                "max_mismatch_tangent": mismatch,
                "square_side": side,
            }
        )
    return {
        "id": "BC-231-P4-control",
        "variant": "adaptive-unconditional",
        "n": 11,
        "claim": "s(11) >= 6/5",
        "outer_side": "6/5",
        "symmetry": "D4",
        "containment_rule": "legacy-linear-v1",
        "seam_owner": "lower-index",
        "angle_cells": cells,
        "total_mass": "7/5",
        "least_cell_mass": "6/5",
        "atoms": [
            ["3/5", "3/5", "1"],
            ["3/10", "3/5", "1/10"],
            ["9/10", "3/5", "1/10"],
            ["3/5", "3/10", "1/10"],
            ["3/5", "9/10", "1/10"],
        ],
    }


def _cells(record: dict[str, object]) -> list[dict[str, object]]:
    return cast(list[dict[str, object]], record["angle_cells"])


def _encode(record: dict[str, object]) -> bytes:
    return json.dumps(record).encode("utf-8")


def _serialize(control: AdaptiveCertificate) -> dict[str, object]:
    record = _record()
    record.update(
        n=control.n,
        outer_side=str(control.outer_side),
        claim=f"s({control.n}) >= {control.outer_side}",
        total_mass=str(control.total_mass),
        least_cell_mass=None,
        atoms=[[str(atom.x), str(atom.y), str(atom.weight)] for atom in control.atoms],
        angle_cells=[
            {
                "index": cell.index,
                "half_tangent": str(cell.half_tangent),
                "lower_boundary_tangent": str(cell.lower_boundary_tangent),
                "upper_boundary_tangent": str(cell.upper_boundary_tangent),
                "max_mismatch_tangent": str(cell.max_mismatch_tangent),
                "square_side": str(cell.square_side),
            }
            for cell in control.cells
        ],
    )
    return record


def test_p4_bytes_feed_the_two_project_routes_without_a_retention_verdict(
    tmp_path: Path,
) -> None:
    path = tmp_path / "control.json"
    data = _encode(_record())
    path.write_bytes(data)
    parsed = load(path)
    assert parsed == load_bytes(data)
    assert parsed.identifier == "BC-231-P4-control"
    assert parsed.declared_total_mass == Fraction(7, 5)
    assert parsed.declared_least_cell_mass == Fraction(6, 5)
    expected = (Fraction(6, 5), Fraction(13, 10), Fraction(7, 5))
    assert tuple(row.minimum for row in sweep_minima(parsed.certificate)) == expected
    enclosed = interval_minima(parsed.certificate)
    for outcome in enclosed.directions:
        index = int(outcome.label.removesuffix("'"))
        assert outcome.lower is not None
        assert outcome.upper is not None
        assert Fraction(outcome.lower, enclosed.scale) == expected[index]
        assert Fraction(outcome.upper, enclosed.scale) == expected[index]
    assert path.read_bytes() == data


@pytest.mark.parametrize("declaration", [None, "0", "4999/5000", "100"])
def test_minimum_is_untrusted_input_not_a_coverage_or_retention_decision(
    declaration: str | None,
) -> None:
    record = _record()
    record["least_cell_mass"] = declaration
    parsed = load_bytes(_encode(record))
    expected = None if declaration is None else Fraction(declaration)
    assert parsed.declared_least_cell_mass == expected


def test_serialized_small_scalar_control_preserves_equal_sides_and_minima() -> None:
    control = load_bytes(_encode(_record())).certificate
    scalar = Certificate(
        control.n,
        control.outer_side,
        Fraction(7, 10),
        control.atoms,
        tuple(cell.half_tangent for cell in control.cells),
    )
    adapted = specialize_scalar(scalar)
    parsed = load_bytes(_encode(_serialize(adapted)))
    assert parsed.certificate.cells == adapted.cells
    assert tuple(row.minimum for row in sweep_minima(parsed.certificate)) == tuple(
        row.minimum for row in sweep_minima(adapted)
    )


@pytest.mark.parametrize("field", list(_record()))
def test_each_top_level_field_is_required(field: str) -> None:
    record = _record()
    del record[field]
    with pytest.raises(AdaptiveFormatError, match=f"missing.*{field}"):
        load_bytes(_encode(record))


@pytest.mark.parametrize("field", list(_cells(_record())[0]))
def test_each_angle_cell_field_is_required(field: str) -> None:
    record = _record()
    del _cells(record)[0][field]
    with pytest.raises(AdaptiveFormatError, match=f"missing.*{field}"):
        load_bytes(_encode(record))


@pytest.mark.parametrize("field", ["source", "square_side", "direction_steps", "angle_limit"])
def test_unknown_or_scalar_fields_are_refused(field: str) -> None:
    record = _record()
    record[field] = "unused"
    with pytest.raises(AdaptiveFormatError, match=f"unknown.*{field}"):
        load_bytes(_encode(record))
    record = _record()
    # square_side is required within an angle cell, only forbidden at the top level.
    cell_field = "source" if field == "square_side" else field
    _cells(record)[0][cell_field] = "unused"
    with pytest.raises(AdaptiveFormatError, match=f"unknown.*{cell_field}"):
        load_bytes(_encode(record))


@pytest.mark.parametrize("field", ["variant", "symmetry", "containment_rule", "seam_owner"])
def test_literal_policies_are_closed(field: str) -> None:
    record = _record()
    record[field] = "unsupported"
    with pytest.raises(AdaptiveFormatError, match=field):
        load_bytes(_encode(record))


@pytest.mark.parametrize("value", [True, "11", 1.5])
@pytest.mark.parametrize("field", ["n", "index"])
def test_integer_fields_do_not_coerce(value: object, field: str) -> None:
    record = _record()
    target = record if field == "n" else _cells(record)[0]
    target[field] = value
    with pytest.raises(AdaptiveFormatError, match=r"integer|inexact JSON number"):
        load_bytes(_encode(record))


@pytest.mark.parametrize("value", ["2/4", "0/7", "01", "-0", "+1", "1.0", "1e0", "1/0"])
def test_noncanonical_rationals_are_not_rescued_by_numeric_equality(value: str) -> None:
    record = _record()
    record["least_cell_mass"] = value
    with pytest.raises(AdaptiveFormatError, match="canonical rational"):
        load_bytes(_encode(record))


@pytest.mark.parametrize("token", ["0.5", "NaN", "Infinity", "-Infinity"])
def test_all_inexact_and_nonfinite_json_tokens_are_refused(token: str) -> None:
    data = _encode(_record()).replace(b'"6/5"', token.encode(), 1)
    with pytest.raises(AdaptiveFormatError, match="inexact JSON number"):
        load_bytes(data)


@pytest.mark.parametrize("key", ["n", "index"])
def test_duplicate_keys_are_refused_before_object_construction(key: str) -> None:
    data = _encode(_record()).replace(f'"{key}":'.encode(), f'"{key}": 0, "{key}":'.encode(), 1)
    with pytest.raises(AdaptiveFormatError, match=f"duplicate.*{key}"):
        load_bytes(data)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("angle_cells", {}, "array"),
        ("atoms", {}, "array"),
        ("angle_cells", [None, None], "object"),
        ("atoms", [["0", "0"]], "three"),
        ("atoms", ["0,0,1"], "array"),
        ("id", 1, "string"),
        ("claim", False, "string"),
        ("n", 0, "positive"),
        ("outer_side", "0", "positive"),
        ("least_cell_mass", 1, "rational string"),
    ],
)
def test_structural_and_scalar_refusals(field: str, value: object, message: str) -> None:
    record = _record()
    record[field] = value
    with pytest.raises(AdaptiveFormatError, match=message):
        load_bytes(_encode(record))


@pytest.mark.parametrize("data", [b"[]", b"{", b"\xff", b"[" * 2000])
def test_bad_json_and_deep_nesting_have_named_format_refusals(data: bytes) -> None:
    with pytest.raises(AdaptiveFormatError):
        load_bytes(data)


@pytest.mark.parametrize(
    ("index", "field", "value", "message"),
    [
        (1, "index", 0, "indices"),
        (1, "half_tangent", "0", "strictly increasing"),
        (0, "half_tangent", "1/10", "start at zero"),
        (2, "half_tangent", "1/3", "bracket"),
        (2, "half_tangent", "1", r"lie in \[0, 1\)"),
        (1, "lower_boundary_tangent", "1/3", "derived boundary"),
        (0, "upper_boundary_tangent", "1/3", "derived boundary"),
        (0, "max_mismatch_tangent", "0", "derived mismatch"),
        (0, "square_side", "4/5", "strict containment"),
        (0, "square_side", "9/10", "strict containment"),
        (0, "square_side", "0", "positive core side"),
        (0, "square_side", "-1", "positive core side"),
    ],
)
def test_serialized_cell_mutations_fail_before_coverage(
    index: int, field: str, value: object, message: str
) -> None:
    record = _record()
    _cells(record)[index][field] = value
    with pytest.raises(AdaptiveFormatError, match=message):
        load_bytes(_encode(record))


def test_missing_swapped_and_overfold_angle_cells_are_refused() -> None:
    record = _record()
    del _cells(record)[1]
    with pytest.raises(AdaptiveFormatError, match="indices"):
        load_bytes(_encode(record))
    record = _record()
    cells = _cells(record)
    cells[0], cells[1] = cells[1], cells[0]
    with pytest.raises(AdaptiveFormatError, match="indices"):
        load_bytes(_encode(record))
    record = _record()
    cells = _cells(record)
    cells[1]["half_tangent"] = "9/20"
    cells[2]["half_tangent"] = "1/2"
    with pytest.raises(AdaptiveFormatError, match="bracket"):
        load_bytes(_encode(record))


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("missing image", "complete equal-weight D4"),
        ("unequal image", "complete equal-weight D4"),
        ("negative weight", "nonnegative"),
        ("duplicate site", "distinct"),
        ("outside support", "inside the container"),
        ("false total", "declared total_mass"),
        ("total equals n", "strictly below n"),
        ("false claim", "claim differs"),
    ],
)
def test_serialized_measure_and_claim_premises(mutation: str, message: str) -> None:
    record = _record()
    atoms = cast(list[list[str]], record["atoms"])
    if mutation == "missing image":
        atoms.pop()
    elif mutation == "unequal image":
        atoms[-1][2] = "1/20"
    elif mutation == "negative weight":
        atoms[0][2] = "-1"
    elif mutation == "duplicate site":
        atoms.append(atoms[0].copy())
    elif mutation == "outside support":
        atoms[0][0] = "2"
    elif mutation == "false total":
        record["total_mass"] = "1"
    elif mutation == "total equals n":
        atoms[0][2] = "53/5"
        record["total_mass"] = "11"
    else:
        record["claim"] = "s(12) >= 6/5"
    with pytest.raises(AdaptiveFormatError, match=message):
        load_bytes(_encode(record))


def test_listed_zero_orbit_is_a_schema_rule_not_a_mass_multiplicity() -> None:
    record = _record()
    atoms = cast(list[list[str]], record["atoms"])
    images = sorted(set(d4_images(Fraction(1, 5), Fraction(3, 10), Fraction(6, 5))))
    assert len(images) == 8
    atoms.extend([[str(x), str(y), "0"] for x, y in images])
    complete = load_bytes(_encode(record))
    assert complete.certificate.total_mass == Fraction(7, 5)
    assert tuple(row.minimum for row in sweep_minima(complete.certificate)) == (
        Fraction(6, 5),
        Fraction(13, 10),
        Fraction(7, 5),
    )
    atoms.pop()
    with pytest.raises(AdaptiveFormatError, match="complete equal-weight D4"):
        load_bytes(_encode(record))


@pytest.mark.parametrize("outer", ["7/10", "1/2"])
def test_empty_or_singleton_center_domains_still_have_control_route_refusals(
    outer: str,
) -> None:
    record = _record()
    center = str(Fraction(outer) / 2)
    record.update(
        outer_side=outer,
        claim=f"s(11) >= {outer}",
        total_mass="1",
        least_cell_mass=None,
        atoms=[[center, center, "1"]],
    )
    control = load_bytes(_encode(record)).certificate
    with pytest.raises(ValueError, match="positive-area centre domain"):
        sweep_minima(control)
    with pytest.raises(ValueError, match="does not fit the container"):
        interval_minima(control)


def test_adaptive_axis_ceiling_does_not_refuse_equality_on_that_guard() -> None:
    record = _record()
    record.update(
        outer_side="14/5", claim="s(11) >= 14/5", total_mass="0", atoms=[], least_cell_mass=None
    )
    parsed = load_bytes(_encode(record))
    assert parsed.certificate.outer_side == 4 * parsed.certificate.cells[0].square_side
    record.update(outer_side="3", claim="s(11) >= 3")
    with pytest.raises(AdaptiveFormatError, match="axis-core method ceiling"):
        load_bytes(_encode(record))


@pytest.mark.parametrize("limit", ["bytes", "atoms", "angle_cells", "rational"])
def test_each_frozen_input_limit_fires_before_geometry(
    limit: str, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        adaptive_io,
        "validate_angle_declarations",
        lambda _cells: pytest.fail("geometry ran before the input-budget refusal"),
    )
    record = _record()
    if limit == "atoms":
        record["atoms"] = [["0", "0", "0"]] * (adaptive_io.MAX_ATOMS + 1)
    elif limit == "angle_cells":
        record["angle_cells"] = [_cells(record)[0]] * (adaptive_io.MAX_ANGLE_CELLS + 1)
    elif limit == "rational":
        record["least_cell_mass"] = "1" * (adaptive_io.MAX_RATIONAL_TEXT + 1)
    data = _encode(record)
    if limit == "bytes":
        data += b" " * (adaptive_io.MAX_CERTIFICATE_BYTES + 1 - len(data))
    with pytest.raises(AdaptiveFormatError, match="limit"):
        load_bytes(data)
    path = tmp_path / "oversized.json"
    path.write_bytes(data)
    with pytest.raises(AdaptiveFormatError, match="limit"):
        load(path)


def test_frozen_limits_and_inclusive_byte_and_rational_boundaries() -> None:
    assert (
        adaptive_io.MAX_CERTIFICATE_BYTES,
        adaptive_io.MAX_ATOMS,
        adaptive_io.MAX_ANGLE_CELLS,
        adaptive_io.MAX_RATIONAL_TEXT,
    ) == (8_388_608, 4_096, 10_001, 512)
    record = _record()
    record["least_cell_mass"] = "1" * 512
    data = _encode(record)
    data += b" " * (8_388_608 - len(data))
    parsed = load_bytes(data)
    assert parsed.declared_least_cell_mass == Fraction("1" * 512)


def _cover() -> tuple[tuple[Fraction, Fraction], ...]:
    return (
        (Fraction(0), Fraction(1, 3)),
        (Fraction(1, 3), Fraction(2, 3)),
        (Fraction(2, 3), Fraction(1)),
    )


def test_f4_gap_and_overlap_reach_the_pure_cover_branch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        adaptive_io,
        "validate_angle_declarations",
        lambda _cells: pytest.fail("declarations ran"),
    )
    monkeypatch.setattr(adaptive_io, "load_bytes", lambda _data: pytest.fail("JSON parser ran"))
    valid = _cover()
    validate_closed_cover(valid)
    for lower, refusal in ((Fraction(2, 5), "gap"), (Fraction(1, 4), "overlap")):
        changed = (valid[0], (lower, valid[1][1]), valid[2])
        with pytest.raises(AdaptiveFormatError, match=refusal):
            validate_closed_cover(changed)


def test_f5_axis_and_fold_reach_the_pure_endpoint_branch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        adaptive_io,
        "validate_angle_declarations",
        lambda _cells: pytest.fail("declarations ran"),
    )
    monkeypatch.setattr(adaptive_io, "load_bytes", lambda _data: pytest.fail("JSON parser ran"))
    valid = _cover()
    validate_endpoints(valid)
    with pytest.raises(AdaptiveFormatError, match="axis endpoint"):
        validate_endpoints(((Fraction(1, 100), valid[0][1]), *valid[1:]))
    with pytest.raises(AdaptiveFormatError, match="fold endpoint"):
        validate_endpoints((*valid[:-1], (valid[-1][0], Fraction(99, 100))))


def _redeclare(cells: list[dict[str, object]]) -> None:
    tangents = tuple(Fraction(cast(str, cell["half_tangent"])) for cell in cells)
    seams = (Fraction(0), *((a + b) / (1 - a * b) for a, b in pairwise(tangents)), Fraction(1))
    for index, (cell, tangent) in enumerate(zip(cells, tangents, strict=True)):
        cosine = (1 - tangent * tangent) / (1 + tangent * tangent)
        sine = 2 * tangent / (1 + tangent * tangent)
        lower, upper = seams[index : index + 2]
        mismatch = max(abs(sine - cosine * q) / (cosine + sine * q) for q in (lower, upper))
        cell.update(
            lower_boundary_tangent=str(lower),
            upper_boundary_tangent=str(upper),
            max_mismatch_tangent=str(mismatch),
        )


def test_f5_redeclared_n12_mutation_reaches_final_seam_not_stale_field_refusal() -> None:
    path = (
        Path(__file__).resolve().parents[1]
        / "cases/n12_fractional_certificate/certificate.json"
    )
    frozen = path.read_bytes()
    scalar, _ = load_scalar(path)
    record = _serialize(specialize_scalar(scalar))
    cells = _cells(record)
    cells[-1]["half_tangent"] = "1/2"
    _redeclare(cells)
    assert cells[-1]["lower_boundary_tangent"] == "164144306/142927847"
    with pytest.raises(AdaptiveFormatError, match=r"final seam q_K >= 1"):
        load_bytes(_encode(record))
    # A stale declaration is a different branch and must precede the final-seam check.
    cells[-1]["max_mismatch_tangent"] = "0"
    with pytest.raises(AdaptiveFormatError, match="derived mismatch"):
        load_bytes(_encode(record))
    assert path.read_bytes() == frozen


@pytest.mark.parametrize(
    "relative_path",
    [
        "n11_fractional_certificate/certificate.json",
        "n12_fractional_certificate/certificate.json",
        "n11_fractional_certificate/thirdparty/control-n17-massaccesi.json",
    ],
)
def test_retained_scalar_bytes_only_supply_serialized_geometry_controls(
    relative_path: str,
) -> None:
    path = Path(__file__).resolve().parents[1] / "cases" / relative_path
    frozen = path.read_bytes()
    scalar, _ = load_scalar(path)
    control = specialize_scalar(scalar)
    parsed = load_bytes(_encode(_serialize(control)))
    assert parsed.certificate.cells == control.cells
    assert parsed.certificate.total_mass == control.total_mass
    assert tuple((a.x, a.y, a.weight) for a in parsed.certificate.atoms) == tuple(
        (a.x, a.y, a.weight) for a in control.atoms
    )
    assert parsed.declared_least_cell_mass is None
    assert path.read_bytes() == frozen
