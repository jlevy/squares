"""Synthetic controls for the UnitSquare provenance and rigid-pose bridge."""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
from dataclasses import replace
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import pytest

from cases.unitsquare_precision.refusal.run import (
    CoverLeaf,
    CoverSplit,
    ExactPose,
    PoseBox,
    ProofFormatError,
    RationalAffine,
    RationalInterval,
    RunnerAuthorization,
    RunnerContract,
    RunnerGuardError,
    RunnerModelEvaluation,
    SourceBinding,
    atomic_publish_new,
    build_exact_witness,
    canonical_proof_bytes,
    canonical_runner_bytes,
    exact_wall_signs,
    run_authorized_runner,
    run_exp051_runner,
    source_cells_sha256,
    synthetic_receipt,
    synthetic_source_cells,
    unit_corners,
)
from cases.unitsquare_precision.refusal.verify import verify_proof
from sqpack.research.unitsquare_precision import (
    RESULT_PATH,
    TARGET_PAIRS,
    ParentEvaluation,
    PrecisionBridgeError,
    TargetMeasurementGatedError,
    canonical_bytes,
    consume_verified_parent,
    fit_rigid_pose,
    parse_svg_scene,
    prepare_target_run,
    seal_first_parent_model,
    source_cell,
    verify_parent_bytes,
    verify_receipt,
)

SVG = b"""<svg xmlns="http://www.w3.org/2000/svg">
  <rect id="container" x="0" y="0" width="4" height="4"/>
  <g transform="translate(2 2)">
    <polygon id="square-b" points="-0.5,-0.5 0.5,-0.5 0.5,0.5 -0.5,0.5"/>
  </g>
  <polygon id="square-a" points="0.25,2.75 1.25,2.75 1.25,3.75 0.25,3.75"/>
</svg>"""


def _receipt(svg: bytes = SVG) -> dict[str, object]:
    scene = parse_svg_scene(svg, model="declared:svg-literal", side=Decimal(4))
    fits = tuple(fit_rigid_pose(square) for square in scene.squares)
    return scene.receipt(fits)


def test_ephemeral_adapter_hashes_before_parsing_and_retains_no_raw_bytes() -> None:
    digest = hashlib.sha256(SVG).hexdigest()
    seen: list[bytes] = []

    summary = verify_parent_bytes(
        SVG,
        expected_sha256=digest,
        consume=lambda payload: seen.append(payload) or {"length": len(payload)},
    )

    assert summary == {"length": len(SVG)}
    assert seen == [SVG]
    with pytest.raises(PrecisionBridgeError, match="digest mismatch"):
        verify_parent_bytes(
            SVG,
            expected_sha256="0" * 64,
            consume=lambda _payload: pytest.fail("unverified bytes reached parser"),
        )

    response = io.BytesIO(SVG)
    assert consume_verified_parent(
        "https://example.invalid/parent.svg",
        expected_sha256=digest,
        consume=lambda payload: {"digest": hashlib.sha256(payload).hexdigest()},
        opener=lambda _url: response,
    ) == {"digest": digest}
    assert response.closed


def test_frozen_target_driver_is_wired_but_gated_before_any_target_access() -> None:
    assert [pair.n for pair in TARGET_PAIRS] == [68, 69]
    assert [pair.child_path for pair in TARGET_PAIRS] == [
        "resources/web/known-best-packings/unitsquare/n068.svg",
        "resources/web/known-best-packings/unitsquare/n069.svg",
    ]
    with pytest.raises(TargetMeasurementGatedError, match="no child read or parent retrieval"):
        prepare_target_run(RESULT_PATH)


