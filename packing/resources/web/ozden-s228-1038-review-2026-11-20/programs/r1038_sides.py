"""The sides at 228 and their differences, exactly; written after the findings were frozen.

Usage: python -I -B r1038_sides.py CERTIFICATE CASE_RECORD CONTRACTION_JSON KKT_REPORT_GZ SOURCE_SLICE OUT_JSON

It reads the certificate's side through the frozen reader; the record's exact side from
the case record's front matter (`reported_upper_bound.exact_form`); T-301's contraction
margin from `devtools.contraction_margin`'s receipt; the side of the KKT point the
record holds at row 3 from the regularization driver's report (`solve.S_exact`, a
63-place decimal, and `solve.S_cert`, a rational); and jazivxt's printed side from the
first line of the source's decimal slice. It decides arithmetic only.
"""

from __future__ import annotations

import gzip
import json
import os
import re
import sys
from decimal import Decimal
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1038_decide as decide  # noqa: E402
import r1038_reader as reader  # noqa: E402

FACTOR = Fraction(2500000000000011391221, 2500000000000000000000)
NEVSKA = "15.596043116631669919627353"  # the leaderboard entry as the issue and the record print it


def main(argv: list[str]) -> int:
    cert_path, case_path, contraction_path, report_path, slice_path, out_path = argv[1:7]
    side = reader.read_path(cert_path).side
    with open(case_path, encoding="utf-8") as handle:
        case = handle.read()
    match = re.search(r"reported_upper_bound:\n(?:    .*\n)*?    exact_form: ([0-9]+/[0-9]+)\n", case)
    assert match, "no exact form in the case record"
    house = Fraction(match.group(1))
    with open(contraction_path, encoding="utf-8") as handle:
        contraction = json.load(handle)
    assert Fraction(contraction["side"]) == house, "the contraction receipt is not of the house"
    margin = Fraction(contraction["margin"])
    with gzip.open(report_path, "rt", encoding="utf-8") as handle:
        report = json.load(handle)
    kkt_exact = Fraction(Decimal(report["solve"]["S_exact"]))
    kkt_cert = Fraction(report["solve"]["S_cert"])
    with open(slice_path, encoding="utf-8") as handle:
        first = handle.readline().split()
    assert first[0] == "228"
    jazivxt = Fraction(Decimal(first[1]))
    eps = FACTOR - 1
    side0 = (side + eps) / FACTOR
    shrunk = house - margin

    def row(value: Fraction) -> dict[str, str]:
        return {"exact": str(value), "decimal": decide.decimal(value, 12)}

    out = {
        "program": "r1038_sides.py",
        "sides": {
            "certificate": decide.fixed(side, 35),
            "house_T301": decide.fixed(house, 40),
            "house_shrunk_to_first_contact": decide.fixed(shrunk, 40),
            "kkt_exact_as_printed": report["solve"]["S_exact"],
            "kkt_rational": decide.fixed(kkt_cert, 40),
            "nevska_as_printed": NEVSKA,
            "jazivxt_as_printed": first[1],
            "pre_image_side_S0": decide.fixed(side0, 20),
        },
        "gain_over_house": row(house - side),
        "house_margin": row(margin),
        "gain_over_margin": f"{float((house - side) / margin):.6f}",
        "below_shrunk_house": row(shrunk - side),
        "kkt_gain_over_house": row(house - kkt_exact),
        "kkt_gain_over_margin": f"{float((house - kkt_exact) / margin):.6f}",
        "certificate_less_kkt_exact": row(side - kkt_exact),
        "certificate_less_kkt_rational": row(side - kkt_cert),
        "kkt_rational_less_kkt_exact": row(kkt_cert - kkt_exact),
        "certificate_less_nevska": row(side - Fraction(Decimal(NEVSKA))),
        "kkt_exact_less_nevska": row(kkt_exact - Fraction(Decimal(NEVSKA))),
        "certificate_less_jazivxt": row(side - jazivxt),
        "jazivxt_less_kkt_exact": row(jazivxt - kkt_exact),
        "certificate_less_S0": row(side - side0),
        "eps_times_S0_less_one": row(eps * (side0 - 1)),
        "S0_less_kkt_exact": row(side0 - kkt_exact),
        "S0_less_jazivxt": row(side0 - jazivxt),
        "relative_gain": decide.decimal((house - side) / house, 6),
    }
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(out, handle, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "sides"}, indent=0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
