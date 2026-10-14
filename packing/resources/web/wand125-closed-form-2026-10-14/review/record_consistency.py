#!/usr/bin/env python3
"""a(N) against every bound the case records hold, and against the known exact values.

A lower bound that is correct can never exceed a correct upper bound, and where s(N) is
known exactly it can at most reach it. This program takes the enclosures of a(N) that
review/a_of_n_by_definition.py wrote (review/outputs/a_by_definition.json) and, for every
non-square count from 49 to 324, reads the front matter of packing/frontier/n-NNN.md with
PyYAML and compares a(N) with the four lanes: the reported and verified upper bounds (a(N)
must not exceed them) and the reported and verified lower bounds (counted above, equal or
below, to compare with the intake evaluation's table). Each bound is read from its decimal
`value`; an enclosure that cannot be placed against a value is reported as undecided
rather than counted.

It then checks the values the source says its bound recovers: a(N) = m exactly at
N = m^2 - 1, m^2 - 2 and m^2 - 3 for m = 8, ..., 18, which the case records hold as
proved, and a(N) < m at N = m^2 - 4, which is also known to be m. Finally it checks that
a(N) <= k + 1 everywhere, and reports whether a(N) is nondecreasing in N, which is not
required of a lower bound and is printed as information.

Run from packing/ with the project interpreter, after a_of_n_by_definition.py:

    uv run --frozen --all-extras --group dev python -I \\
        resources/web/wand125-closed-form-2026-10-14/review/record_consistency.py \\
        --out resources/web/wand125-closed-form-2026-10-14/review/outputs/consistency.json

It decides nothing about the certificate: a bound consistent with the record can still
be unproved, and this program only looks for a contradiction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Q
from itertools import pairwise
from math import isqrt
from pathlib import Path
from typing import Any

import yaml

sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
PACKING = PACKET.parents[2]
FRONTIER = PACKING / "frontier"
ENCLOSURES = HERE / "outputs" / "a_by_definition.json"

LANES = (
    "reported_upper_bound",
    "verified_upper_bound",
    "reported_lower_bound",
    "verified_lower_bound",
)


def emit(line: str) -> None:
    sys.stdout.write(line + "\n")


def front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        msg = f"{path.name}: no front matter"
        raise ValueError(msg)
    body = text[4:].split("\n---\n", 1)[0]
    return yaml.safe_load(body)["packing"]


def relation(lo: Q, hi: Q, bound: Q) -> str:
    """How the number enclosed by [lo, hi] stands to bound: '>', '=', '<' or '?'."""
    if lo > bound:
        return ">"
    if hi < bound:
        return "<"
    if lo == hi == bound:
        return "="
    return "?"


def ranges(ns: list[int]) -> str:
    out: list[str] = []
    run: list[int] = []
    for n in sorted(ns):
        if run and n == run[-1] + 1:
            run.append(n)
            continue
        if run:
            out.append(f"{run[0]}-{run[-1]}" if len(run) > 1 else str(run[0]))
        run = [n]
    if run:
        out.append(f"{run[0]}-{run[-1]}" if len(run) > 1 else str(run[0]))
    return ", ".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first", type=int, default=49)
    parser.add_argument("--last", type=int, default=324)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    receipt_in = json.loads(ENCLOSURES.read_text(encoding="utf-8"))
    enclosures = {int(r["N"]): (Q(r["lo"]), Q(r["hi"])) for r in receipt_in["rows"]}
    problems: list[str] = []
    rows: list[dict[str, Any]] = []
    tallies: dict[str, dict[str, list[int]]] = {lane: {} for lane in LANES}
    for n in range(args.first, args.last + 1):
        k = isqrt(n)
        if k * k == n:
            continue
        lo, hi = enclosures[n]
        case = front_matter(FRONTIER / f"n-{n:03d}.md")
        row: dict[str, Any] = {
            "N": n,
            "k": k,
            "lo": str(lo),
            "hi": str(hi),
            "status": case.get("status"),
        }
        if hi > k + 1:
            problems.append(f"{n}: a(N) above k + 1")
        for lane in LANES:
            record = case[lane]
            bound = Q(str(record["value"]))
            rel = relation(lo, hi, bound)
            row[lane] = {"value": str(record["value"]), "relation": rel}
            tallies[lane].setdefault(rel, []).append(n)
            if rel == "?":
                problems.append(f"{n}: undecided against {lane} = {record['value']}")
            if lane.endswith("upper_bound") and rel == ">":
                problems.append(f"{n}: a(N) exceeds {lane} = {record['value']}")
        rows.append(row)

    # The known exact values at the top of each block, m = 8..18 within 49..324.
    tops: dict[str, list[int]] = {"equal_at_m2_minus_1_2_3": [], "below_at_m2_minus_4": []}
    for m in range(8, isqrt(args.last + 4) + 2):
        for j in (1, 2, 3):
            n = m * m - j
            if args.first <= n <= args.last:
                lo, hi = enclosures[n]
                case = front_matter(FRONTIER / f"n-{n:03d}.md")
                exact = lo == hi == m
                proved = (
                    case.get("status") == "proved"
                    and Q(str(case["verified_upper_bound"]["value"])) == m
                )
                if exact and proved:
                    tops["equal_at_m2_minus_1_2_3"].append(n)
                else:
                    problems.append(
                        f"{n} = {m}^2 - {j}: a(N) = [{lo}, {hi}], case proved {proved}"
                    )
        n = m * m - 4
        if args.first <= n <= args.last:
            lo, hi = enclosures[n]
            if hi < m:
                tops["below_at_m2_minus_4"].append(n)
            else:
                problems.append(f"{n} = {m}^2 - 4: a(N) = [{lo}, {hi}] is not below {m}")

    ns = sorted(enclosures)
    monotone = all(
        enclosures[a][1] <= enclosures[b][0] or enclosures[a][0] <= enclosures[b][0]
        for a, b in pairwise(ns)
    )
    summary = {
        "non_square_counts": len(rows),
        "lanes": {
            lane: {rel: {"count": len(v), "n": ranges(v)} for rel, v in sorted(t.items())}
            for lane, t in tallies.items()
        },
        "known_values": {key: ranges(v) for key, v in tops.items()},
        "a_nondecreasing_in_N_over_the_receipt": monotone,
        "problems": problems,
    }
    for lane, t in summary["lanes"].items():
        emit(f"{lane}: " + "; ".join(f"{rel} {v['count']} ({v['n']})" for rel, v in t.items()))
    for key, value in summary["known_values"].items():
        emit(f"{key}: {value}")
    emit(f"a(N) nondecreasing in N: {monotone}")
    emit(f"problems: {problems or 'none'}")
    receipt = {
        "schema": "closed-form-review-record-consistency/v1",
        "program": "review/record_consistency.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "enclosures_sha256": hashlib.sha256(ENCLOSURES.read_bytes()).hexdigest(),
        "summary": summary,
        "rows": rows,
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    emit("RECORD CONSISTENCY OK" if not problems else "RECORD CONSISTENCY NG")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
