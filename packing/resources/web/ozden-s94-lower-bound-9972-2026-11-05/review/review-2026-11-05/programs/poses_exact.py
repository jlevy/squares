"""Exact captures at named poses: the controls' witnesses and the sampled minima.

For each pose (r, x, y) it computes, in exact rationals, the certificate's capture F
(capture_exact.py for r >= 1, the product formula at r = 0), the 99/100 mutant's
capture 99/100 F, and whether the pose lies in the per-bin domain and in the searched
quadrant. Poses come from:

- the lab's controls: control.json's rational witness at r = 1198 (its stated exact
  capture compared for equality) and native-mutant.jsonl's binary64 witness at 1198
  (its stated exact_coverage compared) and axis argmin at r = 0;
- each sampled direction's lowest box centre in bnb.py's receipts (out/sample/*.json);
- the crate's least-bound box centres for the sampled directions whose lab row keeps
  them (stream A, E, F rows).

Usage: poses_exact.py PACKET_DIR SAMPLE_DIR RECEIPTS_READ_JSON OUT_JSON
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from gmpy2 import mpq

from capture_exact import Evaluator
from xzcommon import direction, frac_str, load_certificate, read_bytes


def axis_capture(ev: Evaluator, x: mpq, y: mpq) -> mpq:
    h = ev.h
    tot = mpq(0)
    for k, d in ev.dens.items():
        ox = max(mpq(0), min(x + h, k[2]) - max(x - h, k[0]))
        oy = max(mpq(0), min(y + h, k[3]) - max(y - h, k[1]))
        if ox and oy:
            tot += d * ox * oy
    return tot


def main() -> int:
    t0 = time.process_time()
    packet = Path(sys.argv[1])
    sample_dir = Path(sys.argv[2])
    rr = json.loads(Path(sys.argv[3]).read_text())
    out = Path(sys.argv[4])
    cert = load_certificate(packet / "source" / "certificate" / "n94-L9972.json.gz")
    ev = Evaluator(cert)
    poses: list[dict[str, object]] = []
    ctrl = json.loads((packet / "source" / "controls" / "control.json").read_text())
    ce = ctrl["exact_counterexample"]
    poses.append({"label": "lab rational witness (control.json)", "r": ce["r"], "x": mpq(ce["x"]), "y": mpq(ce["y"]),
                  "stated_mutant_capture": mpq(ce["capture"])})
    for line in (packet / "source" / "controls" / "native-mutant.jsonl").read_text().splitlines():
        row = json.loads(line)
        if row.get("verdict") == "counterexample-candidate":
            w = row["witness"]
            poses.append({"label": "crate binary64 witness (native-mutant.jsonl)", "r": row["r"],
                          "x": mpq(float(w["exact_pose"][0])), "y": mpq(float(w["exact_pose"][1])),
                          "stated_mutant_capture": mpq(w["exact_coverage"])})
        elif row.get("method") == "axis-vertex-sweep":
            ax, ay = (mpq(v) for v in row["argmin"])
            poses.append({"label": "crate axis argmin (native-mutant.jsonl)", "r": 0, "x": ax, "y": ay})
    for f in sorted(sample_dir.glob("bnb-r*.json")):
        rep = json.loads(f.read_text())
        if rep.get("mass_factor") != "1" or rep.get("lowest_centre_estimate_at") is None:
            continue
        x, y = rep["lowest_centre_estimate_at"]
        poses.append({"label": "lowest box centre of this review's run", "r": rep["r"], "x": mpq(x), "y": mpq(y),
                      "float_estimate": rep["lowest_centre_estimate"]})
    # The crate's least-bound boxes for sampled directions, where the lab's row keeps them.
    sampled = {json.loads(f.read_text())["r"] for f in sample_dir.glob("bnb-r*.json")}
    merged = read_bytes(packet / "source" / "receipts" / "directions.jsonl.gz").decode().splitlines()
    for line in merged:
        row = json.loads(line)
        if row["r"] in sampled and "least_bound_box" in row:
            b = row["least_bound_box"]
            poses.append({"label": "crate least-bound box centre (lab row)", "r": row["r"],
                          "x": mpq(float(b["x"])), "y": mpq(float(b["y"])),
                          "crate_bound": row["min_certified_lower_bound"]})
    results = []
    ok = True
    for p in poses:
        r = int(p["r"])  # type: ignore[arg-type]
        x, y = p["x"], p["y"]
        assert isinstance(x, type(mpq(0))) and isinstance(y, type(mpq(0)))
        F = axis_capture(ev, x, y) if r == 0 else ev.capture(r, x, y)
        mut = mpq(99, 100) * F
        dr = direction(cert, r)
        res = {
            "label": p["label"], "r": r, "x": frac_str(x), "y": frac_str(y),
            "x_float": float(x), "y_float": float(y),
            "capture": float(F), "mutant_capture": float(mut),
            "capture_ge_1": F >= 1, "mutant_below_1": mut < 1,
            "in_per_bin_domain": all(dr.margin <= v <= cert.L - dr.margin for v in (x, y)),
            "in_quadrant": all(cert.L / 2 <= v <= dr.U for v in (x, y)),
            "distance_to_wall_edge_U_r": float(min(dr.U - x, dr.U - y)),
        }
        if "stated_mutant_capture" in p:
            res["stated_mutant_capture_equal"] = p["stated_mutant_capture"] == mut
            ok = ok and bool(res["stated_mutant_capture_equal"])
        for key in ("float_estimate", "crate_bound"):
            if key in p:
                res[key] = p[key]
        ok = ok and bool(res["capture_ge_1"])
        results.append(res)
        print(json.dumps(res), flush=True)
    rep_out = {"poses": results, "all_captures_ge_1_and_stated_values_equal": ok,
               "cpu_seconds": time.process_time() - t0}
    out.write_text(json.dumps(rep_out, indent=1) + "\n")
    print("ALL_HOLD" if ok else "SOME_FAIL", rep_out["cpu_seconds"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
