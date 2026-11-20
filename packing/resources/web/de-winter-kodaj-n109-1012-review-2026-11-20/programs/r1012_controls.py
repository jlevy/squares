"""Lane r1012's controls: every control of controls-plan.json, by both methods or the reader.

Usage: r1012_controls.py CERTIFICATE PLAN.json CLAIM OUT.json

Each rule is evaluated exactly, from method A's facts on the unmodified file, and
compared with what methods A and B (and, where a margin or clearance is predicted,
the centre-and-half-width formulation) decide on the modified packing.
"""

import json
import os
import sys
import time
from decimal import Decimal
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)

import r1012_clip  # noqa: E402
import r1012_decide  # noqa: E402
import r1012_geom as G  # noqa: E402
import r1012_reader  # noqa: E402
import r1012_sat  # noqa: E402
import r1012_writer  # noqa: E402

EPS = F(1, 10 ** 30)


def mclass(m):
    return "apart" if m > 0 else ("touch" if m == 0 else "overlap")


def cclass(c):
    return "clear" if c > 0 else ("touch" if c == 0 else "cross")


def sci(x):
    x = F(x)
    if x == 0:
        return "0"
    return f"{Decimal(x.numerator) / Decimal(x.denominator):.6e}"


def key(i, j):
    return (i, j) if i < j else (j, i)


class Base:
    def __init__(self, packing):
        self.p = packing
        self.n = packing["n"]
        self.side = packing["side"]
        self.ids = packing["ids"]
        self.quads = packing["corners"]
        r = r1012_decide.decide(self.side, self.quads)
        self.result = r
        a = r["a"]
        self.units = list(a["unit"])
        self.M = {k: (F(*v) if v is not None else None) for k, v in a["pairs"].items()}
        self.C = [tuple(F(*v) for v in c) if c is not None else None for c in a["walls"]]
        self.S = list(a["sense"])
        self.verdict = r["verdict"]


def predicted_verdict(units, margins, clear):
    if not all(units):
        return "REFUSE"
    for c in clear:
        if c is not None and min(c) < 0:
            return "REFUSE"
    for m in margins.values():
        if isinstance(m, F) and m < 0:
            return "REFUSE"
        if m == "overlap":
            return "REFUSE"
    return "ACCEPT"


def compare(side, quads, units, margins, clear, senses=None, verdict=None, geom=True):
    """Decide (side, quads) by both methods and compare with exact predictions.

    margins: {(i, j): Fraction | 'apart' | 'not-overlap' | None}; clear: [tuple | None].
    Returns (mismatches, result).
    """
    r = r1012_decide.decide(side, quads)
    a, b = r["a"], r["b"]
    bad = []
    n = len(quads)
    for k in range(n):
        if a["unit"][k] != units[k]:
            bad.append(f"A unit {k}: {a['unit'][k]} != {units[k]}")
        if b["unit"][k] != units[k]:
            bad.append(f"B unit {k}: {b['unit'][k]} != {units[k]}")
    if senses is not None:
        for k in range(n):
            if units[k] and (a["sense"][k] != senses[k] or b["sense"][k] != senses[k]):
                bad.append(f"sense {k}")
    for k in range(n):
        pc = clear[k]
        if not units[k] or pc is None:
            continue
        ac = tuple(F(*v) for v in a["walls"][k])
        if ac != pc:
            bad.append(f"A clearances {k}: {[sci(v) for v in ac]} != {[sci(v) for v in pc]}")
        if geom and tuple(G.clearances(quads[k], side)) != pc:
            bad.append(f"geom clearances {k}")
        cls = tuple(cclass(v) for v in pc)
        if a["wall_class"][k] != cls:
            bad.append(f"A wall classes {k}: {a['wall_class'][k]} != {cls}")
        if b["wall_class"][k] != cls:
            bad.append(f"B wall classes {k}: {b['wall_class'][k]} != {cls}")
        inside = b["inside_area"][k]
        if min(pc) >= 0 and inside != 1:
            bad.append(f"B area inside {k} != 1")
        if min(pc) < 0 and not inside < 1:
            bad.append(f"B area inside {k} not below 1")
    for (i, j), pm in margins.items():
        if pm is None or not (units[i] and units[j]):
            continue
        am = a["pairs"][(i, j)]
        am = F(*am) if am is not None else None
        ca, cb = a["pair_class"][(i, j)], b["pair_class"][(i, j)]
        if isinstance(pm, F):
            if am != pm:
                bad.append(f"A margin {i},{j}: {sci(am)} != {sci(pm)}")
            if geom and G.margin(quads[i], quads[j]) != pm:
                bad.append(f"geom margin {i},{j}")
            want = mclass(pm)
            if ca != want or cb != want:
                bad.append(f"classes {i},{j}: {ca}/{cb} != {want}")
        elif pm == "apart":
            if ca != "apart" or cb != "apart":
                bad.append(f"classes {i},{j}: {ca}/{cb} != apart")
        elif pm == "not-overlap":
            if ca == "overlap" or cb == "overlap" or ca != cb:
                bad.append(f"classes {i},{j}: {ca}/{cb} not a non-overlap agreed")
    if r["b"]["order_disagree"]:
        bad.append(f"B clip orders disagree on {len(r['b']['order_disagree'])} pairs")
    if r["disagreements"]:
        bad.append(f"A/B disagreements {len(r['disagreements'])}")
    want_verdict = verdict if verdict is not None else predicted_verdict(units, margins, clear)
    if r["verdict"] != want_verdict:
        bad.append(f"verdict {r['verdict']} != {want_verdict}")
    return bad, r


