from __future__ import annotations

import ast
import hashlib
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from cases.n17_weighted_certificate.extract import (
    StaticExtractionError,
    literal_assignments,
)
from cases.n17_weighted_certificate.fixture import load_retained_fixture
from cases.n17_weighted_certificate.independent import accumulate_fixture
from cases.n17_weighted_certificate.model import (
    Atom,
    Direction,
    Fixture,
    TranslationDomain,
    canonical_hash,
    canonical_json,
    scaling_preconditions,
)
from cases.n17_weighted_certificate.run import CLEAN_ROOM_SHA256, build_parser
from cases.n17_weighted_certificate.selftest import run_selftest
from cases.n17_weighted_certificate.source_faithful import accumulate_source_faithful
from cases.n17_weighted_certificate.target_independent import (
    accumulate_target_independent,
)


def synthetic_fixture() -> Fixture:
    atoms = tuple(
        Atom(f"a{index}", Fraction(x, 2), Fraction(y, 2), Fraction(1))
        for index, (x, y) in enumerate(((1, 1), (1, 3), (3, 1), (3, 3)))
    )
    directions = (
        Direction("axis", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),
        Direction("swapped", Fraction(0), Fraction(1), Fraction(1), Fraction(0)),
    )
    return Fixture(
        atoms=atoms,
        directions=directions,
        window_side=Fraction(1),
        domain=TranslationDomain(Fraction(0), Fraction(1), Fraction(0), Fraction(1)),
    )


def test_direct_cartesian_known_answer_and_stable_manifest() -> None:
    manifest = accumulate_fixture(synthetic_fixture())

    assert manifest.atom_count == 4
    assert manifest.total_weight == 4
    assert manifest.direction_count == 2
    assert manifest.global_minimum == 1
    assert [row.event_cell_count for row in manifest.rows] == [4, 4]
    assert [row.evaluated_state_count for row in manifest.rows] == [25, 25]
    assert [row.minimum for row in manifest.rows] == [1, 1]
    assert [row.witness for row in manifest.rows] == [(Fraction(0), Fraction(0))] * 2
    assert canonical_json(manifest).startswith('{"atom_count":4,')
    assert canonical_hash(manifest) == (
        "ef661b7e544fe8f199c73261ee7a2a179f835f1745dec6b35ab1a2833017427c"
    )


def test_atom_weight_and_direction_mutations_change_frozen_manifest() -> None:
    fixture = synthetic_fixture()
    control = accumulate_fixture(fixture)

    atom_mutation = Fixture(
        fixture.atoms[1:], fixture.directions, fixture.window_side, fixture.domain
    )
    weighted = list(fixture.atoms)
    first = weighted[0]
    weighted[0] = Atom(first.label, first.x, first.y, first.weight + Fraction(1, 576))
    weight_mutation = Fixture(
        tuple(weighted), fixture.directions, fixture.window_side, fixture.domain
    )
    direction_mutation = Fixture(
        fixture.atoms, fixture.directions[:-1], fixture.window_side, fixture.domain
    )

    assert accumulate_fixture(atom_mutation).atom_hash != control.atom_hash
    assert accumulate_fixture(weight_mutation).total_weight != control.total_weight
    assert accumulate_fixture(direction_mutation).direction_hash != control.direction_hash


