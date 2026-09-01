"""Run the preregistered exact comparison for the retained n = 17 certificate.

Importing this module does not parse the retained fixture or perform a measurement.
The target comparison begins only when :func:`main` is called explicitly.
"""

from __future__ import annotations

import argparse
import hashlib
from collections.abc import Callable
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path

from cases.n17_weighted_certificate.fixture import (
    RETAINED_SHA256,
    RetainedFixture,
    load_retained_fixture,
)
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
from cases.n17_weighted_certificate.selftest import selftest_json
from cases.n17_weighted_certificate.source_faithful import (
    accumulate_source_faithful,
)
from cases.n17_weighted_certificate.target_independent import (
    accumulate_target_independent,
)

CLEAN_ROOM_PATH = Path(__file__).with_name("independent.py")
CLEAN_ROOM_SHA256 = "55d36239f1f7e860f059030d87f655d2ac0c82685d788b599a7dd23d33d18de0"
EXPERIMENT_ID = "exp-049"
HYPOTHESIS_ID = "H-052"

Accumulator = Callable[[tuple[Atom, ...], Direction, Fraction, Fraction], DirectionManifest]


class ReadinessError(RuntimeError):
    """A frozen provenance or exact-agreement guard failed."""


def _verify_clean_room_hash() -> None:
    actual = hashlib.sha256(CLEAN_ROOM_PATH.read_bytes()).hexdigest()
    if actual != CLEAN_ROOM_SHA256:
        raise ReadinessError(
            f"clean-room hash mismatch: expected {CLEAN_ROOM_SHA256}, got {actual}"
        )


def _normalized_atoms(fixture: RetainedFixture) -> tuple[Atom, ...]:
    scale = Fraction(fixture.weight_scale)
    return tuple(
        Atom(atom.label, atom.x, atom.y, atom.weight / scale) for atom in fixture.atoms
    )


def _accumulate(
    fixture: RetainedFixture,
    atoms: tuple[Atom, ...],
    accumulator: Accumulator,
) -> CertificateManifest:
    rows = tuple(
        accumulator(atoms, direction, fixture.outer_side, fixture.square_side)
        for direction in fixture.directions
    )
    return CertificateManifest(
        atom_count=len(atoms),
        atom_hash=canonical_hash(atoms),
        total_weight=sum((atom.weight for atom in atoms), start=Fraction(0)),
        direction_count=len(fixture.directions),
        direction_hash=canonical_hash(fixture.directions),
        rows=rows,
        global_minimum=min(row.minimum for row in rows),
    )


def _preconditions(fixture: RetainedFixture) -> tuple[dict[str, object], bool]:
    direction_unit = tuple(
        direction.ux * direction.ux + direction.uy * direction.uy == 1
        for direction in fixture.directions
    )
    tangent_step = fixture.angle_limit / fixture.direction_steps
    adjacent_half_gap_bounds = tuple(
        tangent_step
        / (
            1
            + (fixture.angle_limit * index / fixture.direction_steps)
            * (fixture.angle_limit * (index + 1) / fixture.direction_steps)
        )
        <= tangent_step
        for index in range(fixture.direction_steps)
    )
    internal_side = fixture.outer_side - fixture.shrink_margin
    side_decomposition = scaling_preconditions(
        outer_side=fixture.outer_side,
        internal_side=internal_side,
        shrink_margin=fixture.shrink_margin,
    )
    final_pair_brackets = (
        fixture.directions[-2].uy < fixture.directions[-2].ux
        and fixture.directions[-1].uy >= fixture.directions[-1].ux
    )
    containment_left_operand = fixture.square_side * (1 + tangent_step)
    values: dict[str, object] = {
        "direction_unit": direction_unit,
        "final_pair_brackets_quarter_turn": final_pair_brackets,
        "adjacent_half_gap_bounds": adjacent_half_gap_bounds,
        "angle_error_bound": tangent_step,
        "containment_left_operand": containment_left_operand,
        "containment_right_operand": Fraction(1),
        "containment_strict": containment_left_operand < 1,
        "side_decomposition_operands": {
            "outer_side": fixture.outer_side,
            "internal_side": internal_side,
            "shrink_margin": fixture.shrink_margin,
        },
        "side_decomposition": side_decomposition,
    }
    passed = (
        all(direction_unit)
        and final_pair_brackets
        and all(adjacent_half_gap_bounds)
        and containment_left_operand < 1
        and all(side_decomposition)
    )
    return values, passed


