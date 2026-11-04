"""Sharp controls and mutants for a centre-basis certificate, each decided by both methods.

Usage: oz_controls.py CERT.yaml N SIDE OUT.json

Every control states its expected outcome before it runs, and the receipt records, for each
method, what it decided. "Contact" means a margin of exactly 0; "past" means 10^-30 beyond
contact. A control that changes some squares re-decides every pair that involves a changed
square and every wall of a changed square (all walls when the box changes); the other pairs
and walls are unchanged inputs and keep the original's decision, which oz_check.py records.

A  the box lowered to the squares' far extent (contact), and 10^-30 below it (past)
B  every square translated toward the nearer near wall by the least near-wall clearance, and 10^-30 more
C  the least-margin pair closed along its centre line to contact, and 10^-30 past it
D  every pair with margin below 10^-9 closed the same way, pair decisions only
E  every square alone translated toward its nearest wall by its clearance, and 10^-30 more, wall decisions only
F  one square of the least-margin pair enlarged about its centre to touch its partner, and 10^-30 more
G  the square of least wall clearance enlarged to touch that wall, and 10^-30 more
H  a duplicated square (one square replaced by a copy of another)
I  a square translated by (S, 0), out of the box
J  one basis scaled by 1 + 10^-30 (not a unit square)
K  one square dropped (count n - 1), and one id repeated
L  every basis reflected to (a, -b): the reversed rotation sense
"""

from __future__ import annotations

import json
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ozlib as oz  # noqa: E402

EPS = Fraction(1, 10**30)


def sq_from_F(sid, x, y, a, b, s=Fraction(1)):
    F = (x, y, a, b, s)
    Q = tuple(oz.F_to_Q(v) for v in F)
    return {"id": sid, "F": F, "Q": Q}


def shape_ok(sq) -> dict:
    x, y, a, b, s = sq["F"]
    m1 = (a * a + b * b == 1) and s == 1
    cor = oz.corners_Q(sq["Q"])
    m2 = oz.area2(cor) == 2
    return {"m1": m1, "m2": m2}


def walls_of(sq, S_F) -> dict:
    c1 = oz.wall_clearances_F(sq["F"], S_F)
    cor = oz.corners_Q(sq["Q"])
    S_Q = oz.F_to_Q(S_F)
    c2 = oz.wall_clearances_Q(cor, S_Q)
    inside, _, _ = oz.contained_by_area_Q(cor, S_Q)
    return {"m1": all(c >= 0 for c in c1), "m2": all(c >= 0 for c in c2) and inside,
            "least_m1": min(c1), "least_m2": oz.Q_to_F(min(c2)), "area_agrees": inside == all(c >= 0 for c in c2)}


def pair_of(P, Q) -> dict:
    m, _ = oz.sat_margin_F(P["F"], Q["F"])
    area = oz.overlap_area_Q(oz.corners_Q(P["Q"]), oz.corners_Q(Q["Q"]))
    return {"m1": m >= 0, "m2": area == 0, "margin": m, "area": oz.Q_to_F(area)}


def decide_changed(squares, S_F, changed_ids, all_walls=False) -> dict:
    """Re-decide what the change touches: shapes and walls of changed squares, their pairs."""
    byid = {}
    dup_ids = False
    for sq in squares:
        if sq["id"] in byid:
            dup_ids = True
        byid.setdefault(sq["id"], sq)
    m1 = m2 = True
    shape_fail = []
    wall_fail = []
    pair_fail = []
    walls_checked = 0
    pairs_checked = 0
    targets = [sq for sq in squares if all_walls or sq["id"] in changed_ids]
    for sq in targets:
        sh = shape_ok(sq)
        w = walls_of(sq, S_F)
        walls_checked += 1
        if not sh["m1"] or not sh["m2"]:
            shape_fail.append([sq["id"], sh["m1"], sh["m2"]])
        m1 &= sh["m1"] and w["m1"]
        m2 &= sh["m2"] and w["m2"]
        if not w["m1"] or not w["m2"]:
            wall_fail.append([sq["id"], w["m1"], w["m2"]])
    for k, sq in enumerate(squares):
        if sq["id"] not in changed_ids:
            continue
        for t, other in enumerate(squares):
            if t == k:
                continue
            if other["id"] in changed_ids and t < k:
                continue  # each changed-changed pair once
            p = pair_of(sq, other)
            pairs_checked += 1
            m1 &= p["m1"]
            m2 &= p["m2"]
            if not p["m1"] or not p["m2"]:
                pair_fail.append([sq["id"], other["id"], p["m1"], p["m2"], oz.sci(p["margin"]), oz.sci(p["area"])])
    return {"m1_accepts": bool(m1), "m2_accepts": bool(m2), "walls_checked": walls_checked,
            "pairs_checked": pairs_checked, "shape_fail": shape_fail[:10],
            "wall_fail": wall_fail[:10], "pair_fail": pair_fail[:10], "duplicate_ids": dup_ids,
            "shape_fail_count": len(shape_fail), "wall_fail_count": len(wall_fail),
            "pair_fail_count": len(pair_fail)}


