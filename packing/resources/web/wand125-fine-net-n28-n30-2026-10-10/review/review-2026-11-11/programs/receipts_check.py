"""The source's check2 receipts, run logs and 197/200 controls, read as data and held to
this review's own exact evaluator.

Usage: python -I receipts_check.py --release DIR --premises FILE --out FILE

For each certificate it checks: the run log is complete (indices 0 to 2072 once each,
every one verified at threshold 1 with a bound of at least 1, the axis row's vertices
the product of its event counts, every rotated search tree complete), its totals equal
its summary, the summary's premises equal premises.py's, and the receipt and the
pre-publication receipt agree with the log. Then, in fractions, at every rotated
direction the capture at the centre of the source's least-bound box (it must be at
least that box's certified bound), at the axis argmin of the run and of the control,
and at every control witness (scaled by 197/200 it must equal the source's logged
exact_coverage, and lie below 1). It decides those poses only, and no coverage.
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fnlib as F  # noqa: E402

NAMES = ("mixed_n28_L57425", "mixed_n30_L58925")
FACTOR = Fraction(197, 200)


def load_jsonl(path: Path) -> list[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def in_quadrant(L: Fraction, j: int, x: Fraction, y: Fraction) -> bool:
    u = F.upper_end(j, L)
    return L / 2 <= x <= u and L / 2 <= y <= u


def in_domain(L: Fraction, j: int, x: Fraction, y: Fraction) -> bool:
    u = F.upper_end(j, L)
    return L - u <= x <= u and L - u <= y <= u


def one(name: str, cdir: Path, prem: dict) -> dict:
    fails: list[str] = []
    cert = F.read_candidate(cdir / "candidate.json.gz")
    L, M = cert.L, cert.total_mass
    measure = F.Measure(F.expand(cert.rows, L))
    out: dict = {"certificate": name}

    # --- the run log ---
    run = load_jsonl(cdir / "check2" / "run.jsonl.gz")
    summary = run[-1]
    rows = run[:-1]
    idx = sorted(r["r"] for r in rows)
    if idx != list(range(2073)):
        fails.append("run log indices are not 0..2072 once each")
    by_r = {r["r"]: r for r in rows}
    not_verified = [r["r"] for r in rows if r.get("verdict") != "verified" or r.get("threshold") != "1"]
    below_one = [r["r"] for r in rows if not Fraction(r["min_certified_lower_bound"]) >= 1]
    if not_verified or below_one:
        fails.append("a direction not verified, or a bound below 1")
    ax = by_r[0]
    if ax["method"] != "axis-vertex-sweep" or ax["vertices"] != ax["x_events"] * ax["y_events"]:
        fails.append("axis row")
    rot = [by_r[j] for j in range(1, 2073)]
    if any(r["method"] != "interval-branch-and-bound" for r in rot):
        fails.append("a rotated row is not branch and bound")
    incomplete = [r["r"] for r in rot if r["nodes"] != 2 * r["leaves"] - 1]
    if incomplete:
        fails.append("a rotated search tree is not complete")
    nodes = sum(r["nodes"] for r in rot)
    cpu = sum(r["cpu_seconds"] for r in rows)
    if nodes != summary["nodes"]:
        fails.append("node total differs from the summary")
    if abs(cpu - summary["direction_cpu_seconds"]) > 1e-6 * summary["direction_cpu_seconds"]:
        fails.append("CPU total differs from the summary")
    p = summary["premises"]
    mine = prem["certificates"][name]
    expect = {
        "B": "4999/5000",
        "D": "1/5002",
        "L": mine["claim"]["L"],
        "angle_count": 2073,
        "centre_domain": "per-bin",
        "expanded_points": 0,
        "expanded_rectangles": mine["expansion"]["distinct_after_merge"],
        "expanded_segments": 0,
        "format": "M",
        "input_sha256": mine["sha256"],
        "mass_below_n": "1/100000",
        "mass_exact": mine["claim"]["total_mass"],
        "n": mine["claim"]["n"],
        "source_rectangles": mine["rows"]["count"],
    }
    if p != expect:
        fails.append(f"summary premises differ: {p} vs {expect}")
    if not (summary["status"] == "VERIFIED" and summary["refused_directions"] == []
            and summary["directions"] == 2073 and summary["threshold"] == "1"
            and summary["fault_injected_at_box"] is None):
        fails.append("summary verdict")
    receipt = json.loads((cdir / "check2" / "receipt.json").read_text())
    if receipt["verifier_summary"] != summary:
        fails.append("receipt's verifier_summary is not the log's summary")
    rr = receipt["receipt"]
    if not (receipt["file_sha256"] == mine["sha256"] == rr["file_sha256"] == rr["input_sha256"]
            and receipt["candidate_digest"] == mine["candidate_digest"] == rr["candidate_digest"]
            and rr["directions_verified"] == 2073 and rr["directions_failed"] == 0
            and rr["total_mass"] == mine["claim"]["total_mass"]
            and rr["proof_net"] == {"step": "1/5002", "last": 2072}):
        fails.append("receipt fields")
    pre = json.loads((cdir / "verification" / "prepublication-receipt.json").read_text())
    pre_build = pre.get("build") or {k: pre["verifier"][k] for k in ("source_sha256", "rustc", "target")}
    out["receipt"] = {
        "threads": rr["threads"],
        "started_utc": rr["started_utc"],
        "seconds": rr["seconds"],
        "wall_seconds": summary["wall_seconds"],
        "direction_cpu_seconds": summary["direction_cpu_seconds"],
        "direction_seconds": summary["direction_seconds"],
        "nodes": summary["nodes"],
        "build_source_sha256": summary["build"]["source_sha256"],
        "binary_sha256": rr["verifier"]["binary_sha256"],
        "checked_by": receipt["checked_by"],
        "verifier_text": receipt["verifier"],
        "prepublication": {
            "seconds": pre["seconds"],
            "source_sha256": pre_build["source_sha256"],
            "same_record_as_check2": pre.get("started_utc") == rr["started_utc"] and pre["seconds"] == rr["seconds"],
            "control": pre["control"],
        },
    }
    out["run_log"] = {
        "directions": len(rows),
        "indices_complete": idx == list(range(2073)),
        "all_verified_at_threshold_1": not not_verified and not below_one,
        "rotated_trees_complete": not incomplete,
        "nodes_total": nodes,
        "cpu_total": round(cpu, 3),
        "axis": {k: ax[k] for k in ("x_events", "y_events", "vertices", "argmin", "min_certified_lower_bound")},
    }

    # --- poses: the least-bound box centres ---
    t0 = time.process_time()
    pose_rows = []
    below_bound = []
    outside = []
    for r in rot:
        j = r["r"]
        box = r["least_bound_box"]
        x, y = Fraction(box["x"]), Fraction(box["y"])
        val = F.capture(measure, j, x, y)
        bound = Fraction(r["min_certified_lower_bound"])
        if val < bound or val < 1:
            below_bound.append(j)
        if not in_quadrant(L, j, x, y):
            outside.append(j)
        pose_rows.append((j, float(bound - 1), float(val - 1), box["dx"], box["dy"], Fraction(99, 100) * val < 1))
    pose_cpu = time.process_time() - t0
    if below_bound:
        fails.append(f"exact capture below the certified bound at {below_bound[:10]}")
    by_bound = sorted(pose_rows, key=lambda t: t[1])
    by_exact = sorted(pose_rows, key=lambda t: t[2])
    out["least_bound_centres"] = {
        "poses": len(pose_rows),
        "exact_below_bound_or_1": below_bound,
        "centres_outside_quadrant": len(outside),
        "least_certified_margins": [{"r": t[0], "bound_minus_1": t[1], "exact_minus_1": t[2]} for t in by_bound[:12]],
        "least_exact_margins": [{"r": t[0], "bound_minus_1": t[1], "exact_minus_1": t[2], "dx": t[3], "dy": t[4]}
                                for t in by_exact[:12]],
        "median_exact_minus_1": sorted(t[2] for t in pose_rows)[len(pose_rows) // 2],
        "largest_exact_minus_1": max(t[2] for t in pose_rows),
        # Each centre lies in its quadrant, so where 99/100 of its exact capture is below 1
        # the 99/100 mutant has an exact witness in that direction's domain.
        "directions_with_a_99_100_witness_here": sum(1 for t in pose_rows if t[5]),
        "cpu_seconds": round(pose_cpu, 1),
    }

    # --- the axis argmin of the run ---
    ax_x, ax_y = F.rat(ax["argmin"][0]), F.rat(ax["argmin"][1])
    v0 = F.capture(measure, 0, ax_x, ax_y)
    v0b = F.axis_capture(measure, ax_x, ax_y)
    if v0 != v0b:
        fails.append("the two exact axis evaluations differ")
    lb0 = Fraction(ax["min_certified_lower_bound"])
    out["axis_argmin"] = {
        "argmin": ax["argmin"],
        "in_quadrant": in_quadrant(L, 0, ax_x, ax_y),
        "exact": F.fstr(v0),
        "exact_float": float(v0),
        "logged_bound": ax["min_certified_lower_bound"],
        "exact_minus_bound": float(v0 - lb0),
        "bound_not_above_exact": lb0 <= v0,
    }
    if not lb0 <= v0:
        fails.append("the axis bound is above the exact capture at its argmin")

    # --- the 197/200 control ---
    ctl = load_jsonl(cdir / "check2" / "control-197_200.jsonl.gz")
    csum = ctl[-1]
    crows = {r["r"]: r for r in ctl[:-1]}
    planned = sorted({round(k * 2072 / 31) for k in range(32)})
    if sorted(crows) != planned or csum["refused_directions"] != planned:
        fails.append("control directions are not round(k 2072/31)")
    if not (csum["status"] == "REFUSED" and F.rat(csum["premises"]["mass_exact"]) == FACTOR * M):
        fails.append("control summary")
    wit = []
    mismatch = []
    for j in planned:
        r = crows[j]
        if j == 0:
            cx, cy = F.rat(r["argmin"][0]), F.rat(r["argmin"][1])
            val = F.capture(measure, 0, cx, cy)
            scaled = FACTOR * val
            ok = r["verdict"] == "refused" and scaled < 1 and in_quadrant(L, 0, cx, cy)
            gap = float(scaled - Fraction(r["min_certified_lower_bound"]))
            wit.append({"r": 0, "kind": "axis argmin", "scaled_exact": float(scaled), "unscaled_exact": float(val),
                        "exact_minus_logged_bound": gap, "same_argmin_as_run": r["argmin"] == ax["argmin"]})
        else:
            w = r["witness"]
            cx, cy = Fraction(w["exact_pose"][0]), Fraction(w["exact_pose"][1])
            val = F.capture(measure, j, cx, cy)
            scaled = FACTOR * val
            logged = F.rat(w["exact_coverage"])
            ok = (r["verdict"] == "counterexample-candidate" and w["exact_below_threshold"] is True
                  and scaled == logged and scaled < 1 and in_domain(L, j, cx, cy))
            if scaled != logged:
                mismatch.append(j)
            wit.append({"r": j, "scaled_exact": float(scaled), "unscaled_exact": float(val),
                        "equals_logged_fraction": scaled == logged, "in_quadrant": in_quadrant(L, j, cx, cy)})
        if not ok:
            fails.append(f"control row {j}")
    run_gap = v0 - lb0
    axis_ctl = crows[0]
    ctl_gap = FACTOR * F.capture(measure, 0, F.rat(axis_ctl["argmin"][0]), F.rat(axis_ctl["argmin"][1])) - Fraction(
        axis_ctl["min_certified_lower_bound"])
    out["axis_gap"] = {
        "run_exact_minus_bound": float(run_gap),
        "control_197_200_exact_minus_bound": float(ctl_gap),
        "ratio_control_to_run": float(ctl_gap / run_gap),
        "predicted_99_100_gap_if_it_scales": float(Fraction(99, 100) * run_gap),
    }
    out["control"] = {
        "directions": planned,
        "summary_status": csum["status"],
        "mass_exact": csum["premises"]["mass_exact"],
        "oblique_fractions_equal": 31 - len(mismatch),
        "witnesses": wit,
        "scaled_range": [min(w["scaled_exact"] for w in wit), max(w["scaled_exact"] for w in wit)],
        "unscaled_range": [min(w["unscaled_exact"] for w in wit), max(w["unscaled_exact"] for w in wit)],
    }
    out["failures"] = fails
    out["status"] = "CONSISTENT" if not fails else "INCONSISTENT"
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", required=True)
    ap.add_argument("--premises", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    prem = json.loads(Path(args.premises).read_text())
    t0 = time.process_time()
    res = {}
    for name in NAMES:
        res[name] = one(name, Path(args.release) / name, prem)
        print(name, res[name]["status"], res[name]["failures"][:5])
    status = "ALL_CONSISTENT" if all(r["status"] == "CONSISTENT" for r in res.values()) else "INCONSISTENT"
    F.write_json(args.out, {"program": "receipts_check.py", "status": status,
                            "cpu_seconds": round(time.process_time() - t0, 1), "certificates": res})
    print(status)
    return 0 if status == "ALL_CONSISTENT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
