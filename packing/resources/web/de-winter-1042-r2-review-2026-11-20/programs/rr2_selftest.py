"""Lane rR2 (issue 1042 derived bounds), check C4: synthetic tests of C1 to C3.

Decides nothing about the source. It holds rr2_measure, rr2_strips and rr2_envelope to
cases with known answers:

- measure reading: totals, eight images, refusal of bad files;
- periods and strip masses: a synthetic periodic measure passes, a moved rectangle fails,
  and M + d (b_x + b_y) + d^2 c equals the mass of the explicitly built extension;
- the region integrator: a uniform density gives exactly T^2; random small measures agree
  with an independent exact brute force (with a staircase bracket for the disk); the disk
  area routine agrees with staircase brackets; on a periodic measure the plain regions at
  T = S - 1 give M(-1).

Usage: python -I rr2_selftest.py --scratch DIR [--out FILE]
"""

from __future__ import annotations

import argparse
import json
import math
import random
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rr2_envelope as env  # noqa: E402
from rr2_measure import GRID, Measure  # noqa: E402
from rr2_strips import periodic, strip_claim, strip_masses  # noqa: E402

RHO2 = GRID * GRID // 2


def write_measure(path: Path, side: F, prims: list, total: F | None = None) -> Path:
    rects = [
        {"rectangle": [str(v) for v in (x0, y0, x1, y1)], "mass": str(m)}
        for (x0, y0, x1, y1, m) in prims
    ]
    tot = sum((p[4] for p in prims), F(0)) if total is None else total
    data = {"n": 0, "L": str(side), "points": [], "total_mass": str(tot), "rectangles": rects}
    path.write_text(json.dumps(data))
    return path


def test_measure(scratch: Path) -> dict:
    out = {}
    side = F(9)
    prims = [(F(0), F(0), F(9), F(9), F(81, 10)), (F(32, 10), F(5, 10), F(33, 10), F(15, 10), F(1, 7))]
    m = Measure.from_file(write_measure(scratch / "m1.json", side, prims))
    imgs = m.images()
    from rr2_measure import image_mass

    out["eight_images_each"] = len(imgs) == 16
    out["image_masses_sum_to_total"] = sum((image_mass(i) for i in imgs), F(0)) == m.total()
    bad = []
    for name, p, tot in [
        ("total", prims, F(1)),
        ("offgrid", [(F(1, 3), F(0), F(1), F(1), F(1))], None),
        ("negative", [(F(0), F(0), F(1), F(1), F(-1))], None),
        ("outside", [(F(0), F(0), F(10), F(1), F(1))], None),
    ]:
        try:
            Measure.from_file(write_measure(scratch / f"bad-{name}.json", side, p, tot))
            bad.append(name)
        except ValueError:
            pass
    out["bad_files_refused"] = not bad
    return out


def periodic_prims() -> list:
    """A measure on [0, 9]^2 periodic on the centred band [3, 6] of three strips."""
    prims = [(F(0), F(0), F(9), F(9), F(81, 10))]
    for j in range(3):
        x0 = F(32, 10) + j
        prims.append((x0, F(5, 10), x0 + F(1, 10), F(15, 10), F(1, 7)))
        prims.append((x0 + F(1, 100), F(2), x0 + F(5, 100), F(29, 10), F(2, 11)))
    return prims


def extension_mass(imgs, S: int, p: int, d: int) -> F:
    """Mass of the extension built image by image: exterior kept, far side moved by d,
    the band filled with copies of its first strip."""
    a = (S - p * GRID) // 2
    b = a + p * GRID

    def pieces(lo: int, hi: int) -> list[tuple[int, int]]:
        out = []
        if lo < a:
            out.append((lo, min(hi, a)))
        s0, s1 = max(lo, a), min(hi, a + GRID)
        if s0 < s1:
            for k in range(p + d):
                out.append((s0 + k * GRID, s1 + k * GRID))
        if hi > b:
            out.append((max(lo, b) + d * GRID, hi + d * GRID))
        return out

    total = F(0)
    for x0, y0, x1, y1, dens in imgs:
        for u0, u1 in pieces(x0, x1):
            for v0, v1 in pieces(y0, y1):
                total += dens * (u1 - u0) * (v1 - v0)
    return total / (GRID * GRID)


