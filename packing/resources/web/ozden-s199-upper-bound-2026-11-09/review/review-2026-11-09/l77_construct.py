"""Measure the #938 construction exactly against T-282's witness; decides nothing.

- squares 1-172 against the retained #935 corner file and against main's center-basis
  witness n-172.yaml (T-282), corner set for corner set;
- the side against S172 + 1;
- the 27 grid squares: unit, axis-aligned, inside the L region, row and column layout;
- the 172 part against its own box [0, S172]^2, and every gap between an old square and a
  grid square, by method A's margin and method B's class.

Run: python -I -B l77_construct.py CANDIDATE.yaml RETAINED_172.yaml MAIN_172.yaml OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from fractions import Fraction as F

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l77_checker as C  # noqa: E402


def sha(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def fq(t: tuple[int, int]) -> F:
    return F(t[0], t[1])


def read_center_basis(path: str) -> tuple[F, list[tuple[int, tuple[F, F], tuple[F, F]]]]:
    """Main's n-172.yaml: center-basis, rational. Its certificate block holds booleans, so
    it is loaded whole and each geometric scalar goes through the strict rational rule."""
    doc = yaml.safe_load(open(path).read())

    def s(v: object) -> str:
        return v if isinstance(v, str) else str(v)

    w = doc["witness"]
    w = {**w, "side": s(w["side"]), "n": s(w["n"]), "square_size": s(w["square_size"]),
         "squares": [{"id": s(e["id"]), "center": [s(v) for v in e["center"]],
                      "basis": [s(v) for v in e["basis"]]} for e in w["squares"]]}
    assert w["representation"] == "center-basis" and w["scalar"] == {"kind": "rational"}
    assert w["coordinates"]["origin"] == "lower-left" and w["square_size"] == "1"
    side = fq(C.parse_scalar(w["side"]))
    out = []
    for e in w["squares"]:
        c = (fq(C.parse_scalar(e["center"][0])), fq(C.parse_scalar(e["center"][1])))
        b = (fq(C.parse_scalar(e["basis"][0])), fq(C.parse_scalar(e["basis"][1])))
        out.append((int(e["id"]), c, b))
    assert int(w["n"]) == len(out)
    return side, out


def corner_set(cs: list) -> set[tuple[F, F]]:
    return {(fq(x), fq(y)) for x, y in cs}


def main() -> int:
    cand, ret172, main172, out = sys.argv[1:5]
    w = C.read_witness(cand)
    r = C.read_witness(ret172)
    side199 = fq(w["side"])
    side_ret = fq(r["side"])
    side_main, cb = read_center_basis(main172)
    res: dict = {
        "program": "l77_construct.py",
        "program_sha256": sha(__file__),
        "checker_sha256": sha(os.path.join(HERE, "l77_checker.py")),
        "inputs": {
            "candidate": {"file": os.path.basename(cand), "sha256": w["sha256"]},
            "retained_172": {"file": "resources/web/ozden-s172-upper-bound-2026-11-09/source/n-172-candidate.yaml",
                             "sha256": r["sha256"]},
            "main_172": {"file": "witnesses/known-best/n-172.yaml", "sha256": sha(main172)},
        },
    }
    S = side_main
    # --- squares 1-172
    same_ret = all(w["corners"][i] == r["corners"][i] for i in range(172)) and w["ids"][:172] == r["ids"]
    mism_main = []
    for i, (sid, c, b) in enumerate(cb):
        cs = w["corners"][i]
        sq = C.SquareA(cs)
        cen = ((sq.pts[0][0] + sq.pts[2][0]) / 2, (sq.pts[0][1] + sq.pts[2][1]) / 2)
        bx, by = b
        mc = {
            (c[0] + (sx * bx - sy * by) / 2, c[1] + (sx * by + sy * bx) / 2)
            for sx in (-1, 1)
            for sy in (-1, 1)
        }
        if sid != w["ids"][i] or cen != c or mc != corner_set(cs) or bx * bx + by * by != 1:
            mism_main.append(sid)
    res["squares_1_172"] = {
        "equal_to_retained_935_corner_file": same_ret,
        "retained_side_equals_main_side": side_ret == side_main,
        "ids_equal_main": [x[0] for x in cb] == w["ids"][:172],
        "corner_sets_equal_main_center_basis": not mism_main,
        "mismatches_against_main": mism_main,
    }
    # --- side
    res["side"] = {
        "side_equals_S172_plus_1": side199 == S + 1,
        "S172": C.q_str(S),
        "S172_float": float(S),
        "floor_S172": S.numerator // S.denominator,
        "side_lowest_terms_denominator_equals_S172s": side199.denominator == S.denominator,
        "count_2floor_plus_1": 2 * (S.numerator // S.denominator) + 1,
    }
    # --- the 172 part in its own box
    old = [C.SquareA(cs) for cs in w["corners"][:172]]
    walls_old = []
    for i, sq in enumerate(old):
        wl = C.walls_a(sq, S)
        for name, v in wl.items():
            walls_old.append((v, i + 1, name))
    neg = [x for x in walls_old if x[0] < 0]
    res["old_part_in_old_box"] = {
        "inside": not neg,
        "contacts": sorted([[i, nm] for v, i, nm in walls_old if v == 0]),
        "right_clearances_lowest": [[i, float(v)] for v, i, nm in sorted(x for x in walls_old if x[2] == "right")[:5]],
        "top_clearances_lowest": [[i, float(v)] for v, i, nm in sorted(x for x in walls_old if x[2] == "top")[:5]],
        "max_x": float(max(max(p[0] for p in sq.pts) for sq in old)),
        "max_y_short_of_S172": float(S - max(max(p[1] for p in sq.pts) for sq in old)),
    }
    # the far-right square's extreme corner
    far = []
    for i, sq in enumerate(old):
        for p in sq.pts:
            if S - p[0] < F(1, 10**9):
                far.append({"square": i + 1, "x_short_of_S172": float(S - p[0]), "y": float(p[1])})
    res["old_corners_within_1e-9_of_x_S172"] = far
    far_top = []
    for i, sq in enumerate(old):
        for p in sq.pts:
            if S - p[1] < F(1, 10**9):
                far_top.append({"square": i + 1, "y_short_of_S172": float(S - p[1]), "x": float(p[0])})
    res["old_corners_within_1e-9_of_y_S172"] = far_top
    # --- the grid squares
    grid = []
    row, col, other = [], [], []
    for k in range(172, 199):
        sq = C.SquareA(w["corners"][k])
        xs = sorted({p[0] for p in sq.pts})
        ys = sorted({p[1] for p in sq.pts})
        axis = len(xs) == 2 and len(ys) == 2
        in_v = all(S <= p[0] <= S + 1 and 0 <= p[1] <= S + 1 for p in sq.pts)
        in_h = all(0 <= p[0] <= S + 1 and S <= p[1] <= S + 1 for p in sq.pts)
        entry = {"id": k + 1, "axis_aligned": axis, "x": [C.q_str(v) if v.denominator != 1 else int(v) for v in xs],
                 "y": [C.q_str(v) if v.denominator != 1 else int(v) for v in ys],
                 "in_vertical_arm": in_v, "in_horizontal_arm": in_h}
        grid.append(entry)
        if axis and ys == [S, S + 1] and xs[0].denominator == 1 and xs[1] == xs[0] + 1:
            row.append((int(xs[0]), k + 1))
        elif axis and xs == [S, S + 1] and ys[0].denominator == 1 and ys[1] == ys[0] + 1:
            col.append((int(ys[0]), k + 1))
        else:
            other.append(k + 1)
    row.sort()
    col.sort()
    res["grid"] = {
        "count": len(grid),
        "row_top": {"ids": [i for _, i in row], "x_starts": [x for x, _ in row]},
        "column_right": {"ids": [i for _, i in col], "y_starts": [y for y, _ in col]},
        "neither": other,
        "row_is_0_to_13": [x for x, _ in row] == list(range(14)),
        "column_is_0_to_12": [y for y, _ in col] == list(range(13)),
        "all_in_L": all(g["in_vertical_arm"] or g["in_horizontal_arm"] for g in grid),
        "corner_cell_taken_by": [i for x, i in row if x + 1 > S],
        "slack_row_end": float(S + 1 - 14),
        "slack_column_top": float(S - 13),
        "L_area": float(2 * S + 1),
        "L_area_minus_27": float(2 * S + 1 - 27),
    }
    # --- old-grid gaps
    gsq_a = [C.SquareA(w["corners"][k]) for k in range(172, 199)]
    gsq_b = [C.SquareB(w["corners"][k]) for k in range(172, 199)]
    old_b = [C.SquareB(cs) for cs in w["corners"][:172]]
    per_grid = []
    pairs_near = []
    classes = {"clear": 0, "contact": 0, "overlap": 0}
    all_gaps = []
    for g in range(27):
        best = None
        for i in range(172):
            m, ax = C.margin_a(old[i], gsq_a[g])
            cls, _ = C.pair_b(old_b[i], gsq_b[g])
            classes[cls] += 1
            all_gaps.append((m, i + 1, 173 + g))
            if best is None or m < best[0]:
                best = (m, i + 1, ax)
            if m < F(1, 10**12):
                pairs_near.append([i + 1, 173 + g, float(m)])
        per_grid.append({"grid": 173 + g, "nearest_old": best[1], "gap": C.q_str(best[0]),
                         "gap_float": float(best[0]), "axis": ["old u", "old perp", "grid u", "grid perp"][best[2]]})
    all_gaps.sort()
    res["old_grid_pairs"] = {
        "pairs": 172 * 27,
        "method_B_classes": classes,
        "least_gap": {"pair": [all_gaps[0][1], all_gaps[0][2]], "value": C.q_str(all_gaps[0][0]),
                      "float": float(all_gaps[0][0])},
        "below_1e-12": len(pairs_near),
        "below_1e-12_list": sorted(pairs_near, key=lambda x: x[2]),
        "lowest_10": [[a, b, float(m)] for m, a, b in all_gaps[:10]],
        "per_grid_square": per_grid,
    }
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: res[k] for k in ("squares_1_172", "side")}, indent=1))
    print(json.dumps(res["grid"], indent=1)[:1500])
    print(json.dumps({k: v for k, v in res["old_grid_pairs"].items() if k not in ("per_grid_square",)}, indent=1)[:3000])
    print(json.dumps(res["old_part_in_old_box"], indent=1))
    print(json.dumps(res["old_corners_within_1e-9_of_x_S172"]), json.dumps(res["old_corners_within_1e-9_of_y_S172"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
