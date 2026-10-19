"""Saved-pose rejection remains narrower than cell or pattern exclusion."""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_saved_pose_incircles as tool


def fixture() -> tuple[Any, ...]:
    # Deliberately overlapping synthetic cell frames; this is not a scientific packing.
    lo, hi = Q(1, 2), tool.corner.U - Q(1, 2)
    polygon = [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]
    polygons = [polygon[:] for _ in range(24)]
    names = [f"synthetic-{i}" for i in range(24)]
    masks = [
        sum(1 << i for i in cells)
        for cells in itertools.islice(itertools.combinations(range(24), 17), 95)
    ]
    roster = [{"mask": mask} for mask in masks]
    classifications = []
    for cell in range(24):
        for pattern, (horizontal, vertical) in enumerate(tool.corner.CLASSES):
            used = pattern in (0, 8)
            centre = lo if pattern == 0 else hi
            classifications.append(
                {
                    "cell_index": cell,
                    "pattern_id": pattern,
                    "horizontal_class": horizontal,
                    "vertical_class": vertical,
                    "guaranteed_window_bits": list(
                        tool.corner.pattern_bits(horizontal, vertical)
                    ),
                    "rows": [
                        list(map(str, row))
                        for row in tool.corner.pattern_rows(polygon, horizontal, vertical)
                    ]
                    if used
                    else [],
                    "feasible": used,
                    "pose": [str(centre), str(centre), "1/2"] if used else None,
                }
            )
    states = [
        {
            "mask": mask,
            "certificate": {
                "kind": "surviving_relaxation_assignment",
                "cells": [i for i in range(24) if mask & (1 << i)],
                "pattern_ids": [0] * 8 + [8] * 9,
                "counts": [8, 0, 0, 9],
                "transitions": 1,
            },
        }
        for mask in masks
    ]
    accepted = {
        "schema": tool.corner.SCHEMA,
        "status": "criterion_missed",
        "criterion_met": False,
        "complete_classification": True,
        "classifications_accounted": 216,
        "states_accounted": 95,
        "classifications": classifications,
        "states": states,
        "physical_half_extent_squared_bound_checked": True,
        "cell_names": names,
        "constants": {
            "U": str(tool.corner.U),
            "H": str(tool.corner.H),
            "r": str(tool.corner.R),
            "capacity": 10,
        },
        **tool.corner.scope(),
    }
    return polygons, names, roster, accepted


def construct(data: tuple[Any, ...]) -> dict[str, Any]:
    return tool.construct(*data, deadline=time.monotonic() + 60)


def roles(tmp_path: Path, accepted: dict[str, Any]) -> dict[str, Any]:
    descriptor = {"schema": tool.corner.CONTEXT_SCHEMA, "synthetic": True}
    accepted = copy.deepcopy(accepted) | {
        "accepted_inputs": descriptor,
        "verification_passed": False,
    }
    values = {
        "corner_descriptor": descriptor,
        "corner_certificate": accepted,
        "corner_replay": accepted | {"verification_passed": True},
    }
    result: dict[str, Any] = {"schema": tool.CONTEXT_SCHEMA}
    for role, value in values.items():
        p = tmp_path / (role + ".json")
        raw = json.dumps(value).encode()
        _ = p.write_bytes(raw)
        result[role], result[role + "_sha256"] = str(p), hashlib.sha256(raw).hexdigest()
    return result


def fake_intake(data: tuple[Any, ...], calls: list[str]):
    def load(_document: Any, _deadline: float) -> tuple[Any, ...]:
        calls.append("intake")
        return (*data[:3], 0, {})

    return load


@pytest.mark.parametrize(("x", "expected"), [(Q(1, 2), Q(1, 4)), (Q(1), Q(1)), (Q(2), Q(4))])
def test_exact_below_equal_above_one(x: Q, expected: Q) -> None:
    assert tool.distance_squared((Q(0), Q(0), Q(1, 2)), (x, Q(0), Q(1, 2))) == expected


def test_full_pair_accounting_lex_first_and_equality() -> None:
    cells, names = list(range(17)), [str(i) for i in range(24)]
    poses = [(Q(2 * i), Q(0), Q(1, 2)) for i in range(17)]
    poses[1] = (Q(1), Q(0), Q(1, 2))  # Equality is retained.
    poses[2] = (Q(1, 2), Q(0), Q(1, 2))
    work = {"distance_pairs": 0}
    result = tool.evaluate_pairs(cells, poses, names, work, time.monotonic() + 10)
    assert result["first_failing_pair"]["cells"] == [0, 2]
    assert result["first_failing_pair"]["squared_distance"] == "1/4"
    assert result["failing_pair_count"] == 2
    assert work["distance_pairs"] == 136
    assert result["pairs_checked"] == 136


def test_generic_large_container_pair_candidate_is_not_square_packing() -> None:
    poses = [(Q(i), Q(0), Q(1, 2)) for i in range(17)]
    result = tool.evaluate_pairs(
        list(range(17)),
        poses,
        [str(i) for i in range(24)],
        {"distance_pairs": 0},
        time.monotonic() + 10,
    )
    assert result["incircle_compatible"] is True
    assert result["first_failing_pair"] is None