def test_parent_only_selector_seals_first_valid_model_without_child_channel() -> None:
    receipt = _receipt()
    sealed = seal_first_parent_model(
        68,
        (
            ParentEvaluation(
                "declared:svg-literal", compatible=False, valid=False, receipt=None
            ),
            ParentEvaluation("nearest-6", compatible=True, valid=True, receipt=receipt),
            ParentEvaluation("truncate-6", compatible=True, valid=True, receipt=receipt),
        ),
    )
    assert sealed is not None
    assert sealed.model == "nearest-6"
    assert sealed.receipt_sha256 == hashlib.sha256(canonical_bytes(receipt)).hexdigest()


@pytest.mark.parametrize(
    ("model", "literal", "expected"),
    [
        ("declared:svg-literal", "1.234567", ("1.234567", "1.234567")),
        ("nearest-6", "1.234567", ("1.2345665", "1.2345675")),
        ("truncate-6", "1.234567", ("1.234567", "1.234568")),
        ("truncate-6", "-1.234567", ("-1.234568", "-1.234567")),
    ],
)
def test_source_cell_models_are_closed_and_decimal_exact(
    model: str, literal: str, expected: tuple[str, str]
) -> None:
    cell = source_cell(literal, model)
    assert (str(cell.lower), str(cell.upper)) == expected


def test_nested_transform_order_normalization_and_rigid_fit() -> None:
    svg = b"""<svg xmlns="http://www.w3.org/2000/svg">
      <rect id="container" x="10" y="20" width="8" height="8"/>
      <g transform="translate(10 20)">
        <g transform="scale(2)">
          <polygon id="s" points="0,0 1,0 1,1 0,1"/>
        </g>
      </g>
    </svg>"""
    scene = parse_svg_scene(svg, model="declared:svg-literal", side=Decimal(4))
    square = scene.squares[0]

    assert [(point.x.midpoint, point.y.midpoint) for point in square.vertices] == [
        (Decimal(0), Decimal(4)),
        (Decimal(1), Decimal(4)),
        (Decimal(1), Decimal(3)),
        (Decimal(0), Decimal(3)),
    ]
    fit = fit_rigid_pose(square)
    assert fit.square_id == "s"
    assert fit.maximum_corner_residual <= Decimal("1e-12")


def test_rotated_wall_tangent_interior_and_tangent_pair_controls() -> None:
    rotated = b"""<svg xmlns="http://www.w3.org/2000/svg">
      <rect id="container" x="0" y="0" width="5" height="5"/>
      <polygon id="r" transform="translate(2.5 2.5) rotate(30)"
        points="-0.5,-0.5 0.5,-0.5 0.5,0.5 -0.5,0.5"/>
    </svg>"""
    rotated_scene = parse_svg_scene(rotated, model="declared:svg-literal", side=Decimal(5))
    rotated_receipt = rotated_scene.receipt((fit_rigid_pose(rotated_scene.squares[0]),))
    assert verify_receipt(rotated_receipt) == []

    tangent = b"""<svg xmlns="http://www.w3.org/2000/svg">
      <rect id="container" x="0" y="0" width="3" height="3"/>
      <polygon id="wall" points="0,2 1,2 1,3 0,3"/>
      <polygon id="interior" points="1,2 2,2 2,3 1,3"/>
    </svg>"""
    tangent_scene = parse_svg_scene(tangent, model="declared:svg-literal", side=Decimal(3))
    tangent_receipt = tangent_scene.receipt(
        tuple(fit_rigid_pose(square) for square in tangent_scene.squares)
    )
    assert verify_receipt(tangent_receipt) == []
    assert tangent_receipt["pairs"][0]["signed_separation"] == "0"  # type: ignore[index]


