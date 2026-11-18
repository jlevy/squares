"""Self-test of lane r127b-1118's programs, on synthetic packings only.

Usage: ``python -I -B rb127_selftest.py OUT.json``

It reads no certificate. It holds the readers, both methods, the conversions, the
contraction and the identity measurement to closed forms derived by hand, and then runs
the same checks under broken copies of the programs, each of which must fail at least
one check. ``PASSED`` means every check of the intact programs held and every broken
copy was caught.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gmpy2 import mpq  # noqa: E402

import rb127_axes as A  # noqa: E402
import rb127_clip as B  # noqa: E402
import rb127_contract as K  # noqa: E402
import rb127_decide as D  # noqa: E402
import rb127_fmt as F  # noqa: E402
import rb127_identity as ID  # noqa: E402
import rb127_read as R  # noqa: E402
import rb127_twin as T  # noqa: E402
import rb127_write as W  # noqa: E402

Q = tuple[int, int]
TINY = Fr(1, 10**40)
DIRS = [(1, 0, 1), (3, 4, 5), (5, 12, 13), (15, 8, 17), (4, -3, 5), (0, 1, 1)]


class Tally:
    def __init__(self) -> None:
        self.passed = 0
        self.failed: list[str] = []

    def check(self, ok: bool, what: str) -> None:
        if ok:
            self.passed += 1
        else:
            self.failed.append(what)


def pq(f: Fr) -> Q:
    return f.numerator, f.denominator


def row(cx: Fr, cy: Fr, d: tuple[int, int, int]) -> tuple[Q, Q, Q, Q]:
    a, b, r = d
    return pq(cx), pq(cy), pq(Fr(a, r)), pq(Fr(b, r))


def uv(d: tuple[int, int, int]) -> tuple[tuple[Fr, Fr], tuple[Fr, Fr]]:
    a, b, r = d
    u = (Fr(a, r), Fr(b, r))
    return u, (-u[1], u[0])


def pair_decide(r1, r2) -> tuple[Fr, str, Any, bool, Any]:
    i1, i2 = A.to_ipose(*r1), A.to_ipose(*r2)
    m = A.margin(i1, i2)
    p1 = B.to_points(T.corners_pq(r1))
    p2 = B.to_points(T.corners_pq(r2))
    ok1, s1 = B.unit_square(p1)
    ok2, s2 = B.unit_square(p2)
    p1, p2 = B.ccw(p1, s1), B.ccw(p2, s2)
    cls, ar, agree = B.pair(p1, p2)
    proj = B.projections_margin(p1, p2)
    return m, cls, ar, agree and ok1 and ok2, proj


def sign_class(m: Fr) -> str:
    return "apart" if m > 0 else "contact" if m == 0 else "overlap"


def test_pairs(t: Tally) -> None:
    gaps = [TINY, Fr(0), -TINY, Fr(1, 7), -Fr(1, 7)]
    for d in DIRS:
        u, v = uv(d)
        c0 = (Fr(5), Fr(5))
        # Edge contacts of parallel squares across each of the four edges.
        for e_u, e_v in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for tau in (Fr(0), Fr(1, 3), -Fr(1, 3)):
                for g in gaps:
                    # The second square sits across edge (e_u, e_v) at gap g, slid by tau.
                    if e_u:
                        du, dv = e_u * (1 + g), tau
                    else:
                        du, dv = tau, e_v * (1 + g)
                    cx = c0[0] + du * u[0] + dv * v[0]
                    cy = c0[1] + du * u[1] + dv * v[1]
                    r1, r2 = row(c0[0], c0[1], d), row(cx, cy, d)
                    for first, second in ((r1, r2), (r2, r1)):
                        m, cls, ar, agree, proj = pair_decide(first, second)
                        what = f"edge contact dir {d} edge {(e_u, e_v)} tau {tau} gap {g}"
                        t.check(m == g, what + " margin")
                        t.check(proj == g, what + " projections")
                        t.check(cls == sign_class(g) and agree, what + " class")
                        if g < 0:
                            want = mpq(-g.numerator, g.denominator) * (1 - abs(mpq(tau.numerator, tau.denominator)))
                            t.check(ar == want, what + " area")
        # Corner to corner along each diagonal.
        for su, sv in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            for g in gaps:
                cx = c0[0] + su * (1 + g) * u[0] + sv * (1 + g) * v[0]
                cy = c0[1] + su * (1 + g) * u[1] + sv * (1 + g) * v[1]
                m, cls, ar, agree, proj = pair_decide(row(c0[0], c0[1], d), row(cx, cy, d))
                what = f"corner contact dir {d} diag {(su, sv)} gap {g}"
                t.check(m == g and proj == g, what + " margin")
                t.check(cls == sign_class(g) and agree, what + " class")
                if g < 0 and abs(g) < 1:
                    t.check(ar == mpq(g.numerator**2, g.denominator**2), what + " area")
    # A tilted corner on an upright edge, and an upright corner on a tilted edge.
    for d, k in (((3, 4, 5), Fr(25, 24)), ((5, 12, 13), Fr(169, 120))):
        u, v = uv(d)
        h = (abs(u[0]) + abs(u[1])) / 2
        for g in (TINY, Fr(0), -TINY, -Fr(1, 100)):
            for flip in (1, -1):
                c1 = (Fr(3), Fr(3))
                c2 = (Fr(3) + Fr(1, 10), Fr(3) + flip * (Fr(1, 2) + h + g))
                up, tl = row(c1[0], c1[1], (1, 0, 1)), row(c2[0], c2[1], d)
                for first, second, order in ((up, tl, "upright first"), (tl, up, "tilted first")):
                    m, cls, ar, agree, proj = pair_decide(first, second)
                    what = f"tilted corner on an upright edge dir {d} gap {g} flip {flip} {order}"
                    t.check(m == g and proj == g, what + " margin")
                    t.check(cls == sign_class(g) and agree, what + " class")
                    if g < 0:
                        t.check(ar == mpq(k.numerator * g.numerator**2, k.denominator * g.denominator**2), what + " area")
                # The same, turned so that the upright corner meets the tilted edge.
                m2, cls2, _, agree2, proj2 = pair_decide(
                    rot_row(row(c1[0], c1[1], (1, 0, 1)), d), rot_row(row(c2[0], c2[1], d), d)
                )
                t.check(m2 == g and proj2 == g and cls2 == sign_class(g) and agree2, what + " turned")
    # Duplicates and concentric turns.
    for d in DIRS:
        m, cls, ar, agree, _ = pair_decide(row(Fr(2), Fr(2), d), row(Fr(2), Fr(2), d))
        t.check(m == -1 and cls == "overlap" and ar == 1 and agree, f"duplicate {d}")
    for d, area in (((3, 4, 5), Fr(5, 6)), ((5, 12, 13), Fr(13, 15))):
        a, b, r = d
        H = Fr(1, 2) + (Fr(abs(a), r) + Fr(abs(b), r)) / 2
        m, cls, ar, agree, _ = pair_decide(row(Fr(2), Fr(2), (1, 0, 1)), row(Fr(2), Fr(2), d))
        t.check(m == -H and cls == "overlap" and ar == mpq(area.numerator, area.denominator) and agree, f"concentric {d}")


def rot_row(r: tuple[Q, Q, Q, Q], d: tuple[int, int, int]) -> tuple[Q, Q, Q, Q]:
    """Turn a row about the origin by the direction ``d`` (an exact rotation)."""
    a, b, rr = d
    c, s = Fr(a, rr), Fr(b, rr)
    x, y, u0, u1 = (Fr(v[0], v[1]) for v in r)
    nx, ny = c * x - s * y, s * x + c * y
    nu0, nu1 = c * u0 - s * u1, s * u0 + c * u1
    return pq(nx + 20), pq(ny + 20), pq(nu0), pq(nu1)


def random_dir(rng: random.Random) -> tuple[int, int, int]:
    p = rng.randint(-10**6, 10**6)
    q = rng.randint(1, 10**6)
    return q * q - p * p, 2 * p * q, q * q + p * p


def test_random(t: Tally, rng: random.Random, count: int) -> None:
    for k in range(count):
        d1, d2 = random_dir(rng), random_dir(rng)
        c1 = (Fr(rng.randint(0, 10**6), 10**6) + 5, Fr(rng.randint(0, 10**6), 10**6) + 5)
        ang = rng.randint(0, 10**6)
        dist = Fr(rng.randint(5 * 10**5, 2 * 10**6), 10**6)
        dd = random_dir(rng)
        c2 = (c1[0] + dist * Fr(dd[0], dd[2]), c1[1] + dist * Fr(dd[1], dd[2]))
        r1, r2 = row(c1[0], c1[1], d1), row(c2[0], c2[1], d2)
        m, cls, _, agree, proj = pair_decide(r1, r2)
        t.check(m == proj, f"random {k}: method A equals the corner projections")
        t.check(cls == sign_class(m) and agree, f"random {k}: B's class is A's sign")
        i1, i2 = A.to_ipose(*r1), A.to_ipose(*r2)
        M, Hn, L = A.pair_numbers(i1, i2)
        for target in (TINY, Fr(0), -TINY):
            s = (target + Fr(Hn, L)) / Fr(M, L)
            n2 = (c1[0] + s * (c2[0] - c1[0]), c1[1] + s * (c2[1] - c1[1]))
            m2, cls2, _, agree2, proj2 = pair_decide(r1, row(n2[0], n2[1], d2))
            t.check(m2 == target and proj2 == target, f"random {k} closed to {target}: margin")
            t.check(cls2 == sign_class(target) and agree2, f"random {k} closed to {target}: class")
        del ang


def test_walls(t: Tally) -> None:
    S = Fr(10)
    for d in DIRS:
        a, b, r = d
        h = (Fr(abs(a), r) + Fr(abs(b), r)) / 2
        for g in (TINY, Fr(0), -TINY, Fr(1, 9), -Fr(1, 9)):
            places = [
                (h + g, Fr(5), 0), (Fr(5), h + g, 1), (S - h - g, Fr(5), 2), (Fr(5), S - h - g, 3),
            ]
            for cx, cy, w in places:
                rr = row(cx, cy, d)
                cl = A.clearances(A.to_ipose(*rr), pq(S))
                t.check(cl[w] == g, f"wall {w} dir {d} gap {g}: A clearance")
                pts = B.to_points(T.corners_pq(rr))
                ok, sense = B.unit_square(pts)
                cls, inside = B.walls(B.ccw(pts, sense), mpq(10))
                want = "apart" if g > 0 else "contact" if g == 0 else "overlap"
                t.check(ok and cls[w][0] == want, f"wall {w} dir {d} gap {g}: B class")
                t.check((inside == 1) == (g >= 0), f"wall {w} dir {d} gap {g}: B inside")
                for other in range(4):
                    if other != w:
                        t.check(cls[other][0] == "apart", f"wall {w} dir {d} gap {g}: other walls clear")


def test_shapes(t: Tally) -> None:
    good = [(mpq(0), mpq(0)), (mpq(1), mpq(0)), (mpq(1), mpq(1)), (mpq(0), mpq(1))]
    t.check(B.unit_square(good) == (True, 1), "unit square ccw")
    t.check(B.unit_square(list(reversed(good))) == (True, -1), "unit square cw")
    bad = {
        "corner off by 1e-40": [(mpq(0), mpq(0)), (mpq(1), mpq(0)), (mpq(1), mpq(1)), (mpq(0), mpq(1, 1) + mpq(1, 10**40))],
        "bowtie": [good[0], good[2], good[1], good[3]],
        "rhombus with unit sides": [(mpq(0), mpq(0)), (mpq(1), mpq(0)), (mpq(8, 5), mpq(4, 5)), (mpq(3, 5), mpq(4, 5))],
        "rectangle": [(mpq(0), mpq(0)), (mpq(1) + mpq(1, 10**40), mpq(0)), (mpq(1) + mpq(1, 10**40), mpq(1)), (mpq(0), mpq(1))],
        "side 2": [(mpq(0), mpq(0)), (mpq(2), mpq(0)), (mpq(2), mpq(2)), (mpq(0), mpq(2))],
        "point": [good[0]] * 4,
        "repeated corner": [good[0], good[1], good[1], good[3]],
    }
    for name, pts in bad.items():
        t.check(B.unit_square(pts)[0] is False, f"shape refused by B: {name}")
    for name, (a, b, r) in {"(1,1)/1": (1, 1, 1), "(3,4)/6": (3, 4, 6), "(1+1e-40, 0)": (10**40 + 1, 0, 10**40)}.items():
        t.check(A.is_unit(A.to_ipose((0, 1), (0, 1), (a, r), (b, r))) is False, f"direction refused by A: {name}")


def test_twin(t: Tally) -> None:
    for d in DIRS:
        r = row(Fr(7, 3), Fr(11, 5), d)
        cs = T.corners_pq(r)
        t.check(T.match(cs, T.corners_of_pose(r)) == (0, 1), f"twin identity {d}")
        for off in range(4):
            rot = tuple(cs[(off + k) % 4] for k in range(4))
            t.check(T.match(rot, T.corners_of_pose(r)) == (off, 1), f"twin offset {off} {d}")
            rev = tuple(cs[(off - k) % 4] for k in range(4))
            t.check(T.match(rev, T.corners_of_pose(r)) == (off, -1), f"twin reversed {off} {d}")
        back = T.pose_of_corners(cs)
        t.check(Fr(*back[0]) == Fr(7, 3) and Fr(*back[1]) == Fr(11, 5), f"pose of corners centre {d}")
        u = (Fr(*back[2]), Fr(*back[3]))
        a, b, rr = d
        t.check(u == (Fr(a, rr), Fr(b, rr)), f"pose of corners direction {d}")
        moved = list(cs)
        moved[0] = ((moved[0][0][0] * 10**40 + moved[0][0][1], moved[0][0][1] * 10**40), moved[0][1])
        t.check(T.match(tuple(moved), T.corners_of_pose(r)) is None, f"twin refuses a moved corner {d}")
    # A known corner listing written out by hand: centre (1/2, 1/2), upright.
    r = row(Fr(1, 2), Fr(1, 2), (1, 0, 1))
    t.check(T.corners_pq(r) == ((((0, 1)), (0, 1)), ((1, 1), (0, 1)), ((1, 1), (1, 1)), ((0, 1), (1, 1))), "corners by hand")


def grid(eps: Fr, tilted: bool = False) -> tuple[list[tuple[Q, Q, Q, Q]], Q]:
    s = 1 + eps
    rows = []
    for i, j in ((0, 0), (1, 0), (0, 1), (1, 1)):
        cx = 1 + Fr(2 * i - 1, 2) * s + eps / 2
        cy = 1 + Fr(2 * j - 1, 2) * s + eps / 2
        rows.append(row(cx, cy, (1, 0, 1)))
    side = 2 + 2 * eps
    if tilted:
        rows.append(row(Fr(4), Fr(1), (3, 4, 5)))
        side = Fr(5)
    return rows, pq(side)


def test_files(t: Tally) -> None:
    rows, side = grid(Fr(1, 10**6))
    corners = [T.corners_pq(r) for r in rows]
    jb, cb = W.form_j(4, side, rows), W.form_c(4, side, corners)
    J, C = R.read_form_j(jb), R.read_form_c(cb)
    t.check(J["rows"] == rows, "form J read back")
    t.check([tuple(c) for c in C["corners"]] == corners, "form C read back")
    t.check(R.read_form_c(W.form_c(4, side, corners, id_style="integer"))["id_style"] == "integer", "integer ids")
    t.check(R.read_form_j(W.form_j(4, (2 * side[0], 2 * side[1]), rows))["flags"] == ["side not in lowest terms"], "non-canonical side flagged")
    jt = jb.decode()
    ct = cb.decode()
    j_bad = {
        "count": jt.replace('"n": 4', '"n": 5'),
        "plus sign": jt.replace('   "1",', '   "+1",', 1),
        "float number": jt.replace('"n": 4', '"n": 4.0'),
        "duplicate key": jt.replace('"square_size": "1",', '"square_size": "1",\n "square_size": "1",'),
        "number scalar": jt.replace('   "1",', "   1,", 1),
        "leading zero": jt.replace('   "1",', '   "01",', 1),
        "zero denominator": jt.replace('   "1",', '   "1/0",', 1),
        "negative zero": jt.replace('   "0"\n', '   "-0"\n', 1),
        "decimal": jt.replace('   "1",', '   "1.0",', 1),
        "format sentence": jt.replace("unit direction", "unit vector"),
        "extra key": jt.replace('"square_size": "1",', '"square_size": "1",\n "extra": "1",'),
        "five scalars": jt.replace('[\n   "', '[\n   "0",\n   "', 1),
        "carriage return": jt.replace("\n", "\r\n", 1),
        "tab": jt.replace(" ", "\t", 1),
        "nan": jt.replace('"n": 4', '"n": NaN'),
        "true": jt.replace('"n": 4', '"n": true'),
    }
    for name, text in j_bad.items():
        t.check(text != jt, f"form J mutation applied: {name}")
        try:
            R.read_form_j(text.encode())
            t.check(False, f"form J refuses {name}")
        except R.ReadError:
            t.check(True, f"form J refuses {name}")
    c_bad = {
        "count": ct.replace("  n: 4", "  n: 5"),
        "ids out of order": ct.replace("square-1\n", "square-9\n", 1),
        "anchor": ct.replace("  scalar:\n    kind: rational", "  scalar: &a\n    kind: rational"),
        "duplicate key": ct.replace("  square_size: '1'", "  square_size: '1'\n  square_size: '1'"),
        "float corner": ct.replace("    - - '0'", "    - - 0.0", 1),
        "integer corner": ct.replace("    - - '0'", "    - - 0", 1),
        "plus sign": ct.replace("    - - '0'", "    - - '+0'", 1),
        "contract": ct.replace("Witness/v2", "Witness/v3"),
        "representation": ct.replace("representation: corners", "representation: center-basis"),
        "origin": ct.replace("origin: lower-left", "origin: container-center"),
        "extra witness key": ct.replace("  square_size: '1'", "  square_size: '1'\n  extra: x"),
        "five corners": ct.replace("  - id: square-1\n    corners:\n", "  - id: square-1\n    corners:\n    - - '0'\n      - '0'\n", 1),
        "a corner double-quoted, which the line reading does not take": ct.replace("    - - '0'", '    - - "0"', 1),
        "tag": ct.replace("  n: 4", "  n: !!int 4"),
        "flow sequence": ct.replace("    kind: rational", "    kind: [rational]"),
        "square size": ct.replace("square_size: '1'", "square_size: '2'"),
        "no final newline": ct.rstrip("\n"),
        "two documents": ct + "---\nx: 1\n",
        "null value": ct.replace("    kind: rational", "    kind:"),
    }
    for name, text in c_bad.items():
        t.check(text != ct, f"form C mutation applied: {name}")
        try:
            R.read_form_c(text.encode())
            t.check(False, f"form C refuses {name}")
        except R.ReadError:
            t.check(True, f"form C refuses {name}")


def test_decide_files(t: Tally) -> None:
    rows, side = grid(Fr(1, 10**6))
    corners = [T.corners_pq(r) for r in rows]
    dec = D.decide(rows, corners, side)
    t.check(dec["verdict"] == "ACCEPT", "dilated grid accepted")
    rows0, side0 = grid(Fr(0))
    dec0 = D.decide(rows0, [T.corners_pq(r) for r in rows0], side0)
    t.check(dec0["verdict"] == "ACCEPT", "touching grid accepted")
    s0 = D.summary(dec0)
    t.check(s0["pair_classes_a"] == {"contact": 6} and s0["pair_classes_b"] == {"contact": 6}, "touching grid: six contacts")
    t.check(s0["wall_classes_a"].get("touch") == 8 and s0["wall_classes_b"].get("touch") == 8, "touching grid: eight wall contacts")
    small = (side0[0] * 10**40 - side0[1], side0[1] * 10**40)
    t.check(D.decide(rows0, [T.corners_pq(r) for r in rows0], small)["verdict"] == "REFUSE", "grid in a box 1e-40 small refused")
    dup = rows0[:3] + [rows0[0]]
    t.check(D.decide(dup, [T.corners_pq(r) for r in dup], side0)["verdict"] == "REFUSE", "duplicate square refused")
    rt, st = grid(Fr(1, 10**6), tilted=True)
    t.check(D.decide(rt, [T.corners_pq(r) for r in rt], st)["verdict"] == "ACCEPT", "grid with a tilted square accepted")
    bad_corners = [T.corners_pq(r) for r in rows]
    c = bad_corners[1]
    bad_corners[1] = (((c[0][0][0] * 10**40 + c[0][0][1], c[0][0][1] * 10**40), c[0][1]),) + c[1:]
    t.check(D.decide(rows, bad_corners, side)["verdict"] == "REFUSE", "a corner moved by 1e-40 refused")


def test_contraction(t: Tally) -> None:
    for eps in (Fr(1, 10**6), Fr(1, 10**30), Fr(3, 7)):
        rows, side = grid(eps)
        k = K.contraction(rows, side)
        t.check(k["_lam"] == 1 / (1 + eps), f"grid eps {eps}: lambda* = 1/(1+eps)")
        t.check(k["_shrunk_side"] == 2, f"grid eps {eps}: shrunk side 2")
        t.check(k["_margin"] == Fr(side[0], side[1]) - 2, f"grid eps {eps}: margin")
        t.check(len(k["binding_pairs"]) == 6, f"grid eps {eps}: six binding pairs")
        sr, ss = K.shrunk_rows(rows, k["_lam"])
        dec = D.decide(sr, [T.corners_pq(r) for r in sr], ss)
        t.check(dec["verdict"] == "ACCEPT", f"grid eps {eps}: shrunk packing accepted")
        past = k["_lam"] * (1 - TINY)
        sp, sps = K.shrunk_rows(rows, past)
        decp = D.decide(sp, [T.corners_pq(r) for r in sp], sps)
        t.check(decp["verdict"] == "REFUSE", f"grid eps {eps}: past first contact refused")
    # The grid with a far tilted square: unequal factors, the grid's pairs bind.
    eps = Fr(1, 10**6)
    rows, side = grid(eps, tilted=True)
    k = K.contraction(rows, side)
    t.check(k["_lam"] == 1 / (1 + eps), "grid and a far square: lambda* is the grid's")
    t.check(sorted(map(tuple, k["binding_pairs"])) == [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)],
            "grid and a far square: the grid's six pairs bind")
    sr, ss = K.shrunk_rows(rows, k["_lam"])
    t.check(D.decide(sr, [T.corners_pq(r) for r in sr], ss)["verdict"] == "ACCEPT", "grid and a far square: shrunk accepted")
    sp, sps = K.shrunk_rows(rows, k["_lam"] * (1 - TINY))
    t.check(D.decide(sp, [T.corners_pq(r) for r in sp], sps)["verdict"] == "REFUSE", "grid and a far square: past refused")
    # Two squares, one tilted, touching only after contraction; the factor by hand.
    d = (3, 4, 5)
    h = Fr(7, 10)
    gap = Fr(1, 1000)
    rows = [row(Fr(1, 2), Fr(1, 2), (1, 0, 1)), row(Fr(1, 2) + Fr(1, 10), 1 + h + gap, d)]
    side = (5, 1)
    k = K.contraction(rows, side)
    # The pair's centre difference is (1/10, 1/2 + h + gap); its margin at scale lam is
    # lam*(1/2 + h + gap) - (1/2 + h) on the upright normal, which binds.
    want = (Fr(1, 2) + h) / (Fr(1, 2) + h + gap)
    t.check(k["_lam"] == want, "tilted pair: lambda* by hand")
    width = max(Fr(1, 2) * want + Fr(1, 2), (Fr(1, 2) + Fr(1, 10)) * want + h) - min(Fr(1, 2) * want - Fr(1, 2), (Fr(1, 2) + Fr(1, 10)) * want - h)
    height = max(Fr(1, 2) * want + Fr(1, 2), (1 + h + gap) * want + h) - min(Fr(1, 2) * want - Fr(1, 2), (1 + h + gap) * want - h)
    t.check(k["_shrunk_side"] == max(width, height), "tilted pair: shrunk side by hand")


def test_identity(t: Tally) -> None:
    rows, side = grid(Fr(1, 10**3), tilted=True)
    perm = [rows[k] for k in (4, 2, 0, 3, 1)]
    m = ID.measure(rows, side, perm, side)
    best = [r for r in m["by_symmetry"] if r["symmetry"] == "identity" and r["frame"] == "lower-left"][0]
    t.check(best["nearest_centre_one_to_one"] and best["moved_beyond"]["1e-9"] == 0, "identity: a permuted copy has no move")
    t.check(best["orientation_kept_exactly"] == 5, "identity: orientations kept")
    S = Fr(side[0], side[1])
    mir = [(pq(S - Fr(*r[0])), r[1], pq(-Fr(*r[2])), r[3]) for r in rows]
    m2 = ID.measure(rows, side, mir, side)
    t.check(m2["nearest_symmetry"]["lower-left"] == "mirror x -> S - x", "identity: a mirror is found")
    mm = [r for r in m2["by_symmetry"] if r["symmetry"] == "mirror x -> S - x" and r["frame"] == "lower-left"][0]
    t.check(mm["moved_beyond"]["1e-9"] == 0 and mm["orientation_kept_exactly"] == 5, "identity: the mirror moves nothing")
    moved = list(rows)
    moved[4] = (pq(Fr(*rows[4][0]) + Fr(1, 5)), rows[4][1], rows[4][2], rows[4][3])
    m3 = ID.measure(rows, side, moved, side)
    b3 = [r for r in m3["by_symmetry"] if r["symmetry"] == "identity" and r["frame"] == "lower-left"][0]
    t.check(b3["moved_beyond"]["1e-1"] == 1 and b3["moved_beyond"]["1e-9"] == 1, "identity: one square moved by 1/5")
    t.check(b3["largest_move"].startswith("2.0000000e-1"), "identity: the move printed as 2e-1")


def test_fmt(t: Tally) -> None:
    t.check(F.ceil_places(Fr(1, 3), 3) == "0.334", "ceil 1/3")
    t.check(F.floor_places(Fr(1, 3), 3) == "0.333", "floor 1/3")
    t.check(F.ceil_places(Fr(-1, 3), 3) == "-0.333", "ceil -1/3")
    t.check(F.ceil_places(Fr(5, 2), 0) == "3", "ceil 5/2")
    t.check(F.ceil_places(Fr(12345, 1000), 3) == "12.345", "ceil exact")
    t.check(F.nearest_places(Fr(2, 3), 2) == "0.67", "nearest 2/3")
    t.check(F.sci(Fr(1, 3), 5) == "3.3333e-1", "sci 1/3")
    t.check(F.sci(Fr(2, 3), 3) == "6.67e-1", "sci 2/3")
    t.check(F.sci(Fr(999999, 10**18), 3) == "1.00e-12", "sci rounding carry")
    t.check(F.sci(Fr(-1, 10**40), 2) == "-1.0e-40", "sci negative")
    t.check(F.terminating_places(Fr(5900396863307571, 500000000000000)) == 15, "terminating places")
    t.check(F.terminating_places(Fr(1, 3)) is None, "non-terminating")


def run_all() -> Tally:
    t = Tally()
    rng = random.Random(20261118)
    test_pairs(t)
    test_random(t, rng, 120)
    test_walls(t)
    test_shapes(t)
    test_twin(t)
    test_files(t)
    test_decide_files(t)
    test_contraction(t)
    test_identity(t)
    test_fmt(t)
    return t


def _mutants() -> list[tuple[str, Callable[[], Callable[[], None]]]]:
    def m_first_normals():
        orig = A.pair_numbers

        def broken(pi, pj):
            Ei, Ej = pi.E, pj.E
            dx = pj.X * Ei - pi.X * Ej
            dy = pj.Y * Ei - pi.Y * Ej
            pu = abs(dx * pi.a + dy * pi.b) * 2 * pj.r
            pv = abs(-dx * pi.b + dy * pi.a) * 2 * pj.r
            cosn = abs(pi.a * pj.a + pi.b * pj.b)
            sinn = abs(pi.a * pj.b - pi.b * pj.a)
            return max(pu, pv), (pi.r * pj.r + cosn + sinn) * Ei * Ej, 2 * Ei * Ej * pi.r * pj.r

        A.pair_numbers = broken

        def undo():
            A.pair_numbers = orig
        return undo

    def m_zero_is_overlap():
        orig = dict(D.A_PAIR)
        D.A_PAIR[0] = "overlap"

        def undo():
            D.A_PAIR.clear()
            D.A_PAIR.update(orig)
        return undo

    def m_open_halfplanes():
        orig = B._side

        def broken(p, q, x):
            v = orig(p, q, x)
            return v if v != 0 else mpq(-1, 10**60)
        B._side = broken

        def undo():
            B._side = orig
        return undo

    def m_no_diagonals():
        orig = B.unit_square

        def broken(pts):
            for k in range(4):
                if B._d2(pts[k], pts[(k + 1) % 4]) != 1:
                    return False, 0
            s2 = B.shoelace2(pts)
            return (True, 1) if s2 > 0 else (True, -1) if s2 < 0 else (False, 0)
        B.unit_square = broken

        def undo():
            B.unit_square = orig
        return undo

    def m_plus_sign():
        orig = R.SCALAR_RE
        import re
        R.SCALAR_RE = re.compile(r"[-+]?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?")

        def undo():
            R.SCALAR_RE = orig
        return undo

    def m_min_factor():
        orig = K.contraction

        def broken(rows, side):
            ip = [A.to_ipose(*r) for r in rows]
            fs = [f for f, _ in K.factors(ip) if f is not None]
            out = orig(rows, side)
            lam = min(fs)
            w, h, _, _ = K.extent(ip, lam)
            out["_lam"] = lam
            out["_shrunk_side"] = max(w, h)
            out["_margin"] = Fr(side[0], side[1]) - max(w, h)
            return out
        K.contraction = broken

        def undo():
            K.contraction = orig
        return undo

    def m_one_sense():
        orig = T.match

        def broken(listing, ref):
            r = orig(listing, ref)
            return r if r is None or r[1] == 1 else None
        T.match = broken

        def undo():
            T.match = orig
        return undo

    return [
        ("method A with only the first square's two normals", m_first_normals),
        ("method A counting a zero margin as overlap", m_zero_is_overlap),
        ("method B clipping with open half-planes", m_open_halfplanes),
        ("method B without its diagonal test", m_no_diagonals),
        ("a reader that takes a leading plus sign", m_plus_sign),
        ("the contraction taking the least contact factor", m_min_factor),
        ("the twin relation in one sense only", m_one_sense),
    ]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    t0 = time.process_time()
    t = run_all()
    mutants = []
    for name, make in _mutants():
        undo = make()
        try:
            tm = run_all()
            fails = len(tm.failed)
        except Exception as exc:  # a broken copy may also crash, which also catches it
            fails = -1
            name = f"{name} (raised {type(exc).__name__})"
        finally:
            undo()
        mutants.append({"mutant": name, "failed_checks": fails, "caught": fails != 0})
    passed = not t.failed and all(m["caught"] for m in mutants)
    out = {
        "program": "rb127_selftest.py",
        "verdict": "PASSED" if passed else "FAILED",
        "checks": t.passed + len(t.failed),
        "failed": t.failed[:100],
        "mutants": mutants,
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    Path(argv[1]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(out["verdict"], out["checks"], "checks,", len(t.failed), "failed;",
          ", ".join(f"{m['failed_checks']}" for m in mutants), "failures under the broken copies")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
