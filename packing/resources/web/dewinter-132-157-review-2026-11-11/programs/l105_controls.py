"""Lane L105's controls: run every control the plan states and hold it to the plan.

Usage: python -I -B l105_controls.py SOURCE_DIR N PLAN_JSON OUT_JSON

Written after the plan's digest was recorded. Builds each modified file or packing,
decides it with the frozen reader and `l105_check.decide` (both methods), or, for the
pair- and square-level controls, with the frozen methods directly, and compares the
result with the stated outcome exactly. Prints EVERY_CONTROL_AS_STATED or the list of
controls that were not.
"""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l105_check as K  # noqa: E402
import l105_clip as B  # noqa: E402
import l105_geom as G  # noqa: E402
import l105_reader as R  # noqa: E402
import l105_sat as A  # noqa: E402

EPS = F(1, 10**30)
WALLS = ("left", "bottom", "right", "top")


def walls(rows: list[dict[str, Any]]) -> list[list[Any]]:
    return sorted([r["square"], r["wall"]] for r in rows)


def pairs(rows: list[list[int]]) -> list[list[int]]:
    return sorted(sorted(p) for p in rows)


def pk_of(base: dict[str, Any], squares: list[G.Sq] | None = None, side: F | None = None) -> dict[str, Any]:
    return {
        "n": len(squares) if squares is not None else base["n"],
        "side": G.rat(side) if side is not None else base["side"],
        "squares": squares if squares is not None else list(base["squares"]),
    }


def summary(r: dict[str, Any]) -> dict[str, Any]:
    return {
        "verdict": r["verdict"],
        "overlapping_pairs": pairs(r["overlapping_pairs"]),
        "overlapping_pair_count": r["overlapping_pair_count"],
        "touching_pairs": pairs(r["touching_pairs"]),
        "walls_outside": walls(r["walls_outside"]),
        "wall_contacts": walls(r["wall_contacts"]),
        "unit_squares_a": r["unit_squares_a"],
        "unit_squares_b": r["unit_squares_b"],
        "pair_class_disagreement_count": r["pair_class_disagreement_count"],
        "wall_class_disagreements": r["wall_class_disagreements"],
        "wall_clearances_unequal_a_b": r["wall_clearances_unequal_a_b"],
        "margin_list_sha256": r["margin_list_sha256"],
        "sum_clipped_pair_area_b_sci": r["sum_clipped_pair_area_b_sci"],
    }


def held(expect: dict[str, Any], got: dict[str, Any]) -> bool:
    for k, v in expect.items():
        if k == "overlapping_pairs_at_least":
            if got["overlapping_pair_count"] < v:
                return False
        elif got.get(k) != v:
            return False
    return True


def pair_both(si: G.Sq, sj: G.Sq) -> tuple[F, str, str, F]:
    m, _ = A.margin(A.build(si), A.build(sj))
    cb, ar = B.pair_class(B.ccw(B.corners(si)), B.ccw(B.corners(sj)))
    return m, A.classify(m), cb, F(int(ar.numerator), int(ar.denominator))


