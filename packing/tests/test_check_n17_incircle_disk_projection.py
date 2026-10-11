"""Exact disk diagnostics use synthetic projections, never scientific poses."""

from __future__ import annotations

import copy
import itertools
import json
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_incircle_disk_projection as tool


@pytest.mark.parametrize(
    ("point", "inside"),
    [
        (("0", "0"), True),
        (("1", "0"), False),
        (("-1", "0"), False),
        (("0", "1"), False),
        (("3/5", "4/5"), False),
        (("7/10", "7/10"), True),
        (("1", "1"), False),
    ],
)
def test_exact_disk_boundary(point: tuple[str, str], *, inside: bool) -> None:
    work = {"norms_checked": 0}
    result = tool.disk_extremes([list(point)], work, time.monotonic() + 10)
    assert bool(result["strict_disk_extreme_indices"]) is inside
    assert result["whole_difference_in_open_disk"] is inside
    assert work == {"norms_checked": 1}


def test_all_vs_one_segment_and_nonvertex_pitfall() -> None:
    result = tool.disk_extremes(
        [["0", "0"], ["1", "0"]], {"norms_checked": 0}, time.monotonic() + 10
    )
    assert result["strict_disk_extreme_indices"] == [0]
    assert result["whole_difference_in_open_disk"] is False
    outside = tool.disk_extremes(
        [["-1", "0"], ["1", "0"]], {"norms_checked": 0}, time.monotonic() + 10
    )
    assert outside["disk_convexification_redundant"] is True
    with pytest.raises(ValueError, match="canonical"):
        _ = tool.disk_extremes(
            [["-1", "0"], ["0", "0"], ["1", "0"]], {"norms_checked": 0}, time.monotonic() + 10
        )


