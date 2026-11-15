"""Lane L169 self-test: both methods and the reader against cases with hand-derived answers.

Usage: l169_selftest.py OUT_JSON

Every expected margin, class and area below is derived by hand in the comments, not from
either method. The test passes when the real methods meet every case, and each of three
deliberately broken copies fails some: method A using only square i's two normals,
method A counting a zero margin as apart, and method B clipping with open half-planes.
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves it off

import l169_clip as clipm
import l169_decide as dec
import l169_geom as geom
import l169_reader as rd
import l169_sat as sat

EPS = F(1, 10**30)
DELTAS = (EPS, F(0), -EPS)


def rf(f: F) -> tuple[int, int]:
    f = F(f)
    return (f.numerator, f.denominator)


def cls(m: F) -> str:
    return "apart" if m > 0 else ("contact" if m == 0 else "overlap")


def wcls(c: F) -> str:
    return "clear" if c > 0 else ("contact" if c == 0 else "crossing")


class Tally:
    def __init__(self) -> None:
        self.cases = 0
        self.fail: list[str] = []
        self.broken = {"A_only_i_normals": 0, "A_zero_is_apart": 0, "B_open_half_planes": 0}

    def check(self, ok: bool, what: str) -> None:
        if not ok:
            self.fail.append(what)


def a_margin_only_i(si: sat.Square, sj: sat.Square) -> F:
    g, den = sat.pair_gaps(si, sj)
    return F(max(g[0], g[1]), den)


def a_class_zero_apart(m: F) -> str:
    return "apart" if m >= 0 else "overlap"


def pair_case(T: Tally, name: str, ci: tuple[F, F], ti: F, cj: tuple[F, F], tj: F,
              exp_m: F, exp_area: F) -> None:
    """One pair under every equivalent half-angle of each square, in both orders."""
    exp_c = cls(exp_m)
    for tia in geom.t_equivalents(ti):
        for tja in geom.t_equivalents(tj):
            for (c1, t1), (c2, t2) in (((ci, tia), (cj, tja)), ((cj, tja), (ci, tia))):
                T.cases += 1
                r1 = (rf(c1[0]), rf(c1[1]), rf(t1))
                r2 = (rf(c2[0]), rf(c2[1]), rf(t2))
                s1, s2 = sat.Square(*r1), sat.Square(*r2)
                m = sat.pair_margin(s1, s2)
                tag = f"{name} t=({t1},{t2})"
                T.check(m == exp_m, f"A margin {tag}: {m} != {exp_m}")
                T.check(sat.classify(m) == exp_c, f"A class {tag}")
                gm = geom.margin(geom.sq_of(c1[0], c1[1], t1), geom.sq_of(c2[0], c2[1], t2))
                T.check(gm == exp_m, f"geom margin {tag}: {gm} != {exp_m}")
                b1, b2 = clipm.corners(*r1), clipm.corners(*r2)
                kb, area = clipm.pair_class(b1, b2)
                T.check(kb == exp_c, f"B class {tag}: {kb} != {exp_c}")
                T.check(F(int(area.numerator), int(area.denominator)) == exp_area,
                        f"B area {tag}: {area} != {exp_area}")
                if a_margin_only_i(s1, s2) != exp_m:
                    T.broken["A_only_i_normals"] += 1
                if a_class_zero_apart(m) != exp_c:
                    T.broken["A_zero_is_apart"] += 1
                kbo, _ = clipm.pair_class(b1, b2, closed=False)
                if kbo != exp_c:
                    T.broken["B_open_half_planes"] += 1


def wall_case(T: Tally, name: str, cx: F, cy: F, t: F, side: F, exp: dict[str, F]) -> None:
    for ta in geom.t_equivalents(t):
        T.cases += 1
        row = (rf(cx), rf(cy), rf(ta))
        s = sat.Square(*row)
        ca = sat.clearances(s, rf(side))
        cg = geom.clearances(geom.sq_of(cx, cy, ta), side)
        b = clipm.corners(*row)
        tag = f"{name} t={ta}"
        for w, v in exp.items():
            T.check(ca[w] == v, f"A clearance {w} {tag}: {ca[w]} != {v}")
            T.check(cg[w] == v, f"geom clearance {w} {tag}")
            kb, _ = clipm.wall_class(b, w, rf(side))
            T.check(kb == wcls(v), f"B wall {w} {tag}: {kb} != {wcls(v)}")
            kbo, _ = clipm.wall_class(b, w, rf(side), closed=False)
            if kbo != wcls(v):
                T.broken["B_open_half_planes"] += 1
        inside = all(v >= 0 for v in ca.values())
        ain = clipm.area_in_box(b, rf(side))
        T.check((ain == 1) == inside, f"B containment {tag}: area {ain}, inside {inside}")


def run_pairs(T: Tally) -> None:
    ci = (F(7, 3), F(5, 7))
    rot = {F(0): ((F(1), F(0)), (F(0), F(1))),
           F(1, 2): ((F(3, 5), F(4, 5)), (F(-4, 5), F(3, 5))),
           F(2, 3): ((F(5, 13), F(12, 13)), (F(-12, 13), F(5, 13)))}
    for t, (u, v) in rot.items():
        dirs = [u, v, (-u[0], -u[1]), (-v[0], -v[1])]
        # Edge to edge: j = i + (1 + d) e + o p, p the edge direction; the gap on e's
        # normal is d, on p's it is o - 1 < 0; overlap for d < 0 is |d| (1 - o).
        for e in dirs:
            p = (-e[1], e[0])
            for o in (F(0), F(1, 3)):
                for d in DELTAS:
                    cj = (ci[0] + (1 + d) * e[0] + o * p[0], ci[1] + (1 + d) * e[1] + o * p[1])
                    area = -d * (1 - o) if d < 0 else F(0)
                    pair_case(T, f"edge t={t} e={e} o={o} d={d}", ci, t, cj, t, d, area)
        # Corner to corner: j = i + (1 + d)(+-u +- v); the gap is d on both normals and
        # the overlap a d by d square.
        for su in (1, -1):
            for sv in (1, -1):
                e = (su * u[0] + sv * v[0], su * u[1] + sv * v[1])
                for d in DELTAS:
                    cj = (ci[0] + (1 + d) * e[0], ci[1] + (1 + d) * e[1])
                    pair_case(T, f"corner t={t} e={e} d={d}", ci, t, cj, t, d,
                              d * d if d < 0 else F(0))
    # A turned corner on an upright edge: j turned by (3/5, 4/5) or (4/5, 3/5) has
    # half-extent 7/10, so at i + (6/5 + d, 0) its corner meets i's edge at d; past it the
    # corner triangle has legs (5/3)|d| and (5/4)|d|, area 25 d^2 / 24. Each quarter turn
    # of the plane maps the pair to a congruent one with the same t (a square is its own
    # quarter turn).
    for tj in (F(1, 2), F(1, 3)):
        for k in range(4):
            for d in DELTAS:
                x, y = F(6, 5) + d, F(0)
                for _ in range(k):
                    x, y = -y, x
                cj = (ci[0] + x, ci[1] + y)
                pair_case(T, f"turned-corner tj={tj} k={k} d={d}", ci, F(0), cj, tj, d,
                          F(25, 24) * d * d if d < 0 else F(0))
    # Duplicates: margin 0 - 1/2 - 1/2 = -1, area 1.
    for t in (F(0), F(1, 2), F(2, 3), F(-1, 3)):
        pair_case(T, f"duplicate t={t}", ci, t, ci, t, F(-1), F(1))
    # Concentric, upright against (3/5, 4/5) or (4/5, 3/5): margin -1/2 - 7/10 = -6/5;
    # each turned corner pokes out by 1/5 with legs 1/3 and 1/4, so the intersection is
    # 1 - 4/24 = 5/6.
    for tj in (F(1, 2), F(1, 3)):
        pair_case(T, f"concentric tj={tj}", ci, F(0), ci, tj, F(-6, 5), F(5, 6))


CERT_TS = (F(-20267519227291, 100000000000000), F(-11062871348759, 50000000000000))


def run_walls(T: Tally) -> None:
    side = F(3)
    for t in (F(0), F(1, 2), F(1, 3), F(-2, 3), EPS, *CERT_TS):
        c, s = geom.cs_of_t(t)
        h = (abs(c) + abs(s)) / 2
        mid = side / 2
        far = side / 2 - h  # clearance at the opposite and side walls when centred
        for d in DELTAS:
            wall_case(T, f"left d={d}", h + d, mid, t, side,
                      {"left": d, "right": side - 2 * h - d, "bottom": far, "top": far})
            wall_case(T, f"right d={d}", side - h - d, mid, t, side,
                      {"right": d, "left": side - 2 * h - d, "bottom": far, "top": far})
            wall_case(T, f"bottom d={d}", mid, h + d, t, side,
                      {"bottom": d, "top": side - 2 * h - d, "left": far, "right": far})
            wall_case(T, f"top d={d}", mid, side - h - d, t, side,
                      {"top": d, "bottom": side - 2 * h - d, "left": far, "right": far})


def run_units(T: Tally) -> None:
    for t in (F(0), F(1, 2), F(-2, 3), EPS, *CERT_TS):
        T.cases += 1
        row = ((0, 1), (0, 1), rf(t))
        T.check(sat.Square(*row).is_unit(), f"A unit t={t}")
        u, c = clipm.is_unit_ccw(clipm.corners(*row))
        T.check(u and c, f"B unit and ccw t={t}")
    for a, b, r in ((3, 4, 6), (0, 0, 0), (1, 1, 1)):
        T.cases += 1
        s = sat.Square((0, 1), (0, 1), (0, 1))
        s.a, s.b, s.r = a, b, r
        T.check(not s.is_unit(), f"A must refuse ({a},{b},{r})")
    q = clipm.mpq
    e = q(1, 10**30)
    shapes = {
        "rectangle 1 by 1+e": [(q(0), q(0)), (q(1), q(0)), (q(1), 1 + e), (q(0), 1 + e)],
        "square of side 2": [(q(0), q(0)), (q(2), q(0)), (q(2), q(2)), (q(0), q(2))],
        "unit rhombus": [(q(0), q(0)), (q(1), q(0)), (q(8, 5), q(4, 5)), (q(3, 5), q(4, 5))],
        "unit square clockwise": [(q(0), q(0)), (q(0), q(1)), (q(1), q(1)), (q(1), q(0))],
        "unit square out of cyclic order": [(q(0), q(0)), (q(1), q(1)), (q(1), q(0)), (q(0), q(1))],
        "kite": [(q(0), q(0)), (q(1), q(0)), (q(1), q(1)), (-e, 1 + e)],
        "one point four times": [(q(0), q(0))] * 4,
    }
    for name, pts in shapes.items():
        T.cases += 1
        u, c = clipm.is_unit_ccw(pts)
        T.check(not (u and c), f"B must refuse {name}")


def run_random(T: Tally) -> None:
    rng = random.Random(169)

    def rt() -> F:
        return F(rng.randint(-60, 60), rng.randint(1, 60))

    def rc() -> F:
        return F(rng.randint(0, 3 * 97), 97) + F(rng.randint(0, 50), 1009)

    for k in range(300):
        T.cases += 1
        ci, cj = (rc(), rc()), (rc(), rc())
        ti, tj = rt(), rt()
        ri = (rf(ci[0]), rf(ci[1]), rf(ti))
        rj = (rf(cj[0]), rf(cj[1]), rf(tj))
        m = sat.pair_margin(sat.Square(*ri), sat.Square(*rj))
        gm = geom.margin(geom.sq_of(ci[0], ci[1], ti), geom.sq_of(cj[0], cj[1], tj))
        T.check(m == gm, f"random {k}: A {m} != closed form {gm}")
        b1, b2 = clipm.corners(*ri), clipm.corners(*rj)
        kb, a1 = clipm.pair_class(b1, b2)
        kb2, a2 = clipm.pair_class(b2, b1)
        T.check(kb == cls(gm) and kb2 == kb and a1 == a2, f"random {k}: B {kb}/{kb2} vs {cls(gm)}")
    done = 0
    while done < 300:
        ci, cj = (rc(), rc()), (rc(), rc())
        ti, tj = rt(), rt()
        qi, qj = geom.sq_of(ci[0], ci[1], ti), geom.sq_of(cj[0], cj[1], tj)
        try:
            taus = [geom.close_time(qi, qj, target) for target in (EPS, F(0), -EPS)]
        except ValueError:
            continue
        done += 1
        for target, tau in zip((EPS, F(0), -EPS), taus, strict=True):
            T.cases += 1
            mj = geom.moved_toward(qi, qj, tau)
            ri = (rf(ci[0]), rf(ci[1]), rf(ti))
            rj = (rf(mj[0]), rf(mj[1]), rf(tj))
            m = sat.pair_margin(sat.Square(*ri), sat.Square(*rj))
            gm = geom.margin(qi, mj)
            T.check(m == target and gm == target, f"closing {done}: A {m}, closed form {gm}, target {target}")
            kb, _ = clipm.pair_class(clipm.corners(*ri), clipm.corners(*rj))
            T.check(kb == cls(target), f"closing {done}: B {kb} vs {cls(target)}")
            if a_class_zero_apart(m) != cls(target):
                T.broken["A_zero_is_apart"] += 1
            kbo, _ = clipm.pair_class(clipm.corners(*ri), clipm.corners(*rj), closed=False)
            if kbo != cls(target):
                T.broken["B_open_half_planes"] += 1
    side = F(4)
    for k in range(300):
        t = rt()
        q0 = geom.sq_of(F(rng.randint(80, 320), 100), F(rng.randint(80, 320), 100), t)
        w = rng.choice(dec.WALLS)
        c0 = geom.clearances(q0, side)[w]
        for target in (EPS, F(0), -EPS):
            T.cases += 1
            q1 = geom.moved_to_wall(q0, w, c0 - target)
            row = (rf(q1[0]), rf(q1[1]), rf(t))
            ca = sat.clearances(sat.Square(*row), rf(side))[w]
            T.check(ca == target, f"random wall {k} {w}: A {ca} vs {target}")
            kb, _ = clipm.wall_class(clipm.corners(*row), w, rf(side))
            T.check(kb == wcls(target), f"random wall {k} {w}: B {kb} vs {wcls(target)}")


VALID = b"2 3\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n"
MALFORMED = {
    "empty": b"",
    "last line not terminated": b"2 3\r\n1/2 1/2 0\r\n3/2 1/2 0",
    "mixed terminators": b"2 3\r\n1/2 1/2 0\n3/2 1/2 0\r\n",
    "header of three tokens": b"2 3 1\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n",
    "n zero": b"0 3\r\n",
    "n a fraction": b"2/3 3\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n",
    "n with a leading zero": b"02 3\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n",
    "side negative": b"2 -3\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n",
    "side zero": b"2 0\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n",
    "side not in lowest terms": b"2 6/2\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n",
    "row of two tokens": b"2 3\r\n1/2 1/2\r\n3/2 1/2 0\r\n",
    "row of four tokens": b"2 3\r\n1/2 1/2 0 0\r\n3/2 1/2 0\r\n",
    "double space": b"2 3\r\n1/2  1/2 0\r\n3/2 1/2 0\r\n",
    "trailing space": b"2 3\r\n1/2 1/2 0 \r\n3/2 1/2 0\r\n",
    "numerator with a leading zero": b"2 3\r\n01/2 1/2 0\r\n3/2 1/2 0\r\n",
    "denominator with a leading zero": b"2 3\r\n1/02 1/2 0\r\n3/2 1/2 0\r\n",
    "zero denominator": b"2 3\r\n1/0 1/2 0\r\n3/2 1/2 0\r\n",
    "integer written over 1": b"2 3\r\n1/2 1/2 0/1\r\n3/2 1/2 0\r\n",
    "signed zero": b"2 3\r\n1/2 1/2 -0\r\n3/2 1/2 0\r\n",
    "plus sign": b"2 3\r\n+1/2 1/2 0\r\n3/2 1/2 0\r\n",
    "decimal": b"2 3\r\n0.5 1/2 0\r\n3/2 1/2 0\r\n",
    "exponent": b"2 3\r\n5e-1 1/2 0\r\n3/2 1/2 0\r\n",
    "non-ASCII byte": b"2 3\r\n1/2 1/2 0\xc2\xa0\r\n3/2 1/2 0\r\n",
    "tab separator": b"2 3\r\n1/2\t1/2 0\r\n3/2 1/2 0\r\n",
    "header 2, three rows": b"2 3\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n5/2 1/2 0\r\n",
    "header 3, two rows": b"3 3\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n",
    "blank last line": b"2 3\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n\r\n",
    "comment line": b"# a comment\r\n2 3\r\n1/2 1/2 0\r\n3/2 1/2 0\r\n",
    "negative denominator": b"2 3\r\n1/-2 1/2 0\r\n3/2 1/2 0\r\n",
    "zero written as a fraction": b"2 3\r\n1/2 1/2 0/3\r\n3/2 1/2 0\r\n",
}


def run_reader(T: Tally) -> None:
    for name, raw in MALFORMED.items():
        T.cases += 1
        try:
            rd.read_text(raw)
            T.check(False, f"reader accepted: {name}")
        except rd.ReadError:
            pass
    T.cases += 2
    a = rd.read_text(VALID)
    b = rd.read_text(VALID.replace(b"\r\n", b"\n"))
    T.check(a["squares"] == b["squares"] and a["side"] == b["side"] and a["n"] == 2,
            "valid CRLF and LF texts read equal")
    T.check(rd.write_text(a) == VALID, "canonical text round trip")


def run_files(T: Tally) -> None:
    def rdg(side: F, rows: list[tuple[F, F, F]]) -> dict:
        return {"n": len(rows), "side": rf(side), "squares": [tuple(rf(v) for v in r) for r in rows]}

    h = F(7, 10)
    cases = [
        ("duplicate", rdg(F(3), [(F(1), F(1), F(0)), (F(1), F(1), F(0))]), "REFUSE", {"overlapping_pairs": [(1, 2)]}),
        ("square 1e-30 outside", rdg(F(3), [(F(1, 2) - EPS, F(1), F(0))]), "REFUSE", {"wall_crossings": [(1, "left")]}),
        ("edge contact", rdg(F(2), [(F(1, 2), F(1, 2), F(0)), (F(3, 2), F(1, 2), F(0))]), "ACCEPT", {"touching_pairs": [(1, 2)]}),
        ("turned square at two walls", rdg(F(2), [(h, h, F(1, 2))]), "ACCEPT", {"wall_contacts": [(1, "left"), (1, "bottom")]}),
    ]
    for name, reading, verdict, facts in cases:
        T.cases += 1
        res = dec.decide(reading, keep_lists=False)
        T.check(res["verdict"] == verdict, f"file {name}: {res['verdict']} != {verdict}")
        for k, v in facts.items():
            T.check(res[k] == v, f"file {name}: {k} {res[k]} != {v}")


def main(argv: list[str]) -> int:
    t0 = time.process_time()
    T = Tally()
    run_pairs(T)
    run_walls(T)
    run_units(T)
    run_random(T)
    run_reader(T)
    run_files(T)
    broken_ok = all(v > 0 for v in T.broken.values())
    status = "PASSED" if not T.fail and broken_ok else "FAILED"
    out = {
        "program": "l169_selftest.py",
        "status": status,
        "cases": T.cases,
        "failures": len(T.fail),
        "first_failures": T.fail[:20],
        "broken_copies_failures": T.broken,
        "every_broken_copy_fails": broken_ok,
        "python": sys.version.split()[0],
        "gmp": clipm.gmp_version(),
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    with open(argv[1], "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(f"{status} {T.cases} cases {len(T.fail)} failed; broken copies {T.broken}")
    for f in T.fail[:10]:
        print("  ", f)
    return 0 if status == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
