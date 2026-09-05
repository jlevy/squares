"""Target-blind controls for the UnitSquare production adapter."""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import urllib.request
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import BinaryIO, cast

import pytest

from cases.unitsquare_precision.production.adapter import (
    BoundedResponse,
    ProductionAdapterError,
    StructuralRefusalError,
    TransformRefusalError,
    bounded_parent_opener,
    parse_scene,
    parse_transform,
    production_model_factory,
    structural_scanner,
)
from cases.unitsquare_precision.production.run import (
    EXP054_RESULT_PATH,
    PARENT_SHA256,
    PARENT_URL,
    ProductionDependencies,
    ProductionGuardError,
    literal_test_dependencies,
    production_dependencies,
    run_literal,
    verified_publisher,
)
from cases.unitsquare_precision.production.verify import (
    ResultVerificationError,
    verify_result_bytes,
)
from cases.unitsquare_precision.refusal.run import (
    RunnerAuthorization,
    RunnerGuardError,
    atomic_publish_new,
)

_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 4">
<rect id="container" width="4" height="4"/>
<g transform="translate(1,1)">
<polygon id="b"
 points="0.000000,0.000000 1.000000,0.000000 1.000000,1.000000 0.000000,1.000000"/>
</g></svg>"""


def _bytes(document: object) -> bytes:
    return json.dumps(document, sort_keys=True, separators=(",", ":")).encode() + b"\n"


def _reseal_first_proof(document: dict[str, object]) -> None:
    models = cast(list[dict[str, object]], document["models"])
    envelope = cast(dict[str, object], models[0]["proof"])
    proof = cast(dict[str, object], envelope["proof"])
    envelope["proof_sha256"] = hashlib.sha256(
        json.dumps(proof, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def test_literal_production_argv_is_target_blind_and_optimized() -> None:
    command = [
        sys.executable,
        "-m",
        "cases.unitsquare_precision.production.run",
        "--record",
        EXP054_RESULT_PATH,
    ]
    normal = subprocess.run(command, check=False, capture_output=True)
    optimized = subprocess.run(
        [sys.executable, "-O", *command[1:]], check=False, capture_output=True
    )
    assert normal.returncode == optimized.returncode == 0
    assert normal.stdout == optimized.stdout
    assert not Path(EXP054_RESULT_PATH).exists()


def test_literal_command_binds_path_and_refuses_existing_result_before_open(
    tmp_path: Path,
) -> None:
    dependencies = literal_test_dependencies(tmp_path)
    opened: list[str] = []
    guarded = replace(
        dependencies,
        opener=lambda url: opened.append(url) or io.BytesIO(_SVG),
    )
    with pytest.raises(RunnerGuardError, match="result path"):
        run_literal(["--record", "wrong.json"], guarded)
    assert opened == []

    mismatched = replace(
        guarded,
        authorization=RunnerAuthorization(
            "session-074",
            "2026-09-02T00:30:01Z",
            "2026-09-02T00:50:00Z",
        ),
    )
    with pytest.raises(RunnerGuardError, match="authorization"):
        run_literal(["--record", EXP054_RESULT_PATH], mismatched)
    assert opened == []

    target = tmp_path / EXP054_RESULT_PATH
    target.parent.mkdir(parents=True)
    target.write_text("standing", encoding="utf-8")
    with pytest.raises(RunnerGuardError, match="existing result"):
        run_literal(["--record", EXP054_RESULT_PATH], guarded)
    assert opened == []


def test_digest_guard_precedes_scanner_and_closes_response(tmp_path: Path) -> None:
    dependencies = literal_test_dependencies(tmp_path)
    target = tmp_path / EXP054_RESULT_PATH
    target.parent.mkdir(parents=True)
    response = io.BytesIO(b"changed source")
    scanned: list[bool] = []
    bad = ProductionDependencies(
        dependencies.contract,
        dependencies.authorization,
        lambda _url: response,
        lambda _payload: scanned.append(True) or (),
        dependencies.model_factory,
        tmp_path,
    )
    with pytest.raises(RunnerGuardError, match="digest mismatch"):
        run_literal(["--record", EXP054_RESULT_PATH], bad)
    assert scanned == []
    assert response.closed
    assert not target.exists()


def test_strict_scanner_selects_utf8_order_and_binds_polygon_digest() -> None:
    first = _SVG.replace(b'id="b"', b'id="z"')
    second = first.replace(b"</svg>", b'<polygon id="a" points="0,0 1,0 1,1 0,1"/></svg>')
    rows = structural_scanner(expected_polygon_count=2)(memoryview(second))
    assert [row["stable_id"] for row in rows] == ["a", "z"]
    assert all(len(str(row["polygon_sha256"])) == 64 for row in rows)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (b'<!DOCTYPE svg [<!ENTITY x "y">]><svg viewBox="0 0 1 1"/>', "DTD"),
        (_SVG.replace(b'id="b"', b'id=""'), "stable id"),
        (_SVG.replace(b"0.000000,1.000000", b""), "four coordinate"),
        (_SVG.replace(b"0.000000,0.000000", b"0.0.0,0.000000"), "unsupported syntax"),
        (_SVG.replace(b"0.000000,0.000000", b"0.000000,,0.000000"), "unsupported syntax"),
        (_SVG.replace(b'id="b"', b'id="b" style="transform:scale(2)"'), "CSS transform"),
        (_SVG.replace(b"</svg>", b'<use href="#b"/></svg>'), "geometry indirection"),
        (_SVG.replace(b'viewBox="0 0 4 4"', b'viewBox="0 0 5 4"'), "disagree"),
    ],
)
def test_scanner_named_structure_mutations_refuse(mutation: bytes, message: str) -> None:
    with pytest.raises(StructuralRefusalError, match=message):
        structural_scanner(expected_polygon_count=1)(memoryview(mutation))


def test_exact_transform_order_nested_composition_and_quadrant_rotation() -> None:
    forward = parse_transform("translate(1,2) scale(2,3)")
    reverse = parse_transform("scale(2,3) translate(1,2)")
    assert forward.apply("1", "1") == ("3", "5")
    assert reverse.apply("1", "1") == ("4", "9")
    assert forward != reverse
    assert parse_transform("rotate(90)").apply("1", "0") == ("0", "1")
    parent = parse_transform("translate(1,0)")
    child = parse_transform("scale(2)")
    assert parent.compose(child).apply("1", "0") == ("3", "0")


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("rotate(13.5)", "outward exact certificate"),
        ("matrix(1 0 0 0 0 0)", "singular"),
        ("translate(1) garbage", "malformed"),
    ],
)
def test_transform_mutations_refuse(text: str, message: str) -> None:
    with pytest.raises(TransformRefusalError, match=message):
        parse_transform(text)


def test_only_the_selected_polygon_transform_can_refuse_its_model() -> None:
    scene = b"""<svg viewBox="0 0 4 4">
