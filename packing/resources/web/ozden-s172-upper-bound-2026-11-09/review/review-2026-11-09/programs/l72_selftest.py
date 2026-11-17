"""Self-test of the L72 clean-room checker (lane L72, bead think-qqyg).

Usage: python -I -B l72_selftest.py OUT.json

Holds methods A and B to known answers, to random pairs taken exactly to contact and
1e-30 either side, to random squares taken to a wall and past it, and holds the reader to
malformed files it must refuse. Exit status 0 and verdict PASSED when every case holds.
"""

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction  # noqa: E402

from gmpy2 import mpq  # noqa: E402

import l72_clip as clipm  # noqa: E402
import l72_reader as reader  # noqa: E402
import l72_sat as sat  # noqa: E402
import l72_util as util  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
EPS = Fraction(1, 10**30)
F = Fraction

results = []


def record(name, ok, detail=""):
    results.append({"case": name, "ok": bool(ok), "detail": detail})


# ---------- construction helpers (exact Fractions; corners to raw integers) ----------


def raw(P):
    return tuple((F(x).numerator, F(x).denominator, F(y).numerator, F(y).denominator) for x, y in P)


def sq_from(c, u, ccw=True):
    """Unit square with centre c and edge direction u (u.u == 1)."""
    f = (-u[1], u[0])
    h = (u[0] / 2, u[1] / 2)
    g = (f[0] / 2, f[1] / 2)
    p0 = (c[0] - h[0] - g[0], c[1] - h[1] - g[1])
    p1 = (c[0] + h[0] - g[0], c[1] + h[1] - g[1])
    p2 = (c[0] + h[0] + g[0], c[1] + h[1] + g[1])
    p3 = (c[0] - h[0] + g[0], c[1] - h[1] + g[1])
    P = [p0, p1, p2, p3]
    if not ccw:
        P = [p0, p3, p2, p1]
    return P


def shift(P, d):
    return [(x + d[0], y + d[1]) for x, y in P]


def both_pair(Pf, Qf):
    """Decide one pair by both methods from Fraction corners. Returns (margin, area, ne, ok)."""
    ra, rb = raw(Pf), raw(Qf)
    PA, QA = sat.corners_frac(ra), sat.corners_frac(rb)
    sa, sb = sat.square(PA), sat.square(QA)
    PB, QB = clipm.corners_q(ra), clipm.corners_q(rb)
    ta, tb = clipm.square(PB), clipm.square(QB)
    if not (sa[0] and sb[0] and ta[0] and tb[0]):
        return None, None, None, False
    m, _ = sat.pair_margin(PA, sa[2], sat.own_ranges(PA, sa[2]), QA, sb[2], sat.own_ranges(QA, sb[2]))
    a, ne = clipm.pair(PB, clipm.halfplanes(QB, tb[1]))
    a2, ne2 = clipm.pair(QB, clipm.halfplanes(PB, ta[1]))
    sym = (a == a2) and (ne == ne2)
    return m, a, ne, sym


def expect_pair(name, P, Q, margin, area, cls):
    for sense in (True, False):
        Pp = P if sense else [P[0], P[3], P[2], P[1]]
        Qq = Q if sense else [Q[0], Q[3], Q[2], Q[1]]
        m, a, ne, sym = both_pair(Pp, Qq)
        if m is None:
            record(f"{name} ({'ccw' if sense else 'cw'})", False, "a square was refused")
            continue
        ok = (
            m == margin
            and a == mpq(area.numerator, area.denominator)
            and sat.classify(m) == cls
            and clipm.classify(a, ne) == cls
            and sym
        )
        record(
            f"{name} ({'ccw' if sense else 'cw'})",
            ok,
            f"margin {util.frac_str(m)}, area {a}, class A {sat.classify(m)}, B {clipm.classify(a, ne)}",
        )