def _mutation_guards(fixture: RetainedFixture, atoms: tuple[Atom, ...]) -> dict[str, bool]:
    first = atoms[0]
    removed = atoms[1:]
    reweighted = (
        Atom(first.label, first.x, first.y, first.weight + Fraction(1, 576)),
        *atoms[1:],
    )
    shortened_directions = fixture.directions[:-1]
    boundary_fixture = Fixture(
        atoms=(Atom("upper", Fraction(1), Fraction(1, 2), Fraction(1)),),
        directions=(Direction("axis", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),),
        window_side=Fraction(1),
        domain=TranslationDomain(Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
    )
    correct_internal = fixture.outer_side - fixture.shrink_margin
    defective_internal = Fraction(7909, 2000)
    return {
        "atom_mutation_rejected": (
            len(removed) != len(atoms) and canonical_hash(removed) != canonical_hash(atoms)
        ),
        "weight_mutation_rejected": (
            sum((atom.weight for atom in reweighted), start=Fraction(0))
            != sum((atom.weight for atom in atoms), start=Fraction(0))
            and canonical_hash(reweighted) != canonical_hash(atoms)
        ),
        "direction_cell_mutation_rejected": (
            len(shortened_directions) != len(fixture.directions)
            and canonical_hash(shortened_directions) != canonical_hash(fixture.directions)
        ),
        "event_boundary_mutation_rejected": (
            accumulate_fixture(boundary_fixture).global_minimum == 1
            and accumulate_fixture(boundary_fixture, upper_inclusive=False).global_minimum == 0
        ),
        "scaling_mutation_rejected": (
            scaling_preconditions(
                outer_side=fixture.outer_side,
                internal_side=correct_internal,
                shrink_margin=fixture.shrink_margin,
            )
            == (True, True, True)
            and scaling_preconditions(
                outer_side=fixture.outer_side,
                internal_side=defective_internal,
                shrink_margin=fixture.shrink_margin,
            )
            != (True, True, True)
        ),
    }


def _first_disagreement(
    source: CertificateManifest, independent: CertificateManifest
) -> dict[str, object] | None:
    for index, (source_row, independent_row) in enumerate(
        zip(source.rows, independent.rows, strict=True)
    ):
        if source_row != independent_row:
            return {
                "row_index": index,
                "direction_label": source_row.label,
                "source_faithful": asdict(source_row),
                "independent": asdict(independent_row),
            }
    if source != independent:
        return {
            "row_index": None,
            "direction_label": None,
            "source_faithful_aggregate": {
                "atom_count": source.atom_count,
                "atom_hash": source.atom_hash,
                "total_weight": source.total_weight,
                "direction_count": source.direction_count,
                "direction_hash": source.direction_hash,
                "global_minimum": source.global_minimum,
            },
            "independent_aggregate": {
                "atom_count": independent.atom_count,
                "atom_hash": independent.atom_hash,
                "total_weight": independent.total_weight,
                "direction_count": independent.direction_count,
                "direction_hash": independent.direction_hash,
                "global_minimum": independent.global_minimum,
            },
        }
    return None


def build_target_record() -> dict[str, object]:
    """Perform the authorized target comparison and return its canonical record."""

    _verify_clean_room_hash()
    fixture = load_retained_fixture()
    atoms = _normalized_atoms(fixture)
    source = _accumulate(fixture, atoms, accumulate_source_faithful)
    independent = _accumulate(fixture, atoms, accumulate_target_independent)
    preconditions, all_preconditions = _preconditions(fixture)
    agreement = source == independent
    mutation_guards = _mutation_guards(fixture, atoms)
    frozen_values = (
        source.atom_count == 168
        and source.direction_count == 181
        and source.total_weight == Fraction(9744, 576)
        and source.global_minimum == Fraction(576, 576)
    )
    all_mutations_rejected = all(mutation_guards.values())
    instrument_valid = all_preconditions and frozen_values and all_mutations_rejected
    decision = (
        "accepted"
        if instrument_valid and agreement
        else "rejected"
        if instrument_valid
        else "unresolved-invalid-instrument"
    )
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "fixture": {
            "retained_sha256": RETAINED_SHA256,
            "clean_room_sha256": CLEAN_ROOM_SHA256,
            "grid_size": fixture.grid_size,
            "weight_scale": fixture.weight_scale,
            "outer_side": fixture.outer_side,
            "square_side": fixture.square_side,
            "shrink_margin": fixture.shrink_margin,
            "angle_limit": fixture.angle_limit,
            "direction_steps": fixture.direction_steps,
        },
        "preconditions": preconditions,
        "source_faithful": asdict(source),
        "independent": asdict(independent),
        "exact_manifest_agreement": agreement,
        "first_disagreement": _first_disagreement(source, independent),
        "frozen_invariants_pass": frozen_values,
        "mutation_guards": mutation_guards,
        "all_mutations_rejected": all_mutations_rejected,
        "instrument_valid": instrument_valid,
        "decision": decision,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--record", type=Path)
    action.add_argument("--selftest", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.selftest:
        print(selftest_json())
        return 0
    if args.record is None:
        raise ReadinessError("--record is required for target measurement")
    record = build_target_record()
    args.record.parent.mkdir(parents=True, exist_ok=True)
    args.record.write_text(canonical_json(record) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