def test_cyclic_and_reversed_vertices_have_one_canonical_serialization() -> None:
    original = parse_svg_scene(SVG, model="declared:svg-literal", side=Decimal(4))
    cyclic = SVG.replace(
        b"0.25,2.75 1.25,2.75 1.25,3.75 0.25,3.75",
        b"1.25,3.75 0.25,3.75 0.25,2.75 1.25,2.75",
    )
    reversed_svg = SVG.replace(
        b"0.25,2.75 1.25,2.75 1.25,3.75 0.25,3.75",
        b"0.25,2.75 0.25,3.75 1.25,3.75 1.25,2.75",
    )

    documents = []
    for payload in (SVG, cyclic, reversed_svg):
        scene = parse_svg_scene(payload, model="declared:svg-literal", side=Decimal(4))
        documents.append(scene.receipt(tuple(fit_rigid_pose(s) for s in scene.squares)))
    assert canonical_bytes(documents[0]) == canonical_bytes(documents[1])
    assert canonical_bytes(documents[0]) == canonical_bytes(documents[2])
    assert canonical_bytes(original.receipt(tuple(fit_rigid_pose(s) for s in original.squares)))


def test_independent_verifier_accepts_control_and_rejects_wall_and_overlap_mutations() -> None:
    receipt = _receipt()
    assert verify_receipt(receipt) == []

    wall = json.loads(canonical_bytes(receipt))
    wall["squares"][0]["pose"]["center_x"] = "-0.6"
    assert any("source cell" in error or "wall" in error for error in verify_receipt(wall))

    overlap = json.loads(canonical_bytes(receipt))
    overlap["squares"][1]["pose"] = dict(overlap["squares"][0]["pose"])
    overlap["squares"][1]["source_cells"] = list(overlap["squares"][0]["source_cells"])
    assert any("overlap" in error for error in verify_receipt(overlap))


def test_every_named_parser_and_geometry_mutation_is_refused() -> None:
    duplicate = SVG.replace(b'id="square-b"', b'id="square-a"')
    with pytest.raises(PrecisionBridgeError, match="duplicate square id"):
        parse_svg_scene(duplicate, model="declared:svg-literal", side=Decimal(4))

    malformed = SVG.replace(b"1.25,3.75", b"1.28,3.75")
    scene = parse_svg_scene(malformed, model="declared:svg-literal", side=Decimal(4))
    changed = next(square for square in scene.squares if square.square_id == "square-a")
    with pytest.raises(PrecisionBridgeError, match="compatible rigid pose"):
        fit_rigid_pose(changed)

    forward = b"""<svg xmlns="http://www.w3.org/2000/svg">
      <rect id="container" x="0" y="0" width="8" height="8"/>
      <polygon id="s" transform="translate(1 0) scale(2)" points="0,0 1,0 1,1 0,1"/>
    </svg>"""
    reverse = forward.replace(b"translate(1 0) scale(2)", b"scale(2) translate(1 0)")
    forward_x = (
        parse_svg_scene(forward, model="declared:svg-literal", side=Decimal(8))
        .squares[0]
        .vertices[0]
        .x.midpoint
    )
    reverse_x = (
        parse_svg_scene(reverse, model="declared:svg-literal", side=Decimal(8))
        .squares[0]
        .vertices[0]
        .x.midpoint
    )
    assert (forward_x, reverse_x) == (Decimal(1), Decimal(2))


def test_receipt_is_sorted_stable_and_contains_no_source_bytes_or_fetch_paths() -> None:
    first = canonical_bytes(_receipt())
    second = canonical_bytes(_receipt())

    assert first == second
    assert [square["id"] for square in json.loads(first)["squares"]] == [
        "square-a",
        "square-b",
    ]
    assert b"<svg" not in first
    assert b"url" not in first.lower()
    assert b"path" not in first.lower()


