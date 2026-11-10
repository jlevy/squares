"""Run the 23 controls of controls-plan.json with the frozen checker and compare each with
its stated outcome. Written after the plan was stated and hashed.

Run: python -I -B l77_controls.py CANDIDATE.yaml PLAN.json OUT.json [WORKERS]
"""

from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import os
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l77_checker as C  # noqa: E402

EPS = F(1, 10**30)
W: dict = {}


def q(x: F) -> tuple[int, int]:
    return (x.numerator, x.denominator)


def fq(t: tuple[int, int]) -> F:
    return F(t[0], t[1])


def shift(cs: list, dx: F, dy: F) -> list:
    return [(q(fq(x) + dx), q(fq(y) + dy)) for x, y in cs]


def unit(x0: F, y0: F) -> list:
    return [(q(x0), q(y0)), (q(x0 + 1), q(y0)), (q(x0 + 1), q(y0 + 1)), (q(x0), q(y0 + 1))]


def setup(cand: str) -> None:
    w = C.read_witness(cand)
    W["w"] = w
    W["S"] = fq(w["side"])
    W["corners"] = w["corners"]
    W["text"] = open(cand).read()
    W["WC0"] = {(46, "left"), (85, "bottom"), (173, "left"), (173, "top"), (187, "bottom"), (187, "right")} | {
        (k, "top") for k in range(174, 187)} | {(k, "right") for k in range(188, 200)}
    W["TP0"] = {(k, k + 1) for k in range(173, 186)} | {(k, k + 1) for k in range(187, 199)}


def contacts(r: dict) -> set:
    a = {(i, s) for i, s in r["wall_contacts"]["A"]}
    b = {(i, s) for i, s in r["wall_contacts"]["B"]}
    assert a == b
    return a


def touching(r: dict) -> set:
    a = {tuple(p) for p in r["touching_pairs"]["A"]}
    b = {tuple(p) for p in r["touching_pairs"]["B"]}
    assert a == b
    return a


def overl(r: dict, m: str) -> list:
    return [tuple(p) for p in r["overlapping_pairs"][m]]


def outside(r: dict) -> list:
    assert r["outside"]["A"] == r["outside"]["B"]
    return r["outside"]["A"]


def summary(r: dict) -> dict:
    return {"verdict": r["verdict"], "outside": r["outside"]["A"], "overlapping_A": r["overlapping_pairs"]["A"][:80],
            "overlapping_B": r["overlapping_pairs"]["B"][:80], "n_overlapping": len(r["overlapping_pairs"]["A"]),
            "not_unit_square": r["not_unit_square"], "n_wall_contacts": len(r["wall_contacts"]["A"]),
            "n_touching": len(r["touching_pairs"]["A"]), "least_positive_pair_margin": r["least_positive_pair_margin"],
            "least_positive_wall_clearance": r["least_positive_wall_clearance"],
            "disagreements": [r["pair_class_disagreements"], r["wall_class_disagreements"]]}