def test_strips(scratch: Path) -> dict:
    out = {}
    side = F(9)
    m = Measure.from_file(write_measure(scratch / "per.json", side, periodic_prims()))
    imgs = m.images()
    per = periodic(imgs, m.S, 3)
    out["periodic_measure_holds"] = per["holds"]
    sm = strip_masses(imgs, m.S, 3)
    M = m.total()
    for d in (-1, 1, 2):
        formula = M + d * (sm["bx"] + sm["by"]) + d * d * sm["c"]
        out[f"formula_equals_built_extension_d{d}"] = formula == extension_mass(imgs, m.S, 3, d)
    moved = periodic_prims()
    x0, y0, x1, y1, w = moved[1]
    moved[1] = (x0 + F(1, 100), y0, x1 + F(1, 100), y1, w)
    m2 = Measure.from_file(write_measure(scratch / "moved.json", side, moved))
    out["moved_rectangle_refused"] = not periodic(m2.images(), m2.S, 3)["holds"]
    heavier = periodic_prims()
    heavier[3] = heavier[3][:4] + (heavier[3][4] * (1 + F(1, 10**12)),)
    m3 = Measure.from_file(write_measure(scratch / "heavier.json", side, heavier))
    out["heavier_rectangle_refused"] = not periodic(m3.images(), m3.S, 3)["holds"]
    bx, by, c = sm["bx"], sm["by"], sm["c"]
    out["p2_refused"] = not strip_claim(10**6, 1, 2, side + 1, side, M, bx, by, c, None, side + 1)["decided"]
    out["p_plus_d_1_refused"] = not strip_claim(10**6, -2, 3, side - 2, side, M, bx, by, c, None, side - 2)["decided"]
    out["mass_at_n_refused"] = not strip_claim(int(M), 0, 3, side, side, M, bx, by, c, None, side)["decided"]
    return out


# ---------------------------------------------------------------- region integrator


