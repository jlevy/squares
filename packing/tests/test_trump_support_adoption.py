"""Source-free BC259 controls; neither the fixed certificate nor Trump is evaluated."""

from __future__ import annotations

import copy
import json
from dataclasses import replace
from fractions import Fraction

import pytest

from devtools import check_full_size_density_support_ceiling as source_reader
from devtools import check_trump_support_adoption as checker
from sqpack.field import NumberField
from sqpack.full_size_density.support_ceiling import Support, axis_square


@pytest.fixture(autouse=True)
def forbid_science(monkeypatch):
    def forbidden(*_args, **_kwargs):
        raise AssertionError("scientific construction is forbidden in these controls")

    monkeypatch.setattr(source_reader, "build", forbidden)
    monkeypatch.setattr(checker, "check_trump", forbidden)
    monkeypatch.setattr(checker, "trump_specification", forbidden)

    def unrelated_field(polynomial, interval):
        if tuple(polynomial) == tuple(source_reader.U_MIN_POLY):
            raise AssertionError("the legacy algebraic toy uses the scientific field")
        return NumberField(polynomial, interval)

    monkeypatch.setattr(source_reader, "NumberField", unrelated_field)


def toy(monkeypatch, *, quadratic=False):
    if quadratic:
        field = NumberField((1, 0, -3), (1, 2))
        c, s = field.alpha / 2, field.rational(Fraction(1, 2))
        square = tuple(
            (field.one + c * x - s * y, field.one + s * x + c * y)
            for x, y in (
                (-Fraction(1, 2), -Fraction(1, 2)),
                (Fraction(1, 2), -Fraction(1, 2)),
                (Fraction(1, 2), Fraction(1, 2)),
                (-Fraction(1, 2), Fraction(1, 2)),
            )
        )
        seeds, side = (square,), field.rational(2)
        spec = checker.Specification(
            "toy-v1",
            (0,),
            (2,),
            (1,),
            (checker.BoxRow((Fraction(1), Fraction(1)), Fraction(1, 10), (2,)),),
            (Fraction(1),),
            Fraction(1),
        )
    else:
        field = NumberField((1, 0), (-1, 1))
        seeds = tuple(
            axis_square(
                field.rational(Fraction(2 * x + 1, 2)), field.rational(Fraction(2 * y + 1, 2))
            )
            for x in range(3)
            for y in range(3)
        )
        side = field.rational(3)
        spec = checker.Specification(
            "toy-v1",
            (4, 0, 1),
            (1, 4, 4),
            (1, 4, 4),
            (
                checker.BoxRow((Fraction(1, 2), Fraction(1, 2)), Fraction(1, 10), (0, 1, 0)),
                checker.BoxRow((Fraction(1, 2), Fraction(3, 2)), Fraction(1, 10), (0, 0, 1)),
                checker.BoxRow((Fraction(3, 2), Fraction(3, 2)), Fraction(1, 10), (1, 0, 0)),
            ),
            (Fraction(4), Fraction(4), Fraction(1)),
            Fraction(9),
        )
    monkeypatch.setattr(source_reader, "load_source", lambda _name: (seeds, side))
    return (*source_reader.reconstruct_source("toy-v1"), spec)


def run(data, **changes):
    seeds, support, metadata, spec = data
    return checker.check_certificate(
        "toy-v1", seeds, support, metadata, replace(spec, **changes)
    )


def test_positive_and_nontrivial_permutation(monkeypatch):
    result = run(toy(monkeypatch))
    assert result["status"] == "verified_support_ceiling"
    assert result["ceiling_proved"] is True
    assert result["upper_bound"] == result["baseline_mass"] == "9"
    assert result["archive_to_current"] == [2, 0, 1]
    assert result["selected_incidences"] == 3
    assert all(len(row["selected_members"]) == sum(row["counts"]) for row in result["rows"])


def test_quadratic_same_center_squares_and_reflected_corners(monkeypatch):
    seeds, support, metadata, spec = toy(monkeypatch, quadratic=True)
    reflected = Support(
        support.side,
        tuple(tuple(tuple(reversed(square)) for square in orbit) for orbit in support.orbits),
    )
    result = checker.check_certificate("toy-v1", seeds, reflected, metadata, spec)
    assert result["upper_bound"] == "1"
    assert result["selected_incidences"] == 2
    assert len({tuple(member) for member in result["rows"][0]["selected_members"]}) == 2


def test_source_and_metadata_mutations(monkeypatch):
    seeds, support, metadata, spec = toy(monkeypatch)
    with pytest.raises(checker.AdoptionError, match="source"):
        checker.check_certificate("wrong", seeds, support, metadata, spec)
    for name, value in (
        ("sizes", [1, 4, 4]),
        ("original_counts", [4, 3, 2]),
        ("uniform_weights", ["0", "1", "1"]),
        ("preimages", []),
    ):
        changed = copy.deepcopy(metadata)
        changed[name] = value
        with pytest.raises(checker.AdoptionError, match="metadata"):
            checker.check_certificate("toy-v1", seeds, support, changed, spec)
    duplicate = Support(
        support.side, ((support.orbits[0][0], *support.orbits[0]), *support.orbits[1:])
    )
    with pytest.raises(checker.AdoptionError, match="support"):
        checker.check_certificate("toy-v1", seeds, duplicate, metadata, spec)