def test_refusal_exact_half_angle_witness_is_rational_and_canonical() -> None:
    binding = SourceBinding.synthetic()
    pose = ExactPose.from_strings("2", "2", "1/2")
    corners = unit_corners(pose)
    assert corners == (
        ("21/10", "13/10"),
        ("27/10", "21/10"),
        ("19/10", "27/10"),
        ("13/10", "19/10"),
    )

    cells = (
        (
            RationalInterval.from_strings("2", "11/5"),
            RationalInterval.from_strings("6/5", "7/5"),
        ),
        (
            RationalInterval.from_strings("13/5", "14/5"),
            RationalInterval.from_strings("2", "11/5"),
        ),
        (
            RationalInterval.from_strings("9/5", "2"),
            RationalInterval.from_strings("13/5", "14/5"),
        ),
        (
            RationalInterval.from_strings("6/5", "7/5"),
            RationalInterval.from_strings("9/5", "2"),
        ),
    )
    witness = build_exact_witness(binding, pose, cells)
    encoded = canonical_proof_bytes(witness.to_document())
    assert encoded == canonical_proof_bytes(witness.to_document())
    assert b"0.5" not in encoded
    assert b'"t":"1/2"' in encoded
    with pytest.raises(ProofFormatError, match="source cell"):
        build_exact_witness(binding, ExactPose.from_strings("23/10", "2", "1/2"), cells)
    with pytest.raises(ProofFormatError, match="dihedral"):
        build_exact_witness(binding, pose, cells, (0, 2, 1, 3))


def test_refusal_complete_cover_split_has_no_gap_or_overlap() -> None:
    root = PoseBox.from_strings(("0", "1"), ("2", "2"), ("-1/2", "1/2"))
    lower_box, upper_box = root.split("cx", "1/2")
    cover = CoverSplit(
        region=root,
        axis="cx",
        cut="1/2",
        lower=CoverLeaf(lower_box, "rejected", "outside-source-cell"),
        upper=CoverLeaf(upper_box, "retained", "outward-image"),
    )
    assert cover.to_document()["axis"] == "cx"

    bad_upper = PoseBox.from_strings(("3/5", "1"), ("2", "2"), ("-1/2", "1/2"))
    with pytest.raises(ProofFormatError, match="partition"):
        CoverSplit(
            region=root,
            axis="cx",
            cut="1/2",
            lower=CoverLeaf(lower_box, "rejected", "outside-source-cell"),
            upper=CoverLeaf(bad_upper, "retained", "outward-image"),
        )


def test_refusal_rational_transform_order_and_nested_composition_are_exact() -> None:
    translation = RationalAffine.translation("1", "0")
    scale = RationalAffine.scale("2", "2")
    assert translation.compose(scale).apply("0", "0") == ("1", "0")
    assert scale.compose(translation).apply("0", "0") == ("2", "0")

    parent = RationalAffine.translation("10", "20")
    local = RationalAffine.scale("2", "3")
    assert parent.compose(local).apply("1/2", "1/3") == ("11", "21")


def test_refusal_exact_wall_sign_controls_distinguish_interior_tangent_crossing() -> None:
    interior = exact_wall_signs(ExactPose.from_strings("2", "2", "1/2"), "4")
    assert interior.minimum == "13/10"
    assert interior.classification == "positive"

    tangent = exact_wall_signs(ExactPose.from_strings("1/2", "1/2", "0"), "4")
    assert tangent.minimum == "0"
    assert tangent.classification == "zero"

    crossing = exact_wall_signs(ExactPose.from_strings("2/5", "1/2", "0"), "4")
    assert crossing.minimum == "-1/10"
    assert crossing.classification == "negative"