<g transform="translate(1,1)">
<polygon id="a"
 points="0.000000,0.000000 1.000000,0.000000 1.000000,1.000000 0.000000,1.000000"/>
</g>
<g transform="rotate(13.5)">
<polygon id="b"
 points="0.000000,0.000000 1.000000,0.000000 1.000000,1.000000 0.000000,1.000000"/>
</g></svg>"""
    factory = production_model_factory(expected_polygon_count=2, side=Fraction(4))
    selected = factory("declared:svg-literal")(memoryview(scene), "a")
    unsupported = factory("declared:svg-literal")(memoryview(scene), "b")
    assert selected.outcome == "compatible"
    assert (unsupported.outcome, unsupported.reason) == (
        "refused",
        "affine-transform-refusal",
    )


def test_selected_path_scan_enforces_depth_before_python_recursion() -> None:
    depth = sys.getrecursionlimit() + 1
    scene = (
        b'<svg viewBox="0 0 1 1">'
        + b"<g>" * depth
        + b'<polygon id="a" points="0,0 1,0 1,1 0,1"/>'
        + b"</g>" * depth
        + b"</svg>"
    )
    with pytest.raises(StructuralRefusalError, match="bounded parser limits"):
        parse_scene(memoryview(scene), parse_transforms=True, selected_id="a")


def test_three_models_are_isolated_and_produce_exact_verified_proofs() -> None:
    scanner_row = structural_scanner(expected_polygon_count=1)(memoryview(_SVG))[0]
    factory = production_model_factory(expected_polygon_count=1, side=Fraction(4))
    evaluators = [
        factory(model)
        for model in (
            "declared:svg-literal",
            "nearest-6",
            "truncate-6",
        )
    ]
    evaluations = [evaluator(memoryview(_SVG), "b") for evaluator in evaluators]
    assert len({id(evaluator) for evaluator in evaluators}) == 3
    assert [evaluation.model for evaluation in evaluations] == [
        "declared:svg-literal",
        "nearest-6",
        "truncate-6",
    ]
    assert all(evaluation.outcome == "compatible" for evaluation in evaluations)
    assert all(
        evaluation.expected_binding["polygon_sha256"] == scanner_row["polygon_sha256"]
        for evaluation in evaluations
        if evaluation.expected_binding is not None
    )


def test_selected_polygon_gets_a_complete_nonnegative_wall_cover() -> None:
    near_wall = _SVG.replace(b"translate(1,1)", b"translate(0.25,1)")
    evaluation = production_model_factory(expected_polygon_count=1, side=Fraction(4))(
        "declared:svg-literal"
    )(memoryview(near_wall), "b")
    assert evaluation.outcome == "compatible"
    assert evaluation.proof is not None
    proof = cast(dict[str, object], evaluation.proof["proof"])
    cover = cast(dict[str, object], proof["cover"])
    walls = cast(dict[str, object], proof["wall_signs"])
    assert cover["kind"] == "split"
    assert walls["decision"] == "nonnegative"


@pytest.mark.parametrize(("left", "right"), [("0", "1"), ("-0.1", "0.9")])
def test_tangent_and_crossing_squares_remain_typed_unresolved(left: str, right: str) -> None:
    points = " ".join(
        (
            f"{left},4",
            f"{right},4",
            f"{right},3",
            f"{left},3",
        )
    )
    scene = f'<svg viewBox="0 0 4 4"><polygon id="w" points="{points}"/></svg>'.encode()
    evaluation = production_model_factory(expected_polygon_count=1, side=Fraction(4))(
        "declared:svg-literal"
    )(memoryview(scene), "w")
    assert (evaluation.outcome, evaluation.reason) == ("refused", "unresolved")


def test_rational_half_angle_scene_replays_exactly() -> None:
    rotated = b"""<svg viewBox="0 0 4 4">
