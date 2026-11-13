"""Run the 20 controls of controls-plan.json and compare each with its stated outcome.

Lane L127, clean room. Written after the plan was stated and hashed. Usage:

    python -I -B l127_controls.py CERT.yaml TWIN.json PLAN.json FACTS.json CHECK.json OUT.json

Whole-file controls are decided by l127_check.decide (both methods, every square, wall
and pair); reader controls by l127_reader on the changed YAML and twin; S5 at pair level
and S6 at square level by both methods.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l127_check as ck  # noqa: E402
import l127_clip as mb  # noqa: E402
import l127_geom as g  # noqa: E402
import l127_reader as rd  # noqa: E402
import l127_sat as ma  # noqa: E402

TINY = F(1, 10**30)
Corner = tuple[tuple[int, int], tuple[int, int]]


def frac_pts(sq: list[Corner]) -> list[tuple[F, F]]:
    return [(F(*x), F(*y)) for x, y in sq]


def int_pts(pts: list[tuple[F, F]]) -> list[Corner]:
    return [((x.numerator, x.denominator), (y.numerator, y.denominator)) for x, y in pts]


def transform(squares: list[list[Corner]], fn: Any) -> list[list[Corner]]:
    return [int_pts([fn(x, y) for x, y in frac_pts(sq)]) for sq in squares]


def centre(sq: list[Corner]) -> tuple[F, F]:
    p = frac_pts(sq)
    return ((p[0][0] + p[2][0]) / 2, (p[0][1] + p[2][1]) / 2)


def translate(sq: list[Corner], dx: F, dy: F) -> list[Corner]:
    return int_pts([(x + dx, y + dy) for x, y in frac_pts(sq)])


def compare_whole(res: dict[str, Any], expect: dict[str, Any]) -> list[str]:
    diffs: list[str] = []
    for key, want in expect.items():
        if key == "overlapping_pairs":
            got = [o["pair"] for o in res.get("overlapping_pairs", [])]
            ok = bool(got) if want == "nonempty" else got == want
        elif key == "overlap_margin":
            m = res["_margins"].get((1, 269))
            got = None if m is None else ck.rat_str(m)
            ok = got == want
        elif key == "overlap_area":
            got = [o["area"] for o in res.get("overlapping_pairs", [])]
            ok = got == [want]
        elif key == "least_margin_value":
            got = res.get("least_margin", {}).get("value")
            ok = got == want
        elif key in ("wall_contacts", "outside_a", "outside_b"):
            got = sorted(res.get(key, []))
            ok = got == sorted(want)
        else:
            got = res.get(key)
            ok = got == want
        if not ok:
            diffs.append(f"{key}: stated {want!r}, came out {got!r}")
    return diffs


def summary(res: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "verdict",
        "not_unit_a",
        "not_unit_b",
        "wall_contacts",
        "outside_a",
        "outside_b",
        "not_inside_b",
        "wall_disagreements",
        "pair_disagreements",
        "overlap_count",
        "touching_pairs",
        "ccw_count",
        "cw_count",
        "margin_list_sha256",
        "least_margin",
        "overlap_area_sum",
    )
    out = {k: res[k] for k in keys if k in res}
    if res.get("overlapping_pairs"):
        out["overlapping_pairs_first"] = res["overlapping_pairs"][:5]
    return out


def reader_control(ytext: str, jtext: str, want: str) -> tuple[bool, str]:
    try:
        rd.read_certificate(ytext, jtext)
    except rd.Refused as exc:
        return (want in str(exc), f"refused: {exc}")
    return (False, "accepted")


def main(argv: list[str]) -> int:
    t0 = time.process_time()
    cert, twin, planp, factsp, checkp, outp = (Path(a) for a in argv[1:7])
    ytext = cert.read_text(encoding="utf-8")
    jtext = twin.read_text(encoding="utf-8")
    plan = json.loads(planp.read_text(encoding="utf-8"))
    facts = json.loads(factsp.read_text(encoding="utf-8"))
    rec = json.loads(checkp.read_text(encoding="utf-8"))
    doc = rd.read_certificate(ytext, jtext)
    side = doc["side"]
    S = F(*side)
    sqs: list[list[Corner]] = doc["squares"]
    n = len(sqs)
    assert plan["certificate_margin_list_sha256"] == rec["margin_list_sha256"]
    results: list[dict[str, Any]] = []

    def whole(cid: str, side_: tuple[int, int], squares: list[list[Corner]]) -> None:
        c = next(c for c in plan["controls"] if c["id"] == cid)
        t = time.process_time()
        res = ck.decide(side_, squares, keep_margins=True)
        diffs = compare_whole(res, c["expect"])
        entry = {"id": cid, "as_stated": not diffs, "diffs": diffs, "result": summary(res), "cpu": round(time.process_time() - t, 1)}
        results.append(entry)
        print(cid, "as stated" if not diffs else f"NOT as stated: {diffs}", flush=True)

    def reader(cid: str, y: str, j: str) -> None:
        c = next(c for c in plan["controls"] if c["id"] == cid)
        ok, got = reader_control(y, j, c["expect"]["refused"])
        results.append({"id": cid, "as_stated": ok, "result": got})
        print(cid, "as stated" if ok else "NOT as stated", got[:120], flush=True)

    # ---- G1
    g1 = [list(s) for s in sqs]
    g1[n - 1] = list(sqs[0])
    whole("G1", side, g1)
    # ---- G2
    g2 = [list(s) for s in sqs]
    g2[0] = translate(sqs[0], S, F(0))
    whole("G2", side, g2)
    # ---- G3: delete square 269's entry
    start = ytext.index(f"  - id: {n}\n")
    end = ytext.index("  claim:\n")
    y3 = ytext[:start] + ytext[end:]
    t3 = json.loads(jtext)
    del t3["witness"]["squares"][n - 1]
    reader("G3", y3, json.dumps(t3))
    # ---- G4: square 269's id set to 1
    y4 = ytext.replace(f"  - id: {n}\n", "  - id: 1\n", 1)
    t4 = json.loads(jtext)
    t4["witness"]["squares"][n - 1]["id"] = 1
    reader("G4", y4, json.dumps(t4))
    # ---- G5
    g5 = [list(s) for s in sqs]
    p = frac_pts(sqs[0])
    p[2] = (p[2][0] + TINY, p[2][1])
    g5[0] = int_pts(p)
    whole("G5", side, g5)
    # ---- G6: every square reflected in its own horizontal centre line
    g6 = []
    for s in sqs:
        _, cy = centre(s)
        g6.append(int_pts([(x, 2 * cy - y) for x, y in frac_pts(s)]))
    whole("G6", side, g6)
    # ---- G7: the twin's side altered in its last digit
    t7 = json.loads(jtext)
    sd = t7["witness"]["side"]
    t7["witness"]["side"] = sd[:-1] + ("1" if sd[-1] != "1" else "2")
    reader("G7", ytext, json.dumps(t7))
    # ---- G8
    whole("G8", side, transform(sqs, lambda x, y: (y, x)))
    # ---- G9: the side as 2p/2q
    sp, sq_ = side
    old_line = f"  side: {sp}/{sq_}\n"
    assert ytext.count(old_line) == 1
    y9 = ytext.replace(old_line, f"  side: {2 * sp}/{2 * sq_}\n")
    t9 = json.loads(jtext)
    t9["witness"]["side"] = f"{2 * sp}/{2 * sq_}"
    reader("G9", y9, json.dumps(t9))
    # ---- G10, G11
    whole("G10", side, [s[1:] + s[:1] for s in sqs])
    whole("G11", side, [[s[0], s[3], s[2], s[1]] for s in sqs])
    # ---- G12: quarter turn about the box centre
    whole("G12", side, transform(sqs, lambda x, y: (S - y, x)))
    # ---- S1
    def rat(x: F) -> tuple[int, int]:
        return (x.numerator, x.denominator)

    whole("S1a", rat(S - F(1, sq_)), sqs)
    whole("S1b", rat(S - TINY), sqs)
    whole("S1c", rat(F(facts["floor12_decimal"])), sqs)
    whole("S1d", rat(F(facts["ceil12_decimal"])), sqs)
    # ---- S4
    ch = facts["S4"]["chosen"]
    cand = next(c for c in facts["S4"]["candidates"] if c["move"] == ch["move"])
    mv, tw = ch["move"], ch["towards"]
    cm, ct = centre(sqs[mv - 1]), centre(sqs[tw - 1])
    for cid, tkey in (("S4c", "t_star"), ("S4p", "t_past")):
        t = F(cand[tkey])
        s4 = [list(s) for s in sqs]
        s4[mv - 1] = translate(sqs[mv - 1], -t * (cm[0] - ct[0]), -t * (cm[1] - ct[1]))
        whole(cid, side, s4)
    # ---- S5: pair level
    t = time.process_time()
    digest = hashlib.sha256()
    s5_bad: list[str] = []
    s5_count = 0
    past_vals: dict[str, int] = {}
    pl = []
    for s in sqs:
        pts = frac_pts(s)
        cx, cy = centre(s)
        pl.append(g.Placed(cx, cy, pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]))
    stated = {tuple(e["pair"]): e["cf_past"] for e in facts["S5"]["pairs"]}
    for item in rec["near_pairs_below_1e-12"]:
        a, b = item["pair"]
        clo = g.closing(pl[a - 1], pl[b - 1])
        t_past = clo.t_star + TINY / min(clo.binding_rates)
        sa_ = ma.make_square(sqs[a - 1])
        sb_ = mb.make_square(sqs[a - 1])
        cb_ = centre(sqs[b - 1])
        ca_ = centre(sqs[a - 1])
        for label, tt, want_m, want_c in (("at", clo.t_star, F(0), "touch"), ("past", t_past, F(stated[(a, b)]), "overlap")):
            moved = translate(sqs[b - 1], -tt * (cb_[0] - ca_[0]), -tt * (cb_[1] - ca_[1]))
            m = ma.pair_margin(sa_, ma.make_square(moved))
            cls_b, _ = mb.pair(sb_, mb.make_square(moved))
            got_m = F(m[0], m[1])
            if got_m != want_m or ma.pair_class(m) != want_c or cls_b != want_c:
                s5_bad.append(f"{a},{b} {label}: margin {float(got_m):.3e} A {ma.pair_class(m)} B {cls_b}")
            if label == "past":
                past_vals[ck.rat_str(m)] = past_vals.get(ck.rat_str(m), 0) + 1
        digest.update(f"{a} {b} {ck.rat_str((clo.t_star.numerator, clo.t_star.denominator))} "
                      f"{ck.rat_str((t_past.numerator, t_past.denominator))} {stated[(a, b)]}\n".encode())
        s5_count += 1
    digest_ok = digest.hexdigest() == facts["S5"]["closing_digest"]
    s5_ok = not s5_bad and digest_ok and s5_count == facts["S5"]["count"]
    results.append(
        {
            "id": "S5",
            "as_stated": s5_ok,
            "result": {
                "pairs": s5_count,
                "failures": s5_bad[:10],
                "past_margins": past_vals,
                "closing_digest_matches_plan": digest_ok,
            },
            "cpu": round(time.process_time() - t, 1),
        }
    )
    print("S5", "as stated" if s5_ok else f"NOT as stated {s5_bad[:3]} digest {digest_ok}", s5_count, flush=True)
    # ---- S6: square level
    t = time.process_time()
    s6_bad: list[str] = []
    walls_hist: dict[str, int] = {}
    for e in facts["S6"]["nearest_walls"]:
        k, wall, c = e["square"], e["wall"], F(e["clearance"])
        walls_hist[wall] = walls_hist.get(wall, 0) + 1
        for label, dist, want, want_ca, want_cb, want_in in (
            ("at", c, F(0), "touch", "touch", True),
            ("past", c + TINY, -TINY, "outside", "outside", False),
        ):
            dx, dy = {"left": (-dist, F(0)), "bottom": (F(0), -dist), "right": (dist, F(0)), "top": (F(0), dist)}[wall]
            moved = translate(sqs[k - 1], dx, dy)
            sa_ = ma.make_square(moved)
            sb_ = mb.make_square(moved)
            cl = ma.wall_clearances(sa_, side)[wall]
            cb = mb.wall_classes(sb_, side)[wall]
            inside = mb.inside_box(sb_, side)
            if F(cl[0], cl[1]) != want or ma.wall_class(cl) != want_ca or cb != want_cb or inside != want_in:
                s6_bad.append(f"{k} {wall} {label}")
    s6_ok = not s6_bad and len(facts["S6"]["nearest_walls"]) == n
    results.append({"id": "S6", "as_stated": s6_ok, "result": {"squares": n, "nearest_walls": walls_hist, "failures": s6_bad[:10]}, "cpu": round(time.process_time() - t, 1)})
    print("S6", "as stated" if s6_ok else f"NOT as stated {s6_bad[:3]}", flush=True)

    order = [c["id"] for c in plan["controls"]]
    results.sort(key=lambda r: order.index(r["id"]))
    not_ok = [r["id"] for r in results if not r["as_stated"]]
    receipt = {
        "program": "l127_controls.py",
        "verdict": "EVERY_CONTROL_AS_STATED" if not not_ok and len(results) == len(order) else "NOT_EVERY_CONTROL_AS_STATED",
        "as_stated": len(results) - len(not_ok),
        "of": len(order),
        "not_as_stated": not_ok,
        "plan_sha256": hashlib.sha256(planp.read_bytes()).hexdigest(),
        "controls": results,
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    outp.write_text(json.dumps(receipt, indent=1, default=str) + "\n", encoding="utf-8")
    print(receipt["verdict"], receipt["as_stated"], "of", receipt["of"])
    return 0 if not not_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
