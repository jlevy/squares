"""The audit of Hosono's ValidTilt9 records, and the receipts of its stage-3 sample.

The three record files are pinned by SHA-256 and not retained, so the tests over the run
read the retained receipts: the audit's JSON, the log of the source's
``verify_tilt9.sh``, the sample's comparison and the controls. The rest builds small
inputs and checks each rule of ``devtools.audit_validtilt9_independent`` on them.
"""

from __future__ import annotations

import json
import re
from fractions import Fraction
from typing import cast

import pytest

from devtools import audit_validtilt9_independent as audit

F = Fraction
ZERO: audit.Box = (F(0), F(0), F(0), F(0), F(0), F(0))
RECEIPTS = audit.PACKET / "receipts"
AUDIT_JSON = RECEIPTS / "validtilt9_records_audit.json"
VERIFY_LOG = RECEIPTS / "validtilt9_verify.log"
SAMPLE_PLAN = RECEIPTS / "validtilt9_sample_plan.json"
SAMPLE_COMPARE = RECEIPTS / "validtilt9_sample_compare.json"
CONTROLS = RECEIPTS / "validtilt9_controls.json"


def _json(path: object) -> dict[str, object]:
    return cast("dict[str, object]", json.loads(audit.Path(str(path)).read_text("utf-8")))


def _root(record: str, box: audit.Box, index: int = 0) -> audit.Root:
    return audit.Root(record, index, box, 1.0, 1, audit.phase_of(record, index))


def _split_grid() -> list[audit.RecordStats]:
    records = [audit.RecordStats(name) for name in audit.RECORDS]
    for box in sorted(audit.expected_roots()):
        for stats in records:
            lo, hi = audit.SPLIT[stats.name]
            if lo <= box[0] < hi:
                stats.roots.append(_root(stats.name, box))
    return records


def test_the_grid_is_45_by_45_centres_by_14_u_bins() -> None:
    grid = audit.expected_roots()
    assert len(grid) == 28_350
    assert {b[4] for b in grid} | {b[5] for b in grid} == {F(k, 32) for k in range(15)}
    assert {b[0] for b in grid} | {b[1] for b in grid} == {F(k, 10) for k in range(46)}


def test_the_grid_covers_validtilt9_and_a_shorter_one_does_not() -> None:
    grid = audit.expected_roots()
    assert audit.statement_problems(grid) == []
    short = {b for b in grid if b[5] <= F(13, 32)}
    assert audit.statement_problems(short) == [
        "the u grid [0, 13/32] does not reach sqrt 2 - 1"
    ], "13/32 < sqrt 2 - 1 < 7/16"
    narrow = {b for b in grid if b[1] <= F(44, 10) and b[3] <= F(44, 10)}
    assert audit.statement_problems(narrow) == ["the centre grid is not [0, 9/2]"]


def test_the_split_grid_passes_and_a_repeat_a_gap_or_a_stray_does_not() -> None:
    records = _split_grid()
    assert [len(r.roots) for r in records] == [23_940, 3_780, 630]
    assert audit.grid_problems(records) == []
    records[2].roots.append(records[2].roots[0])
    assert audit.grid_problems(records) == ["1 roots appear more than once"]
    records[2].roots[:2] = []
    assert audit.grid_problems(records) == ["1 grid roots are missing"]
    records[0].roots.append(records[1].roots[0])
    assert "tilt9_a.jsonl: 1 roots outside 0 <= x < 19/5" in audit.grid_problems(records)


def test_the_phases_cut_each_record_where_the_run_notes_say() -> None:
    assert [audit.phase_of("tilt9_a.jsonl", i) for i in (0, 16_404, 16_405, 22_661)] == [
        "amin-1/320", "amin-1/320", "amin-1/1280", "amin-1/1280",
    ]  # fmt: skip
    assert [audit.phase_of("tilt9_a.jsonl", i) for i in (22_662, 22_663, 22_664, 23_939)] == [
        "bmid-3/16", "bmid-3/16", "bmid-7/16", "bmid-7/16",
    ]  # fmt: skip
    assert [audit.phase_of("tilt9_b.jsonl", i) for i in (349, 350, 2_432, 2_587, 3_779)] == [
        "amin-1/320", "amin-1/1280", "bmid-3/16", "bmid-7/16", "bmid-7/16",
    ]  # fmt: skip
    for name in audit.RECORDS:
        last = audit.PHASES[name][-1][0]
        audit.phase_of(name, last - 1)
        with pytest.raises(ValueError, match="has no phase"):
            audit.phase_of(name, last)


