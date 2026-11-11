"""Self-test of the L96 reader and both methods, against cases derived by hand.

Usage: python -I -B l96_selftest.py OUT_JSON
"""

import json
import os
import random
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l96_check as C  # noqa: E402
import l96_clip as B  # noqa: E402
import l96_read as R  # noqa: E402
import l96_sat as A  # noqa: E402
from gmpy2 import mpq  # noqa: E402

E30 = F(1, 10**30)
cases = []


def fs(q):
    q = F(q)
    return f"{q.numerator}/{q.denominator}" if q.denominator != 1 else str(q.numerator)


def cert(side, sqs, comments=("# test",)):
    lines = list(comments) + [f"{len(sqs)} {fs(side)}"] + [" ".join(fs(v) for v in s) for s in sqs]
    return ("\n".join(lines) + "\n").encode()


def record(name, ok, detail=""):
    cases.append({"case": name, "ok": bool(ok), "detail": detail})


def pair_both(si, sj):
    """Margin by A and (class, area) by B for one pair given as (x, y, t) Fractions."""
    ma, _ = A.margin(A.square(*map(F, si)), A.square(*map(F, sj)))
    pi = B.corners(*(mpq(F(v).numerator, F(v).denominator) for v in si))
    pj = B.corners(*(mpq(F(v).numerator, F(v).denominator) for v in sj))
    cls, area = B.pair_class(pi, pj)
    return ma, cls, C.as_frac(area)


def expect_pair(name, si, sj, margin, cls, area):
    ma, cb, ab = pair_both(si, sj)
    ok = ma == margin and cb == cls and ab == area and A.classify(ma) == cls
    record(name, ok, f"A margin {ma}, B {cb} area {ab}")
    # Same pair, listed the other way round, and reflected in the line y = x.
    ma2, cb2, ab2 = pair_both(sj, si)
    record(name + " (swapped)", ma2 == margin and cb2 == cls and ab2 == area)
    tr = lambda s: (s[1], s[0], -F(s[2]))  # noqa: E731
    ma3, cb3, ab3 = pair_both(tr(si), tr(sj))
    record(name + " (transposed)", ma3 == margin and cb3 == cls and ab3 == area)


