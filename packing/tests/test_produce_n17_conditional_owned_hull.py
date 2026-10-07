"""Synthetic conditional-state plumbing; no actual parent geometry is evaluated."""

from __future__ import annotations

import copy
import gzip
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest

from devtools import produce_n17_conditional_owned_hull as control
from devtools.verify_n17_conditional_owned_hull import ChildStream
from sqpack.hull_kernel.geometry import IncompleteError, RefusalError


def prepared() -> dict[str, Any]:
    mask = list(range(17))
    return {
        "parent": {"node_sha256": "parent-content", "accepted_h290": "receipt"},
        "guard_source": {"finite_certificate": "finite-content", "fresh_receipt": "fresh"},
        "constraints": [copy.deepcopy(control.GUARD)],
        "frame": {"U": "1169/250", "B": "1", "cells": []},
        "initial_state": {
            "mask": mask,
            "cells": {
                str(owner): [
                    {
                        "interval": ["0", "1"],
                        "reference": {"owner": owner},
                        "outer_domain": [],
                        "residual_polygons": [],
                    }
                ]
                for owner in mask
            },
            "groups": {str(owner): [] for owner in mask},
        },
        "custody": {
            "label_to_owner": {"6": 6},
            "parent_step_owners": [o for o in mask if o != 6],
        },
    }


def install_engine(
    monkeypatch: pytest.MonkeyPatch, *, failure: str | None = None
) -> list[dict[str, Any]]:
    seen: list[dict[str, Any]] = []
    monkeypatch.setattr(control, "initial_closure", lambda _: None)
    monkeypatch.setattr(control, "guard_closure", lambda _rows, _step: None)
    monkeypatch.setattr(
        control,
        "read_frame",
        lambda _: SimpleNamespace(
            cell_names=["corner-SW"] + [f"side-{i}" for i in range(1, 17)]
        ),
    )

    def step(_frame: Any, **kwargs: Any) -> tuple[Any, Any, Any]:
        seen.append(kwargs)
        if failure == "incomplete" or (failure == "afterfirst" and len(seen) == 2):
            raise IncompleteError("synthetic ceiling")
        owner = kwargs["owner"]
        record = {
            "owner": owner,
            "index": kwargs["step_index"],
            "allowed_half_angle": ["0", "1"],
            "complete": True,
            "rows": copy.deepcopy(kwargs["rows"][owner]),
        }
        return record, {"splits": 1 if failure == "split" else 0}, record["rows"]

    def certify(
        _frame: Any, step: Any, _groups: Any, rows: Any, **_kwargs: Any
    ) -> dict[str, Any]:
        if failure == "refused":
            rows[step["owner"]] = []
            raise RefusalError("synthetic row refusal")
        if failure == "coarse":
            rows[6] = []
        if failure == "partner":
            rows[2] = []
        if failure == "agreement":
            rows[step["owner"]] = []
        if failure == "partition":
            rows[step["owner"]][0]["interval"] = ["0", "1/2"]
        if failure == "hull":
            _groups[step["owner"]] = [(control.Q(i), control.Q(i * i)) for i in range(49)]
        return {
            "closure": {"kind": "all_parent_poses_forbidden", "owner": step["owner"], "step": 0}
            if failure == "closure"
            else None,
            "checked_rows": 1,
        }

    monkeypatch.setattr(control.pilot, "produce_step", step)
    monkeypatch.setattr(control.pilot, "certify_step", certify)
    return seen


