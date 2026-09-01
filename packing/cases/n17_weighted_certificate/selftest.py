"""Production readiness checks for the target-blind n = 17 instrument."""

from __future__ import annotations

import ast
import hashlib
from fractions import Fraction
from pathlib import Path

from cases.n17_weighted_certificate.independent import accumulate_fixture
from cases.n17_weighted_certificate.model import (
    Atom,
    CertificateManifest,
    Direction,
    DirectionManifest,
    Fixture,
    TranslationDomain,
    canonical_hash,
    canonical_json,
    scaling_preconditions,
)
from cases.n17_weighted_certificate.source_faithful import accumulate_source_faithful
from cases.n17_weighted_certificate.target_independent import (
    accumulate_target_independent,
)

CLEAN_ROOM_SHA256 = "55d36239f1f7e860f059030d87f655d2ac0c82685d788b599a7dd23d33d18de0"
CLEAN_ROOM_PATH = Path(__file__).with_name("independent.py")


class SelftestError(RuntimeError):
    """A production readiness guard failed."""


def _require(condition: bool, guard: str) -> None:  # noqa: FBT001
    if not condition:
        raise SelftestError(f"readiness guard failed: {guard}")


def _fixture(atoms: tuple[Atom, ...], directions: tuple[Direction, ...]) -> Fixture:
    return Fixture(
        atoms=atoms,
        directions=directions,
        window_side=Fraction(1),
        domain=TranslationDomain(Fraction(0), Fraction(1), Fraction(0), Fraction(1)),
    )


def _paired_manifests(
    fixture: Fixture, outer_side: Fraction
) -> tuple[CertificateManifest, CertificateManifest]:
    source_rows = tuple(
        accumulate_source_faithful(fixture.atoms, direction, outer_side, fixture.window_side)
        for direction in fixture.directions
    )
    independent_rows = tuple(
        accumulate_target_independent(fixture.atoms, direction, outer_side, fixture.window_side)
        for direction in fixture.directions
    )

    def manifest(rows: tuple[DirectionManifest, ...]) -> CertificateManifest:
        return CertificateManifest(
            atom_count=len(fixture.atoms),
            atom_hash=canonical_hash(fixture.atoms),
            total_weight=sum((atom.weight for atom in fixture.atoms), start=Fraction(0)),
            direction_count=len(fixture.directions),
            direction_hash=canonical_hash(fixture.directions),
            rows=rows,
            global_minimum=min(row.minimum for row in rows),
        )

    return manifest(source_rows), manifest(independent_rows)


def _base_fixture() -> Fixture:
    atoms = tuple(
        Atom(f"a{index}", Fraction(x, 2), Fraction(y, 2), Fraction(1))
        for index, (x, y) in enumerate(((1, 1), (1, 3), (3, 1), (3, 3)))
    )
    directions = (
        Direction("axis", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),
        Direction("swapped", Fraction(0), Fraction(1), Fraction(1), Fraction(0)),
    )
    return _fixture(atoms, directions)


def _wrong_denominator_receipt() -> dict[str, object]:
    outer_side = Fraction(3)
    margin = Fraction(1)
    intervals = 28
    correct_step = (outer_side - margin) / intervals
    wrong_step = (outer_side - margin) / (intervals + 1)
    correct_atoms = tuple(
        Atom(
            f"grid-{index}",
            margin / 2 + correct_step * index,
            Fraction(3, 2),
            Fraction(1),
        )
        for index in range(intervals + 1)
    )
    wrong_atoms = tuple(
        Atom(
            f"grid-{index}",
            margin / 2 + wrong_step * index,
            Fraction(3, 2),
            Fraction(1),
        )
        for index in range(intervals + 1)
    )
    directions = (Direction("axis", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),)
    correct_source, correct_independent = _paired_manifests(
        _fixture(correct_atoms, directions), outer_side
    )
    wrong_source, wrong_independent = _paired_manifests(
        _fixture(wrong_atoms, directions), outer_side
    )
    _require(correct_source == correct_independent, "wrong-denominator-control-agreement")
    _require(wrong_source == wrong_independent, "wrong-denominator-mutant-agreement")
    _require(
        correct_source.atom_hash != wrong_source.atom_hash,
        "wrong-denominator-atom-hash-rejection",
    )
    _require(
        correct_atoms[-1].x == outer_side - margin / 2,
        "correct-grid-final-endpoint",
    )
    _require(
        wrong_atoms[-1].x != outer_side - margin / 2,
        "wrong-denominator-final-endpoint-rejection",
    )
    return {
        "name": "wrong-grid-denominator-28-vs-29",
        "passed": True,
        "correct_atom_hash": correct_source.atom_hash,
        "mutant_atom_hash": wrong_source.atom_hash,
        "correct_final_coordinate": correct_atoms[-1].x,
        "mutant_final_coordinate": wrong_atoms[-1].x,
    }


