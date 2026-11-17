"""Run the stated controls on one certificate (lane L72, bead think-qqyg).

Usage: python -I -B l72_controls.py PLAN.json COUNT CERT.yaml CHECK.json OUT.json

Written after controls-plan.json was stated and hashed. Every control is decided by the
frozen checker's modules: file-level controls by l72_check.decide_data (both methods,
every square, wall and pair), pair-level and square-level controls by l72_sat (method A)
and l72_clip (method B) directly, and reader controls by l72_reader.read_texts. Each
outcome is held to the plan's statement; a control whose outcome differs is reported as
MISSED with what was observed, never adjusted.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction  # noqa: E402

import l72_check as chk  # noqa: E402
import l72_clip as clipm  # noqa: E402
import l72_reader as reader  # noqa: E402
import l72_sat as sat  # noqa: E402
import l72_util as util  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
EPS = Fraction(1, 10**30)
PROGRAMS = [
    "l72_util.py",
    "l72_reader.py",
    "l72_sat.py",
    "l72_clip.py",
    "l72_check.py",
    "l72_controls.py",
    "controls-plan.json",
]


def to_raw(P):
    return tuple((x.numerator, x.denominator, y.numerator, y.denominator) for x, y in P)


def with_changes(data, corners=None, side=None):
    d = dict(data)
    if corners is not None:
        d["corners"] = corners
    if side is not None:
        S = Fraction(side)
        d["side"] = (S.numerator, S.denominator)
    return d


def centre(P):
    return ((P[0][0] + P[2][0]) / 2, (P[0][1] + P[2][1]) / 2)


def closing_parameter(Pi, ai, Pj, aj, d):
    """Least s at which Pj + s d touches Pi, for Pi, Pj apart at s = 0 and d = c_i - c_j."""
    best = None
    for a in (ai[0], ai[1], aj[0], aj[1]):
        lo_i, hi_i = sat.proj_range(Pi, a)
        lo_j, hi_j = sat.proj_range(Pj, a)
        da = d[0] * a[0] + d[1] * a[1]
        for alpha, beta in ((lo_j - hi_i, da), (lo_i - hi_j, -da)):
            if alpha > 0:
                if beta >= 0:
                    raise ValueError("a gap that does not close along the centre line")
                root = alpha / -beta
                if best is None or root > best:
                    best = root
    return best


def enlargement_factor(Pi, ai, Pj, aj):
    """Least lambda > 1 at which Pj scaled about its centre by lambda touches Pi."""
    cj = centre(Pj)
    best = None
    for a in (ai[0], ai[1], aj[0], aj[1]):
        lo_i, hi_i = sat.proj_range(Pi, a)
        ca = cj[0] * a[0] + cj[1] * a[1]
        offs = [(p[0] - cj[0]) * a[0] + (p[1] - cj[1]) * a[1] for p in Pj]
        m_lo, m_hi = min(offs), max(offs)
        # gap pieces at scale L: (ca + L*m_lo) - hi_i  and  lo_i - (ca + L*m_hi)
        for alpha, beta in ((ca - hi_i, m_lo), (lo_i - ca, -m_hi)):
            if alpha + beta > 0:  # positive at L = 1
                root = alpha / -beta
                if best is None or root > best:
                    best = root
    return best


def scaled(P, lam):
    c = centre(P)
    return [(c[0] + lam * (x - c[0]), c[1] + lam * (y - c[1])) for x, y in P]


def summary(r):
    """The parts of a decide_data receipt the plan's statements are about."""
    pairs = r.get("pairs") or {}
    walls = r.get("walls") or {}
    return {
        "verdict": r["verdict"],
        "problems": r["problems"],
        "unit_A": r["squares"]["unit_A"],
        "unit_B": r["squares"]["unit_B"],
        "not_unit": r["squares"]["not_unit"],
        "inside_A": walls.get("inside_A"),
        "inside_B": walls.get("inside_B"),
        "contacts": sorted([c["id"], c["wall"]] for c in walls.get("contacts", [])),
        "outside": sorted([o["id"], o["wall"]] for o in walls.get("outside", [])),
        "wall_class_disagreements": len(walls.get("class_disagreements", [])),
        "classes_A": pairs.get("classes_A"),
        "classes_B": pairs.get("classes_B"),
        "pair_class_disagreements": pairs.get("class_disagreement_count"),
        "overlapping": [o["pair"] for o in pairs.get("overlapping", [])],
        "overlapping_detail": pairs.get("overlapping", [])[:5],
        "touching": [t["pair"] for t in pairs.get("touching", [])],
        "margins_sha256": pairs.get("margins_sha256"),
    }


