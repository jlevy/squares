"""Synthetic controls for the UnitSquare provenance and rigid-pose bridge."""

from __future__ import annotations

import hashlib
import io
import json
from decimal import Decimal

import pytest

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
    scene = parse_svg_scene(svg, model="declared:svg-literal", side=Decimal("4"))
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
    scene = parse_svg_scene(svg, model="declared:svg-literal", side=Decimal("4"))
    square = scene.squares[0]

    assert [(point.x.midpoint, point.y.midpoint) for point in square.vertices] == [
        (Decimal("0"), Decimal("4")),
        (Decimal("1"), Decimal("4")),
        (Decimal("1"), Decimal("3")),
        (Decimal("0"), Decimal("3")),
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
    rotated_scene = parse_svg_scene(rotated, model="declared:svg-literal", side=Decimal("5"))
    rotated_receipt = rotated_scene.receipt((fit_rigid_pose(rotated_scene.squares[0]),))
    assert verify_receipt(rotated_receipt) == []

    tangent = b"""<svg xmlns="http://www.w3.org/2000/svg">
      <rect id="container" x="0" y="0" width="3" height="3"/>
      <polygon id="wall" points="0,2 1,2 1,3 0,3"/>
      <polygon id="interior" points="1,2 2,2 2,3 1,3"/>
    </svg>"""
    tangent_scene = parse_svg_scene(tangent, model="declared:svg-literal", side=Decimal("3"))
    tangent_receipt = tangent_scene.receipt(
        tuple(fit_rigid_pose(square) for square in tangent_scene.squares)
    )
    assert verify_receipt(tangent_receipt) == []
    assert tangent_receipt["pairs"][0]["signed_separation"] == "0"  # type: ignore[index]


def test_cyclic_and_reversed_vertices_have_one_canonical_serialization() -> None:
    original = parse_svg_scene(SVG, model="declared:svg-literal", side=Decimal("4"))
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
        scene = parse_svg_scene(payload, model="declared:svg-literal", side=Decimal("4"))
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
        parse_svg_scene(duplicate, model="declared:svg-literal", side=Decimal("4"))

    malformed = SVG.replace(b"1.25,3.75", b"1.28,3.75")
    scene = parse_svg_scene(malformed, model="declared:svg-literal", side=Decimal("4"))
    changed = next(square for square in scene.squares if square.square_id == "square-a")
    with pytest.raises(PrecisionBridgeError, match="compatible rigid pose"):
        fit_rigid_pose(changed)

    forward = b"""<svg xmlns="http://www.w3.org/2000/svg">
      <rect id="container" x="0" y="0" width="8" height="8"/>
      <polygon id="s" transform="translate(1 0) scale(2)" points="0,0 1,0 1,1 0,1"/>
    </svg>"""
    reverse = forward.replace(b"translate(1 0) scale(2)", b"scale(2) translate(1 0)")
    forward_x = (
        parse_svg_scene(forward, model="declared:svg-literal", side=Decimal("8"))
        .squares[0]
        .vertices[0]
        .x.midpoint
    )
    reverse_x = (
        parse_svg_scene(reverse, model="declared:svg-literal", side=Decimal("8"))
        .squares[0]
        .vertices[0]
        .x.midpoint
    )
    assert (forward_x, reverse_x) == (Decimal("1"), Decimal("2"))


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