def test_all95_fail_complete12920_without_ordinary_exclusion() -> None:
    result = construct(fixture())
    assert result["status"] == "all_fixed_poses_rejected"
    assert result["criterion_met"] is False
    assert result["complete_classification"] is True
    assert result["work"]["distance_pairs"] == 12920
    assert result["work"]["one_square_inequalities"] <= 9072
    assert len(result["states"]) == 95
    assert all(
        r["pairs_checked"] == 136 and r["failing_pair_count"] > 0 for r in result["states"]
    )
    assert all(result[key] is False for key in tool.scope())


def test_candidate_status_with_explicit_stubbed_geometry_is_only_diagnostic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def stub(_polygon: Any, record: dict[str, Any], _work: Any, _deadline: float) -> tool.Pose:
        return Q(record["cell_index"] * 2), Q(0), Q(1, 2)

    monkeypatch.setattr(tool, "validate_pose", stub)
    result = construct(fixture())
    assert result["status"] == "orientation_realization_candidates"
    assert result["criterion_met"] is True
    assert len(result["incircle_compatible_masks"]) == 95
    assert result["physical_packing_proved"] is False


@pytest.mark.parametrize(
    "change",
    [
        "missing_class",
        "duplicate_class",
        "wrong_bits",
        "wrong_cell",
        "wrong_mask",
        "wrong_mask_type",
        "wrong_pattern",
        "wrong_counts",
        "wrong_pose",
        "wrong_rows",
        "bad_item",
    ],
)
def test_changed_saved_rosters_or_pose_refuse(change: str) -> None:
    data = fixture()
    accepted = data[3]
    if change == "missing_class":
        accepted["classifications"].pop()
    elif change == "duplicate_class":
        accepted["classifications"][-1] = accepted["classifications"][0]
    elif change == "wrong_bits":
        accepted["classifications"][0]["guaranteed_window_bits"] = [0, 0, 0, 0]
    elif change == "wrong_cell":
        accepted["states"][0]["certificate"]["cells"][0] = 1
    elif change == "wrong_mask":
        accepted["states"][0]["mask"] = accepted["states"][1]["mask"]
    elif change == "wrong_mask_type":
        accepted["states"][0]["mask"] = float(accepted["states"][0]["mask"])
    elif change == "wrong_pattern":
        accepted["states"][0]["certificate"]["pattern_ids"][0] = True
    elif change == "wrong_counts":
        accepted["states"][0]["certificate"]["counts"][0] = 9
    elif change == "wrong_pose":
        accepted["classifications"][0]["pose"][0] = "0"
    elif change == "wrong_rows":
        accepted["classifications"][0]["rows"][0][3] = "999"
    else:
        accepted["states"][0]["certificate"] = []
    with pytest.raises(ValueError, match=r"class|roster|choice|pattern|capacity|row|object"):
        _ = construct(data)


def test_half_extent_reach_and_one_square_rows() -> None:
    polygon = [
        (Q(0), Q(0)),
        (tool.corner.U, Q(0)),
        (tool.corner.U, tool.corner.U),
        (Q(0), tool.corner.U),
    ]
    record = {
        "feasible": True,
        "pattern_id": 0,
        "pose": ["1", "1", "1/2"],
        "rows": [list(map(str, r)) for r in tool.corner.pattern_rows(polygon, 0, 0)],
    }
    work = {"one_square_inequalities": 0}
    assert tool.validate_pose(polygon, record, work, time.monotonic() + 10)[2] == Q(1, 2)
    record["pose"][2] = "3/4"
    with pytest.raises(ValueError, match=r"one-square|half-extent"):
        _ = tool.validate_pose(polygon, record, work, time.monotonic() + 10)
    assert tool.corner.physical_half_extent_squared(Q(1, 2)) is True
    assert tool.corner.physical_half_extent_squared(Q(1, 2) + Q(1, 2**100)) is False


def test_used_big_scalar_incomplete_unused_opaque() -> None:
    data = fixture()
    data[3]["classifications"][1]["pose"] = ["1e999999999"] * 3
    assert construct(data)["complete_classification"]
    data[3]["classifications"][0]["pose"][0] = str(1 << 4096)
    with pytest.raises(tool.finite.IncompleteError, match="bit"):
        _ = construct(data)


def test_resource_boundaries_suppress_complete(monkeypatch: pytest.MonkeyPatch) -> None:
    data = fixture()
    monkeypatch.setattr(tool, "PAIR_LIMIT", 135)
    with pytest.raises(tool.finite.IncompleteError, match="pair"):
        _ = construct(data)
    monkeypatch.setattr(tool, "PAIR_LIMIT", 12920)
    monkeypatch.setattr(tool, "ROW_LIMIT", 0)
    with pytest.raises(tool.finite.IncompleteError, match="inequality"):
        _ = construct(data)
    result = tool.failure(tool.finite.IncompleteError("wall"))
    assert result["criterion_met"] is False
    assert result["complete_classification"] is False