def judge_file(exp, s, original_sha):
    """Hold a file-level summary to the plan's expectation. Returns a list of mismatches."""
    bad = []
    if s["verdict"] != exp["verdict"]:
        bad.append(f"verdict {s['verdict']}")
    if s["wall_class_disagreements"]:
        bad.append("the methods disagree on a wall class")
    if s["pair_class_disagreements"]:
        bad.append("the methods disagree on a pair class")
    if "overlapping_pairs" in exp and sorted(s["overlapping"]) != sorted(exp["overlapping_pairs"]):
        bad.append(f"overlapping {s['overlapping'][:10]}")
    if "touching_pairs" in exp and sorted(s["touching"]) != sorted(exp["touching_pairs"]):
        bad.append(f"touching {s['touching'][:10]}")
    if "outside" in exp and s["outside"] != sorted(exp["outside"]):
        bad.append(f"outside {s['outside'][:20]}")
    if "outside_ids" in exp and sorted({o[0] for o in s["outside"]}) != sorted(exp["outside_ids"]):
        bad.append(f"outside ids {sorted({o[0] for o in s['outside']})}")
    if "contacts" in exp and s["contacts"] != sorted(exp["contacts"]):
        bad.append(f"contacts {s['contacts']}")
    if "overlap_margin_A" in exp:
        det = s["overlapping_detail"]
        if not det or det[0]["margin"] != exp["overlap_margin_A"] or det[0]["area"] != exp["overlap_area_B"]:
            bad.append(f"overlap detail {det[:1]}")
    if "not_unit_A_and_B" in exp:
        ids = sorted(x["id"] for x in s["not_unit"])
        both = all(x["A"] and x["B"] for x in s["not_unit"])
        if ids != sorted(exp["not_unit_A_and_B"]) or not both:
            bad.append(f"not unit {s['not_unit']}")
    if "overlapping_pairs_at_least" in exp:
        a = (s["classes_A"] or {}).get("overlapping", 0)
        b = (s["classes_B"] or {}).get("overlapping", 0)
        if a < exp["overlapping_pairs_at_least"] or a != b:
            bad.append(f"overlapping A {a}, B {b}")
    if "unit_A_and_B" in exp and not (s["unit_A"] == s["unit_B"] == exp["unit_A_and_B"]):
        bad.append(f"unit A {s['unit_A']}, B {s['unit_B']}")
    if "inside_A_and_B" in exp and not (s["inside_A"] == s["inside_B"] == exp["inside_A_and_B"]):
        bad.append(f"inside A {s['inside_A']}, B {s['inside_B']}")
    if exp.get("margins_sha256_equal_original") and s["margins_sha256"] != original_sha:
        bad.append("margins differ from the original's")
    return bad


