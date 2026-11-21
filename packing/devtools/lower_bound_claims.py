#!/usr/bin/env python3
"""Classify a batch of reported lower bounds against the case records, in report order.

An intake of lower bounds at many counts needs the same three answers at every count,
and this module is the one place they are computed (OR-1): where each claimed side
stands against the case record's two lower lanes, whether a smaller count's lane
already gives as much by monotonicity, and which of several reports at one count the
owner's report-order rule of 14 October 2026 records ("each one should be recorded as a
result, as long as each one is stronger than the last",
`campaign/result-import.md` → Several Reports at One Count). The upper-bound walk,
`devtools.intake_ledger`, reads upper bounds only; this reads lower ones.

The input is a YAML file of reports in the order they reached the repository:

```yaml
start: {main: <commit>}             # the main commit the case records were read at
reports:
  - id: issue-1039                  # any key
    reported_at: '2026-11-19T04:49:37Z'
    claims:
      - {n: 19, rational: '<p/q>'}  # the claimed side, exactly
      - {n: 101, sqrt: '<p/q>'}     # the positive square root of a rational
      - {n: 102, sqrt: '<p/q>', from_n: 101}   # a consequence of monotonicity
```

Each claim is compared exactly with the case record's `verified_lower_bound` and
`reported_lower_bound`, each read as `render_recent_results.span`'s interval (an exact
form where it is a number, and a closed form's printed value one unit either way of its
last place); a square root is compared by squares. A claim is

- `above` a lane when every number it may be exceeds every number the lane may be,
- `equal` when the two meet, and `below` otherwise;

and `new` when it is above both lanes and above the monotone floor, the stronger lane at
every smaller count; a claim that is not is `not-an-improvement`. A new claim no greater
than a claim at a smaller count, which monotonicity carries up, is a `consequence` where
that claim is its own report's and equal to it (the parent's scope covers it), and
`weaker` where it is an earlier report's. In report order, at each count a claim is
`recorded` when it is new and strictly above every claim recorded there before it, and
`weaker` when it is not; a recorded claim or consequence a later one passes is
`superseded`, and the last one recorded is `current`. A tie stays with the earlier
report. Nothing here reads a certificate: it decides standing and order, never whether
a claim is true.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.lower_bound_claims \\
        CLAIMS.yaml [--out RECEIPT.json] [--table TABLE.md]

`--check RECEIPT.json` recomputes the receipt and fails if it differs.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Mapping, Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.build_bound_citations import load_case
from devtools.render_recent_results import span
from sqpack.yamlio import safe_load

ABOVE = "above"
EQUAL = "equal"
BELOW = "below"
LANES = ("verified", "reported")
FORMAT = "lower-bound-claims/v1"


def side(claim: Mapping[str, Any]) -> tuple[str, Fraction]:
    """The claimed side as (kind, number): `rational` is the side, `sqrt` its square."""
    kinds = [kind for kind in ("rational", "sqrt") if kind in claim]
    if len(kinds) != 1:
        raise ValueError(f"claim at n = {claim.get('n')} needs one of rational or sqrt")
    value = Fraction(str(claim[kinds[0]]))
    if value <= 0:
        raise ValueError(f"claim at n = {claim['n']} is not positive")
    return kinds[0], value


def against(kind: str, value: Fraction, low: Fraction, high: Fraction) -> str:
    """Where a claimed side stands against the closed interval [low, high]."""
    if kind == "sqrt":
        if low <= 0:
            return ABOVE
        low_test, high_test = low * low, high * high
    else:
        low_test, high_test = low, high
    if value > high_test:
        return ABOVE
    if value < low_test:
        return BELOW
    return EQUAL


def decimal(kind: str, value: Fraction, places: int = 12) -> str:
    """The side rounded down at `places`, for reading only."""
    scale = 10**places
    if kind == "sqrt":
        scaled = _isqrt_fraction(value * scale * scale)
    else:
        scaled = value.numerator * scale // value.denominator
    whole, part = divmod(scaled, scale)
    return f"{whole}.{part:0{places}d}"


def _isqrt_fraction(value: Fraction) -> int:
    """The floor of the square root of a positive rational."""
    guess = math.isqrt(value.numerator // value.denominator)
    while Fraction((guess + 1) ** 2) <= value:
        guess += 1
    while Fraction(guess**2) > value:
        guess -= 1
    return guess


def lanes(n: int) -> dict[str, dict[str, Any] | None]:
    """The case record's two lower lanes at `n`, as written."""
    case = load_case(n)
    return {lane: case.get(f"{lane}_lower_bound") for lane in LANES}