def test_wrong_orbit_contract_and_multipliers(monkeypatch):
    data = toy(monkeypatch)
    for changes in (
        {"representatives": (4, 0, 0)},
        {"representatives": (4, 1, 0)},
        {"sizes": (4, 1, 4)},
        {"original_counts": (1, 3, 5)},
        {"multipliers": (Fraction(3), Fraction(4), Fraction(1))},
        {"multipliers": (Fraction(-4), Fraction(4), Fraction(1))},
    ):
        with pytest.raises(checker.AdoptionError):
            run(data, **changes)


def test_box_boundary_wall_radius_and_quota_refusals(monkeypatch):
    data = toy(monkeypatch)
    first, *rest = data[3].rows
    for bad in (
        replace(first, radius=Fraction(0)),
        replace(first, radius=Fraction(-1)),
        replace(first, radius=Fraction(1, 2)),
        replace(first, point=(Fraction(1), Fraction(1, 2))),
        replace(first, counts=(0, 4, 0)),
    ):
        with pytest.raises(checker.AdoptionError):
            run(data, rows=(bad, *rest))


def test_foreign_field_and_nonpacking_source(monkeypatch):
    seeds, support, metadata, spec = toy(monkeypatch)
    other = NumberField((1, 0), (-1, 1))
    corner = support.orbits[0][0][0]
    malformed = ((other.rational(corner[0].coeffs[0]), corner[1]), *support.orbits[0][0][1:])
    changed = Support(support.side, ((malformed, *support.orbits[0][1:]), *support.orbits[1:]))
    with pytest.raises(checker.AdoptionError, match="field"):
        checker.check_certificate("toy-v1", seeds, changed, metadata, spec)
    with pytest.raises(checker.AdoptionError, match="packing"):
        checker.check_certificate(
            "toy-v1", (seeds[0], seeds[0], *seeds[2:]), support, metadata, spec
        )


def test_missing_row_and_exact_type_refusals(monkeypatch):
    data = toy(monkeypatch)
    with pytest.raises(checker.AdoptionError):
        run(data, rows=data[3].rows[:-1])
    for bad in (True, 0.1, "1e100000000"):
        with pytest.raises(checker.AdoptionError):
            run(data, bound=bad)


def test_false_integer_metadata_and_label_omission(monkeypatch):
    seeds, support, metadata, spec = toy(monkeypatch)
    for change in ("boolean", "omit", "duplicate"):
        altered = copy.deepcopy(metadata)
        labels = altered["preimages"][0]["labels"]
        if change == "boolean":
            labels[0][0] = False
        elif change == "omit":
            labels.pop()
        else:
            labels.append(labels[0])
        with pytest.raises(checker.AdoptionError, match="metadata"):
            checker.check_certificate("toy-v1", seeds, support, altered, spec)


def test_selected_members_and_positive_only_scope(monkeypatch):
    data = toy(monkeypatch)
    result = run(data)
    assert result["predicate"] == "necessary-lower-incidence"
    assert result["labelled_images"] == 72
    assert result["distinct_placements"] == 9
    for row, expected in zip(result["rows"], data[3].rows, strict=True):
        for column, quota in enumerate(expected.counts):
            current = result["archive_to_current"][column]
            assert sum(member[0] == current for member in row["selected_members"]) == quota
    assert "exclusions_verified" not in result


def test_source_escape_and_noncyclic_order(monkeypatch):
    seeds, support, metadata, spec = toy(monkeypatch)
    escaped = tuple((x - 1, y) for x, y in seeds[0])
    with pytest.raises(checker.AdoptionError, match="escapes"):
        checker.check_certificate("toy-v1", (escaped, *seeds[1:]), support, metadata, spec)
    p, q, r, s = support.orbits[0][0]
    altered = Support(
        support.side, (((p, r, q, s), *support.orbits[0][1:]), *support.orbits[1:])
    )
    with pytest.raises(checker.AdoptionError, match="ordered unit square"):
        checker.check_certificate("toy-v1", seeds, altered, metadata, spec)


def test_output_cap_and_cli_refusal(monkeypatch, capsys):
    data = toy(monkeypatch)
    monkeypatch.setattr(checker, "MAX_OUTPUT_BYTES", 1)
    with pytest.raises(checker.AdoptionError, match="byte cap"):
        run(data)

    def refused():
        raise checker.AdoptionError("source-free refusal control")

    monkeypatch.setattr(checker, "check_trump", refused)
    assert checker.main(["--target-trump"]) == 2
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["status"] == "unresolved"
    assert receipt["ceiling_proved"] is False


def test_explicit_cli_dispatch_only(monkeypatch, capsys):
    data = toy(monkeypatch)
    with pytest.raises(SystemExit) as missing:
        checker.main([])
    assert missing.value.code == 2
    capsys.readouterr()
    receipt = run(data)
    monkeypatch.setattr(checker, "check_trump", lambda: receipt)
    assert checker.main(["--target-trump"]) == 0
    assert json.loads(capsys.readouterr().out) == receipt