def test_generate_fresh_custody_and_no_classification_or_dp(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    data = fixture()
    document = roles(tmp_path, data[3])
    calls: list[str] = []
    monkeypatch.setattr(tool.corner, "intake", fake_intake(data, calls))

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("old classification/DP/replay must not run")

    for name in ("classify", "capacity_dp", "construct", "generate", "check"):
        monkeypatch.setattr(tool.corner, name, forbidden)
    result = tool.generate(document, deadline=time.monotonic() + 60)
    fresh = tool.check(document, result, deadline=time.monotonic() + 60)
    assert tool.payload(result) == tool.payload(fresh)
    assert fresh["verification_passed"] is True
    assert calls == ["intake", "intake"]
    changed = copy.deepcopy(result)
    changed["states"][0]["failing_pair_count"] = 0
    with pytest.raises(ValueError, match="fresh"):
        _ = tool.check(document, changed, deadline=time.monotonic() + 60)
    p = Path(document["corner_replay"])
    _ = p.write_bytes(p.read_bytes() + b" ")
    with pytest.raises(ValueError, match="bytes"):
        _ = tool.generate(document, deadline=time.monotonic() + 60)


def test_two_clean_process_reconstruction_with_explicit_synthetic_intake(
    tmp_path: Path,
) -> None:
    data = fixture()
    document = roles(tmp_path, data[3])
    fixture_path = tmp_path / "synthetic.json"
    _ = fixture_path.write_text(
        json.dumps(
            {
                "polygons": [[[str(x), str(y)] for x, y in p] for p in data[0]],
                "names": data[1],
                "roster": data[2],
            }
        )
    )
    descriptor = tmp_path / "descriptor.json"
    _ = descriptor.write_text(json.dumps(document))
    script = """
import json, sys
from pathlib import Path
from fractions import Fraction as Q
from devtools import check_n17_saved_pose_incircles as t
f=json.loads(Path(sys.argv[1]).read_bytes())
polys=[[(Q(x),Q(y)) for x,y in p] for p in f['polygons']]
t.corner.intake=lambda d,deadline:(polys,f['names'],f['roster'],0,{})
raise SystemExit(t.main(sys.argv[2:]))
"""
    outputs = [tmp_path / "result.json", tmp_path / "fresh.json"]
    for index, output in enumerate(outputs):
        args = [
            sys.executable,
            "-c",
            script,
            str(fixture_path),
            "--descriptor",
            str(descriptor),
            "--output",
            str(output),
        ]
        if index:
            args += ["--certificate", str(outputs[0])]
        completed = subprocess.run(
            args, capture_output=True, text=True, timeout=60, check=False
        )
        assert completed.returncode == 0, completed.stderr
    assert tool.payload(json.loads(outputs[0].read_bytes())) == tool.payload(
        json.loads(outputs[1].read_bytes())
    )


@pytest.mark.parametrize("change", ["payload", "status", "schema", "counter", "extra", "list"])
def test_accepted_role_premise_refuses_before_old_intake(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    change: str,
) -> None:
    data = fixture()
    document = roles(tmp_path, data[3])
    role = "corner_replay" if change == "payload" else "corner_certificate"
    p = Path(document[role])
    record = json.loads(p.read_bytes())
    if change == "payload":
        record["classifications"][0]["feasible"] = False
    elif change == "status":
        record["status"] = "ordinary_assignment_obstructions"
    elif change == "schema":
        record["schema"] = "other"
    elif change == "counter":
        record["states_accounted"] = 95.0
    elif change == "extra":
        document["unknown"] = True
    else:
        record = []
    raw = json.dumps(record).encode()
    _ = p.write_bytes(raw)
    document[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    calls: list[str] = []
    monkeypatch.setattr(tool.corner, "intake", fake_intake(data, calls))
    with pytest.raises(ValueError, match=r"premise|descriptor|object"):
        _ = tool.intake(document, time.monotonic() + 60)
    assert not calls


def test_postread_mutation_and_transitive_alias_refuse(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data = fixture()
    document = roles(tmp_path, data[3])
    p = Path(document["corner_certificate"])

    def mutate(_document: Any, _deadline: float) -> tuple[Any, ...]:
        _ = p.write_bytes(p.read_bytes() + b" ")
        return (*data[:3], 0, {})

    monkeypatch.setattr(tool.corner, "intake", mutate)
    with pytest.raises(ValueError, match="premise bytes changed"):
        _ = tool.generate(document, deadline=time.monotonic() + 60)
    document = roles(tmp_path, data[3])

    def alias(_document: Any, _deadline: float) -> tuple[Any, ...]:
        return (*data[:3], 0, {p: b"conflicting"})

    monkeypatch.setattr(tool.corner, "intake", alias)
    with pytest.raises(ValueError, match="conflicting transitive"):
        _ = tool.intake(document, time.monotonic() + 60)
