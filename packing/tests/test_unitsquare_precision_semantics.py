"""Named controls for the exp-057 n = 68 side-semantics binding."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from cases.unitsquare_precision.production.adapter import (
    REPORTED_SIDE_TOKEN,
    production_model_factory,
)
from cases.unitsquare_precision.production.bound_run import (
    EXP057_RESULT_PATH,
    SELFTEST_SIDE_TOKEN,
    ProductionGuardError,
    bound_literal_dependencies,
    bound_model_factory,
    bound_production_dependencies,
    run_bound_literal,
)
from cases.unitsquare_precision.production.run import (
    PARENT_SHA256,
    PARENT_URL,
    run_literal,
)
from cases.unitsquare_precision.production.semantics import (
    MODEL_DIRECTIONS,
    MODEL_ORDER,
    QUARTER_GAIN,
    RELEASED_GAIN,
    SIX_DECIMAL_QUANTUM,
    DirectionError,
    QuantumError,
    ReleasedGainError,
    SideBinding,
    SideSemanticsError,
    ThresholdError,
    UnboundTokenError,
    UnknownModelError,
    bind_all_sides,
    bind_side,
    semantics_document,
)
from cases.unitsquare_precision.production.verify import verify_result_bytes

_EXACT_SIDE = Fraction(880345993651653, 100_000_000_000_000)
_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 4">
<rect id="container" width="4" height="4"/>
<g transform="translate(1,1)">
<polygon id="b"
 points="0.000000,0.000000 1.000000,0.000000 1.000000,1.000000 0.000000,1.000000"/>
</g></svg>"""


def _first_cell(model: str) -> list[str]:
    evaluation = production_model_factory(expected_polygon_count=1, side=Fraction(4))(model)(
        memoryview(_SVG), "b"
    )
    assert evaluation.outcome == "compatible"
    assert evaluation.proof is not None
    witness = cast(dict[str, object], evaluation.proof["proof"])["witness"]
    cells = cast(list[dict[str, list[str]]], cast(dict[str, object], witness)["source_cells"])
    return cells[0]["x"]


def test_declared_literal_side_is_the_exact_decimal_rational() -> None:
    binding = bind_side("declared:svg-literal")
    assert REPORTED_SIDE_TOKEN == "8.80345993651653"
    assert binding.lower == binding.upper == binding.scalar == _EXACT_SIDE
    assert binding.scalar.numerator == 880345993651653
    assert binding.scalar.denominator == 100_000_000_000_000
    assert binding.width == 0
    assert binding.direction == "exact"


def test_six_decimal_models_keep_their_declared_intervals() -> None:
    quantum = SIX_DECIMAL_QUANTUM
    nearest = bind_side("nearest-6")
    assert nearest.direction == "symmetric"
    assert nearest.lower == _EXACT_SIDE - quantum / 2
    assert nearest.upper == _EXACT_SIDE + quantum / 2
    assert nearest.width == quantum

    truncate = bind_side("truncate-6")
    assert truncate.direction == "away-from-zero"
    assert truncate.lower == _EXACT_SIDE
    assert truncate.upper == _EXACT_SIDE + quantum
    assert truncate.width == quantum


def test_declared_directions_match_the_adapter_coordinate_rule() -> None:
    """The binding restates the interval rule the frozen adapter already applies."""

    assert _first_cell("declared:svg-literal") == ["1", "1"]
    assert _first_cell("nearest-6") == ["1999999/2000000", "2000001/2000000"]
    assert _first_cell("truncate-6") == ["1", "1000001/1000000"]
    for model, cell in (
        ("nearest-6", _first_cell("nearest-6")),
        ("truncate-6", _first_cell("truncate-6")),
    ):
        width = Fraction(cell[1]) - Fraction(cell[0])
        assert width == SIX_DECIMAL_QUANTUM
        assert bind_side(model).width == width
        assert bind_side(model).direction == MODEL_DIRECTIONS[model]


def test_every_threshold_is_at_most_one_quarter_of_the_released_gain() -> None:
    assert Fraction("7.68618004216131e-5") == RELEASED_GAIN
    assert QUARTER_GAIN == RELEASED_GAIN / 4
    for binding in bind_all_sides():
        assert binding.width <= QUARTER_GAIN
        assert (binding.upper - binding.scalar) <= QUARTER_GAIN
        assert (binding.scalar - binding.lower) <= QUARTER_GAIN
    assert SIX_DECIMAL_QUANTUM <= QUARTER_GAIN


def test_the_admitted_scalar_lies_inside_every_declared_interval() -> None:
    for binding in bind_all_sides():
        assert binding.lower <= binding.scalar <= binding.upper
        assert binding.scalar == _EXACT_SIDE