<polygon id="r"
 points="2.100000,2.700000 2.700000,1.900000 1.900000,1.300000 1.300000,2.100000"/>
</svg>"""
    evaluation = production_model_factory(expected_polygon_count=1, side=Fraction(4))(
        "declared:svg-literal"
    )(memoryview(rotated), "r")
    assert evaluation.outcome == "compatible"
    assert evaluation.proof is not None
    witness = cast(dict[str, object], evaluation.proof["proof"])["witness"]
    pose = cast(dict[str, object], cast(dict[str, object], witness)["pose"])
    rotation = cast(dict[str, object], cast(dict[str, object], witness)["rotation"])
    assert pose == {"cx": "2", "cy": "2", "t": "1/2"}
    assert rotation == {"c": "3/5", "s": "4/5"}

    reversed_scene = rotated.replace(
        b"2.100000,2.700000 2.700000,1.900000 1.900000,1.300000 1.300000,2.100000",
        b"1.300000,2.100000 1.900000,1.300000 2.700000,1.900000 2.100000,2.700000",
    )
    reversed_evaluation = production_model_factory(expected_polygon_count=1, side=Fraction(4))(
        "declared:svg-literal"
    )(memoryview(reversed_scene), "r")
    assert reversed_evaluation.outcome == "compatible"
    assert reversed_evaluation.proof is not None
    reversed_witness = cast(dict[str, object], reversed_evaluation.proof["proof"])["witness"]
    assert cast(dict[str, object], reversed_witness)["correspondence"] in (
        [0, 3, 2, 1],
        [3, 2, 1, 0],
        [2, 1, 0, 3],
        [1, 0, 3, 2],
    )


def test_negative_zero_truncation_uses_the_published_sign() -> None:
    negative_zero = _SVG.replace(
        b"0.000000,0.000000",
        b"-0.000000,0.000000",
        1,
    )
    evaluation = production_model_factory(expected_polygon_count=1, side=Fraction(4))(
        "truncate-6"
    )(memoryview(negative_zero), "b")
    assert evaluation.outcome == "compatible"
    assert evaluation.proof is not None
    witness = cast(dict[str, object], evaluation.proof["proof"])["witness"]
    cells = cast(list[dict[str, list[str]]], cast(dict[str, object], witness)["source_cells"])
    assert cells[0]["x"] == ["999999/1000000", "1"]


def test_six_place_semantics_refuse_only_the_inapplicable_models() -> None:
    short = _SVG.replace(b"0.000000", b"0.0").replace(b"1.000000", b"1.0")
    factory = production_model_factory(expected_polygon_count=1, side=Fraction(4))
    outcomes = [
        factory(model)(memoryview(short), "b")
        for model in ("declared:svg-literal", "nearest-6", "truncate-6")
    ]
    assert outcomes[0].outcome == "compatible"
    assert [(item.outcome, item.reason) for item in outcomes[1:]] == [
        ("refused", "serialization-refusal"),
        ("refused", "serialization-refusal"),
    ]


def test_undeclared_reported_side_is_a_typed_serialization_refusal() -> None:
    factory = production_model_factory(expected_polygon_count=1, side=None)
    outcomes = [
        factory(model)(memoryview(_SVG), "b")
        for model in ("declared:svg-literal", "nearest-6", "truncate-6")
    ]
    assert [(item.outcome, item.reason) for item in outcomes] == [
        ("refused", "serialization-refusal"),
        ("refused", "serialization-refusal"),
        ("refused", "serialization-refusal"),
    ]


def test_whole_runner_retains_three_typed_side_refusals(tmp_path: Path) -> None:
    dependencies = literal_test_dependencies(tmp_path)
    target = tmp_path / EXP054_RESULT_PATH
    target.parent.mkdir(parents=True)
    dependencies = replace(
        dependencies,
        model_factory=production_model_factory(expected_polygon_count=1, side=None),
    )
    document = run_literal(["--record", EXP054_RESULT_PATH], dependencies)
    models = cast(list[dict[str, object]], document["models"])
    assert [(row["outcome"], row["reason"]) for row in models] == [
        ("refused", "serialization-refusal"),
        ("refused", "serialization-refusal"),
        ("refused", "serialization-refusal"),
    ]
    assert verify_result_bytes(target.read_bytes(), dependencies.contract) == document


def test_bounded_response_refuses_oversize_nonbytes_and_second_read() -> None:
    response = io.BytesIO(b"12345")
    bounded = BoundedResponse(response, byte_cap=4)
    with pytest.raises(ProductionAdapterError, match="byte cap"):
        bounded.read()
    bounded.close()
    assert response.closed

    class NonBytes:
        closed = False

        def read(self, _size: int | None = -1) -> object:
            return "not bytes"

        def close(self) -> None:
            self.closed = True

    nonbytes = BoundedResponse(cast(BinaryIO, NonBytes()))
    with pytest.raises(ProductionAdapterError, match="did not return bytes"):
        nonbytes.read()
    nonbytes.close()

    once = BoundedResponse(io.BytesIO(b"ok"))
    assert once.read() == b"ok"
    with pytest.raises(ProductionAdapterError, match="one bounded read"):
        once.read()
    once.close()


def test_bounded_opener_binds_url_timeout_redirect_and_cleanup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_url = "https://example.invalid/parent.svg"

    class Response(io.BytesIO):
        def __init__(self, payload: bytes, final_url: str) -> None:
            super().__init__(payload)
            self._final_url = final_url

        def geturl(self) -> str:
            return self._final_url

    class Network:
        def __init__(self, response: Response) -> None:
            self.response = response
            self.calls: list[tuple[str, int]] = []

        def open(self, url: str, *, timeout: int) -> Response:
            self.calls.append((url, timeout))
            return self.response

    response = Response(b"bounded", expected_url)
    network = Network(response)
    monkeypatch.setattr(urllib.request, "build_opener", lambda *_handlers: network)
    opener = bounded_parent_opener(expected_url, byte_cap=8, timeout_seconds=7)
    with pytest.raises(ProductionAdapterError, match="frozen source"):
        opener("https://example.invalid/wrong.svg")
    assert network.calls == []
    bounded = opener(expected_url)
    assert bounded.read() == b"bounded"
    bounded.close()
    assert response.closed
    assert network.calls == [(expected_url, 7)]

    redirect = Response(b"bounded", "https://example.invalid/redirected.svg")
    redirected_network = Network(redirect)
    monkeypatch.setattr(
        urllib.request,
        "build_opener",
        lambda *_handlers: redirected_network,
    )
    redirect_opener = bounded_parent_opener(expected_url)
    with pytest.raises(ProductionAdapterError, match="redirect"):
        redirect_opener(expected_url)
    assert redirect.closed


def test_production_constructor_binds_only_the_frozen_parent(tmp_path: Path) -> None:
    synthetic = literal_test_dependencies(tmp_path)
    with pytest.raises(ProductionGuardError, match="frozen n=68 parent"):
        production_dependencies(
            contract=synthetic.contract,
            authorization=synthetic.authorization,
            output_root=tmp_path,
        )

    target_contract = replace(
        synthetic.contract,
        parent_url=PARENT_URL,
        parent_sha256=PARENT_SHA256,
    )
    production = production_dependencies(
        contract=target_contract,
        authorization=synthetic.authorization,
        output_root=tmp_path,
    )
    polygons = "".join(
        f'<polygon id="p{index:03d}" points="0,0 1,0 1,1 0,1"/>' for index in range(68)
    )
    scene = f'<svg viewBox="0 0 4 4">{polygons}</svg>'.encode()
    rows = production.structural_scan(memoryview(scene))
    assert len(rows) == 68
    evaluation = production.model_factory("declared:svg-literal")(memoryview(scene), "p000")
    assert (evaluation.outcome, evaluation.reason) == (
        "refused",
        "serialization-refusal",
    )


def test_whole_result_verifier_rejects_model_binding_and_proof_mutations(
    tmp_path: Path,
) -> None:
    dependencies = literal_test_dependencies(tmp_path)
    target = tmp_path / EXP054_RESULT_PATH
    target.parent.mkdir(parents=True)
    document = run_literal(["--record", EXP054_RESULT_PATH], dependencies)
    content = target.read_bytes()
    assert verify_result_bytes(content, dependencies.contract) == document

    reordered = json.loads(content)
    reordered["model_order"] = list(reversed(reordered["model_order"]))
    with pytest.raises(ResultVerificationError, match="inventory"):
        verify_result_bytes(_bytes(reordered), dependencies.contract)

    forged = json.loads(content)
    forged["models"][0]["proof"]["proof"]["witness"]["rotation"]["c"] = "0"
    _reseal_first_proof(forged)
    with pytest.raises(ResultVerificationError, match="proof verification"):
        verify_result_bytes(_bytes(forged), dependencies.contract)

    missing_leaf = json.loads(content)
    del missing_leaf["models"][0]["proof"]["proof"]["cover"]["corner_images"]
    _reseal_first_proof(missing_leaf)
    with pytest.raises(ResultVerificationError, match="cover leaf"):
        verify_result_bytes(_bytes(missing_leaf), dependencies.contract)

    wall = json.loads(content)
    wall["models"][0]["proof"]["proof"]["wall_signs"]["decision"] = "negative"
    _reseal_first_proof(wall)
    with pytest.raises(ResultVerificationError, match="nonnegative wall"):
        verify_result_bytes(_bytes(wall), dependencies.contract)

    pair = json.loads(content)
    pair["models"][0]["proof"]["proof"]["pair_controls"][0]["signs"]["decision"] = "overlap"
    _reseal_first_proof(pair)
    with pytest.raises(ResultVerificationError, match="proof verification"):
        verify_result_bytes(_bytes(pair), dependencies.contract)

    leaked = json.loads(content)
    leaked["models"][0]["proof"]["proof"]["child"] = "forbidden"
    _reseal_first_proof(leaked)
    with pytest.raises(ResultVerificationError, match="forbidden retained key"):
        verify_result_bytes(_bytes(leaked), dependencies.contract)

    extra = json.loads(content)
    extra["models"][0]["proof"]["proof"]["note"] = "seemingly harmless"
    _reseal_first_proof(extra)
    with pytest.raises(ResultVerificationError, match="proof fields"):
        verify_result_bytes(_bytes(extra), dependencies.contract)


def test_verify_before_publication_and_atomic_cleanup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dependencies = literal_test_dependencies(tmp_path)
    target = tmp_path / "result.json"
    called: list[bytes] = []
    publisher = verified_publisher(
        dependencies.contract,
        lambda _path, content: called.append(content),
    )
    with pytest.raises(ResultVerificationError):
        publisher(target, b"{}\n")
    assert called == []
    assert not target.exists()

    atomic_publish_new(target, b"one\n")
    with pytest.raises(RunnerGuardError, match="existing result"):
        atomic_publish_new(target, b"two\n")
    assert target.read_bytes() == b"one\n"
    assert not list(tmp_path.glob(".result.json.*.tmp"))

    target.unlink()

    def interrupt(_source: object, _destination: object) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(os, "link", interrupt)
    with pytest.raises(KeyboardInterrupt):
        atomic_publish_new(target, b"interrupted\n")
    assert not target.exists()
    assert not list(tmp_path.glob(".result.json.*.tmp"))


def test_parser_never_exposes_xml_nodes_or_source_bytes() -> None:
    scene = parse_scene(memoryview(_SVG), parse_transforms=True)
    encoded = repr(scene).lower().encode()
    assert b"<svg" not in encoded
    assert b"element" not in encoded
    assert b"child" not in encoded
    assert b"gain" not in encoded


def test_successful_production_parse_zeroes_the_runner_buffer(tmp_path: Path) -> None:
    dependencies = literal_test_dependencies(tmp_path)
    target = tmp_path / EXP054_RESULT_PATH
    target.parent.mkdir(parents=True)
    retained_views: list[memoryview] = []
    scanner = dependencies.structural_scan

    def retaining_scan(view: memoryview):
        retained_views.append(view)
        return scanner(view)

    run_literal(
        ["--record", EXP054_RESULT_PATH],
        replace(dependencies, structural_scan=retaining_scan),
    )
    assert retained_views
    assert bytes(retained_views[0]) == b"\0" * len(retained_views[0])


def test_production_module_has_no_assertion_dependent_guard() -> None:
    root = Path("cases/unitsquare_precision/production")
    for path in root.glob("*.py"):
        assert "assert " not in path.read_text(encoding="utf-8")
