"""Written after the checker freeze (lane r1021-1118): compare this review's route with the second.

Usage: python -I -B r1021_routes.py OUT_DIR

Reads out/post-measure.json (this lane's frozen modules, through r1021_post.py) and the
receipts of the repository's devtools.contraction_margin and devtools.measure_identity
in out/second-route/, run unread after the freeze, and compares them exactly: for every
certificate lambda*, the binding pair, the contracted side and the margin as fractions;
for every step the gain as a fraction and whether it lies outside the margin; for every
identity measurement whether nearest centres pair the squares one to one, and, for the
best assignment in each frame, the counts beyond each bound and the largest move at the
second route's printed places.  Decides nothing.  Writes out/routes.json.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction


def load(path: str):
    with open(path) as f:
        return json.load(f)


def main(argv: list[str]) -> int:
    out = argv[0]
    post = load(os.path.join(out, "post-measure.json"))
    sr = os.path.join(out, "second-route")
    rec: dict = {"contraction": {}, "steps": {}, "identity": {}}
    mine = {}
    for n, e in post["counts"].items():
        succ = "1021" if n == "268" else "1022"
        for key, c in e["contraction"].items():
            label = succ if key == "successor" else key
            mine[label] = c
        sides = {("1021" if k == "#1021" else "1022" if k == "#1022" else k): Fraction(v["exact"]) for k, v in e["sides"].items()}
        for pred in ([("T-289", "T289"), ("T-320", "T320")] if n == "268" else [("T-283", "T283"), ("T-321", "T321")]):
            r = load(os.path.join(sr, f"contraction-{pred[1]}-vs-{succ}.json"))
            gain_mine = sides[pred[0]] - sides[succ]
            rec["steps"][f"{pred[0]} -> #{succ}"] = {
                "gain_equal": Fraction(r["against"]["gain"]) == gain_mine,
                "outside_margin_both": (not r["against"]["within_margin"]) and gain_mine > Fraction(mine[pred[0]]["margin_exact"]),
                "gain_over_margin_second_route": r["against"]["gain_over_margin"],
            }
            rec["contraction"][pred[0]] = compare_contraction(r, mine[pred[0]])
        r = load(os.path.join(sr, f"contraction-{succ}-own.json"))
        rec["contraction"][succ] = compare_contraction(r, mine[succ])
        ident = load(os.path.join(sr, f"identity-{succ}.json"))
        for pair in ident["pairs"]:
            pred = pair["against"]
            step = next(s for s in e["steps"] if s["step"] == f"{pred} -> #{succ}")
            rows = step["identity"]["rows"]
            ll = min((x for x in rows if x["frame"] == "lower-left"), key=lambda x: x["summed_squared_move"])
            bc = min((x for x in rows if x["frame"] == "box-centred"), key=lambda x: x["summed_squared_move"])
            one_mine = bool(step["identity"]["one_to_one_under"])
            rec["identity"][f"{pred} -> #{succ}"] = {
                "one_to_one_equal": pair["nearest_centre"]["one_to_one"] == one_mine,
                "one_to_one": one_mine,
                "lower_left_counts_equal": [pair["assignment"]["moved_beyond"][k] for k in ("1e-9", "1e-6", "1e-3", "1e-2", "1e-1")]
                == [ll["beyond"][k] for k in ("1e-9", "1e-6", "1e-3", "1e-2", "1e-1")],
                "lower_left_largest_equal": same_print(pair["assignment"]["largest_move"], ll["largest_move"]),
                "box_centred_counts_equal": [pair["centred"]["moved_beyond"][k] for k in ("1e-9", "1e-6", "1e-3", "1e-2", "1e-1")]
                == [bc["beyond"][k] for k in ("1e-9", "1e-6", "1e-3", "1e-2", "1e-1")],
                "box_centred_largest_equal": same_print(pair["centred"]["largest_move"], bc["largest_move"]),
                "mine_lower_left": [ll["symmetry"], ll["beyond"], round(ll["largest_move"], 6)],
                "second_route_lower_left": [pair["assignment"]["symmetry"], pair["assignment"]["moved_beyond"],
                                            pair["assignment"]["largest_move"]],
            }
    flat = [v for group in ("contraction", "steps", "identity") for item in rec[group].values()
            for k, v in item.items() if k.endswith("_equal") or k == "outside_margin_both"]
    rec["all_equal"] = all(flat)
    with open(os.path.join(out, "routes.json"), "w") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    print("all equal:", rec["all_equal"], "comparisons:", len(flat))
    return 0 if rec["all_equal"] else 1


def same_print(text, value: float) -> bool:
    """The second route prints moves to six significant figures: compare at its printed places."""
    text = str(text)
    places = len(text.split(".")[1]) if "." in text else 0
    return round(value, places) == float(text)


def compare_contraction(r: dict, c: dict) -> dict:
    return {
        "lambda_equal": Fraction(r["lambda_star"]) == Fraction(c["lambda_exact"]),
        "binding_equal": list(r["binding_pair"]) == c["binding_pairs"][0] and len(c["binding_pairs"]) == 1,
        "contracted_side_equal": Fraction(r["contracted_side"]) == Fraction(c["shrunk_side_exact"]),
        "margin_equal": Fraction(r["margin"]) == Fraction(c["margin_exact"]),
    }


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
