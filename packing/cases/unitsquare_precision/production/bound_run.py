"""Bound-side entry point composing the frozen UnitSquare production adapter.

This module adds no parser, no proof rule and no channel.  It composes the unchanged
exp-054 adapter, runner and whole-result verifier with the exp-057 side binding, so the
three declared models receive an exact or directional side instead of `None`.

At this stage the entry point runs only the literal target-blind path: a synthetic SVG
in memory, a temporary output root, no network and no target source.  The frozen-parent
constructor exists, but it delegates its URL and digest guard to the unchanged
`run.production_dependencies`, so it cannot bind anything but the declared parent, and
retrieval itself belongs to a separately routed block.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import tempfile
from collections.abc import Callable
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Final

from cases.unitsquare_precision.production.adapter import (
    REPORTED_SIDE_TOKEN,
    ProductionAdapterError,
    production_model_factory,
    structural_scanner,
)
from cases.unitsquare_precision.production.run import (
    PARENT_SHA256,
    PARENT_URL,
    ProductionDependencies,
    ProductionGuardError,
    production_dependencies,
    run_literal,
)
from cases.unitsquare_precision.production.semantics import (
    MODEL_ORDER,
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
    bind_side,
    semantics_document,
)
from cases.unitsquare_precision.production.verify import (
    ResultVerificationError,
    verify_result_bytes,
)
from cases.unitsquare_precision.refusal.run import (
    ModelFactory,
    RunnerAuthorization,
    RunnerContract,
    RunnerGuardError,
    RunnerModelEvaluator,
    canonical_runner_bytes,
)

EXP057_RESULT_PATH: Final = (
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-057-h-058-n68-one-parent-localization.json"
)
EXPECTED_PARENT_POLYGONS: Final = 68
SELFTEST_AUTHORIZATION: Final = RunnerAuthorization(
    "session-080", "2026-09-02T05:28:00Z", "2026-09-02T06:18:00Z"
)

_SYNTHETIC_URL: Final = "https://example.invalid/bound-synthetic-parent.svg"
_SYNTHETIC_SVG: Final = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 4">
<rect id="container" x="0" y="0" width="4" height="4"/>
<g transform="translate(1,1) scale(1)">
<polygon id="square-a"
 points="0.000000,0.000000 1.000000,0.000000 1.000000,1.000000 0.000000,1.000000"/>
</g></svg>"""
SELFTEST_SIDE_TOKEN: Final = "4.000000"
"""The synthetic container side, printed so all three declared models can read it."""


def bound_model_factory(
    *,
    expected_polygon_count: int,
    token: str | None,
) -> ModelFactory:
    """Bind every declared model's side up front, then compose the frozen factory.

    Every model is bound before any factory is returned, so an unbound, malformed or
    misdeclared token refuses here and can never reach the runner or an opener.
    """

    bindings: dict[str, SideBinding] = {
        model: bind_side(model, token=token, quantum=SIX_DECIMAL_QUANTUM)
        for model in MODEL_ORDER
    }

    def factory(model_name: str) -> RunnerModelEvaluator:
        binding = bindings.get(model_name)
        if binding is None:
            raise UnknownModelError(f"unknown declared model: {model_name}")
        inner = production_model_factory(
            expected_polygon_count=expected_polygon_count,
            side=binding.scalar,
        )
        return inner(model_name)

    return factory


def bound_production_dependencies(
    *,
    contract: RunnerContract,
    authorization: RunnerAuthorization,
    output_root: Path,
    token: str | None = REPORTED_SIDE_TOKEN,
) -> ProductionDependencies:
    """Bind the frozen parent contract to the adapter with the reported side bound.

    The URL and digest guard is `run.production_dependencies` itself, unchanged, so this
    constructor refuses exactly what that one refuses.  Constructing it performs no I/O;
    an authorized retrieval block supplies the authority to call the opener.
    """

    base = production_dependencies(
        contract=contract,
        authorization=authorization,
        output_root=output_root,
    )
    factory = bound_model_factory(
        expected_polygon_count=EXPECTED_PARENT_POLYGONS,
        token=token,
    )
    return replace(base, model_factory=factory)