def _omitted_endpoint_receipt() -> dict[str, object]:
    atoms = _base_fixture().atoms
    correct_directions = (
        Direction("k=0", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),
        Direction("k=1", Fraction(3, 5), Fraction(4, 5), Fraction(-4, 5), Fraction(3, 5)),
    )
    omitted_directions = correct_directions[:-1]
    correct_source, correct_independent = _paired_manifests(
        _fixture(atoms, correct_directions), Fraction(2)
    )
    omitted_source, omitted_independent = _paired_manifests(
        _fixture(atoms, omitted_directions), Fraction(2)
    )
    _require(correct_source == correct_independent, "endpoint-control-agreement")
    _require(omitted_source == omitted_independent, "omitted-endpoint-mutant-agreement")
    _require(
        correct_source.direction_count == 2 and omitted_source.direction_count == 1,
        "kmax-plus-one-count-rejection",
    )
    _require(
        correct_source.direction_hash != omitted_source.direction_hash,
        "omitted-endpoint-direction-hash-rejection",
    )
    _require(
        correct_directions[-1].uy >= correct_directions[-1].ux,
        "final-endpoint-brackets-quarter-turn",
    )
    _require(
        omitted_directions[-1].uy < omitted_directions[-1].ux,
        "omitted-endpoint-bracket-rejection",
    )
    return {
        "name": "omitted-kmax-final-endpoint",
        "passed": True,
        "control_direction_count": correct_source.direction_count,
        "mutant_direction_count": omitted_source.direction_count,
        "control_direction_hash": correct_source.direction_hash,
        "mutant_direction_hash": omitted_source.direction_hash,
    }


def run_selftest() -> dict[str, object]:
    """Run every readiness guard with explicit exceptions, including under ``-O``."""

    actual_hash = hashlib.sha256(CLEAN_ROOM_PATH.read_bytes()).hexdigest()
    _require(actual_hash == CLEAN_ROOM_SHA256, "clean-room-file-hash")
    tree = ast.parse(CLEAN_ROOM_PATH.read_text(encoding="utf-8"))
    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    _require(
        all("source_faithful" not in module for module in imported_modules),
        "clean-room-import-independence",
    )

    base = _base_fixture()
    direct = accumulate_fixture(base)
    _require(direct.global_minimum == 1, "direct-known-answer-minimum")
    _require(
        canonical_hash(direct)
        == "ef661b7e544fe8f199c73261ee7a2a179f835f1745dec6b35ab1a2833017427c",
        "direct-known-answer-manifest",
    )
    source, independent = _paired_manifests(base, Fraction(2))
    _require(source == independent, "source-independent-synthetic-agreement")

    first = base.atoms[0]
    atom_mutant = _fixture(base.atoms[1:], base.directions)
    weight_mutant = _fixture(
        (
            Atom(first.label, first.x, first.y, first.weight + Fraction(1, 576)),
            *base.atoms[1:],
        ),
        base.directions,
    )
    atom_source, atom_independent = _paired_manifests(atom_mutant, Fraction(2))
    weight_source, weight_independent = _paired_manifests(weight_mutant, Fraction(2))
    _require(atom_source == atom_independent, "atom-mutant-path-agreement")
    _require(weight_source == weight_independent, "weight-mutant-path-agreement")
    _require(atom_source.atom_hash != source.atom_hash, "atom-mutation-rejection")
    _require(weight_source.total_weight != source.total_weight, "weight-mutation-rejection")

    boundary = _fixture(
        (Atom("upper", Fraction(1), Fraction(1, 2), Fraction(1)),),
        (Direction("axis", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),),
    )
    boundary = Fixture(
        boundary.atoms,
        boundary.directions,
        boundary.window_side,
        TranslationDomain(Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
    )
    _require(accumulate_fixture(boundary).global_minimum == 1, "inclusive-boundary-control")
    _require(
        accumulate_fixture(boundary, upper_inclusive=False).global_minimum == 0,
        "exclusive-boundary-mutation-rejection",
    )
    _require(
        scaling_preconditions(
            outer_side=Fraction(22529, 5000),
            internal_side=Fraction(5909, 2000),
            shrink_margin=Fraction(15513, 10000),
        )
        == (True, True, True),
        "scaling-control",
    )
    _require(
        scaling_preconditions(
            outer_side=Fraction(22529, 5000),
            internal_side=Fraction(7909, 2000),
            shrink_margin=Fraction(15513, 10000),
        )
        != (True, True, True),
        "scaling-mutation-rejection",
    )

    wrong_denominator = _wrong_denominator_receipt()
    omitted_endpoint = _omitted_endpoint_receipt()
    receipts = {
        "atom-mutation": True,
        "canonical-serialization": True,
        "clean-room-hash": True,
        "clean-room-import-independence": True,
        "direction-cell-mutation": True,
        "event-boundary-mutation": True,
        "omitted-final-endpoint-source-defect": omitted_endpoint,
        "scaling-mutation": True,
        "source-independent-synthetic-agreement": True,
        "weight-mutation": True,
        "wrong-grid-denominator-source-defect": wrong_denominator,
    }
    return {
        "schema_version": 1,
        "selftest": "exp-049-w7-readiness",
        "passed": True,
        "clean_room_sha256": actual_hash,
        "receipts": receipts,
        "receipt_hash": canonical_hash(receipts),
    }


def selftest_json() -> str:
    return canonical_json(run_selftest())
