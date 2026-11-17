"""Self-test of the reader and of both exact methods, with known answers and a random sweep.

Usage (from packing/, Python 3.14):  python -I self_test.py OUT.json

Known answers: edge contact, 1e-30 overlap and 1e-30 clearance of aligned squares; a
corner-to-corner contact; a 3-4-5 rotated square (t = 1/2) with a vertex exactly on an
aligned square's edge, then 1e-30 into it and 1e-30 off it; the reversed sense of the
same; a duplicated square; squares in the box at exact wall contact and 1e-30 past it.
Random sweep: pairs of squares with random rational half-angle tangents and centres
within reach, plus each pair moved to exact contact along its separating axis and
1e-30 past it; both methods must give the same three-way class on every one.
Reader: a valid file parses, and each malformed variant is refused.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exact_geometry as eg  # noqa: E402
from cert_reader import parse_text  # noqa: E402

E30 = F(1, 10**30)
H = F(1, 2)


def cls_a(p, q):
    g, _ = eg.pair_gap_a(p, q)
    return ("separated" if g > 0 else "touching" if g == 0 else "overlapping"), g


def cls_b(p, q):
    poly = list(p)
    for k in range(4):
        ax, ay = q[k]
        bx, by = q[(k + 1) % 4]
        poly = eg._clip(poly, ax, ay, bx, by)
        if not poly:
            return "separated", 0
    a = eg.area_b(poly)
    return ("touching" if a == 0 else "overlapping"), a


def both(si, sj, sense=1, hi=H, hj=H):
    pa, qa = eg.square_a(*si, h=hi, sense=sense), eg.square_a(*sj, h=hj, sense=sense)
    pb, qb = eg.square_b(*si, h=hi, sense=sense), eg.square_b(*sj, h=hj, sense=sense)
    ca, g = cls_a(pa, qa)
    ca2, g2 = cls_a(qa, pa)
    cb, a = cls_b(pb, qb)
    cb2, a2 = cls_b(qb, pb)
    if g != g2 or ca != ca2 or cb != cb2 or a != a2:
        raise AssertionError("asymmetric result")
    return ca, cb, g, a


def wall_both(s, side, h=H, sense=1):
    c = eg.wall_clearance_a(eg.square_a(*s, h=h, sense=sense), side)
    d = eg.wall_deficit_b(eg.square_b(*s, h=h, sense=sense), side)
    return ("inside" if c >= 0 else "outside"), ("inside" if d == 0 else "outside"), c, d


def main() -> None:
    out_path = sys.argv[1]
    t0 = time.process_time()
    checks: list[dict] = []

    def expect(name, got_a, got_b, want, extra=None):
        ok = got_a == want and got_b == want
        checks.append({"case": name, "want": want, "method_a": got_a, "method_b": got_b, "ok": ok, **(extra or {})})
        if not ok:
            print("FAIL", name, got_a, got_b, want)

    z = F(0)
    # aligned squares
    a, b, g, ar = both((H, H, z), (F(3, 2), H, z))
    expect("aligned edge contact", a, b, "touching", {"gap": str(g), "area": str(ar)})
    a, b, g, ar = both((H, H, z), (F(3, 2) - E30, H, z))
    expect("aligned overlap 1e-30", a, b, "overlapping", {"gap": str(g), "area": str(ar)})
    assert g == -E30 and ar == E30, (g, ar)
    a, b, g, ar = both((H, H, z), (F(3, 2) + E30, H, z))
    expect("aligned clearance 1e-30", a, b, "separated", {"gap": str(g)})
    assert g == E30
    a, b, g, ar = both((H, H, z), (F(3, 2), F(3, 2), z))
    expect("aligned corner-to-corner contact", a, b, "touching")
    a, b, g, ar = both((H, H, z), (F(3, 2) - E30, F(3, 2) - E30, z))
    expect("aligned corner overlap 1e-30 x 1e-30", a, b, "overlapping", {"area": str(ar)})
    assert ar == E30 * E30
    # 3-4-5 square, t = 1/2: lowest corner offset (1/10, -7/10)
    t = F(1, 2)
    a, b, g, ar = both((z, z, z), (z, F(6, 5), t))
    expect("3-4-5 vertex on edge", a, b, "touching", {"gap": str(g)})
    a, b, g, ar = both((z, z, z), (z, F(6, 5) - E30, t))
    expect("3-4-5 vertex 1e-30 into edge", a, b, "overlapping", {"area": str(ar)})
    a, b, g, ar = both((z, z, z), (z, F(6, 5) + E30, t))
    expect("3-4-5 vertex 1e-30 off edge", a, b, "separated")
    a, b, g, ar = both((z, z, z), (z, F(6, 5), t), sense=-1)
    expect("3-4-5 vertex on edge, reversed sense", a, b, "touching")
    # a 3-4-5 vertex placed where only the reversed sense touches:
    # sense +1 lowest corner (1/10, -7/10); at centre (-3/5, 6/5) it lands at (-1/2, 1/2),
    # the aligned square's top-left corner (touching); reversed sense lowest corner is
    # (-1/10, -7/10), landing at (-7/10, 1/2), off the square: separated.
    a, b, g, ar = both((z, z, z), (F(-3, 5), F(6, 5), t))
    expect("3-4-5 vertex on a corner", a, b, "touching")
    a, b, g, ar = both((z, z, z), (F(-3, 5), F(6, 5), t), sense=-1)
    expect("3-4-5 vertex beside a corner, reversed sense", a, b, "separated")
    # duplicate
    a, b, g, ar = both((F(5, 7), F(3, 11), F(2, 9)), (F(5, 7), F(3, 11), F(2, 9)))
    expect("duplicated square", a, b, "overlapping", {"gap": str(g), "area": str(ar)})
    assert ar == 1
    # nested: a half-size square inside a unit square
    a, b, g, ar = both((z, z, F(1, 3)), (F(1, 100), z, F(2, 7)), hj=F(1, 4))
    expect("small square inside", a, b, "overlapping")
    # walls
    for name, s, side, h, want in (
        ("unit square at the corner, box 1", (H, H, z), F(1), H, "inside"),
        ("unit square, box 1 - 1e-30", (H, H, z), 1 - E30, H, "outside"),
        ("3-4-5 square touching all four walls, box 7/5", (F(7, 10), F(7, 10), t), F(7, 5), H, "inside"),
        ("3-4-5 square, box 7/5 - 1e-30", (F(7, 10), F(7, 10), t), F(7, 5) - E30, H, "outside"),
        ("3-4-5 square moved 1e-30 left", (F(7, 10) - E30, F(7, 10), t), F(7, 5), H, "outside"),
        ("square below the floor", (F(1), F(-1, 2), z), F(3), H, "outside"),
    ):
        wa, wb, c, d = wall_both(s, side, h)
        expect("wall: " + name, wa, wb, want, {"clearance": str(c), "deficit": str(d)})
    # every square's own area is exactly 1
    for tt in (z, F(1, 2), F(-7, 3), F(10**35 - 1, 10**35), F(123456789, 987654321)):
        assert eg.area_b(eg.square_b(z, z, tt)) == 1
        cs = eg.frame_a(tt)
        assert cs[0] ** 2 + cs[1] ** 2 == 1

    # random sweep
    rng = random.Random(20261105)
    agree = 0
    tally = {"separated": 0, "touching": 0, "overlapping": 0}
    constructed = {"touching": 0, "overlapping": 0, "separated": 0}
    disagreements = []
    for trial in range(3000):
        def rt():
            r = rng.random()
            if r < 0.25:
                return F(0)
            if r < 0.5:
                return F(rng.randint(-50, 50), rng.randint(1, 50))
            return F(rng.randint(-(10**30), 10**30), 10**30 + rng.randint(1, 10**20))
        si = (F(rng.randint(0, 10**12), 10**12), F(rng.randint(0, 10**12), 10**12), rt())
        sj = (si[0] + F(rng.randint(-1600, 1600), 1000), si[1] + F(rng.randint(-1600, 1600), 1000), rt())
        a, b, g, ar = both(si, sj)
        tally[a] += 1
        if a == b:
            agree += 1
        else:
            disagreements.append(trial)
        # move j to exact contact along the axis giving the gap, then 1e-30 past it
        pa, qa = eg.square_a(*si), eg.square_a(*sj)
        g, k = eg.pair_gap_a(pa, qa)
        ax, ay = (pa[1] + qa[1])[k]
        # orientation: is j above i along the axis?
        pi = [px * ax + py * ay for (px, py) in pa[0]]
        pj = [px * ax + py * ay for (px, py) in qa[0]]
        sign = 1 if (min(pj) - max(pi)) == g else -1
        for extra, label in ((F(0), "contact"), (E30, "past")):
            m = g + extra
            sj2 = (sj[0] - sign * m * ax, sj[1] - sign * m * ay, sj[2])
            a2, b2, g2, _ = both(si, sj2)
            constructed[a2] += 1
            if a2 != b2:
                disagreements.append((trial, label))
            if label == "contact" and g2 < 0:
                disagreements.append((trial, "contact went negative"))
    # reader
    good = b"# c\n2 3/1\n1/2 1/2 0\n3/2 1/2 -1/3\n"
    parse_text(good)
    bad_variants = {
        "blank line": b"# c\n2 3\n\n1/2 1/2 0\n3/2 1/2 0\n",
        "CRLF": good.replace(b"\n", b"\r\n"),
        "no final LF": good[:-1],
        "count mismatch": b"3 3\n1/2 1/2 0\n3/2 1/2 0\n",
        "four tokens": b"2 3\n1/2 1/2 0 0\n3/2 1/2 0\n",
        "decimal token": b"2 3\n0.5 1/2 0\n3/2 1/2 0\n",
        "zero denominator": b"2 3\n1/0 1/2 0\n3/2 1/2 0\n",
        "plus sign": b"2 3\n+1/2 1/2 0\n3/2 1/2 0\n",
        "underscore": b"2 3\n1_0/2 1/2 0\n3/2 1/2 0\n",
        "double space": b"2 3\n1/2  1/2 0\n3/2 1/2 0\n",
        "zero count": b"0 3\n",
        "negative denominator": b"2 3\n1/-2 1/2 0\n3/2 1/2 0\n",
        "exponent": b"2 3\n1e0 1/2 0\n3/2 1/2 0\n",
        "non-ascii digit": "2 3\n١/2 1/2 0\n3/2 1/2 0\n".encode(),
    }
    reader = {}
    for name, raw in bad_variants.items():
        try:
            parse_text(raw)
            reader[name] = "ACCEPTED (bad)"
        except (ValueError, UnicodeDecodeError):
            reader[name] = "refused"
    ok_all = (
        all(c["ok"] for c in checks)
        and not disagreements
        and all(v == "refused" for v in reader.values())
    )
    result = {
        "ok": ok_all,
        "known_answers": checks,
        "random_pairs": 3000,
        "random_classes": tally,
        "random_agree": agree,
        "constructed_contact_and_past": constructed,
        "disagreements": disagreements[:20],
        "reader_refusals": reader,
        "cpu_seconds": round(time.process_time() - t0, 3),
    }
    Path(out_path).write_text(json.dumps(result, indent=1) + "\n")
    print("self-test", "PASS" if ok_all else "FAIL", "known", sum(c["ok"] for c in checks), "/", len(checks),
          "random agree", agree, tally, "constructed", constructed, "reader", sorted(set(reader.values())),
          "cpu", result["cpu_seconds"])


if __name__ == "__main__":
    main()
