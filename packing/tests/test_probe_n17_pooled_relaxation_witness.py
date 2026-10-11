"""Synthetic single-square relaxation checks; no accepted scientific data is read."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import probe_n17_pooled_relaxation_witness as tool

Q = tool.Q


def deadline() -> float:
    return time.monotonic() + 30


def pts(values: Any) -> list[tool.Point]:
    return [(Q(x), Q(y)) for x, y in values]


def selected() -> list[tool.Point]:
    return pts(
        [
            (Q(99, 100), 1),
            (1, Q(99, 100)),
            (Q(101, 100), 1),
            (Q(101, 100), Q(101, 100)),
            (1, Q(101, 100)),
        ]
    )


def pools(foreign: list[tool.Point] | None = None) -> dict[int, list[tool.Point]]:
    return {
        i: pts([(1, 1)]) if i == 0 else (foreign if i == 1 and foreign is not None else [])
        for i in range(17)
    }


def fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    source = {
        "schema": tool.cases.DESCRIPTOR_SCHEMA,
        "base_kind": tool.cases.BASE_INITIAL,
        "proof_pool": "accepted_original_parent_kernels",
        "initialization_descriptor": "init.json",
        "initialization_descriptor_sha256": "a" * 64,
    }
    certificate = {
        "schema": tool.union.SCHEMA,
        "status": "criterion_missed",
        "criterion_met": False,
        "pooled_coverage": False,
        "conditional_I_exclusion_proved": False,
        "guard": copy.deepcopy(tool.cases.GUARD),
        "container": tool.standing.CenteredContainer(tool.cases.U, tool.cases.V).record(),
        "mask": list(range(17)),
        "constants": {
            "margin": str(tool.cases.MARGIN),
            "core_vertices": tool.union.CORE_LIMIT,
            "minkowski_vertices": tool.union.MINKOWSKI_LIMIT,
            "clipped_vertices": tool.union.CLIPPED_LIMIT,
            "center_vertices": tool.cases.CENTER_LIMIT,
            "necessary_pieces": tool.union.PIECE_LIMIT,
            "generated_pairs_per_row_both_controls": tool.union.PAIR_LIMIT,
            "polygon_edges": tool.union.EDGE_LIMIT,
            "prospective_edge_pairs": tool.union.EDGE_PAIR_LIMIT,
            "input_vertices": tool.cases.INPUT_VERTICES,
            "normalized_rational_bits": tool.finite.BIT_LIMIT,
        },
    }
    hulls = {str(o): tool.finite.serial(p) for o, p in pools(pts([(3, 3)])).items()}
    five = tool.finite.serial(selected())
    certificate["custody"] = {
        "base_kind": tool.cases.BASE_INITIAL,
        "initialization_freshly_reconstructed": True,
        "parent_geometry_replayed": False,
        "child_geometry_replayed_now": False,
        "initialization_descriptor": source["initialization_descriptor"],
        "initialization_descriptor_sha256": source["initialization_descriptor_sha256"],
        "parent": {"node_sha256": "b" * 64, "seed_sha256": "c" * 64},
        "guard_source": {
            "point_origins": {"selected": five},
            "guard": copy.deepcopy(tool.cases.GUARD),
        },
        "proof_pool": {
            "original_final_contained": True,
            "unconditional_parent_pools_disjoint": True,
            "parent_geometry_replayed": False,
            "node_sha256": "b" * 64,
            "seed_sha256": "c" * 64,
            "pools": hulls,
            "selected_five": five,
        },
    }
    a, b = map(str, tool.cases.INTERVAL)
    region = {str(i): [] for i in range(1, 17)}
    piece = {
        "piece_index": 0,
        "domain": [["1", "1"]],
        "pooled": {"covered": False, "regions": region, "uncovered_probe": None},
    }
    certificate["rows"] = [
        {
            "row_index": i,
            "interval": bounds,
            "reference": {"kind": "phase3", "node": "synthetic", "step": 0, "row": i},
            "pieces": [piece] if i == 26 else [],
        }
        for i, bounds in [(25, [a, a]), (26, [a, b]), (27, [b, b])]
    ]
    return source, certificate


def write_inputs(tmp_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    source, certificate = fixture()
    replay = copy.deepcopy(certificate) | {
        "verification_passed": True,
        "invocation": {"argv": ["synthetic"]},
    }
    document: dict[str, Any] = {"schema": tool.DESCRIPTOR_SCHEMA}
    for key, value in zip(tool.INPUTS, (source, certificate, replay), strict=True):
        raw = json.dumps(value, sort_keys=True).encode()
        path = tmp_path / (key + ".json")
        path.write_bytes(raw)
        document[key] = path.name
        document[key + "_sha256"] = hashlib.sha256(raw).hexdigest()
    return document, certificate


@pytest.mark.parametrize(
    ("spans", "expected"),
    [
        ([], (Q(0), Q(1))),
        ([(Q(0), Q(1, 2)), (Q(1, 2), Q(1))], None),
        ([(Q(0), Q(1, 4)), (Q(1, 2), Q(3, 4))], (Q(1, 4), Q(1, 2))),
        ([(Q(-1), Q(2))], None),
    ],
)
def test_first_gap_closed_touching_order(spans: Any, expected: Any) -> None:
    assert tool.first_gap(Q(0), Q(1), list(reversed(spans))) == expected
    assert tool.first_gap(Q(1), Q(1), []) == (Q(1), Q(1))
    assert tool.first_gap(Q(1), Q(1), [(Q(1), Q(1))]) is None


@pytest.mark.parametrize("domain", [[(1, 1)], [(1, 1), (1, 2)], [(1, 1), (2, 2)]])
def test_point_vertical_and_diagonal_segment_selection(domain: Any) -> None:
    p = pts(domain)
    found = tool.choose_center(p, [], None, deadline())
    center = tuple(map(Q, found["center"]))
    assert center == ((p[0][0] + p[-1][0]) / 2, (p[0][1] + p[-1][1]) / 2)
    with pytest.raises(ValueError, match="no uncovered gap"):
        tool.choose_center(p, [p], None, deadline())


def test_first_sweep_x_and_vertical_gap_reconstructed() -> None:
    domain = pts([(0, 0), (2, 0), (2, 2), (0, 2)])
    regions = [
        pts([(0, 0), (2, 0), (2, Q(1, 2)), (0, Q(1, 2))]),
        pts([(0, Q(3, 2)), (2, Q(3, 2)), (2, 2), (0, 2)]),
    ]
    covered, probe = tool.sweep(domain, regions, deadline())
    assert not covered
    assert probe is not None
    found = tool.choose_center(domain, regions, str(probe), deadline())
    assert found["center"] == [str(probe), "1"]
    with pytest.raises(ValueError, match="probe differs"):
        tool.choose_center(domain, regions, str(probe + Q(1, 10)), deadline())


def test_region_384_limit_not_silently_reduced_to_256() -> None:
    # Half-plane parameter clipping accepts a convex region's full source edge roster.
    region = [(Q(i), Q(i * i)) for i in range(300)]
    assert tool.parameter_span(region, (Q(1), Q(1)), (Q(2), Q(4)), deadline()) is not None


def test_exact_pose_positive_two_square_and_containment() -> None:
    result = tool.pose((Q(1), Q(1)), pools(pts([(3, 3)])), selected(), deadline())
    assert result["status"] == "owned_point_relaxation_witness"
    assert result["all_owner0_strict"]
    assert result["all_foreign_open_avoidance"]
    shape = pts(result["square"])
    assert len(shape) == 4
    assert all(
        abs(x) == Q(1, 2) and abs(y) == Q(1, 2)
        for x, y in (tool.body(p, (Q(1), Q(1))) for p in shape)
    )
    result = tool.pose((Q(0), Q(0)), pools(), selected(), deadline())
    assert result["status"] == "criterion_missed"
    assert not result["container_passed"]


@pytest.mark.parametrize(
    "kind", ["boundary_point", "boundary_edge", "diagonal", "interior", "empty"]
)
def test_foreign_open_interior_vs_closed_boundary(kind: str) -> None:
    center = (Q(1), Q(1))
    square = tool.square(center, deadline())
    if kind == "boundary_point":
        foreign = [square[0]]
    elif kind == "boundary_edge":
        foreign = square[:2]
    elif kind == "diagonal":
        foreign = [square[0], square[2]]
    elif kind == "interior":
        foreign = [center]
    else:
        foreign = []
    result = tool.pose(center, pools(foreign), selected(), deadline())
    assert result["all_foreign_open_avoidance"] is (kind not in {"diagonal", "interior"})
    assert result["foreign_tests"]["1"]["meets_open_square"] is (
        kind in {"diagonal", "interior"}
    )


def test_owner0_boundary_is_not_strict() -> None:
    center = (Q(1), Q(1))
    own = pools()
    own[0] = [tool.square(center, deadline())[0]]
    result = tool.pose(center, own, selected(), deadline())
    assert not result["all_owner0_strict"]
    assert result["status"] == "criterion_missed"


def test_first_piece_no_candidate_fallback_and_inapplicable() -> None:
    _, certificate = fixture()
    row = certificate["rows"][1]
    first = copy.deepcopy(row["pieces"][0])
    first["domain"] = [["0", "0"]]
    second = copy.deepcopy(row["pieces"][0]) | {"piece_index": 1}
    row["pieces"] = [first, second]
    result = tool.construct(certificate, deadline=deadline())
    assert result["piece_index"] == 0
    assert result["selection"]["center"] == ["0", "0"]
    assert result["status"] == "criterion_missed"
    row["pieces"] = []
    assert tool.construct(certificate, deadline=deadline())["applicable"] is False


@pytest.mark.parametrize(
    "mutation",
    ["miss", "replay", "guard", "pool", "id", "constants", "source", "row", "regions"],
)
def test_custody_and_closed_roster_tamper_refused(mutation: str) -> None:
    source, certificate = fixture()
    replay = copy.deepcopy(certificate) | {"verification_passed": True}
    if mutation == "miss":
        certificate["status"] = "closed_I_exclusion"
    elif mutation == "replay":
        replay["verification_passed"] = False
    elif mutation == "guard":
        certificate["guard"]["owner"] = 1
    elif mutation == "pool":
        certificate["custody"]["proof_pool"]["original_final_contained"] = False
    elif mutation == "id":
        certificate["custody"]["parent"]["node_sha256"] = "d" * 64
    elif mutation == "constants":
        certificate["constants"]["clipped_vertices"] = 256
    elif mutation == "source":
        source["base_kind"] = tool.cases.BASE_CHILD
    elif mutation == "row":
        certificate["rows"].pop()
    else:
        certificate["rows"][1]["pieces"][0]["pooled"]["regions"].pop("1")
    if mutation != "replay":
        replay = copy.deepcopy(certificate) | {"verification_passed": True}
    if mutation in {"row", "regions"}:
        with pytest.raises(ValueError, match="roster"):
            tool.construct(certificate, deadline=deadline())
    else:
        with pytest.raises(ValueError, match=r"union|custody|identities|calibration"):
            tool.union_contract(source, certificate, replay)


def test_used_big_scalar_incomplete_unused_opaque() -> None:
    _, certificate = fixture()
    certificate["unused"] = "1" + "0" * 5000
    assert tool.construct(certificate, deadline=deadline())["criterion_met"] is True
    certificate["rows"][1]["pieces"][0]["domain"][0][0] = "1" + "0" * 5000
    with pytest.raises(tool.IncompleteError):
        tool.construct(certificate, deadline=deadline())


def test_sweep_resource_and_deadline_refuse_incomplete(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(tool.IncompleteError):
        tool.choose_center(pts([(1, 1)]), [], None, time.monotonic() - 1)
    monkeypatch.setattr(tool.union, "EDGE_LIMIT", 2)
    with pytest.raises(tool.IncompleteError, match="edge/pair"):
        tool.sweep(pts([(0, 0), (1, 0), (1, 1), (0, 1)]), [], deadline())


def test_actual_generate_byte_custody_and_own_replay(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document, _ = write_inputs(tmp_path)
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    result = tool.generate(document, deadline=deadline())
    assert result["criterion_met"]
    assert not result["seventeen_square_packing_proved"]
    assert tool.check(document, result, deadline=deadline())["verification_passed"] is True
    changed = copy.deepcopy(result)
    changed["selection"]["center"] = ["2", "2"]
    with pytest.raises(ValueError, match="reconstruction differs"):
        tool.check(document, changed, deadline=deadline())
    path = tmp_path / document["union_certificate"]
    path.write_bytes(path.read_bytes() + b" ")
    with pytest.raises(ValueError, match="byte identity"):
        tool.generate(document, deadline=deadline())


def test_clean_two_process_cli_reconstruction(tmp_path: Path) -> None:
    document, _ = write_inputs(tmp_path)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(document))
    script = (
        "from pathlib import Path;import sys;"
        "from devtools import probe_n17_pooled_relaxation_witness as t;"
        "t.finite.REPO=Path(sys.argv[1]);raise SystemExit(t.main(sys.argv[2:]))"
    )
    first, second = tmp_path / "first.json", tmp_path / "second.json"
    for output, args in [(first, []), (second, ["--certificate", str(first)])]:
        done = subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                str(tmp_path),
                "--descriptor",
                str(descriptor),
                *args,
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        assert done.returncode == 0, done.stderr + (
            output.read_text() if output.exists() else ""
        )
    result, replay = json.loads(first.read_text()), json.loads(second.read_text())
    assert tool.payload(result) == tool.payload(replay)
    assert replay["verification_passed"] is True
    assert result["status"] == "owned_point_relaxation_witness"
    assert not result["parent_geometry_replayed"]
    assert not result["global_optimality_proved"]


def test_input_and_output_byte_caps(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    document, _ = write_inputs(tmp_path)
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    monkeypatch.setattr(tool, "JSON_LIMIT", 8)
    with pytest.raises(tool.IncompleteError):
        tool.generate(document, deadline=deadline())
    monkeypatch.setattr(tool, "JSON_LIMIT", 10 << 20)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(document))
    monkeypatch.setattr(tool, "OUTPUT_LIMIT", 10)
    output = tmp_path / "output.json"
    assert tool.main(["--descriptor", str(descriptor), "--output", str(output)]) == 1
    assert json.loads(output.read_text())["status"] == "incomplete"


def test_positive_area_singleton_vertical_section() -> None:
    domain = pts([(0, 0), (1, 0), (1, 1)])
    covered, probe = tool.sweep(domain, [], deadline())
    assert covered is False
    assert probe == 0
    found = tool.choose_center(domain, [], str(probe), deadline())
    assert found["center"] == ["0", "0"]
    assert found["first_gap"] == ["0", "0"]


def test_quarterturn_square_equivalence() -> None:
    center = (Q(1), Q(1))
    shape = tool.square(center, deadline())
    rotated = [(2 - y, x) for x, y in shape]
    assert set(rotated) == set(shape)


def test_immutable_inputs_rechecked_after_pose(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document, _ = write_inputs(tmp_path)
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    original = tool.construct
    path = tmp_path / document["union_replay"]

    def mutate(certificate: dict[str, Any], *, deadline: float) -> dict[str, Any]:
        result = original(certificate, deadline=deadline)
        path.write_bytes(path.read_bytes() + b" ")
        return result

    monkeypatch.setattr(tool, "construct", mutate)
    with pytest.raises(ValueError, match="input bytes changed"):
        tool.generate(document, deadline=deadline())