def contact_lambda(P, Q) -> Fraction:
    """Scale of the centre offset c_Q - c_P at which the pair first touches (exact)."""
    xP, yP, aP, bP, sP = P["F"]
    xQ, yQ, aQ, bQ, sQ = Q["F"]
    dx = xQ - xP
    dy = yQ - yP
    lam = None
    for da, db in ((aP, bP), (-bP, aP), (aQ, bQ), (-bQ, aQ)):
        a_k = abs(dx * da + dy * db)
        h_k = oz.halfwidth_F(P["F"], da, db) + oz.halfwidth_F(Q["F"], da, db)
        if a_k == 0:
            continue
        v = h_k / a_k
        if lam is None or v < lam:
            lam = v
    return lam


def moved(Q, P, lam):
    xP, yP = P["F"][0], P["F"][1]
    xQ, yQ, a, b, s = Q["F"]
    return sq_from_F(Q["id"], xP + lam * (xQ - xP), yP + lam * (yQ - yP), a, b, s)


def enlarge_to_pair(P, Q) -> Fraction:
    """Side of P (about its centre) at which P first touches Q (exact)."""
    xP, yP, aP, bP, _ = P["F"]
    xQ, yQ, aQ, bQ, _ = Q["F"]
    dx = xQ - xP
    dy = yQ - yP
    unitP = (xP, yP, aP, bP, Fraction(1))
    s_star = None
    for da, db in ((aP, bP), (-bP, aP), (aQ, bQ), (-bQ, aQ)):
        a_k = abs(dx * da + dy * db)
        w_q = oz.halfwidth_F(Q["F"], da, db)
        w_p = oz.halfwidth_F(unitP, da, db)
        v = (a_k - w_q) / w_p
        if s_star is None or v > s_star:
            s_star = v
    return s_star


def run_control(name, expect, squares, S_F, changed, all_walls=False, note="") -> dict:
    d = decide_changed(squares, S_F, set(changed), all_walls=all_walls)
    want = expect == "accept"
    d.update({
        "control": name, "expected": expect, "note": note,
        "m1_as_expected": d["m1_accepts"] == want, "m2_as_expected": d["m2_accepts"] == want,
    })
    return d


