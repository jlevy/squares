"""Hold lane L81's receipts to this review's, after the findings were frozen (review L83).

Usage: python -I -B l83_compare_lane.py REVIEW_OUT LANE_DIR SRC_DIR KNOWN_BEST OUT.json

LANE_DIR holds, per count, the lane's packet files extracted from its branch at
740fa72c5: sNNN/measure/identity.json, sNNN/measure/contraction-nNNN.json, and
xz/<packet>.json.xz (receipts/exact-certification.json.xz).
"""

from __future__ import annotations

import json
import lzma
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l83_check as C  # noqa: E402
import l83_identity as I  # noqa: E402

PACKET = {156: "ozden-s156-upper-bound-2026-11-10", 180: "ozden-s180-upper-bound-2026-11-10", 268: "ozden-s268-upper-bound-2026-11-10", 269: "ozden-s269-upper-bound-2026-11-11"}


def signs(angs):
    t = angs[np.abs(angs) > 1]
    return {"tilted_beyond_1deg": int(len(t)), "positive": int((t > 0).sum()), "negative": int((t < 0).sum()), "within_1deg_of_45": int((np.abs(t) > 44).sum()), "range": [round(float(np.abs(t).min()), 3), round(float(np.abs(t).max()), 3)] if len(t) else None}


def main(argv):
    mine, lane, src, kb, out = (Path(a) for a in argv[1:6])
    res = {}
    agree = True
    for n, packet in PACKET.items():
        chk = json.loads((mine / f"check-n{n}.json").read_text())
        hs = json.loads((mine / f"houses-n{n}.json").read_text())
        idn = json.loads((mine / f"identity-n{n}.json").read_text())["against_house"]
        cert = json.loads(lzma.open(lane / "xz" / f"{packet}.json.xz").read())
        pos = cert["cases"][0]
        my_gap = F(chk["least_pair_margin"]["exact"])
        routes = {}
        for r in ("exact_verify", "independent"):
            v = pos[r]
            routes[r] = {
                "passed": v["verification_passed"],
                "least_gap_equals_review": F(v["minimum_best_pair_gap"]) == my_gap,
                "containment_clearance_zero": F(v["minimum_containment_clearance"]) == 0,
                "side_equals_review": F(v["side"]) == F(chk["side"]),
                "pairs_tested": v["pairs_tested"],
            }
        con = json.loads((lane / f"s{n}" / "measure" / f"contraction-n{n}.json").read_text())
        lane_margin = F(con["margin"]) if con.get("margin") not in (None, "0") else F(0)
        contraction = {
            "lane_margin_float": con.get("margin_float"),
            "review_margin_float": hs["margin_float"],
            "margin_equal_exactly": lane_margin == F(hs["margin"]),
            "lane_one_minus_lambda_star": con.get("one_minus_lambda_star"),
            "lane_binding_pair": con.get("binding_pair"),
            "review_binding_pair": hs["binding_pair"],
        }
        li = json.loads((lane / f"s{n}" / "measure" / "identity.json").read_text())
        house_pair = next(p for p in li["pairs"] if p["against"] not in ("regularized", "house-witness"))
        block = house_pair["centred"] if idn["anchor"] == "centre" else house_pair["assignment"]
        identity = {
            "review_anchor": idn["anchor"],
            "lane_block": "centred" if idn["anchor"] == "centre" else "assignment",
            "lane_moved_beyond_0.1": block["moved_beyond"].get("1e-1"),
            "review_moved_beyond_0.1": idn["assignment"]["moved_beyond"]["0.1"],
            "lane_moved_beyond_1e-3": block["moved_beyond"].get("1e-3"),
            "review_moved_beyond_1e-3": idn["assignment"]["moved_beyond"]["1e-3"],
            "lane_largest_move": block["largest_move"],
            "review_largest_move": round(idn["assignment"]["largest_move"], 6),
            "lane_assignment_largest_move_lower_left": house_pair["assignment"]["largest_move"],
            "lane_turned_beyond_1e-6": house_pair["assignment"].get("turned_beyond_1e-6"),
            "review_turned_beyond_1e-6rad": idn["assignment"]["turned_beyond_1e-6rad"],
            "lane_nearest_one_to_one": house_pair["nearest_centre"]["one_to_one"],
            "review_nearest_one_to_one_best_symmetry": idn["nearest_one_to_one"],
        }
        identity["moves_agree"] = identity["lane_moved_beyond_0.1"] == identity["review_moved_beyond_0.1"] and abs(float(identity["lane_largest_move"]) - identity["review_largest_move"]) < 5e-6
        # tilt signs, recomputed from this review's own reading
        _, _, ca = I.cert_pose(src / f"s{n}" / f"n-{n}-candidate.yaml")
        _, _, ha = I.ref_pose(kb / f"n-{n}.yaml")
        lane_t = li["tilts"]
        house_key = next(k for k in lane_t if k not in ("OZDEN", "regularized", "house-witness"))
        tilts = {
            "review_new": signs(ca),
            "review_house": signs(ha),
            "lane_new": {k: lane_t["OZDEN"][k] for k in ("tilted_beyond_1_degree", "tilted_positive", "tilted_negative", "tilt_range_degrees")},
            "lane_house": {k: lane_t[house_key][k] for k in ("tilted_beyond_1_degree", "tilted_positive", "tilted_negative", "tilt_range_degrees")},
        }
        rn, rh = tilts["review_new"], tilts["review_house"]
        ln, lh = tilts["lane_new"], tilts["lane_house"]
        tilts["counts_agree"] = (rn["tilted_beyond_1deg"], rn["positive"], rn["negative"]) == (ln["tilted_beyond_1_degree"], ln["tilted_positive"], ln["tilted_negative"]) and (rh["tilted_beyond_1deg"], rh["positive"], rh["negative"]) == (lh["tilted_beyond_1_degree"], lh["tilted_positive"], lh["tilted_negative"])
        tilts["none_near_45"] = rn["within_1deg_of_45"] == 0 and rh["within_1deg_of_45"] == 0
        ok = all(r["passed"] and r["least_gap_equals_review"] and r["containment_clearance_zero"] and r["side_equals_review"] for r in routes.values()) and contraction["margin_equal_exactly"] and identity["moves_agree"] and tilts["counts_agree"]
        agree = agree and ok
        res[str(n)] = {"routes": routes, "contraction": contraction, "identity": identity, "tilts": tilts, "agree": ok}
        print(n, "agree", ok, "| routes", {k: (v["least_gap_equals_review"], v["side_equals_review"]) for k, v in routes.items()}, "| margin", contraction["margin_equal_exactly"], "| moves", identity["lane_moved_beyond_0.1"], identity["review_moved_beyond_0.1"], identity["lane_largest_move"], identity["review_largest_move"], "| turned1e-6", identity["lane_turned_beyond_1e-6"], identity["review_turned_beyond_1e-6rad"])
        print("    tilts review", rn, rh, "| lane", ln, lh, "| near45 none", tilts["none_near_45"])
    doc = {"verdict": "LANE_EQUALS_REVIEW" if agree else "LANE_DIFFERS", "counts": res, "lane_head": "740fa72c572ce027d7b0e393d257d1e467a5d588", "programs": C.program_digests()}
    out.write_text(json.dumps(doc, indent=1) + "\n")
    print(doc["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