def ctl(cid: str) -> dict:
    S, cs, WC0, TP0 = W["S"], W["corners"], W["WC0"], W["TP0"]
    ids = list(range(1, 200))
    t0 = time.process_time()
    ok = False
    obs: dict = {}
    if cid == "G1":
        c2 = list(cs)
        c2[198] = cs[0]
        r = C.decide(q(S), c2)
        ok = (r["verdict"] == "REFUSE" and overl(r, "A") == [(1, 199, "-1")] and overl(r, "B") == [(1, 199, "1")]
              and touching(r) == TP0 - {(198, 199)} and contacts(r) == WC0 - {(199, "right")} and not outside(r))
        obs = summary(r)
    elif cid == "G2":
        c2 = list(cs)
        c2[0] = shift(cs[0], S, F(0))
        r = C.decide(q(S), c2)
        ok = (r["verdict"] == "REFUSE" and outside(r) == [1] and not overl(r, "A") and not overl(r, "B")
              and touching(r) == TP0 and contacts(r) == WC0)
        obs = summary(r)
    elif cid in ("G3", "G4"):
        text = W["text"]
        a = text.index("  - id: 199\n")
        if cid == "G3":
            b = text.index("  claim:\n")
            t2 = text[:a] + text[b:]
        else:
            t2 = text[:a] + "  - id: 1\n" + text[a + len("  - id: 199\n"):]
        try:
            C.read_witness_text(t2)
            obs = {"reader": "accepted"}
        except C.Refused as e:
            obs = {"reader": "refused", "reason": str(e)}
            want = "n = 199 but 198 squares" if cid == "G3" else "repeated square id"
            ok = want in str(e)
    elif cid == "G5":
        c2 = list(cs)
        sq = list(cs[0])
        x, y = sq[2]
        sq[2] = (q(fq(x) + EPS), y)
        c2[0] = sq
        r = C.decide(q(S), c2)
        ok = r["verdict"] == "REFUSE" and r["not_unit_square"] == {"A": [1], "B": [1]}
        obs = summary(r)
    elif cid == "G6":
        def refl(sqc: list) -> list:
            ys = [fq(y) for _, y in sqc]
            cy = (ys[0] + ys[2]) / 2
            return [(x, q(2 * cy - fq(y))) for x, y in sqc]
        c2 = [refl(s) for s in cs]
        r = C.decide(q(S), c2)
        r172 = C.decide(q(S - 1), c2[:172])
        oa = set(overl(r, "A"))
        oa172 = set(overl(r172, "A"))
        ok = (r["verdict"] == "REFUSE" and not r["not_unit_square"]["A"] and not r["not_unit_square"]["B"]
              and not outside(r) and oa == oa172 and all(i <= 172 and j <= 172 for i, j, _ in oa)
              and {p[:2] for p in overl(r, "B")} == {p[:2] for p in oa} and r172["verdict"] == "REFUSE")
        obs = summary(r)
        obs["n_overlapping_172_alone"] = len(oa172)
        obs["new_touching_pairs"] = sorted(touching(r) - TP0)
    elif cid in ("G8", "G9"):
        if cid == "G8":
            f = lambda x, y: (y, x)  # noqa: E731
            mp_ = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}
        else:
            f = lambda x, y: (S - y, x)  # noqa: E731
            mp_ = {"left": "bottom", "bottom": "right", "right": "top", "top": "left"}
        c2 = [[tuple(q(v) for v in f(fq(x), fq(y))) for x, y in s] for s in cs]
        r = C.decide(q(S), c2)
        base = W["base"]
        ok = (r["verdict"] == "ACCEPT" and contacts(r) == {(i, mp_[s]) for i, s in WC0} and touching(r) == TP0
              and r["least_positive_pair_margin"]["value"] == base["least_positive_pair_margin"]["value"]
              and r["least_positive_pair_margin"]["pair"] == [161, 199])
        obs = summary(r)
    elif cid in ("S1a", "S1b", "S1c", "S1d"):
        side = {"S1a": S - F(1, S.denominator), "S1b": S - EPS, "S1c": F("14.614689853286"),
                "S1d": F("14.614689853287")}[cid]
        r = C.decide(q(side), cs)
        if cid == "S1d":
            ok = (r["verdict"] == "ACCEPT" and contacts(r) == {(46, "left"), (85, "bottom"), (173, "left"), (187, "bottom")}
                  and touching(r) == TP0)
        else:
            ok = (r["verdict"] == "REFUSE" and outside(r) == list(range(173, 200)) and not overl(r, "A")
                  and not overl(r, "B"))
        obs = summary(r)
        obs["side"] = C.q_str(side)
    elif cid == "L1":
        c2 = list(cs)
        c2[198] = shift(cs[198], -EPS, F(0))
        r = C.decide(q(S), c2)
        lw = r["least_positive_wall_clearance"]
        ok = (r["verdict"] == "ACCEPT" and contacts(r) == WC0 - {(199, "right")} and touching(r) == TP0
              and lw["value"] == C.q_str(EPS) and lw["square"] == 199 and lw["wall"] == "right")
        obs = summary(r)
    elif cid == "L2":
        c2 = list(cs)
        c2[183] = shift(cs[183], F(0), -EPS)
        r = C.decide(q(S), c2)
        g = W["g"]
        m, _ = C.margin_a(C.SquareA(c2[158]), C.SquareA(c2[183]))
        ok = (r["verdict"] == "ACCEPT" and contacts(r) == WC0 - {(184, "top")} and touching(r) == TP0 and m == g - EPS)
        obs = summary(r)
        obs["margin_159_184"] = C.q_str(m)
    elif cid == "L3":
        c2 = list(cs)
        for k in range(172, 186):
            c2[k] = shift(cs[k], F(0), -EPS)
        for k in range(186, 199):
            c2[k] = shift(cs[k], -EPS, F(0))
        r = C.decide(q(S), c2)
        ok = (r["verdict"] == "ACCEPT" and contacts(r) == {(46, "left"), (85, "bottom"), (173, "left"), (187, "bottom")}
              and touching(r) == TP0)
        obs = summary(r)
    elif cid in ("L4c", "L4p"):
        g = W["g"]
        d = g if cid == "L4c" else g + EPS
        c2 = list(cs)
        c2[183] = shift(cs[183], F(0), -d)
        r = C.decide(q(S), c2)
        if cid == "L4c":
            ok = (r["verdict"] == "ACCEPT" and touching(r) == TP0 | {(159, 184)} and contacts(r) == WC0 - {(184, "top")})
        else:
            xl = min(fq(x) for x, _ in cs[158])
            ok = (r["verdict"] == "REFUSE" and overl(r, "A") == [(159, 184, C.q_str(-EPS))]
                  and overl(r, "B") == [(159, 184, C.q_str(EPS * (12 - xl)))] and not outside(r))
        obs = summary(r)
    elif cid == "L5":
        res = []
        for i, gq in W["near"]:
            a, b = cs[i - 1], cs[gq - 1]
            sa, sb = C.SquareA(a), C.SquareA(b)
            ca = (sum(p[0] for p in sa.pts) / 4, sum(p[1] for p in sa.pts) / 4)
            cb = (sum(p[0] for p in sb.pts) / 4, sum(p[1] for p in sb.pts) / 4)
            d = (ca[0] - cb[0], ca[1] - cb[1])  # the grid square moves toward the old one
            lo = None
            zero_rate = False
            for ax, ay in sa.axes + sb.axes:
                pa = [ax * x + ay * y for x, y in sa.pts]
                pb = [ax * x + ay * y for x, y in sb.pts]
                rate = ax * d[0] + ay * d[1]
                for a0, b1 in ((min(pb) - max(pa), rate), (min(pa) - max(pb), -rate)):
                    if b1 < 0:
                        lam = -a0 / b1
                        lo = lam if lo is None or lam > lo else lo
                    elif b1 == 0 and a0 >= 0:
                        zero_rate = True
            one = {"pair": [i, gq], "lambda_contact": float(lo), "zero_rate_axis": zero_rate}
            good = not zero_rate
            for dl, cls in ((F(0), "contact"), (EPS, "overlap")):
                bb = shift(b, (lo + dl) * d[0], (lo + dl) * d[1])
                m, _ = C.margin_a(C.SquareA(a), C.SquareA(bb))
                cb_, area = C.pair_b(C.SquareB(a), C.SquareB(bb))
                ca_ = C._class_a(m)
                one[cls] = {"A": ca_, "B": cb_, "margin": float(m), "area": float(area)}
                good = good and ca_ == cls and cb_ == cls
            one["as_stated"] = good
            res.append(one)
        ok = len(res) == 43 and all(x["as_stated"] for x in res)
        obs = {"pairs": len(res), "as_stated": sum(1 for x in res if x["as_stated"]), "detail": res}
    elif cid == "L6":
        S172 = S - 1
        c2 = list(cs[:172]) + [unit(F(k), S172) for k in range(13)] + [unit(S172, F(k)) for k in range(14)]
        r = C.decide(q(S), c2)
        want_t = {(k, k + 1) for k in range(173, 185)} | {(k, k + 1) for k in range(186, 199)} | {(161, 199)}
        want_c = {(46, "left"), (85, "bottom"), (173, "left"), (186, "bottom")} | {(k, "top") for k in range(173, 186)} | {
            (k, "right") for k in range(186, 200)}
        ok = r["verdict"] == "ACCEPT" and touching(r) == want_t and contacts(r) == want_c
        obs = summary(r)
    elif cid in ("R1", "R2", "R3"):
        drop = {"R1": 199, "R2": 173, "R3": 161}[cid]
        keep = [i for i in ids if i != drop]
        r = C.decide(q(S), [cs[i - 1] for i in keep], keep)
        wc = {"R1": WC0 - {(199, "right")}, "R2": WC0 - {(173, "left"), (173, "top")}, "R3": WC0}[cid]
        tp = {"R1": TP0 - {(198, 199)}, "R2": TP0 - {(173, 174)}, "R3": TP0}[cid]
        ok = r["verdict"] == "ACCEPT" and r["n"] == 198 and contacts(r) == wc and touching(r) == tp
        obs = summary(r)
    elif cid == "T1":
        r = C.decide(q(S - 1), cs[:172])
        ok = (r["verdict"] == "ACCEPT" and contacts(r) == {(46, "left"), (85, "bottom"), (161, "right")}
              and not touching(r) and r["least_pair_margin"]["pair"] == [36, 38])
        obs = summary(r)
    else:
        raise KeyError(cid)
    return {"id": cid, "as_stated": bool(ok), "observed": obs, "cpu_seconds": round(time.process_time() - t0, 1)}


