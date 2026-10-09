"""Target-free full-roster endpoint containment and retained-prefix controls."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from devtools import check_n17_endpoint_prefix as control
from sqpack.hull_kernel.frame import Frame, SymmetryAction
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError
from sqpack.hull_kernel.rational import Q


def fixture() -> tuple[Frame, tuple[control.EndpointPose, ...], dict[str, Any]]:
    points = tuple((Q(2 + 2 * (i % 5)), Q(2 + 2 * (i // 5))) for i in range(17))
    frame = Frame(
        "synthetic-seventeen-point-cells",
        Q(12),
        Q(12),
        tuple((point,) for point in points),
        tuple(f"cell{i}" for i in range(17)),
        17,
        (SymmetryAction("r0", (1, 0, 0, 1), tuple(range(17))),),
    )
    poses = tuple(
        control.EndpointPose(
            i + 1,
            i,
            (
                control.Box(Fraction(str(x)), Fraction(str(x))),
                control.Box(Fraction(str(y)), Fraction(str(y))),
            ),
            ((Q(0), Q(0)), (Q(1), Q(1))),
        )
        for i, (x, y) in enumerate(points)
    )
    return frame, poses, {"cells": list(frame.cell_names), "state": list(range(17))}


def first_step() -> dict[str, Any]:
    return {
        "index": 0,
        "owner": 0,
        "complete": True,
        "prior_owned_hulls": {str(i): [] for i in range(17)},
        "rows": [],
    }


def admitted_seed() -> tuple[Any, tuple[control.EndpointPose, ...], dict[str, Any]]:
    frame, poses, _ = fixture()
    seed = control.seed_from_first_step(frame, list(range(17)), first_step())
    accepted = control.node.admit_seed(
        frame,
        seed,
        mask=list(range(17)),
        bins=64,
        budget=Budget(time.monotonic() + 30, 200000),
        allow_empty_groups=True,
    )
    return accepted, poses, seed


def test_full_declared_wall_seed_independently_admits_and_holds_all_seventeen() -> None:
    admitted, poses, seed = admitted_seed()
    result = control.endpoint_check(poses, admitted.rows)
    assert result["held"]
    assert len(result["owners"]) == 17
    assert all(len(rows) == 64 for rows in seed["cells"].values())
    assert seed["cells"]["0"][0]["interval"][0] == "0"
    assert seed["cells"]["0"][-1]["interval"][1] == "1"


def test_declared_seed_domain_mutation_is_refused() -> None:
    frame, _, _ = fixture()
    seed = control.seed_from_first_step(frame, list(range(17)), first_step())
    seed["cells"]["16"][63]["interval"][1] = "999/1000"
    with pytest.raises(RefusalError, match="gap/overlap"):
        control.node.admit_seed(
            frame,
            seed,
            mask=list(range(17)),
            bins=64,
            budget=Budget(time.monotonic() + 30, 200000),
            allow_empty_groups=True,
        )


def test_label_seventeen_loss_is_detected() -> None:
    admitted, poses, _ = admitted_seed()
    admitted.rows[16] = []
    assert control.endpoint_check(poses, admitted.rows)["lost_labels"] == [17]


def test_missing_or_duplicate_label_roster_refused() -> None:
    admitted, poses, _ = admitted_seed()
    for changed in (poses[:-1], (*poses[:-1], replace(poses[-1], label=16))):
        with pytest.raises(RefusalError, match="seventeen"):
            control.endpoint_check(changed, admitted.rows)


def test_full_root_box_needs_one_polygon_and_whole_angle_interval() -> None:
    pose = control.EndpointPose(
        1,
        0,
        (control.Box(Fraction(1), Fraction(2)), control.Box(Fraction(1), Fraction(2))),
        ((Q(1, 4), Q(1, 2)),),
    )
    row = {
        "interval": ["1/4", "1/2"],
        "reference": {"row": 0},
        "residual_polygons": [[["1", "1"], ["2", "1"], ["2", "2"], ["1", "2"]]],
    }
    assert control.endpoint_witness(pose, [row]) is not None
    row["interval"] = ["1/4", "499/1000"]
    assert control.endpoint_witness(pose, [row]) is None
    row["interval"] = ["1/4", "1/2"]
    row["residual_polygons"] = [[["1", "1"]], [["2", "1"]], [["2", "2"]], [["1", "2"]]]
    assert control.endpoint_witness(pose, [row]) is None


def test_exact_quarterturn_endpoint_alternative() -> None:
    _, poses, _ = fixture()
    row = {"interval": ["1", "1"], "reference": {}, "residual_polygons": [[["2", "2"]]]}
    assert control.endpoint_witness(poses[0], [row]) is not None


def install_control(
    monkeypatch: pytest.MonkeyPatch,
    *,
    mutation: str | None = None,
    replay_change: dict[str, Any] | None = None,
) -> list[str]:
    frame, poses, inputs = fixture()
    events: list[str] = []
    monkeypatch.setattr(control, "load_endpoint", lambda: (frame, poses, inputs))

    def certify(
        _frame: Frame, _step: Any, _groups: Any, rows: Any, **kwargs: Any
    ) -> dict[str, Any]:
        events.append("certify")
        assert set(rows) == set(range(17))
        assert all(len(value) == 64 for value in rows.values())
        assert kwargs["mask"] == list(range(17))
        if mutation == "lost":
            rows[16] = []
        if mutation == "refused":
            raise RefusalError("synthetic invalid step")
        return {"checked_rows": 64, "closure": {"owner": 0} if mutation == "closure" else None}

    monkeypatch.setattr(control.pilot, "certify_step", certify)

    def produce(_frame: Frame, mask: Any, **kwargs: Any) -> Any:
        assert mask == list(range(17))
        assert kwargs["bins"] == 64
        assert kwargs["max_rounds"] == 24
        assert kwargs["hull_limit"] == 16
        assert kwargs["core"] == "envelope"
        assert kwargs["collision"] is True
        assert kwargs["split"] == control.producer.SplitPolicy(512, 1152, 1)
        monitor = kwargs["step_log"]
        if mutation == "budget":
            raise IncompleteError("synthetic producer ceiling")
        step = first_step()
        if mutation == "partial":
            step["complete"] = False
        monitor.append(step)
        raise AssertionError("must stop after first complete update")

    monkeypatch.setattr(control.producer, "produce", produce)

    def replay(directory: Path, output: Path, seconds: float) -> dict[str, Any]:
        events.append("replay")
        assert seconds == 60
        seed, saved_node, seed_sha, node_sha = control.saved.load_certificate(directory)
        assert seed["bins"] == 64
        assert saved_node["closed"] is (mutation == "closure")
        assert len(saved_node["steps"]) == 1
        assert saved_node["final_state"]["mask"] == list(range(17))
        receipt = {
            "status": "PASS_SAVED_STALL",
            "producer_imported": False,
            "closure": None,
            "seed_sha256": seed_sha,
            "node_sha256": node_sha,
            "steps_checked": 1,
            "frame": frame.name,
            "cells": list(frame.cell_names),
            "mask": list(range(17)),
            "bins": 64,
            "cover_backend": "indexed",
        }
        receipt.update(replay_change or {})
        output.write_text(json.dumps(receipt))
        return {"exit_code": 0, "receipt": receipt}

    monkeypatch.setattr(control, "fresh_replay", replay)
    return events


def test_complete_first_update_retained_with_all_seventeen_checks(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    events = install_control(monkeypatch)
    result = control.run(tmp_path / "objects")
    assert result["control_passed"]
    assert result["status"] == "PASS_ENDPOINT_PREFIX"
    assert events == ["certify", "replay"]
    assert result["prefix_outcome"] == "declared_update_prefix"
    assert result["complete_owner_updates"] == 1
    assert [item["phase"] for item in result["endpoint_checks"]] == ["seed", "owner_update"]
    assert all(len(item["owners"]) == 17 for item in result["endpoint_checks"])
    assert result["closure"] is None
    assert result["excluded_orbits"] == 0
    assert result["global_admission_proved"] is result["capture_tree_proved"] is False


def test_real_synthetic_owner_update_and_full_saved_state_replay(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Exercise actual producer/row/compression/replay APIs on synthetic point cells.

    The separate-process/no-producer launch contract has its own control below; this
    integration replays directly with the explicit producer-import prohibition disabled.
    """
    frame, poses, inputs = fixture()
    monkeypatch.setattr(control, "load_endpoint", lambda: (frame, poses, inputs))
    replay_receipts = []

    def replay(directory: Path, output: Path, seconds: float) -> dict[str, Any]:
        result = control.saved.check_saved(
            directory, frame, max_seconds=seconds, require_no_producer=False
        )
        assert result["producer_imported"] is True
        replay_receipts.append(result)
        # Simulate only the separately controlled fresh-interpreter absence predicate.
        receipt = {**result, "producer_imported": False}
        output.write_text(json.dumps(receipt))
        return {"exit_code": 0, "receipt": receipt}

    monkeypatch.setattr(control, "fresh_replay", replay)
    result = control.run(tmp_path / "objects", prefix_seconds=30)
    assert result["control_passed"], result
    assert result["complete_owner_updates"] == 1
    assert result["step_checks"][0]["checked_rows"] == 64
    assert replay_receipts[0]["steps_checked"] == 1
    assert replay_receipts[0]["rows_checked"] == 64
    assert replay_receipts[0]["closure"] is None


