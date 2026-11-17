"""Lane L180: run the stated controls by both methods, and compare each with the plan.

Written for the blind stage 4 review of issue #996 as a clean-room implementation,
after ``controls-plan.json`` was written and hashed. It imports nothing from this
repository or the source, and reuses no code of any earlier review.

Usage: l180_controls.py JSON TWIN PLAN PLAN_FACTS CHECK_RECEIPT OUT

Every whole-file control writes the modified certificate as JSON text, reads it back
through the reader, and decides it by both methods over every square, wall and pair;
the twin controls write the modified twin as YAML text and read it back.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction as F
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l180_axes as A  # noqa: E402
import l180_clip as B  # noqa: E402
import l180_decide as D  # noqa: E402
import l180_geom as G  # noqa: E402
import l180_reader as R  # noqa: E402
from gmpy2 import mpq  # noqa: E402
from l180_decide import fstr  # noqa: E402
from l180_reader import Pose, Reading, TwinReading  # noqa: E402

TINY = F(1, 10**30)
WALLS = ("left", "bottom", "right", "top")


def reread(r: Reading, poses: list[Pose], side: F) -> Reading:
    mod = Reading(n=len(poses), side=side, side_text=fstr(side), format_text=r.format_text, poses=tuple(poses))
    return R.read_json_text(R.write_json_text(mod))


def decide_reading(back: Reading) -> D.Decision:
    return D.decide(back.n, back.side, back.poses, [R.json_corners(p) for p in back.poses])


def observe(d: D.Decision) -> dict[str, Any]:
    obs: dict[str, Any] = {"verdict": d.verdict}
    obs["not_unit_a"] = [k + 1 for k, ok in enumerate(d.unit_a) if not ok]
    obs["not_unit_b"] = [k + 1 for k, ok in enumerate(d.unit_b) if not ok]
    if not d.margins:
        return obs
    for name, cls_a, cls_b in (("overlapping", A.OVERLAP, B.OVERLAP), ("touching", A.TOUCH, B.TOUCH)):
        la = sorted([list(k) for k, c in d.class_a.items() if c == cls_a])
        lb = sorted([list(k) for k, c in d.class_b.items() if c == cls_b])
        obs[name] = la if la == lb else {"A": la, "B": lb}
    ca = {w: sorted(i for (i, ww), c in d.clear.items() if ww == w and c == 0) for w in WALLS}
    cb = {w: sorted(i for (i, ww), c in d.wall_b.items() if ww == w and c == B.TOUCH) for w in WALLS}
    obs["contacts"] = ca if ca == cb else {"A": ca, "B": cb}
    xa = {w: sorted(i for (i, ww), c in d.clear.items() if ww == w and c < 0) for w in WALLS}
    xb = {w: sorted(i for (i, ww), c in d.wall_b.items() if ww == w and c == B.CROSS) for w in WALLS}
    obs["crossings"] = xa if xa == xb else {"A": xa, "B": xb}
    obs["margin_sha256"] = D.margin_digest(d)
    obs["clearance_sha256"] = D.clearance_digest(d)
    obs["classes_agree"] = all(d.class_a[k] == d.class_b[k] for k in d.margins) and all(d.wall_a[k] == d.wall_b[k] for k in d.clear)
    obs["method_b_both_orders_agree"] = all(d.both_orders.values())
    least = min(d.margins, key=lambda k: d.margins[k])
    obs["least_margin"] = {"pair": list(least), "approx": D.sci(d.margins[least])}
    return obs


def compare(exp: dict[str, Any], obs: dict[str, Any], d: D.Decision | None) -> tuple[bool, list[str]]:
    bad: list[str] = []
    for key, want in exp.items():
        if key == "pair_values":
            assert d is not None
            for pk, vals in want.items():
                i, j = (int(x) for x in pk.split())
                if "margin" in vals and fstr(d.margins[(i, j)]) != vals["margin"]:
                    bad.append(f"margin {pk} {fstr(d.margins[(i, j)])}")
                if "area_b" in vals and str(d.area_b[(i, j)]) != vals["area_b"]:
                    bad.append(f"area {pk} {d.area_b[(i, j)]}")
        elif key == "clearances":
            assert d is not None
            for ck, val in want.items():
                i, w = ck.split()
                if fstr(d.clear[(int(i), w)]) != val:
                    bad.append(f"clearance {ck}")
        elif key == "inside_area":
            assert d is not None
            for i, val in want.items():
                if str(d.inside_area[int(i) - 1]) != val:
                    bad.append(f"inside area {i} {d.inside_area[int(i) - 1]}")
        elif obs.get(key) != want:
            bad.append(f"{key}: observed {str(obs.get(key))[:200]}")
    if d is not None and d.margins and not (obs.get("classes_agree") and obs.get("method_b_both_orders_agree")):
        bad.append("methods disagree")
    return not bad, bad


def run_whole(r: Reading, poses: list[Pose], side: F, exp: dict[str, Any]) -> dict[str, Any]:
    back = reread(r, poses, side)
    d = decide_reading(back)
    obs = observe(d)
    ok, bad = compare(exp, obs, d)
    if "overlapping" in obs and isinstance(obs["overlapping"], list) and len(obs["overlapping"]) > 12:
        obs["overlapping"] = {"count": len(obs["overlapping"]), "first": obs["overlapping"][:6]}
    return {"as_stated": ok, "differences": bad, "observed": obs}


def run_reader(text: bytes, exp: dict[str, Any]) -> dict[str, Any]:
    try:
        R.read_json_text(text)
    except R.ReadError as exc:
        ok = exp["verdict"] == "READER_REFUSES" and exp["reason_contains"] in str(exc)
        return {"as_stated": ok, "observed": {"verdict": "READER_REFUSES", "reason": str(exc)}}
    return {"as_stated": False, "observed": {"verdict": "READ"}}


def run_twin(r: Reading, t: TwinReading, exp: dict[str, Any]) -> dict[str, Any]:
    back = R.read_twin_text(R.write_twin_text(t))
    cmp_ = R.compare_twin(r, back)
    obs: dict[str, Any] = {"twin_agree": cmp_["agree"], "twin_problems": cmp_["problems"], "listings": cmp_["listings"]}
    d = None
    if "verdict" in exp:
        d = D.decide(r.n, r.side, r.poses, list(back.corners))
        o2 = observe(d)
        obs["verdict"] = d.verdict
        obs["not_unit_a"], obs["not_unit_b"] = o2["not_unit_a"], o2["not_unit_b"]
        obs["sense_b"] = {"counterclockwise": d.sense_b.count(1), "clockwise": d.sense_b.count(-1)}
        if d.margins:
            obs["margin_sha256"], obs["clearance_sha256"] = o2["margin_sha256"], o2["clearance_sha256"]
    bad = [f"{k}: observed {str(obs.get(k))[:200]}" for k, v in exp.items() if obs.get(k) != v]
    return {"as_stated": not bad, "differences": bad, "observed": obs}


def main(argv: list[str]) -> int:
    if len(argv) != 7:
        print(__doc__)
        return 2
    jpath, tpath, ppath, fpath, cpath, out = argv[1:]
    t0 = time.process_time()
    with open(jpath, "rb") as fh:
        jtext = fh.read()
    r = R.read_json_text(jtext)
    tw = R.read_twin(tpath)
    with open(ppath, encoding="utf-8") as fh:
        plan = json.load(fh)
    with open(fpath, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(cpath, encoding="utf-8") as fh:
        json.load(fh)
    C = plan["controls"]
    poses = list(r.poses)
    S = r.side
    n = r.n
    res: dict[str, Any] = {}

    def ex(cid: str) -> dict[str, Any]:
        return C[cid]["expect"]

    res["G1"] = run_whole(r, [*poses[:-1], poses[0]], S, ex("G1"))
    p1 = poses[0]
    res["G2"] = run_whole(r, [Pose(p1.x + S, p1.y, p1.c, p1.s), *poses[1:]], S, ex("G2"))
    obj = json.loads(jtext)
    obj["squares"].pop()
    res["G3"] = run_reader(json.dumps(obj).encode(), ex("G3"))
    obj = json.loads(jtext)
    obj["side"] = f"{2 * S.numerator}/{2 * S.denominator}"
    res["G4"] = run_reader(json.dumps(obj).encode(), ex("G4"))
    k5 = plan["g5"]["square"] - 1
    for cid, t in (("G5a", TINY), ("G5b", -TINY)):
        mod = list(poses)
        mod[k5] = G.rotated(poses[k5], t)
        res[cid] = run_whole(r, mod, S, ex(cid))
    res["G6"] = run_whole(r, [Pose(p.x, p.y, p.c, -p.s) for p in poses], S, ex("G6"))
    c0 = tw.corners[0]
    moved = ((c0[0][0] + TINY, c0[0][1]), c0[1], c0[2], c0[3])
    res["G7a"] = run_twin(r, TwinReading(**{**tw.__dict__, "corners": (moved, *tw.corners[1:])}), ex("G7a"))
    s2 = S + F(4, S.denominator)
    res["G7b"] = run_twin(r, TwinReading(**{**tw.__dict__, "side": s2, "side_text": fstr(s2)}), ex("G7b"))
    res["G7c"] = run_twin(r, TwinReading(**{**tw.__dict__, "corners": tuple(tuple(reversed(cs)) for cs in tw.corners)}), ex("G7c"))
    res["G7d"] = run_twin(r, TwinReading(**{**tw.__dict__, "corners": tuple(cs[1:] + cs[:1] for cs in tw.corners)}), ex("G7d"))
    res["G8"] = run_whole(r, [Pose(p.y, p.x, p.s, p.c) for p in poses], S, ex("G8"))
    res["G9"] = run_whole(r, [Pose(p.x, p.y, -p.s, p.c) for p in poses], S, ex("G9"))
    res["G10"] = run_whole(r, [Pose(p.x, p.y, -p.c, -p.s) for p in poses], S, ex("G10"))
    res["G11"] = run_whole(r, [Pose(S - p.y, p.x, -p.s, p.c) for p in poses], S, ex("G11"))
    res["G12"] = run_whole(r, [Pose(p1.x, p1.y, p1.c, p1.s + TINY), *poses[1:]], S, ex("G12"))
    least_rt = F(facts["S1"]["least_positive_right_top"]["exact"])
    for cid, side in (
        ("S1a", S - F(1, S.denominator)),
        ("S1b", S - TINY),
        ("S1c", S - least_rt),
        ("S1d", S - least_rt - TINY),
        ("S1e", F(facts["S1"]["claim"])),
        ("S1f", F(facts["S1"]["floor12"])),
    ):
        res[cid] = run_whole(r, poses, side, ex(cid))
    s4 = plan["s4"]
    mv, to = s4["moving"] - 1, s4["toward"] - 1
    for cid, target in (("S4c", F(0)), ("S4p", -TINY)):
        mod = list(poses)
        mod[mv], _ = G.close_pair(poses[to], poses[mv], target)
        res[cid] = run_whole(r, mod, S, ex(cid))

    # S5: pair-level, every pair.
    ints = [A.to_ints(p.x, p.y, p.c, p.s) for p in poses]
    lines: list[str] = []
    s5_ok = 0
    s5_bad: list[str] = []
    for i in range(n):
        bi = B.ccw(B.to_mpq(R.json_corners(poses[i])))
        for j in range(i + 1, n):
            good = True
            times = []
            for target, want_b in ((F(0), B.TOUCH), (-TINY, B.OVERLAP)):
                q, t = G.close_pair(poses[i], poses[j], target)
                times.append(t)
                ma, _ = A.pair_margin(ints[i], A.to_ints(q.x, q.y, q.c, q.s))
                mg = G.margin(poses[i], q)
                cb, _, both = B.pair(bi, B.ccw(B.to_mpq(R.json_corners(q))))
                if not (ma == target and mg == target and cb == want_b and both):
                    good = False
                    s5_bad.append(f"{i + 1} {j + 1} target {target}: A {D.sci(ma)}, B {cb}")
            lines.append(f"{i + 1} {j + 1} {fstr(times[0])} {fstr(times[1])}\n")
            s5_ok += good
    digest = hashlib.sha256("".join(lines).encode()).hexdigest()
    e5 = ex("S5")
    res["S5"] = {
        "as_stated": s5_ok == e5["pairs"] and digest == e5["closing_times_sha256"],
        "observed": {"pairs_as_stated": s5_ok, "closing_times_sha256": digest, "first_failures": s5_bad[:10]},
    }

    # S6: square-level, every square to its nearest wall.
    s6_ok = 0
    s6_bad: list[str] = []
    counts: dict[str, int] = dict.fromkeys(WALLS, 0)
    sq = mpq(S.numerator, S.denominator)
    for i, p in enumerate(poses):
        cl = G.clearances(p, S)
        w = min(WALLS, key=lambda ww: (cl[ww], WALLS.index(ww)))
        counts[w] += 1
        good = True
        for by, want_c, want_b, inside in ((cl[w], F(0), B.TOUCH, True), (cl[w] + TINY, -TINY, B.CROSS, False)):
            q = G.move_to_wall(p, w, by)
            ca = A.wall_clearances(A.to_ints(q.x, q.y, q.c, q.s), S)[w]
            qb = B.ccw(B.to_mpq(R.json_corners(q)))
            cb = B.walls(qb, sq)[w][0]
            ia = B.area_inside(qb, sq) == 1
            if not (ca == want_c and cb == want_b and ia == inside):
                good = False
                s6_bad.append(f"{i + 1} {w}: A {D.sci(ca)}, B {cb}, inside {ia}")
        s6_ok += good
    e6 = ex("S6")
    res["S6"] = {
        "as_stated": s6_ok == e6["squares"] and counts == e6["nearest_wall_counts"],
        "observed": {"squares_as_stated": s6_ok, "nearest_wall_counts": counts, "first_failures": s6_bad[:10]},
    }

    every = all(v["as_stated"] for v in res.values())
    receipt = {
        "program": "l180_controls.py",
        "lane": "L180",
        "plan_sha256": hashlib.sha256(open(ppath, "rb").read()).hexdigest(),
        "verdict": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
        "as_stated": sum(1 for v in res.values() if v["as_stated"]),
        "controls": len(res),
        "results": {cid: {"stated": C[cid]["stated"], **res[cid]} for cid in C},
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1)
        fh.write("\n")
    print(f"{receipt['verdict']}: {receipt['as_stated']} of {receipt['controls']}")
    for cid, v in res.items():
        if not v["as_stated"]:
            print("  NOT AS STATED", cid, v.get("differences") or v["observed"])
    return 0 if every else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