def main() -> int:
    # The frozen checker prints exact rationals; under G6 the summed overlap areas exceed
    # CPython's default 4,300-digit int-to-str guard and the first run stopped there
    # (failing loud, deciding nothing). The guard is lifted here, in the driver; the
    # frozen checker is unchanged.
    sys.set_int_max_str_digits(0)
    cand, plan_p, out = sys.argv[1:4]
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    plan = json.load(open(plan_p))
    setup(cand)
    W["base"] = C.decide(q(W["S"]), W["corners"])
    assert W["base"]["verdict"] == "ACCEPT"
    s159 = C.SquareA(W["corners"][158])
    W["g"] = (W["S"] - 1) - max(p[1] for p in s159.pts)
    near = []
    for i in range(172):
        for gq in range(172, 199):
            m, _ = C.margin_a(C.SquareA(W["corners"][i]), C.SquareA(W["corners"][gq]))
            if m < F(1, 10**12):
                near.append((i + 1, gq + 1))
    W["near"] = near
    order = [c["id"] for c in plan["controls"]]
    with mp.get_context("fork").Pool(workers) as pool:
        results = pool.map(ctl, order, chunksize=1)
    by = {r["id"]: r for r in results}
    out_d = {
        "program": "l77_controls.py",
        "program_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
        "checker_sha256": hashlib.sha256(open(os.path.join(HERE, "l77_checker.py"), "rb").read()).hexdigest(),
        "plan_sha256": hashlib.sha256(open(plan_p, "rb").read()).hexdigest(),
        "candidate_sha256": W["w"]["sha256"],
        "verdict": "EVERY_CONTROL_AS_STATED" if all(r["as_stated"] for r in results) else "SOME_CONTROL_NOT_AS_STATED",
        "missed": [r["id"] for r in results if not r["as_stated"]],
        "controls": [{"id": c["id"], "change": c["change"], "expect": c["expect"], **{k: v for k, v in by[c["id"]].items() if k != "id"}}
                     for c in plan["controls"]],
    }
    with open(out, "w") as fh:
        json.dump(out_d, fh, indent=1)
        fh.write("\n")
    print(out_d["verdict"], out_d["missed"])
    for r in results:
        print(r["id"], r["as_stated"], r["cpu_seconds"])
    return 0 if not out_d["missed"] else 1


if __name__ == "__main__":
    sys.exit(main())
