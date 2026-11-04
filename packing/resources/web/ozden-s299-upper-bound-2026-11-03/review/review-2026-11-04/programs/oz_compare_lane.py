"""Hold the import lane's receipts to this review's own results. Decides nothing about the bound.

Usage: oz_compare_lane.py CERT.yaml EXACT_CERTIFICATION.json.xz SHARP_CONTROLS.json IDENTITY.json
                          MY_CHECK.json MY_IDENTITY.json OUT.json

1. The maintained routes decided (x, y, t) poses that the lane converted from the certificate.
   Each positive pose is turned back into a basis, ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)), and
   must equal the certificate's square exactly; each control must differ from the
   certificate only where the control says.
2. The routes' least pair gap and least clearance must equal this review's exact values.
3. The lane's identity and sharp-control receipts are compared with this review's numbers.
"""

from __future__ import annotations

import json
import lzma
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ozlib as oz  # noqa: E402


def basis_of(t: Fraction):
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def main() -> int:
    cert_p, ec_p, sc_p, id_p, mine_p, myid_p, out_p = sys.argv[1:8]
    t0 = time.process_time()
    doc = oz.read_witness_yaml(cert_p)
    squares = [(oz.to_F(s["center"][0]), oz.to_F(s["center"][1]), oz.to_F(s["basis"][0]), oz.to_F(s["basis"][1]))
               for s in doc["squares"]]
    ec = json.loads(lzma.decompress(Path(ec_p).read_bytes()))
    cases = []
    for case in ec["cases"]:
        poses = case["checker_input"]["poses"]
        diffs = []
        for k, (p, s) in enumerate(zip(poses, squares)):
            x, y, t = (oz.to_F(v) for v in p)
            a, b = basis_of(t)
            if (x, y, a, b) != s:
                diffs.append(k)
        side_ok = oz.to_F(case["checker_input"]["side"]) == oz.to_F(doc["header"]["side"])
        row = {
            "control": case["control"],
            "poses": len(poses),
            "pose_count_is_n": len(poses) == len(squares),
            "side_is_certificate": side_ok,
            "indices_differing_from_certificate": diffs,
            "routes_passed": {r: case[r]["verification_passed"] for r in ec["routes"]},
            "routes_least_gap": {r: case[r]["minimum_best_pair_gap"] for r in ec["routes"]},
            "routes_least_clearance": {r: case[r]["minimum_containment_clearance"] for r in ec["routes"]},
            "routes_pairs_tested": {r: case[r]["pairs_tested"] for r in ec["routes"]},
        }
        if case["control"] == "duplicate-square-overlap" and diffs:
            k = diffs[0]
            row["duplicate_equals_square"] = [
                j for j, p in enumerate(poses)
                if j != k and [oz.to_F(v) for v in p] == [oz.to_F(v) for v in poses[k]]]
        cases.append(row)
    mine = json.loads(Path(mine_p).read_text())
    pos = next(c for c in cases if c["control"] == "positive")
    agree = {
        "positive_poses_are_certificate": not pos["indices_differing_from_certificate"] and pos["pose_count_is_n"] and pos["side_is_certificate"],
        "least_gap_equal": all(oz.to_F(v) == oz.to_F(mine["pairs"]["least_margin"]) for v in pos["routes_least_gap"].values()),
        "least_clearance_equal": all(oz.to_F(v) == oz.to_F(mine["walls"]["least_clearance"]) for v in pos["routes_least_clearance"].values()),
        "pairs_tested_equal": all(v == mine["pairs"]["pairs_decided"] for v in pos["routes_pairs_tested"].values()),
    }
    sc = json.loads(Path(sc_p).read_text())
    tight = next(c for c in sc["controls"] if c["control"] == "tightest-pair-closed-past-contact")
    agree["sharp_tightest_pair_equal"] = sorted([tight["detail"]["square"], tight["detail"]["partner"]]) == sorted(mine["pairs"]["least_margin_pair"][:2])
    agree["sharp_all_as_expected"] = sc["all_as_expected"]
    lid = json.loads(Path(id_p).read_text())
    myid = json.loads(Path(myid_p).read_text())
    lp = lid["pairs"][0]
    me = next(r for r in myid["by_symmetry"] if r["symmetry"] == "identity")
    lane_moves = lp["assignment"]["moved_beyond"]
    my_moves = me["moved_beyond"]
    agree["identity_one_to_one_both"] = lp["nearest_centre"]["one_to_one"] and me["nearest_one_to_one"] and lp["nearest_centre"]["symmetry"] == 0
    agree["identity_moves_equal"] = {
        k: (lane_moves[k], my_moves[m]) for k, m in (("1e-9", "1e-09"), ("1e-6", "1e-06"), ("1e-3", "0.001"), ("1e-2", "0.01"), ("1e-1", "0.1"))}
    agree["identity_moves_all_equal"] = all(a == b for a, b in agree["identity_moves_equal"].values())
    agree["identity_max_move"] = (lp["assignment"]["largest_move"], round(me["max_move"], 6))
    names = [k for k in lid["tilts"] if k != "OZDEN"]
    agree["tilts_lane"] = {k: (lid["tilts"][k]["exactly_turned"], lid["tilts"][k]["tilted_beyond_1_degree"]) for k in lid["tilts"]}
    agree["tilts_mine"] = {"OZDEN": (myid["tilts_candidate"]["exact_nonaxis"], myid["tilts_candidate"][">1deg"]),
                           names[0]: (myid["tilts_house"]["exact_nonaxis"], myid["tilts_house"][">1deg"])}
    agree["tilts_equal"] = agree["tilts_lane"] == {k: tuple(v) for k, v in agree["tilts_mine"].items()}
    agree["lane_turned_beyond_1e-6"] = lp["assignment"]["turned_beyond_1e-6"]
    agree["mine_turned_beyond_deg"] = me["turned_beyond_deg"]
    receipt = {
        "program": "oz_compare_lane.py",
        "program_sha256": oz.sha256_file(__file__),
        "ozlib_sha256": oz.sha256_file(HERE / "ozlib.py"),
        "python": platform.python_version(),
        "argv": sys.argv[1:],
        "replay_cases": cases,
        "agreement": agree,
        "decides": "nothing about the bound; a comparison of receipts",
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    Path(out_p).write_text(json.dumps(receipt, indent=1) + "\n")
    print(json.dumps({k: v for k, v in agree.items()}, indent=None)[:1500])
    for c in cases:
        print(" ", c["control"], "differ", c["indices_differing_from_certificate"][:5], c.get("duplicate_equals_square"), c["routes_passed"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