def run(src: Path, n: int, plan: dict[str, Any]) -> dict[str, Any]:
    d = src / f"n{n}"
    jtext = (d / f"n{n}_exact.json").read_bytes().decode()
    ytext = (d / f"n{n}_witness.yaml").read_bytes().decode()
    base = R.read_json_text(jtext)
    S = A.frac(base["side"])
    sqs: list[G.Sq] = list(base["squares"])
    base_clr = [A.clearances(A.build(s), S) for s in sqs]
    res: dict[str, Any] = {}

    def full(name: str, pk: dict[str, Any], extra: dict[str, Any] | None = None) -> dict[str, Any]:
        r = K.decide(pk, name)
        got = summary(r)
        if extra:
            got.update(extra)
        exp = plan[name]["expect"]
        res[name] = {"what": plan[name].get("what", ""), "stated": exp, "came_out": got, "as_stated": held(exp, got)}
        return r

    # G1: duplicate
    g1 = list(sqs)
    g1[n - 1] = sqs[0]
    m1n, ca, cb, ar = pair_both(sqs[0], g1[n - 1])
    eq = all(
        A.margin(A.build(g1[k]), A.build(g1[n - 1]))[0] == A.margin(A.build(sqs[k]), A.build(sqs[0]))[0]
        for k in range(1, n - 1)
    )
    full("G1_duplicate", pk_of(base, g1), {"margin_1n": K.frac_text(m1n), "area_1n": K.frac_text(ar), "margins_k_n_equal_base_k_1": eq})

    # G2: square 1 translated by (S, 0)
    g2 = list(sqs)
    x, y, c, s = G.unpack(sqs[0])
    g2[0] = G.sq(x + S, y, c, s)
    full("G2_translated", pk_of(base, g2))

    # G3: last entry deleted, JSON and YAML
    obj = json.loads(jtext)
    obj["squares"] = obj["squares"][:-1]
    jt3 = json.dumps(obj, indent=0)
    cut = ytext.index(f"  - id: {n}\n")
    yt3 = ytext[:cut]

    def reader_outcome(fn: Any, text: str) -> str:
        try:
            fn(text)
            return "accepts"
        except R.ReadError as exc:
            return f"refuses: {exc}"

    jr, yr = reader_outcome(R.read_json_text, jt3), reader_outcome(R.read_yaml_text, yt3)
    exp = plan["G3_deleted"]["expect"]
    ok = jr.startswith("refuses") and "entries" in jr and yr.startswith("refuses") and "entries" in yr
    res["G3_deleted"] = {"what": plan["G3_deleted"]["what"], "stated": exp, "came_out": {"json_reader": jr, "yaml_reader": yr}, "as_stated": ok}

    # G4: YAML id 2 -> 1
    yt4 = ytext.replace("  - id: 2\n", "  - id: 1\n", 1)
    yr4 = reader_outcome(R.read_yaml_text, yt4)
    res["G4_id"] = {"what": plan["G4_id"]["what"], "stated": plan["G4_id"]["expect"], "came_out": {"yaml_reader": yr4}, "as_stated": yr4.startswith("refuses") and "order" in yr4}

    # G5: square 1 not a unit square
    g5 = list(sqs)
    g5[0] = G.sq(x, y, c + EPS, s)
    full("G5_not_unit", pk_of(base, g5))

    # G6: rotation read the other way
    g6 = [G.sq(*(lambda t: (t[0], t[1], t[2], -t[3]))(G.unpack(q))) for q in sqs]
    clr6 = [A.clearances(A.build(q), S) for q in g6]
    full("G6_rotation_reversed", pk_of(base, g6), {"clearances_equal_base": clr6 == base_clr})

    # G7: twin side altered; G7b: one scalar altered
    js = R.read_json_text(jtext)
    side_line_start = ytext.index("  side: ")
    slash = ytext.index("/", side_line_start)
    last = ytext[slash - 1]
    yt7 = ytext[: slash - 1] + ("8" if last != "8" else "7") + ytext[slash:]
    c7 = R.compare(js, R.read_yaml_text(yt7))
    got7 = {"same_packing": c7["same_packing"], "side_equal": c7["side_equal"], "scalar_difference_count": c7["scalar_difference_count"]}
    res["G7_twin_side"] = {"what": plan["G7_twin_side"]["what"], "stated": plan["G7_twin_side"]["expect"], "came_out": got7, "as_stated": held(plan["G7_twin_side"]["expect"], got7)}
    blk = ytext.index("  - id: 2\n")
    xline = ytext.index("    - ", ytext.index("    center:\n", blk))
    eol = ytext.index("\n", xline)
    sl = ytext.index("/", xline) if "/" in ytext[xline:eol] else eol
    d0 = ytext[sl - 1]
    yt7b = ytext[: sl - 1] + ("8" if d0 != "8" else "7") + ytext[sl:]
    c7b = R.compare(js, R.read_yaml_text(yt7b))
    got7b = {"same_packing": c7b["same_packing"], "side_equal": c7b["side_equal"], "scalar_difference_count": c7b["scalar_difference_count"], "differences": c7b["scalar_differences"]}
    res["G7b_twin_scalar"] = {"what": plan["G7b_twin_scalar"]["what"], "stated": plan["G7b_twin_scalar"]["expect"], "came_out": got7b, "as_stated": held(plan["G7b_twin_scalar"]["expect"], got7b)}

    # G8: transpose
    g8 = [G.sq(*(lambda t: (t[1], t[0], t[3], t[2]))(G.unpack(q))) for q in sqs]
    clr8 = [A.clearances(A.build(q), S) for q in g8]
    tr = all(clr8[k] == (base_clr[k][1], base_clr[k][0], base_clr[k][3], base_clr[k][2]) for k in range(n))
    full("G8_transposed", pk_of(base, g8), {"clearances_transposed_exactly": tr})

    # S1: the side lowered or raised
    for name in ("S1a_side_minus_1_over_q", "S1b_side_minus_1e-30", "S1c_side_floor12", "S1d_side_ceil12"):
        num, _, den = plan[name]["side"].partition("/")
        new = F(int(num), int(den or "1"))
        full(name, pk_of(base, side=new))

    # S3: tightest qualifying pair closed to contact, whole file
    s3 = plan["S3_tightest_pair_contact"]
    if s3.get("expect"):
        i, j = s3["pair"]
        mover = s3["moved"]
        other = j if mover == i else i
        g3 = list(sqs)
        g3[mover - 1] = G.close_pair(sqs[other - 1], sqs[mover - 1], F(0))
        full("S3_tightest_pair_contact", pk_of(base, g3))
    else:
        res["S3_tightest_pair_contact"] = {"stated": None, "came_out": None, "as_stated": True}

    # S4: every near pair, pair-level
    bad4 = []
    count4 = 0
    facts = json.loads((Path(sys.argv[4]).parent / f"plan-facts-n{n}.json").read_text())
    for rec in facts["near_pairs"]:
        i, j = rec["pair"]
        for t, cls in ((F(0), "contact"), (-EPS, "overlap")):
            mv = G.close_pair(sqs[i - 1], sqs[j - 1], t)
            m, ca, cb, _ = pair_both(sqs[i - 1], mv)
            count4 += 1
            if not (m == t and ca == cls and cb == cls):
                bad4.append([i, j, K.sci(t), K.sci(m), ca, cb])
    res["S4_near_pairs"] = {
        "what": plan["S4_near_pairs"]["what"],
        "stated": plan["S4_near_pairs"]["expect"],
        "came_out": {"pairs": len(facts["near_pairs"]), "decisions": count4, "not_as_stated": bad4[:20]},
        "as_stated": not bad4 and len(facts["near_pairs"]) == plan["S4_near_pairs"]["pairs"],
    }

    # S5: every square to its nearest wall, square-level
    bad5 = []
    sideQ = B.q(G.rat(S))
    for rec in facts["nearest_walls"]:
        k, w = rec["square"], rec["wall"]
        wi = WALLS.index(w)
        for t, cls_a, cls_b in ((F(0), "contact", "contact"), (-EPS, "outside", "outside")):
            mv = G.move_to_wall(sqs[k - 1], w, S, t)
            ca = A.clearances(A.build(mv), S)[wi]
            cb, clr_b, _ = B.wall_facts(B.ccw(B.corners(mv)), sideQ)[wi]
            if not (ca == t and A.wall_class(ca) == cls_a and cb == cls_b and F(int(clr_b.numerator), int(clr_b.denominator)) == ca):
                bad5.append([k, w, K.sci(t), K.sci(ca), cb])
    res["S5_walls"] = {
        "what": plan["S5_walls"]["what"],
        "stated": plan["S5_walls"]["expect"],
        "came_out": {"squares": len(facts["nearest_walls"]), "not_as_stated": bad5[:20]},
        "as_stated": not bad5 and len(facts["nearest_walls"]) == n,
    }
    return res


