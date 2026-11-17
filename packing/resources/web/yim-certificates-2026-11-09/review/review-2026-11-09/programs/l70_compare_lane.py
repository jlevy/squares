"""Hold the import lane's receipts to this review's, exactly (L70; after the findings froze).

Reads lane L65's retained receipts (copied from claude/bold-ritchie-xo28us-l65 at
66555e138a54 into LANE/ by plain `git show`) and this review's receipts:

* each positive case's least pair gap and least containment clearance, on both
  maintained routes, against this review's least pair margin and least wall clearance;
* the contraction measures (lambda*, contracted side, margin, gain, gain over margin) at
  130, 299 and 303 and the two precedents, against this review's contract.json.

Usage: python -I l70_compare_lane.py --lane LANE --out OUTDIR/compare-lane.json [--checks OUTDIR]
"""

from __future__ import annotations

import argparse
import json
import lzma
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402

LABELS = {
    "130": "yim-n130", "299": "yim-n299", "303": "yim-n303", "303-first": "yim-n303-first",
    **{str(n): f"yim-n{n}" for n in (553, 599, 600, 601, 602, 604, 645, 647, 648, 699, 700)},
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--checks", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    lane = Path(ns.lane)
    chk = Path(ns.checks)
    rows: dict[str, Any] = {}
    problems: list[str] = []
    for key, label in LABELS.items():
        path = lane / f"exact-certification-n{key}.json.xz"
        if not path.exists():
            rows[key] = "lane receipt not copied"
            continue
        d = json.loads(lzma.open(path).read())
        pos = [c for c in d["cases"] if c.get("control") == "positive"]
        mine = json.loads((chk / f"check-{label}.json").read_text())
        my_gap = F(mine["A"]["least_margin"])
        my_wall = min(F(mine["A"]["walls"][w]["least"]) for w in C.WALLS)
        entry: dict[str, Any] = {"cases": len(d["cases"]), "positives": len(pos)}
        for case in pos:
            for route in ("exact_verify", "independent"):
                r = case[route]
                g = F(r["minimum_best_pair_gap"])
                w = F(r["minimum_containment_clearance"])
                same = g == my_gap and w == my_wall and r["verification_passed"] and r["pairs_tested"] == mine["pairs"]
                entry[route] = {"gap_equal": g == my_gap, "clearance_equal": w == my_wall, "passed": r["verification_passed"], "pairs": r["pairs_tested"]}
                if not same:
                    problems.append(f"{key} {route}: gap {float(g):.6e} vs {float(my_gap):.6e}, clearance {float(w):.6e} vs {float(my_wall):.6e}")
        controls = [c.get("control") for c in d["cases"] if c.get("control") != "positive"]
        entry["controls"] = controls
        entry["controls_refused_by_both"] = all(
            not c[r]["verification_passed"] for c in d["cases"] if c.get("control") != "positive" for r in ("exact_verify", "independent")
        )
        rows[key] = entry
    mine_c = json.loads((chk / "contract.json").read_text())["measurements"]
    contr: dict[str, Any] = {}
    pairs = {
        "contraction-n299.json": ("house-t277-n299", "yim-n299"),
        "contraction-n303.json": ("house-t278-n303", "yim-n303"),
        "contraction-n130.json": ("house-t259-n130", "yim-n130"),
        "precedent-contraction-n130-t259.json": ("precedent-t254-n130", "house-t259-n130"),
        "precedent-contraction-n260-t265.json": ("precedent-t257-n260", "precedent-t265-n260"),
    }
    for fname, (old, new) in pairs.items():
        p = lane / fname
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        m = mine_c[old]
        res = {
            "side_equal": F(d["side"]) == F(m["side"]),
            "lambda_star_equal": F(d["lambda_star"]) == F(m["lambda_star"]),
            "contracted_side_equal": F(d["contracted_side"]) == F(m["contracted_side"]),
            "margin_equal": F(d["margin"]) == F(m["margin"]),
            "binding_pair_lane": d.get("binding_pair"),
            "binding_pair_here": m["binding_pairs"][0][:2],
            "routes_accept_lane": d.get("routes_accept"),
        }
        ag = d.get("against")
        if ag:
            gain_here = F(m["side"]) - F(mine_c[new]["side"])
            res["gain_equal"] = F(ag["gain"]) == gain_here
            res["share_lane"] = ag["gain_over_margin"]
            res["share_here"] = f"{float(gain_here / F(m['margin'])):.4f}"
        contr[fname] = res
        if not all(v for k, v in res.items() if k.endswith("_equal")):
            problems.append(f"{fname}: {res}")
    out = {
        "program": "l70_compare_lane.py",
        "program_digests": C.file_digests(C.CHECKER_FILES + ("l70_compare_lane.py",)),
        "lane_head": "66555e138a54f9d98eabc00b7cd32aab75e9b06e",
        "replay": rows,
        "contraction": contr,
        "problems": problems,
        "verdict": "LANE_AGREES_EXACTLY" if not problems else "DIFFERENCES",
    }
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    print(out["verdict"])
    for p in problems:
        print("  ", p)
    for k, v in contr.items():
        print(k, {kk: vv for kk, vv in v.items()})
    for k, v in rows.items():
        if isinstance(v, dict):
            print(k, "positives", v["positives"], "controls", v["controls"], "refused by both", v["controls_refused_by_both"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