def known_answers():
    A = sq_from((F(1, 2), F(1, 2)), (F(1), F(0)))
    # edge contact, and 1e-30 overlap
    B = shift(A, (F(1), F(0)))
    expect_pair("edge contact", A, B, F(0), F(0), "touching")
    expect_pair("edge overlap 1e-30", A, shift(B, (-EPS, F(0))), -EPS, EPS, "overlapping")
    expect_pair("edge apart 1e-30", A, shift(B, (EPS, F(0))), EPS, F(0), "apart")
    # corner contact
    C = shift(A, (F(1), F(1)))
    expect_pair("corner contact", A, C, F(0), F(0), "touching")
    expect_pair("corner overlap 1e-30", A, shift(C, (-EPS, -EPS)), -EPS, EPS * EPS, "overlapping")
    # 3-4-5 vertex on an edge: corner p0 = (1, 1/2), u = (3/5, 4/5), f = (4/5, -3/5)
    u = (F(3, 5), F(4, 5))
    f = (F(4, 5), F(-3, 5))
    p0 = (F(1), F(1, 2))
    D = [p0, (p0[0] + u[0], p0[1] + u[1]), (p0[0] + u[0] + f[0], p0[1] + u[1] + f[1]), (p0[0] + f[0], p0[1] + f[1])]
    expect_pair("3-4-5 vertex-edge contact", A, D, F(0), F(0), "touching")
    expect_pair(
        "3-4-5 vertex-edge overlap 1e-30", A, shift(D, (-EPS, F(0))), -EPS, F(25, 24) * EPS * EPS, "overlapping"
    )
    # duplicate
    expect_pair("duplicate", A, A, F(-1), F(1), "overlapping")
    # own rotation about the same centre
    R1 = sq_from((F(1, 2), F(1, 2)), (F(3, 5), F(4, 5)))
    R2 = sq_from((F(1, 2), F(1, 2)), (F(4, 5), F(3, 5)))
    expect_pair("own rotation by (3/5, 4/5)", A, R1, F(-6, 5), F(5, 6), "overlapping")
    expect_pair("own rotation by (4/5, 3/5)", A, R2, F(-6, 5), F(5, 6), "overlapping")


def walls():
    S = F(3)
    SB = mpq(3)
    base = sq_from((F(3, 2), F(3, 2)), (F(3, 5), F(4, 5)))
    for w, d in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
        PA = sat.corners_frac(raw(base))
        cl = sat.wall_clearances(PA, S)[w]
        for label, step, clsA_exp in (("contact", cl, "contact"), ("past", cl + EPS, "outside")):
            moved = shift(base, (d[0] * step, d[1] * step))
            r = raw(moved)
            cA = sat.wall_class(sat.wall_clearances(sat.corners_frac(r), S)[w])
            cB = clipm.wall_classes(clipm.corners_q(r), SB)[w]
            ia = clipm.inside_area(clipm.corners_q(r), SB)
            ok = cA == clsA_exp and cB == clsA_exp and ((ia == 1) == (label == "contact"))
            record(f"wall {sat.WALLS[w]} {label}", ok, f"A {cA}, B {cB}, inside area {ia}")


def refused_shapes():
    A = sq_from((F(1, 2), F(1, 2)), (F(1), F(0)))
    cases = {
        "scaled by 1 + 1e-30": [(x * (1 + EPS), y * (1 + EPS)) for x, y in A],
        "rhombus u=(1,0), f=(3/5,4/5)": [(F(0), F(0)), (F(1), F(0)), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))],
        "bowtie order p0 p2 p1 p3": [A[0], A[2], A[1], A[3]],
        "p2 moved 1e-30 in x": [A[0], A[1], (A[2][0] + EPS, A[2][1]), A[3]],
        "rectangle 1 x (1 + 1e-30)": [A[0], A[1], (A[2][0], A[2][1] + EPS), (A[3][0], A[3][1] + EPS)],
        "zigzag of unit edges": [(F(0), F(0)), (F(1), F(0)), (F(0), F(0)), (F(1), F(0))],
        "one point": [(F(1), F(1))] * 4,
    }
    for name, P in cases.items():
        r = raw(P)
        a = sat.square(sat.corners_frac(r))
        b = clipm.square(clipm.corners_q(r))
        record(f"refuse shape: {name}", (not a[0]) and (not b[0]), f"A: {a[3]}; B: {b[2]}")


def rand_unit(rng):
    while True:
        b = rng.randint(1, 10**6)
        a = rng.randint(-b + 1, b - 1)
        t = F(a, b)
        if abs(t) < 1:
            return ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))


def rand_rat(rng, lo, hi):
    den = rng.randint(1, 10**9)
    return F(rng.randint(lo * den, hi * den), den)


def contact_parameter(P, Q, d):
    """Least s > 0 at which Q + s d first touches P (P, Q concentric-overlapping at s = 0)."""
    sP = sat.square(P)
    sQ = sat.square(Q)
    roots = []
    for a in (sP[2][0], sP[2][1], sQ[2][0], sQ[2][1]):
        loP, hiP = sat.proj_range(P, a)
        loQ, hiQ = sat.proj_range(Q, a)
        da = d[0] * a[0] + d[1] * a[1]
        for alpha, beta in ((loQ - hiP, da), (loP - hiQ, -da)):
            if beta > 0:
                roots.append(-alpha / beta)
    return min(roots)


