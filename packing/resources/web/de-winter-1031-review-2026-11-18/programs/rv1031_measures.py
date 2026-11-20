"""The gains of jlevy/squares#1031 against the record at 299, exactly (decides nothing).

Written for this review after the checker's freeze; imports nothing from this repository
or the source.

    python -I -B rv1031_measures.py --subject json:n299_exact.json \
        --contraction out/contraction-t325.json --house "T-325=witness:..." ... --out measures.json

For each house it gives the exact side and the subject's gain below it.  From the
contraction receipt of the house of record (T-325) it gives that house shrunk until its
squares first touch, the subject's gain below the shrunk side, and the gain as a multiple
of the house's contraction margin: the comparison the owner's option D (think-b0w5) asks
for.  It also compares the issue's printed values (the claim, the house it cites, the
gain, the Kaggle value) with the exact sides.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this packet's own modules, under python -I

import rv1031_decide as D
import rv1031_reader as R


def dec(text: str) -> F:
    a, b = text.split(".")
    return F(int(a + b), 10 ** len(b))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--contraction", required=True)
    ap.add_argument("--house", action="append", default=[])
    ap.add_argument("--issue-claim", default="17.793636991744")
    ap.add_argument("--issue-house", default="17.801004434255294")
    ap.add_argument("--issue-kaggle", default="17.793636991746555")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    kind, path = args.subject.split(":", 1)
    s = R.read_any(path, kind)["side"]
    with open(args.contraction) as fh:
        con = json.load(fh)
    cm = F(con["contraction_margin"])
    s325 = F(con["side"])
    shrunk = s325 - cm
    rec: dict = {
        "program": "rv1031_measures.py",
        "subject_side": D.fstr(s),
        "subject_side_short": D.short(s, 30),
        "house_of_record": {
            "label": con.get("label"),
            "side": D.fstr(s325),
            "contraction_margin": D.fstr(cm),
            "contraction_margin_short": D.short(cm),
            "one_less_g_star_short": con["one_less_g_star_short"],
            "shrunk_side": D.fstr(shrunk),
            "shrunk_side_short": D.short(shrunk, 40),
            "gain": D.fstr(s325 - s),
            "gain_short": D.short(s325 - s, 15),
            "gain_below_shrunk_side": D.fstr(shrunk - s),
            "gain_below_shrunk_side_short": D.short(shrunk - s, 15),
            "gain_over_contraction_margin_short": D.short((s325 - s) / cm, 6),
            "below_shrunk_side": shrunk > s,
        },
        "houses": {},
    }
    for spec in args.house:
        label, rest = spec.split("=", 1)
        k, p = rest.split(":", 1)
        hs = R.read_any(p, k, require_claim=False)["side"]
        rec["houses"][label] = {"path": p, "side": D.fstr(hs), "side_short": D.short(hs, 20), "gain": D.fstr(hs - s), "gain_short": D.short(hs - s, 12)}
    claim, house, kag = dec(args.issue_claim), dec(args.issue_house), dec(args.issue_kaggle)
    rec["issue"] = {
        "claim": args.issue_claim,
        "claim_less_side_short": D.short(claim - s),
        "cited_house": args.issue_house,
        "cited_house_less_side_short": D.short(house - s, 12),
        "kaggle_value": args.issue_kaggle,
        "kaggle_less_side_short": D.short(kag - s, 6),
    }
    with open(args.out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(rec["house_of_record"], indent=0)[:1500])
    for k, v in rec["houses"].items():
        print(k, v["side_short"], v["gain_short"])
    print(rec["issue"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