@pytest.mark.parametrize("mutation", ["lost", "refused", "closure", "partial"])
def test_invalid_or_endpoint_losing_update_never_passes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, mutation: str
) -> None:
    install_control(monkeypatch, mutation=mutation)
    result = control.run(tmp_path / "objects")
    assert not result["control_passed"]
    assert result["status"] == "REFUSED_ENDPOINT_CONTROL"
    assert result["excluded_orbits"] == 0


def test_no_complete_update_is_incomplete_not_endpoint_loss(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    install_control(monkeypatch, mutation="budget")
    result = control.run(tmp_path / "objects")
    assert result["status"] == "INCOMPLETE"
    assert result["endpoint_checks"] == []
    assert result["complete_owner_updates"] == 0


@pytest.mark.parametrize("unobserved", [False, True])
def test_normal_zero_update_time_cap_is_incomplete_but_dropped_observer_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, unobserved: bool
) -> None:
    install_control(monkeypatch)
    monkeypatch.setattr(
        control.producer,
        "produce",
        lambda *_args, **_kwargs: SimpleNamespace(
            outcome="time_cap", node={"steps": [first_step()] if unobserved else []}
        ),
    )
    result = control.run(tmp_path / "objects")
    assert result["status"] == ("REFUSED_ENDPOINT_CONTROL" if unobserved else "INCOMPLETE")
    assert result["control_passed"] is False
    assert result["complete_owner_updates"] == 0


