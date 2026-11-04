"""Self-test of ozlib's two methods on cases whose answers are known by hand, and at random.

Usage: oz_selftest.py OUT.json [SEED]

Known cases: edge, corner and vertex-edge contacts and their 10^-30 overlaps; a duplicate;
the overlap of a unit square with its own rotation by basis (3/5, 4/5), which is
1 - t(1 - t)/(1 + t) = 5/6 at t = tan(theta/2) = 1/2; axis-parallel offsets with areas
known in closed form; walls at contact and 10^-30 past; a non-unit basis.
Random cases: pairs with rational half-angle bases, decided by both methods, then closed
to exact contact along the centre line (margin must be exactly 0, area exactly 0), and
10^-30 past it (both must see an overlap) and 10^-30 short of it (both must see none).
"""

from __future__ import annotations

import json
import platform
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ozlib as oz  # noqa: E402

EPS = Fraction(1, 10**30)


def mk(x, y, a, b, s=Fraction(1)):
    F = (Fraction(x), Fraction(y), Fraction(a), Fraction(b), Fraction(s))
    return {"id": 0, "F": F, "Q": tuple(oz.F_to_Q(v) for v in F)}


def both(P, Q):
    m, _ = oz.sat_margin_F(P["F"], Q["F"])
    area = oz.Q_to_F(oz.overlap_area_Q(oz.corners_Q(P["Q"]), oz.corners_Q(Q["Q"])))
    return m, area