def _reseal(document: dict[str, object]) -> dict[str, object]:
    copied = json.loads(canonical_proof_bytes(document))
    copied["proof_sha256"] = hashlib.sha256(canonical_proof_bytes(copied["proof"])).hexdigest()
    return copied


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda proof: proof["binding"].update({"source_sha256": "3" * 64}),
            "independently supplied source facts",
        ),
        (lambda proof: proof["witness"].update({"correspondence": [0, 2, 1, 3]}), "dihedral"),
        (
            lambda proof: proof["witness"]["pose"].update({"cx": "21/10"}),
            "corners do not replay",
        ),
        (lambda proof: proof["witness"]["pose"].update({"t": "2/4"}), "canonical"),
        (lambda proof: proof["witness"]["rotation"].update({"c": "4/5"}), "does not match t"),
        (
            lambda proof: proof["witness"].update({"source_cells_sha256": "0" * 64}),
            "source-cell digest",
        ),
        (lambda proof: proof["cover"].pop("upper"), "cover node"),
        (
            lambda proof: proof["cover"]["upper"]["region"]["cx"].__setitem__(0, "5/2"),
            "partition",
        ),
        (
            lambda proof: proof["cover"]["lower"]["corner_images"][0]["x"].__setitem__(0, "0"),
            "corner images",
        ),
        (lambda proof: proof["wall_signs"].update({"decision": "negative"}), "wall-sign"),
        (
            lambda proof: proof["pair_controls"][1]["signs"].update({"decision": "separated"}),
            "pair-sign",
        ),
    ],
)
def test_refusal_independent_verifier_rejects_named_mutations(mutation, message: str) -> None:
    receipt = synthetic_receipt()
    proof = receipt["proof"]
    mutation(proof)
    errors = verify_proof(
        _reseal(receipt),
        SourceBinding.synthetic().to_document(),
        source_cells_sha256(synthetic_source_cells()),
    )
    assert errors
    assert message in errors[0]


def test_refusal_independent_verifier_accepts_shared_boundary_complete_cover() -> None:
    receipt = synthetic_receipt()
    assert (
        verify_proof(
            receipt,
            SourceBinding.synthetic().to_document(),
            source_cells_sha256(synthetic_source_cells()),
        )
        == []
    )


def test_refusal_pair_sign_controls_distinguish_separation_contact_and_overlap() -> None:
    proof = cast(dict[str, Any], synthetic_receipt()["proof"])
    controls = cast(list[dict[str, Any]], proof["pair_controls"])
    assert [
        (item["label"], item["signs"]["maximum"], item["signs"]["decision"])
        for item in controls
    ] == [
        ("separated", ["1", "1"], "separated"),
        ("tangent", ["0", "0"], "possible-contact"),
        ("overlap", ["-1/2", "-1/2"], "overlap"),
    ]


def test_refusal_selftest_is_byte_identical_with_assertions_disabled() -> None:
    command = [sys.executable, "-m", "cases.unitsquare_precision.refusal.run", "--selftest"]
    normal = subprocess.run(command, check=False, capture_output=True)
    optimized = subprocess.run(
        [sys.executable, "-O", *command[1:]], check=False, capture_output=True
    )
    assert normal.returncode == optimized.returncode == 0
    assert normal.stdout == optimized.stdout


def _runner_contract(payload: bytes) -> RunnerContract:
    return RunnerContract(
        experiment_id="exp-051",
        session_id="session-069",
        result_path=(
            "campaign/series/series-000-smoke-and-calibration/results/"
            "exp-051-h-053-n68-refusal-localization.json"
        ),
        authorization=RunnerAuthorization(
            session_id="session-069",
            phase_started_at="2026-09-01T13:46:55Z",
            phase_deadline_at="2026-09-01T14:11:55Z",
        ),
        parent_url="https://example.invalid/synthetic-parent.svg",
        parent_sha256=hashlib.sha256(payload).hexdigest(),
    )


def _bound_synthetic_proof(
    source_sha256: str, polygon_sha256: str
) -> tuple[dict[str, object], dict[str, object]]:
    binding = SourceBinding(
        "declared:svg-literal",
        source_sha256,
        polygon_sha256,
        RationalAffine.identity(),
        (Fraction(0), Fraction(0), Fraction(4), Fraction(4), Fraction(4)),
    )
    receipt = synthetic_receipt()
    proof = cast(dict[str, Any], receipt["proof"])
    proof["binding"] = binding.to_document()
    cast(dict[str, Any], proof["witness"])["binding"] = binding.to_document()
    return _reseal(receipt), binding.to_document()


