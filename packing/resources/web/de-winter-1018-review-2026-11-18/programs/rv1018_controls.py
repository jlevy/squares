"""The controls of `controls-plan.json`, run on #1018's certificate after the checker's freeze.

Lane r108-1118, blind review of jlevy/squares#1018. Each control changes one thing in an
in-memory copy (or reads the certificate a wrong way) and records what this lane's checks
decided. The must-refuse controls fail on an always-accepting checker; the must-accept
ones (the originals) fail on an always-refusing one. Outcomes are compared with the plan.

- P: premises (rv1018_premises.premises on changed copies of the measure or the claim);
- M: measure identity (rv1018_measure.compare on changed copies);
- R: run coverage (rv1018_runs.check_runs on changed copies of the parsed logs);
- W: readings of the format, at the source's logged poses (r = 0 and every fourth rotated
  direction): the right reading must sit at or above every logged bound, each wrong one
  must fall below at least one or miss the axis bound by more than 1e-6;
- A: the axis decision of the 99/100 copy;
- D: the branch and bound on the 99/100 copy at r = 1, 200 and 399, and at the sampled
  direction of least capture with the threshold 1e-4 above that capture.

Imports nothing from jlevy/squares or the source.

Usage: python -I rv1018_controls.py --measure N108 --base T216 --runs DIR --runs-out RUNS.json
         --sample SAMPLE.json --reviewed-source SHA --scratch DIR --out OUT.json
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1018_axis as ax  # noqa: E402
import rv1018_common as cm  # noqa: E402
import rv1018_decide as dd  # noqa: E402
import rv1018_measure as mm  # noqa: E402
import rv1018_poses as po  # noqa: E402
import rv1018_premises as pr  # noqa: E402
import rv1018_runs as rn  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    for k in ("measure", "base", "runs", "runs-out", "sample", "reviewed-source", "scratch", "out"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--skip-decider", action="store_true")
    args = ap.parse_args()
    t0 = time.process_time()
    meas = cm.read_measure(args.measure)
    base = cm.read_measure(args.base)
    out: dict[str, dict] = {}

    def record(cid: str, expect: str, got: str, detail: object = None) -> None:
        out[cid] = {"expected": expect, "got": got, "as_planned": expect == got, "detail": detail}
        print(cid, expect, got, "OK" if expect == got else "NOT AS PLANNED", flush=True)

    # ---- P: premises
    def prem(m: dict, h: F = pr.STATED["h"], claim: F = pr.STATED["S"]) -> str:
        return pr.premises(m, h, claim, None)["verdict"]

    record("P0", "PREMISES_HOLD", prem(meas))
    m1 = copy.deepcopy(meas)
    m1["total_mass"] = F(108)
    m1["rows"][0] = m1["rows"][0][:4] + (m1["rows"][0][4] + F(1, 100000),)
    record("P1", "PREMISES_FAIL", prem(m1), "total mass 108 (row 0 heavier by 1/100000)")
    m2 = copy.deepcopy(meas)
    m2["B"] = F(12488, 12500)
    record("P2", "PREMISES_FAIL", prem(m2), "B = 12488/12500")
    m3 = copy.deepcopy(meas)
    m3["last"] = 399
    record("P3", "PREMISES_FAIL", prem(m3), "last = 399")
    m4 = copy.deepcopy(meas)
    m4["step"] = F(83, 79000)
    record("P4", "PREMISES_FAIL", prem(m4), "step 83/79000")
    record("P5", "PREMISES_FAIL", prem(meas, h=F(7071, 10000)), "h = 7071/10000")
    record("P6", "PREMISES_FAIL", prem(meas, claim=pr.STATED["S"] + F(1, 10**30)), "S + 1e-30")

    # ---- M: measure identity
    lam = F(1063, 1062)
    record("M0", "SCALED_COPY", mm.compare(base, meas, lam)["verdict"])
    n1 = copy.deepcopy(meas)
    x = n1["rows"][400]
    n1["rows"][400] = (x[0] + F(1, 10**30),) + x[1:]
    record("M1", "NOT_A_SCALED_COPY", mm.compare(base, n1, lam)["verdict"], "row 400 x0 + 1e-30")
    n2 = copy.deepcopy(meas)
    x = n2["rows"][0]
    n2["rows"][0] = x[:4] + (x[4] * (1 + F(1, 10**30)),)
    record("M2", "NOT_A_SCALED_COPY", mm.compare(base, n2, lam)["verdict"], "row 0 mass changed")
    record("M3", "NOT_A_SCALED_COPY", mm.compare(base, meas, F(1064, 1062))["verdict"], "1064/1062")
    n4 = copy.deepcopy(meas)
    n4["rows"] = n4["rows"][::-1]
    n4["raw_strings"] = n4["raw_strings"][::-1]
    c4 = mm.compare(base, n4, lam)
    record("M4", "NOT_A_SCALED_COPY", c4["verdict"], {"multiset": c4["rows_scaled_as_multiset"]})

    # ---- R: run coverage
    files = {p.name: rn.load_lines(p) for p in sorted(Path(args.runs).glob("*"))}
    reviewed = args.reviewed_source
    record("R0", "RUNS_COVER_THE_NET", rn.check_runs(files, meas, reviewed)["verdict"])
    names = sorted(files)

    def mut(cid: str, what: str, fn) -> None:
        f2 = copy.deepcopy(files)
        fn(f2)
        record(cid, "RUNS_DO_NOT_COVER_THE_NET", rn.check_runs(f2, meas, reviewed)["verdict"], what)

    def rec(f2: dict, r: int) -> dict:
        for nm in names:
            for x in f2[nm][:-1]:
                if x.get("r") == r:
                    return x
        raise KeyError(r)

    def drop(f2: dict, r: int) -> None:
        for nm in names:
            f2[nm] = [x for x in f2[nm] if x.get("r") != r]

    mut("R1", "direction 200 deleted", lambda f: drop(f, 200))
    mut("R2", "direction 17 duplicated into the last file", lambda f: f[names[-1]].insert(0, copy.deepcopy(rec(f, 17))))
    mut("R3", "direction 300 refused", lambda f: rec(f, 300).__setitem__("verdict", "refused"))
    mut("R4", "direction 50 bound 0.99999", lambda f: rec(f, 50).__setitem__("min_certified_lower_bound", rn.Dec("0.99999")))
    mut("R5", "input digest changed", lambda f: f[names[3]][-1]["premises"].__setitem__("input_sha256", "0" * 64))
    mut("R6", "B changed to T-216's", lambda f: f[names[5]][-1]["premises"].__setitem__("B", "9977/10000"))
    mut("R7", "crate source changed", lambda f: f[names[0]][-1]["build"].__setitem__("source_sha256", "0" * 64))
    mut("R8", "a summary's node total + 1", lambda f: f[names[7]][-1].__setitem__("nodes", f[names[7]][-1]["nodes"] + 1))
    mut("R9", "standard centre domain", lambda f: f[names[2]][-1]["premises"].__setitem__("centre_domain", "standard"))
    mut("R10", "angle count 201", lambda f: f[names[9]][-1]["premises"].__setitem__("angle_count", 201))
    mut("R11", "direction 7 tree incomplete", lambda f: rec(f, 7).__setitem__("leaves", rec(f, 7)["leaves"] + 1))
    mut("R12", "direction 123 box centre moved past U_r", lambda f: rec(f, 123)["least_bound_box"].__setitem__("x", rn.Dec("10.2")))

    # ---- W: readings at the logged poses
    runs = json.loads(Path(args.runs_out).read_text())
    table = [t for t in runs["directions"] if t["r"] == 0 or t["r"] % 4 == 0]
    rows = meas["rows"]
    right = cm.to_mpq_rects(cm.expand(rows, meas["L"]))
    no_d4 = cm.to_mpq_rects(
        [(a, b, c, d, m, m / ((c - a) * (d - b))) for (a, b, c, d, m) in rows]
    )
    unscaled = cm.to_mpq_rects(cm.expand(base["rows"], meas["L"]))
    swapped_rows = [(a, c, b, d, m) for (a, b, c, d, m) in rows]
    kept = [x for x in swapped_rows if x[0] < x[2] and x[1] < x[3]]
    swapped = cm.to_mpq_rects(cm.expand(kept, meas["L"]))
    readings = {
        "W0": ("right reading", right, meas["step"], meas["B"]),
        "W1": ("rows without their D4 images", no_d4, meas["step"], meas["B"]),
        "W2": ("T-216's rows not rescaled", unscaled, meas["step"], meas["B"]),
        "W3": ("T-216's core B = 9977/10000", right, meas["step"], F(9977, 10000)),
        "W4": ("the standard step 83/40000", right, F(83, 40000), meas["B"]),
        "W5": (f"field order [x0, x1, y0, y1] ({len(rows) - len(kept)} rows degenerate)", swapped, meas["step"], meas["B"]),
    }
    for cid, (what, rq, step, side_b) in readings.items():
        vals = po.pose_values(rq, table, step, side_b, meas["L"], cross_every=0)
        below = [v["r"] for v in vals if not v["at_least_bound"]]
        axis = next(v for v in vals if v["r"] == 0)
        miss = not (0 <= axis["exact_minus_bound"] <= 1e-6)
        got = "REFUSED" if (below or miss) else "ACCEPTED"
        record(
            cid,
            "ACCEPTED" if cid == "W0" else "REFUSED",
            got,
            {"what": what, "poses": len(vals), "below_logged_bound": len(below),
             "axis_exact_minus_bound": axis["exact_minus_bound"]},
        )

    # ---- A: the axis decision of the 99/100 copy
    a99 = ax.decide_axis(meas, F(99, 100))
    record("A1", "REFUSED_EXACT", a99["verdict"], {"least": a99["least_exact_vertex_value"]})

    # ---- D: the branch and bound
    if not args.skip_decider:
        scratch = Path(args.scratch) / f"rv1018-controls-{os.getpid()}"
        exe, _ = dd.build(scratch)
        rects = cm.expand(rows, meas["L"])
        q99 = cm.to_mpq_rects(rects, F(99, 100))
        for cid, r in (("D1", 1), ("D2", 200), ("D3", 399)):
            res = dd.decide_direction(exe, scratch, rects, q99, r, meas["step"], meas["B"], meas["L"],
                                      F(99, 100), F(1), 4e8)
            record(cid, "REFUSED_EXACT", res["verdict"], {"r": r, "nodes": res.get("nodes"),
                                                           "witness": res.get("candidate_exact")})
        sample = json.loads(Path(args.sample).read_text())
        least = sample["least"]
        thr = F(least["least_exact_digits"]) + F(1, 10**4)
        res = dd.decide_direction(exe, scratch, rects, right, least["r"], meas["step"], meas["B"],
                                  meas["L"], F(1), thr, 4e8)
        record("D4", "REFUSED_EXACT", res["verdict"], {"r": least["r"], "threshold": str(thr),
                                                       "nodes": res.get("nodes"),
                                                       "witness": res.get("candidate_exact")})

    planned = all(v["as_planned"] for v in out.values())
    res = {
        "program": "rv1018_controls.py",
        "verdict": "ALL_CONTROLS_AS_PLANNED" if planned else "SOME_CONTROLS_NOT_AS_PLANNED",
        "not_as_planned": [k for k, v in out.items() if not v["as_planned"]],
        "controls": out,
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
    print(res["verdict"], res["not_as_planned"])
    return 0 if planned else 1


if __name__ == "__main__":
    raise SystemExit(main())
