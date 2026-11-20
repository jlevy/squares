"""Decide the certificate of jlevy/squares#1031 by both methods, directly and crossed.

Written for this review; imports nothing from this repository or the source.

    python -I -B rv1031_check.py --json n299_exact.json --witness n299_witness.yaml \
        --claim 17.793636991744 --out check.json

1. Read form J (poses) and form C (corners) strictly (``rv1031_reader``).
2. The twin relation: square k of form C is square k of form J, its four corners a
   cyclic rotation, in either sense, of ``c +- u/2 +- v/2``.
3. Direct decision: method A on form J's poses, method B on form C's corners; equal
   classes at every pair and wall, equal clearances, area inside exactly 1.
4. Crossed decision: method A on the poses taken from form C's corners, method B on the
   corners written from form J's poses; margins identical to the direct decision's at
   every pair, classes and areas identical.
5. The side: the two forms' sides equal; the packing's exact extent; whether the claim is
   the ceiling of the side at its decimal places; the squares decided in the box of the
   claim by both methods.

The verdict is ACCEPT only when every step holds and no pair overlaps and no square
crosses a wall.  Contact (a margin or clearance of exactly 0) is allowed: the bound needs
disjoint interiors inside the closed box.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this packet's own modules, under python -I

import rv1031_axes as A
import rv1031_clip as B
import rv1031_decide as D
import rv1031_reader as R


def decimal_ceiling(v: Fraction, places: int) -> Fraction:
    scale = 10**places
    q = -((-v.numerator * scale) // v.denominator)
    return Fraction(q, scale)


def parse_decimal(text: str) -> tuple[Fraction, int]:
    if not text.replace(".", "", 1).isdigit():
        raise ValueError(text)
    if "." in text:
        a, b = text.split(".")
        return Fraction(int(a + b), 10 ** len(b)), len(b)
    return Fraction(int(text)), 0


def sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(json_path: str, witness_path: str, claim_text: str) -> dict:
    t0 = time.process_time()
    rec: dict = {"program": "rv1031_check.py", "python": sys.version.split()[0], "platform": platform.platform(), "arith": B.version()}
    rec["inputs"] = {"json": {"path": json_path, "sha256": sha256(json_path)}, "witness": {"path": witness_path, "sha256": sha256(witness_path)}}
    problems: list[str] = []
    try:
        dj = R.read_json(json_path)
    except R.ReadError as exc:
        return {**rec, "verdict": "REFUSE", "problems": [f"form J refused: {exc}"]}
    try:
        dc = R.read_witness(witness_path)
    except R.ReadError as exc:
        return {**rec, "verdict": "REFUSE", "problems": [f"form C refused: {exc}"]}
    if dc["representation"] != "corners":
        return {**rec, "verdict": "REFUSE", "problems": ["form C is not a corners witness"]}
    n = dj["n"]
    side = dj["side"]
    rec["reading"] = {
        "json": {k: v for k, v in dj["facts"].items() if k != "notes"} | {"notes": dj["facts"]["notes"][:20], "note_count": len(dj["facts"]["notes"])},
        "witness": {k: v for k, v in dc["facts"].items() if k != "notes"} | {"notes": dc["facts"]["notes"][:20], "note_count": len(dc["facts"]["notes"])},
    }
    if dc["n"] != n:
        problems.append(f"counts differ: J {n}, C {dc['n']}")
    if dc["side"] != side:
        problems.append("the two forms state different sides")
    rec["side"] = {"exact": D.fstr(side), "short": D.short(side, 30), "same_in_both_forms": dc["side"] == side, "same_text": dj["facts"]["side_text"] == dc["facts"]["side_text"]}
    if problems:
        return {**rec, "verdict": "REFUSE", "problems": problems}

    poses_j = dj["poses"]
    corners_c = dc["corners"]
    # 2. the twin relation
    twin_counts: dict[str, int] = {}
    twin_fail = []
    for k in range(n):
        m = R.twin_match(R.pose_corners(poses_j[k]), corners_c[k])
        if m is None:
            twin_fail.append(k + 1)
        else:
            key = f"offset {m[0]} {m[1]}"
            twin_counts[key] = twin_counts.get(key, 0) + 1
    rec["twin"] = {"holds_at": n - len(twin_fail), "fails_at": twin_fail[:50], "fail_count": len(twin_fail), "listings": twin_counts}
    if twin_fail:
        problems.append(f"the twin relation fails at {len(twin_fail)} squares")
    t1 = time.process_time()
    # 3. direct decision
    da = D.decide_a(poses_j, side)
    t2 = time.process_time()
    db = D.decide_b(corners_c, side)
    t3 = time.process_time()
    cmp_direct = D.compare(da, db)
    sa = D.summarize_a(da, side)
    sb = D.summarize_b(db)
    rec["direct"] = {"method_a": sa, "method_b": sb, "compare": cmp_direct, "cpu_s": {"a": round(t2 - t1, 2), "b": round(t3 - t2, 2)}}
    if not D.verdict_ok(sa, cmp_direct):
        problems.append("the direct decision does not accept")
    # 4. crossed decision
    poses_c = [R.corners_pose(c) for c in corners_c]
    if any(p is None for p in poses_c):
        problems.append("a form C square gives no pose")
        rec["crossed"] = {"poses_from_corners": "failed"}
    else:
        corners_j = [R.pose_corners(p) for p in poses_j]
        da2 = D.decide_a([p for p in poses_c if p is not None], side)
        t4 = time.process_time()
        db2 = D.decide_b(corners_j, side)
        t5 = time.process_time()
        same_margins = da2["margins"] == da["margins"]
        same_clear = da2["clearances"] == da["clearances"]
        same_b = db2.get("classes") == db.get("classes")
        cmp_crossed = D.compare(da2, db2)
        sa2 = D.summarize_a(da2, side)
        rec["crossed"] = {
            "margins_identical_to_direct": same_margins,
            "clearances_identical_to_direct": same_clear,
            "method_b_classes_and_areas_identical_to_direct": same_b,
            "margins_sha256": sa2["margins_sha256"],
            "compare": cmp_crossed,
            "cpu_s": {"a": round(t4 - t3, 2), "b": round(t5 - t4, 2)},
        }
        if not (same_margins and same_clear and same_b and D.verdict_ok(sa2, cmp_crossed)):
            problems.append("the crossed decision differs or does not accept")
    # 5. the side and the claim
    ext = D.extent(poses_j)
    claim, places = parse_decimal(claim_text)
    ceil = decimal_ceiling(side, places)
    rec["extent"] = {k: D.fstr(v) for k, v in ext.items()} | {
        "side_less_width": D.fstr(side - ext["width"]),
        "side_less_height": D.fstr(side - ext["height"]),
        "box_is_tight": max(ext["width"], ext["height"]) == side and ext["xmin"] == 0 and ext["ymin"] == 0,
    }
    claim_walls_a = [A.clearances(p, claim) for p in poses_j]
    claim_b = D.decide_b(corners_c, claim, pairs=[])
    claim_walls_b_ok = all(min(B.mpq_to_fraction(x) for x in w) >= 0 for w in claim_b["walls"]) and all(a == 1 for a in claim_b["inside"])
    claim_ok_a = all(min(c) >= 0 for c in claim_walls_a)
    rec["claim"] = {
        "text": claim_text,
        "exact": D.fstr(claim),
        "places": places,
        "ceiling_of_side_at_places": D.fstr(ceil),
        "claim_is_ceiling": ceil == claim,
        "claim_less_side": D.fstr(claim - side),
        "claim_less_side_short": D.short(claim - side),
        "accepted_in_box_of_claim_a": claim_ok_a,
        "accepted_in_box_of_claim_b": claim_walls_b_ok,
    }
    if not (claim >= side and claim_ok_a and claim_walls_b_ok):
        problems.append("the claim is not proved by the squares in its box")
    rec["problems"] = problems
    rec["verdict"] = "ACCEPT" if not problems else "REFUSE"
    rec["cpu_s_total"] = round(time.process_time() - t0, 2)
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--witness", required=True)
    ap.add_argument("--claim", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    rec = run(args.json, args.witness, args.claim)
    with open(args.out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(rec["verdict"], rec.get("problems"))
    return 0 if rec["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
