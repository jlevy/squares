"""Target-free exact center-case and accepted-premise controls."""

from __future__ import annotations

import copy
import gzip
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import probe_n17_conditional_center_cases as control

Q = control.Q


def deadline() -> float:
    return time.monotonic() + 30


def groups(points: dict[int, list[tuple[Q, Q]]] | None = None) -> dict[str, Any]:
    return {str(i): control.finite.serial((points or {}).get(i, [])) for i in range(17)}


def row(
    polygons: list[list[tuple[Q, Q]]], lo: Q = control.INTERVAL[0], hi: Q = control.INTERVAL[1]
) -> dict[str, Any]:
    return {
        "interval": [str(lo), str(hi)],
        "reference": {"kind": "parent", "node": "synthetic", "step": 0, "row": 0},
        "outer_domain": [],
        "residual_polygons": [control.finite.serial(p) for p in polygons],
    }


def test_feasible_two_square_control_never_closes() -> None:
    # Exact feasible pair; no claim of a complete seventeen-square packing.
    p = (Q(1), Q(1))
    result = control.construct(
        [row([[p]], Q(53, 128), Q(53, 128))],
        groups({0: [p], 1: [(Q(3), Q(3))]}),
        deadline=deadline(),
    )
    assert result["status"] == "criterion_missed"
    assert not result["conditional_I_exclusion_proved"]
    assert result["alpha"] == "2"
    assert result["beta"] == "0"
    assert [c["id"] for c in result["cases"]] == ["--", "-+", "+-", "++"]
    assert all(c["status"] == "unresolved" for c in result["cases"])
    assert all(["1", "1"] in c["rows"][0]["pieces"][0] for c in result["cases"])
    assert control.contains(control.finite.polygon(result["unsplit"]["K"]), p)


@pytest.mark.parametrize("removed", [None, 1, 2, 3, 4])
def test_all_four_positive_and_three_of_four_missed(removed: int | None) -> None:
    points = [(Q(2), Q(1)), (Q(1), Q(2)), (Q(3), Q(2)), (Q(2), Q(3))]
    foreign = {i + 1: [p] for i, p in enumerate(points) if i + 1 != removed}
    result = control.construct(
        [row([[p] for p in points])], groups(foreign), deadline=deadline()
    )
    assert result["unsplit"]["status"] == "unresolved"
    assert result["unsplit"]["K"] == []
    assert result["alpha"] == "4"
    assert result["beta"] == "0"
    assert sum(c["closed"] for c in result["cases"]) == (4 if removed is None else 3)
    assert result["conditional_I_exclusion_proved"] == (removed is None)
    assert result["status"] == ("closed_I_exclusion" if removed is None else "criterion_missed")


def test_unsplit_and_pooled_intersection_priority() -> None:
    p = (Q(1), Q(1))
    result = control.construct([row([[p]])], groups({1: [p]}), deadline=deadline())
    assert result["unsplit"]["status"] == "shared_owned_point"
    assert all(c["status"] == "not_needed_unsplit_proved" for c in result["cases"])
    result = control.construct(
        [row([[(Q(3), Q(3))]])], groups({0: [p], 1: [p]}), deadline=deadline()
    )
    assert result["unsplit"]["status"] == "conditional_pooled_intersection"


def test_disconnected_clip_precedes_convexification_and_empty_case() -> None:
    pieces = control.necessary_pieces([row([[(Q(0), Q(1))], [(Q(5), Q(1))]])], deadline(), [0])
    assert pieces[0]["pieces"] == []
    result = control.construct(
        [row([[(Q(0), Q(1))], [(Q(5), Q(1))]])], groups(), deadline=deadline()
    )
    assert result["unsplit"]["status"] == "empty_case"
    assert result["conditional_I_exclusion_proved"]


def test_closed_guard_seams_are_preserved() -> None:
    p = (Q(1), Q(1))
    pieces = control.necessary_pieces(
        [row([[p]], Q(25, 64), Q(13, 32)), row([[p]], Q(27, 64), Q(7, 16))], deadline(), [0]
    )
    assert [r["interval"] for r in pieces] == [(Q(13, 32), Q(13, 32)), (Q(27, 64), Q(27, 64))]


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ([], [(0, 0)], []),
        ([(0, 0)], [(0, 0)], [(0, 0)]),
        ([(0, 0), (2, 0)], [(1, 0), (3, 0)], [(1, 0), (2, 0)]),
        ([(0, 0), (2, 2)], [(0, 2), (2, 0)], [(1, 1)]),
        ([(0, 0), (1, 0), (1, 1), (0, 1)], [(1, 1), (2, 1), (2, 2), (1, 2)], [(1, 1)]),
        ([(0, 0)], [(1, 1)], []),
    ],
)
def test_closed_intersection_degeneracies(first: Any, second: Any, expected: Any) -> None:
    def convert(pts: Any) -> list[tuple[Q, Q]]:
        return [(Q(x), Q(y)) for x, y in pts]

    assert control.intersection(convert(first), convert(second), deadline()) == convert(
        expected
    )