def test_model_order_is_the_frozen_x011_order() -> None:
    assert MODEL_ORDER == ("declared:svg-literal", "nearest-6", "truncate-6")
    document = semantics_document()
    assert document["model_order"] == list(MODEL_ORDER)
    bindings = cast(list[dict[str, str]], document["bindings"])
    assert [row["model"] for row in bindings] == list(MODEL_ORDER)


def test_unbound_token_mutation_refuses_before_any_factory_exists() -> None:
    with pytest.raises(UnboundTokenError, match="unbound"):
        bind_side("declared:svg-literal", token=None)
    with pytest.raises(UnboundTokenError, match="unbound"):
        bind_side("nearest-6", token="   ")
    with pytest.raises(UnboundTokenError):
        bound_model_factory(expected_polygon_count=68, token=None)


@pytest.mark.parametrize(
    "token",
    ["8.80345993651653e0", "8.8034 5993", "eight", "1/2", "", "-8.80345993651653", "0.000000"],
)
def test_malformed_or_nonpositive_token_mutation(token: str) -> None:
    with pytest.raises(SideSemanticsError):
        bind_side("declared:svg-literal", token=token)


def test_wrong_direction_mutation() -> None:
    with pytest.raises(DirectionError, match="away-from-zero"):
        bind_side("truncate-6", direction="symmetric")
    with pytest.raises(DirectionError, match="symmetric"):
        bind_side("nearest-6", direction="away-from-zero")
    with pytest.raises(DirectionError, match="exact"):
        bind_side("declared:svg-literal", direction="symmetric")
    assert bind_side("truncate-6", direction="away-from-zero").width == SIX_DECIMAL_QUANTUM


def test_wrong_quantum_mutation() -> None:
    with pytest.raises(QuantumError, match="frozen six-decimal quantum"):
        bind_side("nearest-6", quantum=Fraction(1, 10_000_000))
    with pytest.raises(QuantumError, match="frozen six-decimal quantum"):
        bind_side("truncate-6", quantum=Fraction(1, 100_000))
    with pytest.raises(QuantumError, match="positive"):
        bind_side("nearest-6", quantum=Fraction(0))


def test_threshold_exceeding_a_quarter_gain_mutation() -> None:
    with pytest.raises(ThresholdError, match="one quarter"):
        bind_side("nearest-6", quantum=Fraction(1, 1_000))
    with pytest.raises(ThresholdError, match="one quarter"):
        bind_side("truncate-6", quantum=RELEASED_GAIN)


def test_changed_released_gain_mutation() -> None:
    with pytest.raises(ReleasedGainError, match="frozen"):
        bind_side("nearest-6", released_gain=RELEASED_GAIN * 2)
    with pytest.raises(ReleasedGainError, match="frozen"):
        bind_side("declared:svg-literal", released_gain=Fraction("6.54811e-6"))


def test_unknown_model_mutation() -> None:
    with pytest.raises(UnknownModelError, match="unknown declared model"):
        bind_side("nearest-7")
    with pytest.raises(UnknownModelError, match="unknown declared model"):
        bind_side("declared:svg-literal-2")
    factory = bound_model_factory(expected_polygon_count=1, token=SELFTEST_SIDE_TOKEN)
    with pytest.raises(UnknownModelError):
        factory("truncate-7")


def test_scalar_outside_the_declared_interval_refuses() -> None:
    binding = bind_side("nearest-6")
    with pytest.raises(SideSemanticsError, match="outside its declared interval"):
        SideBinding(
            binding.model,
            binding.lower,
            binding.upper,
            binding.upper + 1,
            binding.direction,
            binding.quantum,
        )
    with pytest.raises(SideSemanticsError, match="empty"):
        SideBinding(
            binding.model,
            binding.upper,
            binding.lower,
            binding.scalar,
            binding.direction,
            binding.quantum,
        )
    with pytest.raises(SideSemanticsError, match="positive"):
        SideBinding(
            binding.model,
            Fraction(-1),
            Fraction(1),
            Fraction(0),
            binding.direction,
            binding.quantum,
        )


def test_bound_side_replaces_the_three_typed_serialization_refusals() -> None:
    unbound = production_model_factory(expected_polygon_count=1, side=None)
    assert [unbound(model)(memoryview(_SVG), "b").reason for model in MODEL_ORDER] == [
        "serialization-refusal"
    ] * 3

    factory = bound_model_factory(expected_polygon_count=1, token=SELFTEST_SIDE_TOKEN)
    assert [factory(model)(memoryview(_SVG), "b").outcome for model in MODEL_ORDER] == [
        "compatible"
    ] * 3


