"""After the findings' freeze: the import lane's receipts held to this review's (lane L72).

Usage: python -I -B l72_compare_lane.py REPO COMMIT SRC REVIEW172 REVIEW270 OUT.json

Reads lane L71's packets from COMMIT of REPO (git show, read-only): the exact replay
receipts, the identity measurements and the packet READMEs' padding figures, and the draft
register entries' sides and scores. Holds each to this review's receipts, recomputes each
certificate's own uniform-contraction margin with l72_houses.contraction, and counts the
tilted squares within 1 degree of 45 degrees, whose sign in (-45, 45] is a convention.
Written and run after the findings were frozen (bead think-qqyg). Decides no bound.
"""

import json
import lzma
import math
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction  # noqa: E402

import numpy as np  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402

import l72_house as house  # noqa: E402
import l72_houses as houses  # noqa: E402
import l72_identity as ident  # noqa: E402
import l72_reader as reader  # noqa: E402
import l72_sat as sat  # noqa: E402
import l72_util as util  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PACKET = "packing/resources/web/ozden-s{n}-upper-bound-2026-11-09"
DRAFT_SCORE = {"172": 3, "270": 2}  # this review's frozen proposal (F8)


def show(repo, commit, path, binary=False):
    out = subprocess.run(
        ["git", "-C", repo, "show", f"{commit}:{path}"],
        capture_output=True,
        check=True,
        env={"PATH": "/usr/bin:/bin", "HOME": "/nonexistent", "GIT_CONFIG_NOSYSTEM": "1"},
    ).stdout
    return out if binary else out.decode("utf-8")


def frac(text):
    a, _, b = str(text).partition("/")
    return Fraction(int(a), int(b) if b else 1)


def turns_rad(cand, ref):
    C = np.array([(p[0], p[1]) for p in cand])
    R = np.array([(p[0], p[1]) for p in ref])
    D2 = ((C[:, None, :] - R[None, :, :]) ** 2).sum(axis=2)
    ri, ci = linear_sum_assignment(D2)
    return [math.radians(abs(ident.wrap90(cand[i][2] - ref[j][2]))) for i, j in zip(ri, ci)]