def test_refusal_authorized_runner_is_ordered_sanitized_verified_and_cleaned(
    tmp_path: Path,
) -> None:
    payload = b"synthetic parent bytes"
    contract = _runner_contract(payload)
    target = tmp_path / contract.result_path
    target.parent.mkdir(parents=True)
    response = io.BytesIO(payload)
    retained_view: list[memoryview] = []
    events: list[str] = []
    polygon_sha256 = "a" * 64
    proof, binding = _bound_synthetic_proof(contract.parent_sha256, polygon_sha256)
    evaluators: list[object] = []

    def scan_parent(view: memoryview):
        events.append("scan")
        retained_view.append(view)
        return (
            {"stable_id": "square-b", "vertex_count": 4, "polygon_sha256": "b" * 64},
            {
                "stable_id": "square-a",
                "vertex_count": 4,
                "polygon_sha256": polygon_sha256,
            },
        )

    def model_factory(model: str):
        events.append(f"factory:{model}")

        class Evaluator:
            def __call__(self, view: memoryview, stable_id: str):
                assert bytes(view) == payload
                assert stable_id == "square-a"
                events.append(f"evaluate:{model}")
                if model == "declared:svg-literal":
                    return RunnerModelEvaluation(
                        model=model,
                        outcome="compatible",
                        reason="localized-compatible",
                        proof=proof,
                        expected_binding=binding,
                        source_cells_sha256=source_cells_sha256(synthetic_source_cells()),
                    )
                return RunnerModelEvaluation(
                    model=model,
                    outcome="refused",
                    reason="pose-compatibility-refusal",
                )

        evaluator = Evaluator()
        evaluators.append(evaluator)
        return evaluator

    document = run_authorized_runner(
        contract=contract,
        authorization=contract.authorization,
        record_path=contract.result_path,
        output_root=tmp_path,
        opener=lambda _url: response,
        structural_scan=scan_parent,
        model_factory=model_factory,
    )

    assert response.closed
    assert retained_view
    assert bytes(retained_view[0]) == b"\0" * len(payload)
    assert len({id(evaluator) for evaluator in evaluators}) == 3
    assert events == [
        "scan",
        "factory:declared:svg-literal",
        "evaluate:declared:svg-literal",
        "factory:nearest-6",
        "evaluate:nearest-6",
        "factory:truncate-6",
        "evaluate:truncate-6",
    ]
    assert document["selection"] == {
        "stable_id": "square-a",
        "polygon_sha256": polygon_sha256,
    }
    assert target.read_bytes() == canonical_runner_bytes(document) + b"\n"
    retained = target.read_bytes().lower()
    assert payload not in retained
    for forbidden in (b"child", b"gain", b"header", b"temporary", b"buffer"):
        assert forbidden not in retained


def test_refusal_runner_hashes_before_scan_and_checks_structure_and_existing_result(
    tmp_path: Path,
) -> None:
    payload = b"synthetic parent bytes"
    contract = _runner_contract(payload)
    target = tmp_path / contract.result_path
    target.parent.mkdir(parents=True)
    scanned: list[bool] = []
    opened: list[bool] = []

    bad_contract = replace(contract, parent_sha256="0" * 64)
    bad_response = io.BytesIO(payload)
    with pytest.raises(RunnerGuardError, match="digest mismatch"):
        run_authorized_runner(
            contract=bad_contract,
            authorization=bad_contract.authorization,
            record_path=bad_contract.result_path,
            output_root=tmp_path,
            opener=lambda _url: bad_response,
            structural_scan=lambda _view: scanned.append(True) or (),
            model_factory=lambda _model: pytest.fail("model evaluation reached"),
        )
    assert scanned == []
    assert bad_response.closed

    target.write_text("standing result")
    with pytest.raises(RunnerGuardError, match="existing result"):
        run_authorized_runner(
            contract=contract,
            authorization=contract.authorization,
            record_path=contract.result_path,
            output_root=tmp_path,
            opener=lambda _url: opened.append(True) or io.BytesIO(payload),
            structural_scan=lambda _view: (),
            model_factory=lambda _model: pytest.fail("model evaluation reached"),
        )
    assert opened == []