def _shown(bound: Mapping[str, Any] | None) -> str | None:
    return None if bound is None else str(bound["value"])


def lane_span(bound: Mapping[str, Any] | None) -> tuple[Fraction, Fraction] | None:
    return None if not bound else span(bound)


def classify(data: Mapping[str, Any]) -> dict[str, Any]:
    """The receipt: every claim's standing against the record and its report-order verdict."""
    reports = list(data["reports"])
    counts = sorted({int(claim["n"]) for report in reports for claim in report["claims"]})
    spans: dict[int, dict[str, tuple[Fraction, Fraction] | None]] = {}
    shown: dict[int, dict[str, str | None]] = {}
    for n in range(1, max(counts) + 1):
        found = lanes(n)
        spans[n] = {lane: lane_span(found[lane]) for lane in LANES}
        shown[n] = {lane: _shown(found[lane]) for lane in LANES}
    floor_low: dict[int, Fraction] = {}
    floor_from: dict[int, int] = {}
    best_low, best_at = Fraction(0), 0
    for n in range(1, max(counts) + 1):
        for got in spans[n].values():
            if got and got[0] > best_low:
                best_low, best_at = got[0], n
        floor_low[n], floor_from[n] = best_low, best_at

    rows: list[dict[str, Any]] = []
    held: dict[int, tuple[str, Fraction, int]] = {}
    for order, report in enumerate(reports):
        for claim in report["claims"]:
            n = int(claim["n"])
            kind, value = side(claim)
            row: dict[str, Any] = {
                "report": str(report["id"]),
                "order": order,
                "n": n,
                "kind": kind,
                "value": str(value),
                "decimal": decimal(kind, value),
                "from_n": int(claim.get("from_n", n)),
            }
            for lane in LANES:
                got = spans[n][lane]
                row[f"{lane}_lane"] = shown[n][lane]
                row[f"against_{lane}"] = None if got is None else against(kind, value, *got)
            row["monotone_floor_from"] = floor_from[n]
            row["against_monotone_floor"] = against(kind, value, floor_low[n], floor_low[n])
            below = _claimed_floor(reports, order, n)
            row["claimed_floor"] = below[0] if below else None
            exceeds_floor = below is None or _exceeds((kind, value), below[1][1])
            row["above_claimed_floor"] = exceeds_floor
            row["new"] = (
                all(row[f"against_{lane}"] in (ABOVE, None) for lane in LANES)
                and row["against_monotone_floor"] == ABOVE
            )
            previous = held.get(n)
            if not row["new"]:
                row["order_verdict"] = "not-an-improvement"
            elif below is not None and not exceeds_floor:
                same = below[1][0] == order and not _exceeds(below[1][1], (kind, value))
                row["order_verdict"] = "consequence" if same else "weaker"
                if same:
                    row["consequence_of"] = below[0]
                    held[n] = (kind, value, len(rows))
            elif previous is not None and not _exceeds((kind, value), previous[:2]):
                row["order_verdict"] = "weaker"
                row["weaker_than"] = rows[previous[2]]["report"]
            else:
                row["order_verdict"] = "recorded"
                if previous is not None:
                    rows[previous[2]]["order_verdict"] = "superseded"
                    rows[previous[2]]["superseded_by"] = str(report["id"])
                held[n] = (kind, value, len(rows))
            rows.append(row)
    for _, _, index in held.values():
        if rows[index]["order_verdict"] == "recorded":
            rows[index]["order_verdict"] = "current"
    return {
        "format": FORMAT,
        "start": dict(data.get("start") or {}),
        "reports": [
            {
                "id": str(report["id"]),
                "reported_at": str(report["reported_at"]),
                "claims": len(report["claims"]),
            }
            for report in reports
        ],
        "rows": rows,
        "summary": summary(rows),
    }