def main(argv):
    repo, commit, src, r172, r270, out = argv[1:7]
    reviews = {"172": r172, "270": r270}
    t0 = util.cpu_seconds()
    report = {
        "program": "l72_compare_lane.py",
        "lane": "L72",
        "bead": "think-qqyg",
        "lane_compared": "L71",
        "commit": commit,
        "environment": util.environment(),
        "program_digests": util.program_digests(
            [os.path.join(HERE, f) for f in ("l72_compare_lane.py", "l72_houses.py", "l72_identity.py", "l72_house.py", "l72_reader.py", "l72_sat.py", "l72_util.py")]
        ),
    }
    statements = json.load(open(os.path.join(HERE, "issue-statements.json")))
    results_text = show(repo, commit, "packing/frontier/results.yaml")
    mismatches = []
    for n in ("172", "270"):
        st = statements[n]
        mine = json.load(open(os.path.join(reviews[n], "out", f"check-n{n}.json")))
        my_ident = json.load(open(os.path.join(reviews[n], "out", f"identity-n{n}.json")))
        pk = PACKET.format(n=n)
        ec = json.loads(lzma.decompress(show(repo, commit, f"{pk}/receipts/exact-certification.json.xz", binary=True)))
        pos = [c for c in ec["cases"] if c.get("control") == "positive"][0]
        my_gap = frac(mine["pairs"]["least_margin"]["margin"])
        row = {"packet": pk}
        replay = {}
        for route in ("exact_verify", "independent"):
            r = pos[route]
            gap = frac(r["minimum_best_pair_gap"])
            clr = frac(r["minimum_containment_clearance"])
            replay[route] = {
                "passed": r["verification_passed"],
                "pairs_tested": r["pairs_tested"],
                "least_pair_gap_equals_review": gap == my_gap,
                "least_clearance": util.frac_str(clr),
                "least_clearance_equals_review": clr == 0 and len(mine["walls"]["contacts"]) > 0,
                "side_equals_review": frac(r["side"]) == frac(mine["side"]),
            }
            if not (replay[route]["least_pair_gap_equals_review"] and replay[route]["side_equals_review"] and replay[route]["passed"]):
                mismatches.append(f"{n} {route}")
        row["replay"] = replay
        # identity
        li = json.loads(show(repo, commit, f"{pk}/measure/identity.json"))
        pair = [p for p in li["pairs"] if p["view"] == "OZDEN" and p["against"].startswith("T-")][0]
        a = pair["assignment"]
        mb = my_ident["house"]["lower-left"]["best"]
        mine_moved = mb["moved_beyond"]
        cmp_moved = {
            k: (a["moved_beyond"][k], mine_moved[m])
            for k, m in (("1e-9", "1e-9"), ("1e-6", "1e-6"), ("1e-3", "1e-3"), ("1e-2", "0.01"), ("1e-1", "0.1"))
        }
        # turns beyond 1e-6 radian, recomputed here from this review's poses
        data = reader.read_files(os.path.join(src, f"s{n}-upper-bound", f"n-{n}-candidate.yaml"))
        cand = ident.cert_poses(data)
        hw = house.read_center_basis(os.path.join(repo, st["house_witness"]))
        ref = ident.house_poses(hw)
        tr = turns_rad(cand, ref)
        near45 = {
            "candidate": sum(1 for p in cand if abs(p[2]) > 44.0),
            "house": sum(1 for p in ref if abs(p[2]) > 44.0),
        }
        sign_flips = []
        C = np.array([(p[0], p[1]) for p in cand])
        R = np.array([(p[0], p[1]) for p in ref])
        ri, ci = linear_sum_assignment(((C[:, None, :] - R[None, :, :]) ** 2).sum(axis=2))
        for i, j in zip(ri, ci):
            if abs(cand[i][2]) > 1 and abs(ref[j][2]) > 1 and (cand[i][2] > 0) != (ref[j][2] > 0):
                sign_flips.append(
                    {
                        "square": data["ids"][i],
                        "from_deg": round(ref[j][2], 3),
                        "to_deg": round(cand[i][2], 3),
                        "turn_deg": round(abs(ident.wrap90(cand[i][2] - ref[j][2])), 3),
                    }
                )
        row["identity"] = {
            "nearest_one_to_one": (pair["nearest_centre"]["one_to_one"], mb["nearest_one_to_one"]),
            "moved_beyond_lane_review": cmp_moved,
            "largest_move_lane_review": (a["largest_move"], mb["largest_move"]),
            "largest_turn_lane_review": (a["largest_turn_degrees"], mb["largest_turn_deg"]),
            "turned_beyond_1e-6_rad_lane_review": (a["turned_beyond_1e-6"], sum(1 for t in tr if t > 1e-6)),
            "tilted_beyond_1deg_lane": (li["tilts"]["OZDEN"]["tilted_beyond_1_degree"], li["tilts"]["house-witness"]["tilted_beyond_1_degree"]),
            "tilted_beyond_1deg_review": (my_ident["candidate_tilts"]["beyond_1deg"], my_ident["house"]["reference_tilts"]["beyond_1deg"]),
            "lane_opposite_sign": pair.get("bands", {}).get("tilted_paired_opposite_sign"),
            "sign_changes_recomputed": sign_flips,
            "tilted_within_1deg_of_45": near45,
        }
        for k, (x, y) in cmp_moved.items():
            if x != y:
                mismatches.append(f"{n} moved beyond {k}: lane {x}, review {y}")
        if abs(float(a["largest_move"]) - float(mb["largest_move"])) > 1e-6:
            mismatches.append(f"{n} largest move")
        # padding: the lane's README figures against houses.json, and each certificate's own margin
        readme = show(repo, commit, f"{pk}/README.md").translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"))
        m = re.search(r"loses ([0-9.]+) × 10⁻(\d+) of side", readme)
        m2 = re.search(r"own margin,\s+measured the same way, is ([0-9.]+) × 10⁻(\d+)", readme)
        hj = json.load(open(os.path.join(r172, "out", "houses.json")))[n]["contraction"]
        own = houses.contraction(
            {
                "n": data["n"],
                "side": data["side"],
                "ids": data["ids"],
                "corners": data["corners"],
                "centres": [
                    ((Q[0][0] + Q[2][0]) / 2, (Q[0][1] + Q[2][1]) / 2) for Q in (sat.corners_frac(c) for c in data["corners"])
                ],
                "bases": None,
            }
        )
        own.pop("_margin_fraction", None)
        row["padding"] = {
            "lane_house_margin": f"{m.group(1)}e-{m.group(2)}" if m else None,
            "review_house_margin": hj["margin"],
            "lane_certificate_own_margin": f"{m2.group(1)}e-{m2.group(2)}" if m2 else None,
            "review_certificate_own_margin": own["margin"],
            "review_certificate_one_minus_lambda": own["one_minus_lambda_star"],
            "review_certificate_binding_pair": own["binding_pair"],
            "review_certificate_contracted_decided": {k: v["verdict"] for k, v in own["decided"].items()},
        }
        # the draft entry: side and score
        blocks = re.split(r"\n  - id: ", results_text)
        entry = [b for b in blocks if f"scope:\n      n_values:\n      - {n}\n" in b and "Özden" in b.split("claim:")[0]]
        side_ok = None
        score = None
        if entry:
            e = entry[-1]
            mm = re.search(r"s\(" + n + r"\) <=\s+(\d+/\d+)", e)
            side_ok = mm is not None and frac(mm.group(1)) == frac(mine["side"])
            sm = re.search(r"significance:\n\s+score: (\d)", e)
            score = int(sm.group(1)) if sm else None
        row["draft_entry"] = {"found": bool(entry), "side_equals_certificate": side_ok, "score": score, "review_score": DRAFT_SCORE[n]}
        report[n] = row
    report["mismatches"] = mismatches
    report["verdict"] = "LANE_EQUALS_REVIEW" if not mismatches else "LANE_DIFFERS"
    report["cpu_seconds"] = round(util.cpu_seconds() - t0, 2)
    util.write_receipt(out, report)
    print(json.dumps({k: v for k, v in report.items() if k not in ("environment", "program_digests")}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