def main(argv):
    plan_path, count, cert, check_path, out = argv[1:6]
    t0 = util.cpu_seconds()
    plan = json.load(open(plan_path))
    cplan = plan["counts"][count]
    controls = cplan["controls"]
    with open(cert, encoding="utf-8") as fh:
        ytext = fh.read()
    data = reader.read_texts(ytext)
    original = json.load(open(check_path))
    original_sha = original["pairs"]["margins_sha256"]
    n = data["n"]
    ids = data["ids"]
    p, q = data["side"]
    S = Fraction(p, q)
    P = [sat.corners_frac(c) for c in data["corners"]]
    sq = [sat.square(x) for x in P]
    axes = [r[2] for r in sq]
    results = {}

    def file_control(name, d):
        r = chk.decide_data(d)
        s = summary(r)
        bad = judge_file(controls[name]["expect"], s, original_sha)
        s.pop("overlapping_detail", None)
        s["overlapping"] = s["overlapping"][:20]
        s["touching"] = s["touching"][:20]
        results[name] = {"level": "file", "status": "as stated" if not bad else "MISSED", "mismatches": bad, "observed": s}
        print(name, results[name]["status"], bad, flush=True)

    # G1: the last square given square 1's corners
    corners = list(data["corners"])
    corners[-1] = corners[0]
    file_control("G1", with_changes(data, corners=corners))
    # G2: square 1 translated by (S, 0)
    corners = list(data["corners"])
    corners[0] = to_raw([(x + S, y) for x, y in P[0]])
    file_control("G2", with_changes(data, corners=corners))
    # G3, G4: the reader
    last = f"  - id: {n}\n"
    head, tail = ytext.split(last, 1)
    claim_at = tail.index("  claim:\n")
    for name, text in (("G3", head + tail[claim_at:]), ("G4", ytext.replace(last, "  - id: 1\n", 1))):
        want = controls[name]["expect"]["reader_refuses_with"]
        try:
            reader.read_texts(text)
            got = "accepted"
        except reader.ReadError as exc:
            got = str(exc)
        ok = want in got and got != "accepted"
        results[name] = {"level": "reader", "status": "as stated" if ok else "MISSED", "observed": got}
        print(name, results[name]["status"], got, flush=True)
    # G5: square 1's third corner moved 1e-30 in x
    corners = list(data["corners"])
    P1 = list(P[0])
    P1[2] = (P1[2][0] + EPS, P1[2][1])
    corners[0] = to_raw(P1)
    file_control("G5", with_changes(data, corners=corners))
    # G6: every square reflected in its horizontal centre line
    refl = []
    for x in P:
        c = centre(x)
        refl.append(to_raw([(px, 2 * c[1] - py) for px, py in x]))
    file_control("G6", with_changes(data, corners=refl))
    # G8: transposed; G9: a quarter turn about the box centre
    file_control("G8", with_changes(data, corners=[to_raw([(y, x) for x, y in Q]) for Q in P]))
    file_control("G9", with_changes(data, corners=[to_raw([(S - y, x) for x, y in Q]) for Q in P]))
    # S1: the side
    floor12 = Fraction(util.floor_decimal(S, 12).replace(".", "")) / 10**12
    ceil12 = Fraction(util.ceil_decimal(S, 12).replace(".", "")) / 10**12
    file_control("S1a", with_changes(data, side=Fraction(p - 1, q)))
    file_control("S1b", with_changes(data, side=S - EPS))
    file_control("S1c", with_changes(data, side=floor12))
    file_control("S1d", with_changes(data, side=ceil12))
    # S3: every square moved 1e-30
    for name, (dx, dy) in (("S3L", (-EPS, 0)), ("S3R", (EPS, 0)), ("S3D", (0, -EPS)), ("S3U", (0, EPS))):
        file_control(name, with_changes(data, corners=[to_raw([(x + dx, y + dy) for x, y in Q]) for Q in P]))
    # S4: the least pair closed along its centre line, the second square moved
    lp = cplan["original"]["least_pair"]
    i, j = ids.index(lp[0]), ids.index(lp[1])
    ci, cj = centre(P[i]), centre(P[j])
    d = (ci[0] - cj[0], ci[1] - cj[1])
    s_star = closing_parameter(P[i], axes[i], P[j], axes[j], d)
    for name, s in (("S4c", s_star), ("S4p", s_star + EPS)):
        corners = list(data["corners"])
        corners[j] = to_raw([(x + s * d[0], y + s * d[1]) for x, y in P[j]])
        file_control(name, with_changes(data, corners=corners))
    results["S4c"]["closing"] = {"moved": lp[1], "toward": lp[0], "parameter": util.frac_str(s_star), "sci": util.sci(s_star, 10)}

    # S5: every pair below 1e-12 closed along its centre line (pair-level)
    own = [sat.own_ranges(P[k], axes[k]) for k in range(n)]
    PB = [clipm.corners_q(c) for c in data["corners"]]
    sqB = [clipm.square(x) for x in PB]
    thr = Fraction(1, 10**12)
    near = []
    for a in range(n):
        for b in range(a + 1, n):
            m, _ = sat.pair_margin(P[a], axes[a], own[a], P[b], axes[b], own[b])
            if 0 <= m < thr:
                near.append((a, b))
    s5_bad = []
    for a, b in near:
        ca, cb = centre(P[a]), centre(P[b])
        dd = (ca[0] - cb[0], ca[1] - cb[1])
        s = closing_parameter(P[a], axes[a], P[b], axes[b], dd)
        outcome = []
        for label, ss in (("contact", s), ("past", s + EPS)):
            Qb = [(x + ss * dd[0], y + ss * dd[1]) for x, y in P[b]]
            raw_b = to_raw(Qb)
            QA = sat.corners_frac(raw_b)
            mA, _ = sat.pair_margin(P[a], axes[a], own[a], QA, axes[b], sat.own_ranges(QA, axes[b]))
            QB = clipm.corners_q(raw_b)
            area, ne = clipm.pair(PB[a], clipm.halfplanes(QB, sqB[b][1]))
            if label == "contact":
                outcome.append(mA == 0 and area == 0 and ne)
            else:
                outcome.append(mA < 0 and area > 0)
        if not all(outcome):
            s5_bad.append({"pair": [ids[a], ids[b]], "contact_ok": outcome[0], "past_ok": outcome[1]})
    exp5 = controls["S5"]["expect"]
    ok5 = len(near) == exp5["pairs"] and not s5_bad
    results["S5"] = {
        "level": "pair",
        "status": "as stated" if ok5 else "MISSED",
        "pairs_closed": len(near),
        "failures": s5_bad[:50],
        "failure_count": len(s5_bad),
    }
    print("S5", results["S5"]["status"], len(near), len(s5_bad), flush=True)

    # S6: every square to its nearest wall by its clearance, and 1e-30 further (square-level)
    SB = clipm.mpq(p, q)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    s6_bad = []
    for k in range(n):
        cl = sat.wall_clearances(P[k], S)
        w = min(range(4), key=lambda t: (cl[t], t))
        okk = True
        for label, step in (("contact", cl[w]), ("past", cl[w] + EPS)):
            Q = [(x + dirs[w][0] * step, y + dirs[w][1] * step) for x, y in P[k]]
            r = to_raw(Q)
            ca = sat.wall_clearances(sat.corners_frac(r), S)
            QB = clipm.corners_q(r)
            cb = clipm.wall_classes(QB, SB)
            ia = clipm.inside_area(QB, SB)
            if label == "contact":
                okk = okk and ca[w] == 0 and all(c >= 0 for c in ca) and cb[w] == "contact" and ia == 1
            else:
                okk = okk and ca[w] < 0 and cb[w] == "outside" and ia < 1
        if not okk:
            s6_bad.append(ids[k])
    exp6 = controls["S6"]["expect"]
    results["S6"] = {
        "level": "square",
        "status": "as stated" if (not s6_bad and n == exp6["squares"]) else "MISSED",
        "squares": n,
        "failures": s6_bad[:50],
    }
    print("S6", results["S6"]["status"], len(s6_bad), flush=True)

    # S7: square j of the least pair enlarged about its centre until it touches i
    lam = enlargement_factor(P[i], axes[i], P[j], axes[j])
    for name, L in (("S7c", lam), ("S7p", lam + EPS)):
        Q = scaled(P[j], L)
        r = to_raw(Q)
        QA = sat.corners_frac(r)
        QB = clipm.corners_q(r)
        shape_refused = (not sat.square(QA)[0]) and (not clipm.square(QB)[0])
        mA, _ = sat.pair_margin(P[i], axes[i], own[i], QA, axes[j], sat.own_ranges(QA, axes[j]))
        area, ne = clipm.pair(PB[i], clipm.halfplanes(QB, sqB[j][1]))
        if name == "S7c":
            ok = shape_refused and mA == 0 and area == 0 and ne
        else:
            ok = shape_refused and mA < 0 and area > 0
        results[name] = {
            "level": "pair",
            "status": "as stated" if ok else "MISSED",
            "factor": util.frac_str(L),
            "factor_minus_one_sci": util.sci(L - 1, 8),
            "shape_refused_A_and_B": shape_refused,
            "margin_A": util.sci(mA, 8),
            "area_B": util.sci(Fraction(int(area.numerator), int(area.denominator)), 8) if area else "0",
            "nonempty_B": ne,
        }
        print(name, results[name]["status"], flush=True)

    # S8: the far-wall square enlarged by 1 + 1e-30
    far = [c for c in cplan["original"]["contacts"] if c[1] in ("right", "top")][0]
    k = ids.index(far[0])
    w = {"right": 1, "top": 3}[far[1]]
    Q = scaled(P[k], 1 + EPS)
    r = to_raw(Q)
    QA = sat.corners_frac(r)
    QB = clipm.corners_q(r)
    shape_refused = (not sat.square(QA)[0]) and (not clipm.square(QB)[0])
    wa = sat.wall_class(sat.wall_clearances(QA, S)[w])
    wb = clipm.wall_classes(QB, SB)[w]
    corners = list(data["corners"])
    corners[k] = r
    fv = chk.decide_data(with_changes(data, corners=corners))["verdict"]
    ok8 = shape_refused and wa == "outside" and wb == "outside" and fv == "REFUSE"
    results["S8"] = {
        "level": "square",
        "status": "as stated" if ok8 else "MISSED",
        "square": far,
        "shape_refused_A_and_B": shape_refused,
        "wall_A": wa,
        "wall_B": wb,
        "file_verdict": fv,
    }
    print("S8", results["S8"]["status"], flush=True)

    missed = sorted(name for name, r in results.items() if r["status"] != "as stated")
    stated = sorted(controls)
    receipt = {
        "program": "l72_controls.py",
        "lane": "L72",
        "bead": "think-qqyg",
        "environment": util.environment(),
        "program_digests": util.program_digests([os.path.join(HERE, f) for f in PROGRAMS[:-1]] + [plan_path]),
        "count": count,
        "certificate": {"file": os.path.basename(cert), "sha256": util.sha256_file(cert)},
        "original_margins_sha256": original_sha,
        "controls_stated": len(stated),
        "controls_run": len(results),
        "unrun": sorted(set(stated) - set(results)),
        "missed": missed,
        "verdict": "EVERY_CONTROL_AS_STATED" if not missed and set(stated) == set(results) else "SOME_CONTROL_MISSED",
        "results": results,
        "cpu_seconds": round(util.cpu_seconds() - t0, 2),
    }
    util.write_receipt(out, receipt)
    print(receipt["verdict"], missed, f"{receipt['cpu_seconds']} s")
    return 0 if not missed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