def test_both_axes_rectangle_corners_and_strict_margin() -> None:
    p = (Q(1), Q(1))
    rs = control.necessary_pieces([row([[p]], Q(0), Q(1))], deadline(), [0])
    planes = list(control.ownership_planes(rs, deadline()))
    assert len(planes) == 16
    for a, b, rhs in planes:
        assert control.finite.dot(p, (a, b)) < rhs
    zero = [{"row_index": 0, "reference": {}, "interval": (Q(0), Q(0)), "pieces": [[p]]}]
    k = control.ownership_kernel(zero, deadline())
    assert control.contains(k, p)
    assert not control.contains(k, (Q(3, 2), Q(1)))
    assert control.contains(k, (Q(3, 2) - control.MARGIN, Q(1)))


@pytest.mark.parametrize(
    ("cap", "value"), [("INPUT_VERTICES", 0), ("CENTER_LIMIT", 0), ("K_LIMIT", 0)]
)
def test_resource_caps_are_incomplete(
    monkeypatch: pytest.MonkeyPatch, cap: str, value: int
) -> None:
    monkeypatch.setattr(control, cap, value)
    with pytest.raises(control.IncompleteError):
        control.construct([row([[(Q(1), Q(1))]])], groups(), deadline=deadline())


def test_used_big_rational_and_expired_deadline_incomplete() -> None:
    raw = row([[(Q(1), Q(1))]])
    raw["residual_polygons"][0][0][0] = str(1 << 4097)
    with pytest.raises(control.IncompleteError):
        control.construct([raw], groups(), deadline=deadline())
    with pytest.raises(control.IncompleteError):
        control.construct([], groups(), deadline=time.monotonic() - 1)


def test_selected_five_subset_control_refuses_wrong_point() -> None:
    with pytest.raises(ValueError, match="subset calibration"):
        control.construct(
            [row([[(Q(1), Q(1))]])], groups(), deadline=deadline(), selected=[(Q(3), Q(3))]
        )


@pytest.mark.parametrize(
    "changes",
    [
        {"base_kind": control.BASE_CHILD},
        {"proof_pool": "partial_child"},
        {"child_object": {}},
        {"schema": "wrong"},
    ],
)
def test_selected_descriptor_scope_refuses(changes: dict[str, Any]) -> None:
    descriptor = {
        "schema": control.DESCRIPTOR_SCHEMA,
        "base_kind": control.BASE_INITIAL,
        "proof_pool": "accepted_original_parent_kernels",
        "initialization_descriptor": "missing",
        "initialization_descriptor_sha256": "missing",
    } | changes
    with pytest.raises(ValueError, match=r"descriptor|pool|unsupported"):
        control.intake(descriptor, {}, deadline())


def test_check_reconstructs_and_refuses_margin_or_case_tamper(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rs, gs = [row([[(Q(1), Q(1))]])], groups({1: [(Q(1), Q(1))]})
    monkeypatch.setattr(
        control,
        "intake",
        lambda *_: (
            {"cells": {"0": rs}, "groups": gs, "mask": list(range(17))},
            {"synthetic": True},
            0,
            [],
        ),
    )
    descriptor = {"synthetic": True}
    certificate = control.generate(descriptor, deadline=deadline())
    assert control.check(descriptor, certificate, deadline=deadline())["verification_passed"]
    for key in ("constants", "cases", "guard", "conditional_I_exclusion_proved"):
        bad = copy.deepcopy(certificate)
        bad[key] = None
        with pytest.raises(ValueError, match="reconstruction differs"):
            control.check(descriptor, bad, deadline=deadline())


def test_clean_cli_generation_and_fresh_roundtrip(tmp_path: Path) -> None:
    # Controlled accepted-premise stub, injected in two independent processes.
    # All construction/serialization/import checks run in the real CLI.
    source = tmp_path / "synthetic.json"
    source.write_text(
        json.dumps({"rows": [row([[(Q(1), Q(1))]])], "groups": groups({1: [(Q(1), Q(1))]})})
    )
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text('{"synthetic":true}')
    certificate, replay = tmp_path / "certificate.json", tmp_path / "replay.json"
    script = "\n".join(  # noqa: FLY002
        [
            "import json,sys",
            "from pathlib import Path",
            "from devtools import probe_n17_conditional_center_cases as c",
            "data=json.loads(Path(sys.argv[1]).read_text())",
            (
                "c.intake=lambda *_: ({'cells':{'0':data['rows']},"
                "'groups':data['groups'],'mask':list(range(17))},"
                "{'synthetic_accepted_premise':True},0,[])"
            ),
            "raise SystemExit(c.main(sys.argv[2:]))",
        ]
    )
    for output, extra in ((certificate, []), (replay, ["--certificate", str(certificate)])):
        run = subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                str(source),
                "--descriptor",
                str(descriptor),
                "--output",
                str(output),
                *extra,
            ],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        assert run.returncode == 0, run.stderr
    a, b = json.loads(certificate.read_text()), json.loads(replay.read_text())
    assert a["conditional_I_exclusion_proved"]
    assert b["verification_passed"]
    assert all(
        not b[k]
        for k in (
            "unconditional_exclusion_proved",
            "census_admission_proved",
            "global_optimality_proved",
            "root_checked_now",
        )
    )


