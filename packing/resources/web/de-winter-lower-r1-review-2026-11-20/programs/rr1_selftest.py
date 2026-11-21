"""Lane rR1-lower: self-test on synthetic data only.  It holds the polygon, the clip, the
box bound, the domain and the decider to exact rational computations, and requires three
deliberately broken variants (T1 to T3 of the frozen plan) to be caught.

Usage: rr1_selftest.py --scratch DIR --out FILE
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rr1_common as C  # noqa: E402
import rr1_decide as D  # noqa: E402

FAILS: list[str] = []
COUNTS: dict[str, int] = {}


def check(name: str, ok: bool, detail: str = "") -> None:
    COUNTS[name] = COUNTS.get(name, 0) + 1
    if not ok:
        FAILS.append(f"{name}: {detail}")


def poly_inside_all_squares(verts: list[tuple[int, int]], Q: int, lo: F, hi: F, samples: int = 400) -> float:
    """Largest float violation of |p.e| <= 1/2, |p.e_perp| <= 1/2 over sampled angles."""
    a0, a1 = 2 * math.atan(float(lo)), 2 * math.atan(float(hi))
    worst = -1.0
    for i in range(samples + 1):
        th = a0 + (a1 - a0) * i / samples
        c, s = math.cos(th), math.sin(th)
        for x, y in verts:
            px, py = x / Q, y / Q
            worst = max(worst, abs(px * c + py * s) - 0.5, abs(-px * s + py * c) - 0.5)
    return worst


def random_bin(rng: random.Random) -> tuple[F, F]:
    lo = F(rng.randrange(0, 4100), 10000)
    w = F(rng.randrange(5, 200), 100000)
    return lo, lo + w


def synthetic_measure(rng: random.Random, L: F, nrect: int, thin: bool) -> dict:
    rows = [(F(0), F(0), L, L, F(97, 100) * L * L)]  # background density 0.97
    for _ in range(nrect):
        x0 = F(rng.randrange(0, int(L * 1000) - 50), 1000)
        y0 = F(rng.randrange(0, int(L * 1000) - 50), 1000)
        wx = F(rng.randrange(1, 400), 1000) if not thin else F(rng.randrange(1, 20), 10000)
        wy = F(rng.randrange(1, 400), 1000)
        x1, y1 = min(x0 + wx, L), min(y0 + wy, L)
        rows.append((x0, y0, x1, y1, F(rng.randrange(1, 60), 1000) * 8))
    return C.expand(rows, L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    scr = Path(a.scratch)
    scr.mkdir(parents=True, exist_ok=True)
    exe = C.build_c(scr)
    rng = random.Random(20261120)
    check("tstar", C.tstar_ok())

    # 1. polygons: exact vertices inside I, dense sampling, and T1 caught
    Q = 2**33
    t1_caught = 0
    for _ in range(40):
        lo, hi = random_bin(rng)
        P = C.bin_polygon(lo, hi, Q)
        viol = poly_inside_all_squares(P["verts"], Q, P["lo"], P["hi"])
        check("polygon_inside_sampled_squares", viol <= 1e-12, f"{lo} {hi} {viol}")
        area = F(C.poly_area(P["verts"]), 2 * Q * Q)
        dth = 2 * math.atan(float(P["hi"])) - 2 * math.atan(float(P["lo"]))
        check("polygon_area_near_ideal", float(area) >= 1 - dth / 2 - 1e-6, f"{area} {dth}")
        M = C.bin_polygon(lo, hi, Q, mutant_center_square=True)
        if poly_inside_all_squares(M["verts"], Q, M["lo"], M["hi"]) > 1e-9:
            t1_caught += 1
    check("T1_center_square_mutant_caught", t1_caught == 40, f"{t1_caught}/40")

    # 2. the clip against exact rational areas
    L = F(3)
    merged = synthetic_measure(rng, L, 30, thin=True)
    lat = C.lattice(merged, L)
    Ql = lat["Q"]
    rects = scr / "rects.txt"
    C.write_rects(lat, rects)
    lo, hi = F(1, 10), F(1013, 10000)
    P = C.bin_polygon(lo, hi, Ql)
    pf = scr / "poly.txt"
    pf.write_text(f"{len(P['verts'])}\n" + "".join(f"{x} {y}\n" for x, y in P["verts"]))
    pts = [(rng.randrange(int(Ql * F(1, 2)), int(Ql * F(5, 2))), rng.randrange(int(Ql * F(1, 2)), int(Ql * F(5, 2))))
           for _ in range(12)]
    ptf = scr / "pts.txt"
    ptf.write_text("".join(f"{x} {y}\n" for x, y in pts))
    out = C.run_c(exe, ["clip", str(rects), str(pf), str(ptf)]).splitlines()
    for (cx, cy), line in zip(pts, out, strict=True):
        vals = [int(v) for v in line.split()]
        poly = [(F(cx + x, 1), F(cy + y, 1)) for x, y in P["verts"]]
        for (X0, Y0, X1, Y1, _d, _rho), a2 in zip(lat["rects"], vals, strict=True):
            ex = 2 * C.area_poly(C.clip_convex(poly, F(X0), F(Y0), F(X1), F(Y1)))
            per = 2 * ((X1 - X0) + (Y1 - Y0)) + 8 * Ql
            check("clip_not_above_exact", a2 <= ex, f"{a2} > {ex}")
            check("clip_close_to_exact", ex - a2 <= 4 * per + 64, f"{ex - a2} vs {per}")

    # 3. box bounds against exact captures of c + P at points of the box; T2 caught
    boxes = []
    for _ in range(10):
        xa = rng.randrange(int(Ql * F(3, 2)), int(Ql * F(2)))
        ya = rng.randrange(int(Ql * F(3, 2)), int(Ql * F(2)))
        d = rng.choice([Ql // 1000, Ql // 100, Ql // 20])
        boxes.append((xa, xa + d, ya, ya + d))
    bf = scr / "boxes.txt"
    bf.write_text("".join(f"{a} {b} {c} {e}\n" for a, b, c, e in boxes))
    bounds = [int(v) for v in C.run_c(exe, ["boxb", str(rects), str(pf), str(bf)]).split()]

    def exact_P(cx: F, cy: F, mer: dict) -> F:
        return C.exact_capture(mer, [(cx + F(x, Ql), cy + F(y, Ql)) for x, y in P["verts"]])

    for (xa, xb, ya, yb), bd in zip(boxes, bounds, strict=True):
        for _ in range(4):
            cx = F(rng.randrange(xa, xb + 1), Ql)
            cy = F(rng.randrange(ya, yb + 1), Ql)
            ex = exact_P(cx, cy, merged)
            check("box_bound_not_above_exact", F(bd, 2**C.W_BITS) <= ex, f"{bd / 2**64} > {float(ex)}")
    # the T2 instance: two strips, each captured near only one side of the box
    c0 = F(3, 2)
    mz = {
        (c0 + F(508, 1000), c0 - F(1, 1000), c0 + F(512, 1000), c0 + F(1, 1000)): F(4, 1000) * F(2, 1000),
        (c0 - F(502, 1000), c0 - F(1, 1000), c0 - F(498, 1000), c0 + F(1, 1000)): F(4, 1000) * F(2, 1000),
    }
    latz = C.lattice(mz, L)
    Qz = latz["Q"]
    Pz = C.bin_polygon(F(0), F(1, 100), Qz)
    pz = scr / "polyz.txt"
    pz.write_text(f"{len(Pz['verts'])}\n" + "".join(f"{x} {y}\n" for x, y in Pz["verts"]))
    rz = scr / "rectsz.txt"
    C.write_rects(latz, rz)
    xa = int(c0 * Qz)
    boxz = (xa, xa + Qz // 100, xa, xa + Qz // 1000)
    bzf = scr / "boxz.txt"
    bzf.write_text(" ".join(str(v) for v in boxz) + "\n")
    good = int(C.run_c(exe, ["boxb", str(rz), str(pz), str(bzf)]).split()[0])
    bad = int(C.run_c(exe, ["boxb", str(rz), str(pz), str(bzf)], {"RR1_MUTANT_KEEPZERO": "1"}).split()[0])
    mid = C.exact_capture(mz, [(c0 + F(1, 200) + F(x, Qz), c0 + F(y, Qz)) for x, y in Pz["verts"]])
    check("T2_correct_bound_sound", F(good, 2**64) <= mid, f"{good} vs {mid}")
    check("T2_keep_zero_mutant_caught", F(bad, 2**64) > mid, f"mutant {bad / 2**64} vs exact {float(mid)}")

    # 4. the domain contains every admissible centre of the bin; T3 caught
    t3_caught = 0
    for _ in range(20):
        lo, hi = random_bin(rng)
        Pd = C.bin_polygon(lo, hi, Ql)
        X0, X1 = C.domain(L, Pd["lo"], Ql)
        Xm0, Xm1 = C.domain(L, Pd["hi"], Ql)
        worst_ok = True
        worst_mut = True
        for i in range(41):
            t = Pd["lo"] + (Pd["hi"] - Pd["lo"]) * i / 40
            need = (L - C.w_of(t)) * Ql
            worst_ok &= X1 >= need and X0 <= L / 2 * Ql
            worst_mut &= Xm1 >= need
        check("domain_contains_admissible_centres", worst_ok)
        t3_caught += 0 if worst_mut else 1
    check("T3_right_end_domain_mutant_caught", t3_caught == 20, f"{t3_caught}/20")

    # 5. the decider on synthetic measures with known answers
    L = F(3)
    for rho, thr, expect in ((F(101, 100), F(1), "ACCEPT"), (F(1001, 1000), F(1001, 1000) + F(1, 10**6), "REFUSED_EXACT")):
        mu = {(F(0), F(0), L, L): rho * 9}
        prep = {"L": L, "merged": mu, "lat": C.lattice(mu, L), "n": 9}
        step = C.TSTAR / 40
        bins = [(40, r, (r - F(1, 2)) * step, (r + F(1, 2)) * step) for r in range(0, 41, 8)]
        res = D.decide(exe, prep, bins, thr, scr, 2, 2)
        top = {r["verdict"] for r in res if r["depth"] == 0 or r["verdict"] != "SPLIT"} - {"SPLIT"}
        check(f"uniform_{expect}", top == {expect} if expect == "REFUSED_EXACT" else top <= {"ACCEPT"}, str(top))
    mu = synthetic_measure(rng, L, 40, thin=False)
    lat = C.lattice(mu, L)
    prep = {"L": L, "merged": mu, "lat": lat, "n": 9}
    C.write_rects(lat, scr / "rects.txt")
    import rr1_search as S  # noqa: PLC0415

    found = S.fsearch(exe, scr / "rects.txt", scr, lat["Q"], L, S.ANGLES_T, 21, 8)
    found.sort(key=lambda r: r[3])
    ex = sorted((S.exact_pose(mu, L, *r[:3]) for r in found[:4]), key=lambda e: F(e["capture"]))
    m_star = F(ex[0]["capture"])
    t_star = F(ex[0]["t"])
    step = C.TSTAR / 80
    r_star = int(t_star / step + F(1, 2))
    b_star = [(80, r_star, (r_star - F(1, 2)) * step, (r_star + F(1, 2)) * step)]
    res = D.decide(exe, prep, b_star, m_star + F(1, 10**4), scr, 1, 1)
    check("synthetic_refused_above_least", D.summarize(res) == "REFUSED_EXACT", D.summarize(res))
    allb = [(80, r, (r - F(1, 2)) * step, (r + F(1, 2)) * step) for r in range(0, 81, 10)]
    res = D.decide(exe, prep, allb, m_star - F(2, 100), scr, 2, 2)
    check("synthetic_accepted_below_least", D.summarize(res) == "DECIDED", D.summarize(res))
    nodes = sum(r["nodes"] for r in res)

    result = {
        "program": "rr1_selftest.py",
        "verdict": "PASS" if not FAILS else "FAIL",
        "failures": FAILS,
        "checks": COUNTS,
        "synthetic_least": float(m_star),
        "synthetic_nodes": nodes,
    }
    Path(a.out).write_text(json.dumps(result, indent=1) + "\n")
    print(result["verdict"], FAILS[:5], sum(COUNTS.values()), "checks")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