def bound_literal_dependencies(root: Path) -> ProductionDependencies:
    """The exp-057 target-blind literal dependencies: synthetic bytes, bound side."""

    source_sha256 = hashlib.sha256(_SYNTHETIC_SVG).hexdigest()
    contract = RunnerContract(
        "exp-057",
        "session-080",
        EXP057_RESULT_PATH,
        SELFTEST_AUTHORIZATION,
        _SYNTHETIC_URL,
        source_sha256,
    )
    factory = bound_model_factory(
        expected_polygon_count=1,
        token=SELFTEST_SIDE_TOKEN,
    )
    return ProductionDependencies(
        contract,
        SELFTEST_AUTHORIZATION,
        lambda _url: io.BytesIO(_SYNTHETIC_SVG),
        structural_scanner(expected_polygon_count=1),
        factory,
        root,
    )


def _expect(
    label: str,
    expected: type[BaseException] | tuple[type[BaseException], ...],
    action: Callable[[], object],
    guards: list[str],
) -> None:
    try:
        action()
    except expected:
        guards.append(label)
        return
    raise ProductionGuardError(f"mutation did not fire its named guard: {label}")


def _synthetic_parent_scene() -> bytes:
    polygons = "".join(
        f'<polygon id="p{index:03d}" points="0,0 1,0 1,1 0,1"/>'
        for index in range(EXPECTED_PARENT_POLYGONS)
    )
    return f'<svg viewBox="0 0 4 4">{polygons}</svg>'.encode()


def _binding_guards() -> list[str]:
    """Fire every named binding mutation, in a fixed order."""

    guards: list[str] = []
    _expect(
        "unbound-token",
        UnboundTokenError,
        lambda: bind_side("declared:svg-literal", token=None),
        guards,
    )
    _expect(
        "malformed-token",
        SideSemanticsError,
        lambda: bind_side("declared:svg-literal", token="8.80345993651653e0"),
        guards,
    )
    _expect(
        "unknown-model",
        UnknownModelError,
        lambda: bind_side("nearest-7"),
        guards,
    )
    _expect(
        "wrong-direction",
        DirectionError,
        lambda: bind_side("truncate-6", direction="symmetric"),
        guards,
    )
    _expect(
        "wrong-quantum",
        QuantumError,
        lambda: bind_side("nearest-6", quantum=Fraction(1, 10_000_000)),
        guards,
    )
    _expect(
        "threshold-exceeds-quarter-gain",
        ThresholdError,
        lambda: bind_side("nearest-6", quantum=Fraction(1, 1_000)),
        guards,
    )
    _expect(
        "changed-released-gain",
        ReleasedGainError,
        lambda: bind_side("nearest-6", released_gain=RELEASED_GAIN * 2),
        guards,
    )
    literal = bind_side("declared:svg-literal")
    _expect(
        "scalar-outside-declared-interval",
        SideSemanticsError,
        lambda: SideBinding(
            literal.model,
            literal.lower,
            literal.upper,
            literal.scalar + 1,
            literal.direction,
            literal.quantum,
        ),
        guards,
    )
    return guards