def pool_fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Real native-shaped canonical gzip stream, with a controlled accepted premise."""
    monkeypatch.setattr(control.finite, "REPO", tmp_path)
    initial_groups = groups({0: [(Q(1), Q(1))], 1: [(Q(3), Q(3))]})
    seed = {"groups": initial_groups}
    order = [o for o in range(1, 17) if o != 12] + [0]
    final_groups = copy.deepcopy(initial_groups)
    final_groups["0"] = [["11/10", "1"]]
    cells = {}
    for owner in range(17):
        n = 32 if owner == 12 else 64
        cells[str(owner)] = [
            {
                "interval": [str(Q(i, n)), str(Q(i + 1, n))],
                "reference": {"kind": "wall_seed", "owner": owner, "row": i},
                "outer_domain": [],
                "residual_polygons": [],
            }
            for i in range(n)
        ]
    final = {
        "mask": list(range(17)),
        "mask_index": None,
        "U": str(control.U),
        "B": "1",
        "world": [],
        "cells": cells,
        "groups": final_groups,
    }
    steps = [
        {
            "index": si,
            "owner": owner,
            "complete": True,
            "common_owned_kernel": [["11/10", "1"]]
            if owner == 0
            else copy.deepcopy(initial_groups[str(owner)]),
        }
        for si, owner in enumerate(order)
    ]
    node = {
        "schema": "exact_generic_owned_hull_v1",
        "initial": {
            "groups": initial_groups,
            "cell_references": {
                str(o): [r["reference"] for r in cells[str(o)]] for o in range(17)
            },
        },
        "source": {"sha256": control.finite.identity(seed)},
        "parent": None,
        "guard_source": None,
        "constraints": [],
        "mask": list(range(17)),
        "closed": False,
        "contradiction": None,
        "final_state": final,
        "steps": steps,
    }
    node_path = tmp_path / "provisional.gz"
    node_path.write_bytes(gzip.compress(json.dumps(node, sort_keys=True).encode()))
    stream = control.finite.BoundedNode(node_path, deadline())
    assert len(list(stream.steps())) == 16
    node_id = stream.sha256
    assert node_id is not None
    node_path.rename(tmp_path / f"node-{node_id}.json.gz")
    seed_id = control.finite.identity(seed)
    (tmp_path / f"seed-{seed_id}.json.gz").write_bytes(gzip.compress(json.dumps(seed).encode()))
    selected = [["1", "1"], ["11/10", "9/10"], ["6/5", "1"], ["11/10", "11/10"], ["1", "21/20"]]
    initial = copy.deepcopy(final)
    initial["groups"]["0"] = control.finite.serial(
        control.bounded_hull(
            [(Q(x), Q(y)) for x, y in final_groups["0"] + selected], 128, deadline()
        )
    )
    prepared = {
        "initial_state": initial,
        "guard_source": {"point_origins": {"old": final_groups["0"], "selected": selected}},
    }
    gate = {"saved_objects": ".", "seed_sha256": seed_id, "node_sha256": node_id}
    accepted = {"custody": {"parent_replay": {"mask": list(range(17)), "step_owners": order}}}
    monkeypatch.setattr(control.finite, "accepted_receipt", lambda *_: (b"synthetic", accepted))
    return gate, prepared, node


def test_native_pool_stream_origins_final_containment_and_coarse_rows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate, prepared, _ = pool_fixture(tmp_path, monkeypatch)
    state, evidence, count, selected = control.pool_original(gate, prepared, deadline())
    assert evidence["raw_counts"]["1"] == 2
    assert len(evidence["origins"]["1"]) == 1
    assert evidence["origins"]["1"][0]["origin"]["kind"] == "initial_group"
    assert evidence["origins"]["0"][1]["origin"] == {
        "kind": "common_owned_kernel",
        "step": 15,
        "owner": 0,
        "point_index": 0,
        "jsonpath": "$.steps[15].common_owned_kernel",
    }
    assert evidence["original_final_contained"] is True
    assert evidence["unconditional_parent_pools_disjoint"] is True
    assert count > evidence["raw_total"]
    assert len(selected) == 5
    control.validate_state(state, {"cells": []}, list(range(17)), 12)
    bad = copy.deepcopy(state)
    bad["cells"]["12"][0]["reference"]["owner"] = 13
    with pytest.raises(ValueError, match="wall seed owner"):
        control.validate_state(bad, {"cells": []}, list(range(17)), 12)


@pytest.mark.parametrize("cap", ["RAW_POOL_OWNER_LIMIT", "RAW_POOL_LIMIT", "POOL_LIMIT"])
def test_pool_caps_incomplete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cap: str
) -> None:
    gate, prepared, _ = pool_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(control, cap, 1)
    with pytest.raises(control.IncompleteError, match=r"pool|vertex"):
        control.pool_original(gate, prepared, deadline())


def test_matched_unpooled_precedes_recovered_pool_closure() -> None:
    p = (Q(1), Q(1))
    pooled = groups({0: [p], 1: [p]})
    rows = [row([[(Q(3), Q(3))]])]
    result = control.construct(
        rows, pooled, unpooled_groups=groups({0: [p], 1: [p]}), deadline=deadline()
    )
    assert result["unsplit"]["status"] == "conditional_unpooled_intersection"
    assert result["compression_information_recovered"] is False
    result = control.construct(
        rows, pooled, unpooled_groups=groups({0: [p]}), deadline=deadline()
    )
    assert result["unsplit"]["status"] == "conditional_pooled_intersection"
    assert result["compression_information_recovered"] is True


def test_earlier_proofs_skip_unused_centers_and_midrange(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    p = (Q(1), Q(1))
    bad = row([[p]])
    bad["residual_polygons"][0][0][0] = str(1 << 4097)
    result = control.construct([bad], groups({0: [p], 1: [p]}), deadline=deadline())
    assert result["conditional_I_exclusion_proved"] is True
    assert result["alpha"] is None
    assert result["beta"] is None
    original = control.checked

    def refuse_midrange(value: Q) -> Q:
        if value == 2:
            raise AssertionError("unnecessary midrange sum")
        return original(value)

    monkeypatch.setattr(control, "checked", refuse_midrange)
    result = control.construct([row([[p]])], groups({1: [p]}), deadline=deadline())
    assert result["unsplit"]["status"] == "shared_owned_point"
    assert result["alpha"] is None


def test_pool_unconditional_intersection_refused_before_five(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate, prepared, node = pool_fixture(tmp_path, monkeypatch)
    node["steps"][0]["common_owned_kernel"] = [["1", "1"]]
    provisional = tmp_path / "changed.gz"
    provisional.write_bytes(gzip.compress(json.dumps(node, sort_keys=True).encode()))
    stream = control.finite.BoundedNode(provisional, deadline())
    assert len(list(stream.steps())) == 16
    gate["node_sha256"] = stream.sha256
    provisional.rename(tmp_path / f"node-{stream.sha256}.json.gz")
    with pytest.raises(ValueError, match="unconditional original pool"):
        control.pool_original(gate, prepared, deadline())


def test_pool_identity_and_truncation_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate, prepared, _ = pool_fixture(tmp_path, monkeypatch)
    old = gate["node_sha256"]
    path = tmp_path / f"node-{old}.json.gz"
    gate["node_sha256"] = "bad"
    path.rename(tmp_path / "node-bad.json.gz")
    with pytest.raises(ValueError, match="canonical EOF"):
        control.pool_original(gate, prepared, deadline())
    bad = tmp_path / "node-bad.json.gz"
    bad.write_bytes(bad.read_bytes()[:20])
    with pytest.raises((EOFError, OSError, ValueError), match=r".+"):
        control.pool_original(gate, prepared, deadline())


def test_cli_truncated_premise_retains_refusal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    descriptor, output = tmp_path / "descriptor.json", tmp_path / "result.json"
    descriptor.write_text("{}")

    def truncated(*_args: Any) -> Any:
        raise EOFError("truncated canonical gzip premise")

    monkeypatch.setattr(control, "intake", truncated)
    assert control.main(["--descriptor", str(descriptor), "--output", str(output)]) == 1
    result = json.loads(output.read_text())
    assert result["status"] == "refused"
    assert result["conditional_I_exclusion_proved"] is False


def test_accepted_receipt_bytes_and_ceiling(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(control.finite, "REPO", tmp_path)
    path = tmp_path / "receipt.json"
    path.write_text('{"test":"synthetic"}')
    with pytest.raises(ValueError, match="byte identity"):
        control.read_premise("receipt.json", "wrong", {}, deadline())
    monkeypatch.setattr(control, "JSON_LIMIT", 5)
    with pytest.raises(control.IncompleteError, match="byte ceiling"):
        control.read_premise("receipt.json", "wrong", {}, deadline())
