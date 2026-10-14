"""Both upper lanes of the case record at every in-horizon count of the ledger.

For each count the 2026-10-14 ledger claims at, n <= 324, print the case record's reported
and verified upper bounds (value, exact form, evidence), and flag a count where the
verified lane is below the reported one or where the two lanes' exact forms differ. The
review of 2026-10-14 ran this against `main` f73e9de13; `packing/frontier/` was unchanged
when this copy was made, so the same command reproduces `cases-scan.txt`.

From `packing/`, with the project interpreter::

    python campaign/issue-intake/upper-bounds-20261014/review/scan_cases.py
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml

#: The repository root: this file is packing/campaign/issue-intake/<directory>/review/.
REPO = Path(__file__).resolve().parents[5]
PACKING = REPO / "packing"
FRONTIER = PACKING / "frontier"
LEDGER = PACKING / "campaign/issue-intake/upper-bounds-20261014/ledger.yaml"
HORIZON = 324


def case(n: int) -> dict[str, Any]:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---\n")[1])["packing"]


def counts() -> list[int]:
    ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    found = {claim["n"] for report in ledger["reports"] for claim in report["claims"]}
    return sorted(n for n in found if n <= HORIZON)


def main() -> None:
    flagged = []
    for n in counts():
        record = case(n)
        reported, verified = record["reported_upper_bound"], record["verified_upper_bound"]
        reported_value, verified_value = str(reported["value"]), str(verified["value"])
        reported_form, verified_form = reported.get("exact_form"), verified.get("exact_form")
        mark = ""
        if Fraction(Decimal(verified_value)) < Fraction(Decimal(reported_value)):
            mark += " VERIFIED<REPORTED"
        if reported_form != verified_form:
            mark += " FORMS-DIFFER"
        if mark:
            flagged.append(n)
        print(
            f"n={n:3d} reported={reported_value} ({reported.get('source_key')}; "
            f"form={reported_form}) | verified={verified_value} (form={verified_form}; "
            f"evidence={verified.get('evidence')}){mark}"
        )
    print("flagged:", flagged)


if __name__ == "__main__":
    main()