def isqrt_bounds(y: F) -> tuple[int, int]:
    """Integers lo <= sqrt(y) <= hi for a rational y >= 0."""
    if y <= 0:
        return 0, 0
    fl = y.numerator // y.denominator
    lo = math.isqrt(fl)
    ce = -((-y.numerator) // y.denominator)
    hi = math.isqrt(ce)
    if hi * hi < ce:
        hi += 1
    return lo, hi


def stair_area(ua: int, ub: int, va: int, vb: int, steps: int) -> tuple[F, F]:
    area = F((ub - ua) * (vb - va))
    if ub * ub + vb * vb <= RHO2:
        return area, area
    if ua * ua + va * va >= RHO2:
        return F(0), F(0)
    lo = hi = F(0)
    width = F(ub - ua, steps)
    for k in range(steps):
        s0 = ua + width * k
        s1 = s0 + width
        h_hi = min(max(isqrt_bounds(RHO2 - s0 * s0)[1] - va, 0), vb - va)
        h_lo = min(max(isqrt_bounds(RHO2 - s1 * s1)[0] - va, 0), vb - va)
        lo += width * h_lo
        hi += width * h_hi
    return lo, hi


def brute(imgs, S: F, T: F, q: F, r: F, disk: bool, steps: int = 400) -> tuple[F, F]:
    """Exact integral of the region density over [0, T]^2, cell by cell (independent of
    the C++ sweep); straddling disk cells are bracketed by a staircase."""
    Sg, Tg, qg, rg = (int(v * GRID) for v in (S, T, q, r))
    off = (0, Sg - Tg)
    marks = {0, Tg, qg - rg, qg, qg + rg}
    for x0, y0, x1, y1, _ in imgs:
        for o in off:
            marks.update((x0 - o, x1 - o, y0 - o, y1 - o))
    cuts = sorted(v for v in marks if 0 <= v <= Tg)
    lo = hi = F(0)
    for i in range(len(cuts) - 1):
        xa, xb = cuts[i], cuts[i + 1]
        sx = (xb <= qg + rg, xa >= qg - rg)
        for j in range(len(cuts) - 1):
            ya, yb = cuts[j], cuts[j + 1]
            sy = (yb <= qg + rg, ya >= qg - rg)
            vals = {}
            for s in (0, 1):
                for t in (0, 1):
                    if sx[s] and sy[t]:
                        px2, py2 = xa + xb + 2 * off[s], ya + yb + 2 * off[t]
                        vals[(s, t)] = sum(
                            (d for (x0, y0, x1, y1, d) in imgs
                             if 2 * x0 <= px2 < 2 * x1 and 2 * y0 <= py2 < 2 * y1),
                            F(0),
                        )
            area = (xb - xa) * (yb - ya)
            if disk and len(vals) == 4:
                left, low = xb <= qg, yb <= qg
                opp = (1 if left else 0, 1 if low else 0)
                others = max(v for k, v in vals.items() if k != opp)
                extra = vals[opp] - others
                lo += area * others
                hi += area * others
                if extra > 0:
                    ua, ub = (qg - xb, qg - xa) if left else (xa - qg, xb - qg)
                    va, vb = (qg - yb, qg - ya) if low else (ya - qg, yb - qg)
                    alo, ahi = stair_area(ua, ub, va, vb, steps)
                    lo += alo * extra
                    hi += ahi * extra
            else:
                v = max(vals.values())
                lo += area * v
                hi += area * v
    g2 = GRID * GRID
    return lo / g2, hi / g2


def test_envelope(scratch: Path) -> dict:
    out: dict = {}
    binary = env.build(scratch)
    side = F(9)
    m = Measure.from_file(write_measure(scratch / "uni.json", side, [(F(0), F(0), side, side, side * side)]))
    imgs = env.rounded_images(m)
    for T in (side - F(7, 10), side + F(1, 10)):
        for disk in (False, True):
            res = env.integrate(binary, scratch, imgs, side, T, T / 2, env.R_SOURCE, disk)
            out[f"uniform_T{float(T)}_disk{int(disk)}_exact"] = res["mass_up"] == res["mass_dn"] == T * T
    rng = random.Random(1042)
    agree = []
    for case in range(6):
        S = F(rng.choice([6000, 7500]), 1000)
        prims = []
        for _ in range(rng.randint(2, 3)):
            x0 = F(rng.randint(0, int(S * 1000) - 400), 1000)
            y0 = F(rng.randint(0, int(S * 1000) - 400), 1000)
            prims.append((x0, y0, x0 + F(rng.randint(5, 400), 1000), y0 + F(rng.randint(5, 400), 1000),
                          F(rng.randint(1, 50), rng.randint(7, 40))))
        prims.append((F(0), F(0), S, S, S * S / 4))
        ms = Measure.from_file(write_measure(scratch / f"rnd{case}.json", S, prims))
        T = S + F(rng.randint(-1100, 200), 1000)
        q = T / 2 if case % 2 == 0 else T / 2 + F(rng.randint(-600, 600), 1000)
        disk = case % 3 != 2
        hyp = env.hypotheses(S, T, q, env.R_SOURCE)
        if not all(hyp.values()):
            q = T / 2
        exact_imgs = ms.images()
        blo, bhi = brute(exact_imgs, S, T, q, env.R_SOURCE, disk)
        res = env.integrate(binary, scratch, env.rounded_images(ms), S, T, q, env.R_SOURCE, disk)
        ok = res["mass_dn"] <= bhi and blo <= res["mass_up"]
        tight = res["mass_up"] - res["mass_dn"] < F(1, 10**6)
        agree.append({"case": case, "S": str(S), "T": str(T), "q": str(q), "disk": disk,
                      "brute": [float(blo), float(bhi)], "sweep": [float(res["mass_dn"]), float(res["mass_up"])],
                      "overlap": ok, "tight": tight, "straddling_cells": res["straddling_cells"]})
    # disk stress: features placed so that the opposite region dominates near the circle
    stress = []
    for label, T, lo_c in (("T_S_minus_1", F(5), F(28, 10)), ("T_above_S", F(605, 100), F(23, 10))):
        S = F(6)
        prims = [(F(0), F(0), S, S, S * S / 32)]
        for _ in range(6):
            x0 = lo_c + F(rng.randint(0, 250), 1000)
            y0 = lo_c + F(rng.randint(0, 250), 1000)
            prims.append((x0, y0, x0 + F(rng.randint(10, 150), 1000), y0 + F(rng.randint(10, 150), 1000),
                          F(rng.randint(1, 9), rng.randint(5, 30))))
        ms = Measure.from_file(write_measure(scratch / f"stress-{label}.json", S, prims))
        blo, bhi = brute(ms.images(), S, T, T / 2, env.R_SOURCE, True, steps=200)
        res = env.integrate(binary, scratch, env.rounded_images(ms), S, T, T / 2, env.R_SOURCE, True)
        plain = env.integrate(binary, scratch, env.rounded_images(ms), S, T, T / 2, env.R_SOURCE, False)
        stress.append({"case": label, "brute": [float(blo), float(bhi)],
                       "sweep": [float(res["mass_dn"]), float(res["mass_up"])],
                       "plain_sweep": [float(plain["mass_dn"]), float(plain["mass_up"])],
                       "overlap": res["mass_dn"] <= bhi and blo <= res["mass_up"],
                       "tight": res["mass_up"] - res["mass_dn"] < F(1, 10**6),
                       "disk_below_plain": res["mass_up"] < plain["mass_dn"],
                       "straddling_cells": res["straddling_cells"]})
    out["disk_stress_cases"] = stress
    out["disk_stress_agree"] = all(
        a["overlap"] and a["tight"] and a["disk_below_plain"] and a["straddling_cells"] > 0 for a in stress
    )
    out["random_cases"] = agree
    out["random_cases_agree"] = all(a["overlap"] and a["tight"] for a in agree)
    out["random_cases_use_disk"] = any(a["disk"] and a["straddling_cells"] > 0 for a in agree)
    cells = []
    for _ in range(40):
        theta = rng.uniform(0.0, math.pi / 2)
        cu = int(70_710_678 * math.cos(theta))
        cv = int(70_710_678 * math.sin(theta))
        ua = max(0, cu - rng.randint(0, 30_000))
        va = max(0, cv - rng.randint(0, 30_000))
        cells.append((ua, ua + rng.randint(1, 30_000), va, va + rng.randint(1, 30_000)))
    for _ in range(10):
        ua = rng.randint(0, 70_000_000)
        va = rng.randint(0, 70_000_000)
        cells.append((ua, ua + rng.randint(1, 3_000_000), va, va + rng.randint(1, 3_000_000)))
    cells.append((0, 70_710_678, 0, 1_000))
    cells.append((70_710_000, 70_710_700, 0, 50_000))
    text = "\n".join(" ".join(str(v) for v in c) for c in cells) + "\n"
    proc = subprocess.run([str(binary), "area"], input=text.encode(), capture_output=True, check=True)
    area_ok = []
    for c, line in zip(cells, proc.stdout.decode().splitlines()):
        lo, hi, _ = (int(v) for v in line.split())
        slo, shi = stair_area(*c, steps=3000)
        area_ok.append(lo <= shi and slo <= hi and hi - lo <= 2 * 16 + 2)
    out["disk_area_agrees_with_staircase"] = all(area_ok) and len(area_ok) == len(cells)
    mp = Measure.from_file(write_measure(scratch / "per2.json", side, periodic_prims()))
    sm = strip_masses(mp.images(), mp.S, 3)
    m_minus = mp.total() - (sm["bx"] + sm["by"]) + sm["c"]
    res = env.integrate(binary, scratch, env.rounded_images(mp), side, side - 1, (side - 1) / 2,
                        env.R_SOURCE, False)
    out["periodic_T_S_minus_1_gives_M_minus_1"] = res["mass_dn"] <= m_minus <= res["mass_up"]
    hyp = env.hypotheses(side, side - 1, (side - 1) / 2, F(707106, 10**6))
    out["r_707106_refused"] = not hyp["r_squared_at_least_half"]
    hyp = env.hypotheses(side, side, F(1, 2), env.R_SOURCE)
    out["seam_violating_fit_refused"] = not hyp["regions_fit_in_anchor"]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True, type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    report = {
        "measure": test_measure(args.scratch),
        "strips": test_strips(args.scratch),
        "envelope": test_envelope(args.scratch),
    }
    failed = []
    for group, res in report.items():
        for k, v in res.items():
            if isinstance(v, bool) and not v:
                failed.append(f"{group}.{k}")
    report["failed"] = failed
    text = json.dumps(report, indent=1, default=str)
    if args.out:
        args.out.write_text(text + "\n")
    print("PASS" if not failed else "FAIL", failed)
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