def _claimed_floor(
    reports: Sequence[Mapping[str, Any]], order: int, n: int
) -> tuple[str, tuple[int, tuple[str, Fraction]]] | None:
    """The strongest claim at a smaller count in this report or an earlier one, which
    gives as much at `n` by monotonicity: its label, its report's order and its side."""
    best: tuple[str, tuple[int, tuple[str, Fraction]]] | None = None
    for index, report in enumerate(reports[: order + 1]):
        for claim in report["claims"]:
            if int(claim["n"]) < n:
                found = side(claim)
                if best is None or _exceeds(found, best[1][1]):
                    best = (f"{report['id']} at {claim['n']}", (index, found))
    return best


def _exceeds(new: tuple[str, Fraction], old: tuple[str, Fraction]) -> bool:
    """Whether one claimed side is strictly greater than another, exactly."""
    return _square(new) > _square(old)


def _square(claim: tuple[str, Fraction]) -> Fraction:
    kind, value = claim
    return value if kind == "sqrt" else value * value


def summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, int]]:
    tally: dict[str, dict[str, int]] = {}
    for row in rows:
        per = tally.setdefault(str(row["report"]), {})
        verdict = str(row["order_verdict"])
        per[verdict] = per.get(verdict, 0) + 1
    return tally


def table(receipt: Mapping[str, Any]) -> str:
    """The receipt as one Markdown table, a row per claim in report order."""
    lines = [
        (
            "| Report | n | Claimed side (down, 12 places) | Verified lane | Reported lane | "
            "vs verified | vs reported | Monotone floor from | Verdict |"
        ),
        "| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |",
    ]
    for row in receipt["rows"]:
        via = f" (from {row['from_n']})" if row["from_n"] != row["n"] else ""
        verdict = str(row["order_verdict"])
        if row.get("superseded_by"):
            verdict += f" by {row['superseded_by']}"
        if row.get("consequence_of"):
            verdict += f" (equal to {row['consequence_of']})"
        lines.append(
            f"| {row['report']} | {row['n']}{via} | {row['decimal']} | "
            f"{row['verified_lane']} | {row['reported_lane']} | {row['against_verified']} | "
            f"{row['against_reported']} | {row['monotone_floor_from']} | {verdict} |"
        )
    return "\n".join(lines) + "\n"


def render(receipt: Mapping[str, Any]) -> str:
    """The receipt as the JSON text `--out` writes and `--check` compares."""
    return json.dumps(receipt, indent=1, sort_keys=True) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    parser.add_argument("claims", type=Path)
    parser.add_argument("--out", type=Path, help="write the JSON receipt here")
    parser.add_argument("--table", type=Path, help="write the Markdown table here")
    parser.add_argument("--check", type=Path, help="fail unless this receipt is current")
    args = parser.parse_args(argv)
    receipt = classify(safe_load(args.claims.read_text(encoding="utf-8")))
    text = render(receipt)
    if args.check is not None:
        if args.check.read_text(encoding="utf-8") != text:
            print(f"{args.check} is not current; rerun with --out", file=sys.stderr)
            return 1
        print(f"{args.check} is current ({len(receipt['rows'])} claims)")
        return 0
    if args.out is not None:
        args.out.write_text(text, encoding="utf-8")
    if args.table is not None:
        args.table.write_text(table(receipt), encoding="utf-8")
    for report, tally in receipt["summary"].items():
        print(report, json.dumps(tally, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
