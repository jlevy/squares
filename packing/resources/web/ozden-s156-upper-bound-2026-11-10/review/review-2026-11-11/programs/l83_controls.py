"""Run the controls stated in controls-plan.json (review L83).

Usage: python -I -B l83_controls.py N CERT.yaml PLAN.json OUT.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l83_check as C  # noqa: E402
import l83_clip as B  # noqa: E402
import l83_geom as G  # noqa: E402
import l83_reader as R  # noqa: E402
import l83_sat as A  # noqa: E402

E30 = F(1, 10**30)
NEAR = F(1, 10**12)


def main(argv):
    n = int(argv[1])
    cert, plan_path, out = Path(argv[2]), Path(argv[3]), Path(argv[4])
    plan = json.loads(plan_path.read_text())["counts"][str(n)]
    t0 = time.process_time()
    text = cert.read_text()
    w = R.read_text(text)
    ids, corners = w.ids, w.corners
    S = F(*w.side)
    pts = [G.from_pq(c) for c in corners]
    res = {}

    def put(name, ok, observed):
        res[name] = {"stated": plan[name] if isinstance(plan[name], str) else plan[name]["statement"], "as_stated": bool(ok), "observed": observed}

    base = C.decide(n, w.side, ids, corners)
    assert base["accept"]

    def with_square(k, new_pts):
        c2 = list(corners)
        c2[k] = G.to_pq(new_pts)
        return c2

    def pairs_of(k):
        return [(min(k, j), max(k, j)) for j in range(n) if j != k]

    # G1
    r = C.decide(n, w.side, ids, with_square(n - 1, pts[0]), pairs=pairs_of(n - 1), squares=[n - 1])
    ok = r["overlaps"] == [(1, n)] and not r["touching"] and r["margins"][(0, n - 1)] == -1 and r["total_area"] == 1 and not r["outside"] and not r["accept"]
    put("G1", ok, {"overlaps": r["overlaps"], "touching": r["touching"], "margin": str(r["margins"][(0, n - 1)]), "area": str(r["total_area"])})
    # G2
    r = C.decide(n, w.side, ids, with_square(0, G.translate(pts[0], S, F(0))), pairs=pairs_of(0), squares=[0])
    ok = r["outside"] == [1] and not r["overlaps"] and not r["touching"] and not r["accept"]
    put("G2", ok, {"outside": r["outside"], "overlaps": r["overlaps"], "touching": r["touching"]})
    # G3, G4: reader refusals on edited text
    lines = text.split("\n")
    start = lines.index(f"  - id: {n}")
    end = next(i for i in range(start + 1, len(lines)) if not lines[i].startswith("    "))
    for name, edited in (("G3", "\n".join(lines[:start] + lines[end:])), ("G4", text.replace(f"  - id: {n}\n", "  - id: 1\n", 1))):
        try:
            R.read_text(edited)
            put(name, False, "accepted")
        except R.Refused as exc:
            want = "squares is not a list" if name == "G3" else "repeated id"
            put(name, want in str(exc), f"refused: {exc}")
    # G5
    bent = [list(p) for p in pts[0]]
    bent[2][0] += E30
    bent = [tuple(p) for p in bent]
    try:
        A.Square(bent)
        ra = "accepted"
    except ValueError as exc:
        ra = f"refused: {exc}"
    try:
        B.unit_square_sense(B.points(G.to_pq(bent)))
        rb = "accepted"
    except ValueError as exc:
        rb = f"refused: {exc}"
    r = C.decide(n, w.side, ids, with_square(0, bent), pairs=[], squares=[0])
    put("G5", ra.startswith("refused") and rb.startswith("refused") and r["bad_shape"] == [1] and not r["accept"], {"A": ra, "B": rb})
    # G6: whole file, rotation read the other way
    refl = [G.to_pq(G.reflect_h(p)) for p in pts]
    r = C.decide(n, w.side, ids, refl)
    ok = not r["accept"] and len(r["overlaps"]) >= 1 and not r["bad_shape"] and not r["outside"] and r["contacts"] == base["contacts"] and not r["pair_disagree"] and not r["wall_disagree"]
    put("G6", ok, {"overlapping_pairs": len(r["overlaps"]), "touching": len(r["touching"]), "first": r["overlaps"][:5], "contacts": r["contacts"], "all_clockwise": all(s == -1 for s in r["senses"].values())})
    # G8: whole file, transposed
    trans = [G.to_pq([(y, x) for x, y in p]) for p in pts]
    r = C.decide(n, w.side, ids, trans)
    same = r["margins"] == base["margins"]
    want = sorted(tuple(c) for c in plan["G8"]["contacts"])
    ok = r["accept"] and same and r["contacts"] == want
    put("G8", ok, {"accept": r["accept"], "every_margin_equal": same, "contacts": r["contacts"]})
    # S1a-d: sides
    q = w.side[1]
    floor12 = F(int(S * 10**12), 10**12)
    ceil12 = floor12 if floor12 == S else floor12 + F(1, 10**12)
    for name, side in (("S1a", S - F(1, q)), ("S1b", S - E30), ("S1c", floor12), ("S1d", ceil12)):
        r = C.decide(n, (side.numerator, side.denominator), ids, corners, pairs=[])
        if name == "S1d":
            want = sorted(tuple(c) for c in plan[name]["contacts"])
            ok = not r["outside"] and r["contacts"] == want
            put(name, ok, {"outside": r["outside"], "contacts": r["contacts"], "side": f"{side}"})
        else:
            ok = r["outside"] == plan[name]["outside"] and not r["bad_shape"]
            put(name, ok, {"outside": r["outside"], "count": len(r["outside"])})
    # S4c, S4p: least pair along its centre line
    a, b = plan["S4c"]["pair"]
    ia, ib = a - 1, b - 1
    for name, extra in (("S4c", F(0)), ("S4p", E30)):
        moved = G.close_pair(pts[ia], pts[ib], extra)
        r = C.decide(n, w.side, ids, with_square(ib, moved), pairs=pairs_of(ib), squares=[ib])
        pair = (min(a, b), max(a, b))
        base_contacts_b = [c for c in base["contacts"] if c[0] == b]
        if name == "S4c":
            ok = r["touching"] == [pair] and not r["overlaps"] and not r["outside"] and r["contacts"] == base_contacts_b
        else:
            ok = r["overlaps"] == [pair] and not r["touching"] and not r["outside"] and r["contacts"] == base_contacts_b
        put(name, ok, {"touching": r["touching"], "overlaps": r["overlaps"], "outside": r["outside"], "contacts": r["contacts"]})
    # S5: every pair below 1e-12 closed along its centre line
    near = sorted((i, j) for (i, j), m in base["margins"].items() if m < NEAR)
    bad = []
    for i, j in near:
        for extra, kind in ((F(0), "touching"), (E30, "overlaps")):
            moved = G.close_pair(pts[i], pts[j], extra)
            r = C.decide(n, w.side, ids, with_square(j, moved), pairs=[(i, j)], squares=[])
            other = "overlaps" if kind == "touching" else "touching"
            if r[kind] != [(i + 1, j + 1)] or r[other] or r["pair_disagree"]:
                bad.append([i + 1, j + 1, kind])
    put("S5", not bad and len(near) == plan["S5"]["pairs"], {"pairs_closed": len(near), "misses": bad})
    # S6: every square to its nearest wall
    bad = []
    direction = {"left": (-1, 0), "right": (1, 0), "bottom": (0, -1), "top": (0, 1)}
    for k in range(n):
        cl = A.wall_clearances(pts[k], S)
        wall = min(C.WALLS, key=lambda x: cl[x])
        dx, dy = direction[wall]
        for extra in (F(0), E30):
            d = cl[wall] + extra
            r = C.decide(n, w.side, ids, with_square(k, G.translate(pts[k], d * dx, d * dy)), pairs=[], squares=[k])
            if extra == 0:
                good = (k + 1, wall) in r["contacts"] and not r["outside"] and not r["wall_disagree"]
            else:
                good = r["outside"] == [k + 1] and not r["wall_disagree"]
            if not good:
                bad.append([k + 1, wall, str(extra)])
    put("S6", not bad, {"squares": n, "misses": bad})
    every = all(v["as_stated"] for v in res.values())
    doc = {
        "n": n,
        "verdict": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
        "controls": res,
        "cpu_seconds": round(time.process_time() - t0, 1),
        "programs": C.program_digests(),
    }
    out.write_text(json.dumps(doc, indent=1) + "\n")
    print(n, doc["verdict"], {k: v["as_stated"] for k, v in res.items()}, "cpu", doc["cpu_seconds"])
    return 0 if every else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
