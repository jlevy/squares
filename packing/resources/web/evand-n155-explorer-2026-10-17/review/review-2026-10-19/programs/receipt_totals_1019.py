"""Sum each packet's retained receipt with `upper_bound_reports.receipt_summary`.

Written for the stage 4 review of 19 October 2026; it decides nothing. For each packet it
prints the jobs, pair decisions, route CPU seconds and job wall seconds of its receipt,
and each positive job's two margins as both routes state them, exactly and to four
significant digits.

Usage, from ``packing/`` with the project interpreter::

    python -I receipt_totals_1019.py PACKET...
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from devtools import evand_arrangement_reports as kernel  # noqa: E402
from devtools import upper_bound_reports as upper  # noqa: E402


def main(argv: list[str]) -> int:
    for name in argv:
        packet = upper.packet_path(name)
        record = kernel.read_xz(packet / upper.RECEIPT)
        summary = upper.receipt_summary(record)
        (positive,) = [row for row in record["cases"] if row["control"] == "positive"]
        margins = {
            route: {
                field: (
                    positive[route][field],
                    f"{float(Fraction(positive[route][field])):.4e}",
                )
                for field in ("minimum_containment_clearance", "minimum_best_pair_gap")
            }
            for route in ("exact_verify", "independent")
        }
        print(json.dumps({"packet": name, "summary": summary, "positive_margins": margins}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
