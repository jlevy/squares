"""Synthetic conditional ancestry and exact full replay; no scientific inputs."""

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

from devtools import verify_n17_conditional_owned_hull as control

Q = control.Q


def fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    mask = list(range(17))
    frame = {
        "U": str(control.finite.U),
        "B": "1",
        "capture_cap": str(control.finite.V),
        "cells": [[["0", "0"], ["1", "0"], ["1", "1"], ["0", "1"]] for _ in range(24)],
    }
    initial = {
        "schema": control.INITIAL_SCHEMA,
        "U": frame["U"],
        "B": "1",
        "mask_index": None,
        "mask": mask,
        "world": frame["cells"],
        "source": {"sha256": "accepted-parent-seed"},
        "guard": copy.deepcopy(control.GUARD),
        "constraints": [copy.deepcopy(control.GUARD)],
        "groups": {str(o): [] for o in mask},
        "cells": {},
    }
    for owner in mask:
        count = 32 if owner == 12 else 64
        initial["cells"][str(owner)] = [
            {
                "interval": [str(Q(k, count)), str(Q(k + 1, count))],
                "reference": {"kind": "parent", "node": "parent", "step": owner, "row": k},
                "outer_domain": [],
                "residual_polygons": [],
            }
            for k in range(count)
        ]
    prepared = {
        "frame": frame,
        "initial_state": initial,
        "parent": {"node_sha256": "accepted-parent"},
        "guard_source": {"certificate_sha256": "accepted-finite"},
        "constraints": [copy.deepcopy(control.GUARD)],
        "custody": {
            "label_to_owner": {"6": 12},
            "parent_step_owners": [o for o in mask if o != 12],
        },
    }
    initial.update(
        parent=copy.deepcopy(prepared["parent"]),
        guard_source=copy.deepcopy(prepared["guard_source"]),
    )
    source = {"conditional_initial_sha256": control.identity(initial)}
    final = copy.deepcopy(initial)
    final["source"] = source
    node = {
        "schema": control.CHILD_SCHEMA,
        "node_id": control.NODE_ID,
        "mask_index": None,
        "mask": mask,
        "U": frame["U"],
        "B": "1",
        "parent": copy.deepcopy(prepared["parent"]),
        "guard_source": copy.deepcopy(prepared["guard_source"]),
        "constraints": copy.deepcopy(prepared["constraints"]),
        "source": source,
        "initial": copy.deepcopy(initial),
        "steps": [],
        "final_state": final,
        "contradiction": None,
        "closed": False,
        "terminal": False,
        "mask_exclusion_proved": False,
        "conditional_exclusion_proved": False,
        "global_optimality_proved": False,
        "census_admission_proved": False,
    }
    return prepared, node


def check(tmp_path: Path, prepared: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
    path = tmp_path / "child.json.gz"
    path.write_bytes(gzip.compress(control.finite.canonical(node), mtime=0))
    return control.replay(
        prepared,
        control.finite.BoundedNode(path, time.monotonic() + 10),
        deadline=time.monotonic() + 10,
    )


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ([(0, 0)], [(0, 0)], [(0, 0)]),
        ([(0, 0), (2, 0)], [(1, 0), (3, 0)], [(1, 0), (2, 0)]),
        ([(0, 0), (2, 2)], [(0, 2), (2, 0)], [(1, 1)]),
        ([(0, 0), (1, 0), (1, 1), (0, 1)], [(1, 1), (2, 1), (2, 2), (1, 2)], [(1, 1)]),
        ([], [(0, 0)], []),
        ([(0, 0), (1, 0)], [(2, 0), (3, 0)], []),
    ],
)
def test_closed_all_dimensional_intersection(first: Any, second: Any, expected: Any) -> None:
    def points(seq):
        return [(Q(x), Q(y)) for x, y in seq]

    assert control.intersection(points(first), points(second)) == points(expected)


def test_initial_touch_is_checked_conditional_only(tmp_path: Path) -> None:
    prepared, node = fixture()
    for value in (prepared["initial_state"], node["initial"], node["final_state"]):
        value["groups"]["0"] = [["0", "0"]]
        value["groups"]["1"] = [["0", "0"]]
    source = {"conditional_initial_sha256": control.identity(prepared["initial_state"])}
    node["source"] = node["final_state"]["source"] = source
    node["contradiction"] = control.initial_closure(control.state_from(prepared).groups)
    node["closed"] = node["terminal"] = True
    result = check(tmp_path, prepared, node)
    assert result["status"] == "PASS_CONDITIONAL_CLOSED"
    assert result["closure"]["step"] == -1
    assert result["steps_checked"] == 0
    assert result["conditional_exclusion_proved"]
    assert not result["mask_exclusion_proved"]
    assert not result["existing_U_census_admission"]


