"""Self-test of the readers, both methods, the closed form, the decision, the twin
comparison and the contraction, on synthetic cases whose answers are derived by hand.

Lane r127-1118.  Written for this review; imports only its own modules.

    python -I -B r127_selftest.py --out OUT.json

Exit status 0 when every check passes.  r127_mutants.py runs this file against broken
copies of the programs, each of which must fail at least one check.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir

import argparse
import json
import random
import sys
import time
from fractions import Fraction

import r127_area as B
import r127_axes as A
import r127_contract as K
import r127_decide as D
import r127_frame as F
import r127_read as R
import r127_synth as Y
import r127_twin as T

FAILS: list[str] = []
COUNT = [0]
E30 = Fraction(1, 10**30)
DIRS = [(Fraction(1), Fraction(0)), (Fraction(3, 5), Fraction(4, 5)),
        (Fraction(5, 13), Fraction(12, 13)), (Fraction(8, 17), Fraction(15, 17)),
        (Fraction(20, 29), Fraction(21, 29))]


def check(cond: bool, what: str) -> None:
    COUNT[0] += 1
    if not cond:
        FAILS.append(what)


def rot(p, u):
    a, b = u
    return (a * p[0] - b * p[1], b * p[0] + a * p[1])


def sq(c, u):
    return R.centre_corners(c, u)


def pairA(P, Q):
    return A.margin(A.prepare(P), A.prepare(Q))


def pairB(P, Q):
    return B.pair_class(B.ccw(B.to_mpq(P)), B.ccw(B.to_mpq(Q)))


def clip_area(P, Q):
    """Sutherland-Hodgman clipping of P by Q, in Fractions; an algorithm method B does
    not use, for comparison only."""
    out = list(P)
    k = len(Q)
    for i in range(k):
        a, b = Q[i], Q[(i + 1) % k]
        inp, out = out, []
        if not inp:
            break
        def side(p, a=a, b=b):
            return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        for j in range(len(inp)):
            cur, prv = inp[j], inp[j - 1]
            sc, sp = side(cur), side(prv)
            if sc >= 0:
                if sp < 0:
                    t = sp / (sp - sc)
                    out.append((prv[0] + t * (cur[0] - prv[0]), prv[1] + t * (cur[1] - prv[1])))
                out.append(cur)
            elif sp >= 0:
                t = sp / (sp - sc)
                out.append((prv[0] + t * (cur[0] - prv[0]), prv[1] + t * (cur[1] - prv[1])))
    s = Fraction(0)
    for j in range(len(out)):
        s += out[j][0] * out[(j + 1) % len(out)][1] - out[(j + 1) % len(out)][0] * out[j][1]
    return abs(s) / 2


def mpq_frac(q):
    return Fraction(int(q.numerator), int(q.denominator))


def test_edge_contacts():
    half = Fraction(1, 2)
    for u in DIRS:
        for tau in (Fraction(0), Fraction(1, 3), Fraction(2, 3)):
            for delta in (E30, Fraction(0), -E30, Fraction(1, 7), -Fraction(1, 7)):
                for flip in (1, -1):
                    c1 = (half, half)
                    c2 = (half + flip * (1 + delta), half + tau)
                    P = [rot(p, u) for p in sq(c1, (Fraction(1), Fraction(0)))]
                    Q = [rot(p, u) for p in sq(c2, (Fraction(1), Fraction(0)))]
                    shift = (Fraction(7, 3), Fraction(-5, 11))
                    P = [(x + shift[0], y + shift[1]) for x, y in P]
                    Q = [(x + shift[0], y + shift[1]) for x, y in Q]
                    m1, m2 = pairA(P, Q), pairA(Q, P)
                    check(m1 == delta and m2 == delta, f"edge contact margin u={u} tau={tau} d={delta}")
                    cf = F.pair_margin(F.frame_of_corners(P)[0], F.frame_of_corners(P)[1],
                                       F.frame_of_corners(Q)[0], F.frame_of_corners(Q)[1])
                    check(cf == delta, f"edge contact closed form u={u} d={delta}")
                    cl, area = pairB(P, Q)
                    want = "apart" if delta > 0 else ("contact" if delta == 0 else "overlap")
                    check(cl == want, f"edge contact class B u={u} tau={tau} d={delta}: {cl}")
                    if delta < 0:
                        check(mpq_frac(area) == -delta * (1 - tau), f"edge overlap area u={u} tau={tau}")
                    # listing from each corner in both senses
                    for s0 in range(4):
                        Q2 = Q[s0:] + Q[:s0]
                        Q3 = list(reversed(Q2))
                        check(pairA(P, Q3) == delta if A.prepare(Q3).unit else False,
                              f"listing invariance A u={u} s0={s0}")
                        check(pairB(P, Q2)[0] == want, f"listing invariance B u={u} s0={s0}")
                # corner to corner along the diagonal
                for delta in (E30, Fraction(0), -E30):
                    P = [rot(p, u) for p in sq((half, half), (Fraction(1), Fraction(0)))]
                    Q = [rot(p, u) for p in sq((half + 1 + delta, half + 1 + delta), (Fraction(1), Fraction(0)))]
                    check(pairA(P, Q) == delta, f"corner contact margin u={u} d={delta}")
                    cl, area = pairB(P, Q)
                    want = "apart" if delta > 0 else ("contact" if delta == 0 else "overlap")
                    check(cl == want, f"corner contact class u={u} d={delta}")
                    if delta < 0:
                        check(mpq_frac(area) == delta * delta, f"corner overlap area u={u}")


def test_tilted_corner():
    expected = {(Fraction(4, 5), Fraction(3, 5)): Fraction(25, 24),
                (Fraction(12, 13), Fraction(5, 13)): Fraction(169, 120),
                (Fraction(15, 17), Fraction(8, 17)): Fraction(289, 240)}
    for u, k in expected.items():
        h = (u[0] + u[1]) / 2
        for delta in (E30, Fraction(0), -E30, -Fraction(1, 100)):
            P = sq((Fraction(1, 2), Fraction(1, 2)), (Fraction(1), Fraction(0)))
            Q = sq((1 + h + delta, Fraction(1, 2)), u)
            check(pairA(P, Q) == delta and pairA(Q, P) == delta, f"tilted corner margin {u} {delta}")
            cl, area = pairB(P, Q)
            want = "apart" if delta > 0 else ("contact" if delta == 0 else "overlap")
            check(cl == want, f"tilted corner class {u} {delta}")
            if delta < 0:
                check(mpq_frac(area) == k * delta * delta, f"tilted corner area {u} {delta}")


def test_concentric_and_duplicate():
    c = (Fraction(3, 2), Fraction(5, 2))
    P = sq(c, (Fraction(1), Fraction(0)))
    check(pairA(P, P) == -1, "duplicate margin -1")
    cl, area = pairB(P, P)
    check(cl == "overlap" and area == 1, "duplicate area 1")
    for u, want_m, want_a in (((Fraction(3, 5), Fraction(4, 5)), -Fraction(6, 5), Fraction(5, 6)),
                              ((Fraction(5, 13), Fraction(12, 13)), -Fraction(15, 13), Fraction(13, 15))):
        Q = sq(c, u)
        check(pairA(P, Q) == want_m, f"concentric margin {u}")
        cl, area = pairB(P, Q)
        check(cl == "overlap" and mpq_frac(area) == want_a, f"concentric area {u}: {area}")


def test_walls():
    S = Fraction(5)
    for u in DIRS:
        a, b = u
        h = (a + b) / 2
        for delta in (E30, Fraction(0), -E30, -Fraction(1, 100)):
            cases = {0: (h + delta, S / 2), 1: (S / 2, h + delta), 2: (S - h - delta, S / 2),
                     3: (S / 2, S - h - delta)}
            for wall, c in cases.items():
                P = sq(c, u)
                cl = A.walls(A.prepare(P), S)
                check(cl[wall] == delta, f"wall clearance A {u} wall {wall} {delta}")
                cls, inside = B.wall_classes(B.ccw(B.to_mpq(P)), B.mpq(5))
                want = "clear" if delta > 0 else ("touch" if delta == 0 else "cross")
                check(cls[wall] == want, f"wall class B {u} wall {wall} {delta}: {cls[wall]}")
                if delta >= 0:
                    check(inside == 1, f"inside area 1 {u} {wall}")
                else:
                    out = (-delta) if b == 0 else delta * delta / (2 * a * b)
                    check(mpq_frac(inside) == 1 - out, f"inside area {u} wall {wall} {delta}")
                cc = F.clearances(c, u, S)
                check(cc[wall] == delta, f"wall clearance closed form {u} {wall}")


def test_unit_tests():
    half = Fraction(1, 2)
    for u in DIRS:
        P = sq((half, half), u)
        for s0 in range(4):
            for rev in (False, True):
                Q = P[s0:] + P[:s0]
                if rev:
                    Q = list(reversed(Q))
                sa = A.prepare(Q)
                ok, sense = B.unit_square(B.to_mpq(Q))
                check(sa.unit and ok, f"unit test accepts {u} {s0} {rev}")
                check(sa.sense == sense == (-1 if rev else 1), f"sense {u} {s0} {rev}")
    z, o = Fraction(0), Fraction(1)
    bad = {
        "corner off by 1e-30": [(z, z), (o + E30, z), (o, o), (z, o)],
        "bowtie": [(z, z), (o, o), (o, z), (z, o)],
        "unit rhombus": [(z, z), (o, z), (o + Fraction(3, 5), Fraction(4, 5)), (Fraction(3, 5), Fraction(4, 5))],
        "rectangle": [(z, z), (o, z), (o, o + E30), (z, o + E30)],
        "side 2": [(z, z), (2 * o, z), (2 * o, 2 * o), (z, 2 * o)],
        "point": [(z, z)] * 4,
        "repeated corner": [(z, z), (o, z), (o, z), (z, o)],
        "parallelogram": [(z, z), (o, z), (2 * o, o), (o, o)],
        "folded": [(z, z), (o, z), (z, z), (o, z)],
    }
    for name, pts in bad.items():
        check(not A.prepare(pts).unit, f"A refuses {name}")
        check(not B.unit_square(B.to_mpq(pts))[0], f"B refuses {name}")
    for u in [(o, E30), (Fraction(3, 5), Fraction(4, 5) + E30), (half, half), (o + E30, z),
              (Fraction(6, 10), Fraction(8, 10) - E30), (z, z)]:
        P = sq((half, half), u)
        check(not A.prepare(P).unit and not B.unit_square(B.to_mpq(P))[0], f"direction {u} refused")


def test_random_pairs(rnd):
    for t in range(400):
        m = rnd.randrange(2, 10**7)
        k = rnd.randrange(1, m)
        u1 = Y.pyth(m, k)
        m2 = rnd.randrange(2, 10**7)
        k2 = rnd.randrange(1, m2)
        u2 = Y.pyth(m2, k2)
        if rnd.random() < 0.5:
            u2 = (-u2[1], u2[0])
        c1 = (Fraction(rnd.randrange(-10**6, 10**6), 10**6), Fraction(rnd.randrange(-10**6, 10**6), 10**6))
        c2 = (c1[0] + Fraction(rnd.randrange(-2 * 10**6, 2 * 10**6), 10**6),
              c1[1] + Fraction(rnd.randrange(-2 * 10**6, 2 * 10**6), 10**6))
        P, Q = sq(c1, u1), sq(c2, u2)
        mA1, mA2 = pairA(P, Q), pairA(Q, P)
        cf = F.pair_margin(c1, u1, c2, u2)
        check(mA1 == mA2 == cf, f"random pair {t}: A both ways and closed form")
        cl, area = pairB(P, Q)
        want = A.cls(cf)
        check(cl == want, f"random pair {t}: B class {cl} vs {want}")
        ca = clip_area(P, Q)
        check(mpq_frac(area) == ca, f"random pair {t}: B area equals clipping")
        d = (c2[0] - c1[0], c2[1] - c1[1])
        if d == (0, 0):
            continue
        TT, M = F.T_of(u1, u2), F.M_of(u1, u2, d)
        for mstar in (E30, Fraction(0), -E30):
            tau = (mstar + TT) / M
            c3 = (c1[0] + tau * d[0], c1[1] + tau * d[1])
            Q3 = sq(c3, u2)
            check(pairA(P, Q3) == mstar and pairA(Q3, P) == mstar, f"random closing {t} {mstar}")
            check(F.pair_margin(c1, u1, c3, u2) == mstar, f"random closing closed form {t}")
            want = "apart" if mstar > 0 else ("contact" if mstar == 0 else "overlap")
            check(pairB(P, Q3)[0] == want, f"random closing B {t} {mstar}")
    S = Fraction(9)
    for t in range(120):
        m = rnd.randrange(2, 10**6)
        k = rnd.randrange(1, m)
        u = Y.pyth(m, k)
        h = F.half_extent(u)
        for wall in range(4):
            for delta in (E30, Fraction(0), -E30):
                base = Fraction(rnd.randrange(2 * 10**6, 7 * 10**6), 10**6)
                c = [(h + delta, base), (base, h + delta), (S - h - delta, base), (base, S - h - delta)][wall]
                P = sq(c, u)
                check(A.walls(A.prepare(P), S)[wall] == delta, f"random wall A {t}")
                cls, inside = B.wall_classes(B.ccw(B.to_mpq(P)), B.mpq(9))
                want = "clear" if delta > 0 else ("touch" if delta == 0 else "cross")
                check(cls[wall] == want and ((inside == 1) == (delta >= 0)), f"random wall B {t}")


def write_and_read(p, form):
    if form == "centre":
        return R.read_centre(R.write_centre(p.n, p.side, p.centres, p.directions))
    return R.read_witness(R.write_witness(p.n, p.side, p.corners))


def test_whole_files():
    g = Y.grid(2, 2)
    for form in ("centre", "witness"):
        q = write_and_read(g, form)
        s = D.summarize(D.decide_full(q))
        check(s["verdict"] == "ACCEPT", f"2x2 grid accepted ({form})")
        check(len(s["touching_pairs"]) == 6, f"2x2 grid six touching pairs ({form})")
        check(sum(len(v) for v in s["wall_contacts"].values()) == 8, f"2x2 eight wall contacts ({form})")
        q.side -= E30
        check(D.summarize(D.decide_full(q))["verdict"] == "REFUSE", f"2x2 in a box 1e-30 small ({form})")
    g3 = Y.grid(3, 3)
    check(D.summarize(D.decide_full(g3))["verdict"] == "ACCEPT", "3x3 tight")
    g3l = Y.grid(3, 3, gap=Fraction(1, 10))
    s = D.summarize(D.decide_full(g3l))
    check(s["verdict"] == "ACCEPT" and not s["touching_pairs"], "3x3 loose")
    dup = Y.from_frames(3, g3.centres[:-1] + [g3.centres[0]], g3.directions)
    s = D.summarize(D.decide_full(dup))
    check(s["verdict"] == "REFUSE" and [1, 9] in [list(x) for x in s["overlapping_pairs"]], "duplicate refused")
    u = (Fraction(3, 5), Fraction(4, 5))
    one = Y.from_frames(Fraction(7, 5), [(Fraction(7, 10), Fraction(7, 10))], [u])
    s = D.summarize(D.decide_full(one))
    check(s["verdict"] == "ACCEPT" and all(len(v) == 1 for v in s["wall_contacts"].values()),
          "3-4-5 square touching all four walls")
    bad = Y.from_frames(3, g3.centres, g3.directions[:-1] + [(Fraction(1), E30)])
    check(D.summarize(D.decide_full(bad))["verdict"] == "REFUSE", "non-unit square refused")
    # patched decision equals a fresh one
    r = Y.realistic(n=30, seed=7, digits=12)
    base = D.decide_full(r)
    cs = list(r.centres)
    cs[4] = (cs[4][0] + Fraction(1, 3000), cs[4][1])
    cs[17] = (cs[17][0], cs[17][1] - Fraction(1, 2500))
    r2 = Y.from_frames(r.side - Fraction(1, 10**13), cs, r.directions)
    s_patch = D.summarize(D.decide_patch(base, r2, [4, 17]))
    s_full = D.summarize(D.decide_full(r2))
    check(s_patch == s_full, "patched decision equals fresh")
    # twin comparison
    w = R.read_witness(R.write_witness(r.n, r.side, r.corners))
    check(T.compare(r, w)["verdict"] == "SAME_PACKING", "twin same")
    cs = list(r.centres)
    cs[0] = (cs[0][0] + E30, cs[0][1])
    r3 = Y.from_frames(r.side, cs, r.directions)
    res = T.compare(r3, w)
    check(res["verdict"] == "DIFFERENT" and res["unequal_squares"] == [1], "twin differs in square 1")
    rr = Y.from_frames(r.side, r.centres[1:] + r.centres[:1], r.directions[1:] + r.directions[:1])
    check(T.compare(rr, w)["verdict"] == "DIFFERENT", "twin reordered differs")
    rs = Y.from_frames(r.side + E30, r.centres, r.directions)
    check(T.compare(rs, w)["verdict"] == "DIFFERENT", "twin resized differs")
    for k in (1, 2, 3):
        cr = [list(x) for x in w.corners]
        cr[5][k] = (cr[5][k][0], cr[5][k][1] + E30)
        w2 = R.read_witness(R.write_witness(r.n, r.side, cr))
        res = T.compare(r, w2)
        check(res["verdict"] == "DIFFERENT" and res["unequal_squares"] == [6],
              f"twin differs at corner {k} of square 6")


def test_contraction():
    # two upright squares at gap g on a line: lambda* = 1/(1+g), and L' = 2 exactly
    g = Fraction(1, 7)
    p = Y.from_frames(Fraction(3), [(Fraction(1, 2), Fraction(1, 2)), (Fraction(3, 2) + g, Fraction(1, 2))],
                      [(Fraction(1), Fraction(0))] * 2)
    c = K.contraction(p)
    check(c["_lam"] == 1 / (1 + g), "contraction lambda* of a pair")
    check(c["_L"] == 2, "contraction L' of a pair")
    check(c["contracted_decision"]["verdict"] == "ACCEPT" and c["binding_pairs_touch_in_contracted"],
          "contracted pair accepted, touching")
    check(c["past_refused_as_stated"], "contraction past refused")
    # a tight grid has lambda* = 1 and margin S - extent
    g3 = Y.grid(3, 3, side=Fraction(3) + Fraction(1, 9))
    c = K.contraction(g3)
    check(c["_lam"] == 1 and c["_L"] == 3, "tight grid: lambda* 1, L' 3")
    # a loose grid: lambda* = 1/(1+gap) and L' = 3
    g3l = Y.grid(3, 3, gap=Fraction(1, 10))
    c = K.contraction(g3l)
    check(c["_lam"] == Fraction(10, 11) and c["_L"] == 3, "loose grid contraction")
    # a 3-4-5 square beside an upright one, gap 1/5 along x: lambda* = T/M with T = 6/5
    u = (Fraction(4, 5), Fraction(3, 5))
    p = Y.from_frames(Fraction(4), [(Fraction(1, 2), Fraction(1, 2)), (Fraction(1) + Fraction(7, 10) + Fraction(1, 5), Fraction(1, 2))],
                      [(Fraction(1), Fraction(0)), u])
    c = K.contraction(p)
    M = Fraction(1) + Fraction(7, 10) + Fraction(1, 5) - Fraction(1, 2)
    check(c["_lam"] == Fraction(6, 5) / M, "tilted pair lambda*")


def reader_cases():
    good_c = R.write_centre(2, Fraction(5, 2), [(Fraction(1, 2), Fraction(1, 2)), (Fraction(3, 2), Fraction(1, 2))],
                            [(Fraction(1), Fraction(0)), (Fraction(3, 5), Fraction(4, 5))])
    good_w = R.write_witness(1, Fraction(1), [R.centre_corners((Fraction(1, 2), Fraction(1, 2)), (Fraction(1), Fraction(0)))])
    return good_c, good_w


def test_readers():
    gc, gw = reader_cases()
    check(R.read_centre(gc).n == 2, "good centre file reads")
    check(R.read_witness(gw).n == 1, "good witness file reads")
    side_line = [ln for ln in gw.split("\n") if ln.startswith("  side:")][0]
    bad_c = {
        "duplicate key": gc.replace('"n": 2,', '"n": 2,\n "n": 2,'),
        "float side": gc.replace('"side": "5/2"', '"side": 2.5'),
        "integer side": gc.replace('"side": "5/2"', '"side": 2'),
        "leading plus": gc.replace('"1/2"', '"+1/2"', 1),
        "leading zero": gc.replace('"5/2"', '"05/2"'),
        "negative zero": gc.replace('"0"', '"-0"', 1),
        "zero denominator": gc.replace('"5/2"', '"5/0"'),
        "count": gc.replace('"n": 2', '"n": 3'),
        "extra key": gc.replace('"n": 2,', '"n": 2,\n "x": "1",'),
        "missing key": gc.replace('"square_size": "1",', ''),
        "format sentence": gc.replace("(cos, sin)", "(sin, cos)"),
        "five scalars": gc.replace('"1",\n   "0"', '"1",\n   "0",\n   "0"', 1),
        "number scalar": gc.replace('"1/2",', '0.5,', 1),
        "NaN": gc.replace('"5/2"', 'NaN'),
        "true": gc.replace('"5/2"', 'true'),
        "square_size": gc.replace('"square_size": "1"', '"square_size": "2"'),
        "decimal scalar": gc.replace('"5/2"', '"2.5"'),
    }
    for name, text in bad_c.items():
        check(text != gc, f"centre mutation changed the text: {name}")
        try:
            R.read_centre(text)
            check(False, f"centre reader refuses {name}")
        except R.ReadError:
            check(True, "")
    bad_w = {
        "duplicate key": gw.replace("  n: 1\n", "  n: 1\n  n: 1\n"),
        "anchor": gw.replace("  scalar:\n", "  scalar: &a\n"),
        "tag": gw.replace("  n: 1", "  n: !!int 1"),
        "flow": gw.replace("  scalar:\n    kind: rational", "  scalar: {kind: rational}"),
        "tab": gw.replace("  n: 1", "  n:\t1"),
        "carriage return": gw.replace("\n", "\r\n", 1),
        "document start": "---\n" + gw,
        "two documents": gw + "---\nx: 1\n",
        "envelope": gw.replace("Witness/v2", "Witness/v1"),
        "origin": gw.replace("origin: lower-left", "origin: container-center"),
        "representation": gw.replace("representation: corners", "representation: center-angle"),
        "square_size": gw.replace("square_size: '1'", "square_size: '2'"),
        "count": gw.replace("  n: 1", "  n: 2"),
        "unknown key": gw.replace("  n: 1\n", "  n: 1\n  extra: 1\n"),
        "missing claim": gw.replace("  claim:\n    coordinate_provenance: reported\n    method: exact-algebraic\n    limitations: control file written by r127_controls\n", ""),
        "float side": gw.replace(side_line, "  side: 1.0"),
        "block scalar": gw.replace("  id: W-r127-control", "  id: |\n    W"),
        "three scalars": gw.replace("      - '0'\n", "      - '0'\n      - '0'\n", 1),
        "bool": gw.replace("  n: 1", "  n: true"),
        "alias": gw.replace("  scalar:\n    kind: rational", "  scalar:\n    kind: &k rational\n  source: *k"),
        "duplicate id": R.write_witness(2, Fraction(2), [R.centre_corners((Fraction(1, 2), Fraction(1, 2)), (Fraction(1), Fraction(0)))] * 2, ids=["a", "a"]),
        "leading plus": gw.replace("    - - '0'", "    - - '+0'", 1),
        "hex int": gw.replace("  n: 1", "  n: 0x1"),
    }
    for name, text in bad_w.items():
        check(text != gw, f"witness mutation changed the text: {name}")
        try:
            R.read_witness(text)
            check(False, f"witness reader refuses {name}")
        except R.ReadError:
            check(True, "")
    p = R.read_centre(gc.replace('"5/2"', '"10/4"'))
    check(p.side == Fraction(5, 2) and p.not_lowest == ["side"], "side out of lowest terms read and flagged")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    t0 = time.process_time()
    rnd = random.Random(20261118)
    for f in (test_edge_contacts, test_tilted_corner, test_concentric_and_duplicate, test_walls,
              test_unit_tests, lambda: test_random_pairs(rnd), test_whole_files, test_contraction,
              test_readers):
        try:
            f()
        except Exception as exc:  # noqa: BLE001 - a crash is a failed check here
            FAILS.append(f"{getattr(f, '__name__', 'test')}: raised {type(exc).__name__}: {exc}")
    res = {"program": "r127_selftest.py", "checks": COUNT[0], "failures": len(FAILS),
           "first_failures": FAILS[:20], "verdict": "PASSED" if not FAILS else "FAILED",
           "cpu_seconds": round(time.process_time() - t0, 2)}
    if a.out:
        json.dump(res, open(a.out, "w"), indent=1)
    print(f"selftest: {res['verdict']} checks={res['checks']} failures={res['failures']} "
          f"cpu={res['cpu_seconds']}s")
    for f in FAILS[:10]:
        print("  FAIL", f)
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
