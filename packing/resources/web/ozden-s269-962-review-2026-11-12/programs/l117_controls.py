"""Lane L117: run the stated controls and compare each with its stated outcome.

Clean-room code for the stage 4 review of jlevy/squares#962. Written after
controls-plan.json was hashed. Every geometric control is decided with the frozen
l117_check.decide (both methods); the reader controls with the frozen reader. The
comparison is literal: a key that does not match is reported, never adjusted.

Usage: python -I -B l117_controls.py CERT.yaml TWIN.json PLAN.json FACTS.json CHECK.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l117_check as ck  # noqa: E402
import l117_geom as g  # noqa: E402
import l117_reader as rd  # noqa: E402
import l117_sat as sa  # noqa: E402

E30 = F(1, 10**30)
WALLS = ("left", "bottom", "right", "top")


def rat_side(S: F) -> tuple[int, int]:
    return S.numerator, S.denominator


def summary(res: dict) -> dict:
    p, w, s = res["pairs"], res["walls"], res["squares"]
    return {
        "verdict": res["verdict"],
        "unit_A": s["unit_by_A"],
        "unit_B": s["unit_by_B"],
        "counterclockwise": s["counterclockwise"],
        "clockwise": s["clockwise"],
        "not_unit_A": s["not_unit_A"],
        "not_unit_B": s["not_unit_B"],
        "outside_A": sorted(w["outside_A"]),
        "outside_B": sorted(w["outside_B"]),
        "centre_outside_B": w["centre_outside_B"],
        "wall_class_disagreements": w["class_disagreements"],
        "contacts": sorted(w["contacts"]),
        "overlap_A": sorted(p["overlap_A"]),
        "overlap_B": sorted(p["overlap_B"]),
        "contact_A": sorted(p["contact_A"]),
        "contact_B": sorted(p["contact_B"]),
        "pair_class_disagreements": len(p["class_disagreements"]),
        "least_margin": p["least_margin"][0:3] if p["least_margin"] else None,
        "least_margin_sci": p["least_margin"][3] if p["least_margin"] else None,
        "overlap_area_sum_B": p["overlap_area_sum_B"],
        "margin_list_sha256": p["margin_list_sha256"],
        "pairs_decided": p["decided"],
        "squares_wall_decided": w["squares_decided"],
    }


def compare(sm: dict, expect: dict) -> list[str]:
    """Literal comparison of a decision summary with the stated outcome."""
    bad: list[str] = []
    for k, v in expect.items():
        if k == "verdict":
            ok = sm["verdict"] == v
        elif k == "overlap_pairs":
            if isinstance(v, str):
                ok = bool(sm["overlap_A"]) and sm["overlap_A"] == sm["overlap_B"]
            else:
                ok = sm["overlap_A"] == sm["overlap_B"] == sorted(v)
        elif k == "contact_pairs":
            ok = sm["contact_A"] == sm["contact_B"] == sorted(v)
        elif k == "outside":
            ok = sm["outside_A"] == sm["outside_B"] == sorted(v)
        elif k == "unit_both":
            ok = sm["unit_A"] == sm["unit_B"] == v
        elif k == "class_disagreements":
            ok = sm["pair_class_disagreements"] == v and sm["wall_class_disagreements"] == v
        elif k == "contacts":
            ok = sm["contacts"] == sorted(v)
        else:
            ok = sm[k] == v
        if not ok:
            bad.append(k)
    return bad


def main(argv: list[str]) -> int:
    ypath, jpath, ppath, fpath, cpath, opath = argv[1:7]
    t0 = time.process_time()
    with open(ypath, encoding="utf-8") as fh:
        ytext = fh.read()
    with open(jpath, encoding="utf-8") as fh:
        jtext = fh.read()
    with open(ppath, encoding="utf-8") as fh:
        plan = {c["id"]: c for c in json.load(fh)["controls"]}
    with open(fpath, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(cpath, encoding="utf-8") as fh:
        check = json.load(fh)
    rec = rd.read_pair(ytext, jtext)
    side = rec["side"]
    sq = rec["squares"]
    assert isinstance(side, tuple) and isinstance(sq, list)
    S = F(side[0], side[1])
    n = len(sq)
    pts = [g.from_rat(c) for c in sq]
    results: dict[str, dict] = {}

    def run(cid: str, sd: F, squares: list[list[g.Pt]], pairs=None, wall_squares=None) -> None:
        t = time.process_time()
        res = ck.decide(rat_side(sd), [g.to_rat(p) for p in squares], pairs=pairs, wall_squares=wall_squares)
        sm = summary(res)
        bad = compare(sm, plan[cid]["expect"])
        results[cid] = {"as_stated": not bad, "mismatched_keys": bad, "came_out": sm,
                        "cpu_seconds": round(time.process_time() - t, 1)}
        print(cid, "AS STATED" if not bad else f"NOT AS STATED {bad}", sm["verdict"], flush=True)

    def reader(cid: str, y: str, j: str) -> None:
        why = plan[cid]["expect"]["refused_for"]
        try:
            rd.read_pair(y, j)
            got = "accepted"
        except rd.ReadRefused as exc:
            got = str(exc)
        ok = got == why or (got != "accepted" and why in got)
        results[cid] = {"as_stated": ok, "came_out": got}
        print(cid, "AS STATED" if ok else "NOT AS STATED", got, flush=True)

    # reader controls
    twin = rd._strict_json(jtext)
    assert isinstance(twin, dict)
    start = ytext.index(f"  - id: {n}\n")
    end = ytext.index("  claim:\n")
    t3 = json.loads(json.dumps(twin))
    t3["witness"]["squares"].pop()
    reader("G3", ytext[:start] + ytext[end:], json.dumps(t3))
    assert ytext.count(f"  - id: {n}\n") == 1
    t4 = json.loads(json.dumps(twin))
    t4["witness"]["squares"][-1]["id"] = 1
    reader("G4", ytext.replace(f"  - id: {n}\n", "  - id: 1\n"), json.dumps(t4))
    side_str = f"{side[0]}/{side[1]}"
    side_key = f'"side": "{side_str}"'  # the side's string is also a corner coordinate at the top wall
    assert jtext.count(side_key) == 1
    last = side_str[-1]
    alt = side_str[:-1] + ("1" if last != "1" else "2")
    reader("G7", ytext, jtext.replace(side_key, f'"side": "{alt}"'))
    dbl = f"{2 * side[0]}/{2 * side[1]}"
    assert ytext.count(f"  side: {side_str}\n") == 1
    t9 = json.loads(json.dumps(twin))
    t9["witness"]["side"] = dbl
    reader("G9", ytext.replace(f"  side: {side_str}\n", f"  side: {dbl}\n"), json.dumps(t9))

    # whole-file geometric controls
    g1 = pts[:-1] + [list(pts[0])]
    run("G1", S, g1)
    g2 = [g.shift(pts[0], S, F(0))] + pts[1:]
    run("G2", S, g2)
    g5 = [list(p) for p in pts]
    c2 = g5[0][2]
    g5[0][2] = (c2[0] + E30, c2[1])
    run("G5", S, g5)
    g6 = []
    for p in pts:
        cy = (p[0][1] + p[2][1]) / 2
        g6.append([(x, 2 * cy - y) for x, y in p])
    run("G6", S, g6)
    run("G8", S, [[(y, x) for x, y in p] for p in pts])
    run("G10", S, [p[1:] + p[:1] for p in pts])
    run("G11", S, [list(reversed(p)) for p in pts])
    run("G12", S, [[(S - y, x) for x, y in p] for p in pts])

    # side controls: every square's walls
    run("S1a", S - F(1, side[1]), pts, pairs=[])
    run("S1b", S - E30, pts, pairs=[])
    run("S1c", F(facts["floor_12"]), pts, pairs=[])
    run("S1d", F(facts["claim"]), pts, pairs=[])

    # S4: the closest pair
    i0, j0 = facts["S4_closest_pair"][0] - 1, facts["S4_closest_pair"][1] - 1
    t_star, t_past, _, _ = g.closing(pts[i0], pts[j0], E30)
    pj = [(min(k, j0), max(k, j0)) for k in range(n) if k != j0]
    for cid, t in (("S4c", t_star), ("S4p", t_past)):
        mod = list(pts)
        mod[j0] = g.moved(pts[j0], pts[i0], t)
        run(cid, S, mod, pairs=pj)

    # S5: every pair below 1e-12 by method A, closed (pair-level)
    A = [sa.SquareA(c) for c in sq]
    near = [(i, j) for i in range(n) for j in range(i + 1, n) if sa.pair_margin(A[i], A[j]) < F(1, 10**12)]
    h = hashlib.sha256()
    s5 = {"pairs": len(near), "contact_as_stated": 0, "past_as_stated": 0, "failures": []}
    for i, j in near:
        t_star, t_past, _, _ = g.closing(pts[i], pts[j], E30)
        h.update(f"{i + 1} {j + 1} {ck.frac_str(t_star)} {ck.frac_str(t_past)}\n".encode())
        for label, t, want_m, want_c in (("contact", t_star, F(0), "contact"), ("past", t_past, -E30, "overlap")):
            M = ck.Model(side, [sq[i], g.to_rat(g.moved(pts[j], pts[i], t))])
            ca, cb, m, _ = M.pair(0, 1)
            if m == want_m and ca == cb == want_c:
                s5[f"{label}_as_stated"] += 1
            else:
                s5["failures"].append([i + 1, j + 1, label, ca, cb])
    s5["times_sha256_equals_plan_facts"] = h.hexdigest() == facts["S5_times_sha256"]
    ok5 = (s5["pairs"] == plan["S5"]["expect"]["pairs"] and s5["contact_as_stated"] == s5["pairs"]
           and s5["past_as_stated"] == s5["pairs"])
    results["S5"] = {"as_stated": ok5, "came_out": s5}
    print("S5", "AS STATED" if ok5 else "NOT AS STATED", s5["pairs"], s5["contact_as_stated"], s5["past_as_stated"], flush=True)

    # S6: every square to its nearest wall (square-level)
    s6 = {"squares": 0, "contact_as_stated": 0, "past_as_stated": 0, "failures": []}
    for k in range(n):
        cl = sa.wall_clearances(A[k], S)
        c = min(cl.values())
        w = next(x for x in WALLS if cl[x] == c)
        s6["squares"] += 1
        for label, mv, want_c, want_k in (("contact", c, F(0), "contact"), ("past", c + E30, -E30, "outside")):
            dx, dy = {"left": (-mv, F(0)), "right": (mv, F(0)), "bottom": (F(0), -mv), "top": (F(0), mv)}[w]
            M = ck.Model(side, [g.to_rat(g.shift(pts[k], dx, dy))])
            clm, ca, cb, cin = M.walls(0)
            others_ok = all(ca[x] != "outside" and cb[x] != "outside" for x in WALLS if x != w)
            if clm[w] == want_c and ca[w] == cb[w] == want_k and others_ok and cin:
                s6[f"{label}_as_stated"] += 1
            else:
                s6["failures"].append([k + 1, w, label, ca[w], cb[w], cin])
    ok6 = s6["contact_as_stated"] == n and s6["past_as_stated"] == n
    results["S6"] = {"as_stated": ok6, "came_out": s6}
    print("S6", "AS STATED" if ok6 else "NOT AS STATED", s6["contact_as_stated"], s6["past_as_stated"], flush=True)

    order = [c for c in plan]
    every = all(results[c]["as_stated"] for c in order)
    out = {
        "program": "l117_controls.py",
        "certificate_sha256": check["source"]["yaml_sha256"],
        "verdict": "EVERY_CONTROL_AS_STATED" if every else "NOT_EVERY_CONTROL_AS_STATED",
        "as_stated": sum(1 for c in order if results[c]["as_stated"]),
        "stated": len(order),
        "not_as_stated": [c for c in order if not results[c]["as_stated"]],
        "controls": {c: results[c] for c in order},
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    with open(opath, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(out["verdict"], out["as_stated"], "of", out["stated"], out["not_as_stated"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
