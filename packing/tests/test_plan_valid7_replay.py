"""The Valid7 replay planner, and the plan and calibration receipts it wrote.

``devtools.plan_valid7_replay`` prices a full replay of either Valid7 checker from its run
record, splits it into shards, and compares a sharded replay with the published record.
Daniel's record is retained, so the tests over it use the real file; Hosono's release
records are pinned by digest and not retained, so its paths are tested on small
synthetic records, and its committed plan is read only as a receipt.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from devtools import plan_valid7_replay as pv

EVAND_RECEIPTS = pv.WEB / "evand-square-packing-2026-10-01/receipts/valid7"
WAND_RECEIPTS = pv.WEB / "wand125-valid7-independent-check-2026-10-02/receipts"
F = Fraction


def _rect_cells(rect: pv.Rect) -> set[pv.Cell]:
    x0, x1, y0, y1 = rect
    return {
        (x0 + pv.PITCH * i, y0 + pv.PITCH * j)
        for i in range(int((x1 - x0) / pv.PITCH))
        for j in range(int((y1 - y0) / pv.PITCH))
    }


def test_partition_is_consecutive_and_balanced() -> None:
    runs = pv.partition([5.0, 1.0, 1.0, 1.0, 5.0], 3)
    assert runs == [(0, 1), (1, 4), (4, 5)]
    assert pv.partition([1.0] * 10, 4) == [(0, 3), (3, 6), (6, 9), (9, 10)]


@pytest.mark.parametrize(("start", "stop"), [(0, 9), (1, 8), (2, 3), (3, 6), (4, 9)])
def test_rectangles_cover_exactly_their_cells(start: int, stop: int) -> None:
    side = 3
    rects = pv.rectangles(start, stop, side)
    assert len(rects) <= 3
    covered = set[pv.Cell]().union(*(_rect_cells(r) for r in rects))
    want = {(pv.PITCH * (i // side), pv.PITCH * (i % side)) for i in range(start, stop)}
    assert covered == want
    assert sum(len(_rect_cells(r)) for r in rects) == stop - start


def test_mirror_is_an_involution_that_negates_u() -> None:
    box = (F(1, 10), F(1, 5), F(3, 10), F(2, 5), F(1, 32), F(1, 16))
    assert pv.mirror(box) == (F(34, 5), F(69, 10), F(3, 10), F(2, 5), F(-1, 16), F(-1, 32))
    assert pv.mirror(pv.mirror(box)) == box


def test_a_v1_root_is_priced_at_its_v2_mirror() -> None:
    box = (F(0), F(1, 10), F(0), F(1, 10), F(0), F(1, 32))
    roots = [
        pv.Root(box, 90.0, [], 0, comparable=False),
        pv.Root(pv.mirror(box), 7.0, [], 0),
    ]
    assert pv.priced("wand125", roots) == {box: 7.0, pv.mirror(box): 7.0}
    assert pv.priced("qx2", roots) == {box: 90.0, pv.mirror(box): 7.0}


def test_the_qx2_plan_covers_the_d4_region_once() -> None:
    result = pv.plan("qx2", 3, None)
    assert result["roots"] == 9800
    assert result["recorded_cpu_hours"] == pytest.approx(22.6, abs=0.01)
    shards = cast("list[dict[str, object]]", result["shards"])
    cells: list[pv.Cell] = []
    for shard in shards:
        for run in cast("list[dict[str, object]]", shard["runs"]):
            rect = cast("pv.Rect", tuple(F(v) for v in cast("list[str]", run["rectangle"])))
            cells += _rect_cells(rect)
            command = cast("list[str]", run["command"])
            assert command[1:3] == ["checker/qx2_zm.py", "L4_k02_box7.txt"]
            assert "--dump-leaves" in command
    assert len(cells) == len(set(cells)) == 35 * 35


def _qx2_shard(tmp_path: Path, roots: list[dict[str, object]], argv: list[str]) -> Path:
    header = {
        "kind": "header",
        "sha256": {**pv.QX2_FILES, "input": pv.COVER_SHA256},
        "argv": argv,
    }
    path = tmp_path / "shard.jsonl"
    path.write_text("".join(json.dumps(x) + "\n" for x in [header, *roots]), encoding="utf-8")
    return path


def _published_qx2_lines(count: int) -> list[dict[str, object]]:
    with gzip.open(pv.QX2_RECORD, "rt", encoding="utf-8") as handle:
        lines = [cast("dict[str, object]", json.loads(raw)) for raw in handle]
    return lines[1 : count + 1]


ARGV = [
    "checker/qx2_zm.py", "L4_k02_box7.txt", "--depth", "18", "--nproc", "4",
    "--exact-umax", "1/2", "--exact-from", "3", "--cx-lo", "0", "--cx-hi", "1/10",
    "--resume", "runs/x.jsonl", "--dump-leaves",
]  # fmt: skip


def test_a_faithful_qx2_shard_passes_and_each_fault_is_named(tmp_path: Path) -> None:
    lines = _published_qx2_lines(2)
    ok = pv.compare("qx2", [_qx2_shard(tmp_path, lines, ARGV)], None, partial=True)
    assert ok["ok"], ok["problems"]
    assert ok["roots_matching_published_leaves"] == 2
    whole = pv.compare("qx2", [_qx2_shard(tmp_path, lines, ARGV)], None)
    assert whole["problems"] == ["9798 published roots are missing"]
    tampered = json.loads(json.dumps(lines))
    leaves = cast("list[list[object]]", tampered[0]["leaves"])
    leaves[0][1] = "EMPTY" if leaves[0][1] != "EMPTY" else "CAP"
    problems = pv.compare("qx2", [_qx2_shard(tmp_path, tampered, ARGV)], None, partial=True)
    assert problems["problems"] == ["1 roots have leaves other than the published ones"]
    twice = pv.compare(
        "qx2", [_qx2_shard(tmp_path, [*lines, lines[0]], ARGV)], None, partial=True
    )
    assert twice["problems"] == ["1 roots recorded more than once"]
    coarse = pv.compare(
        "qx2", [_qx2_shard(tmp_path, lines, [*ARGV, "--pitch", "1/5"])], None, partial=True
    )
    assert coarse["problems"] == ["shard.jsonl: argv changes a setting with --pitch"]
    shallow = [v if v != "18" else "12" for v in ARGV]
    lax = pv.compare("qx2", [_qx2_shard(tmp_path, lines, shallow)], None, partial=True)
    assert lax["problems"] == ["shard.jsonl: argv does not set --depth 18"]


def _wand_record(
    path: Path, roots: list[tuple[pv.Box, float, str]], names: dict[str, str]
) -> None:
    lines: list[object] = [{"header": {"argv": ["src/run_all.py"], "sha256": names}}]
    lines += [
        {
            "root": [str(v) for v in box],
            "cpu": cpu,
            "leaves": [[[str(v) for v in box], kind, None]],
            "uncert": [],
            "cex": [],
        }
        for box, cpu, kind in roots
    ]
    raw = "".join(json.dumps(x) + "\n" for x in lines).encode()
    path.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".gz" else raw)


def test_wand125_compares_v2_roots_only_and_knows_the_guard(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(pv, "WAND125_V1_ROOTS", 1)
    v1 = (F(0), F(1, 10), F(0), F(1, 10), F(0), F(1, 32))
    v2 = pv.mirror(v1)
    names = {f"src/{n}": d for n, d in pv.WAND125_FILES.items() if d}
    names["cover/L4_k02_box7.txt"] = pv.COVER_SHA256
    _wand_record(tmp_path / "full.jsonl.gz", [(v1, 90.0, "CORE")], names)
    _wand_record(tmp_path / "full_b.jsonl.gz", [(v2, 7.0, "TIERB2")], names)
    replay = tmp_path / "shard.jsonl"
    _wand_record(replay, [(v1, 1.0, "EMPTY"), (v2, 1.0, "TIERB2")], names)
    result = pv.compare("wand125", [replay], tmp_path)
    assert result["ok"], result["problems"]
    assert result["roots_matching_published_leaves"] == 1
    assert (result["leaves"], result["root_hours"]) == (2, round(2.0 / 3600, 2))
    assert (
        pv.region("wand125", (F(0), F(7)), (F(0), F(1, 10)), tmp_path)["priced_cpu_seconds"]
        == 14.0
    )
    guarded = pv.guard_d1(pv.WAND125_TREE / "src/tier_b2.py")
    names["src/tier_b2.py"] = hashlib.sha256(guarded).hexdigest()
    _wand_record(replay, [(v1, 1.0, "EMPTY"), (v2, 1.0, "TIERB2")], names)
    assert pv.compare("wand125", [replay], tmp_path, guarded=True)["ok"]
    assert pv.compare("wand125", [replay], tmp_path)["problems"] == [
        "shard.jsonl: tier_b2.py is not the retained V2 file"
    ]


def test_stage_refuses_nothing_retained_and_the_guard_changes_one_line(tmp_path: Path) -> None:
    qx2 = pv.stage("qx2", tmp_path / "qx2")
    assert {k.removeprefix("checker/"): v for k, v in qx2.items()} == {
        **pv.QX2_FILES,
        "L4_k02_box7.txt": pv.COVER_SHA256,
    }
    wand = pv.stage("wand125", tmp_path / "wand", guard=True)
    source = (pv.WAND125_TREE / "src/tier_b2.py").read_text(encoding="utf-8")
    staged = (tmp_path / "wand/src/tier_b2.py").read_text(encoding="utf-8")
    assert wand["src/tier_b2.py"] != pv.WAND125_FILES["tier_b2.py"]
    assert wand["src/run_all.py"] == pv.WAND125_FILES["run_all.py"]
    assert staged == source.replace(pv.D1_LINE, pv.D1_GUARD)
    assert staged.count("raise ArithmeticError") == 1
    with pytest.raises(SystemExit, match="exactly once"):
        pv.guard_d1(tmp_path / "wand/src/rf.py")


def test_the_committed_qx2_plan_is_what_the_tool_writes() -> None:
    receipt = json.loads((EVAND_RECEIPTS / "qx2_replay_plan.json").read_text(encoding="utf-8"))
    fresh = pv.plan(
        "qx2",
        len(receipt["shards"]),
        None,
        speed=receipt["speed"],
        cores=receipt["cores_per_shard"],
    )
    assert fresh == receipt


def _footer(log: Path) -> tuple[float, str]:
    text = log.read_text(encoding="utf-8")
    cpu = re.search(r"exit 0; wall [\d.]+ s; CPU ([\d.]+) s", text)
    assert cpu is not None, log
    return float(cpu.group(1)), text


def test_the_calibrations_reproduce_published_leaves_and_bound_the_speed() -> None:
    qx2_cpu, qx2_log = _footer(EVAND_RECEIPTS / "qx2_calibration_x27-28_y23-24.log")
    assert "VERIFIED-D4" in qx2_log
    qx2_plan = json.loads((EVAND_RECEIPTS / "qx2_replay_plan.json").read_text(encoding="utf-8"))
    recorded = pv.region("qx2", (F(27, 10), F(14, 5)), (F(23, 10), F(12, 5)), None)
    assert qx2_cpu / cast("float", recorded["recorded_cpu_seconds"]) <= qx2_plan["speed"]
    compare = json.loads((EVAND_RECEIPTS / "qx2_calibration_compare.json").read_text("utf-8"))
    assert (compare["ok"], compare["roots_matching_published_leaves"]) == (True, 8)
    wand_cpu = sum(
        _footer(WAND_RECEIPTS / f"valid7_calibration_{cell}.log")[0]
        for cell in ("x51-52_y25-26", "x54-55_y63-64")
    )
    wand_plan = json.loads((WAND_RECEIPTS / "valid7_replay_plan.json").read_text("utf-8"))
    # The two cells' published times, 122.6 s and 232.0 s, from the plan's own region tool.
    assert wand_cpu / (122.6 + 232.0) <= wand_plan["speed"]
    assert wand_plan["host_cpu_hours_estimate"] == pytest.approx(540.54 * 0.40, abs=0.01)
    forkserver, _ = _footer(WAND_RECEIPTS / "valid7_calibration_forkserver_x51-52_y25-26.log")
    assert forkserver < 1.0
    compare = json.loads((WAND_RECEIPTS / "valid7_calibration_compare.json").read_text("utf-8"))
    assert (compare["ok"], compare["roots_matching_published_leaves"]) == (True, 64)


def test_the_guarded_wand125_replay_is_complete_and_matches_the_published_leaves() -> None:
    """The full replay of 2 and 3 October, staged with ``--guard-d1``: every run the plan
    names has its record, and its last receipt reads VERIFIED with exit 0; no attempt
    records an uncertified box, a counterexample or a Tier B error, which is how a guard
    refusal would show; and the committed comparison holds over all 156,800 roots."""
    plan = json.loads((WAND_RECEIPTS / "valid7_replay_plan.json").read_text("utf-8"))
    replay = WAND_RECEIPTS / "replay"
    runs = [
        Path(cast("str", run["receipt"])).stem
        for shard in cast("list[dict[str, object]]", plan["shards"])
        for run in cast("list[dict[str, object]]", shard["runs"])
    ]
    assert len(runs) == 33
    attempts = 0
    cpu = 0.0
    for run in runs:
        assert (replay / f"{run}.jsonl.gz").is_file(), run
        logs = sorted(replay.glob(f"{run}*.log"))
        attempts += len(logs)
        for log in logs:
            text = log.read_text(encoding="utf-8")
            for refusal in ("TIERB-ERROR", "UNCERTIFIED", "COUNTEREXAMPLE", "NOT VERIFIED"):
                assert refusal not in text, (log.name, refusal)
            assert ("# finished" in text) == (log == logs[-1]), log.name
        seconds, last = _footer(logs[-1])
        assert "VERIFIED" in last.splitlines(), logs[-1].name
        cpu += seconds
    assert attempts == len(list(replay.glob("*.log"))) == 53
    assert round(cpu / 3600, 1) == 85.3
    compare = json.loads((replay / "wand125_replay_compare.json").read_text("utf-8"))
    assert compare["shards"] == [f"{run}.jsonl.gz" for run in sorted(runs)]
    assert (compare["ok"], compare["problems"], compare["partial"]) == (True, [], False)
    assert (compare["roots"], compare["leaves"]) == (156_800, 9_808_968)
    assert compare["roots_matching_published_leaves"] == 156_800 - pv.WAND125_V1_ROOTS
    assert compare["roots_not_compared"] == pv.WAND125_V1_ROOTS
    assert compare["root_hours"] <= plan["host_cpu_hours_estimate"]


def test_the_fast_verify_and_the_leaf_recheck_receipts() -> None:
    _, fast = _footer(EVAND_RECEIPTS / "k2m3_verify_fast.log")
    for line in (
        "    cover: CLEAN",
        "    FAMILY CHECK OK",
        "    identical to the shipped qx2_zm/lemmaZ.out",
        "    record: CLEAN",
        "    identical to lean/Sqpack/BentzData.lean",
        "s(k^2 - 3) = k bundle: OK",
    ):
        assert line in fast.splitlines()
    recheck_cpu, recheck = _footer(WAND_RECEIPTS / "valid7_leaf_recheck_x54-55_y63-64.log")
    assert "--recheck 2425 --recheck-b 438" in recheck
    assert "RECORD OK" in recheck.splitlines()
    search_cpu, _ = _footer(WAND_RECEIPTS / "valid7_calibration_x54-55_y63-64.log")
    assert recheck_cpu >= search_cpu
