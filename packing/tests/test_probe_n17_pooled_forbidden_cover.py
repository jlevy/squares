"""Synthetic exact union coverage; no scientific parent geometry is read."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import probe_n17_pooled_forbidden_cover as control

Q = control.Q


def deadline() -> float:
    return time.monotonic() + 30


def points(raw: list[tuple[int | Q, int | Q]]) -> list[control.Point]:
    return [(Q(x), Q(y)) for x, y in raw]


def groups(raw: dict[int, list[control.Point]] | None = None) -> dict[str, Any]:
    return {str(i): control.finite.serial((raw or {}).get(i, [])) for i in range(17)}


def row(
    pieces: list[list[control.Point]], lo: Q | None = None, hi: Q | None = None
) -> dict[str, Any]:
    lo = control.cases.INTERVAL[0] if lo is None else lo
    hi = control.cases.INTERVAL[1] if hi is None else hi
    return {
        "interval": [str(lo), str(hi)],
        "reference": {"kind": "phase3", "node": "synthetic", "step": 0, "row": 0},
        "outer_domain": [],
        "residual_polygons": [control.finite.serial(p) for p in pieces],
    }


def test_strict_zero_centered_core_both_axes_and_quarterturn() -> None:
    lo, hi = control.cases.INTERVAL
    square_core = control.core(lo, hi, deadline())
    assert control.cases.contains(square_core, (Q(0), Q(0)))
    assert control.standing.core_strict(square_core, lo, hi)
    rotated = control.cases.bounded_hull([(-y, x) for x, y in square_core], 32, deadline())
    assert rotated == square_core
    assert all(-1 < x < 1 and -1 < y < 1 for x, y in square_core)


def test_asymmetric_minkowski_sign_and_owner0_is_not_obstacle() -> None:
    core = points([(0, 0), (1, 0), (0, 1)])
    result = control.foreign_regions(
        {0: points([(100, 100)]), 1: points([(3, 4)]), 2: []}, core, [0], deadline()
    )
    assert set(result) == {1, 2}
    assert set(result[1]) == set(points([(3, 4), (2, 4), (3, 3)]))
    assert result[2] == []


@pytest.mark.parametrize(
    ("domain", "regions", "covered"),
    [
        ([(0, 0)], [[(0, 0)]], True),
        ([(0, 0)], [[(1, 0)]], False),
        ([(0, 0), (2, 0)], [[(0, 0), (1, 0)], [(1, 0), (2, 0)]], True),
        (
            [(0, 0), (1, 0)],
            [[(0, 0), (Q(1, 4), 0)], [(Q(1, 2), 0)], [(Q(3, 4), 0), (1, 0)]],
            False,
        ),
        (
            [(0, 0), (2, 0), (2, 1), (0, 1)],
            [[(0, 0), (1, 0), (1, 1), (0, 1)], [(1, 0), (2, 0), (2, 1), (1, 1)]],
            True,
        ),
        ([], [], True),
    ],
)
def test_exact_closed_union_degenerate_and_polygon(
    domain: Any,
    regions: Any,
    covered: bool,  # noqa: FBT001
) -> None:
    result = control.cover_piece(
        points(domain), {i: points(p) for i, p in enumerate(regions)}, deadline()
    )
    assert result["covered"] is covered
    assert result["internal_events"] is None
    assert result["event_probe_caps_enforced"] is False


def test_positive_narrow_gap_is_not_covered() -> None:
    delta = Q(1, 2**30)
    domain = points([(0, 0), (2, 0), (2, 1), (0, 1)])
    regions = {
        1: points([(0, 0), (1 - delta, 0), (1 - delta, 1), (0, 1)]),
        2: points([(1 + delta, 0), (2, 0), (2, 1), (1 + delta, 1)]),
    }
    result = control.cover_piece(domain, regions, deadline())
    assert result["covered"] is False
    assert result["uncovered_probe"] is not None


def test_three_region_union_needs_every_partner() -> None:
    domain = points([(0, 0), (3, 0), (3, 1), (0, 1)])
    regions = {i + 1: points([(i, 0), (i + 1, 0), (i + 1, 1), (i, 1)]) for i in range(3)}
    assert control.cover_piece(domain, regions, deadline())["covered"] is True
    for missing in regions:
        remaining = {k: v for k, v in regions.items() if k != missing}
        assert control.cover_piece(domain, remaining, deadline())["covered"] is False


def test_two_partner_union_and_pooled_only_recovery() -> None:
    lo = Q(53, 128)
    domain = points([(Q(4, 5), Q(3, 2)), (Q(11, 5), Q(3, 2))])
    foreign = {1: points([(Q(11, 10), Q(3, 2))]), 2: points([(Q(19, 10), Q(3, 2))])}
    rs = [row([domain], lo, lo)]
    for owner, hull in foreign.items():
        result = control.construct(rs, groups({owner: hull}), groups(), deadline=deadline())
        assert result["pooled_coverage"] is False
    result = control.construct(rs, groups(foreign), groups(), deadline=deadline())
    assert result["pooled_coverage"] is True
    assert result["ordinary_final_coverage"] is False
    assert result["compression_information_recovered"] is True
    assert result["conditional_I_exclusion_proved"] is True


def test_feasible_two_square_pose_remains_uncovered() -> None:
    lo = Q(53, 128)
    foreign = groups({0: points([(1, 1)]), 1: points([(3, 3)])})
    result = control.construct(
        [row([points([(1, 1)])], lo, lo)], foreign, foreign, deadline=deadline()
    )
    assert result["status"] == "criterion_missed"
    assert result["conditional_I_exclusion_proved"] is False
    assert result["relaxation_gap_is_feasible_packing"] is False


def test_matched_ordinary_success_and_empty_piece_vacuity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    foreign = groups({1: points([(1, 1)])})
    result = control.construct([row([points([(1, 1)])])], foreign, foreign, deadline=deadline())
    assert result["ordinary_final_coverage"] is True
    assert result["pooled_coverage"] is True
    assert result["compression_information_recovered"] is False
    monkeypatch.setattr(control, "CORE_LIMIT", 0)
    result = control.construct([row([points([(0, 0)])])], foreign, foreign, deadline=deadline())
    assert result["pooled_coverage"] is True
    assert result["rows"][0]["status"] == "empty_necessary_row"


def test_disconnected_walls_and_closed_seams() -> None:
    left, right = control.cases.INTERVAL
    rs = [
        row([points([(0, 1)]), points([(5, 1)])], left, left),
        row([points([(1, 1)])], right, right),
    ]
    result = control.construct(rs, groups(), groups(), deadline=deadline())
    assert result["rows"][0]["pieces"] == []
    assert result["rows"][1]["interval"] == [str(right), str(right)]
    assert len(result["rows"][1]["pieces"]) == 1
    assert result["pooled_coverage"] is False


def test_ordinary_subset_and_monotonicity_refuse(monkeypatch: pytest.MonkeyPatch) -> None:
    rs = [row([points([(1, 1)])])]
    with pytest.raises(ValueError, match="not contained"):
        control.construct(rs, groups(), groups({1: points([(1, 1)])}), deadline=deadline())
    outcomes = iter([{"covered": True}, {"covered": False}])
    monkeypatch.setattr(control, "cover_piece", lambda *_: next(outcomes))
    with pytest.raises(ValueError, match="ordinary-covered pooled-uncovered"):
        control.construct(rs, groups(), groups(), deadline=deadline())


@pytest.mark.parametrize(
    "cap", ["CORE_LIMIT", "MINKOWSKI_LIMIT", "CLIPPED_LIMIT", "PIECE_LIMIT", "PAIR_LIMIT"]
)
def test_geometry_resource_caps_incomplete(monkeypatch: pytest.MonkeyPatch, cap: str) -> None:
    monkeypatch.setattr(control, cap, 0)
    with pytest.raises(control.IncompleteError, match=r"ceiling"):
        control.construct(
            [row([points([(1, 1)])])],
            groups({1: points([(1, 1)])}),
            groups(),
            deadline=deadline(),
        )


@pytest.mark.parametrize("cap", ["EDGE_LIMIT", "EDGE_PAIR_LIMIT"])
def test_sweep_preflight_guards_incomplete(monkeypatch: pytest.MonkeyPatch, cap: str) -> None:
    monkeypatch.setattr(control, cap, 0)
    domain = points([(0, 0), (1, 0), (1, 1), (0, 1)])
    with pytest.raises(control.IncompleteError, match="edge/pair"):
        control.cover_piece(domain, {1: domain}, deadline())


def test_completed_sweep_after_lease_is_incomplete(monkeypatch: pytest.MonkeyPatch) -> None:
    def slow_sweep(*_args: Any) -> tuple[bool, None]:
        time.sleep(0.02)
        return True, None

    monkeypatch.setattr(control.standing, "covered_by_sweep", slow_sweep)
    domain = points([(0, 0), (1, 0), (1, 1), (0, 1)])
    with pytest.raises(control.IncompleteError, match="wall ceiling"):
        control.cover_piece(domain, {1: domain}, time.monotonic() + 0.01)


def test_used_big_rational_incomplete_but_unused_row_opaque() -> None:
    rs = [row([points([(1, 1)])])]
    bad = copy.deepcopy(rs)
    bad[0]["residual_polygons"][0][0][0] = str(1 << 4097)
    with pytest.raises(control.IncompleteError, match="bit ceiling"):
        control.construct(bad, groups(), groups(), deadline=deadline())
    outside = row([points([(1, 1)])], Q(0), Q(1, 64))
    outside["residual_polygons"][0][0][0] = str(1 << 4097)
    result = control.construct([outside, *rs], groups(), groups(), deadline=deadline())
    assert result["status"] == "criterion_missed"


def synthetic_intake(data: dict[str, Any]) -> tuple[Any, Any, int, list[Any]]:
    return (
        {"cells": {"0": data["rows"]}, "groups": data["pools"], "mask": list(range(17))},
        {
            "synthetic_accepted_premise": True,
            "proof_pool": {"unpooled_conditional_groups": data["ordinary"]},
        },
        0,
        [],
    )


def test_fresh_reconstruction_requires_every_piece_and_constants(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    foreign = groups({1: points([(1, 1)])})
    data = {
        "rows": [
            row([points([(1, 1)])], *interval)
            for interval in (
                (Q(13, 32), Q(13, 32)),
                control.cases.INTERVAL,
                (Q(27, 64), Q(27, 64)),
            )
        ],
        "pools": foreign,
        "ordinary": foreign,
    }
    monkeypatch.setattr(control.cases, "intake", lambda *_: synthetic_intake(data))
    cert = control.generate({}, deadline=deadline())
    assert control.check({}, cert, deadline=deadline())["verification_passed"]
    for key in ("constants", "guard", "conditional_I_exclusion_proved"):
        tampered = copy.deepcopy(cert)
        tampered[key] = None
        with pytest.raises(ValueError, match="reconstruction differs"):
            control.check({}, tampered, deadline=deadline())
    tampered = copy.deepcopy(cert)
    tampered["rows"].pop(0)
    with pytest.raises(ValueError, match="reconstruction differs"):
        control.check({}, tampered, deadline=deadline())


def test_clean_two_process_cli_reconstruction(tmp_path: Path) -> None:
    foreign = groups({1: points([(1, 1)])})
    data = tmp_path / "synthetic.json"
    data.write_text(
        json.dumps({"rows": [row([points([(1, 1)])])], "pools": foreign, "ordinary": foreign})
    )
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text("{}")
    cert, fresh = tmp_path / "certificate.json", tmp_path / "fresh.json"
    script = "\n".join(  # noqa: FLY002
        [
            "import json,sys",
            "from pathlib import Path",
            "from devtools import probe_n17_pooled_forbidden_cover as c",
            "d=json.loads(Path(sys.argv[1]).read_text())",
            (
                "c.cases.intake=lambda *_: ({'cells':{'0':d['rows']},"
                "'groups':d['pools'],'mask':list(range(17))},"
                "{'synthetic_accepted_premise':True,'proof_pool':"
                "{'unpooled_conditional_groups':d['ordinary']}},0,[])"
            ),
            "raise SystemExit(c.main(sys.argv[2:]))",
        ]
    )
    for output, extra in ((cert, []), (fresh, ["--certificate", str(cert)])):
        run = subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                str(data),
                "--descriptor",
                str(descriptor),
                "--output",
                str(output),
                *extra,
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
        assert run.returncode == 0, run.stderr
    report = json.loads(fresh.read_text())
    assert report["verification_passed"] is True
    assert report["conditional_I_exclusion_proved"] is True
    assert all(
        not report[k]
        for k in (
            "unconditional_exclusion_proved",
            "census_admission_proved",
            "global_optimality_proved",
            "parent_geometry_replayed",
            "root_checked_now",
        )
    )