def main():
    third = F(1, 3)  # t = 1/3 gives cos 4/5, sin 3/5
    expect_pair("edge contact", (1, 1, 0), (2, 1, 0), 0, "contact", 0)
    expect_pair("edge apart 1e-30", (1, 1, 0), (2 + E30, 1, 0), E30, "clear", 0)
    expect_pair("edge overlap 1e-30", (1, 1, 0), (2 - E30, 1, 0), -E30, "overlap", E30)
    expect_pair("corner contact", (1, 1, 0), (2, 2, 0), 0, "contact", 0)
    expect_pair("corner overlap", (1, 1, 0), (2 - E30, 2 - E30, 0), -E30, "overlap", E30 * E30)
    bx = 1 + F(6, 5)
    expect_pair("3-4-5 vertex on edge", (1, 1, 0), (bx, 1, third), 0, "contact", 0)
    expect_pair("3-4-5 vertex 1e-30 in", (1, 1, 0), (bx - E30, 1, third), -E30, "overlap", F(25, 24) * E30 * E30)
    expect_pair("3-4-5 vertex 1e-30 out", (1, 1, 0), (bx + E30, 1, third), E30, "clear", 0)
    expect_pair("3-4-5 other sense on edge", (1, 1, 0), (bx, 1, -third), 0, "contact", 0)
    expect_pair("duplicate", (1, 1, 0), (1, 1, 0), -1, "overlap", 1)
    expect_pair("t = 1 is a quarter turn", (1, 1, 0), (1, 1, 1), -1, "overlap", 1)
    expect_pair("own 3-4-5 rotation", (1, 1, 0), (1, 1, third), F(-6, 5), "overlap", F(5, 6))

    # Walls, through the full driver.
    rec, _, _ = C.check_bytes(cert(1, [(F(1, 2), F(1, 2), 0)]))
    record("unit box, four contacts", rec["verdict"] == "ACCEPT" and len(rec["walls"]["contacts"]) == 4)
    rec, _, _ = C.check_bytes(cert(1 - E30, [(F(1, 2), F(1, 2), 0)]))
    record("unit box short by 1e-30", rec["verdict"] == "REFUSE" and "outside" in rec["problems"][0])
    for t in (third, -third):
        rec, _, _ = C.check_bytes(cert(F(7, 5), [(F(7, 10), F(7, 10), t)]))
        record(f"3-4-5 in 7/5 box, t={t}", rec["verdict"] == "ACCEPT" and len(rec["walls"]["contacts"]) == 4)
        rec, _, _ = C.check_bytes(cert(F(7, 5), [(F(7, 10) - E30, F(7, 10), t)]))
        record(f"3-4-5 1e-30 past the left wall, t={t}", rec["verdict"] == "REFUSE")
    rec, _, _ = C.check_bytes(cert(2, [(F(1, 2), F(1, 2), 0), (F(3, 2), F(1, 2), 0), (F(1, 2), F(3, 2), 0), (F(3, 2), F(3, 2), 0)]))
    record("2x2 grid", rec["verdict"] == "ACCEPT" and len(rec["pairs"]["contacts"]) == 6)
    rec, _, _ = C.check_bytes(cert(2, [(F(1, 2), F(1, 2), 0), (F(1, 2), F(1, 2), 0)]))
    record("duplicate refused by driver", rec["verdict"] == "REFUSE" and rec["pairs"]["overlaps_A"] == [[1, 2]])

    # The reader: refusals, each for its own reason, and acceptances.
    good = cert(2, [(F(1, 2), F(1, 2), 0)])
    bad = {
        "no final newline": good[:-1],
        "count short": b"2 2\n1/2 1/2 0\n",
        "count long": b"1 2\n1/2 1/2 0\n3/2 1/2 0\n",
        "decimal": b"1 2\n0.5 1/2 0\n",
        "zero denominator": b"1 2\n1/0 1/2 0\n",
        "leading zero": b"1 2\n01/2 1/2 0\n",
        "denominator leading zero": b"1 2\n1/02 1/2 0\n",
        "negative zero": b"1 2\n1/2 1/2 -0\n",
        "four fields": b"1 2\n1/2 1/2 0 0\n",
        "two fields": b"1 2\n1/2 1/2\n",
        "comment after header": b"1 2\n# x\n1/2 1/2 0\n",
        "blank line": b"1 2\n\n1/2 1/2 0\n",
        "double space": b"1 2\n1/2  1/2 0\n",
        "carriage return": b"1 2\r\n1/2 1/2 0\r\n",
        "tab": b"1 2\n1/2\t1/2 0\n",
        "non-ASCII": "1 2\n1/2 1/2 0 é\n".encode(),
        "negative side": b"1 -2\n1/2 1/2 0\n",
        "zero n": b"0 2\n",
        "fractional n": b"3/2 2\n1/2 1/2 0\n",
        "header three fields": b"1 2 3\n1/2 1/2 0\n",
        "trailing space": b"1 2\n1/2 1/2 0 \n",
        "plus sign": b"1 2\n+1/2 1/2 0\n",
        "empty": b"",
    }
    for name, data in bad.items():
        try:
            R.read_cert(data)
            record("reader refuses " + name, False)
        except R.ReadError:
            record("reader refuses " + name, True)
    for name, data in {"commented": good, "no comments": b"1 2\n1/2 1/2 0\n"}.items():
        try:
            R.read_cert(data)
            record("reader accepts " + name, True)
        except R.ReadError:
            record("reader accepts " + name, False)
    record("reader counts a non-canonical scalar", R.read_cert(b"1 4/2\n1/2 1/2 0\n")["noncanonical_scalars"] == 1)

    # Random pairs closed along their centre line to exact contact, by the SAT formula,
    # then decided by both methods at contact and 1e-30 either side.
    rng = random.Random(96)
    closed = 0
    for _ in range(300):
        ti = F(rng.randint(-40, 40), rng.randint(1, 41))
        tj = F(rng.randint(-40, 40), rng.randint(1, 41))
        xi, yi = F(rng.randint(0, 10**6), 10**6), F(rng.randint(0, 10**6), 10**6)
        ang = F(rng.randint(-1000, 1000), 997)
        dx, dy = 1 + ang * ang, 2 * ang  # any rational direction, scaled
        scale = F(3, 1) / (abs(dx) + abs(dy))
        dx, dy = dx * scale, dy * scale
        si, sj = A.square(xi, yi, ti), A.square(xi + dx, yi + dy, tj)
        lam = None
        for ax, ay, other_i in ((si[2], si[3], False), (-si[3], si[2], False), (sj[2], sj[3], True), (-sj[3], sj[2], True)):
            proj = abs(ax * dx + ay * dy)
            if proj == 0:
                continue
            H = F(1, 2) + A.support(ax, ay, si if other_i else sj)
            cand = 1 - H / proj
            lam = cand if lam is None or cand > lam else lam
        for delta, want in ((0, "contact"), (E30, "overlap"), (-E30, "clear")):
            l2 = lam + delta
            pj = (xi + dx * (1 - l2), yi + dy * (1 - l2), tj)
            ma, cb, _ = pair_both((xi, yi, ti), pj)
            if A.classify(ma) != want or cb != want:
                record(f"closed pair {closed} at {delta}", False, f"A {A.classify(ma)} B {cb}")
                break
        else:
            closed += 1
    record(f"300 random pairs closed along the centre line ({closed} passed)", closed == 300)

    # Both prunes against brute force on random dense configurations.
    agree = 0
    for trial in range(25):
        sqs = []
        for _ in range(30):
            sqs.append(((rng.randint(0, 6000), 1000), (rng.randint(0, 6000), 1000), (rng.randint(-9, 9), rng.randint(1, 9))))
        ra = A.decide((7, 1), sqs)
        rb = B.decide((7, 1), sqs)
        fa = [A.square(F(*a), F(*b), F(*c)) for a, b, c in sqs]
        pb = [B.corners(mpq(*a), mpq(*b), mpq(*c)) for a, b, c in sqs]
        ok = True
        for i in range(30):
            for j in range(i + 1, 30):
                m, _ = A.margin(fa[i], fa[j])
                cls_brute = A.classify(m)
                cls_b, _ = B.pair_class(pb[i], pb[j])
                key = (i + 1, j + 1)
                cls_a = A.classify(ra["margins"][key][0]) if key in ra["margins"] else "clear"
                cls_bp = rb["classes"].get(key, "clear")
                if not (cls_brute == cls_b == cls_a == cls_bp):
                    ok = False
        agree += ok
    record(f"prunes equal brute force on 25 random sets of 30 ({agree} passed)", agree == 25)

    passed = all(c["ok"] for c in cases)
    out = {"programs": C.program_digests(), "selftest": "l96_selftest.py", "cases": len(cases), "result": "PASSED" if passed else "FAILED", "detail": cases}
    with open(sys.argv[1], "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(out["result"], len(cases), [c["case"] for c in cases if not c["ok"]])


if __name__ == "__main__":
    main()