def update(prepared: dict[str, Any], node: dict[str, Any]) -> None:
    owner = 1
    rows = []
    for k, prior in enumerate(prepared["initial_state"]["cells"][str(owner)]):
        rows.append(
            {
                **copy.deepcopy(prior),
                "prior_reference": prior["reference"],
                "reference": {"kind": "phase3", "node": control.NODE_ID, "step": 0, "row": k},
                "collision_regions": [],
                "common_core_halfplanes": [],
                "outer_bounds": [],
            }
        )
    node["steps"] = [
        {
            "owner": owner,
            "index": 0,
            "complete": True,
            "allowed_half_angle": ["0", "1"],
            "rows": rows,
            "prior_owned_hulls": copy.deepcopy(prepared["initial_state"]["groups"]),
            "prior_partner_pose_covers": {},
            "common_owned_kernel": [],
        }
    ]
    node["final_state"]["cells"][str(owner)] = copy.deepcopy(rows)
    node["contradiction"] = {"kind": "all_parent_poses_forbidden", "owner": owner, "step": 0}
    node["closed"] = node["terminal"] = True


def test_actual_standing_full_dead_row_update(tmp_path: Path) -> None:
    prepared, node = fixture()
    update(prepared, node)
    result = check(tmp_path, prepared, node)
    assert result["status"] == "PASS_CONDITIONAL_CLOSED"
    assert result["steps_checked"] == 1
    assert result["counts"]["steps"] == 1
    assert result["final_state_equal"]


@pytest.mark.parametrize(
    "mutation",
    [
        "guard",
        "parent",
        "initial",
        "source",
        "finalinterval",
        "pair",
        "afterclosure",
        "owner",
        "refine",
        "prior",
        "claimed",
    ],
)
def test_custody_or_full_replay_mutations_refused(tmp_path: Path, mutation: str) -> None:
    prepared, node = fixture()
    update(prepared, node)
    if mutation == "guard":
        node["constraints"] = []
    elif mutation == "parent":
        node["parent"]["node_sha256"] = "foreign"
    elif mutation == "initial":
        node["initial"]["groups"]["2"] = [["0", "0"]]
    elif mutation == "source":
        node["source"] = {"sha256": "generic-seed"}
    elif mutation == "finalinterval":
        node["final_state"]["cells"]["0"][0]["interval"][0] = "1/2"
    elif mutation == "pair":
        node["contradiction"] = {"kind": "owned_hulls_intersect", "owners": [2, 3], "step": 0}
    elif mutation == "afterclosure":
        node["steps"].append(copy.deepcopy(node["steps"][0]))
    elif mutation == "owner":
        node["steps"][0]["owner"] = 0
    elif mutation == "refine":
        node["steps"][0]["rows"][0]["interval"][1] = "1/128"
    elif mutation == "prior":
        node["steps"][0]["prior_owned_hulls"]["2"] = [["0", "0"]]
    elif mutation == "claimed":
        node["conditional_exclusion_proved"] = True
    with pytest.raises((ValueError, control.standing.VerificationError)):
        check(tmp_path, prepared, node)


def test_partial_saved_prefix_is_incomplete(tmp_path: Path) -> None:
    prepared, node = fixture()
    result = check(tmp_path, prepared, node)
    assert result["status"] == "INCOMPLETE"
    assert not result["conditional_exclusion_proved"]


def test_deadline_and_truncated_stream(tmp_path: Path) -> None:
    prepared, node = fixture()
    path = tmp_path / "broken.json.gz"
    path.write_bytes(gzip.compress(control.finite.canonical(node)[:-3]))
    with pytest.raises((ValueError, control.standing.VerificationError)):
        control.replay(
            prepared,
            control.finite.BoundedNode(path, time.monotonic() + 10),
            deadline=time.monotonic() + 10,
        )
    with pytest.raises(control.IncompleteError):
        control.finite.BoundedNode(path, time.monotonic() - 1)