def test_bound_production_dependencies_refuses_an_unfrozen_parent_contract(
    tmp_path: Path,
) -> None:
    synthetic = bound_literal_dependencies(tmp_path)
    with pytest.raises(ProductionGuardError, match="frozen n=68 parent"):
        bound_production_dependencies(
            contract=synthetic.contract,
            authorization=synthetic.authorization,
            output_root=tmp_path,
        )

    frozen = bound_production_dependencies(
        contract=replace(
            synthetic.contract,
            parent_url=PARENT_URL,
            parent_sha256=PARENT_SHA256,
        ),
        authorization=synthetic.authorization,
        output_root=tmp_path,
    )
    polygons = "".join(
        f'<polygon id="p{index:03d}" points="0,0 1,0 1,1 0,1"/>' for index in range(68)
    )
    scene = f'<svg viewBox="0 0 4 4">{polygons}</svg>'.encode()
    assert len(frozen.structural_scan(memoryview(scene))) == 68
    evaluation = frozen.model_factory("declared:svg-literal")(memoryview(scene), "p000")
    assert evaluation.reason != "serialization-refusal"


def test_bound_literal_command_publishes_only_below_a_temporary_root(
    tmp_path: Path,
) -> None:
    dependencies = bound_literal_dependencies(tmp_path)
    target = tmp_path / EXP057_RESULT_PATH
    target.parent.mkdir(parents=True)
    document = run_literal(["--record", EXP057_RESULT_PATH], dependencies)
    content = target.read_bytes()
    assert verify_result_bytes(content, dependencies.contract) == document
    models = cast(list[dict[str, object]], document["models"])
    assert [row["outcome"] for row in models] == ["compatible"] * 3
    assert not Path(EXP057_RESULT_PATH).exists()


def test_bound_record_mode_refuses_a_foreign_result_path() -> None:
    with pytest.raises(ProductionGuardError, match="result path must be exactly"):
        run_bound_literal("wrong.json")
    with pytest.raises(ProductionGuardError, match="result path must be exactly"):
        run_bound_literal(
            "campaign/series/series-000-smoke-and-calibration/results/"
            "exp-054-h-058-n68-one-parent-production-serialization.json"
        )


def test_bound_selftest_fires_every_named_guard() -> None:
    receipt = run_bound_literal(EXP057_RESULT_PATH)
    assert receipt["guards"] == [
        "unbound-token",
        "malformed-token",
        "unknown-model",
        "wrong-direction",
        "wrong-quantum",
        "threshold-exceeds-quarter-gain",
        "changed-released-gain",
        "scalar-outside-declared-interval",
        "unbound-side-refuses-every-model",
        "bound-side-admits-geometry",
        "unfrozen-parent-contract",
        "frozen-contract-side-is-bound",
        "wrong-result-path-before-open",
    ]
    assert receipt["outcomes"] == ["compatible"] * 3
    semantics = cast(dict[str, object], receipt["semantics"])
    assert semantics["reported_side_token"] == REPORTED_SIDE_TOKEN
    assert semantics["released_improvement"] == str(RELEASED_GAIN)
    assert not Path(EXP057_RESULT_PATH).exists()


def test_bound_receipt_is_identical_under_normal_and_optimized_python() -> None:
    command = [
        sys.executable,
        "-m",
        "cases.unitsquare_precision.production.bound_run",
        "--record",
        EXP057_RESULT_PATH,
    ]
    normal = subprocess.run(command, check=False, capture_output=True)
    optimized = subprocess.run(
        [sys.executable, "-O", *command[1:]], check=False, capture_output=True
    )
    assert normal.returncode == optimized.returncode == 0
    assert normal.stdout == optimized.stdout
    assert hashlib.sha256(normal.stdout).hexdigest() == (
        hashlib.sha256(optimized.stdout).hexdigest()
    )
    receipt = json.loads(normal.stdout)
    assert receipt["format"] == "UnitSquareBoundSideSelftest/v1"
    assert receipt["argv"] == ["--record", EXP057_RESULT_PATH]
    assert not Path(EXP057_RESULT_PATH).exists()


def test_selftest_flag_and_record_flag_agree_except_on_argv() -> None:
    command = [sys.executable, "-m", "cases.unitsquare_precision.production.bound_run"]
    flagged = subprocess.run([*command, "--selftest"], check=False, capture_output=True)
    recorded = subprocess.run(
        [*command, "--record", EXP057_RESULT_PATH], check=False, capture_output=True
    )
    assert flagged.returncode == recorded.returncode == 0
    assert json.loads(flagged.stdout) == json.loads(recorded.stdout)

    missing = subprocess.run(command, check=False, capture_output=True)
    assert missing.returncode == 2
    assert b"--record or --selftest" in missing.stderr