def random_pairs(count, rng):
    bad = 0
    for k in range(count):
        c = (rand_rat(rng, 1, 4), rand_rat(rng, 1, 4))
        P = sq_from(c, rand_unit(rng), rng.random() < 0.5)
        Q0 = sq_from(c, rand_unit(rng), rng.random() < 0.5)
        while True:
            d = (rand_rat(rng, -2, 2), rand_rat(rng, -2, 2))
            if d != (0, 0):
                break
        PA = sat.corners_frac(raw(P))
        QA = sat.corners_frac(raw(Q0))
        s = contact_parameter(PA, QA, d)
        outs = []
        for label, ss, exp in (("short", s - EPS, "overlapping"), ("contact", s, "touching"), ("beyond", s + EPS, "apart")):
            Q = shift(Q0, (d[0] * ss, d[1] * ss))
            m, a, ne, sym = both_pair(P, Q)
            okk = m is not None and sat.classify(m) == exp and clipm.classify(a, ne) == exp and sym
            if label == "contact":
                okk = okk and m == 0 and a == 0
            outs.append(okk)
        if not all(outs):
            bad += 1
            if bad <= 5:
                record(f"random pair {k}", False, f"outcomes {outs}")
    record(f"{count} random pairs to contact and 1e-30 either side", bad == 0, f"{bad} failed")


def random_walls(count, rng):
    S = F(10)
    SB = mpq(10)
    bad = 0
    for k in range(count):
        c = (rand_rat(rng, 2, 8), rand_rat(rng, 2, 8))
        P = sq_from(c, rand_unit(rng), rng.random() < 0.5)
        w = rng.randrange(4)
        d = [(-1, 0), (1, 0), (0, -1), (0, 1)][w]
        cl = sat.wall_clearances(sat.corners_frac(raw(P)), S)[w]
        ok = True
        for step, exp in ((cl, "contact"), (cl + EPS, "outside"), (cl - EPS, "clear")):
            Q = shift(P, (d[0] * step, d[1] * step))
            r = raw(Q)
            cA = sat.wall_class(sat.wall_clearances(sat.corners_frac(r), S)[w])
            cB = clipm.wall_classes(clipm.corners_q(r), SB)[w]
            ia = clipm.inside_area(clipm.corners_q(r), SB)
            ok = ok and cA == exp and cB == exp and ((ia == 1) == (exp != "outside"))
        if not ok:
            bad += 1
    record(f"{count} random squares to a wall, past it and short of it", bad == 0, f"{bad} failed")


# ---------- reader ----------

BASE_YAML = """softschema:
  contract: packing.squares:Witness/v2
  schema: witness.schema.yaml
  envelope: witness
  status: enforced
witness:
  id: W-selftest
  n: 2
  side: 2
  square_size: '1'
  representation: corners
  scalar:
    kind: rational
  coordinates:
    origin: lower-left
    axes: x-right-y-up
    angle_unit: not-applicable
  squares:
  - id: 1
    corners:
    - - 0
      - 0
    - - 1
      - 0
    - - 1
      - 1
    - - 0
      - 1
  - id: 2
    corners:
    - - 1
      - 0
    - - 2
      - 0
    - - 2
      - 1
    - - 2/2
      - 1
  claim:
    coordinate_provenance: verified
    method: exact-algebraic
    limitations: self-test
  source:
    path: none
  certificate:
    kind: test
"""


def base_json():
    t = reader.yaml_tree(BASE_YAML)
    w = t["witness"]
    w["n"] = 2
    for s in w["squares"]:
        s["id"] = int(s["id"])
    return json.dumps(t)