def _composition_guards(dependencies: ProductionDependencies) -> list[str]:
    """Fire the guards that separate an unbound side from a bound one."""

    guards: list[str] = []
    unbound = production_model_factory(expected_polygon_count=1, side=None)
    unbound_outcomes = [
        unbound(model)(memoryview(_SYNTHETIC_SVG), "square-a").reason for model in MODEL_ORDER
    ]
    if unbound_outcomes != ["serialization-refusal"] * 3:
        raise ProductionGuardError("unbound side no longer refuses every declared model")
    guards.append("unbound-side-refuses-every-model")

    factory = bound_model_factory(expected_polygon_count=1, token=SELFTEST_SIDE_TOKEN)
    bound_outcomes = [
        factory(model)(memoryview(_SYNTHETIC_SVG), "square-a").outcome for model in MODEL_ORDER
    ]
    if "compatible" not in bound_outcomes:
        raise ProductionGuardError("bound side did not admit one geometry outcome")
    guards.append("bound-side-admits-geometry")

    _expect(
        "unfrozen-parent-contract",
        ProductionGuardError,
        lambda: bound_production_dependencies(
            contract=dependencies.contract,
            authorization=dependencies.authorization,
            output_root=dependencies.output_root,
        ),
        guards,
    )

    frozen_contract = replace(
        dependencies.contract,
        parent_url=PARENT_URL,
        parent_sha256=PARENT_SHA256,
    )
    frozen = bound_production_dependencies(
        contract=frozen_contract,
        authorization=dependencies.authorization,
        output_root=dependencies.output_root,
    )
    scene = memoryview(_synthetic_parent_scene())
    evaluation = frozen.model_factory("declared:svg-literal")(scene, "p000")
    if evaluation.reason == "serialization-refusal":
        raise ProductionGuardError("frozen-parent constructor still carries an unbound side")
    guards.append("frozen-contract-side-is-bound")
    return guards


def run_bound_literal(record_path: str) -> dict[str, object]:
    """Run the exact exp-057 argv over synthetic bytes under a temporary root."""

    if record_path != EXP057_RESULT_PATH:
        raise ProductionGuardError(f"result path must be exactly {EXP057_RESULT_PATH}")
    with tempfile.TemporaryDirectory(prefix="unitsquare-bound-") as directory:
        root = Path(directory)
        target = root / record_path
        target.parent.mkdir(parents=True)
        dependencies = bound_literal_dependencies(root)
        document = run_literal(["--record", record_path], dependencies)
        retained = target.read_bytes()
        if retained != canonical_runner_bytes(document) + b"\n":
            raise ProductionGuardError("bound literal command publication mismatch")
        verified = verify_result_bytes(retained, dependencies.contract)
        if verified != document:
            raise ProductionGuardError("whole-result verifier changed the bound result")
        if any(token in retained.lower() for token in (b"<svg", b"child", b"gain")):
            raise ProductionGuardError("bound literal command retained a forbidden channel")
        models = document.get("models")
        if not isinstance(models, list) or len(models) != 3:
            raise ProductionGuardError("bound command did not execute all three models")
        outcomes = [model.get("outcome") for model in models if isinstance(model, dict)]
        if "compatible" not in outcomes:
            raise ProductionGuardError("bound synthetic scene lacked a compatible model")

        guards = _binding_guards()
        guards.extend(_composition_guards(dependencies))
        opened: list[str] = []
        guarded = replace(
            dependencies,
            opener=lambda url: opened.append(url) or io.BytesIO(_SYNTHETIC_SVG),
        )
        _expect(
            "wrong-result-path-before-open",
            RunnerGuardError,
            lambda: run_literal(["--record", "wrong.json"], guarded),
            guards,
        )
        if opened:
            raise ProductionGuardError("wrong result path reached the opener")
        return {
            "format": "UnitSquareBoundSideSelftest/v1",
            "argv": ["--record", record_path],
            "result_sha256": hashlib.sha256(retained).hexdigest(),
            "models": document["model_order"],
            "outcomes": outcomes,
            "selection": document["selection"],
            "selftest_side_token": SELFTEST_SIDE_TOKEN,
            "semantics": semantics_document(),
            "publication": "whole-result-verified-before-atomic-create",
            "guards": guards,
        }


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record")
    parser.add_argument("--selftest", action="store_true")
    arguments = parser.parse_args(argv)
    record_path = arguments.record or (EXP057_RESULT_PATH if arguments.selftest else None)
    if record_path is None:
        print("one of --record or --selftest is required", file=sys.stderr)
        return 2
    try:
        receipt = run_bound_literal(record_path)
    except (
        ProductionAdapterError,
        ProductionGuardError,
        ResultVerificationError,
        RunnerGuardError,
        SideSemanticsError,
    ) as error:
        print(f"bound side selftest failed: {error}", file=sys.stderr)
        return 2
    sys.stdout.write(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