def test_full_round_preserves_guard_parent_rows_and_coarse(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = prepared()
    before = copy.deepcopy(source)
    seen = install_engine(monkeypatch)
    result = control.produce(source, deadline=time.monotonic() + 10)
    assert source == before
    assert result["complete_round"]
    assert result["completed_owner_count"] == 16
    assert result["owner_order"] == list(range(1, 6)) + list(range(7, 17)) + [0]
    assert all(
        call["max_live"] == 0 and call["hull_limit"] == 48 and call["core_kind"] == "octagon"
        for call in seen
    )
    child = result["child"]
    assert child["schema"] == control.CHILD_SCHEMA
    assert child["initial"] == source["initial_state"]
    assert child["parent"] == child["final_state"]["parent"] == source["parent"]
    assert child["constraints"] == child["final_state"]["constraints"] == [control.GUARD]
    assert child["guard_source"] == source["guard_source"]
    assert child["final_state"]["cells"]["6"] == source["initial_state"]["cells"]["6"]
    assert result["endpoint_monitor_used"] is False
    assert result["fresh_conditional_replay_required"] is True
    assert result["conditional_exclusion_proved"] is False


@pytest.mark.parametrize(
    ("failure", "status"),
    [
        ("incomplete", "incomplete"),
        ("refused", "refused"),
        ("coarse", "refused"),
        ("agreement", "refused"),
        ("split", "refused"),
        ("partition", "refused"),
        ("hull", "refused"),
        ("partner", "refused"),
    ],
)
def test_failed_update_preserves_last_certified_state(
    monkeypatch: pytest.MonkeyPatch, failure: str, status: str
) -> None:
    source = prepared()
    install_engine(monkeypatch, failure=failure)
    result = control.produce(source, deadline=time.monotonic() + 10)
    assert result["status"] == status
    assert result["completed_owner_count"] == 0
    assert result["child"]["final_state"]["cells"] == source["initial_state"]["cells"]
    assert result["child"]["closed"] is False


def test_closure_is_only_a_production_candidate(monkeypatch: pytest.MonkeyPatch) -> None:
    install_engine(monkeypatch, failure="closure")
    result = control.produce(prepared(), deadline=time.monotonic() + 10)
    assert result["status"] == "production_closed_candidate"
    assert result["completed_owner_count"] == 1
    assert not result["complete_round"]
    assert result["child"]["closed"] is True
    assert result["child"]["conditional_exclusion_proved"] is False


@pytest.mark.parametrize(("shift", "overlap"), [("1/2", True), ("1", True), ("2", False)])
def test_initial_exact_cross_touch_and_disjoint(shift: str, *, overlap: bool) -> None:
    q = control.Q
    first = [(q(0), q(0)), (q(1), q(0)), (q(1), q(1)), (q(0), q(1))]
    second = [(x + q(shift), y) for x, y in first]
    found = control.initial_closure({7: second, 2: first, 0: []})
    assert bool(found) is overlap
    if found:
        assert found["owners"] == [2, 7]
        assert found["step"] == -1
        assert found["intersection"]


def test_initial_corner_touch_and_degenerate() -> None:
    q = control.Q
    first = [(q(0), q(0)), (q(1), q(0)), (q(1), q(1)), (q(0), q(1))]
    second = [(x + 1, y + 1) for x, y in first]
    found = control.initial_closure({0: first, 1: second})
    assert found is not None
    assert found["intersection"] == [["1", "1"]]
    found = control.initial_closure({0: first, 1: [(q(1), q(1))]})
    assert found is not None
    assert found["intersection"] == [["1", "1"]]


def test_initial_closure_calls_no_producer(monkeypatch: pytest.MonkeyPatch) -> None:
    original = control.initial_closure
    seen = install_engine(monkeypatch)
    monkeypatch.setattr(control, "initial_closure", original)
    source = prepared()
    square = [["0", "0"], ["1", "0"], ["1", "1"], ["0", "1"]]
    source["initial_state"]["groups"]["1"] = square
    source["initial_state"]["groups"]["2"] = square
    result = control.produce(source, deadline=time.monotonic() + 10)
    assert seen == []
    assert result["completed_owner_count"] == 0
    assert result["child"]["contradiction"]["step"] == -1
    assert result["status"] == "production_closed_candidate"


def test_off_grid_compression_has_exact_barycentric_witnesses() -> None:
    q = control.Q
    original = [(q(1, 3), q(1, 3)), (q(4, 3), q(1, 3)), (q(4, 3), q(4, 3)), (q(1, 3), q(4, 3))]
    selected, witnesses = control.pilot.producer.compress(original)
    assert selected != original
    step = {
        "compression_source_hull": control.encode(original),
        "inner_grid_compression": {
            "vertices": control.encode(selected),
            "witnesses": witnesses,
            "denominator": control.pilot.producer.GRID,
            "original_vertices": len(original),
            "retained_vertices": len(selected),
        },
    }
    assert control.node.compression_points(step, original, []) == selected
    step["inner_grid_compression"]["witnesses"][0]["weights"][0] = "0"
    with pytest.raises(RefusalError):
        control.node.compression_points(step, original, [])


def test_expired_budget_never_calls_producer(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = install_engine(monkeypatch)
    result = control.produce(prepared(), deadline=time.monotonic() - 1)
    assert result["status"] == "incomplete"
    assert seen == []


def test_ceiling_after_one_update_retains_certified_prefix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = prepared()
    seen = install_engine(monkeypatch, failure="afterfirst")
    result = control.produce(source, deadline=time.monotonic() + 10)
    assert len(seen) == 2
    assert result["status"] == "incomplete"
    assert result["completed_owner_count"] == 1
    assert result["child"]["steps"][0]["owner"] == 1
    assert len(result["child"]["steps"]) == 1
    assert result["child"]["initial"] == source["initial_state"]
    assert result["child"]["parent"] == source["parent"]
    assert result["child"]["closed"] is False
    assert result["conditional_exclusion_proved"] is False


def test_initial_scan_ceiling_never_promotes_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = install_engine(monkeypatch)
    expired = False

    def propose(_groups: Any) -> Any:
        nonlocal expired
        expired = True
        return {
            "kind": "owned_hulls_intersect",
            "owners": [1, 2],
            "step": -1,
            "intersection": [["1", "1"]],
        }

    monkeypatch.setattr(control, "initial_closure", propose)
    monkeypatch.setattr(control.time, "monotonic", lambda: 20.0 if expired else 0.0)
    result = control.produce(prepared(), deadline=10)
    assert result["status"] == "incomplete"
    assert result["child"]["closed"] is False
    assert result["child"]["contradiction"] is None
    assert seen == []


@pytest.mark.parametrize("live", [25, 26, 27, None])
def test_closed_guard_terminal_includes_both_boundary_neighbors(
    monkeypatch: pytest.MonkeyPatch,
    live: int | None,
) -> None:
    original = control.guard_closure
    install_engine(monkeypatch)
    monkeypatch.setattr(control, "guard_closure", original)
    source = prepared()
    q = control.Q
    source["initial_state"]["cells"]["0"] = [
        {
            "interval": [str(q(i, 64)), str(q(i + 1, 64))],
            "reference": {"row": i},
            "outer_domain": [],
            "residual_polygons": [[["1", "1"]]] if i not in (25, 26, 27) or i == live else [],
        }
        for i in range(64)
    ]
    result = control.produce(source, deadline=time.monotonic() + 10)
    assert result["completed_owner_count"] == 16
    if live is None:
        assert result["status"] == "production_closed_candidate"
        assert result["child"]["contradiction"]["row_indices"] == [25, 26, 27]
        assert result["child"]["contradiction"]["step"] == 15
        assert result["child"]["contradiction"]["kind"] == "guarded_owner_cover_empty"
    else:
        assert result["status"] == "production_stall_candidate"
        assert result["child"]["closed"] is False
    assert result["conditional_exclusion_proved"] is False


@pytest.mark.parametrize("field", ["parent", "guard_source", "constraints"])
def test_missing_conditional_premise_refuses(
    monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    install_engine(monkeypatch)
    source = prepared()
    source[field] = [] if field == "constraints" else None
    with pytest.raises(RefusalError):
        control.produce(source, deadline=time.monotonic() + 10)


def test_generic_root_admission_refuses_conditional_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    install_engine(monkeypatch)
    source = prepared()
    child = control.produce(source, deadline=time.monotonic() + 10)["child"]
    frame = SimpleNamespace(cells=list(range(17)))
    seed = SimpleNamespace(groups={}, rows={})
    with pytest.raises(RefusalError, match="wrong terminal schema"):
        control.node.admit_header(
            cast(Any, frame), child, cast(Any, seed), mask=list(range(17)), seed_sha256="unused"
        )


def test_cli_retains_compressed_child_with_content_identity(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    install_engine(monkeypatch)
    source = prepared()
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps({"schema": control.DESCRIPTOR_SCHEMA}))
    checker = SimpleNamespace(
        IncompleteError=IncompleteError,
        read_json=lambda path: (path.read_bytes(), json.loads(path.read_bytes())),
        prepare=lambda _doc, **_kwargs: copy.deepcopy(source),
        initial_closure=lambda _: None,
    )
    monkeypatch.setattr(control, "import_module", lambda _: checker)
    output, child = tmp_path / "receipt.json", tmp_path / "child.json.gz"
    assert (
        control.main(
            [
                "--descriptor",
                str(descriptor),
                "--max-seconds",
                "10",
                "--output",
                str(output),
                "--child-output",
                str(child),
            ]
        )
        == 0
    )
    report = json.loads(output.read_text())
    native = json.loads(gzip.decompress(child.read_bytes()))
    assert report["child_object"]["canonical_sha256"] == control.identity(native)
    assert report["conditional_exclusion_proved"] is False
    assert report["invocation"]["interpreter"] == sys.executable
    stream = ChildStream(child, time.monotonic() + 10)
    assert list(stream.steps()) == native["steps"]
    assert stream.sha256 == control.identity(native)
    assert stream.header["final_state"] == native["final_state"]


def test_cli_bad_descriptor_retains_refused_report(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    checker = SimpleNamespace(IncompleteError=IncompleteError)

    def refused(_path: Path) -> Any:
        raise ValueError("synthetic malformed descriptor")

    checker.read_json = refused
    monkeypatch.setattr(control, "import_module", lambda _: checker)
    output = tmp_path / "refused.json"
    assert (
        control.main(
            [
                "--descriptor",
                "unused",
                "--max-seconds",
                "1",
                "--output",
                str(output),
                "--child-output",
                str(tmp_path / "unused.gz"),
            ]
        )
        == 1
    )
    report = json.loads(output.read_text())
    assert report["status"] == "refused"
    assert report["conditional_exclusion_proved"] is False


def test_child_compressed_and_decoded_limits_are_separate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert control.CHILD_DECODED_LIMIT == 512 << 20
    assert control.CHILD_COMPRESSED_LIMIT == 64 << 20
    assert control.REPORT_LIMIT == 64 << 20
    monkeypatch.setattr(control, "CHILD_DECODED_LIMIT", 8)
    monkeypatch.setattr(control, "CHILD_COMPRESSED_LIMIT", 4)
    control.output_within(b"12345678")
    control.compressed_within(b"1234")
    with pytest.raises(IncompleteError, match="decoded"):
        control.output_within(b"123456789")
    with pytest.raises(IncompleteError, match="compressed"):
        control.compressed_within(b"12345")


@pytest.mark.parametrize("seconds", ["0", "-1", "nan", "inf"])
def test_cli_invalid_ceiling_refuses(seconds: str, tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        control.main(
            [
                "--descriptor",
                "unused",
                "--max-seconds",
                seconds,
                "--output",
                str(tmp_path / "unused"),
                "--child-output",
                str(tmp_path / "unused.gz"),
            ]
        )
