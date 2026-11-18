"""Self-test of this lane's programs on synthetic data only. It reads no certificate.

Lane r108-1118, blind review of jlevy/squares#1018. Holds the evaluators to each other and
the deciders to refusals they must make:

- the strict reader refuses a duplicate key, a float token, a second gzip member, an extra
  top-level key, an extra `proof_net` key and a nonempty `points`;
- on a random D4-symmetric measure with thin dense strips: the clipping and chord methods
  agree exactly at random rotated poses; clipping at r = 0 equals the overlap product; the
  float capture is within 1e-9 of the exact one;
- the C bound for a box never exceeds the exact capture at its corners, centre and random
  points, at ring sizes 1 and 8; for boxes below 1e-6 it is within 1e-4 of the capture;
- the decider decides a uniform measure whose capture is 1.01 at threshold 1, refuses it
  with an exact witness at threshold 1.01 + 1e-6, and on the random measure refuses a
  threshold just above a capture it attains;
- the axis decider's rigorous least equals the least of all vertex values computed exactly
  on a small measure, and the 99/100 copy is refused;
- the enlargement check accepts its own S and refuses a smaller h and a larger claim;
- the measure comparison accepts a scaled copy and refuses a moved coordinate, a changed mass
  and a wrong factor, and reports a permutation;
- the runs check accepts synthetic runs and refuses each of eleven mutations.

Usage: python -I rv1018_selftest.py --scratch DIR --out OUT.json
"""

from __future__ import annotations

import argparse
import copy
import gzip
import json
import os
import random
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1018_axis as ax  # noqa: E402
import rv1018_common as cm  # noqa: E402
import rv1018_decide as dd  # noqa: E402
import rv1018_measure as mm  # noqa: E402
import rv1018_premises as pr  # noqa: E402
import rv1018_runs as rn  # noqa: E402

L = F(1063, 100)
B = F(12487, 12500)
STEP = F(83, 80000)


def synthetic_rows(seed: int, n_rand: int = 120, n_strips: int = 30) -> list[tuple]:
    rng = random.Random(seed)
    rows = [(F(0), F(0), L, L, F(80))]
    for _ in range(n_rand):
        x0 = F(rng.randint(0, 100000), 10000)
        y0 = F(rng.randint(0, 100000), 10000)
        x1 = min(L, x0 + F(rng.randint(10, 20000), 10000))
        y1 = min(L, y0 + F(rng.randint(10, 20000), 10000))
        rows.append((x0, y0, x1, y1, F(rng.randint(1, 100), 100)))
    for _ in range(n_strips):
        x0 = F(rng.randint(30000, 100000), 10000)
        y0 = F(rng.randint(30000, 100000), 10000)
        if rng.random() < 0.5:
            x1, y1 = min(L, x0 + F(rng.randint(1, 30), 100000)), min(L, y0 + F(rng.randint(5000, 20000), 10000))
        else:
            x1, y1 = min(L, x0 + F(rng.randint(5000, 20000), 10000)), min(L, y0 + F(rng.randint(1, 30), 100000))
        rows.append((x0, y0, x1, y1, F(rng.randint(1, 30), 100)))
    return rows


