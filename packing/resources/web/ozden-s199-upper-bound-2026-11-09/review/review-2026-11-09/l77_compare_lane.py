"""After the freeze: hold lane L76's receipts to this review's, and measure the tilt-sign
split its README states. Reads L76's working tree as data.

Run: python -I -B l77_compare_lane.py L76_PACKET L76_RESULTS_YAML CANDIDATE.yaml MAIN_N199.yaml OUT.json
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from fractions import Fraction as F

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l77_checker as C  # noqa: E402


def sha(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def angle_mod90(ux: float, uy: float) -> float:
    """Edge direction in (-45, 45] degrees."""
    a = math.degrees(math.atan2(uy, ux)) % 90.0
    return a - 90.0 if a > 45.0 else a


def tilt_census(angles: list[float]) -> dict:
    tilted = [a for a in angles if abs(a) > 1.0]
    return {"tilted_beyond_1deg": len(tilted),
            "positive": sum(1 for a in tilted if a > 0), "negative": sum(1 for a in tilted if a < 0),
            "within_1deg_of_45": sum(1 for a in tilted if abs(abs(a) - 45.0) < 1.0),
            "positive_away_from_45": sum(1 for a in tilted if a > 0 and abs(a - 45.0) >= 1.0),
            "negative_away_from_45": sum(1 for a in tilted if a < 0 and abs(a + 45.0) >= 1.0)}


def main() -> int:
    packet, l76_results, cand, house, out = sys.argv[1:6]
    mine = os.path.join(HERE, "out")
    res: dict = {"program": "l77_compare_lane.py",
                 "program_sha256": sha(__file__), "checker_sha256": sha(os.path.join(HERE, "l77_checker.py"))}
    agree: dict = {}
    # 1. the retained certificate is the one decided here
    w = C.read_witness(cand)
    agree["packet_certificate_is_the_decided_file"] = sha(os.path.join(packet, "source/n-199-candidate.yaml")) == w["sha256"]
    # 2. draft entry's side
    # the lane's working tree was in flux while it was read: the draft entry may be absent
    rs = yaml.safe_load(open(l76_results))["results"]
    drafts = [e for e in rs if 199 in ((e.get("scope") or {}).get("n_values") or []) and "938" in str(e.get("claim", ""))]
    res["draft_entry_present_at_read"] = [e["id"] for e in drafts]
    if drafts:
        side_text = drafts[0]["claim"].split("s(199) <=")[1].split(".")[0].strip()
        agree["draft_side_equals_certificate"] = F(*C.parse_scalar(side_text)) == F(*w["side"])
        agree["draft_score"] = drafts[0]["significance"]["score"]
    # 3. the L-step scan against this review's propagation, corrected for the 1e-25 tolerance
    prop = json.load(open(os.path.join(mine, "propagate.json")))
    rows = prop["verified"]["rows"]
    mine_set = {(r["n"], r["m"]) for r in rows if r.get("vs_record") == "improves"}
    mine_set |= {(r["n"], r["m"]) for r in rows if r.get("vs_record") == "equal-to-60-digits" and r["record_minus"] > 1e-40}
    scan = json.load(open(os.path.join(packet, "measure/l-step-scan.json")))
    lane_set = {(x["from"], x["n"]) for x in scan["l_step"]["improves"]}
    agree["l_step_improvements_equal"] = lane_set == mine_set
    res["l_step"] = {"lane": sorted(lane_set), "review_corrected": sorted(mine_set),
                     "review_at_freeze": sorted((r["n"], r["m"]) for r in rows if r.get("vs_record") == "improves"),
                     "lane_extensions": len(scan["l_step"]["extensions"]),
                     "review_equal_or_within_1e-40": sum(1 for r in rows if r.get("vs_record") == "equal"
                                                         or (r.get("vs_record") == "equal-to-60-digits" and r["record_minus"] <= 1e-40))}
    # 4. identity against T-127
    ident = json.load(open(os.path.join(packet, "measure/identity.json")))
    p = [x for x in ident["pairs"] if x["view"] == "OZDEN" and x["against"] == "T-127"][0]
    myid = json.load(open(os.path.join(mine, "identity-n199.json")))["new_vs_house"]
    agree["identity_not_one_to_one_both"] = (p["nearest_centre"]["one_to_one"] is False) and myid["nearest_distinct"] < 199
    agree["identity_moved_beyond_0.1_equal"] = p["assignment"]["moved_beyond"]["1e-1"] == myid["moved_beyond"]["0.1"]
    agree["identity_largest_move_equal_to_print"] = abs(float(p["assignment"]["largest_move"]) - myid["largest_move"]) < 1e-5
    # 5. contraction: own margin 0 at a touching pair; house margin, gain equal to the gap
    own = json.load(open(os.path.join(packet, "measure/contraction-n199-own.json")))
    chk = json.load(open(os.path.join(mine, "check-n199.json")))
    agree["own_margin_zero_at_a_touching_pair"] = own["margin"] == "0" and own["binding_pair"] in chk["touching_pairs"]["A"]
    hc = json.load(open(os.path.join(packet, "measure/contraction-n199.json")))
    sides = json.load(open(os.path.join(mine, "sides.json")))
    agree["gain_equals_gap_exactly"] = F(hc["against"]["gain"]) == F(sides["gap_record_minus_side"]["exact"])
    res["house_margin"] = {"margin_float": hc["margin_float"], "gain_over_margin": hc["against"]["gain_over_margin"]}
    # 6. the tilt-sign split
    new_angles = [angle_mod90(float(s.axes[0][0]), float(s.axes[0][1])) for s in (C.SquareA(cs) for cs in w["corners"])]
    hw = yaml.safe_load(open(house))["witness"]["squares"]
    h_angles = []
    for e in hw:
        b = [F(*C.parse_scalar(str(v))) for v in e["basis"]]
        h_angles.append(angle_mod90(float(b[0]), float(b[1])))
    res["tilts"] = {"certificate": tilt_census(new_angles), "house_T127": tilt_census(h_angles),
                    "lane_readme": "49 tilted beyond 1 degree, 36 one way and 13 the other; T-127 47, 13 and 34"}
    res["agreements"] = agree
    res["verdict"] = "LANE_EQUALS_REVIEW_BUT_SEE_FIELDS" if not all(v is True or isinstance(v, int) for v in agree.values()) else "LANE_EQUALS_REVIEW"
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
