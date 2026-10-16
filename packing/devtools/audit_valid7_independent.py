"""Audit the release records of Hosono's independent Valid7 checker against the packet.

wand125/valid7-independent-check is a second, separately written exact checker for the
finite statement Valid7 behind T-064. Its run is published as two JSON-lines records in
the release ``records-v1``, which is pinned here by SHA-256 and not retained, so this
audit takes the two downloaded ``.jsonl.gz`` files as arguments. Its own
``check_record.py`` re-checks the records' tiling and re-certifies sampled leaves; this
audit checks what that script leaves out, and reads nothing it writes:

- each file, compressed and decompressed, has the digest of the retained
  ``release/records.sha256``;
- each record's header names, by SHA-256, the cover and the checker files the packet
  retains: the ``versions/V1/`` copies of ``run_all.py`` and ``tier_b2.py`` for
  ``full.jsonl``, whose header was written by V1, and ``src/`` for the rest;
- the roots of the two records together are exactly the grid ``run_all.py`` builds with
  its defaults (centre pitch 1/10 on ``[0, 7]^2``, 16 u-bins on each side of 0 over
  ``[-1/2, 1/2]``), each once, with ``full.jsonl`` holding the centres ``x < 11/2`` and
  ``full_b.jsonl`` the rest, as ``versions/VERSIONS.md`` says;
- no root has an uncertified box or a counterexample;
- and the totals the source's README states: the leaf count and the CPU time.

It decides nothing about any leaf: that is the checker's, and ``check_record.py``'s
sampled recheck. Usage, from ``packing/``::

    .venv/bin/python3 -m devtools.audit_valid7_independent \\
        --records DIR_WITH_full.jsonl.gz_AND_full_b.jsonl.gz --out RECEIPT.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import cast

from strif import atomic_write_text

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/wand125-valid7-independent-check-2026-10-02"
TREE = PACKET / "valid7-independent-check"
COVER = (
    REPO
    / "packing/resources/web/evand-square-packing-2026-10-01/source/s12/certificates/k2m3"
    / "L4_k02_box7.txt"
)
COVER_SHA256 = "c0a6750997897c21ffc693df6df97f89a248dd9eb588a2fe2b83bf359793694b"
RECORDS = ("full.jsonl", "full_b.jsonl")
#: The record whose header the V1 code wrote; its later roots ran under V2.
V1_RECORD = "full.jsonl"
V1_FILES = {
    "src/run_all.py": "versions/V1/run_all.py",
    "src/tier_b2.py": "versions/V1/tier_b2.py",
}
SIDE = Fraction(7)
PITCH = Fraction(1, 10)
UBINS = 16
U_HALF = Fraction(1, 2)
SPLIT_X = Fraction(11, 2)
#: What the source's README states for the run.
STATED_LEAVES = 9_640_060
STATED_CORE_HOURS = 626

Box = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]


@dataclass
class RecordStats:
    """What one record file holds, read line by line."""

    name: str
    sha256_compressed: str = ""
    sha256_decompressed: str = ""
    header: dict[str, object] = field(default_factory=dict[str, object])
    roots: list[Box] = field(default_factory=list[Box])
    leaves: Counter[str] = field(default_factory=Counter[str])
    uncertified: int = 0
    counterexamples: int = 0
    cpu_seconds: float = 0.0


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def read_sums(path: Path) -> dict[str, str]:
    """``sha256sum`` lines as {file name: digest}."""
    sums: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, name = line.split(maxsplit=1)
        sums[name.lstrip("*")] = digest
    return sums


def read_record(path: Path) -> RecordStats:
    """Stream one ``.jsonl.gz`` record and count what it holds."""
    stats = RecordStats(path.name.removesuffix(".gz"), _sha256(path))
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for raw in handle:
            digest.update(raw)
            entry = cast("dict[str, object]", json.loads(raw))
            if "header" in entry:
                stats.header = cast("dict[str, object]", entry["header"])
                continue
            root = cast("list[str]", entry["root"])
            stats.roots.append(cast("Box", tuple(Fraction(v) for v in root)))
            for leaf in cast("list[list[object]]", entry["leaves"]):
                stats.leaves[cast("str", leaf[1])] += 1
            stats.uncertified += len(cast("list[object]", entry["uncert"]))
            stats.counterexamples += len(cast("list[object]", entry["cex"]))
            stats.cpu_seconds += float(cast("float", entry["cpu"]))
    stats.sha256_decompressed = digest.hexdigest()
    return stats


def expected_roots() -> set[Box]:
    """The root grid ``run_all.py`` builds with its default options."""
    xs = [(PITCH * i, PITCH * (i + 1)) for i in range(int(SIDE / PITCH))]
    cuts = sorted(
        {-U_HALF + U_HALF * k / UBINS for k in range(UBINS + 1)}
        | {U_HALF * k / UBINS for k in range(UBINS + 1)}
    )
    us = list(pairwise(cuts))
    return {(x0, x1, y0, y1, u0, u1) for x0, x1 in xs for y0, y1 in xs for u0, u1 in us}


def grid_problems(records: list[RecordStats]) -> list[str]:
    """The roots of all records together are the grid, each once, split at ``SPLIT_X``."""
    problems: list[str] = []
    seen: Counter[Box] = Counter()
    for stats in records:
        seen.update(stats.roots)
        if stats.name == "full.jsonl" and any(box[0] >= SPLIT_X for box in stats.roots):
            problems.append("full.jsonl has a root with x >= 11/2")
        if stats.name == "full_b.jsonl" and any(box[0] < SPLIT_X for box in stats.roots):
            problems.append("full_b.jsonl has a root with x < 11/2")
    grid = expected_roots()
    if repeated := sum(1 for count in seen.values() if count > 1):
        problems.append(f"{repeated} roots appear more than once")
    if missing := len(grid - set(seen)):
        problems.append(f"{missing} grid roots are missing")
    if extra := len(set(seen) - grid):
        problems.append(f"{extra} roots are not grid roots")
    return problems


def header_problems(stats: RecordStats, tree: Path, cover: Path) -> list[str]:
    """Every digest the header names is that of the retained file it names."""
    problems: list[str] = []
    named = cast("dict[str, str]", stats.header.get("sha256", {}))
    if not named:
        return [f"{stats.name}: the header names no files"]
    for key, digest in sorted(named.items()):
        if key == "cover/L4_k02_box7.txt":
            path = cover
        elif stats.name == V1_RECORD and key in V1_FILES:
            path = tree / V1_FILES[key]
        else:
            path = tree / key
        if not path.is_file():
            problems.append(f"{stats.name}: {key} is not retained")
        elif (actual := _sha256(path)) != digest:
            problems.append(
                f"{stats.name}: {key} is {actual[:16]}, the header says {digest[:16]}"
            )
    return problems


def audit(
    records_dir: Path,
    tree: Path = TREE,
    sums: Path = PACKET / "release/records.sha256",
    cover: Path = COVER,
) -> dict[str, object]:
    """Read both records and return the receipt, with ``ok`` and every problem found."""
    expected = read_sums(sums)
    problems: list[str] = []
    if _sha256(cover) != COVER_SHA256:
        problems.append("the retained cover is not c0a67509")
    stats = [read_record(records_dir / f"{name}.gz") for name in RECORDS]
    for record in stats:
        if expected.get(f"{record.name}.gz") != record.sha256_compressed:
            problems.append(f"{record.name}.gz does not have the release digest")
        if expected.get(record.name) != record.sha256_decompressed:
            problems.append(f"{record.name} does not have the release digest")
        problems += header_problems(record, tree, cover)
        if record.uncertified or record.counterexamples:
            bad = f"{record.uncertified} uncertified, {record.counterexamples} counterexamples"
            problems.append(f"{record.name}: {bad}")
    problems += grid_problems(stats)
    leaves = sum((record.leaves for record in stats), Counter[str]())
    cpu = sum(record.cpu_seconds for record in stats)
    if leaves.total() != STATED_LEAVES:
        problems.append(f"{leaves.total()} leaves, the source states {STATED_LEAVES}")
    return {
        "kind": "valid7-independent-records-audit/v1",
        "ok": not problems,
        "problems": problems,
        "records": [
            {
                "name": record.name,
                "sha256_compressed": record.sha256_compressed,
                "sha256_decompressed": record.sha256_decompressed,
                "header_argv": record.header.get("argv"),
                "header_sha256": record.header.get("sha256"),
                "roots": len(record.roots),
                "leaves": dict(sorted(record.leaves.items())),
                "uncertified": record.uncertified,
                "counterexamples": record.counterexamples,
                "cpu_core_hours": round(record.cpu_seconds / 3600, 2),
            }
            for record in stats
        ],
        "grid_roots": len(expected_roots()),
        "leaves": leaves.total(),
        "leaf_kinds": dict(sorted(leaves.items())),
        "cpu_core_hours": round(cpu / 3600, 2),
        "stated": {"leaves": STATED_LEAVES, "core_hours": STATED_CORE_HOURS},
        "not_checked": (
            "No leaf's bound is recomputed here; check_record.py --recheck/--recheck-b "
            "re-certify a sample, and the run itself is the source's."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--records", type=Path, required=True, help="directory holding the two .jsonl.gz files"
    )
    parser.add_argument("--out", type=Path, required=True, help="JSON receipt to write")
    args = parser.parse_args(argv)
    receipt = audit(args.records)
    atomic_write_text(args.out, json.dumps(receipt, indent=2) + "\n")
    for problem in cast("list[str]", receipt["problems"]):
        print("PROBLEM", problem)
    print("VALID7_RECORDS_AUDIT_OK" if receipt["ok"] else "VALID7_RECORDS_AUDIT_FAILED")
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