def test_event_boundary_mutation_is_detected() -> None:
    fixture = Fixture(
        atoms=(Atom("upper", Fraction(1), Fraction(1, 2), Fraction(1)),),
        directions=(Direction("axis", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),),
        window_side=Fraction(1),
        domain=TranslationDomain(Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
    )

    assert accumulate_fixture(fixture).global_minimum == 1
    assert accumulate_fixture(fixture, upper_inclusive=False).global_minimum == 0


def test_scaling_mutation_is_detected_exactly() -> None:
    outer = Fraction(22529, 5000)
    internal = Fraction(5909, 2000)
    margin = Fraction(15513, 10000)

    assert scaling_preconditions(
        outer_side=outer, internal_side=internal, shrink_margin=margin
    ) == (True, True, True)
    assert scaling_preconditions(
        outer_side=outer,
        internal_side=Fraction(7909, 2000),
        shrink_margin=margin,
    ) == (True, True, False)


def test_static_extractor_checks_hash_and_never_executes(tmp_path: Path) -> None:
    source = tmp_path / "fixture.py"
    source.write_text(
        "from fractions import Fraction\n"
        "SIDE = Fraction(3, 2)\n"
        "ATOMS = [(0, 1, 2), (1, -2, 3)]\n"
        "raise RuntimeError('must never execute')\n"
    )
    digest = hashlib.sha256(source.read_bytes()).hexdigest()

    assert literal_assignments(source, digest, {"SIDE", "ATOMS"}) == {
        "SIDE": Fraction(3, 2),
        "ATOMS": [(0, 1, 2), (1, -2, 3)],
    }
    with pytest.raises(StaticExtractionError, match="source hash mismatch"):
        literal_assignments(source, "0" * 64, {"SIDE"})


def test_clean_room_ast_has_no_source_faithful_dependency() -> None:
    path = Path("cases/n17_weighted_certificate/independent.py")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "55d36239f1f7e860f059030d87f655d2ac0c82685d788b599a7dd23d33d18de0"
    )
    tree = ast.parse(path.read_text(), filename=str(path))
    imports = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}

    assert all("source_faithful" not in module for module in imports)
    assert "source_faithful" not in names
    assert "difference_array" not in names
    assert "prefix_sum" not in names


def test_retained_fixture_is_statically_reconstructed_without_target_execution() -> None:
    fixture = load_retained_fixture()

    assert fixture.outer_side == Fraction(22529, 5000)
    assert fixture.outer_side - fixture.shrink_margin == Fraction(5909, 2000)
    assert fixture.grid_size == 29
    assert len(fixture.atoms) == 168
    assert sum(atom.weight for atom in fixture.atoms) == 9744
    assert fixture.weight_scale == 576
    assert len(fixture.directions) == 181


def test_source_faithful_and_frozen_direct_paths_agree_on_synthetic_fixture() -> None:
    atoms = synthetic_fixture().atoms
    direction = synthetic_fixture().directions[0]

    source = accumulate_source_faithful(atoms, direction, Fraction(2), Fraction(1))
    independent = accumulate_target_independent(atoms, direction, Fraction(2), Fraction(1))

    assert source == independent
    assert source.minimum == 1


def test_preregistered_runner_is_import_safe_and_target_blind(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result = Path(
        "campaign/series/series-000-smoke-and-calibration/results/"
        "exp-049-h-052-n17-independent-certificate-agreement.json"
    )
    monkeypatch.setattr(sys, "argv", ["n17-certificate", "--record", str(result)])

    assert build_parser().parse_args().record == result
    assert not result.exists()
    assert (
        hashlib.sha256(
            Path("cases/n17_weighted_certificate/independent.py").read_bytes()
        ).hexdigest()
        == CLEAN_ROOM_SHA256
    )


def test_both_accumulation_paths_reject_synthetic_atom_and_weight_mutations() -> None:
    fixture = synthetic_fixture()
    direction = fixture.directions[0]
    control_source = accumulate_source_faithful(
        fixture.atoms, direction, Fraction(2), Fraction(1)
    )
    control_independent = accumulate_target_independent(
        fixture.atoms, direction, Fraction(2), Fraction(1)
    )
    removed = fixture.atoms[1:]
    first = fixture.atoms[0]
    reweighted = (
        Atom(first.label, first.x, first.y, first.weight + Fraction(1, 576)),
        *fixture.atoms[1:],
    )

    for accumulator, control in (
        (accumulate_source_faithful, control_source),
        (accumulate_target_independent, control_independent),
    ):
        assert accumulator(removed, direction, Fraction(2), Fraction(1)) != control
        assert accumulator(reweighted, direction, Fraction(2), Fraction(1)) != control


def test_production_selftest_has_named_source_defect_receipts() -> None:
    receipt = run_selftest()

    assert receipt["passed"] is True
    guards = receipt["receipts"]
    assert isinstance(guards, dict)
    denominator = guards["wrong-grid-denominator-source-defect"]
    endpoint = guards["omitted-final-endpoint-source-defect"]
    assert isinstance(denominator, dict)
    assert isinstance(endpoint, dict)
    assert denominator["passed"] is True
    assert endpoint["passed"] is True
