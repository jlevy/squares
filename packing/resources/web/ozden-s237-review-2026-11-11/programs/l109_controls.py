"""Lane L109's controls: runs the 17 controls of the frozen plan and compares each outcome.

Usage: python -I -B l109_controls.py CERT.yaml TWIN.json PLAN.json FACTS.json OUT.json

Written after the plan was stated and hashed. Each control changes the certificate (or
its text, for the reader controls) and decides the change with the frozen checker's
functions; the scope of each is the plan's. Imports nothing from the repository.
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction as Q
from typing import Any

sys.set_int_max_str_digits(0)  # long exact values in this program's own bookkeeping
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l109_axes as A  # noqa: E402
import l109_check as C  # noqa: E402
import l109_clip as B  # noqa: E402
import l109_geom as G  # noqa: E402
import l109_reader as R  # noqa: E402

E = Q(1, 10**30)
PROGRAMS = ["l109_reader.py", "l109_axes.py", "l109_clip.py", "l109_check.py", "l109_geom.py", "l109_controls.py"]

Ints = tuple[int, int]


def ints(q: Q) -> Ints:
    return (q.numerator, q.denominator)


def to_ints(pts: list[tuple[Q, Q]]) -> list[tuple[Ints, Ints]]:
    return [(ints(x), ints(y)) for x, y in pts]


def ij(rows: list[list[Any]]) -> list[list[Any]]:
    return sorted([r[0], r[1]] for r in rows)


def pair_exact(pa: list[tuple[Q, Q]], pb: list[tuple[Q, Q]]) -> tuple[Q, str, str, Any]:
    a1, a2 = A.make(pa), A.make(pb)
    b1 = B.make([(B.as_mpq(ints(x)), B.as_mpq(ints(y))) for x, y in pa])
    b2 = B.make([(B.as_mpq(ints(x)), B.as_mpq(ints(y))) for x, y in pb])
    return C.decide_pair(a1, a2, b1, b2)


def summary(res: dict[str, Any]) -> dict[str, Any]:
    keep = [
        "verdict",
        "squares_decided",
        "pairs_decided",
        "unit_failures",
        "ccw_squares",
        "cw_squares",
        "wall_disagreements",
        "outside",
        "inside_b_failures",
        "wall_contacts",
        "pair_disagreements",
        "touching_pairs",
        "margin_list_sha256",
    ]
    out = {k: res[k] for k in keep if k in res}
    out["overlapping_pairs_count"] = len(res["overlapping_pairs"])
    out["overlapping_pairs_first"] = [r[:3] for r in res["overlapping_pairs"][:12]]
    out["sum_of_clipped_pair_areas_head"] = res["sum_of_clipped_pair_areas"][:40]
    return out


def main() -> int:
    cert, twin, plan_path, facts_path, out = sys.argv[1:6]
    t_start = time.process_time()
    with open(cert, encoding="utf-8") as f:
        ytext = f.read()
    with open(twin, encoding="utf-8") as f:
        jtext = f.read()
    with open(plan_path, encoding="utf-8") as f:
        plan = json.load(f)
    with open(facts_path, encoding="utf-8") as f:
        facts = json.load(f)
    rd = R.read_texts(ytext, jtext)
    n = rd.n
    side = Q(*rd.side)
    pts = [[(Q(*x), Q(*y)) for x, y in sq] for sq in rd.corners]
    base = [to_ints(p) for p in pts]
    expect = {c["id"]: c["expect"] for c in plan["controls"]}
    results: dict[str, dict[str, Any]] = {}

    def record(cid: str, came: dict[str, Any], ok: bool) -> None:
        results[cid] = {"as_stated": ok, "came_out": came}
        print(cid, "as stated" if ok else "NOT AS STATED", flush=True)

    def reader_control(cid: str, y: str, j: str) -> None:
        try:
            R.read_texts(y, j)
            record(cid, {"reader": "accepted"}, False)
        except R.ReadRefused as exc:
            msg = str(exc)
            record(cid, {"reader_refused": msg[:200]}, msg == expect[cid]["reader_refuses_with"])

    twin_tree = json.loads(jtext)

    # G1: square n given square 1's corners
    c1 = list(base)
    c1[n - 1] = base[0]
    res = C.decide(rd.side, c1)
    m, ca, cb, ar = pair_exact(pts[0], pts[0])
    e = expect["G1"]
    ok = (
        res["verdict"] == e["verdict"]
        and ij(res["overlapping_pairs"]) == e["overlapping_pairs"]
        and m == Q(e["margin"])
        and str(ar) == e["area"]
        and ca == cb == "overlap"
        and ij(res["outside"]) == e["outside"]
        and res["touching_pairs"] == e["touching_pairs"]
    )
    record("G1", {**summary(res), "pair_margin": str(m), "pair_area": str(ar)}, ok)

    # G2: square 1 translated by (S, 0)
    c2 = list(base)
    c2[0] = to_ints(G.translate(pts[0], side, Q(0)))
    res = C.decide(rd.side, c2, pairs=[(0, k) for k in range(1, n)], squares=[0])
    e = expect["G2"]
    ok = (
        res["verdict"] == e["verdict"]
        and ij(res["outside"]) == e["outside"]
        and res["overlapping_pairs"] == e["overlapping_pairs"]
        and res["touching_pairs"] == e["touching_pairs"]
    )
    record("G2", summary(res), ok)

    # G3: square n's entry deleted
    start = ytext.index(f"  - id: {n}\n")
    end = ytext.index("  claim:\n", start)
    t3 = json.loads(jtext)
    del t3["witness"]["squares"][-1]
    reader_control("G3", ytext[:start] + ytext[end:], json.dumps(t3))

    # G4: square n's id set to 1
    assert ytext.count(f"  - id: {n}\n") == 1
    t4 = json.loads(jtext)
    t4["witness"]["squares"][-1]["id"] = 1
    reader_control("G4", ytext.replace(f"  - id: {n}\n", "  - id: 1\n"), json.dumps(t4))

    # G5: square 1's third corner moved 1e-30 in x
    p5 = list(pts[0])
    p5[2] = (p5[2][0] + E, p5[2][1])
    c5 = list(base)
    c5[0] = to_ints(p5)
    res = C.decide(rd.side, c5, pairs=[(0, k) for k in range(1, n)], squares=[0])
    e = expect["G5"]
    fails = res["unit_failures"]
    ok = (
        res["verdict"] == e["verdict"]
        and sorted({f["square"] for f in fails}) == e["unit_failures_squares"]
        and sorted({f["method"] for f in fails}) == e["unit_failures_methods"]
    )
    record("G5", summary(res), ok)

    # G6: every square reflected in its own horizontal centre line
    c6 = []
    for p in pts:
        cy = sum((y for _, y in p), Q(0)) / 4
        c6.append(to_ints([(x, 2 * cy - y) for x, y in p]))
    res = C.decide(rd.side, c6)
    e = expect["G6"]
    ok = (
        res["verdict"] == e["verdict"]
        and len(res["overlapping_pairs"]) >= e["overlapping_pairs_at_least"]
        and res["unit_failures"] == e["unit_failures"]
        and res["cw_squares"] == e["cw_squares"]
        and res["outside"] == e["outside"]
        and sorted(res["wall_contacts"]) == sorted(e["wall_contacts"])
    )
    record("G6", summary(res), ok)

    # G7: the twin's side altered in its last digit
    t7 = json.loads(jtext)
    s7 = t7["witness"]["side"]
    t7["witness"]["side"] = s7[:-1] + ("1" if s7[-1] != "1" else "2")
    reader_control("G7", ytext, json.dumps(t7))

    # G8: every corner transposed
    c8 = [[(y, x) for x, y in sq] for sq in base]
    res = C.decide(rd.side, c8)
    e = expect["G8"]
    ok = (
        res["verdict"] == e["verdict"]
        and sorted(res["wall_contacts"]) == e["wall_contacts"]
        and res["margin_list_sha256"] == e["margin_list_sha256"]
        and res["cw_squares"] == e["cw_squares"]
        and res["sum_of_clipped_pair_areas"] == e["sum_of_clipped_pair_areas"]
    )
    record("G8", summary(res), ok)

    # G9: the side written as 2p/2q
    sp, sq_ = rd.side
    old = f"{sp}/{sq_}"
    new = f"{2 * sp}/{2 * sq_}"
    assert ytext.count(f"  side: {old}\n") == 1
    t9 = json.loads(jtext)
    t9["witness"]["side"] = new
    reader_control("G9", ytext.replace(f"  side: {old}\n", f"  side: {new}\n"), json.dumps(t9))

    # S1: the side changed; every square's walls decided again
    f12 = int(side * 10**12)
    floor12 = Q(f12, 10**12)
    ceil12 = Q(f12 + (0 if floor12 == side else 1), 10**12)
    sides = {
        "S1a": side - Q(1, side.denominator),
        "S1b": side - E,
        "S1c": floor12,
        "S1d": ceil12,
    }
    for cid, sd in sides.items():
        res = C.decide(ints(sd), base, pairs=[])
        e = expect[cid]
        ok = res["verdict"] == e["verdict"]
        if "outside" in e:
            ok = ok and ij(res["outside"]) == sorted(e["outside"])
        if "wall_contacts" in e:
            ok = ok and sorted(res["wall_contacts"]) == sorted(e["wall_contacts"])
        record(cid, {**summary(res), "side_approx": f"{float(sd):.15f}"}, ok)

    # S4: the least pair closed along its centre line
    lp = facts["least_pair"]
    mv, st = lp["mover"] - 1, lp["still"] - 1
    info = G.close_along_centres(pts[st], pts[mv], E)
    d = info["d"]
    assert isinstance(d, tuple)
    for cid, key in (("S4c", "t0"), ("S4p", "t1")):
        t = info[key]
        assert isinstance(t, Q)
        moved = G.moved(pts[mv], d, t)
        c4 = list(base)
        c4[mv] = to_ints(moved)
        prs = [(min(mv, k), max(mv, k)) for k in range(n) if k != mv]
        res = C.decide(rd.side, c4, pairs=prs, squares=[mv])
        m, ca, cb, ar = pair_exact(pts[st], moved)
        e = expect[cid]
        ok = (
            res["verdict"] == e["verdict"]
            and res["touching_pairs"] == e["touching_pairs"]
            and ij(res["overlapping_pairs"]) == e["overlapping_pairs"]
            and res["outside"] == e["outside"]
            and m == Q(e["margin"])
        )
        record(cid, {**summary(res), "pair_margin": str(m), "pair_classes": [ca, cb], "pair_area": str(ar)[:60]}, ok)

    # S5: every pair below 1e-12, pair-level
    s5 = []
    for p in facts["near_pairs"]:
        mv, st = p["mover"] - 1, p["still"] - 1
        info = G.close_along_centres(pts[st], pts[mv], E)
        d = info["d"]
        t0, t1 = info["t0"], info["t1"]
        assert isinstance(d, tuple) and isinstance(t0, Q) and isinstance(t1, Q)
        m0, a0, b0, ar0 = pair_exact(pts[st], G.moved(pts[mv], d, t0))
        m1, a1, b1, ar1 = pair_exact(pts[st], G.moved(pts[mv], d, t1))
        good = m0 == 0 and a0 == b0 == "contact" and ar0 == 0 and m1 == -E and a1 == b1 == "overlap" and ar1 > 0
        s5.append({"pair": p["pair"], "ok": good, "contact": [a0, b0], "past": [a1, b1]})
    bad5 = [r for r in s5 if not r["ok"]]
    record("S5", {"pairs": len(s5), "as_stated": len(s5) - len(bad5), "failures": bad5[:10]}, not bad5 and len(s5) == expect["S5"]["pairs"])

    # S6: every square to its nearest wall, square-level
    s6 = []
    side_m = B.as_mpq(rd.side)
    for i in range(n):
        a = A.make(pts[i])
        cl = A.walls(a, side)
        w = min(A.WALLS, key=lambda k: cl[k])
        row: dict[str, Any] = {"square": i + 1, "wall": w}
        good = True
        for tag, past, cls in (("at", Q(0), "contact"), ("past", E, "outside")):
            q = G.to_wall(pts[i], w, cl[w], past)
            aa = A.make(q)
            bb = B.make([(B.as_mpq(ints(x)), B.as_mpq(ints(y))) for x, y in q])
            ws = C.decide_walls(aa, bb, side, side_m)
            row[tag] = [ws[w][1], ws[w][2]]
            good = good and ws[w][1] == ws[w][2] == cls
        row["ok"] = good
        s6.append(row)
    bad6 = [r for r in s6 if not r["ok"]]
    record("S6", {"squares": len(s6), "as_stated": len(s6) - len(bad6), "failures": bad6[:10]}, not bad6 and len(s6) == expect["S6"]["squares"])

    every = all(r["as_stated"] for r in results.values()) and set(results) == set(expect)
    receipt = {
        "program": "l109_controls.py",
        "programs_sha256": C.program_digests(PROGRAMS),
        "plan_sha256": C.sha256_file(plan_path),
        "facts_sha256": C.sha256_file(facts_path),
        "certificate_sha256": C.sha256_file(cert),
        "python": sys.version.split()[0],
        "verdict": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
        "controls": results,
        "cpu_seconds": round(time.process_time() - t_start, 1),
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1)
        f.write("\n")
    print(receipt["verdict"], f"cpu={receipt['cpu_seconds']}s")
    return 0 if every else 1


if __name__ == "__main__":
    raise SystemExit(main())