def _leaf(width: Fraction, u0: Fraction, u1: Fraction) -> tuple[audit.Box, str]:
    return (F(1), F(1) + width, F(1), F(1) + width, u0, u1), "TIERB2"


@pytest.mark.parametrize(
    ("phase", "width", "u", "ok"),
    [
        ("amin-1/320", F(1, 320), (F(1, 32), F(1, 16)), True),
        ("amin-1/320", F(1, 640), (F(1, 32), F(1, 16)), True),
        ("amin-1/320", F(1, 1280), (F(1, 32), F(1, 16)), False),
        ("amin-1/320", F(1, 20), (F(1, 32), F(1, 16)), False),
        ("amin-1/1280", F(1, 1280), (F(1, 32), F(1, 16)), True),
        ("amin-1/1280", F(1, 320), (F(1, 32), F(1, 16)), False),
        ("bmid-7/16", F(1, 20), (F(13, 32), F(7, 16)), True),
        ("bmid-7/16", F(1, 1280), (F(13, 32), F(7, 16)), False),
        ("bmid-3/16", F(1, 20), (F(5, 32), F(3, 16)), True),
        ("bmid-3/16", F(1, 20), (F(7, 32), F(1, 4)), False),
        ("bmid-3/16", F(1, 1280), (F(7, 32), F(1, 4)), True),
        ("amin-1/1280", F(1, 10), (F(0), F(1, 64)), True),
        ("bmid-7/16", F(1, 5), (F(0), F(1, 64)), False),
    ],
)
def test_a_tier_b_leaf_tests_the_phase_it_is_read_in(
    phase: str, width: Fraction, u: tuple[Fraction, Fraction], *, ok: bool
) -> None:
    problem = audit.leaf_problem(phase, [_leaf(width, *u)])
    assert (problem == "") is ok, problem


def test_the_retained_checker_is_the_code_the_headers_name() -> None:
    assert audit.retained_problems(audit.TREE) == []
    receipt = _json(AUDIT_JSON)
    for record in cast("list[dict[str, object]]", receipt["records"]):
        stats = audit.RecordStats(
            cast("str", record["name"]), header={"sha256": record["header_sha256"]}
        )
        assert audit.header_problems(stats, audit.TREE, audit.COVER_SHA256) == []
    stats = audit.RecordStats("tilt9_c.jsonl", header={"sha256": {audit.COVER_KEY: "0" * 64}})
    assert audit.header_problems(stats, audit.TREE, audit.COVER_SHA256)[0] == (
        f"tilt9_c.jsonl: {audit.COVER_KEY} is not a retained file ({'0' * 16})"
    )


def test_the_retained_audit_passed_over_the_whole_region() -> None:
    receipt = _json(AUDIT_JSON)
    assert receipt["ok"] is True
    assert receipt["problems"] == []
    assert receipt["leaf_kinds"] == audit.STATED_LEAVES
    assert receipt["grid_roots"] == 28_350
    records = cast("list[dict[str, object]]", receipt["records"])
    assert [r["roots"] for r in records] == [23_940, 3_780, 630]
    assert all(r["uncertified"] == r["counterexamples"] == 0 for r in records)
    assert cast("float", receipt["cpu_core_hours"]) == pytest.approx(766, abs=0.5)
    region = cast("dict[str, object]", receipt["region"])
    assert region["covers_sqrt2_minus_1"] is True


def test_the_shared_lines_with_daniels_checker_are_the_receipts() -> None:
    """Re-derives the count from the retained files of both checkers now."""
    shared = audit.shared_code()
    receipt = cast("dict[str, object]", _json(AUDIT_JSON)["shared_code"])
    assert shared == receipt
    assert len(cast("list[str]", shared["common_lines"])) <= 10


def test_each_mutant_lightens_one_tight_family() -> None:
    cover = audit.cover_bytes()
    original = cover.decode().splitlines()
    made = audit.mutants(cover)
    wall = made["M1_wall_1e-4.txt"].decode().splitlines()
    leb = made["M2_leb_1e-4.txt"].decode().splitlines()
    assert wall[0] == leb[0] == original[0] == "mixed 1"
    assert re.fullmatch(r"# mutant M1: \d+ segments in .* x \(1 - 1e-4\)", wall[1])
    changed = [(a, b) for a, b in zip(original, wall[:1] + wall[2:], strict=True) if a != b]
    assert len(changed) == int(wall[1].split()[3]) > 0
    for before, after in changed:
        assert before.split()[:4] == after.split()[:4]
        assert int(after.split()[4]) < int(before.split()[4])
    assert leb[:1] + leb[2:-1] == original[:-1]
    assert int(leb[-1].split()[1]) == int(original[-1].split()[1]) * 9999 // 10000


