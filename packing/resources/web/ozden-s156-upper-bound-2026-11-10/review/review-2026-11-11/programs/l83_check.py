"""Decide a Witness/v2 corner certificate by two methods (review L83, clean room).

Usage: python -I -B l83_check.py CERT.yaml [TWIN.json] OUT.json

Every square, every wall and every pair, with no distance filter. Method A
(l83_sat, Fraction) and method B (l83_clip, gmpy2.mpq) share only the reader, which
hands them integers. The verdict is ACCEPT only when both methods find every square a
unit square inside the box and every pair with disjoint interiors, and their
three-way classes agree everywhere.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gmpy2 import mpq  # noqa: E402

import l83_clip as B  # noqa: E402
import l83_reader as R  # noqa: E402
import l83_sat as A  # noqa: E402

NEAR = Fraction(1, 10**12)
REPORT = Fraction(1, 10**9)
WALLS = ("left", "bottom", "right", "top")


def decide(n, side, ids, corners, pairs=None, squares=None):
    """Decide the listed squares (default all) and pairs (default all).

    corners: per square, four ((p, q), (p, q)). Returns a dict of results.
    """
    sideA = A.frac(side)
    sideB = mpq(side[0], side[1])
    idx = range(n) if squares is None else squares
    shapeA, shapeB = {}, {}
    sqA, ptsB, hpsB = {}, {}, {}
    need = set(idx)
    pair_list = list(combinations(range(n), 2)) if pairs is None else list(pairs)
    for i, j in pair_list:
        need.add(i)
        need.add(j)
    for i in sorted(need):
        try:
            sqA[i] = A.Square(A.points(corners[i]))
            shapeA[i] = sqA[i].sense
        except ValueError as exc:
            shapeA[i] = f"refused: {exc}"
        p = B.points(corners[i])
        ptsB[i] = p
        try:
            s = B.unit_square_sense(p)
            shapeB[i] = s
            hpsB[i] = B.halfplanes(p, s)
        except ValueError as exc:
            shapeB[i] = f"refused: {exc}"
    bad_shape = sorted(ids[i] for i in need if not (isinstance(shapeA[i], int) and isinstance(shapeB[i], int)))
    shape_disagree = sorted(ids[i] for i in need if isinstance(shapeA[i], int) != isinstance(shapeB[i], int))
    walls = {}
    wall_disagree = []
    outside = []
    contacts = []
    least_pos_wall = None
    for i in idx:
        clearA = A.wall_clearances(A.points(corners[i]), sideA)
        clsB = B.wall_classes(ptsB[i], sideB)
        area_in = B.box_area(ptsB[i], sideB)
        inside_B = area_in == 1 if isinstance(shapeB[i], int) else None
        rec = {}
        for w in WALLS:
            ca = A.classify(clearA[w])
            cb = {"clear": "clear", "contact": "contact", "overlap": "overlap"}[clsB[w]]
            if ca != cb:
                wall_disagree.append((ids[i], w, ca, cb))
            rec[w] = clearA[w]
            if clearA[w] == 0:
                contacts.append((ids[i], w))
            elif clearA[w] > 0 and (least_pos_wall is None or clearA[w] < least_pos_wall[0]):
                least_pos_wall = (clearA[w], ids[i], w)
        insideA = all(rec[w] >= 0 for w in WALLS)
        if not insideA or inside_B is False:
            outside.append(ids[i])
        if inside_B is not None and inside_B != insideA:
            wall_disagree.append((ids[i], "box", insideA, inside_B))
        walls[i] = rec
    overlaps, touching, pair_disagree = [], [], []
    margins = {}
    least = None
    total_area = mpq(0)
    near = []
    for i, j in pair_list:
        if i not in sqA or j not in sqA or i not in hpsB or j not in hpsB:
            continue
        m = A.pair_margin(sqA[i], sqA[j])
        ca = A.classify(m)
        cb, ar = B.pair_class(ptsB[i], hpsB[j])
        total_area += ar
        if ca != cb:
            pair_disagree.append((ids[i], ids[j], ca, cb))
        if ca == "overlap" or cb == "overlap":
            overlaps.append((ids[i], ids[j]))
        elif ca == "contact" or cb == "contact":
            touching.append((ids[i], ids[j]))
        margins[(i, j)] = m
        if least is None or m < least[0]:
            least = (m, ids[i], ids[j])
        if m < REPORT:
            near.append((ids[i], ids[j], m))
    accept = not bad_shape and not outside and not overlaps and not pair_disagree and not wall_disagree and not shape_disagree
    return {
        "accept": accept,
        "bad_shape": bad_shape,
        "shape_disagree": shape_disagree,
        "outside": sorted(outside),
        "overlaps": sorted(overlaps),
        "touching": sorted(touching),
        "pair_disagree": pair_disagree,
        "wall_disagree": wall_disagree,
        "contacts": sorted(contacts),
        "least_pos_wall": least_pos_wall,
        "least_pair": least,
        "near": near,
        "walls": walls,
        "margins": margins,
        "senses": {ids[i]: shapeA[i] for i in need},
        "pairs_decided": len(margins),
        "squares_decided": len(list(idx)),
        "total_area": total_area,
    }


def summary(res, side) -> dict:
    lp = res["least_pair"]
    lw = res["least_pos_wall"]
    near12 = [x for x in res["near"] if x[2] < NEAR]
    senses = list(res["senses"].values())
    return {
        "verdict": "ACCEPT" if res["accept"] else "REFUSE",
        "squares_decided": res["squares_decided"],
        "pairs_decided": res["pairs_decided"],
        "bad_shape": res["bad_shape"],
        "shape_disagree": res["shape_disagree"],
        "outside": res["outside"],
        "overlapping_pairs": res["overlaps"],
        "touching_pairs": res["touching"],
        "pair_class_disagreements": res["pair_disagree"],
        "wall_class_disagreements": [list(map(str, x)) for x in res["wall_disagree"]],
        "wall_contacts": res["contacts"],
        "sum_of_clipped_pair_areas": str(res["total_area"]),
        "least_positive_wall_clearance": None if lw is None else {"exact": str(lw[0]), "float": float(lw[0]), "id": lw[1], "wall": lw[2]},
        "least_pair_margin": None if lp is None else {"exact": str(lp[0]), "float": float(lp[0]), "ids": [lp[1], lp[2]]},
        "pairs_below_1e-12": len(near12),
        "pairs_below_1e-9": len(res["near"]),
        "near_pairs_below_1e-9": [[a, b, float(m)] for a, b, m in res["near"]],
        "counterclockwise": sum(1 for s in senses if s == 1),
        "clockwise": sum(1 for s in senses if s == -1),
        "side": f"{side[0]}/{side[1]}",
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def program_digests() -> dict:
    here = Path(__file__).resolve().parent
    return {p.name: sha256(p) for p in sorted(here.glob("l83_*.py"))}


def main(argv: list[str]) -> int:
    cert = Path(argv[1])
    twin = Path(argv[2]) if len(argv) == 4 else None
    out = Path(argv[-1])
    t0 = time.process_time()
    try:
        rd = R.read_files(cert, twin)
    except R.Refused as exc:
        out.write_text(json.dumps({"verdict": "REFUSE", "reader": str(exc)}, indent=1) + "\n")
        print("REFUSE (reader):", exc)
        return 1
    w = rd.witness
    res = decide(w.n, w.side, w.ids, w.corners)
    s = summary(res, w.side)
    s.update(
        {
            "file": cert.name,
            "sha256": rd.yaml_sha256,
            "bytes": rd.yaml_bytes,
            "yaml_ends_newline": rd.yaml_ends_newline,
            "json_twin": None if twin is None else {"file": twin.name, "sha256": rd.json_sha256, "equal": rd.json_equal, "ends_newline": rd.json_ends_newline},
            "n": w.n,
            "ids_in_order": w.ids_in_order,
            "scalars_read": w.scalar_count,
            "meta": w.meta,
            "far_wall_clearances_below_1e-9": sorted(
                [[w.ids[i], wall, float(v)] for i, rec in res["walls"].items() for wall, v in rec.items() if 0 < v < REPORT],
                key=lambda x: x[2],
            ),
            "cpu_seconds": round(time.process_time() - t0, 1),
            "programs": program_digests(),
        }
    )
    out.write_text(json.dumps(s, indent=1, ensure_ascii=False) + "\n")
    print(s["verdict"], w.n, "pairs", s["pairs_decided"], "least", s["least_pair_margin"], "contacts", s["wall_contacts"], "cpu", s["cpu_seconds"])
    return 0 if s["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
