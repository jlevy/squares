"""Compare this review's measurements with the repository's two tools (lane r127b-1118).

Written after the checker's freeze; decides nothing. Usage:

    python -I -B rb127_routes.py MEASURE.json SECOND_ROUTE_DIR OUT.json

It reads this review's ``out/measure.json`` and the receipts of
``devtools.contraction_margin`` and ``devtools.measure_identity`` that the lane ran as a
second route (``out/second-route/``), and compares, as exact fractions where both give
one: each certificate's first contact, binding pair, shrunk side and contraction margin;
each step's gain and whether the successor lies below the shrunk predecessor; and each
step's identity counts.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

LABELS = {"T-305": "T-305", "1015": "#1015", "1017": "#1017", "1020": "#1020"}
CONTRACTION = {"T-305": "contraction-T305-vs-1015.json", "1015": "contraction-1015-vs-1017.json",
               "1017": "contraction-1017-vs-1020.json", "1020": "contraction-1020-own.json"}
AGAINST = {("T-305", "1015"): "contraction-T305-vs-1015.json", ("1015", "1017"): "contraction-1015-vs-1017.json",
           ("1017", "1020"): "contraction-1017-vs-1020.json"}
IDENTITY = {("T-305", "1015"): ("identity-1015.json", "#1015", "T-305"),
            ("T-305", "1017"): ("identity-1017.json", "#1017", "T-305"),
            ("T-305", "1020"): ("identity-1020.json", "#1020", "T-305"),
            ("1015", "1017"): ("identity-1017.json", "#1017", "#1015"),
            ("1017", "1020"): ("identity-1020.json", "#1020", "#1017"),
            ("1015", "1020"): ("identity-1020.json", "#1020", "#1015")}


def F(s: str) -> Fraction:
    return Fraction(s)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    mine = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    d = Path(argv[2])
    out = {"program": "rb127_routes.py", "contraction": {}, "steps": {}, "identity": {}}
    agree_all = True
    for label, fname in CONTRACTION.items():
        tool = json.loads((d / fname).read_text(encoding="utf-8"))
        m = mine["certificates"][label]
        row = {
            "side_equal": F(m["side"]) == F(tool["side"]),
            "lambda_star_equal": F(m["lambda_star"]) == F(tool["lambda_star"]),
            "binding_pair_equal": [list(p) for p in m["binding_pairs"]] == [tool["binding_pair"]],
            "shrunk_side_equal": F(m["shrunk_side"]) == F(tool["contracted_side"]),
            "margin_equal": F(m["margin"]) == F(tool["margin"]),
            "tool_routes_accept_shrunk": tool.get("routes_accept"),
            "tool_cpu_seconds": tool.get("cpu_seconds"),
        }
        out["contraction"][label] = row
        agree_all &= all(v for k, v in row.items() if k.endswith("_equal"))
    for (p, q), fname in AGAINST.items():
        tool = json.loads((d / fname).read_text(encoding="utf-8"))["against"]
        step = next(s for s in mine["steps"] if s["step"] == f"{p} -> {q}")
        row = {
            "gain_equal": F(step["gain"]) == F(tool["gain"]),
            "tool_within_margin": tool["within_margin"],
            "mine_below_shrunk_predecessor": step["successor_below_shrunk_predecessor"],
            "verdicts_agree": tool["within_margin"] is (not step["successor_below_shrunk_predecessor"]),
            "tool_gain_over_margin": tool["gain_over_margin"],
            "mine_gain_over_margin": step["gain_over_margin"],
        }
        out["steps"][f"{p} -> {q}"] = row
        agree_all &= row["gain_equal"] and row["verdicts_agree"]
    for (p, q), (fname, view, against) in IDENTITY.items():
        tool = json.loads((d / fname).read_text(encoding="utf-8"))
        pair = next(x for x in tool["pairs"] if x["view"] == view and x["against"] == against)
        step = next(s for s in mine["steps"] if s["step"] == f"{p} -> {q}")
        ll = next(r for r in step["identity"]["by_symmetry"] if r["symmetry"] == "identity" and r["frame"] == "lower-left")
        bc = next(r for r in step["identity"]["by_symmetry"] if r["symmetry"] == "identity" and r["frame"] == "box-centred")
        any_one_to_one = any(r["nearest_centre_one_to_one"] for r in step["identity"]["by_symmetry"])
        row = {
            "tool_nearest_one_to_one": pair["nearest_centre"]["one_to_one"],
            "mine_any_symmetry_one_to_one": any_one_to_one,
            "one_to_one_agree": pair["nearest_centre"]["one_to_one"] == any_one_to_one,
            "assignment_counts_equal": pair["assignment"]["moved_beyond"] == ll["moved_beyond"],
            "centred_counts_equal": pair["centred"]["moved_beyond"] == bc["moved_beyond"],
            "largest_move_tool": pair["assignment"]["largest_move"],
            "largest_move_mine": ll["largest_move"],
            "side_difference_equal": F(pair["side_difference_exact"]) == -F(step["gain"]),
            "tool_bands": pair.get("bands"),
        }
        out["identity"][f"{p} -> {q}"] = row
        agree_all &= row["one_to_one_agree"] and row["assignment_counts_equal"] and row["centred_counts_equal"] and row["side_difference_equal"]
    out["all_agree"] = agree_all
    Path(argv[3]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("all agree:", agree_all)
    return 0 if agree_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
