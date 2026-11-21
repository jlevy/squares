"""Lane rR2 (issue 1042 derived bounds), check C2: repeated central strips and corners.

Decides, exactly, for each anchor of the strip claims (188, 189, 218, and 137 at d = -1)
and for the corner-modified anchor of 217:

- D1, the period relations of the symmetrized density on the centred band of p unit
  strips, on both axes, by comparing signed corner weights of the clipped images;
- D3, the masses M, b_x, b_y, c and M(d) = M + d (b_x + b_y) + d^2 c, against n and the
  source's stated values;
- D7/D8 for 217: which primitives change, where they lie, that the band misses the corner
  squares, and the source's old, removed and new masses.

Usage:
  python -I rr2_strips.py --source DIR [--out FILE] [--controls]
where DIR is the source folder lower_bounds_2026_11_19. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rr2_measure import GRID, Measure, read_json, to_grid  # noqa: E402


def corner_weights(images, wx0, wy0, wx1, wy1, sx, sy):
    """Signed corner weights of images clipped to [wx0,wx1) x [wy0,wy1), moved by (-sx,-sy)."""
    w: dict[tuple[int, int], F] = defaultdict(F)
    for a, b, c, d, dens in images:
        x0 = a if a > wx0 else wx0
        x1 = c if c < wx1 else wx1
        if x0 >= x1:
            continue
        y0 = b if b > wy0 else wy0
        y1 = d if d < wy1 else wy1
        if y0 >= y1:
            continue
        x0 -= sx
        x1 -= sx
        y0 -= sy
        y1 -= sy
        w[(x0, y0)] += dens
        w[(x1, y0)] -= dens
        w[(x0, y1)] -= dens
        w[(x1, y1)] += dens
    return {k: v for k, v in w.items() if v != 0}


def window_mass(images, wx0, wy0, wx1, wy1) -> F:
    total = F(0)
    for a, b, c, d, dens in images:
        x0 = max(a, wx0)
        x1 = min(c, wx1)
        if x0 >= x1:
            continue
        y0 = max(b, wy0)
        y1 = min(d, wy1)
        if y0 >= y1:
            continue
        total += dens * (x1 - x0) * (y1 - y0)
    return total / (GRID * GRID)


def band_start(S: int, p: int) -> int:
    twice = S - p * GRID
    if twice % 2:
        raise ValueError("band start is off the grid")
    return twice // 2


def periodic(images, S: int, p: int) -> dict:
    """D1 on the centred band of p strips: every strip equals the first, on both axes."""
    a = band_start(S, p)
    if a < 0:
        return {"p": p, "holds": False, "reason": "band wider than the board"}
    out = {"p": p, "band": [str(F(a, GRID)), str(F(a + p * GRID, GRID))], "holds": True}
    for axis in ("x", "y"):
        ref = None
        mismatches = []
        for j in range(p):
            lo = a + j * GRID
            if axis == "x":
                w = corner_weights(images, lo, 0, lo + GRID, S, j * GRID, 0)
            else:
                w = corner_weights(images, 0, lo, S, lo + GRID, 0, j * GRID)
            if ref is None:
                ref = w
                out[f"corners_{axis}"] = len(w)
                continue
            if w != ref:
                keys = set(w) | set(ref)
                diff = [k for k in keys if w.get(k, F(0)) != ref.get(k, F(0))]
                mismatches.append({"strip": j, "differing_corners": len(diff)})
        out[f"mismatches_{axis}"] = mismatches
        if mismatches:
            out["holds"] = False
    return out


def strip_masses(images, S: int, p: int) -> dict:
    a = band_start(S, p)
    bx = [window_mass(images, a + j * GRID, 0, a + (j + 1) * GRID, S) for j in range(p)]
    by = [window_mass(images, 0, a + j * GRID, S, a + (j + 1) * GRID) for j in range(p)]
    cells = [
        window_mass(images, a + i * GRID, a + j * GRID, a + (i + 1) * GRID, a + (j + 1) * GRID)
        for i in range(p)
        for j in range(p)
    ]
    return {
        "bx": bx[0],
        "by": by[0],
        "c": cells[0],
        "bx_all_equal": all(v == bx[0] for v in bx),
        "by_all_equal": all(v == by[0] for v in by),
        "cells_all_equal": all(v == cells[0] for v in cells),
    }


def widest_band(images, S: int, start: int) -> int:
    p = start
    while p + 1 <= S // GRID and periodic(images, S, p + 1)["holds"]:
        p += 1
    return p


def frac(v: F) -> dict:
    return {"exact": str(v), "approx": float(v)}


def strip_claim(n: int, d: int, p: int, side: F, S: F, M: F, bx: F, by: F, c: F,
                stated_mass: F | None, stated_side: F) -> dict:
    Md = M + d * (bx + by) + d * d * c
    checks = {
        "p_at_least_3": p >= 3,
        "p_plus_d_at_least_2": p + d >= 2,
        "side_is_S_plus_d": stated_side == S + d,
        "mass_below_n": Md < n,
    }
    return {
        "n": n,
        "d": d,
        "side": str(stated_side),
        "mass": frac(Md),
        "slack": frac(n - Md),
        "equals_stated_mass": (stated_mass == Md) if stated_mass is not None else None,
        "checks": checks,
        "decided": all(checks.values()),
    }


def anchor_report(measure: Measure, p: int, family: dict | None) -> dict:
    imgs = measure.images()
    per = periodic(imgs, measure.S, p)
    sm = strip_masses(imgs, measure.S, p)
    M = measure.total()
    rep = {
        "side": str(measure.side),
        "primitives": len(measure.prims),
        "images": len(imgs),
        "M": frac(M),
        "bx": frac(sm["bx"]),
        "by": frac(sm["by"]),
        "c": frac(sm["c"]),
        "bx_equals_by": sm["bx"] == sm["by"],
        "strip_and_cell_masses_equal": sm["bx_all_equal"] and sm["by_all_equal"]
        and sm["cells_all_equal"],
        "periodic": per,
        "widest_centred_periodic_band": widest_band(imgs, measure.S, p) if per["holds"] else None,
    }
    if family is not None:
        rep["family_matches"] = {
            "base_mass": F(family["base_mass"]) == M,
            "strip_mass": F(family["strip_mass"]) == sm["bx"],
            "cell_mass": F(family["cell_mass"]) == sm["c"],
            "side": F(family["side"]) == measure.side,
        }
    rep["_values"] = (M, sm["bx"], sm["by"], sm["c"])
    return rep


def check_levels_identical(proof_dir: Path) -> dict:
    """The measure levels kNNN.json.gz must carry the same primitives."""
    levels = sorted(proof_dir.glob("k*.json.gz"))
    rects = [read_json(f)["rectangles"] for f in levels]
    return {
        "levels": [f.name for f in levels],
        "same_primitives": all(r == rects[0] for r in rects),
    }


def run_strips(src: Path) -> dict:
    claims = json.loads((src / "followup/repeated/claims.json").read_text())
    by_folder: dict[str, list] = defaultdict(list)
    for cl in claims:
        by_folder[cl["folder"]].append(cl)
    out = {}
    for folder, cls in sorted(by_folder.items()):
        base = src / "followup/repeated" / folder
        family = json.loads((base / "family.json").read_text())
        measure = Measure.from_file(base / "proof/k100.json.gz")
        p = int(family["periods"])
        rep = anchor_report(measure, p, family)
        M, bx, by, c = rep.pop("_values")
        rep["levels"] = check_levels_identical(base / "proof")
        rep["claims"] = []
        for cl in cls:
            fam_cl = next((x for x in family["claims"] if x["n"] == cl["n"]), None)
            res = strip_claim(cl["n"], cl["offset"], p, F(cl["side"]), measure.side, M, bx, by,
                              c, F(cl["mass"]), F(cl["side"]))
            res["anchor_side_matches"] = F(cl["anchor_side"]) == measure.side
            res["family_claim_matches"] = fam_cl is not None and F(fam_cl["mass"]) == F(cl["mass"])
            rep["claims"].append(res)
        out[folder] = rep
    return out


def corner_modified(src: Path, folder: str):
    base = src / "followup/corner_trim" / folder
    claim = json.loads((base / "claim.json").read_text())
    mult = json.loads((base / "multipliers.json").read_text())
    anchor = Measure.from_file(base / "proof/k100.json.gz")
    return base, claim, mult, anchor


def run_corner(src: Path, mult_override: dict | None = None) -> dict:
    claims = json.loads((src / "followup/corner_trim/claims.json").read_text())
    out = {}
    for cl in claims:
        base, claim, mult, anchor = corner_modified(src, cl["folder"])
        if mult_override is not None:
            mult = mult_override
        S = anchor.S
        C = to_grid(F(claim["corner"]), "corner")
        phi = F(claim["factor"])
        p = int(claim["periods"])
        d = int(claim["offset"])
        a = band_start(S, p)
        new_masses = {}
        placement = {"inside_corner_square": 0, "outside": []}
        negative = []
        for key, value in mult.items():
            k = int(key)
            mu = F(value)
            if mu < 0:
                negative.append(k)
            x0, y0, x1, y1, m = anchor.prims[k]
            if 0 <= x0 and x1 <= C and 0 <= y0 and y1 <= C:
                placement["inside_corner_square"] += 1
            else:
                placement["outside"].append(k)
            new_masses[k] = m * mu * phi
        rep = {
            "folder": cl["folder"],
            "anchor_side": str(anchor.side),
            "corner": str(F(C, GRID)),
            "factor": frac(phi),
            "multipliers": len(mult),
            "placement": placement,
            "negative_multipliers": negative,
            "band_misses_corner_squares": C <= a and S - C >= a + p * GRID,
        }
        if negative:
            rep["decided"] = False
            out[cl["folder"]] = rep
            continue
        modified = anchor.with_masses(new_masses)
        base_rep = anchor_report(anchor, p, None)
        M0, bx0, by0, c0 = base_rep.pop("_values")
        mod_rep = anchor_report(modified, p, None)
        M1, bx1, by1, c1 = mod_rep.pop("_values")
        removed = M0 - M1
        old_ext = M0 + d * (bx0 + by0) + d * d * c0
        new_ext = M1 + d * (bx1 + by1) + d * d * c1
        res = strip_claim(cl["n"], d, p, F(cl["side"]), anchor.side, M1, bx1, by1, c1,
                          F(cl["mass"]), F(cl["side"]))
        rep.update({
            "anchor": base_rep,
            "modified": mod_rep,
            "levels": check_levels_identical(base / "proof"),
            "band_unchanged": (bx0, by0, c0) == (bx1, by1, c1),
            "removed_mass": frac(removed),
            "removed_matches": removed == F(claim["removed_mass"]),
            "old_mass_matches": old_ext == F(claim["old_mass"]),
            "new_mass_matches": new_ext == F(claim["new_mass"]),
            "removed_without_factor": frac(
                sum((anchor.prims[int(k)][4] * (1 - F(v)) for k, v in mult.items()), F(0))
            ),
            "claim": res,
        })
        checks = {
            "all_modified_inside_corner_square": not placement["outside"],
            "band_misses_corner_squares": rep["band_misses_corner_squares"],
            "modified_periodic": mod_rep["periodic"]["holds"],
            "band_unchanged": rep["band_unchanged"],
            "strip_claim": res["decided"],
        }
        rep["checks"] = checks
        rep["decided"] = all(checks.values())
        out[cl["folder"]] = rep
    return out


def controls(src: Path) -> dict:
    """Mutations stated in the plan; each must be refused."""
    res = {}
    folder = "162--719881-12.881-100-uniform_finish"
    base = src / "followup/repeated" / folder
    family = json.loads((base / "family.json").read_text())
    measure = Measure.from_file(base / "proof/k100.json.gz")
    p = int(family["periods"])
    a = band_start(measure.S, p)
    # a primitive lying strictly inside the band's first strip in x
    pick = next(
        k for k, (x0, y0, x1, y1, m) in enumerate(measure.prims)
        if m > 0 and a < x0 and x1 < a + GRID
    )
    x0, y0, x1, y1, m = measure.prims[pick]
    moved = list(measure.prims)
    moved[pick] = (x0 + 1, y0, x1 + 1, y1, m)
    per = periodic(Measure(measure.side, moved, measure.n).images(), measure.S, p)
    res["band_primitive_moved_1e-8"] = {"primitive": pick, "refused": not per["holds"]}
    heavier = measure.with_masses({pick: m * (1 + F(1, 10**12))})
    per = periodic(heavier.images(), measure.S, p)
    res["band_primitive_mass_times_1+1e-12"] = {"primitive": pick, "refused": not per["holds"]}
    imgs = measure.images()
    widest = widest_band(imgs, measure.S, p)
    per = periodic(imgs, measure.S, widest + 1)
    res["p_one_above_widest"] = {"p": widest + 1, "refused": not per["holds"]}
    sm = strip_masses(imgs, measure.S, p)
    M = measure.total()
    cl = strip_claim(188, 1, p, measure.side + 1, measure.side, M, sm["bx"], sm["by"], sm["c"],
                     None, measure.side + 1)
    res["n_minus_1_at_189"] = {"refused": not cl["decided"]}
    corner_claims = json.loads((src / "followup/corner_trim/claims.json").read_text())
    _, claim, mult, anchor = corner_modified(src, corner_claims[0]["folder"])
    C = to_grid(F(claim["corner"]), "corner")
    outside = next(
        k for k, (x0, y0, x1, y1, m) in enumerate(anchor.prims)
        if m > 0 and str(k) not in mult and not (x1 <= C and y1 <= C)
    )
    bad = dict(mult)
    bad[str(outside)] = "1/2"
    rep = run_corner(src, mult_override=bad)
    res["corner_multiplier_outside_corner_square"] = {
        "primitive": outside,
        "refused": not next(iter(rep.values()))["decided"],
    }
    bad = dict(mult)
    first = next(iter(bad))
    bad[first] = "-1/1000"
    rep = run_corner(src, mult_override=bad)
    res["corner_negative_multiplier"] = {
        "primitive": int(first),
        "refused": not next(iter(rep.values()))["decided"],
    }
    res["all_refused"] = all(v["refused"] for v in res.values() if isinstance(v, dict))
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--controls", action="store_true")
    args = ap.parse_args()
    report: dict = {"program": "rr2_strips.py"}
    report["strips"] = run_strips(args.source)
    report["corner"] = run_corner(args.source)
    decided = all(c["decided"] for r in report["strips"].values() for c in r["claims"])
    decided = decided and all(r["periodic"]["holds"] for r in report["strips"].values())
    decided = decided and all(r["decided"] for r in report["corner"].values())
    report["verdict"] = "STRIP_AND_CORNER_CLAIMS_DECIDED" if decided else "NOT_DECIDED"
    if args.controls:
        report["controls"] = controls(args.source)
        report["controls_verdict"] = (
            "ALL_CONTROLS_REFUSED" if report["controls"]["all_refused"] else "CONTROL_ACCEPTED"
        )
    text = json.dumps(report, indent=1, default=str)
    if args.out:
        args.out.write_text(text + "\n")
    print(report["verdict"], report.get("controls_verdict", ""))
    return 0 if decided else 1


if __name__ == "__main__":
    raise SystemExit(main())
