"""Decide a certificate by both methods, natively and crossed (lane r1021-1118).

Usage, from this packet's programs/ directory, with the project interpreter:

    python -I -B r1021_check.py report LABEL FORM_J FORM_C OUT.json
    python -I -B r1021_check.py house LABEL CORNERS OUT.json

A report is a centre file (form J) and its corner twin (form C).  The verdict is ACCEPT
only when both files read strictly, they are one packing (square k of form C is the
square of row k of form J, as a cyclic corner list in either sense), method A
(r1021_geom, poses) and method B (r1021_clip, corners) accept every square, wall and
pair of each file with equal classes everywhere, and the margins and clearances read
from the two files are identical.  Form J is decided by A natively and by B on the
corners it implies; form C by B natively and by A on the poses its corners imply.
A house file (one Witness/v2 corners file with integer ids) is decided by B natively
and A on its implied poses.

Every decision is exact: integers, Fractions and GMP rationals; no tolerance and no
distance filter.  Floating point appears only in printed tilts.
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this packet's programs/, run with -I

import hashlib
import json
import math
import sys
import time
from fractions import Fraction

import r1021_clip as clipmod
import r1021_geom as geom
import r1021_read as rd
from r1021_fmt import floor_places, frac_text, sci

THRESHOLDS = [("1e-27", Fraction(1, 10**27)), ("1e-12", Fraction(1, 10**12)),
              ("1e-9", Fraction(1, 10**9)), ("1e-6", Fraction(1, 10**6)), ("1e-3", Fraction(1, 10**3))]


def a_class(m: Fraction) -> str:
    return "apart" if m > 0 else ("contact" if m == 0 else "overlap")


def decide(poses, corners, side: Fraction) -> dict:
    """Method A on poses and method B on corners; their agreement and the verdict."""
    t0 = time.process_time()
    a = geom.decide_poses(poses, side)
    ta = time.process_time() - t0
    t0 = time.process_time()
    b = clipmod.decide_corners(corners, side)
    tb = time.process_time() - t0
    n = len(poses)
    pairs = geom.pair_index(n)
    a_classes = [a_class(m) for m in a["margins"]]
    pair_disagree = []
    for k, (ac, bp) in enumerate(zip(a_classes, b["pairs"], strict=True)):
        if not (ac == bp[0] == bp[2] and bp[1] == bp[3]):
            pair_disagree.append(pairs[k])
    a_walls = [tuple(clipmod.wall_class_from_clearance(v) for v in cl) for cl in a["clearances"]]
    b_walls = [tuple(clipmod.WALL_FROM_CLIP[w] for w in ws) for ws in b["walls"]]
    wall_disagree = [k for k in range(n) if a_walls[k] != b_walls[k]]
    unit_disagree = sorted(set(a["not_unit"]) ^ set(b["not_unit"]))
    a_cross = sorted({k for k, cl in enumerate(a["clearances"]) if min(cl) < 0})
    b_cross = sorted({k for k, ws in enumerate(b_walls) if "crossing" in ws})
    area_short = [k for k, ar in enumerate(b["inside_area"]) if ar != 1]
    a_overlap = [pairs[k] for k, c in enumerate(a_classes) if c == "overlap"]
    b_overlap = [pairs[k] for k, bp in enumerate(b["pairs"]) if "overlap" in (bp[0], bp[2])]
    accept = not (a["not_unit"] or b["not_unit"] or a_cross or b_cross or area_short
                  or a_overlap or b_overlap or pair_disagree or wall_disagree or unit_disagree)
    return {
        "accept": accept,
        "a": a,
        "b": b,
        "a_classes": a_classes,
        "a_walls": a_walls,
        "b_walls": b_walls,
        "pair_disagree": pair_disagree,
        "wall_disagree": wall_disagree,
        "unit_disagree": unit_disagree,
        "a_not_unit": a["not_unit"],
        "b_not_unit": b["not_unit"],
        "a_cross": a_cross,
        "b_cross": b_cross,
        "area_short": area_short,
        "a_overlap": a_overlap,
        "b_overlap": b_overlap,
        "cpu": {"A": round(ta, 2), "B": round(tb, 2)},
    }


def margins_digest(margins) -> str:
    h = hashlib.sha256()
    for m in margins:
        h.update(frac_text(m).encode() + b"\n")
    return h.hexdigest()


def canonical_direction(c: Fraction, s: Fraction):
    """The one of (c, s), (-s, c), (-c, -s), (s, -c) with first coordinate > 0 and second >= 0."""
    for cc, ss in ((c, s), (-s, c), (-c, -s), (s, -c)):
        if cc > 0 and ss >= 0:
            return cc, ss
    raise ValueError("zero direction")


def tilt_degrees(c: Fraction, s: Fraction) -> float:
    cc, ss = canonical_direction(c, s)
    ang = math.degrees(math.atan2(float(ss), float(cc)))
    return min(ang, 90.0 - ang)


def describe(poses, side: Fraction, dec: dict) -> dict:
    """Printed facts of an accepted (or refused) decision; decides nothing."""
    n = len(poses)
    pairs = geom.pair_index(n)
    margins = dec["a"]["margins"]
    order = sorted(range(len(margins)), key=lambda k: margins[k])
    least = [{"pair": [pairs[k][0] + 1, pairs[k][1] + 1], "margin": sci(margins[k], 8)} for k in order[:12]]
    below = {name: sum(1 for m in margins if m < t) for name, t in THRESHOLDS}
    distinct_near = len({margins[k] for k in order if margins[k] < Fraction(1, 1000)})
    clear = dec["a"]["clearances"]
    walls = {}
    for w, name in enumerate(("left", "bottom", "right", "top")):
        vals = [cl[w] for cl in clear]
        lo = min(vals)
        walls[name] = {
            "least": sci(lo, 8),
            "squares": [k + 1 for k, v in enumerate(vals) if v == lo][:20],
            "touching": [k + 1 for k, v in enumerate(vals) if v == 0],
        }
    w_far = min(min(cl[2], cl[3]) for cl in clear)
    e = [geom.half_extent(p) for p in poses]
    xs = [p[0] for p in poses]
    ys = [p[1] for p in poses]
    width = max(x + h for x, h in zip(xs, e, strict=True)) - min(x - h for x, h in zip(xs, e, strict=True))
    height = max(y + h for y, h in zip(ys, e, strict=True)) - min(y - h for y, h in zip(ys, e, strict=True))
    extent = max(width, height)
    ints = dec["a"]["ints"]
    close = 0
    for i in range(n):
        xi, yi, ei = ints[i][0], ints[i][1], ints[i][2]
        for j in range(i + 1, n):
            xj, yj, ej = ints[j][0], ints[j][1], ints[j][2]
            dx = xj * ei - xi * ej
            dy = yj * ei - yi * ej
            if dx * dx + dy * dy < 2 * (ei * ej) ** 2:
                close += 1
    upright = sum(1 for p in poses if p[2] == 0 or p[3] == 0)
    tilts = [tilt_degrees(p[2], p[3]) for p in poses]
    turned = [t for p, t in zip(poses, tilts, strict=True) if not (p[2] == 0 or p[3] == 0)]
    orients = {canonical_direction(p[2], p[3]) for p in poses if not (p[2] == 0 or p[3] == 0)}
    return {
        "least_margins": least,
        "least_margin_exact": frac_text(margins[order[0]]) if len(frac_text(margins[order[0]])) < 2000 else "long",
        "pairs_below": below,
        "pairs_zero": sum(1 for m in margins if m == 0),
        "pairs_negative": sum(1 for m in margins if m < 0),
        "distinct_margins_below_1e-3": distinct_near,
        "margins_sha256": margins_digest(margins),
        "walls": walls,
        "least_right_or_top_clearance": sci(w_far, 8),
        "least_right_or_top_clearance_exact": frac_text(w_far),
        "width_less_side": sci(side - width, 8),
        "height_less_side": sci(side - height, 8),
        "side_less_extent": sci(side - extent, 8),
        "side_less_extent_exact": frac_text(side - extent),
        "extent_30": floor_places(extent, 30),
        "close_pairs_below_sqrt2": close,
        "upright": upright,
        "turned_below_1deg": sum(1 for t in turned if t < 1.0),
        "turned_beyond_1deg": sum(1 for t in turned if t >= 1.0),
        "largest_tilt_deg": round(max(tilts), 4),
        "distinct_turned_orientations": len(orients),
    }


def check_report(raw_j: bytes, raw_c: bytes) -> dict:
    out: dict = {"kind": "report"}
    try:
        fj = rd.read_form_j(raw_j)
    except rd.ReadError as exc:
        return {**out, "verdict": "REFUSE", "reason": f"read: {exc}"}
    try:
        fc = rd.read_corners(raw_c, "square-k", "form C")
    except rd.ReadError as exc:
        return {**out, "verdict": "REFUSE", "reason": f"read: {exc}"}
    out["read"] = {
        "form_j": {"sha256": fj["sha256"], "scalars": fj["scalars"], "flags": fj["flags"][:20], "flag_count": len(fj["flags"])},
        "form_c": {"sha256": fc["sha256"], "scalars": fc["scalars"], "flags": fc["flags"][:20], "flag_count": len(fc["flags"]),
                   "witness_id": fc["witness_id"], "claim": fc["claim"], "blocks": fc["blocks"],
                   "envelope_schema": fc["envelope_schema"], "envelope_status": fc["envelope_status"]},
    }
    if fj["n"] != fc["n"]:
        return {**out, "verdict": "REFUSE", "reason": "the two files' counts differ"}
    if fj["side"] != fc["side"]:
        return {**out, "verdict": "REFUSE", "reason": "the two files' sides differ"}
    n, side = fj["n"], fj["side"]
    out["n"] = n
    out["side_exact"] = fj["side_text"]
    out["side_text_equal"] = fj["side_text"] == fc["side_text"]
    rows = fj["rows"]
    twins = [geom.twin_match(fc["squares"][k], rows[k]) for k in range(n)]
    twin_fail = [k + 1 for k, t in enumerate(twins) if t is None]
    listing = {}
    for t in twins:
        if t is not None:
            listing[f"offset {t[0]} {t[1]}"] = listing.get(f"offset {t[0]} {t[1]}", 0) + 1
    out["twin"] = {"fail": twin_fail, "listing": listing}
    t0 = time.process_time()
    dj = decide(rows, [geom.corners_of(p) for p in rows], side)
    c_poses = []
    c_unit = []
    for q in fc["squares"]:
        u, p = geom.pose_of_corners(q)
        c_unit.append(u)
        c_poses.append(p)
    dc = decide(c_poses, fc["squares"], side)
    same_margins = dj["a"]["margins"] == dc["a"]["margins"]
    same_clear = dj["a"]["clearances"] == dc["a"]["clearances"]
    same_b = [bp[0] for bp in dj["b"]["pairs"]] == [bp[0] for bp in dc["b"]["pairs"]]
    out["form_j"] = {"accept": dj["accept"], **summary(dj)}
    out["form_c"] = {"accept": dc["accept"], **summary(dc), "corner_sets_not_unit": [k + 1 for k, u in enumerate(c_unit) if not u]}
    out["crossed"] = {"margins_identical": same_margins, "clearances_identical": same_clear, "b_classes_identical": same_b}
    accept = (dj["accept"] and dc["accept"] and not twin_fail and same_margins and same_clear and same_b
              and all(c_unit) and out["side_text_equal"])
    out["verdict"] = "ACCEPT" if accept else "REFUSE"
    if accept:
        out["describe"] = describe(rows, side, dj)
    out["cpu_total"] = round(time.process_time() - t0, 2)
    out["_decisions"] = (dj, dc)
    return out


def check_house(raw: bytes) -> dict:
    out: dict = {"kind": "house"}
    try:
        fh = rd.read_corners(raw, "int", "house file")
    except rd.ReadError as exc:
        return {**out, "verdict": "REFUSE", "reason": f"read: {exc}"}
    out["read"] = {"sha256": fh["sha256"], "scalars": fh["scalars"], "flag_count": len(fh["flags"]), "flags": fh["flags"][:20],
                   "witness_id": fh["witness_id"], "blocks": fh["blocks"]}
    n, side = fh["n"], fh["side"]
    out["n"] = n
    out["side_exact"] = fh["side_text"]
    t0 = time.process_time()
    poses = []
    units = []
    for q in fh["squares"]:
        u, p = geom.pose_of_corners(q)
        units.append(u)
        poses.append(p)
    self_twin = [k + 1 for k in range(n) if geom.twin_match(fh["squares"][k], poses[k]) is None]
    dh = decide(poses, fh["squares"], side)
    out["house"] = {"accept": dh["accept"], **summary(dh), "corner_sets_not_unit": [k + 1 for k, u in enumerate(units) if not u],
                    "self_twin_fail": self_twin}
    accept = dh["accept"] and all(units) and not self_twin
    out["verdict"] = "ACCEPT" if accept else "REFUSE"
    if accept:
        out["describe"] = describe(poses, side, dh)
    out["cpu_total"] = round(time.process_time() - t0, 2)
    out["_decisions"] = (dh,)
    out["_poses"] = poses
    return out


def summary(d: dict) -> dict:
    def one(xs):
        return [list(x) if isinstance(x, tuple) else x for x in xs[:20]]

    return {
        "a_not_unit": one([k + 1 for k in d["a_not_unit"]]),
        "b_not_unit": one([k + 1 for k in d["b_not_unit"]]),
        "a_crossing": one([k + 1 for k in d["a_cross"]]),
        "b_crossing": one([k + 1 for k in d["b_cross"]]),
        "b_area_inside_not_1": one([k + 1 for k in d["area_short"]]),
        "a_overlaps": len(d["a_overlap"]),
        "b_overlaps": len(d["b_overlap"]),
        "first_overlaps": [[i + 1, j + 1] for i, j in d["a_overlap"][:10]],
        "pair_disagreements": len(d["pair_disagree"]),
        "wall_disagreements": len(d["wall_disagree"]),
        "unit_disagreements": len(d["unit_disagree"]),
        "a_pair_classes": {c: d["a_classes"].count(c) for c in ("apart", "contact", "overlap")},
        "b_pair_classes": {c: sum(1 for bp in d["b"]["pairs"] if bp[0] == c) for c in ("apart", "contact", "overlap")},
        "cpu": d["cpu"],
    }


def public(result: dict) -> dict:
    return {k: v for k, v in result.items() if not k.startswith("_")}


def main(argv: list[str]) -> int:
    if len(argv) == 5 and argv[0] == "report":
        _, label, fj, fc, out = argv
        with open(fj, "rb") as f1, open(fc, "rb") as f2:
            res = check_report(f1.read(), f2.read())
    elif len(argv) == 4 and argv[0] == "house":
        _, label, fh, out = argv
        with open(fh, "rb") as f:
            res = check_house(f.read())
    else:
        print(__doc__)
        return 2
    res = {"label": label, **public(res)}
    with open(out, "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print(label, res["verdict"], res.get("reason", ""), "cpu", res.get("cpu_total"))
    return 0 if res["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
