"""Lineage: a certificate measured against its house and regularized view (lane L72, bead think-qqyg).

Usage: python -I -B l72_identity.py STATEMENTS.json COUNT SRC REPO_ROOT OUT.json

Pose by pose, in binary64, under all eight symmetries of the reference's own box, with two
anchorings: the reference box's symmetry applied in its own frame and compared with the
certificate in its frame (lower-left anchoring), and both packings centred on their box
centres (centre anchoring). For each: nearest-centre pairing (one to one or not) and SciPy's
optimal assignment of least summed squared move, with the moves and turns of the best
symmetry. A square's turn is its edge direction modulo 90 degrees, in (-45, 45]. Decides no
bound.
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402
from scipy.spatial import cKDTree  # noqa: E402

import l72_house as house  # noqa: E402
import l72_reader as reader  # noqa: E402
import l72_util as util  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def wrap90(deg):
    """An angle in degrees reduced modulo 90 into (-45, 45]."""
    a = math.fmod(deg, 90.0)
    if a <= -45.0:
        a += 90.0
    elif a > 45.0:
        a -= 90.0
    return a


def cert_poses(data):
    out = []
    for c in data["corners"]:
        pts = [(xn / xd, yn / yd) for (xn, xd, yn, yd) in c]
        cx = (pts[0][0] + pts[2][0]) / 2
        cy = (pts[0][1] + pts[2][1]) / 2
        # edge direction p1 - p0 from exact integers, then to float
        from fractions import Fraction

        ux = Fraction(c[1][0], c[1][1]) - Fraction(c[0][0], c[0][1])
        uy = Fraction(c[1][2], c[1][3]) - Fraction(c[0][2], c[0][3])
        ang = math.degrees(math.atan2(float(uy), float(ux)))
        out.append((cx, cy, wrap90(ang)))
    return out


def house_poses(hw):
    out = []
    for (cx, cy), (c, s) in zip(hw["centres"], hw["bases"]):
        out.append((float(cx), float(cy), wrap90(math.degrees(math.atan2(float(s), float(c))))))
    return out


SYMS = ["identity", "rot90", "rot180", "rot270", "flip_x", "flip_y", "transpose", "antitranspose"]


def sym_apply(name, x, y, a, S):
    """A symmetry of the box [0, S]^2 applied to a pose (centre, angle mod 90)."""
    if name == "identity":
        return x, y, a
    if name == "rot90":
        return S - y, x, a
    if name == "rot180":
        return S - x, S - y, a
    if name == "rot270":
        return y, S - x, a
    if name == "flip_x":
        return S - x, y, wrap90(-a)
    if name == "flip_y":
        return x, S - y, wrap90(-a)
    if name == "transpose":
        return y, x, wrap90(-a)
    if name == "antitranspose":
        return S - y, S - x, wrap90(-a)
    raise ValueError(name)


def compare(cand, ref, Sc, Sr, anchor):
    """Measure cand against every symmetric image of ref. Returns per-symmetry rows."""
    rows = {}
    C = np.array([(p[0], p[1]) for p in cand])
    for name in SYMS:
        R = [sym_apply(name, x, y, a, Sr) for (x, y, a) in ref]
        RC = np.array([(r[0], r[1]) for r in R])
        if anchor == "centre":
            Cm = C - Sc / 2
            RCm = RC - Sr / 2
        else:
            Cm, RCm = C, RC
        tree = cKDTree(RCm)
        _, nn = tree.query(Cm)
        one_to_one = len(set(nn.tolist())) == len(cand)
        seen = {}
        for ci_, r_ in enumerate(nn.tolist()):
            seen.setdefault(r_, []).append(ci_)
        shared = [{"reference_index": r_, "candidates": v} for r_, v in seen.items() if len(v) > 1]
        D2 = ((Cm[:, None, :] - RCm[None, :, :]) ** 2).sum(axis=2)
        ri, ci = linear_sum_assignment(D2)
        cost = float(D2[ri, ci].sum())
        moves = np.sqrt(D2[ri, ci])
        turns = np.array([abs(wrap90(cand[i][2] - R[j][2])) for i, j in zip(ri, ci)])
        rows[name] = {
            "nearest_one_to_one": one_to_one,
            "nearest_distinct": len(set(nn.tolist())),
            "assignment_cost": cost,
            "_moves": moves,
            "_turns": turns,
            "_pairs": list(zip(ri.tolist(), ci.tolist())),
            "_shared": shared,
        }
    return rows


def describe(row, cand, ref, cand_ids, ref_ids):
    moves = row["_moves"]
    turns = row["_turns"]
    k = int(np.argmax(moves))
    t = int(np.argmax(turns))
    pairs = row["_pairs"]
    return {
        "nearest_one_to_one": row["nearest_one_to_one"],
        "nearest_distinct": row["nearest_distinct"],
        "assignment_cost": row["assignment_cost"],
        "moved_beyond": {th: int((moves > float(th)).sum()) for th in ("1e-9", "1e-6", "1e-3", "0.01", "0.05", "0.1")},
        "within_0.05": int((moves <= 0.05).sum()),
        "largest_move": round(float(moves[k]), 6),
        "largest_move_square": [cand_ids[pairs[k][0]], ref_ids[pairs[k][1]]],
        "turned_beyond_deg": {th: int((turns > float(th)).sum()) for th in ("1e-6", "0.01", "0.5", "1")},
        "largest_turn_deg": round(float(turns[t]), 4),
        "largest_turn_square": [cand_ids[pairs[t][0]], ref_ids[pairs[t][1]]],
        "largest_turn_from_to_deg": [round(ref[pairs[t][1]][2], 4), round(cand[pairs[t][0]][2], 4)],
        "same_id": int(sum(1 for i, j in pairs if cand_ids[i] == ref_ids[j])),
        "moved_beyond_0.05_list": [
            {
                "square": cand_ids[i],
                "matched": ref_ids[j],
                "from": [round(ref[j][0], 4), round(ref[j][1], 4), round(ref[j][2], 3)],
                "to": [round(cand[i][0], 4), round(cand[i][1], 4), round(cand[i][2], 3)],
                "move": round(float(moves[q]), 4),
            }
            for q, (i, j) in enumerate(pairs)
            if moves[q] > 0.05
        ],
        "turned_beyond_1deg_list": [
            {
                "square": cand_ids[i],
                "matched": ref_ids[j],
                "at": [round(cand[i][0], 3), round(cand[i][1], 3)],
                "from_deg": round(ref[j][2], 3),
                "to_deg": round(cand[i][2], 3),
            }
            for q, (i, j) in enumerate(pairs)
            if turns[q] > 1.0
        ],
        "shared_nearest": [
            {"reference": ref_ids[e["reference_index"]], "candidates": [cand_ids[c] for c in e["candidates"]]}
            for e in row.get("_shared", [])
        ],
    }


def tilt_counts(poses):
    tilts = np.array([abs(p[2]) for p in poses])
    return {
        "beyond_1e-9_rad": int((np.radians(tilts) > 1e-9).sum()),
        "beyond_0.5deg": int((tilts > 0.5).sum()),
        "beyond_1deg": int((tilts > 1.0).sum()),
        "exactly_upright_float": int((tilts == 0.0).sum()),
    }


def main(argv):
    statements = json.load(open(argv[1]))
    count = argv[2]
    src, repo_root, out = argv[3], argv[4], argv[5]
    st = statements[count]
    repo = os.path.join(src, st["repository"].split("/")[1])
    data = reader.read_files(os.path.join(repo, st["certificate"]))
    cand = cert_poses(data)
    Sc = data["side"][0] / data["side"][1]
    report = {
        "program": "l72_identity.py",
        "lane": "L72",
        "bead": "think-qqyg",
        "count": count,
        "environment": util.environment(),
        "program_digests": util.program_digests(
            [os.path.join(HERE, f) for f in ("l72_identity.py", "l72_house.py", "l72_reader.py", "l72_util.py")]
        ),
        "candidate_tilts": tilt_counts(cand),
    }
    refs = {"house": st["house_witness"], "view": st["house_view"]}
    for label, path in refs.items():
        hw = house.read_center_basis(os.path.join(repo_root, path))
        ref = house_poses(hw)
        Sr = hw["side"][0] / hw["side"][1]
        block = {"path": path, "witness_id": hw["witness_id"], "reference_tilts": tilt_counts(ref)}
        for anchor in ("lower-left", "centre"):
            rows = compare(cand, ref, Sc, Sr, anchor)
            best = min(rows, key=lambda nm: rows[nm]["assignment_cost"])
            block[anchor] = {
                "best_symmetry": best,
                "best": describe(rows[best], cand, ref, data["ids"], hw["ids"]),
                "per_symmetry": {
                    nm: {"assignment_cost": round(r["assignment_cost"], 6), "nearest_one_to_one": r["nearest_one_to_one"]}
                    for nm, r in rows.items()
                },
            }
        report[label] = block
    # the view against the house, under the identity
    hw = house.read_center_basis(os.path.join(repo_root, st["house_witness"]))
    vw = house.read_center_basis(os.path.join(repo_root, st["house_view"]))
    rows = compare(house_poses(vw), house_poses(hw), vw["side"][0] / vw["side"][1], hw["side"][0] / hw["side"][1], "lower-left")
    report["view_against_house"] = describe(rows["identity"], house_poses(vw), house_poses(hw), vw["ids"], hw["ids"])
    lin = st["lineage"]
    report["issue_statements"] = lin
    util.write_receipt(out, report)
    print(json.dumps({k: v for k, v in report.items() if k not in ("environment", "program_digests")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
