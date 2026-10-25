"""Compare this review's least slacks with the packets' sharp-control receipts, exactly.

A program of the stage 4 mathematical review of T-241 and T-242 (bead think-vm3m). It
decides nothing: it reads outputs/t241_t242_exact.json, written by t241_t242_exact.py beside
it, and the three receipts/sharp-controls*.json the packets keep, and prints whether the
least pair gap and the least wall clearance agree as exact fractions.

In each receipt, the controls that move a wall report the certificate's own least pair
gap ('gap'), and the control that closes the tightest pair reports its own least wall
clearance ('wall'), each unchanged by that control.

Run from packing/:
    python -I resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/programs/t241_t242_receipts.py
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKING = HERE.parents[5]
RECEIPTS = {
    "T-241 n=304": "resources/web/couzo-n304-2026-10-23/receipts/sharp-controls.json",
    "T-242 n=268": "resources/web/evand-kaggle-descents-2026-10-24/receipts/sharp-controls-n268.json",
    "T-242 n=304": "resources/web/evand-kaggle-descents-2026-10-24/receipts/sharp-controls-n304.json",
}


def main() -> int:
    mine = json.loads((HERE.parent / "outputs" / "t241_t242_exact.json").read_text(encoding="utf-8"))
    by_key = {entry["key"]: entry for entry in mine["certificates"]}
    every = True
    for key, rel in RECEIPTS.items():
        receipt = json.loads((PACKING / rel).read_text(encoding="utf-8"))
        decision = by_key[key]["decision"]
        my_gap = Fraction(decision["least_pair_gaps"][0]["sat_gap"])
        my_wall = min(Fraction(decision["least_near_wall_slack"]), Fraction(decision["least_far_wall_slack"]))
        my_far = Fraction(decision["least_far_wall_slack"])
        same_side = Fraction(receipt["side"]) == Fraction(by_key[key]["side"]["header_side"])
        gaps = set()
        walls = set()
        for control in receipt["controls"]:
            for route in control["routes"].values():
                if control["margin"] == "wall":
                    gaps.add(Fraction(route["gap"]))
                if control["control"].startswith("tightest-pair"):
                    walls.add(Fraction(route["wall"]))
        gap_ok = gaps == {my_gap}
        wall_ok = walls == {my_wall}
        every = every and gap_ok and wall_ok and same_side and receipt.get("all_as_expected") is True
        print(f"{key}: receipt {rel}")
        print(f"  side as in the receipt: {same_side}; receipt all_as_expected: {receipt.get('all_as_expected')}")
        print(f"  least pair gap: mine {float(my_gap):.15e}; receipt {[f'{float(g):.15e}' for g in gaps]}; exactly equal: {gap_ok}")
        print(f"  least wall clearance: mine {my_wall} ({float(my_wall):.6e}); receipt {[str(w) for w in walls]}; exactly equal: {wall_ok}")
        print(f"  least far-wall clearance (the side the receipt lowers to contact): {my_far} = {float(my_far):.15e}")
    print(f"all agree: {every}")
    return 0 if every else 1


if __name__ == "__main__":
    raise SystemExit(main())
