"""Contraction margins for the L70 review (RV-3), exact, from the definition alone.

For a packing with centres c_i and orientations fixed, scale every centre by the
same factor lambda (about any point: the box is re-fitted, so the point does not
matter) and fit the least box around the result. Squares stay unit squares.

* Pair (i, j): with d = c_j - c_i, every one of the four edge normals of the pair
  sees the two squares at total half-width T = (1 + |u_i.u_j| + |u_i.v_j|)/2, so the
  interiors stay disjoint exactly when lambda * max_w |w.d| >= T. The least factor
  is lambda* = max over pairs of T / max_w |w.d|, rational, attained by a pair that
  then touches.
* Box: each square's half-extent on either axis is h_i = (|cos| + |sin|)/2, so the
  contracted width on x is max(lambda x_i + h_i) - min(lambda x_i - h_i), likewise
  on y; the contracted side S_c is the larger.
* The contraction margin is S - S_c: how far the certificate can be shrunk
  uniformly, with no re-solve, and stay a packing. It splits into the envelope part
  S - S_c(1) (re-fitting the box alone) and the scaling part S_c(1) - S_c(lambda*).

The contracted packing is written out exactly and decided by the frozen checker
(l70_check.decide, both methods): at S_c it must be accepted with the binding pair
touching; at S_c - 1e-30, and at the factor lambda* (1 - 1e-30), refused.

Usage: python -I l70_contract.py --src SRC --repo REPO --out contract.json [--only LABEL ...]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402
import l70_reader as R  # noqa: E402

WEB = "packing/resources/web"
EPS = F(1, 10**30)
BH = (553, 599, 600, 601, 602, 604, 645, 647, 648, 699, 700)


def geometry(pk: R.Packing) -> list[tuple[F, F, F, F, F, F]]:
    """(cx, cy, ux, uy, vx, vy) per square, exact."""
    out = []
    if pk.kind == "cert":
        for xn, xd, yn, yd, tn, td in pk.squares:
            t = F(tn, td)
            d = 1 + t * t
            c = (1 - t * t) / d
            s = 2 * t / d
            out.append((F(xn, xd), F(yn, yd), c, s, -s, c))
    else:
        for row in pk.squares:
            p = [(F(row[4 * k], row[4 * k + 1]), F(row[4 * k + 2], row[4 * k + 3])) for k in range(4)]
            cx = (p[0][0] + p[2][0]) / 2
            cy = (p[0][1] + p[2][1]) / 2
            ux, uy = p[1][0] - p[0][0], p[1][1] - p[0][1]
            vx, vy = p[3][0] - p[0][0], p[3][1] - p[0][1]
            out.append((cx, cy, ux, uy, vx, vy))
    return out


def least_factor(g: list[tuple[F, F, F, F, F, F]]) -> tuple[F, list[tuple[F, int, int]]]:
    n = len(g)
    best: list[tuple[F, int, int]] = []
    lam = F(0)
    for i in range(n):
        cxi, cyi, uxi, uyi, vxi, vyi = g[i]
        for j in range(i + 1, n):
            cxj, cyj, uxj, uyj, vxj, vyj = g[j]
            dx, dy = cxj - cxi, cyj - cyi
            t_half = (1 + abs(uxi * uxj + uyi * uyj) + abs(uxi * vxj + uyi * vyj)) / 2
            m = max(abs(uxi * dx + uyi * dy), abs(vxi * dx + vyi * dy), abs(uxj * dx + uyj * dy), abs(vxj * dx + vyj * dy))
            lij = t_half / m
            if lij > lam:
                lam = lij
            if len(best) < 8 or lij > best[-1][0]:
                best.append((lij, i, j))
                best.sort(key=lambda e: -e[0])
                del best[8:]
    return lam, best


def widths(g: list[tuple[F, F, F, F, F, F]], lam: F) -> tuple[F, F, F, F]:
    """(min_x, min_y, width_x, width_y) of the box around the scaled packing."""
    lo_x = lo_y = hi_x = hi_y = None
    for cx, cy, ux, uy, _vx, _vy in g:
        h = (abs(ux) + abs(uy)) / 2
        ax, bx = lam * cx - h, lam * cx + h
        ay, by = lam * cy - h, lam * cy + h
        lo_x = ax if lo_x is None or ax < lo_x else lo_x
        hi_x = bx if hi_x is None or bx > hi_x else hi_x
        lo_y = ay if lo_y is None or ay < lo_y else lo_y
        hi_y = by if hi_y is None or by > hi_y else hi_y
    assert lo_x is not None and lo_y is not None and hi_x is not None and hi_y is not None
    return lo_x, lo_y, hi_x - lo_x, hi_y - lo_y


def contracted_packing(pk: R.Packing, g: list[tuple[F, F, F, F, F, F]], lam: F, side: F) -> R.Packing:
    lo_x, lo_y, _wx, _wy = widths(g, lam)
    rows: list[tuple[int, ...]] = []
    if pk.kind == "cert":
        for (cx, cy, *_), row in zip(g, pk.squares, strict=True):
            x = lam * cx - lo_x
            y = lam * cy - lo_y
            rows.append((x.numerator, x.denominator, y.numerator, y.denominator, row[4], row[5]))
    else:
        for (cx, cy, *_), row in zip(g, pk.squares, strict=True):
            dx = (lam - 1) * cx - lo_x
            dy = (lam - 1) * cy - lo_y
            v: list[int] = []
            for k in range(4):
                x = F(row[4 * k], row[4 * k + 1]) + dx
                y = F(row[4 * k + 2], row[4 * k + 3]) + dy
                v.extend((x.numerator, x.denominator, y.numerator, y.denominator))
            rows.append(tuple(v))
    return R.Packing(n=pk.n, side=(side.numerator, side.denominator), kind=pk.kind, squares=tuple(rows), ids=pk.ids)


def measure(label: str, pk: R.Packing, verify: bool) -> dict[str, Any]:
    t0 = time.process_time()
    side = F(pk.side[0], pk.side[1])
    g = geometry(pk)
    lam, best = least_factor(g)
    _, _, wx1, wy1 = widths(g, F(1))
    env = max(wx1, wy1)
    _, _, wxl, wyl = widths(g, lam)
    sc = max(wxl, wyl)
    out: dict[str, Any] = {
        "label": label,
        "sha256": pk.meta.get("sha256"),
        "n": pk.n,
        "side": C.frac_str(side),
        "lambda_star": C.frac_str(lam),
        "one_minus_lambda_star": float(1 - lam),
        "binding_pairs": [[pk.ids[i], pk.ids[j], float(1 - v)] for v, i, j in best],
        "envelope_side": C.frac_str(env),
        "envelope_part": float(side - env),
        "contracted_side": C.frac_str(sc),
        "contracted_side_floor_40": C.floor_places(sc, 40),
        "contracted_side_ceil_12": C.ceil_places(sc, 12),
        "contracted_binding_axis": "x" if wxl >= wyl else "y",
        "scaling_part": float(env - sc),
        "margin": C.frac_str(side - sc),
        "margin_float": float(side - sc),
    }
    if verify:
        at = C.decide(contracted_packing(pk, g, lam, sc), keep_near=False)
        below = C.decide(contracted_packing(pk, g, lam, sc - EPS), keep_near=False)
        lam2 = lam * (1 - EPS)
        _, _, wx2, wy2 = widths(g, lam2)
        further = C.decide(contracted_packing(pk, g, lam2, max(wx2, wy2)), keep_near=False)
        out["verify"] = {
            "at_contracted_side": {"verdict": at["verdict"], "touching_pairs": at["A"]["touching_pairs"], "classes_A": at["A"]["classes"], "classes_B": at["B"]["classes"], "wall_contacts": {w: at["A"]["walls"][w]["contacts"] for w in C.WALLS}, "agree": at["agree"]},
            "side_minus_1e-30": {"verdict": below["verdict"], "outside_A": below["A"]["outside"], "outside_B": below["B"]["outside"]},
            "factor_times_1_minus_1e-30": {"verdict": further["verdict"], "overlapping_A": further["A"]["overlapping_pairs"], "overlapping_B": further["B"]["overlapping_pairs"]},
            "as_stated": at["verdict"] == "ACCEPT" and at["A"]["classes"]["touch"] >= 1 and below["verdict"] == "REFUSE" and further["verdict"] == "REFUSE" and bool(further["A"]["overlapping_pairs"]),
        }
    out["cpu_seconds"] = round(time.process_time() - t0, 3)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--no-verify", action="store_true")
    ns = ap.parse_args()
    src = Path(ns.src)
    repo = Path(ns.repo)
    head = src / "ac14112"
    certs: dict[str, tuple[str, Path]] = {
        "house-t277-n299": ("corners", repo / WEB / "ozden-s299-upper-bound-2026-11-09/source/n-299-candidate.yaml"),
        "house-t278-n303": ("corners", repo / WEB / "ozden-s303-upper-bound-2026-11-09/source/n-303-candidate.yaml"),
        "house-t259-n130": ("cert", repo / WEB / "mishapolk-issue846-2026-10-30/source/certificates/0000-0999/n130.cert"),
        "precedent-t254-n130": ("cert", repo / WEB / "couzo-issue843-2026-10-28/source/certificates/n130.cert"),
        "precedent-t257-n260": ("cert", repo / WEB / "evand-issue845-2026-10-29/source/search/packer/candidates/s260_1028.cert"),
        "precedent-t265-n260": ("cert", repo / WEB / "yim-s260-upper-bound-2026-11-05/source/n260.cert"),
        "yim-n299": ("cert", head / "n299.cert"),
        "yim-n303": ("cert", head / "n303.cert"),
        "yim-n130": ("cert", head / "n130.cert"),
        "yim-n303-first": ("cert", src / "78eb9ea" / "n303.cert"),
    }
    for n in BH:
        certs[f"yim-n{n}"] = ("cert", head / f"n{n}.cert")
        if n == 604:
            certs[f"couzo-n{n}"] = ("cert", repo / WEB / "couzo-43f666c-2026-10-24/source/certificates/best/n604.cert")
        else:
            certs[f"couzo-n{n}"] = ("cert", repo / WEB / f"couzo-issue763-2026-10-23/source/certificates/best/n{n}.cert")
    pairs = [
        ("yim-n299", "house-t277-n299", "299 against T-277"),
        ("yim-n303", "house-t278-n303", "303 (546928a) against T-278"),
        ("yim-n130", "house-t259-n130", "130 against T-259"),
        ("yim-n303-first", "house-t278-n303", "303 (78eb9ea) against T-278"),
        ("house-t259-n130", "precedent-t254-n130", "precedent: T-259 against T-254"),
        ("precedent-t265-n260", "precedent-t257-n260", "precedent: T-265 against T-257"),
    ] + [(f"yim-n{n}", f"couzo-n{n}", f"{n} against the current row") for n in BH]
    todo = [k for k in certs if not ns.only or k in ns.only]
    meas: dict[str, Any] = {}
    outp = Path(ns.out)
    if outp.exists():
        meas = json.loads(outp.read_text()).get("measurements", {})
    for k in todo:
        fmt, path = certs[k]
        pk = R.read_cert(path) if fmt == "cert" else R.read_corners_yaml(path)
        meas[k] = measure(k, pk, verify=not ns.no_verify)
        m = meas[k]
        print(k, "1-lambda*", f"{m['one_minus_lambda_star']:.4e}", "margin", f"{m['margin_float']:.4e}", "envelope", f"{m['envelope_part']:.3e}", "verify", m.get("verify", {}).get("as_stated"), "cpu", m["cpu_seconds"], flush=True)
    shares = []
    for new, old, what in pairs:
        if new in meas and old in meas:
            gain = F(meas[old]["side"]) - F(meas[new]["side"])
            margin = F(meas[old]["margin"])
            shares.append({
                "what": what,
                "new": new,
                "predecessor": old,
                "gain": C.frac_str(gain),
                "gain_float": float(gain),
                "predecessor_margin_float": float(margin),
                "share": float(gain / margin) if margin else None,
                "new_minus_contracted_predecessor_float": float(F(meas[new]["side"]) - F(meas[old]["contracted_side"])),
            })
    out = {
        "program": "l70_contract.py",
        "program_digests": C.file_digests(C.CHECKER_FILES + ("l70_contract.py",)),
        "definition": "S - S_c, S_c the least box side around the centres scaled by the least factor lambda* keeping every pair interior-disjoint, orientations kept",
        "measurements": meas,
        "shares": shares,
    }
    outp.write_text(json.dumps(out, indent=1) + "\n")
    for s in shares:
        print(s["what"], "gain", f"{s['gain_float']:.4e}", "margin", f"{s['predecessor_margin_float']:.4e}", "share", None if s["share"] is None else f"{s['share']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