def setup(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> tuple[Any, Any, Any]:
    document: dict[str, Any] = {"schema": tool.CONTEXT_SCHEMA}
    for role in tool.prior.prior.ROLES:
        p = tmp_path / (role + ".json")
        _ = p.write_text("{}")
        document[role] = str(p)
        document[role + "_sha256"] = "synthetic held by stub"
    base = {
        "complete_classification": True,
        "states_accounted": 95,
        "work": {"state_pairs_accounted": 12920},
        "pairs": [
            {"cells": [0, 1], "difference_hull": [["7/10", "7/10"]]},
            {"cells": [0, 2], "difference_hull": [["0", "0"], ["1", "0"]]},
        ],
        "all95_shared_convexified_relaxations_redundant": True,
        "states": [{"shared_convexified_relaxation_witness_checked": True}],
        **tool.prior.scope(),
    }
    calls = []

    def inherited(d: Any, deadline: float) -> Any:
        tool.tick(deadline)
        assert d["schema"] == tool.prior.prior.CONTEXT_SCHEMA
        calls.append(d)
        held = {Path(d[role]): Path(d[role]).read_bytes() for role in tool.prior.prior.ROLES}
        return [], [], [], {}, held

    monkeypatch.setattr(tool.prior.prior, "intake", inherited)
    monkeypatch.setattr(tool.prior, "construct", lambda *_args, **_kwargs: copy.deepcopy(base))
    return document, base, calls


def test_fresh_geometry_once_norms_and_scope(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    document, _base, calls = setup(monkeypatch, tmp_path)
    result = tool.generate(document, deadline=time.monotonic() + 10)
    fresh = tool.check(document, result, deadline=time.monotonic() + 10)
    assert tool.payload(result) == tool.payload(fresh)
    assert len(calls) == 2
    assert result["criterion_met"] is True
    assert result["disk_work"] == {"norms_checked": 3}
    assert result["ordinary_impossible_pair_candidates"] == [[0, 1]]
    assert result["octagon_all_redundant_diagnostic"] is True
    assert result["all95_shared_convexified_relaxations_redundant"] is False
    assert result["states"][0]["octagon_shared_convexified_relaxation_witness_checked"] is True
    assert result["states"][0]["disk_shared_convexified_relaxation_witness_checked"] is False
    assert "shared_convexified_relaxation_witness_checked" not in result["states"][0]
    assert all(result[k] is False for k in tool.prior.scope() if k != "shared_center_LP_solved")
    changed = copy.deepcopy(result)
    changed["pairs"][0]["norm_squared"] = ["1"]
    with pytest.raises(ValueError, match="fresh"):
        _ = tool.check(document, changed, deadline=time.monotonic() + 10)


def test_redundant_all_boundary_and_full_accounting(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    document, base, _calls = setup(monkeypatch, tmp_path)
    base["pairs"] = [{"cells": [0, 1], "difference_hull": [["-1", "0"], ["1", "0"]]}]
    result = tool.generate(document, deadline=time.monotonic() + 10)
    assert result["criterion_met"] is False
    assert result["all95_shared_convexified_relaxations_redundant"] is True
    base["work"]["state_pairs_accounted"] = 12919
    with pytest.raises(ValueError, match="accounting"):
        _ = tool.generate(document, deadline=time.monotonic() + 10)


def test_caps_deadline_and_used_big_rational(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tool, "NORM_LIMIT", 1)
    with pytest.raises(tool.finite.IncompleteError, match="work ceiling"):
        _ = tool.disk_extremes(
            [["-1", "0"], ["1", "0"]], {"norms_checked": 0}, time.monotonic() + 10
        )
    with pytest.raises(tool.finite.IncompleteError, match="wall"):
        _ = tool.disk_extremes([["0", "0"]], {"norms_checked": 0}, 0)
    with pytest.raises(tool.finite.IncompleteError, match="bit"):
        _ = tool.disk_extremes(
            [[str(1 << 4097), "0"]], {"norms_checked": 0}, time.monotonic() + 10
        )
    assert tool.checked(Q(3, 5) ** 2 + Q(4, 5) ** 2) == 1


def test_postread_change_and_typed_refusals(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    document, _base, _calls = setup(monkeypatch, tmp_path)
    original = tool.disk_extremes

    def changed(raw: Any, work: Any, deadline: float) -> Any:
        result = original(raw, work, deadline)
        _ = Path(document["corner_replay"]).write_text("changed")
        return result

    monkeypatch.setattr(tool, "disk_extremes", changed)
    with pytest.raises(ValueError, match="bytes changed"):
        _ = tool.generate(document, deadline=time.monotonic() + 10)
    with pytest.raises(ValueError, match="schema"):
        _ = tool.generate([], deadline=time.monotonic() + 10)
    with pytest.raises(ValueError, match="certificate"):
        _ = tool.check(document, [], deadline=time.monotonic() + 10)


def test_cli_fresh_and_output_overflow(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    document, _base, _calls = setup(monkeypatch, tmp_path)
    d, c, r = (tmp_path / name for name in ("d.json", "c.json", "r.json"))
    _ = d.write_text(json.dumps(document))
    assert tool.main(["--descriptor", str(d), "--output", str(c)]) == 0
    assert tool.main(["--descriptor", str(d), "--certificate", str(c), "--output", str(r)]) == 0
    assert json.loads(r.read_text())["verification_passed"] is True
    monkeypatch.setattr(tool, "OUTPUT_LIMIT", 1)
    small = tmp_path / "small.json"
    assert tool.main(["--descriptor", str(d), "--output", str(small)]) == 1
    assert json.loads(small.read_text())["status"] == "incomplete"


def test_failure_flags() -> None:
    for exc in (ValueError("bad"), tool.finite.IncompleteError("limit")):
        result = tool.failure(exc)
        assert result["criterion_met"] is False
        assert result["complete_classification"] is False
        assert all(result[k] is False for k in tool.prior.scope())


def test_two_clean_processes_real_projection_with_explicit_synthetic_intake(
    tmp_path: Path,
) -> None:
    masks = [
        sum(1 << i for i in c)
        for c in itertools.islice(itertools.combinations(range(24), 17), 95)
    ]
    data = tmp_path / "synthetic.json"
    _ = data.write_text(json.dumps({"masks": masks}))
    descriptor = tmp_path / "descriptor.json"
    _ = descriptor.write_text(json.dumps({"schema": tool.CONTEXT_SCHEMA}))
    script = """
import json,sys
from pathlib import Path
from fractions import Fraction as Q
from devtools import check_n17_incircle_disk_projection as t
f=json.loads(Path(sys.argv[1]).read_bytes())
p=[(Q(1,2),Q(1,2)),(Q(4),Q(1,2)),(Q(4),Q(4)),(Q(1,2),Q(4))]
polys=[p[:] for _ in range(24)]
names=[f'synthetic-{i}' for i in range(24)]
roster=[{'mask':m} for m in f['masks']]
t.prior.prior.intake=lambda d,deadline:(polys,names,roster,{}, {})
raise SystemExit(t.main(sys.argv[2:]))
"""
    outputs = [tmp_path / "result.json", tmp_path / "fresh.json"]
    for index, output in enumerate(outputs):
        args = [
            sys.executable,
            "-c",
            script,
            str(data),
            "--descriptor",
            str(descriptor),
            "--output",
            str(output),
        ]
        if index:
            args += ["--certificate", str(outputs[0])]
        completed = subprocess.run(
            args, capture_output=True, text=True, timeout=30, check=False
        )
        assert completed.returncode == 0, completed.stderr
    result, fresh = [json.loads(p.read_bytes()) for p in outputs]
    assert tool.payload(result) == tool.payload(fresh)
    assert result["work"]["state_pairs_accounted"] == 12920
    assert result["disk_work"]["norms_checked"] > 0
    assert fresh["verification_passed"] is True
    assert result["criterion_met"] is False