def reader_cases():
    ok_read = reader.read_texts(BASE_YAML, base_json())
    record("reader accepts the base file and its twin", ok_read["n"] == 2, str(ok_read["meta"]["json_twin"]))
    record(
        "reader counts a scalar not in lowest terms",
        ok_read["meta"]["scalars_not_in_lowest_terms"] == 1,
        str(ok_read["meta"]["scalars_not_in_lowest_terms"]),
    )
    Y = BASE_YAML
    variants = {
        "extra top-level key": Y + "extra: 1\n",
        "missing softschema": "witness:\n" + Y.split("\nwitness:\n", 1)[1],
        "wrong contract": Y.replace("packing.squares:Witness/v2", "packing.squares:Witness/v1"),
        "wrong envelope": Y.replace("envelope: witness", "envelope: other"),
        "missing claim": Y.split("  claim:\n")[0] + "  source:\n    path: none\n",
        "unknown witness key": Y.replace("  square_size: '1'\n", "  square_size: '1'\n  colour: red\n"),
        "n not an integer": Y.replace("  n: 2\n", "  n: two\n"),
        "n mismatch": Y.replace("  n: 2\n", "  n: 3\n"),
        "decimal side": Y.replace("  side: 2\n", "  side: '2.5'\n"),
        "side over zero": Y.replace("  side: 2\n", "  side: 3/0\n"),
        "negative side": Y.replace("  side: 2\n", "  side: -3\n"),
        "zero side": Y.replace("  side: 2\n", "  side: 0\n"),
        "square_size 2": Y.replace("square_size: '1'", "square_size: '2'"),
        "center-angle": Y.replace("representation: corners", "representation: center-angle"),
        "decimal scalars": Y.replace("kind: rational", "kind: decimal"),
        "centred origin": Y.replace("origin: lower-left", "origin: container-center"),
        "axes down": Y.replace("axes: x-right-y-up", "axes: x-right-y-down"),
        "duplicate key": Y.replace("  side: 2\n", "  side: 2\n  side: 3\n"),
        "duplicate id": Y.replace("  - id: 2\n", "  - id: 1\n"),
        "three corners": Y.replace("    - - 2/2\n      - 1\n", ""),
        "five corners": Y.replace("    - - 2/2\n      - 1\n", "    - - 2/2\n      - 1\n    - - 1\n      - 1\n"),
        "three coordinates": Y.replace("    - - 2/2\n      - 1\n", "    - - 2/2\n      - 1\n      - 1\n"),
        "exponent": Y.replace("    - - 2\n      - 0\n", "    - - 2e0\n      - 0\n"),
        "space inside a quoted scalar": Y.replace("    - - 2\n      - 0\n", "    - - ' 2'\n      - 0\n"),
        "leading zero": Y.replace("    - - 2\n      - 0\n", "    - - 02\n      - 0\n"),
        "negative denominator": Y.replace("    - - 2/2\n", "    - - 1/-1\n"),
        "minus zero": Y.replace("    - - 2\n      - 0\n", "    - - 2\n      - -0\n"),
        "plus sign": Y.replace("    - - 2\n      - 0\n", "    - - +2\n      - 0\n"),
        "anchor and alias": Y.replace("  - id: 1\n    corners:\n", "  - id: 1\n    corners: &c\n", 1).replace(
            "  - id: 2\n    corners:\n    - - 1\n      - 0\n    - - 2\n      - 0\n    - - 2\n      - 1\n    - - 2/2\n      - 1\n",
            "  - id: 2\n    corners: *c\n",
        ),
        "explicit tag": Y.replace("  n: 2\n", "  n: !!int 2\n"),
        "extra key on a square": Y.replace("  - id: 2\n    corners:\n", "  - id: 2\n    center: [0, 0]\n    corners:\n"),
        "two documents": Y + "---\nwitness: {}\n",
        "empty file": "",
        "squares not a list": Y.split("  squares:\n")[0] + "  squares: none\n" + "  claim:\n" + Y.split("  claim:\n")[1],
        "id zero": Y.replace("  - id: 2\n", "  - id: 0\n"),
        "id not an integer": Y.replace("  - id: 2\n", "  - id: two\n"),
    }
    for name, text in variants.items():
        try:
            reader.read_texts(text)
        except reader.ReadError as exc:
            record(f"reader refuses: {name}", True, str(exc)[:120])
        else:
            record(f"reader refuses: {name}", False, "accepted")
    J = base_json()
    jvariants = {
        "twin with a changed coordinate": J.replace('"2", "1"]', '"2", "3"]', 1),
        "twin with a float": J.replace('"n": 2', '"n": 2.0'),
        "twin with a duplicate key": J.replace('"n": 2', '"n": 2, "n": 2'),
        "twin with a boolean": J.replace('"n": 2', '"n": true'),
        "twin with a missing square": J.replace('{"id": 2', '{"idx": 2'),
    }
    for name, text in jvariants.items():
        if text == J:
            record(f"reader refuses: {name}", False, "variant construction did not change the twin")
            continue
        try:
            reader.read_texts(BASE_YAML, text)
        except reader.ReadError as exc:
            record(f"reader refuses: {name}", True, str(exc)[:120])
        else:
            record(f"reader refuses: {name}", False, "accepted")


def main(argv):
    out = argv[1] if len(argv) > 1 else None
    t0 = util.cpu_seconds()
    rng = random.Random(20261109)
    known_answers()
    walls()
    refused_shapes()
    reader_cases()
    random_pairs(3000, rng)
    random_walls(1000, rng)
    failed = [r for r in results if not r["ok"]]
    verdict = "PASSED" if not failed else "FAILED"
    payload = {
        "program": "l72_selftest.py",
        "lane": "L72",
        "bead": "think-qqyg",
        "environment": util.environment(),
        "checker_digests": util.program_digests(
            [os.path.join(HERE, f) for f in ("l72_util.py", "l72_reader.py", "l72_sat.py", "l72_clip.py", "l72_check.py", "l72_selftest.py")]
        ),
        "verdict": verdict,
        "cases": len(results),
        "failed": failed,
        "results": results,
        "cpu_seconds": round(util.cpu_seconds() - t0, 2),
    }
    if out:
        util.write_receipt(out, payload)
    print(verdict, f"{len(results)} cases, {len(failed)} failed, {payload['cpu_seconds']} s")
    for r in failed[:20]:
        print("  FAILED", r["case"], r["detail"])
    return 0 if verdict == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