@pytest.mark.parametrize(
    "change",
    [
        {"producer_imported": True},
        {"seed_sha256": "wrong"},
        {"node_sha256": "wrong"},
        {"mask": [0]},
        {"bins": 63},
        {"steps_checked": 0},
        {"frame": "wrong"},
        {"cells": ["cell0"]},
        {"status": "PASS_SAVED_CLOSED"},
        {"cover_backend": "reference"},
        {"status": "REFUSED"},
    ],
)
def test_replay_identity_and_completeness_mutations_do_not_pass(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, change: dict[str, Any]
) -> None:
    install_control(monkeypatch, replay_change=change)
    result = control.run(tmp_path / "objects")
    assert not result["control_passed"]
    assert result["status"] == "REFUSED_ENDPOINT_CONTROL"
    assert result["replay_refused"] is True


@pytest.mark.parametrize("receipt", [False, True])
def test_resource_incomplete_replay_is_not_custody_refusal(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, receipt: bool
) -> None:
    install_control(monkeypatch)
    incomplete = {"receipt": {"status": "INCOMPLETE"}} if receipt else {"status": "INCOMPLETE"}
    monkeypatch.setattr(control, "fresh_replay", lambda *_args: incomplete)
    result = control.run(tmp_path / "objects")
    assert result["status"] == "INCOMPLETE"
    assert result["replay_refused"] is False
    assert result["control_passed"] is False


def test_cli_roundtrip_preserves_inputs_receipts_and_scope(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    install_control(monkeypatch)
    output = tmp_path / "receipt.json"
    assert control.main(["--objects", str(tmp_path / "objects"), "--output", str(output)]) == 0
    result = json.loads(output.read_text())
    assert result["control_passed"]
    assert len(result["endpoint_checks"][0]["owners"]) == 17
    assert result["seed_sha256"] == result["fresh_full_replay"]["receipt"]["seed_sha256"]
    assert result["global_admission_proved"] is result["capture_tree_proved"] is False
    assert result["execution"]["objects"] == str((tmp_path / "objects").resolve())
    assert result["execution"]["output"] == str(output.resolve())


def test_fresh_replay_is_a_separate_full_checker_process(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    output = tmp_path / "fresh.json"

    def execute(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        assert command[:3] == [sys.executable, "-m", "devtools.check_n17_subpattern"]
        assert "--check-saved" in command
        assert "--owners" not in command
        assert kwargs["timeout"] == 60
        assert kwargs["check"] is False
        output.write_text('{"status":"PASS_SAVED_STALL"}')
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(control.subprocess, "run", execute)
    assert control.fresh_replay(tmp_path, output, 60)["receipt"]["status"] == "PASS_SAVED_STALL"


def test_fresh_replay_timeout_keeps_incomplete_status(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def execute(command: list[str], **kwargs: Any) -> Any:
        raise subprocess.TimeoutExpired(command, kwargs["timeout"])

    monkeypatch.setattr(control.subprocess, "run", execute)
    assert control.fresh_replay(tmp_path, tmp_path / "fresh.json", 60)["status"] == "INCOMPLETE"


@pytest.mark.parametrize(
    "kwargs", [{"prefix_seconds": 0}, {"replay_seconds": float("nan")}, {"max_updates": 2}]
)
def test_changed_stop_or_invalid_budget_refused(tmp_path: Path, kwargs: dict[str, Any]) -> None:
    with pytest.raises(RefusalError):
        control.run(tmp_path / "objects", **kwargs)


def test_reused_object_directory_refused(tmp_path: Path) -> None:
    with pytest.raises(RefusalError, match="unique"):
        control.run(tmp_path)
