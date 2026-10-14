#!/usr/bin/env python3
"""The arithmetic of the source's replay receipt, and the digest chain it rests on.

receipts/replay.json records one complete replay of the 136 records by replay4d. Twenty-
five records were cut along grid lines into pieces for that run, each piece replayed as
a record over a sub-box; the receipt gives each piece's bounds, root count and the sum
modulo 2^256 of the SHA-256 digests of its lines. The source says the pieces tile the
region and that the sums are a consistency check, not a proof. This program decides what
the receipt itself allows:

- for every split record, the pieces' bounds are rectangles that tile the region's
  bounds of intervals.json exactly (equal total area, pairwise disjoint interiors, inside
  the region), their root counts add up to the record's, and their line-hash sums add up
  modulo 2^256 to the record's;
- for every record, the receipt's `roots` and `leaves` equal intervals.json's, every
  run is `ok`, and the CPU hours add up to the stated total;
- the digest chain: every record digest in replay.json equals the published record's in
  intervals.json; every family digest in replay.json is the `old_sha256` that
  receipts/families.json maps to the published `new_sha256` of intervals.json; and the
  published-build receipt receipts/published_checker.json replayed intervals 1 and 34
  with the published family digests and the same record digests.

Run from packing/ with the project interpreter:

    uv run --frozen --all-extras --group dev python -I \\
        resources/web/wand125-closed-form-2026-10-14/review/replay_receipt_pieces.py

It reads the retained receipts and intervals.json.gz, every one refused unless its SHA-256
is the packet manifest's. It decides nothing about any leaf: a receipt is the author's
statement, and this program checks only that the statement is consistent with itself and
names the published files.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
FOLDER = PACKET / "square-packing" / "problems" / "closed-form"
MANIFEST = PACKET / "acquisition" / "upstream-subtree.sha256"
MASK = (1 << 256) - 1
REGIONS = ("straddle", "left", "top", "right")


def emit(line: str) -> None:
    sys.stdout.write(line + "\n")


def pinned(relative: str) -> bytes:
    """The decompressed bytes of a retained upstream file, checked against the manifest."""
    want = next(
        line.split("  ")[0]
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.endswith("problems/closed-form/" + relative)
    )
    path = FOLDER / relative
    data = (
        gzip.decompress(path.with_suffix(path.suffix + ".gz").read_bytes())
        if not path.exists()
        else path.read_bytes()
    )
    got = hashlib.sha256(data).hexdigest()
    if got != want:
        msg = f"{relative}: SHA-256 {got} is not the manifest's {want}"
        raise SystemExit(msg)
    return data


def rect(bounds: list[str]) -> tuple[Q, Q, Q, Q]:
    x0, x1, y0, y1 = (Q(b) for b in bounds)
    if not (x0 < x1 and y0 < y1):
        msg = f"degenerate bounds {bounds}"
        raise ValueError(msg)
    return x0, x1, y0, y1


def tiles(pieces: list[tuple[Q, Q, Q, Q]], region: tuple[Q, Q, Q, Q]) -> bool:
    x0, x1, y0, y1 = region
    inside = all(x0 <= p[0] and p[1] <= x1 and y0 <= p[2] and p[3] <= y1 for p in pieces)
    area = sum(((p[1] - p[0]) * (p[3] - p[2]) for p in pieces), Q(0))
    disjoint = all(
        a[1] <= b[0] or b[1] <= a[0] or a[3] <= b[2] or b[3] <= a[2]
        for i, a in enumerate(pieces)
        for b in pieces[i + 1 :]
    )
    return inside and disjoint and area == (x1 - x0) * (y1 - y0)


def main() -> int:
    intervals = json.loads(pinned("intervals.json"), parse_float=str)["intervals"]
    replay = json.loads(pinned("receipts/replay.json"))
    families = json.loads(pinned("receipts/families.json"))
    published = json.loads(pinned("receipts/published_checker.json"))
    by_label = {
        (f"{'(' if iv['open_left'] else '['}{iv['d0_decimal']}, {iv['d1_decimal']}]"): iv
        for iv in intervals
    }
    problems: list[str] = []
    stats: dict[str, Any] = {
        "records": 0,
        "split_records": 0,
        "pieces": 0,
        "runs": 0,
        "cpu_hours": Q(0),
    }
    old_to_new = {
        (f["interval"], f["file"]): (f["old_sha256"], f["new_sha256"])
        for f in families["families"]
    }
    for r in replay["results"]:
        stats["records"] += 1
        stats["runs"] += r["runs"]
        stats["cpu_hours"] += Q(str(r["cpu_hours"]))
        iv = by_label.get(r["interval"])
        if iv is None:
            problems.append(f"{r['interval']} {r['region']}: no such interval label")
            continue
        region = iv["regions"][r["region"]]
        where = f"I{iv['index']} {r['region']}"
        if not r["ok"]:
            problems.append(f"{where}: not ok")
        if (r["roots"], r["leaves"]) != (region["roots"], region["leaves"]):
            problems.append(f"{where}: roots or leaves differ from intervals.json")
        if r["record_sha256"] != region["sha256"]:
            problems.append(f"{where}: record digest is not the published record's")
        old, new = old_to_new[(iv["index"], region["family"])]
        if r["family_sha256"] != old:
            problems.append(f"{where}: family digest is not families.json's old digest")
        if (
            new
            != iv[
                (
                    "family_right_sha256"
                    if region["family"] == "family_right.json"
                    else "family_sha256"
                )
            ]
        ):
            problems.append(f"{where}: families.json's new digest is not intervals.json's")
        split = r.get("split")
        if split:
            stats["split_records"] += 1
            pieces = split["pieces"]
            stats["pieces"] += len(pieces)
            if len(pieces) != r["runs"]:
                problems.append(f"{where}: {len(pieces)} pieces but {r['runs']} runs")
            if not tiles([rect(p["bounds"]) for p in pieces], rect(region["bounds"])):
                problems.append(f"{where}: pieces do not tile the region")
            if sum(p["roots"] for p in pieces) != r["roots"]:
                problems.append(f"{where}: piece roots do not add up")
            total = sum(int(p["line_hash_sum"], 16) for p in pieces) & MASK
            if total != int(split["line_hash_sum"], 16):
                problems.append(f"{where}: line-hash sums do not add up modulo 2^256")
        elif r["runs"] != 1:
            problems.append(f"{where}: {r['runs']} runs for an uncut record")
    if stats["records"] != replay["records"] or stats["runs"] != replay["runs"]:
        problems.append("record or run counts differ from the receipt's totals")
    if abs(stats["cpu_hours"] - Q(str(replay["cpu_hours_total"]))) > Q(1, 2):
        problems.append(
            f"CPU hours add to {float(stats['cpu_hours'])}, not {replay['cpu_hours_total']}"
        )
    leaves = sum(r["leaves"] for r in replay["results"])
    if leaves != replay["leaves"] or leaves != sum(replay["leaves_by_kind"].values()):
        problems.append("leaf totals differ")
    # The published build's runs of intervals 1 and 34.
    runs = published["runs"]
    for run in runs:
        iv = next(i for i in intervals if i["asset"] == run["asset"])
        region = iv["regions"][run["region"]]
        new = iv[
            "family_right_sha256" if run["family"] == "family_right.json" else "family_sha256"
        ]
        if run["family_sha256"] != new or run["record_sha256"] != region["sha256"]:
            problems.append(
                f"published checker I{iv['index']} {run['region']}: not the published digests"
            )
        if (
            not run["ok"]
            or run["roots"] != region["roots"]
            or run["leaves"] != region["leaves"]
        ):
            problems.append(
                f"published checker I{iv['index']} {run['region']}: not ok or counts differ"
            )
        if run["leaves_by_kind"] != region["leaf_kinds"]:
            problems.append(
                f"published checker I{iv['index']} {run['region']}: leaf kinds differ"
            )
    stats["published_checker_runs"] = len(runs)
    stats["published_checker_intervals"] = sorted(
        {next(i["index"] for i in intervals if i["asset"] == r["asset"]) for r in runs}
    )
    stats["cpu_hours"] = float(stats["cpu_hours"])
    for key, value in stats.items():
        emit(f"{key}: {value}")
    emit(f"checker source hash of the full replay: {replay['checker_source_sha256']}")
    emit(f"checker source hash of the published build: {published['checker_source_sha256']}")
    emit(f"problems: {problems or 'none'}")
    emit("REPLAY RECEIPT OK" if not problems else "REPLAY RECEIPT NG")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
