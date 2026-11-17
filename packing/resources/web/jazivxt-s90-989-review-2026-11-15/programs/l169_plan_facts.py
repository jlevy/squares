"""Lane L169 plan facts: the exact facts the controls plan states its outcomes from.

Usage: l169_plan_facts.py CERT CHECK_JSON OUT_JSON

Everything here is computed by the closed form of l169_geom.py (corner projections in
`fractions`), a third formulation apart from both methods. It decides no modified file.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves it off

import l169_geom as geom
import l169_reader as rd

WALLS = ("left", "right", "bottom", "top")
EPS = F(1, 10**30)


def fs(f: F) -> str:
    return f"{f.numerator}/{f.denominator}"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def margin_list(n: int, m: dict[tuple[int, int], F]) -> str:
    return "".join(f"{i} {j} {fs(m[(i, j)])}\n" for i in range(1, n + 1) for j in range(i + 1, n + 1))


def clear_list(cl: list[dict[str, F]]) -> str:
    return "".join(f"{k + 1} {w} {fs(c[w])}\n" for k, c in enumerate(cl) for w in WALLS)


def all_margins(qs: list[geom.Sq]) -> dict[tuple[int, int], F]:
    n = len(qs)
    return {(i + 1, j + 1): geom.margin(qs[i], qs[j]) for i in range(n) for j in range(i + 1, n)}


def main(argv: list[str]) -> int:
    t0 = time.process_time()
    cert, check_path, out_path = argv[1], argv[2], argv[3]
    reading = rd.read_file(cert)
    check = json.load(open(check_path))
    n = reading["n"]
    S = F(*reading["side"])
    rows = [tuple(F(*v) for v in sq) for sq in reading["squares"]]
    ts = [r[2] for r in rows]
    qs = [geom.sq_of(*r) for r in rows]
    M = all_margins(qs)
    CL = [geom.clearances(q, S) for q in qs]
    ml, cl = margin_list(n, M), clear_list(CL)
    facts: dict = {
        "program": "l169_plan_facts.py",
        "n": n,
        "side": fs(S),
        "closed_form_margin_list_sha256": sha(ml),
        "closed_form_clearance_list_sha256": sha(cl),
        "equals_method_A_margin_list": sha(ml) == check["decision"]["margin_list_sha256"],
        "equals_method_A_clearance_list": sha(cl) == check["decision"]["clearance_list_sha256"],
    }
    least = min((m, p) for p, m in M.items())
    facts["least_margin"] = {"pair": list(least[1]), "margin": fs(least[0])}

    # G1: square n given square 1's centre and t.
    qg1 = list(qs)
    qg1[n - 1] = qs[0]
    mg1 = all_margins(qg1)
    facts["G1"] = {
        "overlapping": [list(p) for p, m in mg1.items() if m < 0],
        "touching": [list(p) for p, m in mg1.items() if m == 0],
        "margin_1_n": fs(mg1[(1, n)]),
    }
    # G2: square 1 translated by (S, 0).
    q2 = (qs[0][0] + S, qs[0][1], qs[0][2], qs[0][3])
    m2 = [geom.margin(q2, qs[k]) for k in range(1, n)]
    c2 = geom.clearances(q2, S)
    facts["G2"] = {
        "least_margin_square_1_moved": fs(min(m2)),
        "clearances_square_1_moved": {w: fs(c) for w, c in c2.items()},
    }
    # G5: the turned square with the least positive clearance at any wall, moved to that
    # wall by its clearance, then turned by +-1e-30 in t.
    cand = sorted((CL[k][w], k, w) for k in range(n) for w in WALLS if ts[k] != 0)
    c5, k5, w5 = cand[0]
    moved = geom.moved_to_wall(qs[k5], w5, c5)
    g5 = {"square": k5 + 1, "wall": w5, "t": fs(ts[k5]), "clearance": fs(c5)}
    for tag, dt in (("G5a", EPS), ("G5b", -EPS)):
        tq = geom.sq_of(moved[0], moved[1], ts[k5] + dt)
        cc = geom.clearances(tq, S)
        others = min(geom.margin(tq, qs[j]) for j in range(n) if j != k5)
        g5[tag] = {"clearance_at_wall": fs(cc[w5]), "other_walls_least": fs(min(v for w, v in cc.items() if w != w5)),
                   "least_pair_margin_of_square": fs(others)}
    others0 = min(geom.margin(moved, qs[j]) for j in range(n) if j != k5)
    g5["at_contact"] = {"clearance_at_wall": fs(geom.clearances(moved, S)[w5]), "least_pair_margin_of_square": fs(others0)}
    facts["G5"] = g5
    # G6: every t negated.
    q6 = [geom.sq_of(r[0], r[1], -r[2]) for r in rows]
    m6 = all_margins(q6)
    cl6 = [geom.clearances(q, S) for q in q6]
    ov6 = sorted([list(p) for p, m in m6.items() if m < 0])
    facts["G6"] = {
        "overlapping": ov6,
        "overlapping_count": len(ov6),
        "touching": [list(p) for p, m in m6.items() if m == 0],
        "least_margin": fs(min(m6.values())),
        "least_margin_pair": list(min((m, p) for p, m in m6.items())[1]),
        "clearance_list_sha256": sha(clear_list(cl6)),
        "crossings": [[k + 1, w] for k, c in enumerate(cl6) for w in WALLS if c[w] < 0],
    }
    # G8: transposition; G11: the quarter turn about the box centre.
    tr = [{"left": c["bottom"], "right": c["top"], "bottom": c["left"], "top": c["right"]} for c in CL]
    qt = [{"left": c["top"], "right": c["bottom"], "bottom": c["left"], "top": c["right"]} for c in CL]
    facts["G8_clearance_list_sha256"] = sha(clear_list(tr))
    facts["G11_clearance_list_sha256"] = sha(clear_list(qt))
    # S1: the side lowered.
    q = reading["side"][1]
    rt = sorted((min(c["right"], c["top"]), k) for k, c in enumerate(CL))
    m_rt = rt[0][0]
    facts["S1"] = {
        "one_unit_of_last_place": fs(F(1, q)),
        "S1a_crossings": [[k + 1, w] for k, c in enumerate(CL) for w in ("right", "top") if c[w] < F(1, q)],
        "least_right_or_top_clearance": fs(m_rt),
        "S1c_contacts": [[k + 1, w] for k, c in enumerate(CL) for w in ("right", "top") if c[w] == m_rt],
        "positive_right_or_top_below_1e-30": sum(1 for c in CL for w in ("right", "top") if 0 < c[w] < EPS),
    }
    mL = min(c["left"] for c in CL)
    mB = min(c["bottom"] for c in CL)
    mR = min(c["right"] for c in CL)
    mT = min(c["top"] for c in CL)
    D = min(mR + mL, mT + mB)
    facts["S1"]["S1e"] = {
        "shift": [fs(-mL), fs(-mB)],
        "side_drop": fs(D),
        "side": fs(S - D),
        "contacts": [[k + 1, w] for k, c in enumerate(CL) for w, v in (("left", c["left"] - mL), ("right", c["right"] + mL - D), ("bottom", c["bottom"] - mB), ("top", c["top"] + mB - D)) if v == 0],
        "least_left_bottom_right_top": [fs(mL), fs(mB), fs(mR), fs(mT)],
    }
    facts["S1"]["S1f_crossings"] = [[k + 1, w] for k, c in enumerate(CL) for w, v in (("right", c["right"] + mL - D), ("top", c["top"] + mB - D)) if v == 0]
    # S4: the tightest pair whose closing move, 1e-30 past contact, is shorter than every
    # other margin and every clearance of the moved square (compared through squares).
    chosen = None
    tried = []
    for m, (i, j) in sorted((m, p) for p, m in M.items()):
        for mover, fixed in ((j, i), (i, j)):
            qi, qj = qs[fixed - 1], qs[mover - 1]
            tau0 = geom.close_time(qi, qj, F(0))
            tau1 = geom.close_time(qi, qj, -EPS)
            d2 = geom.move_dist2(qi, qj, tau1)
            other = min(M[tuple(sorted((mover, k)))] for k in range(1, n + 1) if k not in (i, j))
            cmin = min(CL[mover - 1].values())
            ok = d2 < other * other and d2 < cmin * cmin
            tried.append({"pair": [i, j], "mover": mover, "ok": ok})
            if ok:
                chosen = {"pair": [i, j], "mover": mover, "toward": fixed, "tau_contact": fs(tau0),
                          "tau_past": fs(tau1), "move_dist2_past": fs(d2),
                          "next_margin_of_mover": fs(other), "least_clearance_of_mover": fs(cmin),
                          "margin_now": fs(m)}
                break
        if chosen:
            break
    facts["S4"] = {"chosen": chosen, "tried": tried}
    # S5: every pair closed along its centre line, pair-level.
    t5 = []
    for (i, j) in M:
        qi, qj = qs[i - 1], qs[j - 1]
        t5.append(f"{i} {j} {fs(geom.close_time(qi, qj, F(0)))} {fs(geom.close_time(qi, qj, -EPS))}\n")
    facts["S5"] = {"pairs": len(t5), "closing_times_sha256": sha("".join(t5))}
    # S6: every square to its nearest wall, square-level.
    near = []
    for k, c in enumerate(CL):
        w = min(WALLS, key=lambda x: (c[x], WALLS.index(x)))
        near.append((k + 1, w, c[w]))
    facts["S6"] = {
        "nearest_wall_counts": {w: sum(1 for _, x, _ in near if x == w) for w in WALLS},
        "list_sha256": sha("".join(f"{k} {w} {fs(c)}\n" for k, w, c in near)),
    }
    facts["cpu_seconds"] = round(time.process_time() - t0, 2)
    with open(out_path, "w") as fh:
        json.dump(facts, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: facts[k] for k in ("equals_method_A_margin_list", "equals_method_A_clearance_list", "least_margin")}))
    print("G1", facts["G1"]["overlapping"], "G5", {k: v for k, v in g5.items() if k in ("square", "wall", "t", "clearance")})
    print("G5a", g5["G5a"]["clearance_at_wall"], "G5b", g5["G5b"]["clearance_at_wall"])
    print("G6", facts["G6"]["overlapping_count"], facts["G6"]["least_margin_pair"], facts["G6"]["crossings"][:4])
    print("S1", {k: v for k, v in facts["S1"].items() if k != "S1e"})
    print("S1e", facts["S1"]["S1e"], "S1f", facts["S1"]["S1f_crossings"])
    print("S4", chosen, "tried", len(tried))
    print("S6", facts["S6"]["nearest_wall_counts"], "cpu", facts["cpu_seconds"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
