"""Compare this review's contraction receipt with the maintained tool's receipts, exactly,
and set the maintained identity receipts beside this review's; it decides nothing.

Lane r127-1118.  Written after the checker was frozen and before the findings were
frozen.  It reads JSON receipts only.

    python -I -B r127_compare.py --ours out/contract.json --identity out/identity.json
        --maintained out/maintained --out out/compare-maintained.json
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from fractions import Fraction

NAMES = {"t305": "T-305", "1015": "#1015", "1017": "#1017", "1020": "#1020"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ours", required=True)
    ap.add_argument("--identity", required=True)
    ap.add_argument("--maintained", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    ours = json.load(open(a.ours))
    steps = {(s["predecessor"], s["successor"]): s for s in ours["steps"]}
    rows = []
    for path in sorted(glob.glob(os.path.join(a.maintained, "contraction-*.json"))):
        m = json.load(open(path))
        pk, sk = os.path.basename(path)[len("contraction-"):-5].split("-")
        pred, succ = NAMES[pk], NAMES[sk]
        mine = ours["packings"][pred]
        st = steps[(pred, succ)]
        bp = sorted(m["binding_pair"]) if isinstance(m["binding_pair"], list) else m["binding_pair"]
        row = {
            "step": f"{pred} -> {succ}", "receipt": os.path.basename(path),
            "side_equal": Fraction(m["side"]) == Fraction(mine["side"]),
            "lambda_star_equal": Fraction(m["lambda_star"]) == Fraction(mine["lambda_star"]),
            "contracted_side_equal": Fraction(m["contracted_side"]) == Fraction(mine["L_prime"]),
            "margin_equal": Fraction(m["margin"]) == Fraction(mine["margin"]),
            "gain_equal": Fraction(m["against"]["gain"]) == Fraction(st["gain"]),
            "binding_pair_maintained": bp,
            "binding_pairs_ours": mine["binding_pairs"],
            "within_margin_maintained": m["against"].get("within_margin"),
            "beats_ours": st["successor_below_contracted_predecessor"],
            "routes_accept_maintained": m.get("routes_accept"),
            "gain_over_margin_maintained": m["against"].get("gain_over_margin"),
            "cpu_seconds_maintained": m.get("cpu_seconds"),
        }
        row["agree"] = (row["side_equal"] and row["lambda_star_equal"] and row["contracted_side_equal"]
                        and row["margin_equal"] and row["gain_equal"]
                        and row["within_margin_maintained"] == (not row["beats_ours"]))
        rows.append(row)
        print(json.dumps(row))
    ident = []
    for path in sorted(glob.glob(os.path.join(a.maintained, "identity-*.json"))):
        m = json.load(open(path))
        ident.append({"receipt": os.path.basename(path), "keys": sorted(m)[:20]})
    out = {"program": "r127_compare.py", "decides": "nothing", "contraction": rows,
           "all_contraction_rows_agree": all(r["agree"] for r in rows),
           "identity_receipts": ident}
    json.dump(out, open(a.out, "w"), indent=1)
    print("all contraction rows agree:", out["all_contraction_rows_agree"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