def test_clean_cli_refusal_roundtrip_without_scientific_imports(tmp_path: Path) -> None:
    descriptor, output = tmp_path / "context.json", tmp_path / "receipt.json"
    descriptor.write_text(json.dumps({"schema": "generic_wall_seed_v1"}))
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "devtools.verify_n17_conditional_owned_hull",
            "--descriptor",
            str(descriptor),
            "--max-seconds",
            "1",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 1
    receipt = json.loads(output.read_text())
    assert receipt["status"] == "REFUSED"
    assert not receipt["conditional_exclusion_proved"]
    assert "producer/kernel/root import" not in receipt["error"]


@pytest.mark.parametrize("live", [None, 25, 26, 27])
def test_guard_terminal_keeps_both_closed_boundary_rows(live: int | None) -> None:
    prepared, _ = fixture()
    rows = prepared["initial_state"]["cells"]["0"]
    rows[0]["residual_polygons"] = [[["0", "0"]]]
    if live is not None:
        rows[live]["residual_polygons"] = [[["0", "0"]]]
    found = control.guard_closure(rows, 15)
    if live is None:
        assert found is not None
        assert found["row_indices"] == [25, 26, 27]
    else:
        assert found is None


def loader(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    prepared, _ = fixture()
    final = copy.deepcopy(prepared["initial_state"])
    final["groups"]["0"] = [[str(i), str(i * i)] for i in range(20)]
    cert = {
        "variants": {
            "target": {"selected_hull": [[str(i), str(i * i)] for i in range(30, 35)]}
        },
        "endpoint_control": {"strictly_inside": True, "nonempty": True},
    }
    custody = {
        "seed_sha256": "seed",
        "node_sha256": "node",
        "compressed_sha256": {},
        "h290_receipt": "h290.json",
        "h290_receipt_sha256": "h290",
    }
    gate = {
        "frame": prepared["frame"],
        "label_to_owner": {
            str(i): i - 1 if i not in (6, 13) else 12 if i == 6 else 5 for i in range(1, 18)
        },
        "seed_sha256": "seed",
        "node_sha256": "node",
        "saved_objects": "synthetic-parent",
        "compressed_sha256": {
            "synthetic-parent/seed-seed.json.gz": "seed-bytes",
            "synthetic-parent/node-node.json.gz": "node-bytes",
        },
        "h290_receipt_sha256": "h290",
    }
    centered = {
        "schema": "n17-centered-cap-standing-context/v1",
        "status": "centered_stall_control_checked",
        "readiness_passed": True,
        "verification_passed": True,
        "accepted_context": {"accepted_endpoint": {"sha256": "h290"}},
        "fresh_standing": {
            "exit_code": 0,
            "receipt": {
                "schema": "n17-centered-cap-certificate-verification/v1",
                "mode": "full",
                "status": "PASS_STALL",
                "independent_modules": True,
                "root_cap_join_checked": False,
                "owned_hull_limit": 48,
                "container": control.standing.CenteredContainer(
                    control.finite.U, control.finite.V
                ).record(),
                "certificate": {"seed_sha256": "seed", "node_sha256": "node"},
                "compressed_sha256": {"seed": "seed-bytes", "node": "node-bytes"},
                "mask": final["mask"],
                "counts": {"steps": 16},
                "closed": False,
                "closure": None,
            },
        },
    }
    values = {
        "finite_descriptor": gate,
        "finite_certificate": cert,
        "finite_replay": {
            "finite_reconstruction_verified": True,
            "status": "conditional_gain_candidate",
            "certificate_sha256": control.identity(cert),
        },
        "centered_parent_receipt": centered,
    }
    document = {"schema": control.DESCRIPTOR_SCHEMA}
    for key, value in values.items():
        path = tmp_path / (key + ".json")
        path.write_text(json.dumps(value))
        document[key] = path.name
    document["centered_parent_receipt_sha256"] = control.hashlib.sha256(
        (tmp_path / "centered_parent_receipt.json").read_bytes()
    ).hexdigest()
    monkeypatch.setattr(control.finite, "REPO", tmp_path)
    monkeypatch.setattr(
        control.finite,
        "check",
        lambda *_args, **_kwargs: {"status": "conditional_gain_candidate"},
    )
    monkeypatch.setattr(control.finite, "extract", lambda *_args: (final, custody))
    monkeypatch.setattr(
        control.finite,
        "accepted_receipt",
        lambda *_args: (
            b"",
            {
                "custody": {
                    "parent_replay": {"step_owners": prepared["custody"]["parent_step_owners"]}
                }
            },
        ),
    )
    return document, final


def test_preparation_exact_old20_new5_custody_and_no_alias(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    document, final = loader(monkeypatch, tmp_path)
    before = copy.deepcopy(final)
    prepared = control.prepare(document, deadline=time.monotonic() + 10)
    assert final == before
    assert prepared["parent"]["h290_receipt"] == "h290.json"
    assert len(prepared["guard_source"]["point_origins"]["old"]) == 20
    assert len(prepared["guard_source"]["point_origins"]["selected"]) == 5
    for owner in range(1, 17):
        assert prepared["initial_state"]["groups"][str(owner)] == final["groups"][str(owner)]
    assert prepared["initial_state"]["cells"] == final["cells"]
    prepared["constraints"][0]["interval"][0] = "0"
    assert control.GUARD["interval"][0] == "13/32"


@pytest.mark.parametrize(
    "mutation",
    [
        "parentid",
        "sampled",
        "hull",
        "finite",
        "calibration",
        "oldcount",
        "compresseddigest",
        "compressedroles",
    ],
)
def test_preparation_premise_mutations_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, mutation: str
) -> None:
    document, final = loader(monkeypatch, tmp_path)
    field = (
        "finite_replay"
        if mutation == "finite"
        else "finite_certificate"
        if mutation == "calibration"
        else "centered_parent_receipt"
    )
    path = tmp_path / document[field]
    value = json.loads(path.read_text())
    if mutation == "parentid":
        value["fresh_standing"]["receipt"]["certificate"]["node_sha256"] = "foreign"
    elif mutation == "sampled":
        value["fresh_standing"]["receipt"]["mode"] = "sampled"
    elif mutation == "hull":
        value["fresh_standing"]["receipt"]["owned_hull_limit"] = 16
    elif mutation == "finite":
        value["certificate_sha256"] = "stale"
    elif mutation == "calibration":
        value["endpoint_control"]["nonempty"] = False
    elif mutation == "oldcount":
        final["groups"]["0"].pop()
    elif mutation == "compresseddigest":
        value["fresh_standing"]["receipt"]["compressed_sha256"]["seed"] = "foreign-bytes"
    elif mutation == "compressedroles":
        value["fresh_standing"]["receipt"]["compressed_sha256"]["extra"] = "seed-bytes"
    path.write_text(json.dumps(value))
    if field == "centered_parent_receipt":
        document["centered_parent_receipt_sha256"] = control.hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    with pytest.raises(ValueError, match=r"differs|premise|roster"):
        control.prepare(document, deadline=time.monotonic() + 10)


def test_child_decoded_resource_cap_is_separate(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _, node = fixture()
    path = tmp_path / "child.json.gz"
    path.write_bytes(gzip.compress(control.finite.canonical(node)))
    monkeypatch.setattr(control, "CHILD_DECODED_LIMIT", 10)
    with pytest.raises(control.IncompleteError, match="child decoded"):
        control.ChildStream(path, time.monotonic() + 10)


def test_successful_conditional_cli_serializes_own_exact_receipt(tmp_path: Path) -> None:
    prepared, node = fixture()
    update(prepared, node)
    inputs, child, descriptor, output = [
        tmp_path / name
        for name in ("prepared.json", "child.json.gz", "descriptor.json", "receipt.json")
    ]
    inputs.write_text(json.dumps(prepared))
    child.write_bytes(gzip.compress(control.finite.canonical(node)))
    descriptor.write_text(json.dumps({"schema": control.DESCRIPTOR_SCHEMA}))
    code = """import json,sys,time
from pathlib import Path
from devtools import verify_n17_conditional_owned_hull as c
p=json.loads(Path(sys.argv[1]).read_text())
def synthetic(d,*,deadline):
    return c.replay(p,c.ChildStream(Path(sys.argv[2]),deadline),deadline=deadline)
c.consume=synthetic
args=['--descriptor',sys.argv[3],'--max-seconds','10','--output',sys.argv[4]]
raise SystemExit(c.main(args))
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(inputs), str(child), str(descriptor), str(output)],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads(output.read_text())
    assert report["status"] == "PASS_CONDITIONAL_CLOSED"
    assert report["steps_checked"] == 1
    assert report["independent_modules"]
    assert not report["mask_exclusion_proved"]


def test_legacy_generic_frame_refuses_conditional_schema() -> None:
    prepared, node = fixture()
    with pytest.raises(control.standing.VerificationError, match="seed schema"):
        control.standing.check_frame(prepared["initial_state"], node, None)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "raw", [b'{"initial":{"U":1.2},"steps":[]}', b'{"initial":{"U":"1","U":"2"},"steps":[]}']
)
def test_child_nested_duplicate_and_float_refused(tmp_path: Path, raw: bytes) -> None:
    path = tmp_path / "malformed.json.gz"
    path.write_bytes(gzip.compress(raw))
    with pytest.raises(ValueError, match=r"floating|duplicate"):
        control.ChildStream(path, time.monotonic() + 10)


@pytest.mark.parametrize("read_bytes", [64, 1 << 20])
def test_gzip_trailer_eof_retains_cli_refusal_at_initial_or_final_read(
    read_bytes: int, tmp_path: Path
) -> None:
    path = tmp_path / "truncated.json.gz"
    raw = b'{"a":1,"steps":[],"z":"' + b"x" * 256 + b'"}'
    path.write_bytes(gzip.compress(raw)[:-8])
    descriptor, output = tmp_path / "descriptor.json", tmp_path / "receipt.json"
    descriptor.write_text("{}")
    # Keep the production import-purity guard: another test may import the producer
    # into the shared pytest worker before this decoder refusal control runs.
    code = """
import sys
from pathlib import Path
from devtools import verify_n17_conditional_owned_hull as control

control.standing.READ_BYTES = int(sys.argv[1])
path = Path(sys.argv[2])

def consume(_document, *, deadline):
    stream = control.ChildStream(path, deadline)
    list(stream.steps())
    raise AssertionError("truncated child accepted")

control.consume = consume
raise SystemExit(control.main(sys.argv[3:]))
"""
    process = subprocess.run(
        [
            sys.executable,
            "-c",
            code,
            str(read_bytes),
            str(path),
            "--descriptor",
            str(descriptor),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert process.returncode == 1, process.stderr
    report = json.loads(output.read_bytes())
    assert report["status"] == "REFUSED"
    assert "gzip stream is truncated" in report["error"]
    assert "producer/kernel/root import" not in report["error"]
    assert not report["conditional_exclusion_proved"]


@pytest.mark.parametrize("error", [EOFError, RuntimeError])
def test_child_stream_does_not_normalize_non_read_programming_errors(
    error: type[Exception], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "complete.json.gz"
    path.write_bytes(gzip.compress(b'{"steps":[]}'))

    def broken(_deadline: float) -> None:
        raise error("injected non-read failure")

    monkeypatch.setattr(control.finite, "tick", broken)
    with pytest.raises(error, match="injected non-read failure"):
        control.ChildStream(path, time.monotonic() + 10)


def test_expired_after_initial_scan_never_reports_closed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    prepared, node = fixture()
    path = tmp_path / "child.json.gz"
    path.write_bytes(gzip.compress(control.finite.canonical(node)))
    deadline = time.monotonic() + 10
    stream = control.ChildStream(path, deadline)
    real_scan = control.initial_closure

    def expired(groups: dict[int, list[control.Point]]) -> dict[str, Any] | None:
        result = real_scan(groups)
        monkeypatch.setattr(control.finite.time, "monotonic", lambda: deadline + 1)
        return result

    monkeypatch.setattr(control, "initial_closure", expired)
    with pytest.raises(control.IncompleteError, match="wall ceiling"):
        control.replay(prepared, stream, deadline=deadline)


@pytest.mark.parametrize("change", [None, "missing", "extra", "foreign_name", "wrong_digest"])
def test_native_compressed_paths_join_exact_role_roster(change: str | None) -> None:
    gate: dict[str, Any] = {
        "saved_objects": "packing/retained/parent",
        "seed_sha256": "a" * 64,
        "node_sha256": "b" * 64,
    }
    seed = gate["saved_objects"] + "/seed-" + gate["seed_sha256"] + ".json.gz"
    node = gate["saved_objects"] + "/node-" + gate["node_sha256"] + ".json.gz"
    gate["compressed_sha256"] = {seed: "c" * 64, node: "d" * 64}
    expected = {"seed": "c" * 64, "node": "d" * 64}
    if change == "missing":
        del gate["compressed_sha256"][node]
    elif change == "extra":
        gate["compressed_sha256"]["foreign"] = "c" * 64
    elif change == "foreign_name":
        gate["compressed_sha256"][node + ".extra"] = gate["compressed_sha256"].pop(node)
    elif change == "wrong_digest":
        gate["compressed_sha256"][seed] = "e" * 64
    if change in {"missing", "extra", "foreign_name"}:
        with pytest.raises(ValueError, match="path roster"):
            control.parent_compressed_roles(gate)
    else:
        assert (control.parent_compressed_roles(gate) == expected) is (change is None)
