"""The audit of Hosono's Valid7 records, and the receipts of its stage-4 replay.

The record files themselves are pinned by SHA-256 and not retained, so the tests over
the replay read the retained receipts only: the audit's JSON and the log of the
source's ``verify.sh``, whose three mutant covers are the replay's negative controls.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import cast

from devtools import audit_valid7_independent as audit

RECEIPTS = audit.PACKET / "receipts"
VERIFY_LOG = RECEIPTS / "valid7_verify.log"
AUDIT_JSON = RECEIPTS / "valid7_records_audit.json"


def _split_grid() -> list[audit.RecordStats]:
    grid = sorted(audit.expected_roots())
    return [
        audit.RecordStats("full.jsonl", roots=[b for b in grid if b[0] < audit.SPLIT_X]),
        audit.RecordStats("full_b.jsonl", roots=[b for b in grid if b[0] >= audit.SPLIT_X]),
    ]


def test_the_grid_is_70_by_70_centres_by_32_u_bins() -> None:
    grid = audit.expected_roots()
    assert len(grid) == 156_800
    assert {b[4] for b in grid} | {b[5] for b in grid} == {
        Fraction(k, 32) for k in range(-16, 17)
    }


def test_the_split_grid_passes_and_a_repeat_or_a_gap_does_not() -> None:
    records = _split_grid()
    assert audit.grid_problems(records) == []
    records[1].roots.append(records[1].roots[0])
    assert audit.grid_problems(records) == ["1 roots appear more than once"]
    records[1].roots[:2] = []
    assert audit.grid_problems(records) == ["1 grid roots are missing"]
    records[0].roots.append(records[1].roots[0])
    assert "full.jsonl has a root with x >= 11/2" in audit.grid_problems(records)


def test_read_record_counts_leaves_and_hashes_both_forms(tmp_path: Path) -> None:
    lines = [
        {"header": {"argv": ["src/run_all.py"], "sha256": {}}},
        {
            "root": ["0", "1/10", "0", "1/10", "-1/2", "-15/32"],
            "cpu": 1.5,
            "leaves": [[["0"], "EMPTY", None], [["0"], "CORE", None]],
            "uncert": [],
            "cex": [["1"]],
        },
    ]
    raw = "".join(json.dumps(line) + "\n" for line in lines).encode()
    path = tmp_path / "full.jsonl.gz"
    path.write_bytes(gzip.compress(raw, mtime=0))
    stats = audit.read_record(path)
    assert stats.name == "full.jsonl"
    assert stats.sha256_decompressed == hashlib.sha256(raw).hexdigest()
    assert stats.sha256_compressed == hashlib.sha256(path.read_bytes()).hexdigest()
    assert stats.leaves == Counter({"EMPTY": 1, "CORE": 1})
    assert (stats.counterexamples, stats.uncertified, stats.cpu_seconds) == (1, 0, 1.5)
    assert stats.roots == [
        (
            Fraction(0),
            Fraction(1, 10),
            Fraction(0),
            Fraction(1, 10),
            Fraction(-1, 2),
            Fraction(-15, 32),
        )
    ]


def test_a_header_digest_must_match_the_retained_file(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src/rf.py").write_bytes(b"x\n")
    cover = tmp_path / "cover.txt"
    cover.write_bytes(b"c\n")
    good = {"src/rf.py": hashlib.sha256(b"x\n").hexdigest()}
    good["cover/L4_k02_box7.txt"] = hashlib.sha256(b"c\n").hexdigest()
    stats = audit.RecordStats("full_b.jsonl", header={"sha256": good})
    assert audit.header_problems(stats, tmp_path, cover) == []
    stats.header = {"sha256": {**good, "src/rf.py": "0" * 64}}
    assert audit.header_problems(stats, tmp_path, cover) == [
        f"full_b.jsonl: src/rf.py is {good['src/rf.py'][:16]}, the header says {'0' * 16}"
    ]
    stats.name = "full.jsonl"
    stats.header = {"sha256": {**good, "src/tier_b2.py": "0" * 64}}
    assert audit.header_problems(stats, tmp_path, cover) == [
        "full.jsonl: src/tier_b2.py is not retained"
    ], "full.jsonl's V1 tier_b2.py is read from versions/V1/"


def test_the_retained_audit_passed_over_the_whole_grid() -> None:
    receipt = cast("dict[str, object]", json.loads(AUDIT_JSON.read_text(encoding="utf-8")))
    assert receipt["ok"] is True
    assert receipt["problems"] == []
    assert receipt["leaves"] == audit.STATED_LEAVES
    records = cast("list[dict[str, object]]", receipt["records"])
    assert sum(cast("int", r["roots"]) for r in records) == receipt["grid_roots"] == 156_800
    assert all(r["uncertified"] == r["counterexamples"] == 0 for r in records)


def test_the_retained_headers_name_the_retained_code() -> None:
    """Re-derives the header linkage from the receipt and the retained files now."""
    receipt = cast("dict[str, object]", json.loads(AUDIT_JSON.read_text(encoding="utf-8")))
    for record in cast("list[dict[str, object]]", receipt["records"]):
        header = {"sha256": record["header_sha256"]}
        stats = audit.RecordStats(cast("str", record["name"]), header=header)
        assert audit.header_problems(stats, audit.TREE, audit.COVER) == []


def test_the_source_record_check_passed_and_every_mutant_was_refused() -> None:
    log = VERIFY_LOG.read_text(encoding="utf-8")
    assert re.search(r"^# finished \S+; exit 0;", log, re.MULTILINE)
    assert re.search(r"^RECORD OK$", log, re.MULTILINE)
    assert re.search(
        r"^roots 156800 leaf kinds \{'EMPTY': 79927, 'TIERB2': 2886043, 'CORE': 6674090\}$",
        log,
        re.MULTILINE,
    )
    assert len(re.findall(r"^\{'ok': False, 'why': 'value'", log, re.MULTILINE)) == 3, (
        "M1 twice, M3"
    )
    # run_mutants.sh keeps the driver's last two lines for M2, its tally and verdict.
    assert re.search(
        r"^new roots 2 leaves \{\} uncertified 0 counterexamples 2 .*\nNOT VERIFIED$",
        log,
        re.MULTILINE,
    ), "M2"
