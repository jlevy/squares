"""Lineage measurements for the L70 review: each certificate against its predecessor.

A measurement, which decides nothing.

* binary64, pose by pose, in box-centred coordinates, under all eight symmetries of
  the box applied to the newer packing: nearest-centre pairing (one to one or not),
  SciPy's optimal assignment of least summed squared move, and under the best
  symmetry the moves, turns (modulo 90 degrees), tilt counts and kept ids;
* exact, where the pairing is the identity and the predecessor is retained: each
  square's displacement and orientation change in rationals, in the lower-left frame,
  and whether the change is one common translation.

Usage: python -I l70_identity.py --src SRC --repo REPO --checks OUTDIR --out identity.json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402
import l70_reader as R  # noqa: E402

WEB = "packing/resources/web"
BH = (553, 599, 600, 601, 602, 604, 645, 647, 648, 699, 700)
SYMS = {
    "identity": ((1, 0), (0, 1)),
    "mirror x": ((-1, 0), (0, 1)),
    "mirror y": ((1, 0), (0, -1)),
    "rotate 180": ((-1, 0), (0, -1)),
    "transpose": ((0, 1), (1, 0)),
    "rotate 90": ((0, -1), (1, 0)),
    "rotate 270": ((0, 1), (-1, 0)),
    "anti-transpose": ((0, -1), (-1, 0)),
}


def exact_poses(pk: R.Packing) -> list[tuple[F, F, F, F]]:
    """(cx, cy, ux, uy) exact, lower-left frame."""
    out = []
    if pk.kind == "cert":
        for xn, xd, yn, yd, tn, td in pk.squares:
            t = F(tn, td)
            d = 1 + t * t
            out.append((F(xn, xd), F(yn, yd), (1 - t * t) / d, 2 * t / d))
    else:
        for row in pk.squares:
            p = [(F(row[4 * k], row[4 * k + 1]), F(row[4 * k + 2], row[4 * k + 3])) for k in range(4)]
            out.append(((p[0][0] + p[2][0]) / 2, (p[0][1] + p[2][1]) / 2, p[1][0] - p[0][0], p[1][1] - p[0][1]))
    return out


def reduce90(a: np.ndarray) -> np.ndarray:
    """Angles modulo 90 degrees into (-45, 45] degrees (radians in, radians out)."""
    q = math.pi / 2
    r = np.mod(a + math.pi / 4, q) - math.pi / 4
    return r


def float_poses(ex: list[tuple[F, F, F, F]], side: F) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    s = float(side)
    xy = np.array([[float(cx) - s / 2, float(cy) - s / 2] for cx, cy, _ux, _uy in ex])
    u = np.array([[float(ux), float(uy)] for _cx, _cy, ux, uy in ex])
    return xy, u, reduce90(np.arctan2(u[:, 1], u[:, 0]))


def exactly_upright(ex: list[tuple[F, F, F, F]]) -> int:
    return sum(1 for _cx, _cy, ux, uy in ex if ux == 0 or uy == 0)


def compare(new_ex: list[tuple[F, F, F, F]], new_side: F, old_ex: list[tuple[F, F, F, F]], old_side: F) -> dict[str, Any]:
    nxy, nu, _ = float_poses(new_ex, new_side)
    oxy, _ou, oang = float_poses(old_ex, old_side)
    per_sym = {}
    best = None
    for name, ((a, b), (c, d)) in SYMS.items():
        m = np.array([[a, b], [c, d]], dtype=float)
        txy = nxy @ m.T
        tu = nu @ m.T
        tang = reduce90(np.arctan2(tu[:, 1], tu[:, 0]))
        d2 = ((txy[:, None, :] - oxy[None, :, :]) ** 2).sum(axis=2)
        nearest = d2.argmin(axis=1)
        distinct = len(set(nearest.tolist()))
        rows, cols = linear_sum_assignment(d2)
        cost = float(d2[rows, cols].sum())
        per_sym[name] = {"nearest_distinct": distinct, "assignment_cost": cost}
        if best is None or cost < best[1]:
            best = (name, cost, txy, tang, cols, nearest)
    assert best is not None
    name, cost, txy, tang, cols, nearest = best
    mv = np.sqrt(((txy - oxy[cols]) ** 2).sum(axis=1))
    turn = np.abs(reduce90(tang - oang[cols]))
    deg = math.pi / 180
    n = len(new_ex)
    out = {
        "best_symmetry": name,
        "per_symmetry": per_sym,
        "nearest_one_to_one": len(set(nearest.tolist())) == n,
        "nearest_distinct": len(set(nearest.tolist())),
        "assignment_is_identity": bool((cols == np.arange(n)).all()),
        "same_id": int((cols == np.arange(n)).sum()),
        "moved_beyond": {k: int((mv > v).sum()) for k, v in (("1e-9", 1e-9), ("1e-6", 1e-6), ("1e-3", 1e-3), ("1e-2", 1e-2), ("0.05", 0.05), ("0.1", 0.1))},
        "within_0.05": int((mv <= 0.05).sum()),
        "largest_move": float(mv.max()),
        "largest_move_square": int(mv.argmax()) + 1,
        "turned_beyond": {k: int((turn > v).sum()) for k, v in (("1e-9 rad", 1e-9), ("1e-6 rad", 1e-6), ("0.5 deg", 0.5 * deg), ("1 deg", 1 * deg))},
        "largest_turn_deg": float(turn.max() / deg),
        "largest_turn_square": int(turn.argmax()) + 1,
        "tilted_new": {k: int((np.abs(tang) > v).sum()) for k, v in (("1e-9 rad", 1e-9), ("0.5 deg", 0.5 * deg), ("1 deg", 1 * deg))},
        "tilted_old": {k: int((np.abs(oang) > v).sum()) for k, v in (("1e-9 rad", 1e-9), ("0.5 deg", 0.5 * deg), ("1 deg", 1 * deg))},
        "exactly_upright_new": exactly_upright(new_ex),
        "exactly_upright_old": exactly_upright(old_ex),
    }
    return out


def same_orientation(a: tuple[F, F], b: tuple[F, F]) -> bool:
    ux, uy = a
    return b in ((ux, uy), (-uy, ux), (-ux, -uy), (uy, -ux))


def exact_compare(new_ex: list[tuple[F, F, F, F]], old_ex: list[tuple[F, F, F, F]]) -> dict[str, Any]:
    """Identity pairing, lower-left frame, exact."""
    disp = [(n[0] - o[0], n[1] - o[1]) for n, o in zip(new_ex, old_ex, strict=True)]
    ref = disp[0]
    rel = [(dx - ref[0], dy - ref[1]) for dx, dy in disp]
    changed_rel = sum(1 for r in rel if r != (0, 0))
    max_rel = max(math.sqrt(float(r[0]) ** 2 + float(r[1]) ** 2) for r in rel)
    max_disp = max(math.sqrt(float(d[0]) ** 2 + float(d[1]) ** 2) for d in disp)
    orient_same = sum(1 for n, o in zip(new_ex, old_ex, strict=True) if same_orientation((n[2], n[3]), (o[2], o[3])))
    turns = []
    for n, o in zip(new_ex, old_ex, strict=True):
        a = math.atan2(float(n[3]), float(n[2])) - math.atan2(float(o[3]), float(o[2]))
        a = (a + math.pi / 4) % (math.pi / 2) - math.pi / 4
        turns.append(abs(a))
    # least-squares common translation, then the residual moves (binary64 of exact values)
    mx = sum(float(d[0]) for d in disp) / len(disp)
    my = sum(float(d[1]) for d in disp) / len(disp)
    resid = [math.hypot(float(d[0]) - mx, float(d[1]) - my) for d in disp]
    return {
        "common_translation_exact": changed_rel == 0,
        "translation_of_square_1": [C.frac_str(ref[0]), C.frac_str(ref[1])],
        "translation_of_square_1_float": [float(ref[0]), float(ref[1])],
        "squares_moved_relative_to_square_1": changed_rel,
        "largest_move_relative_to_square_1": max_rel,
        "largest_displacement": max_disp,
        "after_mean_translation": {
            "mean": [mx, my],
            "largest_residual": max(resid),
            "beyond_1e-15": sum(1 for r in resid if r > 1e-15),
            "beyond_1e-13": sum(1 for r in resid if r > 1e-13),
            "beyond_1e-12": sum(1 for r in resid if r > 1e-12),
        },
        "orientation_unchanged_exactly": orient_same,
        "orientation_changed": len(new_ex) - orient_same,
        "largest_turn_rad": max(turns),
        "turned_beyond_1e-15_rad": sum(1 for t in turns if t > 1e-15),
        "turned_beyond_1e-12_rad": sum(1 for t in turns if t > 1e-12),
    }


def near_sets(receipt: dict[str, Any], lim: float) -> set[tuple[str, str]]:
    return {(a, b) for a, b, _e, f, _k in receipt["near_pairs_below_1e-9"] if f < lim}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--checks", required=True)
    ap.add_argument("--out", required=True)
    ns, _rest = ap.parse_known_args()  # --extra=label=format=path and --pair=new:old are read below
    src = Path(ns.src)
    repo = Path(ns.repo)
    head = src / "ac14112"
    chk = Path(ns.checks)
    files = {
        "yim-n299": ("cert", head / "n299.cert"),
        "yim-n303": ("cert", head / "n303.cert"),
        "yim-n130": ("cert", head / "n130.cert"),
        "yim-n303-first": ("cert", src / "78eb9ea" / "n303.cert"),
        "house-t277-n299": ("corners", repo / WEB / "ozden-s299-upper-bound-2026-11-09/source/n-299-candidate.yaml"),
        "house-t278-n303": ("corners", repo / WEB / "ozden-s303-upper-bound-2026-11-09/source/n-303-candidate.yaml"),
        "house-t259-n130": ("cert", repo / WEB / "mishapolk-issue846-2026-10-30/source/certificates/0000-0999/n130.cert"),
    }
    for n in BH:
        files[f"yim-n{n}"] = ("cert", head / f"n{n}.cert")
        files[f"couzo-n{n}"] = ("cert", repo / WEB / ("couzo-43f666c-2026-10-24" if n == 604 else "couzo-issue763-2026-10-23") / f"source/certificates/best/n{n}.cert")
    extra = [a for a in sys.argv if a.startswith("--extra=")]
    for e in extra:  # label=format=path, for further references
        label, fmt, path = e[len("--extra="):].split("=", 2)
        files[label] = (fmt, Path(path))
    pk = {k: (R.read_cert(p) if f == "cert" else R.read_corners_yaml(p)) for k, (f, p) in files.items()}
    ex = {k: exact_poses(v) for k, v in pk.items()}
    side = {k: F(v.side[0], v.side[1]) for k, v in pk.items()}
    pairs = [
        ("yim-n299", "house-t277-n299"),
        ("yim-n303", "house-t278-n303"),
        ("yim-n130", "house-t259-n130"),
        ("yim-n303-first", "house-t278-n303"),
        ("yim-n303", "yim-n303-first"),
    ] + [(f"yim-n{n}", f"couzo-n{n}") for n in BH]
    pairs += [tuple(p.split(":")) for p in [a[len("--pair="):] for a in sys.argv if a.startswith("--pair=")]]  # type: ignore[misc]
    out: dict[str, Any] = {"program": "l70_identity.py", "program_digests": C.file_digests(C.CHECKER_FILES + ("l70_identity.py",)), "pairs": {}}
    for new, old in pairs:
        r = compare(ex[new], side[new], ex[old], side[old])
        if r["assignment_is_identity"] and r["best_symmetry"] == "identity":
            r["exact"] = exact_compare(ex[new], ex[old])
        rn = chk / f"check-{new}.json"
        ro = chk / f"check-{old}.json"
        if rn.exists() and ro.exists() and r["assignment_is_identity"] and r["best_symmetry"] == "identity":
            jn = json.loads(rn.read_text())
            jo = json.loads(ro.read_text())
            for lim in (1e-12, 1e-9):
                a, b = near_sets(jn, lim), near_sets(jo, lim)
                r[f"near_pairs_below_{lim:g}"] = {"new": len(a), "old": len(b), "both": len(a & b), "only_new": len(a - b), "only_old": len(b - a)}
        out["pairs"][f"{new} vs {old}"] = r
        print(new, "vs", old, r["best_symmetry"], "nearest 1-1", r["nearest_one_to_one"], r["nearest_distinct"], "same id", r["same_id"], "moved", r["moved_beyond"], "largest", f"{r['largest_move']:.3g}", "turns", r["turned_beyond"], f"{r['largest_turn_deg']:.3g}deg", "tilted new/old 1deg", r["tilted_new"]["1 deg"], r["tilted_old"]["1 deg"], flush=True)
        if "exact" in r:
            e = r["exact"]
            print("   exact: common translation", e["common_translation_exact"], "moved rel sq1", e["squares_moved_relative_to_square_1"], "max rel", f"{e['largest_move_relative_to_square_1']:.3g}", "orient changed", e["orientation_changed"], "max turn rad", f"{e['largest_turn_rad']:.3g}", "after mean:", e["after_mean_translation"])
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