@pytest.mark.parametrize(
    ("rows", "message"),
    [
        (
            (
                {"stable_id": "a", "vertex_count": 4, "polygon_sha256": "a" * 64},
                {"stable_id": "a", "vertex_count": 4, "polygon_sha256": "b" * 64},
            ),
            "duplicate",
        ),
        (
            ({"stable_id": "a", "vertex_count": 3, "polygon_sha256": "a" * 64},),
            "four vertices",
        ),
    ],
)
def test_refusal_runner_rejects_duplicate_ids_and_non_four_vertex_polygons(
    tmp_path: Path, rows, message: str
) -> None:
    payload = b"synthetic"
    contract = _runner_contract(payload)
    (tmp_path / contract.result_path).parent.mkdir(parents=True)
    with pytest.raises(RunnerGuardError, match=message):
        run_authorized_runner(
            contract=contract,
            authorization=contract.authorization,
            record_path=contract.result_path,
            output_root=tmp_path,
            opener=lambda _url: io.BytesIO(payload),
            structural_scan=lambda _view: rows,
            model_factory=lambda _model: pytest.fail("model evaluation reached"),
        )


def test_refusal_runner_rejects_child_channel_model_reordering_and_unverified_proof(
    tmp_path: Path,
) -> None:
    payload = b"synthetic"
    contract = _runner_contract(payload)
    (tmp_path / contract.result_path).parent.mkdir(parents=True)
    row = {"stable_id": "a", "vertex_count": 4, "polygon_sha256": "a" * 64}
    bad_proof, binding = _bound_synthetic_proof(contract.parent_sha256, "a" * 64)
    cast(dict[str, Any], cast(dict[str, Any], bad_proof["proof"])["witness"])["child"] = (
        "forbidden"
    )
    bad_proof = _reseal(bad_proof)

    def factory(model: str):
        return lambda _view, _stable_id: RunnerModelEvaluation(
            model="nearest-6" if model == "declared:svg-literal" else model,
            outcome="compatible",
            reason="localized-compatible",
            proof=bad_proof,
            expected_binding=binding,
            source_cells_sha256=source_cells_sha256(synthetic_source_cells()),
        )

    with pytest.raises(RunnerGuardError, match="model order"):
        run_authorized_runner(
            contract=contract,
            authorization=contract.authorization,
            record_path=contract.result_path,
            output_root=tmp_path,
            opener=lambda _url: io.BytesIO(payload),
            structural_scan=lambda _view: (row,),
            model_factory=factory,
        )

    def child_factory(model: str):
        return lambda _view, _stable_id: RunnerModelEvaluation(
            model=model,
            outcome="compatible",
            reason="localized-compatible",
            proof=bad_proof,
            expected_binding=binding,
            source_cells_sha256=source_cells_sha256(synthetic_source_cells()),
        )

    with pytest.raises(RunnerGuardError, match="forbidden retained key"):
        run_authorized_runner(
            contract=contract,
            authorization=contract.authorization,
            record_path=contract.result_path,
            output_root=tmp_path,
            opener=lambda _url: io.BytesIO(payload),
            structural_scan=lambda _view: (row,),
            model_factory=child_factory,
        )

    invalid_proof, valid_binding = _bound_synthetic_proof(contract.parent_sha256, "a" * 64)
    cast(dict[str, Any], cast(dict[str, Any], invalid_proof["proof"])["witness"])["pose"][
        "cx"
    ] = "21/10"
    invalid_proof = _reseal(invalid_proof)
    published: list[bool] = []
    retained_view: list[memoryview] = []
    response = io.BytesIO(payload)

    def invalid_factory(model: str):
        def evaluate(view: memoryview, _stable_id: str):
            retained_view.append(view)
            if model == "declared:svg-literal":
                return RunnerModelEvaluation(
                    model=model,
                    outcome="compatible",
                    reason="localized-compatible",
                    proof=invalid_proof,
                    expected_binding=valid_binding,
                    source_cells_sha256=source_cells_sha256(synthetic_source_cells()),
                )
            return RunnerModelEvaluation(
                model=model,
                outcome="refused",
                reason="pose-compatibility-refusal",
            )

        return evaluate

    with pytest.raises(RunnerGuardError, match="independent proof verification"):
        run_authorized_runner(
            contract=contract,
            authorization=contract.authorization,
            record_path=contract.result_path,
            output_root=tmp_path,
            opener=lambda _url: response,
            structural_scan=lambda _view: (row,),
            model_factory=invalid_factory,
            publisher=lambda _path, _content: published.append(True),
        )
    assert published == []
    assert response.closed
    assert retained_view
    assert bytes(retained_view[0]) == b"\0" * len(payload)