def test_the_source_record_check_passed_with_a_fresh_seed() -> None:
    log = VERIFY_LOG.read_text(encoding="utf-8")
    assert re.search(r"^# finished \S+; exit 0;", log, re.MULTILINE)
    assert re.search(r"^recheck seed \d+$", log, re.MULTILINE)
    assert "recheck seed 1974443077083783347" not in log, "the source's own seed"
    assert re.search(
        r"^claim tilt roots 28350 leaf kinds "
        r"\{'CORE': 6565165, 'TIERB2': 2940689, 'EMPTY': 31489\}\nRECORD OK$",
        log,
        re.MULTILINE,
    )
    assert len(re.findall(r"^tilt9_[abc]\.jsonl(\.gz)?: OK$", log, re.MULTILINE)) == 6


def test_the_controls_accepted_the_cover_and_refused_each_mutant() -> None:
    receipt = _json(CONTROLS)
    assert receipt["ok"] is True
    rows = {r["control"]: r for r in cast("list[dict[str, object]]", receipt["controls"])}
    assert set(rows) == {"wall_original", "wall_M1", "lebesgue_original", "lebesgue_M2"}
    assert all(row["found"] is True and row["exit"] == 0 for row in rows.values())
    made = audit.mutants(audit.cover_bytes())
    assert receipt["mutants"] == {
        name: audit.hashlib.sha256(data).hexdigest() for name, data in made.items()
    }
    for name, _, expect in audit.control_commands("python3"):
        log = (RECEIPTS / "controls" / f"control_{name}.log").read_text(encoding="utf-8")
        assert expect in log


def test_the_sample_reproduced_every_replayed_root_and_priced_the_replay() -> None:
    plan = _json(SAMPLE_PLAN)
    compare = _json(SAMPLE_COMPARE)
    assert compare["ok"] is True
    runs = cast("list[dict[str, object]]", plan["runs"])
    replays = [run for run in runs if audit.replays(run)]
    assert compare["replays_matching_published_leaves"] == len(replays) > 0
    assert {run["published_phase"] for run in replays} == set(audit.OPTIONS)
    price = cast("dict[str, dict[str, object]]", compare["price"])
    assert cast("float", price["replay"]["host_cpu_hours"]) > 6, "the brief's ceiling"


def test_spread_follows_cost_and_takes_each_root_once() -> None:
    costs = [1.0] * 100 + [100.0]
    pool = [
        audit.Root("tilt9_a.jsonl", i, ZERO, c, 1, "amin-1/320") for i, c in enumerate(costs)
    ]
    picked = audit.spread(pool, 4)
    assert len(picked) == len({id(r) for r in picked}) == 3, "the heavy root is due twice"
    assert [r.cpu for r in picked] == [1.0, 1.0, 100.0]


def test_price_scales_each_stratum_by_its_own_sample() -> None:
    strata = {
        f"{phase}/{part}": {"roots": 1, "recorded_cpu_hours": 1.0}
        for phase in audit.OPTIONS
        for part in ("light", "heavy")
    }
    host = {
        ("replay", "amin-1/320/light"): 50.0,
        ("replay", "amin-1/1280/light"): 50.0,
        ("replay", "bmid-3/16/light"): 50.0,
        ("replay", "bmid-7/16/light"): 50.0,
        ("final", "amin-1/1280/heavy"): 10.0,
    }
    recorded = dict.fromkeys(host, 100.0)
    out = audit.price(strata, host, recorded, audit.Counter(dict.fromkeys(host, 1)))
    replay = cast("dict[str, object]", out["replay"])
    assert replay["host_cpu_hours"] == pytest.approx(4.0), "heavy takes its phase's light ratio"
    final = cast("dict[str, dict[str, dict[str, object]]]", out["final"])
    assert final["strata"]["amin-1/320/heavy"]["ratio"] == pytest.approx(0.1)
    assert final["strata"]["bmid-7/16/light"]["ratio_from"] == ["bmid-7/16/light"]