def via_writer(n, side, ids, quads, **kw):
    return r1012_reader.read_bytes(r1012_writer.write(n, side, ids, quads, **kw))


def reader_refuses(data):
    try:
        r1012_reader.read_bytes(data)
    except r1012_reader.ReadError as exc:
        return True, str(exc)[:160]
    return False, "read"


def main(argv):
    cert, plan_path, claim_text, out_path = argv[1:5]
    t0 = time.process_time()
    with open(plan_path, encoding="utf-8") as handle:
        plan = json.load(handle)
    stated = {c["id"]: c["stated"] for c in plan["controls"]}
    packing = r1012_reader.read_path(cert)
    base = Base(packing)
    n, side, ids, quads = base.n, base.side, base.ids, base.quads
    M, C, S = base.M, base.C, base.S
    claim = F(Decimal(claim_text))
    results = []
    whole_file = [0]

    def record(cid, ok, details, applicable=True):
        results.append({
            "id": cid,
            "stated": stated[cid],
            "outcome": ("not applicable" if not applicable else ("as stated" if ok else "NOT AS STATED")),
            "details": details,
        })
        print(f"{cid}: {results[-1]['outcome']}", flush=True)

    def whole(side_, quads_, units, margins, clear, senses=None, verdict=None, ids_=None, n_=None):
        whole_file[0] += 1
        ids_ = ids_ if ids_ is not None else ids
        n_ = n_ if n_ is not None else len(quads_)
        back = via_writer(n_, side_, ids_, quads_)
        if back["corners"] != quads_ or back["side"] != side_:
            return ["writer round trip changed values"], None
        return compare(side_, quads_, units, margins, clear, senses, verdict)

    all_unit = all(base.units)
    text = r1012_writer.write(n, side, ids, quads).decode()
    lines = text.splitlines()

    # C0
    bad = []
    for (i, j), m in M.items():
        if m is not None and G.margin(quads[i], quads[j]) != m:
            bad.append(f"margin {i},{j}")
    for k in range(n):
        if C[k] is not None and tuple(G.clearances(quads[k], side)) != C[k]:
            bad.append(f"clearance {k}")
    record("C0", not bad and all_unit, {"pairs": len(M), "squares": n, "mismatches": bad[:20]})

    # R0
    back = r1012_reader.read_bytes(text.encode())
    ok = (back["n"] == n and back["side"] == side and back["ids"] == ids and back["corners"] == quads
          and back["noncanonical"] == [])
    record("R0", ok, {"scalars": back["scalars"]})

    # R1: delete the last square's six lines
    k_last = max(i for i, line in enumerate(lines) if line.startswith("  - id: "))
    r1 = "\n".join(lines[:k_last] + lines[k_last + 6:]) + "\n"
    ok, why = reader_refuses(r1.encode())
    record("R1", ok, {"reader": why})

    # R2
    p2 = r1012_reader.read_bytes(r1012_writer.write(
        n, side, ids, quads, side_text=f"'{2 * side.numerator}/{2 * side.denominator}'"))
    ok = p2["side"] == side and p2["corners"] == quads and p2["noncanonical"] == ["side"]
    record("R2", ok, {"noncanonical": p2["noncanonical"]})

    # R3
    id_lines = [i for i, line in enumerate(lines) if line.startswith("  - id: ")]
    r3 = list(lines)
    r3[id_lines[1]] = lines[id_lines[0]]
    ok, why = reader_refuses(("\n".join(r3) + "\n").encode())
    record("R3", ok, {"reader": why})

    # R4
    q40 = Decimal(side.numerator) / Decimal(side.denominator)
    side40 = f"{q40:.40f}"
    ok, why = reader_refuses(r1012_writer.write(n, side, ids, quads, side_text=side40))
    record("R4", ok, {"side_text": side40, "reader": why})

    # R5
    den = side.denominator
    for prime in (2, 5):
        while den % prime == 0:
            den //= prime
    if den == 1:
        places = 0
        while (side * 10 ** places).denominator != 1:
            places += 1
        digits = str(abs((side * 10 ** places).numerator)).rjust(places + 1, "0")
        exact = digits[:-places] + "." + digits[-places:] if places else digits
        p5 = r1012_reader.read_bytes(r1012_writer.write(n, side, ids, quads, side_text=f"'{exact}'"))
        ok = p5["side"] == side and p5["corners"] == quads and p5["scalar_forms"]["decimal"] == 1
        record("R5", ok, {"side_text": exact, "places": places})
    else:
        record("R5", True, {"reason": "the side's decimal expansion does not terminate"}, applicable=False)

    # R6: a fifth corner
    first_corner = lines.index("    corners:") + 1
    r6 = lines[: first_corner + 1] + [lines[first_corner]] + lines[first_corner + 1:]
    ok, why = reader_refuses(("\n".join(r6) + "\n").encode())
    record("R6", ok, {"reader": why})

    # R7: a second side key
    side_line = next(i for i, line in enumerate(lines) if line.startswith("  side: "))
    r7 = lines[: side_line + 1] + [lines[side_line]] + lines[side_line + 1:]
    ok, why = reader_refuses(("\n".join(r7) + "\n").encode())
    record("R7", ok, {"reader": why})

    # R8: anchor and alias
    r8 = list(lines)
    r8[id_lines[0] + 1] = "    corners: &c0"
    r8 = r8[: id_lines[1] + 1] + ["    corners: *c0"] + r8[id_lines[1] + 6:]
    ok, why = reader_refuses(("\n".join(r8) + "\n").encode())
    record("R8", ok, {"reader": why})

    # R9 to R14
    ok, why = reader_refuses(r1012_writer.write(n, side, ids, quads, representation="center-angle"))
    record("R9", ok, {"reader": why})
    r10 = list(lines)
    r10[first_corner] = r10[first_corner].replace("    - ['", "    - ['+", 1)
    ok, why = reader_refuses(("\n".join(r10) + "\n").encode())
    record("R10", ok, {"line": r10[first_corner][:40], "reader": why})
    ok, why = reader_refuses(r1012_writer.write(n, side, ids, quads, square_size="'2'"))
    record("R11", ok, {"reader": why})
    ok, why = reader_refuses(r1012_writer.write(n, side, ids, quads, kind="decimal"))
    record("R12", ok, {"reader": why})
    p13 = r1012_reader.read_bytes(r1012_writer.write(n, side, ids, quads, origin="container-center"))
    record("R13", p13["corners"] == quads and p13["side"] == side, {"origin": p13["origin"]})
    ok, why = reader_refuses(r1012_writer.write(n, side, ids, quads, side_text=f"'{side.numerator}/0'"))
    record("R14", ok, {"reader": why})

    if not all_unit:
        record_rest = "the certificate has a square that is not a unit square; geometric controls not run"
        for cid in [c["id"] for c in plan["controls"]][16:]:
            record(cid, False, {"reason": record_rest})
        finish(out_path, plan, results, base, claim, t0, whole_file[0])
        return 1

    units = [True] * n

    # G1
    last = n - 1
    q1 = quads[:-1] + [list(quads[0])]
    m1 = {}
    for (i, j), m in M.items():
        if j != last:
            m1[(i, j)] = m
        elif i == 0:
            m1[(i, j)] = F(-1)
        else:
            m1[(i, j)] = M[key(0, i)]
    c1 = C[:-1] + [C[0]]
    bad, r = whole(side, q1, units, m1, c1)
    if r is not None and r["b"]["pair_area"][(0, last)] != 1:
        bad.append("B area of (first, last) != 1")
    overlapping = sorted(k for k, m in m1.items() if m < 0)
    record("G1", not bad, {"mismatches": bad[:20], "overlapping_predicted": [list(k) for k in overlapping][:10],
                           "verdict": r["verdict"] if r else None})

    # G2
    q2 = list(quads)
    q2[0] = G.translate(quads[0], (side, F(0)))
    L0, B0, R0_, T0 = C[0]
    c2 = [(L0 + side, B0, R0_ - side, T0)] + C[1:]
    sep = L0 >= 0 and all(C[k][2] >= 0 for k in range(1, n))
    m2 = {}
    for (i, j), m in M.items():
        m2[(i, j)] = m if i != 0 else ("not-overlap" if sep else None)
    bad, r = whole(side, q2, units, m2, c2, verdict="REFUSE")
    if r is not None and L0 >= 0 and r["b"]["inside_area"][0] != 0:
        bad.append("B area inside of the moved square != 0")
    record("G2", not bad, {"mismatches": bad[:20], "R_minus_S": sci(R0_ - side), "separated_by_x_eq_S": sep})

    # G3
    q3 = list(quads)
    (x0, y0) = quads[0][0]
    q3[0] = [(x0 + EPS, y0)] + list(quads[0][1:])
    u3 = [False] + [True] * (n - 1)
    m3 = {(i, j): (m if i != 0 else None) for (i, j), m in M.items()}
    c3 = [None] + C[1:]
    bad, r = whole(side, q3, u3, m3, c3, verdict="REFUSE")
    record("G3", not bad, {"mismatches": bad[:20]})

    # G4 to G8
    flip = [-s for s in S]
    transforms = {
        "G4": (lambda q: q[1:] + q[:1], lambda c: c, S),
        "G5": (lambda q: list(reversed(q)), lambda c: c, flip),
        "G6": (lambda q: [(y, x) for x, y in q], lambda c: (c[1], c[0], c[3], c[2]), flip),
        "G7": (lambda q: [(side - y, x) for x, y in q], lambda c: (c[3], c[0], c[1], c[2]), S),
        "G8": (lambda q: [(side - x, y) for x, y in q], lambda c: (c[2], c[1], c[0], c[3]), flip),
    }
    for cid, (tq, tc, senses) in transforms.items():
        qt = [tq(list(q)) for q in quads]
        ct = [tc(c) for c in C]
        bad, r = whole(side, qt, units, dict(M), ct, senses=senses, verdict=base.verdict)
        record(cid, not bad, {"mismatches": bad[:20]})

    # G9
    q9 = list(quads) + [list(quads[0])]
    ids9 = list(ids) + ["r1012-copy-of-first"]
    m9 = dict(M)
    for k in range(1, n):
        m9[(k, n)] = M[key(0, k)]
    m9[(0, n)] = F(-1)
    c9 = list(C) + [C[0]]
    bad, r = whole(side, q9, [True] * (n + 1), m9, c9, verdict="REFUSE", ids_=ids9, n_=n + 1)
    if r is not None and r["b"]["pair_area"][(0, n)] != 1:
        bad.append("B area of (first, new) != 1")
    record("G9", not bad, {"mismatches": bad[:20]})

    # S1
    W = min(min(c[2], c[3]) for c in C)
    q_den = side.denominator
    deltas = {
        "S1a": EPS,
        "S1b": F(1, q_den),
        "S1c": W,
        "S1d": W + EPS,
        "S1e": side - claim,
        "S1f": side - claim + F(1, 10 ** 12),
    }
    side_verdicts = {}
    for cid, delta in deltas.items():
        side2 = side - delta
        cs = [(c[0], c[1], c[2] - delta, c[3] - delta) for c in C]
        bad, r = whole(side2, quads, units, dict(M), cs)
        crossing = sorted({ids[k] for k, c in enumerate(cs) if min(c) < 0})
        verdict = r["verdict"] if r else None
        side_verdicts[cid] = verdict
        record(cid, not bad, {"delta": sci(delta), "delta_exact": f"{delta.numerator}/{delta.denominator}",
                              "verdict": verdict, "crossing": crossing[:30],
                              "crossing_count": len(crossing), "mismatches": bad[:20]})

    # P1
    pos = sorted(((m, k) for k, m in M.items() if m > 0))
    chosen = None
    for m, (i, j) in pos:
        for fixed, moved in ((i, j), (j, i)):
            qc, vc = G.close_pair(quads[fixed], quads[moved], F(0))
            qp, vp = G.close_pair(quads[fixed], quads[moved], -EPS)
            l1 = max(abs(vc[0]) + abs(vc[1]), abs(vp[0]) + abs(vp[1]))
            others = [M[key(moved, k)] for k in range(n) if k not in (fixed, moved)]
            cl = [(C[moved][0] + v[0], C[moved][1] + v[1], C[moved][2] - v[0], C[moved][3] - v[1])
                  for v in (vc, vp)]
            if all(o > l1 for o in others) and all(min(c) >= 0 for c in cl):
                chosen = (fixed, moved, qc, vc, qp, vp, m, cl)
                break
        if chosen:
            break
    if chosen is None:
        record("P1c", True, {"reason": "no eligible pair"}, applicable=False)
        record("P1p", True, {"reason": "no eligible pair"}, applicable=False)
    else:
        fixed, moved, qc, vc, qp, vp, m, cl = chosen
        for cid, qm, target, cmv in (("P1c", qc, F(0), cl[0]), ("P1p", qp, -EPS, cl[1])):
            qq = list(quads)
            qq[moved] = qm
            mm = {}
            for (i, j), mv in M.items():
                if moved not in (i, j):
                    mm[(i, j)] = mv
                elif fixed in (i, j):
                    mm[(i, j)] = target
                else:
                    mm[(i, j)] = "apart"
            cc = list(C)
            cc[moved] = cmv
            bad, r = whole(side, qq, units, mm, cc)
            record(cid, not bad, {"pair": [ids[fixed], ids[moved]], "moved": ids[moved],
                                  "original_margin": sci(m), "target": sci(target),
                                  "verdict": r["verdict"] if r else None, "mismatches": bad[:20]})

    # W1 at each wall
    wall_names = ["left", "bottom", "right", "top"]
    for cid in ("W1c", "W1p"):
        per_wall = {}
        all_ok = True
        any_applicable = False
        for w in range(4):
            order = sorted(range(n), key=lambda k: (C[k][w], k))
            pick = None
            for k in order:
                c = C[k][w]
                if c < 0:
                    continue
                if all(M[key(k, j)] > c + EPS for j in range(n) if j != k):
                    pick = k
                    break
            if pick is None:
                per_wall[wall_names[w]] = {"outcome": "not applicable: no eligible square"}
                continue
            any_applicable = True
            target = F(0) if cid == "W1c" else -EPS
            qm, shift = G.to_wall(quads[pick], side, w, target)
            qq = list(quads)
            qq[pick] = qm
            cc = list(C)
            new = list(C[pick])
            new[w] = target
            new[(w + 2) % 4] = C[pick][(w + 2) % 4] + shift
            cc[pick] = tuple(new)
            mm = {}
            for (i, j), mv in M.items():
                mm[(i, j)] = mv if pick not in (i, j) else "apart"
            bad, r = whole(side, qq, units, mm, cc)
            crossings = []
            if r is not None:
                for k2 in range(n):
                    for w2, cls in enumerate(r["a"]["wall_class"][k2]):
                        if cls == "cross":
                            crossings.append([ids[k2], wall_names[w2]])
            if cid == "W1p" and crossings != [[ids[pick], wall_names[w]]]:
                bad.append(f"crossings {crossings}")
            per_wall[wall_names[w]] = {"square": ids[pick], "clearance_before": sci(C[pick][w]),
                                       "verdict": r["verdict"] if r else None,
                                       "outcome": "as stated" if not bad else "NOT AS STATED",
                                       "mismatches": bad[:10]}
            all_ok = all_ok and not bad
        record(cid, all_ok, per_wall, applicable=any_applicable)

    # WALL: every square alone, to its nearest wall and past
    bad = []
    moves = 0
    for k in range(n):
        w = min(range(4), key=lambda w2: (C[k][w2], w2))
        for target in (F(0), -EPS):
            qm, shift = G.to_wall(quads[k], side, w, target)
            moves += 1
            sa = r1012_sat.Square(qm)
            ca = F(*r1012_sat.wall_clearances(sa, side)[w])
            cg = G.clearances(qm, side)[w]
            pm = r1012_clip.to_mpq(qm)
            _, sgm, _ = r1012_clip.unit_square(pm)
            pts = r1012_clip.ccw(pm, sgm)
            sm = r1012_clip.mpq(side.numerator, side.denominator)
            cb = r1012_clip.wall_classes(pts, sm)[w]
            area = r1012_clip.area_inside_box(pts, sm)
            other = list(C[k])
            other[w] = target
            other[(w + 2) % 4] += shift
            want_inside = min(other) >= 0
            if ca != target or cg != target:
                bad.append(f"WALL {k} {w} clearance")
            if cb != ("touch" if target == 0 else "cross"):
                bad.append(f"WALL {k} {w} B class {cb}")
            if (area == 1) != want_inside:
                bad.append(f"WALL {k} {w} B area")
    record("WALL", not bad, {"squares": n, "moves": moves, "mismatches": bad[:20]})

    # PALL: every pair alone, closed to contact and past
    bad = []
    closings = 0
    a_sq = [r1012_sat.Square(q) for q in quads]
    b_pts = []
    for q in quads:
        pts = r1012_clip.to_mpq(q)
        ok_, sg, _ = r1012_clip.unit_square(pts)
        b_pts.append(r1012_clip.ccw(pts, sg))
    for (i, j) in M:
        for target, cls in ((F(0), "touch"), (-EPS, "overlap")):
            qm, _ = G.close_pair(quads[i], quads[j], target)
            closings += 1
            mA, _ = r1012_sat.pair_margin(a_sq[i], r1012_sat.Square(qm))
            if F(*mA) != target:
                bad.append(f"PALL {i},{j} A {sci(F(*mA))}")
            if G.margin(quads[i], qm) != target:
                bad.append(f"PALL {i},{j} geom")
            pm = r1012_clip.to_mpq(qm)
            okm, sgm, _ = r1012_clip.unit_square(pm)
            pm = r1012_clip.ccw(pm, sgm)
            c1, a1 = r1012_clip.classify_intersection(r1012_clip.clip_by_convex(pm, b_pts[i]))
            c2, a2 = r1012_clip.classify_intersection(r1012_clip.clip_by_convex(b_pts[i], pm))
            if not okm or c1 != cls or c2 != cls or a1 != a2:
                bad.append(f"PALL {i},{j} B {c1}/{c2}")
    record("PALL", not bad, {"pairs": len(M), "closings": closings, "mismatches": bad[:20]})

    finish(out_path, plan, results, base, claim, t0, whole_file[0], side_verdicts)
    return 0


