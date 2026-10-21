"""Exact margins of the #703 certificate against every result registered at 270.

Each registered side is rebuilt from its own retained packet through the importer's
house readers (`upper_bound_reports.HOUSES`), not read from the frozen claims record;
T-056 is Couzo's binary64 print, taken as the exact binary64 value. The pending reports
(#593, #573, Mishapolk's census) are then compared from the frozen claims record, which
is the record's statement of them. Every difference is exact; the 16-place ceilings are
rounded up.

Usage, from packing/ with the project interpreter:
    python -I margins_708.py CERT CLAIMS_JSON OUT.json
"""

from __future__ import annotations

import json
from decimal import Decimal
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from devtools import upper_bound_reports as reports  # noqa: E402

REGISTERED = (
    ("T-174", "[PingYou PR 574 certificates 2026-10-13]", "Chaoweeraprasit, improved by PingYou Ltd; the house best packing"),
    ("T-151", "[SQUISH fourth request 2026-10-11]", "Chaoweeraprasit (#500)"),
    ("T-140", "[Couzo certificates 2026-10-10]", "Couzo (#488)"),
    ("T-136", "[SQUISH third request 2026-10-09]", "Chaoweeraprasit (#481)"),
    ("T-134", "[Couzo exact certificates 2026-10-09]", "Couzo (#476)"),
    ("T-130", "[Couzo follow-up refinements 2026-10-08]", "Couzo (#460)"),
    ("T-138", "[Mishapolk decimal poses 2026-10-09]", "Polkovskyi (#470)"),
    ("T-119", "[Daniel new arrangements 2026-10-07]", "Daniel (#399)"),
    ("T-098", "[evand exact optima 2026-10-05]", "Daniel, at Couzo's packing (#375)"),
)
T056_PRINT = "16.937810329390629"


def ceil16(v: Fraction) -> str:
    scaled = -(-v.numerator * 10**16 // v.denominator)
    text = str(scaled)
    return text[:-16] + "." + text[-16:]


def main(argv: list[str]) -> int:
    cert, claims_path, out = Path(argv[1]), Path(argv[2]), Path(argv[3])
    header = next(ln for ln in cert.read_text("ascii").split("\n") if ln.strip() and not ln.startswith("#"))
    side = Fraction(header.split()[1])
    rows = []
    for entry, key, who in REGISTERED:
        other = reports.house_side(key, 270)
        rows.append({"entry": entry, "who": who, "side_16_up": ceil16(other), "difference": str(other - side), "difference_float": f"{float(other - side):.6e}", "relation": "above this certificate" if other > side else "not above"})
    other = Fraction(Decimal(T056_PRINT))
    rows.append({"entry": "T-056", "who": "Couzo (decimal print, as the record reads it)", "side_16_up": ceil16(other), "difference": str(other - side), "difference_float": f"{float(other - side):.6e}", "relation": "above this certificate" if other > side else "not above"})
    claims = json.loads(claims_path.read_text("utf-8"))
    (row,) = claims["results"]
    frozen = {}
    frozen["case"] = (row["case"]["result"], Fraction(row["case"]["exact_side"]) - side == Fraction(row["case"]["difference"]))
    for pending in row["pending"]:
        if "exact_side" in pending:
            frozen[pending["report"]] = (f"{float(Fraction(pending['exact_side']) - side):.6e}", Fraction(pending["exact_side"]) - side == Fraction(pending["difference"]))
        else:
            frozen[pending["report"]] = (f"{float(Fraction(Decimal(pending['printed'])) - side):.6e}", Fraction(Decimal(pending["printed"])) - side == Fraction(pending["difference"]))
    smallest = min(rows, key=lambda r: Fraction(r["difference"]))
    result = {
        "this_side": str(side),
        "this_16_up": ceil16(side),
        "registered": rows,
        "all_registered_above": all(r["relation"] == "above this certificate" for r in rows),
        "nearest_registered": smallest["entry"],
        "frozen_claims_record_rebuilt_equal": frozen,
        "smallest_at_270": "this certificate (#703, T-224)" if all(r["relation"] == "above this certificate" for r in rows) else "NOT this certificate",
    }
    out.write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
