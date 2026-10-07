"""Target-free centered-context custody, independent replay and resource controls."""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from test_check_n17_capture_checkpoint import context, saved_fixture

from devtools import check_n17_capture_checkpoint as checkpoint
from devtools import check_n17_centered_cap_standing as control


def fixture(tmp_path: Path) -> tuple[dict[str, Any], Path]:
    saved, _seed, node = saved_fixture(tmp_path)
    # The standing verifier requires all eight declared outer support planes.
    # Enclose each unchanged synthetic rectangle without asserting a packing.
    for step in node["steps"]:
        for row in step["rows"]:
            vertices = [(checkpoint.Q(x), checkpoint.Q(y)) for x, y in row["outer_domain"]]
            row["outer_bounds"] = [
                {
                    "normal": [str(a), str(b)],
                    "upper": str(max(a * x + b * y for x, y in vertices)),
                }
                for a, b in (
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1),
                    (1, 1),
                    (-1, 1),
                    (1, -1),
                    (-1, -1),
                )
            ]
    node_path = tmp_path / "objects/node-synthetic.json.gz"
    node_path.write_bytes(gzip.compress(control.canonical(node), mtime=0))
    saved["node_sha256"] = control.identity(node)
    value = context(world=24)
    world = control.world_record(value["base"])
    objects = tmp_path / saved["saved_objects"]
    digests = {
        kind: hashlib.sha256(next(objects.glob(kind + "-*.json.gz")).read_bytes()).hexdigest()
        for kind in ("seed", "node")
    }
    endpoint = {
        "schema": checkpoint.CHECKPOINT_SCHEMA,
        "verification_passed": True,
        "readiness_passed": True,
        "saved_checkpoint_replayed": True,
        "root": value["root"],
        "custody": {
            "parent_replay": {
                "frame": saved["frame"],
                "mask": saved["state"],
                "steps_checked": 16,
                "seed_sha256": saved["seed_sha256"],
                "node_sha256": saved["node_sha256"],
                "closure": None,
            },
            "endpoint_retention": {
                "held": True,
                "lost_labels": [],
                "owners": [
                    {"label": i, "owner": i - 1, "witness": {"synthetic": True}}
                    for i in range(1, 18)
                ],
            },
        },
    }
    endpoint_path = tmp_path / "endpoint.json"
    endpoint_path.write_text(json.dumps(endpoint))
    document = {
        "schema": control.SCHEMA,
        "context": control.context_record(),
        "world": world,
        "world_sha256": control.identity(world),
        "mask": saved["state"],
        "label_to_owner": saved["label_to_owner"],
        "saved_objects": saved["saved_objects"],
        "seed_sha256": saved["seed_sha256"],
        "node_sha256": saved["node_sha256"],
        "compressed_sha256": digests,
        "expected_status": "PASS_STALL",
        "root": value["root"],
        "root_path": "root.json",
        "cap_certificate": "cap.json",
        "endpoint_receipt": "endpoint.json",
        "endpoint_receipt_sha256": hashlib.sha256(endpoint_path.read_bytes()).hexdigest(),
    }
    path = tmp_path / "descriptor.json"
    path.write_text(json.dumps(document))
    return document, path


def test_real_synthetic16_step_relative_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    monkeypatch.setattr(control, "no_science_imports", lambda: None)
    result = control.relative_replay(document, deadline=time.monotonic() + 20)
    assert result["status"] == "PASS_STALL"
    assert result["counts"]["steps"] == 16
    assert result["root_cap_join_checked"] is False
    assert result["centered_exclusion_proved"] is False
    assert result["existing_U_census_admission"] is False


def test_fresh_cli_is_independent_from_root_kernel_and_producer(tmp_path: Path) -> None:
    _document, path = fixture(tmp_path)
    output = tmp_path / "child.json"
    bootstrap = (
        "import sys; from pathlib import Path; "
        "from devtools import check_n17_centered_cap_standing as c; "
        "c.REPO=Path(sys.argv[1]); raise SystemExit(c.main(sys.argv[2:]))"
    )
    command = [
        sys.executable,
        "-c",
        bootstrap,
        str(tmp_path),
        "--relative-child",
        str(path),
        "--max-seconds",
        "20",
        "--output",
        str(output),
    ]
    execution = subprocess.run(command, capture_output=True, timeout=25, check=False)
    assert execution.returncode == 0, execution.stderr.decode() + execution.stdout.decode()
    result = json.loads(output.read_text())
    assert result["independent_modules"] is True
    assert result["counts"]["steps"] == 16
    assert result["world_sha256"] == control.identity(result["world"])
    assert result["root_cap_join_checked"] is False


