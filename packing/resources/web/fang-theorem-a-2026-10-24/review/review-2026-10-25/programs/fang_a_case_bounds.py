#!/usr/bin/env python3
"""The case records' upper bounds at the counts the review's geometry run reaches.

Stage 4 review of issue #797, lane c-review-797-math, 25 October 2026, written after the
review's findings. For each count n <= 324 that fang_a_review.py's `geometry` subcommand
laid out square by square (k = 6 to 18, both odd widths at k = 8 and 18), it reads the
case record packing/frontier/n-NNN.md as text and decides, exactly, whether both its
reported and its verified upper bound, each read as its printed decimal plus one unit in
the last place, lie below k. It supports the caveat in record-changes.md that no case
record would cite an evidence entry for that run, and decides nothing about the theorem.

    python3 -I fang_a_case_bounds.py --frontier packing/frontier --out case-bounds.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction as Q
from pathlib import Path

#: (k, n): the construction's count N(t) at each k and odd width, from outputs/geometry.json.
PAIRS = ((6, 26), (7, 38), (8, 50), (8, 52), (9, 66), (10, 84), (11, 105), (12, 126),
         (13, 151), (14, 176), (15, 205), (16, 236), (17, 268), (18, 300), (18, 302))
LANES = ("reported_upper_bound", "verified_upper_bound")


def ceiling(printed: str) -> Q:
    whole, point, places = printed.partition(".")
    return Q(int(whole)) if not point else Q(printed) + Q(1, 10 ** len(places))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--frontier", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for k, n in PAIRS:
        path = args.frontier / f"n-{n:03d}.md"
        text = path.read_text(encoding="utf-8")
        row: dict[str, object] = {"k": k, "n": n, "case": path.name,
                                  "sha256": hashlib.sha256(text.encode()).hexdigest()}
        below = True
        for lane in LANES:
            found = re.search(lane + r":\s*\n\s*value:\s*'?([0-9.]+)", text)
            if found is None:
                row[lane] = None
                below = False
                continue
            row[lane] = found.group(1)
            below = below and ceiling(found.group(1)) < k
        row["both_below_k"] = below
        rows.append(row)
    receipt = {
        "program": Path(__file__).name,
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": sys.version.split()[0],
        "rows": rows,
        "all_below_k": all(r["both_below_k"] for r in rows),
    }
    args.out.write_text(json.dumps(receipt, indent=1) + "\n")
    for r in rows:
        print(r["k"], r["n"], r["reported_upper_bound"], r["verified_upper_bound"], r["both_below_k"])
    print("all below k:", receipt["all_below_k"])
    return 0 if receipt["all_below_k"] else 1


if __name__ == "__main__":
    sys.exit(main())
