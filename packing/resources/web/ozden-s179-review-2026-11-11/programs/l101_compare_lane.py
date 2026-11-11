"""Hold the import lane's receipts to this review's, after the freeze. Decides nothing.

Usage: python -I -B l101_compare_lane.py LANE_PACKET_DIR REVIEW_OUT_DIR LANE_HEAD OUT.json

LANE_PACKET_DIR is lane L100's packet ozden-s179-upper-bound-2026-11-11 as committed at
LANE_HEAD (receipts/exact-certification.json decompressed beside its .xz). Compares, exactly
where both are exact: the certificate's digest, the side, the pairs tested, the least pair
gap on both maintained routes and the least containment clearance, against check-n179.json;
the house's contraction margin and binding pair against house-n179.json; the own-contraction
binding pair against the least pair; and the identity receipt's assignment and tilt counts
against identity-n179.json and band-n179.json.
"""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.set_int_max_str_digits(0)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    lane, mine, head, out = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
    cert = load(lane / "receipts/exact-certification.json")
    house = load(lane / "measure/contraction-n179.json")
    own = load(lane / "measure/contraction-n179-own.json")
    ident = load(lane / "measure/identity.json")
    check = load(mine / "check-n179.json")
    my_house = load(mine / "house-n179.json")
    my_ident = load(mine / "identity-n179.json")
    my_band = load(mine / "band-n179.json")
    rows = []

    def same(label: str, theirs: object, ours: object) -> None:
        rows.append({"what": label, "lane": theirs, "review": ours, "equal": theirs == ours})

    positive = next(c for c in cert["cases"] if c["control"] == "positive")
    least = F(check["least_pair_margin"]["value"])
    same("certificate SHA-256", hashlib.sha256((lane / "source/n-179-candidate.yaml").read_bytes()).hexdigest(),
         check["input"]["yaml_sha256"])
    for route in ("exact_verify", "independent"):
        r = positive[route]
        same(f"{route}: passed", r["verification_passed"], check["verdict"] == "ACCEPT")
        same(f"{route}: side", F(r["side"]), F(check["reading"]["side"]))
        same(f"{route}: least pair gap", F(r["minimum_best_pair_gap"]), least)
        same(f"{route}: least containment clearance is 0", F(r["minimum_containment_clearance"]) == 0,
             len(check["wall_contacts"]) > 0)
    same("pairs tested", positive["exact_verify"]["pairs_tested"], check["pairs_decided"])
    same("house contraction margin", F(house["margin"]), F(0))
    same("house binding pair", house["binding_pair"], my_house["touching_pairs"][0])
    same("own contraction binding pair", own["binding_pair"], check["least_pair_margin"]["pair"])
    entry = next(p for p in ident["pairs"] if p["against"] == "T-174" and p["view"] == "OZDEN")
    a = entry["assignment"]
    ll = next(r for r in my_ident["runs"] if r["anchor"] == "lower-left" and r["cost"] == "squared"
              and r["symmetry"] == "flip-y")
    same("assignment: moved beyond 1e-3", a["moved_beyond"]["1e-3"], ll["moved_beyond"]["1e-3"])
    same("assignment: moved beyond 0.1", a["moved_beyond"]["1e-1"], ll["moved_beyond"]["0.1"])
    same("assignment: largest move (6 places)", a["largest_move"], f"{ll['largest_move']:.6f}")
    same("assignment: turned beyond 1e-6 rad", a["turned_beyond_1e-6"], ll["turned_beyond_1e-6_rad"])
    same("assignment: largest turn (2 places)", a["largest_turn_degrees"], f"{ll['largest_turn_deg']:.2f}")
    same("nearest centres one to one", entry["nearest_centre"]["one_to_one"], ll["one_to_one_by_nearest"])
    t = ident["tilts"]
    new_beyond1 = [x for x in my_band["new"]["angles_deg"] if abs(x) > 1]
    same("new: tilted beyond 1 degree", t["OZDEN"]["tilted_beyond_1_degree"], len(new_beyond1))
    same("new: all negative", t["OZDEN"]["tilted_positive"] == 0, all(x < 0 for x in new_beyond1))
    house_angles = my_band["house_179"]["angles_deg"]
    same("house: tilted beyond 1 degree", t["T-174"]["tilted_beyond_1_degree"], len(house_angles))
    same("house: positive, negative", [t["T-174"]["tilted_positive"], t["T-174"]["tilted_negative"]],
         [sum(1 for x in house_angles if x > 0), sum(1 for x in house_angles if x < 0)])
    same("house: tilt range (4 places)", [round(v, 4) for v in t["T-174"]["tilt_range_degrees"]],
         [round(min(abs(x) for x in house_angles), 4), round(max(abs(x) for x in house_angles), 4)])
    receipt = {
        "program": "l101_compare_lane.py",
        "lane_head": head,
        "lane_files_sha256": {
            str(p.relative_to(lane)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(lane.rglob("*")) if p.is_file()
        },
        "rows": rows,
        "verdict": "LANE_EQUALS_REVIEW" if all(r["equal"] for r in rows) else "LANE_DIFFERS",
    }
    out.write_text(json.dumps(receipt, indent=1, default=str) + "\n", encoding="utf-8")
    for r in rows:
        print("equal" if r["equal"] else "DIFFERS", r["what"])
    print(receipt["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
