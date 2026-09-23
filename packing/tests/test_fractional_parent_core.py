"""Adversarial contracts for adaptive parent-core threshold certificates."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import replace
from fractions import Fraction
from math import ceil
from pathlib import Path
from typing import cast

import pytest

from sqpack.fractional import interval as interval_module
from sqpack.fractional import parent_core_interval
from sqpack.fractional.interval import (
    BATCH,
    MAX_BATCH_SITES,
    MAX_INTERVAL_ATOMS,
    DirectionOutcome,
    IntervalInputError,
)
from sqpack.fractional.model import Atom
from sqpack.fractional.parent_core import (
    ParentCoreCertificate,
    ParentCoreRow,
    load_kleddamag_parent_core,
    validate_parent_core,
)
from sqpack.fractional.parent_core_interval import verify_parent_core_rows
from sqpack.fractional.threshold import ThresholdAtom
from sqpack.fractional.threshold_interval import (
    MAX_BATCH_MEMBER_SLOTS,
    MAX_MEMBER_SLOTS,
    MAX_TOKENS_PER_ATOM,
    ThresholdAtomData,
)

F = Fraction
ZERO = F(0)
HALF = F(1, 2)
ONE = F(1)
FLOAT_ZERO = cast(Fraction, 0.0)
FLOAT_TWO = cast(Fraction, 2.0)
PACKING = Path(__file__).resolve().parents[1]
SOURCE = (
    PACKING
    / "resources/web/external-square-certificates-2026-09-22"
    / "kleddamag-11/global-certificate.json"
)


def _row(
    left: Fraction = ZERO,
    right: Fraction = HALF,
    half_tangent: Fraction = ZERO,
    core_side: Fraction = HALF,
) -> ParentCoreRow:
    return ParentCoreRow(left, right, half_tangent, core_side)


def _certificate(
    *,
    n: int = 1,
    minimum_charge: Fraction = ONE,
    atoms: tuple[Atom, ...] = (),
    threshold_atoms: tuple[ThresholdAtom, ...] = (),
    rows: tuple[ParentCoreRow, ...] = (_row(),),
) -> ParentCoreCertificate:
    return ParentCoreCertificate(
        n=n,
        outer_side=F(4),
        parent_side=F(1),
        minimum_charge=minimum_charge,
        atoms=atoms,
        threshold_atoms=threshold_atoms,
        rows=rows,
    )


@pytest.mark.parametrize(
    ("rows", "message"),
    [
        ((_row(left=F(1, 100)),), "noncontiguous parent-angle partition"),
        (
            (_row(right=F(1, 4)), _row(left=F(1, 3))),
            "noncontiguous parent-angle partition",
        ),
        (
            (_row(right=F(1, 4)), _row(left=F(1, 5))),
            "noncontiguous parent-angle partition",
        ),
        ((_row(right=F(1, 3)),), "does not reach pi/4"),
        ((), "empty parent-angle catalogue"),
    ],
)
def test_parent_angle_catalogue_refuses_gaps_overlaps_and_short_cover(
    rows: tuple[ParentCoreRow, ...], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        validate_parent_core(_certificate(rows=rows))


def test_parent_side_sets_the_domain_while_core_side_sets_membership() -> None:
    row = ParentCoreRow(F(1, 5), F(1, 3), F(1, 4), F(2, 5))
    parent = F(9, 10)
    endpoint_factors = tuple((1 + 2 * u - u * u) / (1 + u * u) for u in (row.left, row.right))

    assert row.centre_margin(parent) == parent * min(endpoint_factors) / 2
    assert row.centre_margin(parent) != row.core_side * min(endpoint_factors) / 2

    invalid = replace(_certificate(), rows=(_row(core_side=F(1)),))
    with pytest.raises(ValueError, match="invalid core side"):
        validate_parent_core(invalid)


@pytest.mark.parametrize(
    "build_certificate",
    [
        lambda: replace(_certificate(), outer_side=4.0),
        lambda: replace(_certificate(), outer_side=True),
        lambda: replace(_certificate(), parent_side=1.0),
        lambda: replace(_certificate(), minimum_charge=1.0),
        lambda: replace(_certificate(), rows=(replace(_row(), left=0.0),)),
        lambda: replace(_certificate(), rows=(replace(_row(), right=0.5),)),
        lambda: replace(_certificate(), rows=(replace(_row(), half_tangent=0.0),)),
        lambda: replace(_certificate(), rows=(replace(_row(), core_side=0.5),)),
        lambda: _certificate(atoms=(Atom("float-x", FLOAT_TWO, F(2), F(0)),)),
        lambda: _certificate(atoms=(Atom("float-y", F(2), FLOAT_TWO, F(0)),)),
        lambda: _certificate(atoms=(Atom("float-weight", F(2), F(2), FLOAT_ZERO),)),
        lambda: _certificate(threshold_atoms=(ThresholdAtom(((FLOAT_TWO, F(2)),), 1, F(0)),)),
        lambda: _certificate(threshold_atoms=(ThresholdAtom(((F(2), F(2)),), 1, FLOAT_ZERO),)),
    ],
)
def test_public_validator_refuses_inexact_float_inputs(
    build_certificate: Callable[[], ParentCoreCertificate],
) -> None:
    with pytest.raises((TypeError, ValueError), match="exact"):
        validate_parent_core(build_certificate())


def test_near_boundary_containment_is_never_decided_from_a_float() -> None:
    almost_parent = float(F(1) - F(1, 10**18))

    with pytest.raises((TypeError, ValueError), match="exact"):
        ParentCoreRow(F(0), F(1, 10**6), F(0), almost_parent)  # type: ignore[arg-type]


def test_counting_gap_is_measured_against_gamma_not_one() -> None:
    centre = Atom("centre", F(2), F(2), F(3, 2))
    scaled_objective = _certificate(minimum_charge=F(2), atoms=(centre,))

    premises = validate_parent_core(scaled_objective)
    assert premises.budget == F(3, 2)

    with pytest.raises(ValueError, match="no strict counting gap"):
        validate_parent_core(replace(scaled_objective, minimum_charge=F(1, 2)))


def test_interval_pruning_uses_the_exact_ceiling_of_gamma(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _certificate(
        minimum_charge=F(1, 2),
        atoms=(Atom("centre", F(2), F(2), F(1, 3)),),
    )
    prune_values: list[int] = []

    class Search:
        def search(self, *, prune_at: int) -> DirectionOutcome:
            prune_values.append(prune_at)
            return DirectionOutcome("0", "certified", prune_at, None, None, 1, 0)

    monkeypatch.setattr(parent_core_interval, "parent_core_search", lambda *_: Search())
    verdict = verify_parent_core_rows(certificate, indices=(0,))

    assert verdict.scale == 3
    assert verdict.threshold_units == ceil(certificate.minimum_charge * verdict.scale) == 2
    assert prune_values == [2]


def test_refutation_outside_the_parent_domain_is_never_accepted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _certificate(minimum_charge=F(1, 2))

    class Search:
        def search(self, *, prune_at: int) -> DirectionOutcome:
            assert prune_at == 1
            # x=0.3 lies inside the core-side margin (0.25) but outside the
            # parent-centre margin (0.5). Accepting it would swap B for A.
            return DirectionOutcome("0", "refuted", 0, 0, (0.3, 2.0), 1, 0)

    monkeypatch.setattr(parent_core_interval, "parent_core_search", lambda *_: Search())
    with pytest.raises(ArithmeticError, match="parent-domain witness"):
        verify_parent_core_rows(certificate, indices=(0,))


def test_exact_membership_seam_in_the_parent_domain_is_never_accepted() -> None:
    coordinates = (F(1, 4), F(3, 4), F(5, 4))
    atoms = tuple(Atom(f"{x}:{y}", x, y, F(1)) for x in coordinates for y in coordinates)
    certificate = ParentCoreCertificate(
        n=10,
        outer_side=F(3, 2),
        parent_side=F(4, 5),
        minimum_charge=F(1),
        atoms=atoms,
        threshold_atoms=(),
        rows=(_row(core_side=F(1, 2)),),
    )

    verdict = verify_parent_core_rows(certificate, batch_size=64)

    assert not verdict.accepted
    assert not verdict.covered
    outcome = verdict.directions[0]
    assert outcome.status == "undecided"
    assert outcome.stalled > 0
    assert not outcome.budget_exhausted
    assert outcome.lower == 0
    assert outcome.upper is not None
    assert outcome.upper >= verdict.threshold_units


def test_box_budget_exhaustion_uses_gamma_threshold_not_unit_scale(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    coordinates = (F(1, 4), F(3, 4), F(5, 4))
    atoms = tuple(Atom(f"{x}:{y}", x, y, F(1, 3)) for x in coordinates for y in coordinates)
    certificate = ParentCoreCertificate(
        n=10,
        outer_side=F(3, 2),
        parent_side=F(4, 5),
        minimum_charge=F(1, 3),
        atoms=atoms,
        threshold_atoms=(),
        rows=(_row(core_side=F(1, 2)),),
    )
    monkeypatch.setattr(interval_module, "BOX_BUDGET", 1)

    verdict = verify_parent_core_rows(certificate, batch_size=64)

    outcome = verdict.directions[0]
    assert verdict.scale == 3
    assert verdict.threshold_units == 1
    assert outcome.budget_exhausted
    assert outcome.status == "undecided"
    assert outcome.upper is not None
    assert verdict.threshold_units <= outcome.upper < verdict.scale
    assert not verdict.covered
    assert not verdict.accepted


def test_two_worker_route_matches_a_real_serial_coverage_fixture() -> None:
    coordinates = (F(1, 2), F(11, 10), F(17, 10), F(23, 10), F(29, 10), F(7, 2))
    atoms = tuple(Atom(f"{x}:{y}", x, y, F(1)) for x in coordinates for y in coordinates)
    rows = (
        _row(right=F(1, 4), core_side=F(7, 10)),
        _row(left=F(1, 4), core_side=F(7, 10)),
    )
    certificate = _certificate(n=37, atoms=atoms, rows=rows)

    serial = verify_parent_core_rows(certificate, workers=1)
    parallel = verify_parent_core_rows(certificate, workers=2)

    assert serial.accepted
    assert parallel.accepted
    assert parallel.premises == serial.premises
    assert parallel.indices == serial.indices
    assert parallel.directions == serial.directions
    assert parallel.scale == serial.scale
    assert parallel.threshold_units == serial.threshold_units
    assert parallel.refutations == serial.refutations


def test_threshold_budget_uses_floor_of_tokens_over_threshold() -> None:
    atom = ThresholdAtom(
        ((F(0), F(0)), (F(1), F(0))),
        threshold=2,
        weight=F(3, 7),
        multiplicities=(2, 3),
    )
    certificate = _certificate(threshold_atoms=(atom,))

    assert atom.token_count == 5
    assert atom.budget == F(6, 7)
    assert certificate.budget == F(6, 7)
    data = ThresholdAtomData.of(certificate)
    assert F(data.budget, data.scale) == F(6, 7)
    assert sorted(data.members[0, :5].tolist()) == [0, 0, 1, 1, 1]


def test_threshold_symmetry_keeps_multiplicity_attached_to_each_site() -> None:
    seed = ThresholdAtom(
        ((F(1), F(1)), (F(1), F(2))),
        threshold=4,
        weight=F(1, 5),
        multiplicities=(2, 3),
    )
    orbit = seed.orbit(F(4))
    certificate = _certificate(minimum_charge=F(10), threshold_atoms=orbit)

    validate_parent_core(certificate)
    with pytest.raises(ValueError, match="threshold charges are not D4 invariant"):
        validate_parent_core(replace(certificate, threshold_atoms=orbit[:-1]))


def test_canonical_source_import_retains_exact_proof_inputs() -> None:
    certificate = load_kleddamag_parent_core(SOURCE)
    premises = validate_parent_core(certificate)

    assert certificate.n == 11
    assert certificate.outer_side == F(191, 50)
    assert certificate.parent_side == F(764, 775)
    assert certificate.minimum_charge == F(999_962_528, 1_000_000_000)
    assert certificate.budget == F(10_999_479_944, 1_000_000_000)
    assert len(certificate.atoms) == 496
    assert len(certificate.threshold_atoms) == 2_220
    assert premises.rows == 12_028
    assert premises.minimum_containment_numerator == F(1, 1_000_000_000_000)

    data = ThresholdAtomData.of(certificate, batch_size=BATCH // 2)
    assert len(data.sites.xlo) > MAX_INTERVAL_ATOMS
    assert len(data.sites.xlo) <= MAX_BATCH_SITES
    assert data.members.size > MAX_MEMBER_SLOTS
    assert data.members.size <= MAX_BATCH_MEMBER_SLOTS


def test_source_import_rejects_a_different_container(tmp_path: Path) -> None:
    text = SOURCE.read_text(encoding="utf-8")
    assert text.count('"L": "191/50"') == 1
    altered = tmp_path / "global-certificate.json"
    altered.write_text(text.replace('"L": "191/50"', '"L": "383/100"'), encoding="utf-8")

    with pytest.raises(ValueError, match="not the n11 source container"):
        load_kleddamag_parent_core(altered)


def test_source_import_binds_the_exact_reviewed_bytes(tmp_path: Path) -> None:
    data = SOURCE.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert load_kleddamag_parent_core(SOURCE, expected_sha256=digest).n == 11

    altered = tmp_path / "global-certificate.json"
    altered.write_bytes(data.replace(b'"L": "191/50"', b'"L":  "191/50"', 1))
    with pytest.raises(ValueError, match="bytes differ from the reviewed n11 release"):
        load_kleddamag_parent_core(altered, expected_sha256=digest)


def test_source_import_refuses_duplicate_keys_and_inexact_fields(tmp_path: Path) -> None:
    text = SOURCE.read_text(encoding="utf-8")
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text(
        text.replace('"L": "191/50",', '"L": "191/50", "L": "191/50",', 1),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate JSON key L"):
        load_kleddamag_parent_core(duplicate)

    inexact = tmp_path / "inexact.json"
    inexact.write_text(text.replace('"L": "191/50"', '"L": 3.82', 1), encoding="utf-8")
    with pytest.raises(ValueError, match="exact rational string"):
        load_kleddamag_parent_core(inexact)


@pytest.mark.parametrize("batch_size", [True, 0, BATCH + 1])
def test_batch_size_refuses_values_outside_the_existing_ceiling(
    batch_size: object,
) -> None:
    with pytest.raises(IntervalInputError, match="batch size"):
        ThresholdAtomData.of(_certificate(), batch_size=batch_size)  # type: ignore[arg-type]


def test_smaller_batches_trade_width_without_raising_the_site_byte_cap() -> None:
    points = tuple((F(index, 10_000), F(0)) for index in range(BATCH + 2))
    atoms = tuple(
        ThresholdAtom(part, 1, F(0))
        for part in (points[: BATCH // 2 + 1], points[BATCH // 2 + 1 :])
    )
    certificate = _certificate(threshold_atoms=atoms)

    with pytest.raises(IntervalInputError, match="distinct sites"):
        ThresholdAtomData.of(certificate)

    data = ThresholdAtomData.of(certificate, batch_size=BATCH // 2)
    assert len(data.sites.xlo) == BATCH + 2
    assert data.batch_size == BATCH // 2
    assert len(data.sites.xlo) * data.batch_size <= BATCH * BATCH


def test_smaller_batches_trade_width_without_raising_the_member_byte_cap() -> None:
    wide = ThresholdAtom(((F(0), F(0)),), 1, F(0), multiplicities=(3_000,))
    certificate = _certificate(threshold_atoms=(wide, wide, wide))

    with pytest.raises(IntervalInputError, match="member table"):
        ThresholdAtomData.of(certificate)

    data = ThresholdAtomData.of(certificate, batch_size=BATCH // 2)
    assert data.members.shape == (3, 3_000)
    assert data.members.size * data.batch_size <= 2 * BATCH * BATCH


def test_one_box_request_cannot_raise_the_absolute_site_cap() -> None:
    points = tuple(
        (F(index, MAX_BATCH_SITES + 2), F(0)) for index in range(MAX_BATCH_SITES + 1)
    )
    width = (MAX_BATCH_SITES + 2) // 3
    atoms = tuple(
        ThresholdAtom(points[start : start + width], 1, F(0))
        for start in range(0, len(points), width)
    )
    with pytest.raises(IntervalInputError, match="distinct sites"):
        ThresholdAtomData.of(_certificate(threshold_atoms=atoms), batch_size=1)


def test_one_box_request_cannot_raise_the_absolute_member_cap() -> None:
    wide = ThresholdAtom(
        ((F(0), F(0)),),
        1,
        F(0),
        multiplicities=(MAX_TOKENS_PER_ATOM,),
    )
    count = MAX_BATCH_MEMBER_SLOTS // MAX_TOKENS_PER_ATOM + 1
    with pytest.raises(IntervalInputError, match="member table"):
        ThresholdAtomData.of(_certificate(threshold_atoms=(wide,) * count), batch_size=1)