@pytest.mark.parametrize("mutation", ["offset", "inner", "target", "scale", "mask", "world"])
def test_changed_fixed_context_is_refused(mutation: str, tmp_path: Path) -> None:
    document, _path = fixture(tmp_path)
    if mutation == "mask":
        document["mask"] = document["mask"][:-1]
    elif mutation == "world":
        document["world"]["polygons"][0][0][0] = "2"
    elif mutation == "scale":
        document["world"]["B"] = "2"
    else:
        key = {"offset": "offset", "inner": "inner_V", "target": "target_T"}[mutation]
        document["context"][key] = "0"
    with pytest.raises(ValueError, match=r"differs|identity"):
        control.validate_descriptor(document)


@pytest.mark.parametrize("mutation", ["seed", "node", "compressed"])
def test_changed_saved_identity_is_refused(
    mutation: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    monkeypatch.setattr(control, "no_science_imports", lambda: None)
    if mutation == "compressed":
        document["compressed_sha256"]["node"] = "0" * 64
    else:
        document[mutation + "_sha256"] = "0" * 64
    with pytest.raises(ValueError, match=r"identit"):
        control.relative_replay(document, deadline=time.monotonic() + 20)


@pytest.mark.parametrize("mutation", ["bytes", "lost", "root", "objects", "cap"])
def test_accepted_endpoint_premise_join_refuses_mutation(
    mutation: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    path = tmp_path / "endpoint.json"
    receipt = json.loads(path.read_text())
    if mutation == "lost":
        receipt["custody"]["endpoint_retention"]["held"] = False
    elif mutation == "root":
        receipt["root"] = {}
    elif mutation == "objects":
        receipt["custody"]["parent_replay"]["node_sha256"] = "0" * 64
    elif mutation == "cap":
        receipt["custody"]["parent_replay"]["frame"]["capture_cap"] = str(control.U)
    path.write_text(json.dumps(receipt) + " ")
    if mutation != "bytes":
        document["endpoint_receipt_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match=r"differ|bytes"):
        control.accepted_endpoint(document, document["root"])


def stub_child(document: dict[str, Any]) -> dict[str, Any]:
    return {
        "receipt": {
            "schema": "n17-centered-cap-certificate-verification/v1",
            "container": {k: v for k, v in document["context"].items() if k != "target_T"},
            "root_cap_join_checked": False,
            "counts": {"steps": 16},
            "compressed_sha256": document["compressed_sha256"],
            "context": document["context"],
            "world": document["world"],
            "world_sha256": document["world_sha256"],
            "mask": document["mask"],
            "certificate": {
                "seed_sha256": document["seed_sha256"],
                "node_sha256": document["node_sha256"],
            },
            "mode": "full",
            "status": "PASS_STALL",
            "closed": False,
            "closure": None,
            "centered_exclusion_proved": False,
        }
    }


@pytest.mark.parametrize(
    "outcome",
    [
        "ready",
        "closed",
        "sample",
        "wrong_context",
        "expired",
        "wrong_container",
        "missing_step",
    ],
)
def test_parent_stall_only_semantics_and_child_lease(
    outcome: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    for field in ("root_path", "cap_certificate"):
        (tmp_path / document[field]).write_text("{}")
    joined = {
        "context": document["context"],
        "world_sha256": document["world_sha256"],
        "root_sha256": hashlib.sha256(b"{}").hexdigest(),
        "cap_sha256": hashlib.sha256(b"{}").hexdigest(),
        "accepted_endpoint": {"sha256": document["endpoint_receipt_sha256"]},
    }
    monkeypatch.setattr(control, "accepted_context", lambda *_a, **_k: joined)
    leases = []
    result = stub_child(document)
    if outcome == "closed":
        result["receipt"].update(
            status="PASS_CLOSED",
            closed=True,
            closure={"kind": "closed_owner", "owner": 0, "step": 15},
            centered_exclusion_proved=True,
        )
    elif outcome == "sample":
        result["receipt"]["mode"] = "sample"
    elif outcome == "wrong_context":
        result["receipt"]["context"] = {**document["context"], "offset": "0"}
    elif outcome == "wrong_container":
        result["receipt"]["container"]["offset"] = "0"
    elif outcome == "missing_step":
        result["receipt"]["counts"]["steps"] = 15

    def child(_path: Path, seconds: float) -> dict[str, Any]:
        leases.append(seconds)
        return result

    monkeypatch.setattr(control, "fresh_replay", child)
    deadline = time.monotonic() + 20
    if outcome == "expired":
        monkeypatch.setattr(control.time, "monotonic", lambda: deadline + 1)
        with pytest.raises(control.IncompleteError, match="before independent"):
            control.consume(path, deadline=deadline, child_seconds=300)
        assert leases == []
    elif outcome == "ready":
        report = control.consume(path, deadline=deadline, child_seconds=300)
        assert report["readiness_passed"] is True
        assert 0 < leases[0] < 20
        assert report["existing_U_census_admission"] is False
        assert report["new_target_admission_proved"] is False
        output = tmp_path / "parent.json"
        assert (
            control.main(
                ["--descriptor", str(path), "--max-seconds", "20", "--output", str(output)]
            )
            == 0
        )
        assert json.loads(output.read_text())["root_cap_join_checked"] is True
    else:
        with pytest.raises(ValueError, match=r"differs|unexpectedly closed"):
            control.consume(path, deadline=deadline, child_seconds=300)


def test_gzip_cap_and_truncation_incomplete_or_refused(tmp_path: Path) -> None:
    path = tmp_path / "object.gz"
    path.write_bytes(gzip.compress(b"x" * 100))
    with pytest.raises(control.IncompleteError, match="decoded byte"):
        control.gzip_size(path, 99, time.monotonic() + 5)
    path.write_bytes(path.read_bytes()[:-4])
    with pytest.raises(EOFError):
        control.gzip_size(path, 100, time.monotonic() + 5)


@pytest.mark.parametrize("mutation", ["none", "cells", "actions", "root", "cap"])
def test_parent_fresh_context_binds_original_world_and_endpoint_receipt(
    mutation: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    value = context(world=24)
    monkeypatch.setattr(control, "REPO", tmp_path)
    (tmp_path / "root.json").write_text("{}")
    (tmp_path / "cap.json").write_text("{}")
    cap = SimpleNamespace(
        check=lambda *_: {"verification_passed": True, "cap_certified": mutation != "cap"},
        root_loader=SimpleNamespace(load_root=lambda *_: (value["root"], None, None)),
        exact=SimpleNamespace(
            exact_structure=lambda a, b: control.canonical(a) == control.canonical(b)
        ),
    )
    mask0 = SimpleNamespace(n17_unique_frame=lambda: value["base"])
    monkeypatch.setattr(
        control, "import_module", lambda name: cap if name.endswith("capture_cap") else mask0
    )
    if mutation == "cells":
        document["world"]["polygons"][0][0][0] = "2"
    elif mutation == "actions":
        document["world"]["actions"][0]["matrix"][0] = 0
    elif mutation == "root":
        document["root"] = {}
    document["world_sha256"] = control.identity(document["world"])
    if mutation == "none":
        result = control.accepted_context(document, deadline=time.monotonic() + 10)
        assert result["fresh_cap_check"]["cap_certified"] is True
        assert result["accepted_endpoint"]["sha256"] == document["endpoint_receipt_sha256"]
    else:
        with pytest.raises(ValueError, match=r"differs|refused"):
            control.accepted_context(document, deadline=time.monotonic() + 10)


def test_compressed_object_limit_stays_incomplete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    monkeypatch.setattr(control, "no_science_imports", lambda: None)
    monkeypatch.setattr(control, "SEED_LIMIT", 1)
    with pytest.raises(control.IncompleteError, match="compressed byte ceiling"):
        control.relative_replay(document, deadline=time.monotonic() + 20)


def test_original_saved_bytes_changed_during_standing_replay_refuse(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, _path = fixture(tmp_path)
    monkeypatch.setattr(control, "REPO", tmp_path)
    monkeypatch.setattr(control, "no_science_imports", lambda: None)
    verifier = control.import_module("devtools.verify_n17_kernel_certificate")
    original = verifier.verify

    def changed(*args: Any, **kwargs: Any) -> dict[str, Any]:
        result = original(*args, **kwargs)
        path = next((tmp_path / document["saved_objects"]).glob("node-*.json.gz"))
        path.write_bytes(path.read_bytes() + b"changed")
        return result

    monkeypatch.setattr(verifier, "verify", changed)
    with pytest.raises(ValueError, match="original saved compressed objects changed"):
        control.relative_replay(document, deadline=time.monotonic() + 20)


def test_success_report_byte_limit_becomes_incomplete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        control,
        "consume",
        lambda *_a, **_k: {
            "readiness_passed": True,
            "status": "centered_stall_control_checked",
        },
    )
    monkeypatch.setattr(control, "OUTPUT_LIMIT", 1)
    output = tmp_path / "incomplete.json"
    assert control.main(["--descriptor", "unused", "--output", str(output)]) == 1
    result = json.loads(output.read_text())
    assert result["status"] == "incomplete"
    assert result["readiness_passed"] is False
    assert result["existing_U_census_admission"] is False


@pytest.mark.parametrize("limit", ["nan", "inf", "0", "601"])
def test_invalid_cli_budget_never_reads_input(
    limit: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(control, "consume", lambda *_a, **_k: pytest.fail("input read"))
    output = tmp_path / "refused.json"
    assert (
        control.main(
            ["--descriptor", "unused", "--max-seconds", limit, "--output", str(output)]
        )
        == 1
    )
    assert json.loads(output.read_text())["status"] == "refused"