def test_refusal_atomic_publish_cleans_temporary_on_success_failure_and_interrupt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "result.json"
    atomic_publish_new(target, b"one\n")
    assert target.read_bytes() == b"one\n"
    with pytest.raises(RunnerGuardError, match="existing result"):
        atomic_publish_new(target, b"two\n")
    assert not list(tmp_path.glob(".result.json.*.tmp"))

    target.unlink()
    original_link = os.link

    def interrupted_link(_source, _destination):
        raise KeyboardInterrupt

    monkeypatch.setattr(os, "link", interrupted_link)
    with pytest.raises(KeyboardInterrupt):
        atomic_publish_new(target, b"interrupted\n")
    assert not target.exists()
    assert not list(tmp_path.glob(".result.json.*.tmp"))
    monkeypatch.setattr(os, "link", original_link)

    def failed_link(_source, _destination):
        raise OSError("injected publication failure")

    monkeypatch.setattr(os, "link", failed_link)
    with pytest.raises(OSError, match="injected publication failure"):
        atomic_publish_new(target, b"failed\n")
    assert not target.exists()
    assert not list(tmp_path.glob(".result.json.*.tmp"))
    monkeypatch.setattr(os, "link", original_link)


def test_refusal_exp051_binding_and_runner_selftest_are_target_blind_and_optimized(
    tmp_path: Path,
) -> None:
    opened: list[bool] = []
    with pytest.raises(RunnerGuardError, match="result path"):
        run_exp051_runner(
            record_path="wrong.json",
            authorization=RunnerAuthorization(
                "session-069",
                "2026-09-01T13:46:55Z",
                "2026-09-01T14:11:55Z",
            ),
            output_root=tmp_path,
            opener=lambda _url: opened.append(True) or io.BytesIO(b"forbidden"),
            structural_scan=lambda _view: (),
            model_factory=lambda _model: pytest.fail("model evaluation reached"),
        )
    assert opened == []

    with pytest.raises(RunnerGuardError, match="authorization"):
        run_exp051_runner(
            record_path=(
                "campaign/series/series-000-smoke-and-calibration/results/"
                "exp-051-h-053-n68-refusal-localization.json"
            ),
            authorization=RunnerAuthorization(
                "session-069",
                "2026-09-01T13:46:56Z",
                "2026-09-01T14:11:55Z",
            ),
            output_root=tmp_path,
            opener=lambda _url: opened.append(True) or io.BytesIO(b"forbidden"),
            structural_scan=lambda _view: (),
            model_factory=lambda _model: pytest.fail("model evaluation reached"),
        )
    assert opened == []

    command = [
        sys.executable,
        "-m",
        "cases.unitsquare_precision.refusal.run",
        "--runner-selftest",
    ]
    normal = subprocess.run(command, check=False, capture_output=True)
    optimized = subprocess.run(
        [sys.executable, "-O", *command[1:]], check=False, capture_output=True
    )
    assert normal.returncode == optimized.returncode == 0
    assert normal.stdout == optimized.stdout
    assert not Path(
        "campaign/series/series-000-smoke-and-calibration/results/"
        "exp-051-h-053-n68-refusal-localization.json"
    ).exists()
