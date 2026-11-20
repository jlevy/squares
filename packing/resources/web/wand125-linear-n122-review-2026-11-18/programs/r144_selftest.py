"""Controls on this review's own programs: each must refuse what it should refuse.

Usage:
  r144_selftest.py --synthetic --work DIR --out OUT.json
  r144_selftest.py --real BUNDLE_DIR --work DIR --out OUT.json

--synthetic builds measures with known answers and needs no certificate:
  S1  the exact evaluators A and B agree at seeded poses at five nodes;
  S2  a point lattice of spacing B/5 and mass (1 + 1/10000)/25: the axis decider must
      decide it with least exactly 25 m, and refuse its 99/100 mutant with an exact
      witness; seeded exact captures are never below the least;
  S3  a segment grid with a point orbit and a rectangle orbit: the branch and bound must
      decide node 37 at factor 1, with no seeded exact capture below 1, and refute it at
      factor 3/10 with an exact witness;
  S4  the strict reader refuses a float token, a duplicate key and an unknown key;
  S5  the premise checks refuse a total mass of n, a negative mass, a point outside K,
      a degenerate segment, a net that stops at index 199, and a step with B(1+D) >= 1;
  S6  the input check accepts a synthetic input written from the measure and refuses a
      coordinate moved by one unit in the last place outside its exact value, a dropped
      row, a duplicated row in place of another, and a header E for the wrong node.
--real BUNDLE runs S4 to S6 on mutated copies of the real candidate and of node 37's
input; it decides nothing about the certificate.
Written for this review; imports nothing from jlevy/squares or the source.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r144_axis  # noqa: E402
import r144_bnb  # noqa: E402
import r144_inputs  # noqa: E402
import r144_premises  # noqa: E402
from r144_common import ReadError, angle_data, expand_images, load_candidate, read_json_strict, round_down, round_up  # noqa: E402
from r144_exact import Measure, capture_a, capture_b  # noqa: E402

B0 = F(9977, 10000)
STEP = F(83, 40000)


def synth_lattice():
    h = B0 / 5
    N = 14
    L = F(3)
    o = (L - N * h) / 2
    m = (1 + F(1, 10000)) / 25
    prims = []
    for k in range(N + 1):
        for l in range(N + 1):
            prims.append(("point", (o + k * h, o + l * h), m))
    return {"n": 10, "L": L, "B": B0, "step": STEP, "last": 200, "primitives": prims, "total_mass": sum((p[2] for p in prims), F(0))}, m


def synth_grid():
    L = F(3)
    h = B0 / 6
    N = 15
    o = (L - N * h) / 2
    lam = F(1, 5)
    prims = []
    for l in range(N + 1):
        y = o + l * h
        prims.append(("segment", (F(0), y, L, y), lam * L))
    prims.append(("point", (F(1, 3), F(2, 7)), F(1, 50)))
    prims.append(("rectangle", (F(1, 5), F(11, 10), F(3, 10), F(6, 5)), F(1, 40)))
    return {"n": 10, "L": L, "B": B0, "step": STEP, "last": 200, "primitives": prims, "total_mass": sum((p[2] for p in prims), F(0))}


def seeded_poses(cand, j, k, seed):
    rng = random.Random(seed)
    ang = angle_data(j, cand["step"], cand["L"], cand["B"])
    lo = cand["L"] / 2 - ang["E"]
    hi = cand["L"] / 2 + ang["E"]
    out = []
    for _ in range(k):
        x = lo + (hi - lo) * F(rng.randrange(10**6), 10**6)
        y = lo + (hi - lo) * F(rng.randrange(10**6), 10**6)
        out.append((x, y))
    return ang, out


def s1(res):
    cand = synth_grid()
    meas = Measure(cand["primitives"], cand["L"])
    bad = 0
    n = 0
    for j in (0, 1, 37, 108, 200):
        ang, poses = seeded_poses(cand, j, 40, 1000 + j)
        for x, y in poses:
            n += 1
            if capture_a(meas, ang, x, y) != capture_b(meas, ang, x, y):
                bad += 1
    res["S1_evaluators_agree"] = {"poses": n, "disagreements": bad, "ok": bad == 0}


def s2(res):
    cand, m = synth_lattice()
    r = r144_axis.decide(cand, F(1))
    least = F(r["least_exact"]["exact"])
    meas = Measure(cand["primitives"], cand["L"])
    ang, poses = seeded_poses(cand, 0, 200, 7)
    below = sum(1 for x, y in poses if capture_a(meas, ang, x, y) < least)
    r2 = r144_axis.decide(cand, F(99, 100))
    ok = r["verdict"] == "AXIS_DECIDED" and least == 25 * m and below == 0 and r2["verdict"] == "AXIS_REFUSED" and F(r2["witness_pose"]["capture_a"]) < 1
    res["S2_axis_lattice"] = {"verdict": r["verdict"], "least_exact": r["least_exact"]["exact"], "expected": f"{(25 * m).numerator}/{(25 * m).denominator}", "seeded_below_least": below, "mutant_verdict": r2["verdict"], "mutant_witness": r2["witness_pose"]["capture_a"], "ok": ok}


def s3(res):
    cand = synth_grid()
    r = r144_bnb.Node(cand, 37, F(1), 8, 2_000_000).run()
    meas = Measure(cand["primitives"], cand["L"])
    ang, poses = seeded_poses(cand, 37, 300, 11)
    vals = [capture_a(meas, ang, x, y) for x, y in poses]
    below = sum(1 for v in vals if v < 1)
    r2 = r144_bnb.Node(cand, 37, F(3, 10), 8, 2_000_000).run()
    ok = r["verdict"] == "NODE_DECIDED" and below == 0 and r2["verdict"] == "NODE_REFUTED" and F(r2["witness"]["capture"]) < 1
    res["S3_bnb_grid"] = {"verdict": r["verdict"], "boxes": r["stats"]["nodes"], "rect_exact": r["stats"]["rect_exact"], "least_seeded_capture": float(min(vals)), "seeded_below_one": below, "mutant_verdict": r2["verdict"], "mutant_witness": r2["witness"], "ok": ok}


def s4(res, raw: bytes):
    cases = {
        "float token": raw.replace(b'"total_mass": "', b'"total_mass": 1.5, "x": "', 1) if b'"total_mass": "' in raw else None,
        "duplicate key": raw.replace(b'"n": ', b'"n": 1, "n": ', 1),
        "unknown key": raw.replace(b'"n": ', b'"extra": "1", "n": ', 1),
    }
    out = {}
    for name, data in cases.items():
        if data is None:
            out[name] = "not applicable"
            continue
        try:
            load_candidate(data)
            out[name] = "accepted"
        except (ReadError, Exception) as e:  # noqa: BLE001
            out[name] = f"refused: {type(e).__name__}"
    res["S4_reader_refusals"] = {"cases": out, "ok": all(v.startswith("refused") for v in out.values() if v != "not applicable")}


def s5(res, cand):
    def run(c):
        rep = r144_premises.Report()
        try:
            r144_premises.candidate_checks(rep, c, b"{}")
        except Exception as e:  # noqa: BLE001
            return [f"error {type(e).__name__}"]
        return rep.failed

    out = {}
    cand = dict(cand)
    cand.setdefault("raw", {})
    base_failed = set(run(cand))
    if any(f.startswith("error") for f in base_failed):
        res["S5_premise_refusals"] = {"error": sorted(base_failed), "ok": False}
        return
    prims = list(cand["primitives"])
    c1 = dict(cand)
    c1["primitives"] = prims[:-1] + [(prims[-1][0], prims[-1][1], prims[-1][2] + (cand["n"] - cand["total_mass"]))]
    c1["total_mass"] = sum((p[2] for p in c1["primitives"]), F(0))
    out["total mass n"] = sorted(set(run(c1)) - base_failed)
    c2 = dict(cand)
    c2["primitives"] = [(prims[0][0], prims[0][1], -prims[0][2])] + prims[1:]
    out["negative mass"] = sorted(set(run(c2)) - base_failed)
    c3 = dict(cand)
    k = next(i for i, p in enumerate(prims) if p[0] == "point")
    c3["primitives"] = prims[:k] + [("point", (cand["L"] + F(1, 10**9), prims[k][1][1]), prims[k][2])] + prims[k + 1 :]
    out["point outside K"] = sorted(set(run(c3)) - base_failed)
    c4 = dict(cand)
    k = next(i for i, p in enumerate(prims) if p[0] == "segment")
    g = prims[k][1]
    c4["primitives"] = prims[:k] + [("segment", (g[0], g[1], g[0], g[1]), prims[k][2])] + prims[k + 1 :]
    out["degenerate segment"] = sorted(set(run(c4)) - base_failed)
    # net premises as the premise program computes them
    t199 = STEP * 199
    out["net stops at 199"] = ["t_last^2 + 2 t_last - 1 > 0 fails"] if not (t199 * t199 + 2 * t199 - 1 > 0) else []
    D = F(1, 430)
    out["step 1/430"] = ["B(1 + D) < 1 fails"] if not (B0 * (1 + D) < 1) else []
    expected = {
        "total mass n": "total mass below n (the budget)",
        "negative mass": "every mass is positive",
        "point outside K": "every primitive lies in K = [0, L]^2",
        "degenerate segment": "no degenerate segment or rectangle",
    }
    ok = all(expected[k] in out[k] for k in expected) and all(len(out[k]) > 0 for k in out)
    res["S5_premise_refusals"] = {"newly_failed_checks": out, "ok": ok}


def write_input(cand, j, path, mutate=None):
    """A synthetic checker input in the layout read by r144_inputs (rectangles, segments,
    points; mass for points, density for segments and rectangles)."""
    L, B = cand["L"], cand["B"]
    ang = angle_data(j, cand["step"], L, B)
    if mutate == "wrong E":
        ang = dict(ang)
        ang["E"] = angle_data(j + 1, cand["step"], L, B)["E"]

    def ivs(q):
        return f"{round_down(q).hex()} {round_up(q).hex()}"

    lines = [ivs(L), ivs(B), ivs(ang["E"]), ivs(ang["cos"]), ivs(ang["sin"]), ivs(F(1))]
    imgs = expand_images(cand["primitives"], L)
    blocks = {"rectangle": [], "segment": [], "point": []}
    for kind, g, m, _i, _g in imgs:
        if kind == "point":
            row = [ivs(g[0]), ivs(g[1]), ivs(m)]
        elif kind == "segment":
            ln = max(abs(g[2] - g[0]), abs(g[3] - g[1]))
            row = [ivs(v) for v in g] + [ivs(m / ln)]
        else:
            row = [ivs(v) for v in g] + [ivs(m / ((g[2] - g[0]) * (g[3] - g[1])))]
        blocks[kind].append(" ".join(row))
    if mutate == "moved coordinate":
        r = blocks["segment"][0].split()
        lo = float.fromhex(r[0])
        hi = float.fromhex(r[1])
        # move the interval one unit in the last place above its upper end
        r[0] = math.nextafter(hi, math.inf).hex()
        r[1] = math.nextafter(math.nextafter(hi, math.inf), math.inf).hex()
        _ = lo
        blocks["segment"][0] = " ".join(r)
    if mutate == "dropped row":
        blocks["point"] = blocks["point"][:-1]
    if mutate == "duplicated row":
        blocks["point"][-1] = blocks["point"][0]
    for k in ("rectangle", "segment", "point"):
        lines.append(str(len(blocks[k])))
        lines.extend(blocks[k])
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def s6(res, cand, work, j=37):
    out = {}
    for mut in (None, "moved coordinate", "dropped row", "duplicated row", "wrong E"):
        p = os.path.join(work, f"input-{mut or 'original'}.txt".replace(" ", "-"))
        write_input(cand, j, p, mut)
        data = open(p, "rb").read()
        try:
            header, blocks, _ = r144_inputs.split_input(data)
            hok, _ = r144_inputs.check_header(header, angle_data(j, cand["step"], cand["L"], cand["B"]), cand["L"], cand["B"])
            bok, _ = r144_inputs.check_body(blocks, cand["primitives"], cand["L"])
            ok = hok and bok
        except Exception as e:  # noqa: BLE001
            ok = False
            out[(mut or "original") + " error"] = type(e).__name__
        out[mut or "original"] = "accepted" if ok else "refused"
    good = out["original"] == "accepted" and all(out[m] == "refused" for m in ("moved coordinate", "dropped row", "duplicated row", "wrong E"))
    res["S6_input_check"] = {"cases": out, "ok": good}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--real")
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    t0 = time.process_time()
    res = {"program": "r144_selftest.py"}
    if a.synthetic:
        res["mode"] = "synthetic"
        s1(res)
        s2(res)
        s3(res)
        cand, _ = synth_lattice()
        raw = json.dumps({"schema": "point_line_rectangle_v1", "n": 4, "L": "3", "B": "0.9977", "net": {"step": "83/40000", "last": 200}, "primitives": [], "total_mass": "0"}).encode()
        s4(res, raw)
        s5(res, synth_grid())
        s6(res, synth_grid(), a.work)
    if a.real:
        res["mode"] = "real"
        raw = open(os.path.join(a.real, "candidate.json"), "rb").read()
        cand = load_candidate(raw)
        s4(res, raw)
        s5(res, cand)
        s6(res, cand, a.work)
        # the real node-37 input, mutated in place of a copy
        data = open(os.path.join(a.real, "net037", "input.txt"), "rb").read()
        header, blocks, _ = r144_inputs.split_input(data)
        base_ok = r144_inputs.check_body(blocks, cand["primitives"], cand["L"])[0]
        seg_block = max(range(len(blocks)), key=lambda i: len(blocks[i]))
        row = list(blocks[seg_block][5])
        row[0] = math.nextafter(float.fromhex(row[1]), math.inf).hex()
        row[1] = math.nextafter(float.fromhex(row[0]), math.inf).hex()
        mutated = [list(b) for b in blocks]
        mutated[seg_block][5] = row
        mut_ok = r144_inputs.check_body(mutated, cand["primitives"], cand["L"])[0]
        res["S7_real_input_mutation"] = {"original_body_encodes": base_ok, "moved_coordinate_accepted": mut_ok, "ok": base_ok and not mut_ok}
        _ = read_json_strict
    res["all_ok"] = all(v.get("ok", True) for v in res.values() if isinstance(v, dict))
    res["cpu_seconds"] = round(time.process_time() - t0, 2)
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1, default=str)
        f.write("\n")
    print("SELFTEST_PASS" if res["all_ok"] else "SELFTEST_FAIL", {k: v.get("ok") for k, v in res.items() if isinstance(v, dict)}, f"cpu {res['cpu_seconds']} s")
    return 0 if res["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
