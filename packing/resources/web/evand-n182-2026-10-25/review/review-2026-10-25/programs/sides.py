"""Exact comparison of the #806 certificate's side with the sides around it at 182.

Written for the stage 4 mathematical review of jlevy/squares issue 806. It decides
nothing; it prints, in exact rational arithmetic, the certificate's side, its upward
prints at 12 and 14 places, and its gap to each comparison side: the case record's
verified ceiling (T-174's exact side, read from frontier/n-182.md), T-098's exact side
(read from its retained certificate), T-056's printed side, the source's KKT side S*,
and the side-only leaderboard values the issue quotes.

Run with the project interpreter in isolated mode:

    python3 -I sides.py CERT CASE_RECORD T098_CERT EXACT_TXT --json OUT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction

import yaml


def digest(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def first_side(path: str) -> Fraction:
    for line in open(path, encoding="ascii"):
        if line.strip() and not line.startswith("#"):
            return Fraction(line.split()[1])
    raise ValueError(path)


def up(q: Fraction, places: int) -> str:
    scale = 10**places
    u = -((-q.numerator * scale) // q.denominator)
    return f"{u // scale}.{u % scale:0{places}d}"


def sci(q: Fraction) -> str:
    return f"{float(q):.6e}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cert")
    ap.add_argument("case_record")
    ap.add_argument("t098_cert")
    ap.add_argument("exact")
    ap.add_argument("--json", required=True)
    a = ap.parse_args()
    s = first_side(a.cert)
    text = open(a.case_record, encoding="utf-8").read()
    front = yaml.safe_load(re.split(r"^---\s*$", text, flags=re.M)[1])["packing"]
    house = Fraction(front["verified_upper_bound"]["exact_form"])
    reported = Fraction(front["reported_upper_bound"]["exact_form"])
    t098 = first_side(a.t098_cert)
    s_star = Fraction(open(a.exact, encoding="ascii").readline().split()[1])
    others = {
        "house_verified_T-174": house,
        "house_reported_T-174": reported,
        "T-098": t098,
        "T-056_printed": Fraction("13.974090713124822"),
        "kaggle_Prathamesh_Chavan_side_only": Fraction("13.9727613470647"),
        "kaggle_Subramanya_N_side_only": Fraction("13.9709164362306"),
        "source_KKT_side_S_star": s_star,
    }
    out = {
        "program": "sides.py",
        "program_sha256": digest(__file__),
        "inputs": {k: [p, digest(p)] for k, p in (("cert", a.cert), ("case_record", a.case_record), ("t098_cert", a.t098_cert), ("exact", a.exact))},
        "side": str(s),
        "print_12_up": up(s, 12),
        "print_14_up": up(s, 14),
        "print_12_up_is_least_12_place_decimal_at_or_above": Fraction(up(s, 12)) >= s > Fraction(up(s, 12)) - Fraction(1, 10**12),
        "commit_title_side_13.97091643621468_at_or_above": Fraction("13.97091643621468") >= s,
        "gaps_other_minus_side": {k: {"exact": str(v - s), "approx": sci(v - s), "other_print_12_up": up(v, 12)} for k, v in others.items()},
    }
    print(f"side {s} = {up(s, 30)} (exact, 30 places)")
    print(f"upward prints: 12 places {out['print_12_up']}, 14 places {out['print_14_up']}; the 12-place print is the least 12-place decimal >= side: {out['print_12_up_is_least_12_place_decimal_at_or_above']}")
    print(f"the commit title's 13.97091643621468 is >= side: {out['commit_title_side_13.97091643621468_at_or_above']}")
    for k, v in others.items():
        print(f"  {k:<36} {up(v, 12)} (12 up)  minus side = {sci(v - s)}")
    print(f"house verified == house reported: {house == reported}")
    with open(a.json, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