def main() -> None:
    sys.set_int_max_str_digits(0)
    src, n, planp, outp = Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    plan_bytes = planp.read_bytes()
    plan = json.loads(plan_bytes)["plans"][str(n)]
    res = run(src, n, plan)
    not_as = [k for k, v in res.items() if not v["as_stated"]]
    me = {p: hashlib.sha256((HERE / p).read_bytes()).hexdigest() for p in ("l105_controls.py", "l105_geom.py", "l105_reader.py", "l105_sat.py", "l105_clip.py", "l105_check.py")}
    out = {
        "program": "l105_controls.py",
        "n": n,
        "plan_sha256": hashlib.sha256(plan_bytes).hexdigest(),
        "program_sha256": me,
        "controls": res,
        "status": "EVERY_CONTROL_AS_STATED" if not not_as else "NOT_AS_STATED",
        "not_as_stated": not_as,
    }
    outp.write_text(json.dumps(out, indent=1) + "\n")
    print(f"n={n} {out['status']} {len(res)} controls {not_as}")
    for k, v in res.items():
        co = v["came_out"] or {}
        brief = {kk: co.get(kk) for kk in ("verdict", "overlapping_pair_count", "walls_outside", "touching_pairs") if kk in co}
        print(f"  {k}: {'as stated' if v['as_stated'] else 'NOT AS STATED'} {json.dumps(brief)[:160]}")


if __name__ == "__main__":
    main()