def main() -> int:
    cert, n_s, side_s, out_p = sys.argv[1:5]
    n = int(n_s)
    t0 = time.process_time()
    doc = oz.read_witness_yaml(cert)
    fmt = oz.check_format(doc, n, side_s)
    base = oz.witness_squares(doc)
    S = oz.to_F(doc["header"]["side"])
    for sq in base:
        sq.pop("text", None)
    byid = {sq["id"]: sq for sq in base}
    results = []

    # Base quantities by method 1 (oz_check.py decides the original in full).
    clear = {sq["id"]: oz.wall_clearances_F(sq["F"], S) for sq in base}
    far = min(min(c[1], c[3]) for c in clear.values())
    near_x = min(c[0] for c in clear.values())
    near_y = min(c[2] for c in clear.values())
    margins = []
    for p in range(len(base)):
        for q in range(p + 1, len(base)):
            m, _ = oz.sat_margin_F(base[p]["F"], base[q]["F"])
            margins.append((m, base[p]["id"], base[q]["id"]))
    margins.sort()
    gmin, gi, gj = margins[0]

    # A. The box at the far extent and 10^-30 below.
    E = S - far
    results.append(run_control("A0 box at far extent (contact)", "accept", base, E, [], all_walls=True,
                               note=f"side lowered by the least far-wall clearance {oz.sci(far)}"))
    results.append(run_control("A1 box 1e-30 below far extent (past)", "refuse", base, E - EPS, [], all_walls=True))

    # B. Translate everything toward the nearer near wall by the least near clearance.
    if near_x <= near_y:
        dvec, nd, wall = (Fraction(1), Fraction(0)), near_x, "left"
    else:
        dvec, nd, wall = (Fraction(0), Fraction(1)), near_y, "bottom"
    for tag, amt, exp in (("B0", nd, "accept"), ("B1", nd + EPS, "refuse")):
        sh = [sq_from_F(sq["id"], sq["F"][0] - amt * dvec[0], sq["F"][1] - amt * dvec[1], *sq["F"][2:]) for sq in base]
        results.append(run_control(f"{tag} all squares toward the {wall} wall by {'its least clearance' if tag == 'B0' else 'that plus 1e-30'}",
                                   exp, sh, S, [], all_walls=True, note=f"least near-wall clearance {oz.sci(nd)}"))

    # C. Close the least-margin pair along its centre line; move whichever square keeps its walls.
    P, Qsq = byid[gi], byid[gj]
    choice = None
    for mover, anchor in ((Qsq, P), (P, Qsq)):
        lam = contact_lambda(anchor, mover)
        cand = moved(mover, anchor, lam)
        if walls_of(cand, S)["m1"]:
            choice = (mover, anchor, lam)
            break
    mover, anchor, lam = choice
    for tag, lv, exp in (("C0", lam, "accept"), ("C1", lam - EPS, "refuse")):
        mv = moved(mover, anchor, lv)
        sqs = [mv if sq["id"] == mover["id"] else sq for sq in base]
        pr = pair_of(anchor, mv)
        r = run_control(f"{tag} least-margin pair {gi},{gj} closed along its centre line ({'contact' if tag == 'C0' else 'past'})",
                        exp, sqs, S, [mover["id"]],
                        note=f"pair margin before {oz.sci(gmin)}; square {mover['id']} moved; lambda {oz.sci(lv, 20)}")
        r["pair_margin_after"] = oz.frac_str(pr["margin"])
        r["pair_area_after"] = oz.sci(pr["area"])
        r["pair_expected"] = "touch" if tag == "C0" else "overlap"
        r["pair_as_expected"] = (pr["m1"] and pr["m2"] and pr["margin"] == 0) if tag == "C0" else (not pr["m1"] and not pr["m2"])
        results.append(r)

    # D. Every pair below 1e-9 closed to contact and past, pair decisions only.
    d_rows = {"pairs": 0, "contact_m1_disjoint": 0, "contact_m2_area0": 0, "contact_margin_exactly_0": 0,
              "past_m1_overlap": 0, "past_m2_area_positive": 0, "least_past_area": None}
    for m, i, j in margins:
        if m >= Fraction(1, 10**9):
            break
        A_, B_ = byid[i], byid[j]
        lam_ij = contact_lambda(A_, B_)
        c0 = pair_of(A_, moved(B_, A_, lam_ij))
        c1 = pair_of(A_, moved(B_, A_, lam_ij - EPS))
        d_rows["pairs"] += 1
        d_rows["contact_m1_disjoint"] += c0["m1"]
        d_rows["contact_m2_area0"] += c0["m2"]
        d_rows["contact_margin_exactly_0"] += c0["margin"] == 0
        d_rows["past_m1_overlap"] += not c1["m1"]
        d_rows["past_m2_area_positive"] += not c1["m2"]
        if d_rows["least_past_area"] is None or c1["area"] < d_rows["least_past_area"]:
            d_rows["least_past_area"] = c1["area"]
    d_rows["least_past_area"] = oz.sci(d_rows["least_past_area"]) if d_rows["least_past_area"] is not None else None
    d_rows["all_as_expected"] = (d_rows["contact_m1_disjoint"] == d_rows["contact_m2_area0"] == d_rows["contact_margin_exactly_0"]
                                 == d_rows["past_m1_overlap"] == d_rows["past_m2_area_positive"] == d_rows["pairs"])

    # E. Every square alone toward its nearest wall by its clearance, and 1e-30 more.
    e_rows = {"squares": 0, "contact_both_inside": 0, "past_both_outside": 0, "contact_least_exactly_0": 0}
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for sq in base:
        c = clear[sq["id"]]
        w = min(range(4), key=lambda k: c[k])
        dx, dy = dirs[w]
        ok0 = ok1 = True
        for amt, store in ((c[w], 0), (c[w] + EPS, 1)):
            x, y, a, b, s = sq["F"]
            t = sq_from_F(sq["id"], x + amt * dx, y + amt * dy, a, b, s)
            ww = walls_of(t, S)
            if store == 0:
                ok0 = ww["m1"] and ww["m2"]
                e_rows["contact_least_exactly_0"] += ww["least_m1"] == 0 and ww["least_m2"] == 0
            else:
                ok1 = (not ww["m1"]) and (not ww["m2"])
        e_rows["squares"] += 1
        e_rows["contact_both_inside"] += ok0
        e_rows["past_both_outside"] += ok1
    e_rows["all_as_expected"] = e_rows["contact_both_inside"] == e_rows["past_both_outside"] == e_rows["squares"] == e_rows["contact_least_exactly_0"]

    # F. Enlarge one square of the least-margin pair to touch the other (shape refuses; geometry touches, then overlaps).
    big, other = None, None
    for cand_big, cand_other in ((P, Qsq), (Qsq, P)):
        if min(clear[cand_big["id"]]) > 0:
            big, other = cand_big, cand_other
            break
    if big is None:
        big, other = P, Qsq
    s_star = enlarge_to_pair(big, other)
    for tag, sv in (("F0", s_star), ("F1", s_star + EPS)):
        x, y, a, b, _ = big["F"]
        eb = sq_from_F(big["id"], x, y, a, b, sv)
        sqs = [eb if sq["id"] == big["id"] else sq for sq in base]
        pr = pair_of(eb, other)
        r = run_control(f"{tag} square {big['id']} enlarged to {'touch' if tag == 'F0' else '1e-30 past'} square {other['id']}",
                        "refuse", sqs, S, [big["id"]], note=f"side 1 + {oz.sci(sv - 1)}")
        r["pair_m1_disjoint"] = pr["m1"]
        r["pair_m2_area0"] = pr["m2"]
        r["pair_margin"] = oz.frac_str(pr["margin"])
        r["pair_expected"] = "touch" if tag == "F0" else "overlap"
        r["pair_as_expected"] = (pr["m1"] and pr["m2"] and pr["margin"] == 0) if tag == "F0" else (not pr["m1"] and not pr["m2"])
        results.append(r)

    # G. Enlarge the square of least wall clearance to touch that wall, then 1e-30 more.
    gid = min(clear, key=lambda k: min(clear[k]))
    gsq = byid[gid]
    wk = min(range(4), key=lambda k: clear[gid][k])
    x, y, a, b, _ = gsq["F"]
    w_unit = oz.halfwidth_F((x, y, a, b, Fraction(1)), Fraction(1) if wk < 2 else Fraction(0), Fraction(0) if wk < 2 else Fraction(1))
    s_w = 1 + clear[gid][wk] / w_unit
    for tag, sv in (("G0", s_w), ("G1", s_w + EPS)):
        eg = sq_from_F(gid, x, y, a, b, sv)
        sqs = [eg if sq["id"] == gid else sq for sq in base]
        ww = walls_of(eg, S)
        exp = "accept" if sv == 1 else "refuse"
        r = run_control(f"{tag} square {gid} enlarged to {'touch' if tag == 'G0' else '1e-30 past'} its {['left', 'right', 'bottom', 'top'][wk]} wall",
                        exp, sqs, S, [gid], note=f"side 1 + {oz.sci(sv - 1)} (the original when its clearance is 0)")
        r["wall_m1_inside"] = ww["m1"]
        r["wall_m2_inside"] = ww["m2"]
        r["wall_expected"] = "inside" if tag == "G0" else "outside"
        r["wall_as_expected"] = (ww["m1"] and ww["m2"]) if tag == "G0" else (not ww["m1"] and not ww["m2"])
        results.append(r)

    # H. A duplicated square.
    dup = sq_from_F(gj, *byid[gi]["F"])
    sqs = [dup if sq["id"] == gj else sq for sq in base]
    results.append(run_control(f"H square {gj} replaced by a copy of square {gi}", "refuse", sqs, S, [gj]))

    # I. A square out of the box.
    first = base[0]
    x, y, a, b, s = first["F"]
    out = sq_from_F(first["id"], x + S, y, a, b, s)
    results.append(run_control(f"I square {first['id']} translated by (S, 0)", "refuse",
                               [out if sq["id"] == first["id"] else sq for sq in base], S, [first["id"]]))

    # J. One basis scaled by 1 + 1e-30.
    tgt = next(sq for sq in base if sq["F"][2] * sq["F"][3] != 0)
    x, y, a, b, s = tgt["F"]
    nb = sq_from_F(tgt["id"], x, y, a * (1 + EPS), b * (1 + EPS), s)
    results.append(run_control(f"J square {tgt['id']} basis scaled by 1 + 1e-30", "refuse",
                               [nb if sq["id"] == tgt["id"] else sq for sq in base], S, [tgt["id"]]))

    # K. Count and ids.
    k_drop = {"control": "K0 one square dropped (n - 1 squares)", "expected": "refuse",
              "count_is_n": len(base) - 1 == n}
    k_drop["m1_as_expected"] = k_drop["m2_as_expected"] = not k_drop["count_is_n"]
    ids = [sq["id"] for sq in base]
    ids2 = ids[:-1] + [ids[0]]
    k_dup = {"control": "K1 one id repeated", "expected": "refuse", "ids_unique": len(set(ids2)) == len(ids2)}
    k_dup["m1_as_expected"] = k_dup["m2_as_expected"] = not k_dup["ids_unique"]
    results.extend([k_drop, k_dup])

    # L. Reversed rotation sense: every basis (a, -b), all pairs by both methods.
    rev = [sq_from_F(sq["id"], sq["F"][0], sq["F"][1], sq["F"][2], -sq["F"][3]) for sq in base]
    pr = oz.decide_pairs(rev)
    wr = oz.decide_walls(rev, S)
    l_row = {
        "control": "L every basis reflected to (a, -b)", "expected": "refuse",
        "m1_overlapping_pairs": len(pr["method1_overlapping"]),
        "m2_overlapping_pairs": len(pr["method2_overlapping"]),
        "method_disagreements": len(pr["method_disagreements"]),
        "m1_outside_squares": len(wr["method1_outside"]),
        "m2_outside_squares": len(wr["method2_outside"]),
    }
    l_row["m1_as_expected"] = l_row["m1_overlapping_pairs"] > 0 or l_row["m1_outside_squares"] > 0
    l_row["m2_as_expected"] = l_row["m2_overlapping_pairs"] > 0 or l_row["m2_outside_squares"] > 0
    results.append(l_row)

    def clean(r):
        return {k: (oz.frac_str(v) if isinstance(v, Fraction) else v) for k, v in r.items()}

    every = all(r["m1_as_expected"] and r["m2_as_expected"] for r in results)
    extra = all(r.get("pair_as_expected", True) and r.get("wall_as_expected", True) for r in results)
    receipt = {
        "program": "oz_controls.py",
        "program_sha256": oz.sha256_file(__file__),
        "ozlib_sha256": oz.sha256_file(HERE / "ozlib.py"),
        "python": platform.python_version(),
        "argv": sys.argv[1:],
        "cert_sha256": doc["sha256"],
        "format_all_hold": fmt["all_hold"],
        "least_far_wall_clearance": oz.frac_str(far),
        "least_near_wall_clearance": oz.frac_str(min(near_x, near_y)),
        "least_margin_pair": [gi, gj, oz.frac_str(gmin)],
        "controls": [clean(r) for r in results],
        "D_every_near_pair_closed": d_rows,
        "E_every_square_to_its_wall": e_rows,
        "verdict": "EVERY_CONTROL_AS_EXPECTED" if (every and extra and d_rows["all_as_expected"] and e_rows["all_as_expected"]) else "UNEXPECTED",
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    Path(out_p).write_text(json.dumps(receipt, indent=1) + "\n")
    print(f"{Path(cert).name}: {receipt['verdict']}; {len(results)} controls, D {d_rows['pairs']} pairs, "
          f"E {e_rows['squares']} squares; cpu {receipt['cpu_seconds']} s")
    for r in results:
        print(f"  {r['control']}: expected {r['expected']}; m1 ok {r['m1_as_expected']}, m2 ok {r['m2_as_expected']}"
              + (f"; pair ok {r['pair_as_expected']}" if 'pair_as_expected' in r else "")
              + (f"; wall ok {r['wall_as_expected']}" if 'wall_as_expected' in r else ""))
    print("  D:", d_rows)
    print("  E:", e_rows)
    return 0 if receipt["verdict"] == "EVERY_CONTROL_AS_EXPECTED" else 1


if __name__ == "__main__":
    sys.exit(main())
