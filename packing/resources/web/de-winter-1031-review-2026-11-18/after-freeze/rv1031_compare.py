"""Compare this review's contraction receipt for T-325 with the record's own (decides nothing).

Written after the findings' freeze for the review of jlevy/squares#1031; imports nothing
from this repository. It reads two JSON receipts as data: this lane's
``out/contraction-t325.json`` and the import of #1009's
``measure/contraction-n299-own.json`` (written by the record's ``devtools.contraction_margin``,
which this lane did not run or read), and compares the exact side, the contraction factor,
the contracted side and the margin.

    python -I -B rv1031_compare.py --ours out/contraction-t325.json --record PATH --out compare.json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ours", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with open(a.ours) as fh:
        ours = json.load(fh)
    with open(a.record) as fh:
        rec = json.load(fh)
    g_ours = F(ours["g_star"])
    lam = F(rec["lambda_star"])
    shrunk_ours = F(ours["side"]) - F(ours["contraction_margin"])
    out = {
        "program": "rv1031_compare.py",
        "record_receipt": a.record,
        "same_side": F(ours["side"]) == F(rec["side"]),
        "same_factor": g_ours == lam,
        "same_contracted_side": shrunk_ours == F(rec["contracted_side"]),
        "same_margin": F(ours["contraction_margin"]) == F(rec["margin"]),
        "record_binding_pair": rec.get("binding_pair"),
        "ours_first_contact_pairs": ours["first_contact_pairs"],
        "record_margin_float": rec.get("margin_float"),
        "ours_margin_short": ours["contraction_margin_short"],
    }
    out["agree"] = out["same_side"] and out["same_factor"] and out["same_contracted_side"] and out["same_margin"]
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