def finish(out_path, plan, results, base, claim, t0, whole_files, side_verdicts=None):
    side = base.side
    s12 = 10 ** 12
    ceil12 = F(-((-side.numerator * s12) // side.denominator), s12)
    failing = [r["id"] for r in results if r["outcome"] == "NOT AS STATED"]
    priors = {
        plan["priors"][0]: base.verdict == "ACCEPT",
        plan["priors"][1]: ceil12 == claim,
        plan["priors"][2]: bool(side_verdicts) and side_verdicts.get("S1e") == "ACCEPT"
        and side_verdicts.get("S1f") == "REFUSE",
        plan["priors"][3]: all(m is None or m != 0 for m in base.M.values()),
    }
    receipt = {
        "program": "r1012_controls.py",
        "certificate_sha256": base.p["sha256"],
        "certificate_git_blob": base.p["git_blob"],
        "original_verdict": base.verdict,
        "outcome": "EVERY_CONTROL_AS_STATED" if not failing else "CONTROLS_NOT_AS_STATED",
        "failing": failing,
        "controls": results,
        "as_stated": sum(1 for r in results if r["outcome"] == "as stated"),
        "not_applicable": [r["id"] for r in results if r["outcome"] == "not applicable"],
        "total": len(results),
        "whole_file_decisions": whole_files,
        "priors": priors,
        "cpu_seconds": round(time.process_time() - t0, 1),
        "python": sys.version.split()[0],
    }
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=1)
        handle.write("\n")
    print(f"{receipt['outcome']} {receipt['as_stated']} of {receipt['total']}")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
