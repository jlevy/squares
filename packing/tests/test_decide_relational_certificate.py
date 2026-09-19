"""Admission controls for the relational floor-atom reader.

This file is the think-g3j7 gate: floor versus 2-of-5 threshold charges, serializer
round-trip on direction_steps/angle_limit, inert 2**63 operands, and a T-025-shaped
2-of-3 replay through the preserved threshold loader. It does not mutate T-025 bytes
and it is not a covering run.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Never

import pytest

import devtools.decide_relational_certificate as gate
from devtools.decide_relational_certificate import decide, load, main, write_record
from devtools.decide_threshold_certificate import load as load_threshold
from sqpack.fractional.certificate import d4_images
from sqpack.fractional.model import Atom, rotation_from_half_tangent
from sqpack.fractional.relational import (
    FLOOR_VARIANT,
    RELATIONAL_VARIANT,
    FloorAtom,
    FloorCertificate,
    closed_form_relational_conditions,
    disjoint_floor_charge_sum,
    exact_relational_charge,
    minimum_charge_event_cell,
    minimum_charge_interval_boxes,
)
from sqpack.fractional.threshold import ThresholdAtom, ThresholdCertificate
from tests.test_decide_threshold_certificate import write as write_threshold
from tests.test_fractional_threshold_interval import tight_certificate

SIDE = Fraction(2)
SQUARE = Fraction(1, 2)
LIMIT = Fraction(21, 50)
STEPS = 2
AXIS = rotation_from_half_tangent("0", Fraction(0))


def bomb(*_args: object, **_kwargs: object) -> Never:
    raise AssertionError("a coverage route ran after a decisive refusal")


def no_routes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(gate, "minimum_charge_event_cell", bomb)
    monkeypatch.setattr(gate, "minimum_charge_interval_boxes", bomb)


def _five_sites() -> tuple[tuple[Fraction, Fraction], ...]:
    return tuple((Fraction(k + 1, 10), Fraction(1, 2)) for k in range(5))


def _contains(inside: frozenset[tuple[Fraction, Fraction]]):
    return lambda x, y: (x, y) in inside


def _floor_certificate(
    *,
    atoms: tuple[Atom, ...] = (),
    threshold_atoms: tuple[ThresholdAtom, ...] = (),
    floor_atoms: tuple[FloorAtom, ...] = (),
    n: int = 100,
) -> FloorCertificate:
    return FloorCertificate(
        n=n,
        outer_side=SIDE,
        square_side=SQUARE,
        atoms=atoms,
        threshold_atoms=threshold_atoms,
        floor_atoms=floor_atoms,
        direction_steps=STEPS,
        angle_limit=LIMIT,
    )


def _closed_points(x: Fraction, y: Fraction, weight: Fraction) -> tuple[Atom, ...]:
    sites = dict.fromkeys(d4_images(x, y, SIDE), weight)
    return tuple(
        Atom(f"{index:04d}", px, py, weight)
        for index, ((px, py), weight) in enumerate(sorted(sites.items()))
    )


def test_a_four_site_core_of_a_2_of_5_atom_is_not_a_floor_charge() -> None:
    sites = _five_sites()
    threshold = ThresholdAtom(sites, 2, Fraction(1))
    floor = FloorAtom(sites, (1, 1, 1, 1, 1), 2, Fraction(1))
    four = _contains(frozenset(sites[:4]))
    assert threshold.charge(four) == 1
    assert floor.charge(four) == 2
    assert threshold.budget == 2
    assert floor.budget == 2
    three = _contains(frozenset(sites[:3]))
    assert threshold.charge(three) == 1
    assert floor.charge(three) == 1


def test_unit_floor_and_threshold_agree_only_when_the_support_is_below_2k() -> None:
    sites = _five_sites()[:3]
    threshold = ThresholdAtom(sites, 2, Fraction(1))
    floor = FloorAtom(sites, (1, 1, 1), 2, Fraction(1))
    assert threshold.budget == floor.budget == 1
    for mask in range(8):
        held = frozenset(site for bit, site in enumerate(sites) if mask & (1 << bit))
        contains = _contains(held)
        assert threshold.charge(contains) == floor.charge(contains)


def test_zero_weight_is_admitted_and_zero_multiplicity_is_refused() -> None:
    sites = _five_sites()[:2]
    zero = FloorAtom(sites, (1, 1), 2, Fraction(0))
    assert zero.budget == 0
    assert zero.charge(_contains(frozenset(sites))) == 0
    assert zero.inert
    try:
        FloorAtom(sites, (0, 1), 2, Fraction(1))
    except ValueError:
        pass
    else:
        raise AssertionError("zero multiplicity must be refused")


def test_invalid_signs_and_denominators_are_refused() -> None:
    sites = _five_sites()[:2]
    try:
        FloorAtom(sites, (1, 1), 2, Fraction(-1))
    except ValueError:
        pass
    else:
        raise AssertionError("negative weight must be refused")
    try:
        FloorAtom(sites, (1, 1), 1, Fraction(1))
    except ValueError:
        pass
    else:
        raise AssertionError("divisor 1 must be refused")
    try:
        FloorAtom(sites, (1, -1), 2, Fraction(1))
    except ValueError:
        pass
    else:
        raise AssertionError("negative multiplicity must be refused")
    try:
        FloorAtom.from_record(
            {
                "variant": FLOOR_VARIANT,
                "sites": [["1/0", "0"]],
                "multiplicities": [1],
                "divisor": 2,
                "weight": "1",
            }
        )
    except TypeError, ValueError:
        pass
    else:
        raise AssertionError("denominator 0 must be refused")


def test_floor_certificate_round_trips_direction_steps_not_half_tangents() -> None:
    atoms = _closed_points(Fraction(1, 5), Fraction(2, 5), Fraction(1, 7))
    seed = FloorAtom(
        ((Fraction(1, 5), Fraction(3, 5)), (Fraction(2, 5), Fraction(3, 5))),
        (1, 1),
        2,
        Fraction(1, 3),
    )
    certificate = _floor_certificate(atoms=atoms, floor_atoms=seed.orbit(SIDE))
    record = certificate.to_record()
    assert "half_tangents" not in record
    assert record["direction_steps"] == STEPS
    assert record["angle_limit"] == str(LIMIT)
    assert record["variant"] == RELATIONAL_VARIANT
    loaded = FloorCertificate.from_record(record)
    assert loaded.direction_steps == certificate.direction_steps
    assert loaded.angle_limit == certificate.angle_limit
    assert loaded.half_tangents == certificate.half_tangents
    assert loaded.floor_atoms == certificate.floor_atoms
    assert [(a.x, a.y, a.weight) for a in loaded.atoms] == [
        (a.x, a.y, a.weight) for a in certificate.atoms
    ]
    try:
        FloorCertificate.from_record({**record, "half_tangents": ["0", "1/2"]})
    except ValueError:
        pass
    else:
        raise AssertionError("half_tangents must not load")


def test_declared_budget_mismatch_is_refused_before_coverage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    no_routes(monkeypatch)
    certificate = _floor_certificate(
        atoms=_closed_points(Fraction(1, 5), Fraction(2, 5), Fraction(1, 7)),
        floor_atoms=FloorAtom(
            ((Fraction(1, 5), Fraction(3, 5)), (Fraction(2, 5), Fraction(3, 5))),
            (1, 1),
            2,
            Fraction(1, 3),
        ).orbit(SIDE),
    )
    path = tmp_path / "budget.json"
    record = certificate.to_record()
    record["total_budget"] = "1/2"
    write_record(path, record)
    assert decide(path, workers=1) is False
    out = capsys.readouterr().out
    assert "declared total_budget 1/2" in out
    assert "REFUSED" in out


def test_shared_sites_add_independent_floor_charges() -> None:
    shared = (Fraction(1, 2), Fraction(1, 2))
    extra = (Fraction(3, 5), Fraction(1, 2))
    other = (Fraction(4, 5), Fraction(1, 2))
    left = FloorAtom((shared, extra), (1, 1), 2, Fraction(1))
    right = FloorAtom((shared, other), (1, 1), 2, Fraction(1))
    both = _contains(frozenset({shared, extra, other}))
    only_shared = _contains(frozenset({shared}))
    assert left.charge(both) + right.charge(both) == 2
    assert left.charge(only_shared) == 0
    assert right.charge(only_shared) == 0
    assert exact_relational_charge((), (), (left, right), both) == 2


def test_closed_boundary_membership_includes_the_site() -> None:
    site = (Fraction(1), Fraction(1))
    atom = FloorAtom((site,), (2,), 2, Fraction(1))
    half = SQUARE / 2
    centre_u, centre_v = site[0] + half, site[1]

    def contains(x: Fraction, y: Fraction) -> bool:
        u = AXIS.ux * x + AXIS.uy * y
        v = AXIS.vx * x + AXIS.vy * y
        return abs(u - centre_u) <= half and abs(v - centre_v) <= half

    assert contains(*site)
    assert atom.charge(contains) == 1
    outside_u = site[0] + half + Fraction(1, 100)

    def missed(x: Fraction, y: Fraction) -> bool:
        u = AXIS.ux * x + AXIS.uy * y
        v = AXIS.vx * x + AXIS.vy * y
        return abs(u - outside_u) <= half and abs(v - centre_v) <= half

    assert not missed(*site)
    assert atom.charge(missed) == 0


def test_d4_orbit_carries_multiplicities_and_does_not_collapse_unequal_weights() -> None:
    sites = tuple((Fraction(x, 5), Fraction(1)) for x in (1, 2, 3, 4))
    uneven = FloorAtom(sites, (3, 1, 1, 1), 2, Fraction(1))
    images = uneven.images(SIDE)
    assert images[0].multiplicities == (3, 1, 1, 1)
    assert images[1].sites[0] == (SIDE - sites[0][0], sites[0][1])
    assert images[1].multiplicities == (3, 1, 1, 1)
    keys = {image.key for image in uneven.orbit(SIDE)}
    assert len(keys) == len(uneven.orbit(SIDE))
    assert len(uneven.orbit(SIDE)) > 1


def test_disjoint_cores_cannot_outcharge_the_floor_budget() -> None:
    atom = FloorAtom(_five_sites(), (1, 1, 1, 1, 1), 2, Fraction(3, 2))
    assert disjoint_floor_charge_sum(atom, (2, 2)) == Fraction(3)
    assert disjoint_floor_charge_sum(atom, (4,)) == Fraction(3)
    assert disjoint_floor_charge_sum(atom, (2, 2, 1)) == Fraction(3)
    assert disjoint_floor_charge_sum(atom, (2, 2, 1)) <= atom.budget
    try:
        disjoint_floor_charge_sum(atom, (3, 3))
    except ValueError:
        pass
    else:
        raise AssertionError("overlapping traces must be refused")


def test_inert_floor_atoms_stay_exact_zero_without_overflow() -> None:
    site = ((Fraction(3, 2), Fraction(3, 2)),)
    cases = (
        FloorAtom(site, (1,), 2, Fraction(1)),
        FloorAtom(site, (1,), 2, Fraction(2**63)),
        FloorAtom(site, (1,), 2**63, Fraction(1)),
    )
    for atom in cases:
        assert atom.inert
        assert atom.budget == 0
        assert atom.charge(_contains(frozenset(site))) == 0
        event = minimum_charge_event_cell(
            (), (), (atom,), AXIS, outer_side=Fraction(3), square_side=SQUARE
        )
        interval = minimum_charge_interval_boxes(
            (), (), (atom,), AXIS, outer_side=Fraction(3), square_side=SQUARE
        )
        assert event[0] == 0
        assert interval[0] == 0


def test_both_exact_routes_agree_on_a_mixed_2_of_3_and_floor() -> None:
    atoms = (Atom("0", Fraction(1, 2), Fraction(1, 2), Fraction(1, 5)),)
    threshold = ThresholdAtom(
        (
            (Fraction(1, 5), Fraction(1, 5)),
            (Fraction(2, 5), Fraction(1, 5)),
            (Fraction(3, 5), Fraction(1, 5)),
        ),
        2,
        Fraction(1, 4),
    )
    floor = FloorAtom(
        (
            (Fraction(3, 5), Fraction(1, 2)),
            (Fraction(4, 5), Fraction(1, 2)),
            (Fraction(1), Fraction(1, 2)),
        ),
        (1, 1, 1),
        2,
        Fraction(1, 2),
    )
    event = minimum_charge_event_cell(
        atoms, (threshold,), (floor,), AXIS, outer_side=SIDE, square_side=SQUARE
    )
    interval = minimum_charge_interval_boxes(
        atoms, (threshold,), (floor,), AXIS, outer_side=SIDE, square_side=SQUARE
    )
    assert event[0] == interval[0]
    half = SQUARE / 2
    cu, cv = event[1]

    def contains(x: Fraction, y: Fraction) -> bool:
        u = AXIS.ux * x + AXIS.uy * y
        v = AXIS.vx * x + AXIS.vy * y
        return abs(u - cu) <= half and abs(v - cv) <= half

    assert exact_relational_charge(atoms, (threshold,), (floor,), contains) == event[0]


def test_weighted_majority_records_load_without_becoming_floor_atoms() -> None:
    sites = _five_sites()[:3]
    weighted = ThresholdAtom(sites, 2, Fraction(1, 2), (2, 1, 1))
    certificate = _floor_certificate(threshold_atoms=(weighted,))
    record = certificate.to_record()
    assert record["threshold_atoms"][0]["variant"] == "weighted-threshold/v1"
    assert "floor_atoms" in record
    loaded = FloorCertificate.from_record(record)
    assert loaded.threshold_atoms[0].multiplicities == (2, 1, 1)
    two_sites = _contains(frozenset(sites[:2]))
    assert loaded.threshold_atoms[0].charge(two_sites) == Fraction(1, 2)
    assert loaded.floor_atoms == ()


def test_ordinary_threshold_bytes_are_delegated_not_loaded_as_floor() -> None:
    tight = tight_certificate()
    record = {
        "id": "C-test-threshold",
        "variant": "threshold",
        "n": tight.n,
        "claim": f"s({tight.n}) >= {tight.outer_side}",
        "outer_side": str(tight.outer_side),
        "square_side": str(tight.square_side),
        "angle_limit": "207107/500000",
        "direction_steps": 6,
        "symmetry": "D4",
        "total_budget": str(tight.total_budget),
        "atoms": [[str(a.x), str(a.y), str(a.weight)] for a in tight.atoms],
        "threshold_atoms": [atom.to_record() for atom in tight.threshold_atoms],
    }
    try:
        load(json.dumps(record).encode())
    except gate.FormatError:
        pass
    else:
        raise AssertionError("ordinary threshold bytes must not enter the floor loader")


def test_threshold_mode_redecides_a_synthetic_2_of_3(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    tight = tight_certificate()
    path = write_threshold(tmp_path, tight)
    assert decide(path, workers=1) is True
    out = capsys.readouterr().out
    assert "ordinary threshold record; delegating to the T-025 loader" in out
    assert "RETAINABLE" in out
    loaded, _ = load_threshold(path.read_bytes())
    assert isinstance(loaded, ThresholdCertificate)
    assert loaded.threshold_atoms == tight.threshold_atoms
    assert loaded.total_budget == tight.total_budget


def test_malformed_records_are_refused_before_coverage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    no_routes(monkeypatch)
    path = tmp_path / "inexact.json"
    path.write_text('{"variant": "relational/v1", "n": 1.5}')
    assert decide(path, workers=1) is False
    assert "inexact JSON number '1.5'" in capsys.readouterr().out


def test_closed_form_failures_are_refused_before_coverage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    no_routes(monkeypatch)
    seed = FloorAtom(
        ((Fraction(1, 5), Fraction(3, 5)), (Fraction(2, 5), Fraction(3, 5))),
        (1, 1),
        2,
        Fraction(1, 3),
    )
    certificate = _floor_certificate(
        atoms=_closed_points(Fraction(1, 5), Fraction(2, 5), Fraction(1, 7)),
        floor_atoms=(seed,),
    )
    reports = closed_form_relational_conditions(certificate)
    assert any(not report.holds and "floor atoms" in report.name for report in reports)
    path = tmp_path / "broken.json"
    write_record(path, certificate.to_record())
    assert decide(path, workers=1) is False
    out = capsys.readouterr().out
    assert "Condition 1' floor atoms" in out
    assert "REFUSED" in out


def test_the_command_line_skips_a_duplicate_path_and_refuses_missing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    certificate = _floor_certificate(
        atoms=_closed_points(Fraction(1, 5), Fraction(2, 5), Fraction(1, 7)),
        floor_atoms=FloorAtom(
            ((Fraction(1, 5), Fraction(3, 5)), (Fraction(2, 5), Fraction(3, 5))),
            (1, 1),
            2,
            Fraction(1, 3),
        ).orbit(SIDE),
        n=1,
    )
    path = tmp_path / "tiny.json"
    write_record(path, certificate.to_record())
    assert main([str(path), str(path)]) == 1
    out = capsys.readouterr().out
    assert "SKIPPED duplicate path" in out
    assert main([str(tmp_path / "missing.json")]) == 1
    assert "REFUSED" in capsys.readouterr().out


def test_the_tool_does_not_import_t025_verify_claim() -> None:
    source = Path(gate.__file__).read_text(encoding="utf-8")
    assert "n11_threshold_certificate" not in source
    assert "import verify_claim" not in source