def write_measure(path: Path, rows, side, b, step, last, n, extra=None) -> None:
    obj = {
        "n": n,
        "L": str(side),
        "B": str(b),
        "proof_net": {"step": str(step), "last": last},
        "total_mass": str(sum(r[4] for r in rows)),
        "points": [],
        "rectangles": [
            {"rectangle": [str(r[0]), str(r[1]), str(r[2]), str(r[3])], "mass": str(r[4])} for r in rows
        ],
    }
    if extra:
        extra(obj)
    path.write_bytes(gzip.compress(json.dumps(obj).encode(), mtime=0))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    t0 = time.process_time()
    scratch = Path(args.scratch) / f"rv1018-selftest-{os.getpid()}"
    scratch.mkdir(parents=True, exist_ok=True)
    checks: dict[str, bool] = {}
    rng = random.Random(1018)

    # ---- the strict reader
    good = scratch / "good.json.gz"
    rows = synthetic_rows(5)
    write_measure(good, rows, L, B, STEP, 400, 108)
    cm.read_measure(good)

    def refused(raw: bytes) -> bool:
        p = scratch / "bad.json.gz"
        p.write_bytes(raw)
        try:
            cm.read_measure(p)
        except (cm.FormatError, ValueError):
            return True
        return False

    text = gzip.decompress(good.read_bytes()).decode()
    checks["reader_refuses_duplicate_key"] = refused(gzip.compress(text.replace('"n": 108', '"n": 108, "n": 108', 1).encode()))
    checks["reader_refuses_float_token"] = refused(gzip.compress(text.replace('"n": 108', '"n": 108.0', 1).encode()))
    checks["reader_refuses_second_member"] = refused(good.read_bytes() + gzip.compress(b"{}"))
    checks["reader_refuses_extra_key"] = refused(gzip.compress(text.replace('"n": 108', '"n": 108, "scaling_factor": "1"', 1).encode()))
    checks["reader_refuses_extra_net_key"] = refused(gzip.compress(text.replace('"last": 400', '"last": 400, "offset": "0"', 1).encode()))
    checks["reader_refuses_points"] = refused(gzip.compress(text.replace('"points": []', '"points": [{"point": ["1", "1"], "mass": "1"}]', 1).encode()))

    # ---- exact methods agree
    rects = cm.expand(rows, L)
    rq = cm.to_mpq_rects(rects)
    fm = cm.FloatMeasure(rects)
    agree = float_ok = True
    for _ in range(40):
        r = rng.randint(1, 400)
        c, s = cm.cos_sin(r * STEP)
        up = cm.domain_upper(r, STEP, L)
        px = F(rng.randint(0, 10**6), 10**6) * (up - L / 2) + L / 2
        py = F(rng.randint(0, 10**6), 10**6) * (up - L / 2) + L / 2
        a = cm.capture_exact_clip(rq, cm._q(c), cm._q(s), cm._q(B / 2), cm._q(px), cm._q(py))
        b = cm.capture_exact_chords(rq, cm._q(c), cm._q(s), cm._q(B / 2), cm._q(px), cm._q(py))
        agree &= a == b
        fv = fm.capture(float(c), float(s), float(B) / 2, float(px), float(py))
        float_ok &= abs(fv - float(a)) < 1e-9
    checks["clip_equals_chords_40_poses"] = agree
    checks["float_capture_within_1e-9"] = float_ok
    axis_ok = True
    for _ in range(15):
        px = F(rng.randint(0, 10**6), 10**6) * (L / 2 - F(1, 2)) + L / 2
        py = F(rng.randint(0, 10**6), 10**6) * (L / 2 - F(1, 2)) + L / 2
        a = cm.capture_exact_axis(rq, cm._q(B / 2), cm._q(px), cm._q(py))
        b = cm.capture_exact_clip(rq, cm._q(F(1)), cm._q(F(0)), cm._q(B / 2), cm._q(px), cm._q(py))
        axis_ok &= a == b
    checks["axis_product_equals_clip_15_poses"] = axis_ok

    # ---- the C bound is a lower bound
    exe, _info = dd.build(scratch)
    sound = True
    tight = True
    tested = 0
    for ring in (1, 8):
        for r in (1, 2, 57, 200, 399, 400):
            hdr, _ = dd.direction_header(r, STEP, B, L, F(1), 1e6, ring)
            recs = dd.rect_records(rects, F(1))
            lo, up = float(L) / 2, float(cm.domain_upper(r, STEP, L))
            boxes = []
            for _ in range(24):
                size = 10 ** rng.uniform(-7, -0.3)
                cx, cy = rng.uniform(lo, up), rng.uniform(lo, up)
                boxes.append((cx - size * rng.random(), cx + size * rng.random(), cy - size * rng.random(), cy + size * rng.random()))
            vals = dd.box_bounds(exe, scratch, hdr, recs, boxes)
            for (xa, xb, ya, yb), (bd, _est) in zip(boxes, vals):
                pts = [(xa, ya), (xb, yb), (xa, yb), (xb, ya), (0.5 * (xa + xb), 0.5 * (ya + yb))]
                pts += [(rng.uniform(xa, xb), rng.uniform(ya, yb)) for _ in range(2)]
                for x, y in pts:
                    ex = cm.capture_exact(rq, r, STEP, B, F(x), F(y))
                    tested += 1
                    if F(bd) > F(ex.numerator, ex.denominator):
                        sound = False
                if max(xb - xa, yb - ya) < 1e-6:
                    exc = cm.capture_exact(rq, r, STEP, B, F(0.5 * (xa + xb)), F(0.5 * (ya + yb)))
                    tight &= float(exc) - bd < 1e-4
    checks["box_bound_never_exceeds_exact"] = sound
    checks["box_bound_tight_below_1e-6"] = tight

    # ---- the decider on measures with known answers
    d_uni = F(101, 100) / (B * B)
    uni = cm.expand([(F(0), F(0), L, L, d_uni * L * L)], L)
    uq = cm.to_mpq_rects(uni)
    res1 = dd.decide_direction(exe, scratch, uni, uq, 57, STEP, B, L, F(1), F(1), 2e7, 8)
    res2 = dd.decide_direction(exe, scratch, uni, uq, 57, STEP, B, L, F(1), F(101, 100) + F(1, 10**6), 2e7, 8)
    checks["decider_decides_uniform_1.01"] = res1["verdict"] == "DECIDED"
    checks["decider_refuses_uniform_above_capture"] = res2["verdict"] == "REFUSED_EXACT"
    r = 200
    c, s = cm.cos_sin(r * STEP)
    lo, up = float(L) / 2, float(cm.domain_upper(r, STEP, L))
    grid = sorted(
        (fm.capture(float(c), float(s), float(B) / 2, lo + (up - lo) * i / 30, lo + (up - lo) * j / 30), i, j)
        for i in range(31)
        for j in range(31)
    )
    _v, i, j = grid[0]
    px, py = F(lo + (up - lo) * i / 30), F(lo + (up - lo) * j / 30)
    attained = cm.capture_exact(rq, r, STEP, B, px, py)
    thr = F(attained.numerator, attained.denominator) + F(1, 10**9)
    res3 = dd.decide_direction(exe, scratch, rects, rq, r, STEP, B, L, F(1), thr, 2e7, 8)
    checks["decider_never_accepts_1e-9_above_an_attained_capture"] = res3["verdict"] != "DECIDED"
    thr6 = F(attained.numerator, attained.denominator) + F(1, 10**6)
    res3b = dd.decide_direction(exe, scratch, rects, rq, r, STEP, B, L, F(1), thr6, 2e7, 8)
    checks["decider_refuses_1e-6_above_an_attained_capture_exactly"] = res3b["verdict"] == "REFUSED_EXACT"
    res4 = dd.decide_direction(exe, scratch, rects, rq, r, STEP, B, L, F(1), F(attained.numerator, attained.denominator) / 2, 2e7, 8)
    checks["decider_decides_half_the_least_capture"] = res4["verdict"] == "DECIDED"

    # ---- the axis decider against brute force on a small measure
    small_rows = synthetic_rows(9, n_rand=4, n_strips=2)
    small = {"rows": small_rows, "L": L, "B": B, "step": STEP, "n": 108, "last": 400}
    res = ax.decide_axis(small, F(1))
    exp = cm.expand(small["rows"], L)
    sq = cm.to_mpq_rects(exp)
    h = B / 2
    xe = {L / 2, L - F(1, 2)}
    for x0, y0, x1, y1, _m, _g in exp:
        for v in (x0 - h, x0 + h, x1 - h, x1 + h, y0 - h, y0 + h, y1 - h, y1 + h):
            if L / 2 <= v <= L - F(1, 2):
                xe.add(v)
    brute = min(cm.capture_exact_axis(sq, cm._q(h), cm._q(x), cm._q(y)) for x in xe for y in xe)
    checks["axis_rigorous_least_matches_brute_force"] = (
        abs(res["rigorous_least_capture"] - float(brute)) < 1e-9
        and F(res["rigorous_least_capture"]) <= F(brute.numerator, brute.denominator)
    )
    if float(brute) > 1:
        thr_small = F(1)
    else:
        thr_small = F(brute.numerator, brute.denominator) / 2
    checks["axis_decides_below_least"] = ax.decide_axis(small, F(1), thr_small)["verdict"] == "AXIS_DIRECTION_DECIDED"
    above = F(brute.numerator, brute.denominator) + F(1, 10**9)
    checks["axis_refuses_above_least"] = ax.decide_axis(small, F(1), above)["verdict"] == "REFUSED_EXACT"

    # ---- the enlargement check
    out, fails = pr.check_enlargement(F(7), F(99, 100), F(1, 1000), F(71, 100), F(0))
    s_own = F(out["S"])
    checks["enlargement_accepts_own_S"] = not pr.check_enlargement(F(7), F(99, 100), F(1, 1000), F(71, 100), s_own)[1]
    checks["enlargement_refuses_small_h"] = bool(pr.check_enlargement(F(7), F(99, 100), F(1, 1000), F(7071, 10000), s_own)[1])
    checks["enlargement_refuses_larger_claim"] = bool(pr.check_enlargement(F(7), F(99, 100), F(1, 1000), F(71, 100), s_own + F(1, 10**30))[1])
    del fails

    # ---- the measure comparison
    lam = F(1063, 1062)
    base = {"n": 108, "L": F(1062, 100), "B": F(9977, 10000), "step": F(83, 40000), "last": 200,
            "total_mass": sum(x[4] for x in rows), "rows": [(a * F(1062, 1063), b_ * F(1062, 1063), c_ * F(1062, 1063), d * F(1062, 1063), m) for (a, b_, c_, d, m) in rows]}
    base["raw_strings"] = [{"mass": str(x[4])} for x in base["rows"]]
    new = {"n": 108, "L": L, "B": B, "step": STEP, "last": 400, "total_mass": base["total_mass"], "rows": rows,
           "raw_strings": [{"mass": str(x[4])} for x in rows]}
    checks["measure_accepts_scaled_copy"] = mm.compare(base, new, lam)["verdict"] == "SCALED_COPY"
    moved = copy.deepcopy(new)
    x = moved["rows"][7]
    moved["rows"][7] = (x[0] + F(1, 10**30),) + x[1:]
    checks["measure_refuses_moved_coordinate"] = mm.compare(base, moved, lam)["verdict"] != "SCALED_COPY"
    heavier = copy.deepcopy(new)
    x = heavier["rows"][3]
    heavier["rows"][3] = x[:4] + (x[4] * (1 + F(1, 10**30)),)
    checks["measure_refuses_changed_mass"] = mm.compare(base, heavier, lam)["verdict"] != "SCALED_COPY"
    checks["measure_refuses_wrong_factor"] = mm.compare(base, new, F(1064, 1062))["verdict"] != "SCALED_COPY"
    perm = copy.deepcopy(new)
    perm["rows"] = perm["rows"][::-1]
    perm["raw_strings"] = perm["raw_strings"][::-1]
    pc = mm.compare(base, perm, lam)
    checks["measure_reports_permutation"] = pc["rows_scaled_as_multiset"] and not pc["rows_scaled_in_file_order"]

    # ---- the runs check on synthetic runs
    small_net = scratch / "smallnet.json.gz"
    write_measure(small_net, rows, L, B, F(83, 8000), 40, 200)
    meas = cm.read_measure(small_net)
    exp_p = rn.expected_premises(meas)
    reviewed = "ab" * 32

    def record(r: int) -> dict:
        upper = cm.domain_upper(r, meas["step"], L)
        cx = rn.Dec(repr(float((L / 2 + upper) / 2)))
        if r == 0:
            return {"argmin": [str(L / 2), str(L / 2)], "cpu_seconds": rn.Dec("1.5"), "method": "axis-vertex-sweep",
                    "min_certified_lower_bound": rn.Dec("1.0001"), "r": 0, "seconds": rn.Dec("2.0"), "threshold": "1",
                    "verdict": "verified", "vertices": 100, "x_events": 10, "y_events": 10}
        return {"audit_every": 1024, "audits": 1, "cpu_seconds": rn.Dec("0.5"), "least_bound_box": {"dx": rn.Dec("0.01"), "dy": rn.Dec("0.01"), "x": cx, "y": cx},
                "leaves": 50, "max_depth": 9, "mean_boundary_rectangles": rn.Dec("10.5"), "method": "interval-branch-and-bound",
                "min_certified_lower_bound": rn.Dec("1.00000002"), "nodes": 99, "r": r, "seconds": rn.Dec("1.0"), "threshold": "1", "verdict": "verified"}

    def summary(recs: list[dict]) -> dict:
        return {"build": {"profile": "release", "source_sha256": reviewed}, "direction_cpu_seconds": rn.Dec(repr(sum(float(x["cpu_seconds"]) for x in recs))),
                "direction_seconds": rn.Dec(repr(sum(float(x["seconds"]) for x in recs))), "directions": len(recs), "fault_injected_at_box": None,
                "kind": "sqverify-fast-summary/v1", "nodes": sum(x.get("nodes", 0) for x in recs), "premises": dict(exp_p),
                "refused_directions": [], "status": "PARTIAL", "threads": 6, "threshold": "1", "wall_seconds": rn.Dec("10.0")}

    files = {}
    for lo_, hi_ in ((0, 20), (21, 40)):
        recs = [record(r) for r in range(lo_, hi_ + 1)]
        files[f"directions_{lo_:03d}_{hi_:03d}.jsonl.gz"] = recs + [summary(recs)]
    base_res = rn.check_runs(files, meas, reviewed)
    checks["runs_accepts_synthetic"] = base_res["verdict"] == "RUNS_COVER_THE_NET"

    def mutated(fn) -> bool:
        f2 = copy.deepcopy(files)
        fn(f2)
        return rn.check_runs(f2, meas, reviewed)["verdict"] != "RUNS_COVER_THE_NET"

    a, b2 = "directions_000_020.jsonl.gz", "directions_021_040.jsonl.gz"
    checks["runs_refuses_missing_direction"] = mutated(lambda f: f[b2].pop(5))
    checks["runs_refuses_duplicate_direction"] = mutated(lambda f: f[b2].insert(0, copy.deepcopy(f[a][3])))
    checks["runs_refuses_refused_verdict"] = mutated(lambda f: f[a][4].__setitem__("verdict", "refused"))
    checks["runs_refuses_bound_below_one"] = mutated(lambda f: f[a][6].__setitem__("min_certified_lower_bound", rn.Dec("0.99999")))
    checks["runs_refuses_other_input"] = mutated(lambda f: f[b2][-1]["premises"].__setitem__("input_sha256", "0" * 64))
    checks["runs_refuses_other_B"] = mutated(lambda f: f[a][-1]["premises"].__setitem__("B", "9977/10000"))
    checks["runs_refuses_unreviewed_source"] = mutated(lambda f: f[a][-1]["build"].__setitem__("source_sha256", "cd" * 32))
    checks["runs_refuses_node_total"] = mutated(lambda f: f[a][-1].__setitem__("nodes", f[a][-1]["nodes"] + 1))
    checks["runs_refuses_standard_domain"] = mutated(lambda f: f[a][-1]["premises"].__setitem__("centre_domain", "standard"))
    checks["runs_refuses_angle_count"] = mutated(lambda f: f[b2][-1]["premises"].__setitem__("angle_count", 201))
    checks["runs_refuses_incomplete_tree"] = mutated(lambda f: f[a][8].__setitem__("leaves", 51))

    passed = all(checks.values())
    res = {
        "program": "rv1018_selftest.py",
        "verdict": "PASS" if passed else "FAIL",
        "failed": [k for k, v in checks.items() if not v],
        "checks": checks,
        "box_bound_points_tested": tested,
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
    print(res["verdict"], res["failed"], "points", tested)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