def half_angle(t: Fraction):
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def main() -> int:
    out_p = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261104
    t0 = time.process_time()
    rows = []

    def case(name, P, Q, want_margin=None, want_area=None, want_overlap=None):
        m, area = both(P, Q)
        ok = True
        if want_margin is not None:
            ok &= m == want_margin
        if want_area is not None:
            ok &= area == want_area
        if want_overlap is not None:
            ok &= (m < 0) == want_overlap and (area > 0) == want_overlap
        ok &= (m < 0) == (area > 0)
        rows.append({"case": name, "margin": oz.frac_str(m), "area": oz.frac_str(area), "ok": bool(ok)})

    h = Fraction(1, 2)
    A = mk(h, h, 1, 0)
    case("edge contact", A, mk(Fraction(3, 2), h, 1, 0), 0, 0, False)
    case("edge 1e-30 overlap", A, mk(Fraction(3, 2) - EPS, h, 1, 0), -EPS, EPS, True)
    case("edge 1e-30 gap", A, mk(Fraction(3, 2) + EPS, h, 1, 0), EPS, 0, False)
    case("corner contact", A, mk(Fraction(3, 2), Fraction(3, 2), 1, 0), 0, 0, False)
    case("corner 1e-30 overlap", A, mk(Fraction(3, 2) - EPS, Fraction(3, 2) - EPS, 1, 0), -EPS, EPS * EPS, True)
    case("duplicate", A, mk(h, h, 1, 0), -1, 1, True)
    case("offset (1/4, 1/2)", A, mk(h + Fraction(1, 4), h + Fraction(1, 2), 1, 0), None, Fraction(3, 8), True)
    case("same square rotated by (3/5, 4/5) about its centre", A, mk(h, h, Fraction(3, 5), Fraction(4, 5)), None, Fraction(5, 6), True)
    case("same square rotated by (4/5, 3/5) about its centre", A, mk(h, h, Fraction(4, 5), Fraction(3, 5)), None, Fraction(5, 6), True)
    # Vertex of a (3/5, 4/5) square on the edge x = 1 of A at y = 2/5: half-width along x is 7/10.
    case("vertex-edge contact", A, mk(Fraction(17, 10), h, Fraction(3, 5), Fraction(4, 5)), 0, 0, False)
    case("vertex-edge 1e-30 overlap", A, mk(Fraction(17, 10) - EPS, h, Fraction(3, 5), Fraction(4, 5)), -EPS, None, True)
    # Two (3/5, 4/5) squares in edge contact along their own axis u.
    a, b = Fraction(3, 5), Fraction(4, 5)
    case("rotated edge contact", mk(0, 0, a, b), mk(a, b, a, b), 0, 0, False)
    case("rotated edge 1e-30 overlap", mk(0, 0, a, b), mk(a * (1 - EPS), b * (1 - EPS), a, b), -EPS, EPS, True)

    # Walls.
    wall_rows = []

    def wcase(name, sq, S, inside):
        c1 = oz.wall_clearances_F(sq["F"], Fraction(S))
        cor = oz.corners_Q(sq["Q"])
        c2 = oz.wall_clearances_Q(cor, oz.F_to_Q(Fraction(S)))
        ins, _, _ = oz.contained_by_area_Q(cor, oz.F_to_Q(Fraction(S)))
        m1 = all(c >= 0 for c in c1)
        m2 = all(c >= 0 for c in c2) and ins
        wall_rows.append({"case": name, "m1_inside": m1, "m2_inside": m2,
                          "ok": m1 == inside and m2 == inside and all(oz.F_to_Q(p) == q for p, q in zip(c1, c2))})

    wcase("unit square in the unit box", A, 1, True)
    wcase("unit square in a box 1e-30 short", A, 1 - EPS, False)
    wcase("(3/5, 4/5) square touching all four walls of a 7/5 box", mk(Fraction(7, 10), Fraction(7, 10), a, b), Fraction(7, 5), True)
    wcase("the same 1e-30 short", mk(Fraction(7, 10), Fraction(7, 10), a, b), Fraction(7, 5) - EPS, False)
    wcase("the same moved 1e-30 left", mk(Fraction(7, 10) - EPS, Fraction(7, 10), a, b), Fraction(7, 5), False)

    shape = {"non-unit basis (3/5, 4/5 + 1e-30) refused": (a * a + (b + EPS) ** 2 != 1)
             and oz.area2(oz.corners_Q(mk(h, h, a, b + EPS)["Q"])) != 2}

    # Random pairs.
    rng = random.Random(seed)
    stats = {"pairs": 0, "agree": 0, "contact_margin_0": 0, "contact_area_0": 0,
             "past_both_overlap": 0, "short_both_disjoint": 0}
    for _ in range(3000):
        t1 = Fraction(rng.randint(-10**6, 10**6), rng.randint(1, 10**6))
        t2 = Fraction(rng.randint(-10**6, 10**6), rng.randint(1, 10**6))
        a1, b1 = half_angle(t1)
        a2, b2 = half_angle(t2)
        x = Fraction(rng.randint(-2 * 10**9, 2 * 10**9), 10**9)
        y = Fraction(rng.randint(-2 * 10**9, 2 * 10**9), 10**9)
        P = mk(0, 0, a1, b1)
        Q = mk(x, y, a2, b2)
        m, area = both(P, Q)
        stats["pairs"] += 1
        stats["agree"] += (m < 0) == (area > 0)
        if x == 0 and y == 0:
            continue
        # contact along the centre line
        lam = None
        for da, db in ((a1, b1), (-b1, a1), (a2, b2), (-b2, a2)):
            ak = abs(x * da + y * db)
            hk = oz.halfwidth_F(P["F"], da, db) + oz.halfwidth_F(Q["F"], da, db)
            if ak:
                v = hk / ak
                lam = v if lam is None or v < lam else lam
        for lv, key in ((lam, "contact"), (lam - EPS, "past"), (lam + EPS, "short")):
            Qm = mk(lv * x, lv * y, a2, b2)
            mm, aa = both(P, Qm)
            if key == "contact":
                stats["contact_margin_0"] += mm == 0
                stats["contact_area_0"] += aa == 0
            elif key == "past":
                stats["past_both_overlap"] += mm < 0 and aa > 0
            else:
                stats["short_both_disjoint"] += mm > 0 and aa == 0
    random_ok = (stats["agree"] == stats["pairs"]
                 and stats["contact_margin_0"] == stats["contact_area_0"] == stats["past_both_overlap"]
                 == stats["short_both_disjoint"] == stats["pairs"])

    ok = all(r["ok"] for r in rows) and all(r["ok"] for r in wall_rows) and all(shape.values()) and random_ok
    receipt = {
        "program": "oz_selftest.py",
        "program_sha256": oz.sha256_file(__file__),
        "ozlib_sha256": oz.sha256_file(HERE / "ozlib.py"),
        "python": platform.python_version(),
        "gmpy2": oz.gmpy2_version(),
        "seed": seed,
        "pair_cases": rows,
        "wall_cases": wall_rows,
        "shape_cases": shape,
        "random": stats,
        "verdict": "PASSED" if ok else "FAILED",
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    Path(out_p).write_text(json.dumps(receipt, indent=1) + "\n")
    print(f"selftest {receipt['verdict']}: {len(rows)} pair cases, {len(wall_rows)} wall cases, random {stats}; "
          f"cpu {receipt['cpu_seconds']} s")
    for r in rows + wall_rows:
        if not r["ok"]:
            print("  FAIL", r)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
