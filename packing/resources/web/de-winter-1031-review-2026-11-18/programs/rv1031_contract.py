"""The contraction margin of a packing, exactly, for the review of jlevy/squares#1031.

Written for this review; imports nothing from this repository or the source.

    python -I -B rv1031_contract.py --kind witness --file n-299.yaml [--twin-kind cert \
        --twin n299.cert] --out contraction.json

The packing is shrunk until its squares first touch: every centre is multiplied by one
factor ``g`` (about the origin; the side needed does not depend on the point), the
squares keeping their size and directions, and the box is taken as small as the moved
squares allow.  For a pair with centre difference ``d`` the margin at factor ``g`` is
``g M - H``, ``M`` the largest ``|d . w|`` over the pair's four unit normals and ``H`` the
sum of the two half-lengths (``rv1031_axes``), so the pair first touches at
``g_ij = H / M``; the packing first touches at ``g* = max g_ij``.  The side needed at
``g`` is the larger of the width and the height of the moved squares,
``max_i(g c_i + h_i) - min_i(g c_i - h_i)`` in each axis, and the contraction margin is
the stated side less the side needed at ``g*``.  It splits into the wall slack (the side
less the extent at ``g = 1``) and the part the contraction gains.

Both are exact rationals.  The program then decides, by method A, the contracted packing
moved to the lower-left corner of a box of the side needed (it must be accepted, with
contacts exactly at the pairs whose own factor is ``g*``) and the packing contracted
``10^-40`` further (those pairs, and only those, must overlap).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this packet's own modules, under python -I

import rv1031_axes as A
import rv1031_decide as D
import rv1031_reader as R

EPS = Fraction(1, 10**40)


def sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def needed_side(poses: list[A.Pose], g: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction]:
    """(side needed, width, height, xmin, ymin) of the packing with centres times g."""
    hs = [A.half_extent(p) for p in poses]
    xmin = min(g * p[0] - h for p, h in zip(poses, hs, strict=True))
    xmax = max(g * p[0] + h for p, h in zip(poses, hs, strict=True))
    ymin = min(g * p[1] - h for p, h in zip(poses, hs, strict=True))
    ymax = max(g * p[1] + h for p, h in zip(poses, hs, strict=True))
    w, ht = xmax - xmin, ymax - ymin
    return max(w, ht), w, ht, xmin, ymin


def contraction(poses: list[A.Pose], side: Fraction, verify: bool = True) -> dict:
    n = len(poses)
    t0 = time.process_time()
    factors: dict[tuple[int, int], Fraction] = {}
    overlap = []
    coincident = []
    for i in range(n):
        for j in range(i + 1, n):
            m, h, _ = A.pair_terms(poses[i], poses[j])
            if m == 0:
                coincident.append((i, j))
                continue
            if m < h:
                overlap.append((i, j))
            factors[(i, j)] = h / m
    if overlap or coincident:
        return {"verdict": "NOT_A_PACKING", "overlapping_pairs": [[i + 1, j + 1] for i, j in overlap[:50]], "coincident": [[i + 1, j + 1] for i, j in coincident[:50]]}
    g_star = max(factors.values())
    first = sorted(k for k, g in factors.items() if g == g_star)
    s1, w1, h1, _, _ = needed_side(poses, Fraction(1))
    sg, wg, hg, xg, yg = needed_side(poses, g_star)
    margin = side - sg
    ranked = sorted(factors.values(), reverse=True)
    rec = {
        "verdict": "MEASURED",
        "n": n,
        "pairs": len(factors),
        "side": D.fstr(side),
        "side_short": D.short(side, 30),
        "g_star": D.fstr(g_star),
        "one_less_g_star": D.fstr(1 - g_star),
        "one_less_g_star_short": D.short(1 - g_star),
        "first_contact_pairs": [[i + 1, j + 1] for i, j in first[:200]],
        "first_contact_pair_count": len(first),
        "next_factors_short": [D.short(1 - g) for g in ranked[len(first):len(first) + 5]],
        "pairs_touching_at_scale_one": sum(1 for g in factors.values() if g == 1),
        "extent_at_one": {"width": D.fstr(w1), "height": D.fstr(h1), "side_needed": D.fstr(s1)},
        "wall_slack": D.fstr(side - s1),
        "wall_slack_short": D.short(side - s1),
        "extent_at_g_star": {"width": D.fstr(wg), "height": D.fstr(hg), "side_needed": D.fstr(sg), "side_needed_short": D.short(sg, 30)},
        "contraction_part": D.fstr(s1 - sg),
        "contraction_part_short": D.short(s1 - sg),
        "contraction_margin": D.fstr(margin),
        "contraction_margin_short": D.short(margin),
        "cpu_s_factors": round(time.process_time() - t0, 2),
    }
    if verify:
        t1 = time.process_time()
        moved = [(g_star * p[0] - xg, g_star * p[1] - yg, p[2], p[3]) for p in poses]
        da = D.decide_a(moved, sg)
        sa = D.summarize_a(da, sg)
        contacts = {tuple(x) for x in sa["contact_pairs"]}
        expect = {(i + 1, j + 1) for i, j in first}
        ok_c = sa["classes"]["overlap"] == 0 and all(sa["walls"][w]["cross"] == 0 for w in D.WALLS) and contacts == expect and sa["contact_pairs_listed_all"]
        g_past = g_star * (1 - EPS)
        _, _, _, xp, yp = needed_side(poses, g_past)
        past = [(g_past * p[0] - xp, g_past * p[1] - yp, p[2], p[3]) for p in poses]
        mp = A.all_margins(past)
        over = {(i + 1, j + 1) for (i, j), m in mp.items() if m < 0}
        expect_past = {(i + 1, j + 1) for (i, j), g in factors.items() if g > g_past}
        ok_p = over == expect_past and len(over) > 0
        rec["verify"] = {
            "contracted_accepted_contacts_exactly_first_pairs": ok_c,
            "contracted_contacts": len(contacts),
            "contracted_wall_contacts": len(sa["wall_contacts"]),
            "past_overlaps_exactly_pairs_above": ok_p,
            "past_overlap_count": len(over),
            "cpu_s": round(time.process_time() - t1, 2),
        }
        if not (ok_c and ok_p):
            rec["verdict"] = "VERIFY_FAILED"
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True, choices=["json", "witness", "cert"])
    ap.add_argument("--file", required=True)
    ap.add_argument("--twin-kind", choices=["json", "witness", "cert"])
    ap.add_argument("--twin")
    ap.add_argument("--no-require-claim", action="store_true")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--label", default="")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    rec: dict = {"program": "rv1031_contract.py", "python": sys.version.split()[0], "label": args.label}
    doc = R.read_any(args.file, args.kind, require_claim=not args.no_require_claim)
    rec["input"] = {"path": args.file, "kind": args.kind, "sha256": sha256(args.file), "n": doc["n"], "side": D.fstr(doc["side"])}
    if args.twin:
        tw = R.read_any(args.twin, args.twin_kind, require_claim=not args.no_require_claim)
        same = tw["n"] == doc["n"] and tw["side"] == doc["side"]
        fails = []
        if same:
            for k in range(doc["n"]):
                if R.twin_match(R.pose_corners(doc["poses"][k]), R.pose_corners(tw["poses"][k])) is None:
                    fails.append(k + 1)
        rec["twin"] = {"path": args.twin, "kind": args.twin_kind, "sha256": sha256(args.twin), "same_count_and_side": same, "squares_differing": fails[:50], "differing_count": len(fails), "one_packing": same and not fails}
    rec.update(contraction(doc["poses"], doc["side"], verify=not args.no_verify))
    with open(args.out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(rec["verdict"], rec.get("contraction_margin_short"), rec.get("one_less_g_star_short"))
    return 0 if rec["verdict"] == "MEASURED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
