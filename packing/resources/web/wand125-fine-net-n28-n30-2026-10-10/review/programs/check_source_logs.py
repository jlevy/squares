"""The source's check2 receipts, run log, 197/200 control and pre-publication
receipt of one certificate, read against the candidate (review think-4ul6).

Nothing of the crate, the repository's tools or the source is imported or run.

Checks:
- run log: one row per direction 0 .. last, each `verified` at threshold "1", the
  axis by the vertex sweep and the rest by branch and bound, no witness; the
  summary's sums, premises, build, status; the embedded copies in receipt.json;
- receipt.json, control.json and the pre-publication receipt: every field against
  the candidate, the log and each other;
- control log: the 32 directions are the shipped script's round(i (N - 1) / 31);
  every row refused; the summary's mass is 197/200 of the candidate's; whether the
  mutant's input digest is reproduced by rebuilding the mutant file from the
  candidate; every oblique witness re-evaluated exactly (pose in the per-bin
  domain, capture of the 197/200 measure equal to the crate's rational, below 1);
- the tightest leaves of the run: at the K directions with the least certified
  bounds, the exact capture at the leaf box's centre and four corners, which must
  be at least that bound and at least 1.

Usage: python3 -I check_source_logs.py CERT_DIR CHECK_CANDIDATE_JSON [--leaves K] [--out FILE]
CHECK_CANDIDATE_JSON is check_candidate.py's receipt (for the semantic digest
and the distinct-image count).
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fine_net_exact as fx  # noqa: E402


def jsonl(path):
    with gzip.open(path, "rt") as fh:
        return [json.loads(line) for line in fh if line.startswith("{")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert_dir", type=Path)
    ap.add_argument("premises", type=Path)
    ap.add_argument("--leaves", type=int, default=12)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    t0 = time.time()
    problems: list[str] = []

    def need(ok, what):
        if not ok:
            problems.append(what)
        return bool(ok)

    prem = json.loads(args.premises.read_text())
    cand = fx.load_candidate(args.cert_dir / "candidate.json.gz")
    n, L, B, D, last = cand.n, cand.L, cand.B, cand.D, cand.last
    N = last + 1
    M = sum((m for _, m in cand.rows), F(0))
    sha = cand.file_sha256
    digest = prem["custody"]["semantic_digest"]
    out: dict = {"certificate": prem["certificate"], "candidate_sha256": sha, "semantic_digest": digest}

    # ---------------- run log
    run = jsonl(args.cert_dir / "check2" / "run.jsonl.gz")
    dirs = [r for r in run if "r" in r]
    summ = [r for r in run if r.get("kind") == "sqverify-fast-summary/v1"]
    idx = [r["r"] for r in dirs]
    obl = [r for r in dirs if r["r"] != 0]
    ax = [r for r in dirs if r["r"] == 0]
    s = summ[0] if len(summ) == 1 else {}
    p = s.get("premises", {})
    least = min(obl, key=lambda r: r["min_certified_lower_bound"])
    tight = sorted(obl, key=lambda r: r["min_certified_lower_bound"])[: args.leaves]
    out["run"] = {
        "lines": len(run),
        "direction_rows": len(dirs),
        "indices_exactly_0_to_last_once": sorted(idx) == list(range(N)),
        "all_verified": all(r["verdict"] == "verified" for r in dirs),
        "threshold_1_everywhere": all(r["threshold"] == "1" for r in dirs),
        "axis_by_vertex_sweep": len(ax) == 1 and ax[0]["method"] == "axis-vertex-sweep",
        "obliques_by_branch_and_bound": all(r["method"] == "interval-branch-and-bound" for r in obl),
        "no_witness_in_any_row": not any("witness" in r for r in dirs),
        "every_bound_above_1": all(r["min_certified_lower_bound"] > 1 for r in dirs),
        "every_oblique_audited": all(r.get("audits", 0) >= 1 and r.get("audit_every") == 1024 for r in obl),
        "least_oblique_bound": least["min_certified_lower_bound"],
        "least_oblique_direction": least["r"],
        "axis_bound": ax[0]["min_certified_lower_bound"] if ax else None,
        "axis_events": [ax[0]["x_events"], ax[0]["y_events"]] if ax else None,
        "max_depth": max(r["max_depth"] for r in obl),
        "nodes_sum": sum(r["nodes"] for r in obl),
        "leaves_sum": sum(r["leaves"] for r in obl),
        "most_nodes": max(obl, key=lambda r: r["nodes"])["nodes"],
        "most_nodes_direction": max(obl, key=lambda r: r["nodes"])["r"],
        "fewest_nodes": min(obl, key=lambda r: r["nodes"])["nodes"],
        "cpu_sum": sum(r["cpu_seconds"] for r in dirs),
        "seconds_sum": sum(r["seconds"] for r in dirs),
        "tightest_directions": [[r["r"], r["min_certified_lower_bound"]] for r in tight],
    }
    R = out["run"]
    for k in ("indices_exactly_0_to_last_once", "all_verified", "threshold_1_everywhere", "axis_by_vertex_sweep",
              "obliques_by_branch_and_bound", "no_witness_in_any_row", "every_bound_above_1", "every_oblique_audited"):
        need(R[k], "run " + k)
    exp_premises = {
        "B": str(B), "D": str(D), "L": str(L), "angle_count": N, "centre_domain": "per-bin",
        "expanded_points": 0, "expanded_rectangles": prem["measure"]["distinct_images"], "expanded_segments": 0,
        "format": "M", "input_sha256": sha, "mass_below_n": str(n - M), "mass_exact": str(M), "n": n,
        "source_rectangles": len(cand.rows),
    }
    out["summary"] = {
        "one_summary_last": len(summ) == 1 and run[-1] is summ[0],
        "status": s.get("status"),
        "directions": s.get("directions"),
        "refused_directions": s.get("refused_directions"),
        "threshold": s.get("threshold"),
        "fault_injected_at_box": s.get("fault_injected_at_box", "absent"),
        "premises_equal_recomputed": p == exp_premises,
        "premises_differences": {k: [p.get(k), v] for k, v in exp_premises.items() if p.get(k) != v},
        "premises_keys_extra": sorted(set(p) - set(exp_premises)),
        "nodes_equal_sum": s.get("nodes") == R["nodes_sum"],
        "cpu_equal_sum": abs(s.get("direction_cpu_seconds", -1) - R["cpu_sum"]) < 1e-6 * max(1, R["cpu_sum"]),
        "seconds_equal_sum": abs(s.get("direction_seconds", -1) - R["seconds_sum"]) < 1e-6 * max(1, R["seconds_sum"]),
        "build": s.get("build"),
        "threads": s.get("threads"),
        "wall_seconds": s.get("wall_seconds"),
        "nodes": s.get("nodes"),
        "direction_cpu_seconds": s.get("direction_cpu_seconds"),
    }
    S_ = out["summary"]
    need(S_["one_summary_last"], "summary line")
    need(S_["status"] == "VERIFIED" and S_["directions"] == N and S_["refused_directions"] == [], "summary status")
    need(S_["threshold"] == "1" and S_["fault_injected_at_box"] is None, "summary threshold/fault")
    need(S_["premises_equal_recomputed"], "summary premises")
    need(S_["nodes_equal_sum"] and S_["cpu_equal_sum"] and S_["seconds_equal_sum"], "summary sums")

    # ---------------- receipt.json, control.json, pre-publication receipt
    rc = json.loads((args.cert_dir / "check2" / "receipt.json").read_text())
    inner = rc.get("receipt", {})
    ctl = json.loads((args.cert_dir / "check2" / "control.json").read_text())
    pre = json.loads((args.cert_dir / "verification" / "prepublication-receipt.json").read_text())
    tries = inner.get("control", {}).get("tries", [])
    out["receipt"] = {
        "outer": {k: rc.get(k) for k in ("status", "directions", "failed", "candidate", "verifier", "checked_by", "copied")},
        "outer_digests_match": rc.get("candidate_digest") == digest and rc.get("file_sha256") == sha,
        "verifier_summary_equals_log_summary": rc.get("verifier_summary") == s,
        "inner_schema": inner.get("schema"),
        "inner_fields_match": (
            inner.get("n") == n and F(inner.get("L")) == L and F(inner.get("B")) == B
            and inner.get("proof_net") == cand.doc["proof_net"] and F(inner.get("total_mass")) == M
            and inner.get("directions_expected") == N and inner.get("directions_checked") == N
            and inner.get("directions_verified") == N and inner.get("directions_failed") == 0
            and inner.get("candidate_digest") == digest and inner.get("file_sha256") == sha
            and inner.get("input_sha256") == sha and inner.get("status") == "VERIFIED" and inner.get("exit") == 0
            and inner.get("verdict") == "PASS"
        ),
        "inner_verifier": inner.get("verifier"),
        "inner_source_equals_summary_build": (inner.get("verifier") or {}).get("source_sha256") == (s.get("build") or {}).get("source_sha256"),
        "inner_threads_started_seconds": [inner.get("threads"), inner.get("started_utc"), inner.get("seconds")],
        "inner_control": inner.get("control"),
        "control_try_is_197_200_refused_32": len(tries) == 1 and tries[0].get("factor") == "197/200"
        and tries[0].get("status") == "REFUSED" and tries[0].get("exit") == 1 and tries[0].get("directions") == 32
        and tries[0].get("refused") == 32,
        "control_json_equals_inner_control_plus_source": {k: v for k, v in ctl.items() if k != "source_sha256"} == inner.get("control")
        and ctl.get("source_sha256") == (s.get("build") or {}).get("source_sha256"),
    }
    Rc = out["receipt"]
    need(Rc["outer_digests_match"] and Rc["verifier_summary_equals_log_summary"], "receipt embeds")
    need(Rc["inner_fields_match"] and Rc["inner_source_equals_summary_build"], "inner receipt")
    need(Rc["control_try_is_197_200_refused_32"] and Rc["control_json_equals_inner_control_plus_source"], "receipt control")
    pre_shape = "fine-net-check2-receipt/v1" if pre.get("schema") == "fine-net-check2-receipt/v1" else ("build" if "build" in pre else "other")
    out["prepublication"] = {
        "shape": pre_shape,
        "identical_to_inner_receipt": pre == inner,
        "digests_match": pre.get("candidate_digest") == digest and pre.get("file_sha256") == sha and pre.get("input_sha256") == sha,
        "status_verdict": [pre.get("status"), pre.get("exit"), pre.get("verdict")],
        "directions": [pre.get("directions_expected"), pre.get("directions_checked"), pre.get("directions_verified")],
        "seconds": pre.get("seconds"),
        "build_or_verifier": pre.get("build") or pre.get("verifier"),
        "control": pre.get("control"),
        "fields_absent_from_this_shape": sorted(set(inner) - set(pre)),
    }
    need(out["prepublication"]["digests_match"], "prepublication digests")
    need(out["prepublication"]["status_verdict"] == ["VERIFIED", 0, "PASS"] and out["prepublication"]["directions"] == [N, N, N], "prepublication outcome")

    # ---------------- control log
    con = jsonl(args.cert_dir / "check2" / "control-197_200.jsonl.gz")
    cdirs = [r for r in con if "r" in r]
    csum = [r for r in con if r.get("kind") == "sqverify-fast-summary/v1"]
    cs = csum[0] if len(csum) == 1 else {}
    cp = cs.get("premises", {})
    want = [round(i * (N - 1) / 31) for i in range(32)]
    factor = F(197, 200)
    Mm = M * factor
    out["control_log"] = {
        "direction_rows": len(cdirs),
        "directions_are_round_i_last_over_31": sorted(r["r"] for r in cdirs) == sorted(want),
        "every_row_refused": all(r["verdict"] in ("counterexample-candidate", "refused") for r in cdirs),
        "verdicts": sorted({r["verdict"] for r in cdirs}),
        "summary_status": cs.get("status"),
        "summary_refused_directions_equal": cs.get("refused_directions") == sorted(want),
        "summary_mass_is_197_200_of_candidate": cp.get("mass_exact") == str(Mm) and cp.get("mass_below_n") == str(n - Mm),
        "summary_other_premises_as_run": {k: v for k, v in cp.items() if k not in ("mass_exact", "mass_below_n", "input_sha256")}
        == {k: v for k, v in p.items() if k not in ("mass_exact", "mass_below_n", "input_sha256")},
        "summary_build_as_run": cs.get("build") == s.get("build"),
        "mutant_input_sha256": cp.get("input_sha256"),
    }
    # Can the mutant file be rebuilt from the candidate?  The shipped
    # fine_net_check.sh writes json.dump(d) with masses str(Fraction * 985/1000).
    rebuilt = {}
    for label, dump in (
        ("json.dump default", lambda d: json.dumps(d)),
        ("indent=1", lambda d: json.dumps(d, indent=1)),
        ("indent=2", lambda d: json.dumps(d, indent=2)),
        ("compact", lambda d: json.dumps(d, separators=(",", ":"))),
        ("default + newline", lambda d: json.dumps(d) + "\n"),
        ("indent=2 + newline", lambda d: json.dumps(d, indent=2) + "\n"),
        ("indent=1 + newline", lambda d: json.dumps(d, indent=1) + "\n"),
    ):
        d = json.loads(cand.raw)
        for row in d["rectangles"]:
            row["mass"] = str(F(row["mass"]) * factor)
        for row in d.get("points", []):
            row["mass"] = str(F(row["mass"]) * factor)
        d["total_mass"] = str(sum(F(x["mass"]) for x in d["rectangles"] + d.get("points", [])))
        rebuilt[label] = hashlib.sha256(dump(d).encode()).hexdigest()
    match = [k for k, v in rebuilt.items() if v == cp.get("input_sha256")]
    out["control_log"]["mutant_rebuilt_digest_matches"] = match
    Cl = out["control_log"]
    for k in ("directions_are_round_i_last_over_31", "every_row_refused", "summary_refused_directions_equal",
              "summary_mass_is_197_200_of_candidate", "summary_other_premises_as_run", "summary_build_as_run"):
        need(Cl[k], "control " + k)
    need(Cl["summary_status"] == "REFUSED", "control status")

    ims = fx.images(cand)
    h = cand.h
    wit = []
    for r in sorted(cdirs, key=lambda r: r["r"]):
        if r["r"] == 0:
            continue
        w = r.get("witness") or {}
        px, py = (F(v) for v in w["exact_pose"])
        lo, hi = fx.per_bin_domain(cand, r["r"])
        c, sn = fx.direction(D, r["r"])
        e = fx.capture(ims, px, py, c, sn, h) * factor
        crate = F(w["exact_coverage"])
        wit.append({
            "r": r["r"],
            "verdict": r["verdict"],
            "pose": w["exact_pose"],
            "pose_is_box_centre": w["exact_pose"] == [w["x"], w["y"]],
            "in_per_bin_domain": lo <= px <= hi and lo <= py <= hi,
            "in_quadrant": L / 2 <= px <= hi and L / 2 <= py <= hi,
            "exact_197_200": float(e),
            "equals_crate_rational": e == crate,
            "below_1": e < 1,
            "flag_consistent": bool(w.get("exact_below_threshold")) == (e < 1),
            "centre_lower_bound_le_exact": F(w["centre_lower_bound"]) <= e,
            "original_capture": float(e / factor),
        })
    out["control_witnesses"] = {
        "oblique_witnesses": len(wit),
        "all_in_per_bin_domain": all(x["in_per_bin_domain"] for x in wit),
        "all_in_quadrant": all(x["in_quadrant"] for x in wit),
        "all_equal_crate_rational": all(x["equals_crate_rational"] for x in wit),
        "all_below_1": all(x["below_1"] for x in wit),
        "all_flags_consistent": all(x["flag_consistent"] for x in wit),
        "all_centre_bounds_le_exact": all(x["centre_lower_bound_le_exact"] for x in wit),
        "all_poses_are_box_centres": all(x["pose_is_box_centre"] for x in wit),
        "least_197_200": min(x["exact_197_200"] for x in wit),
        "greatest_197_200": max(x["exact_197_200"] for x in wit),
        "least_original": min(x["original_capture"] for x in wit),
        "rows": wit,
    }
    Cw = out["control_witnesses"]
    for k in ("all_in_per_bin_domain", "all_equal_crate_rational", "all_below_1", "all_flags_consistent", "all_centre_bounds_le_exact"):
        need(Cw[k], "witness " + k)

    # ---------------- tightest leaves
    leaves = []
    for r in tight:
        box = r["least_bound_box"]
        x0, y0, dx, dy = (F(box[k]) for k in ("x", "y", "dx", "dy"))
        c, sn = fx.direction(D, r["r"])
        bound = F(r["min_certified_lower_bound"])
        vals = []
        for qx, qy in ((x0, y0), (x0 - dx, y0 - dy), (x0 + dx, y0 - dy), (x0 - dx, y0 + dy), (x0 + dx, y0 + dy)):
            vals.append(fx.capture(ims, qx, qy, c, sn, h))
        lo, hi = fx.per_bin_domain(cand, r["r"])
        leaves.append({
            "r": r["r"],
            "bound": r["min_certified_lower_bound"],
            "box": box,
            "centre_in_quadrant": L / 2 <= x0 <= hi and L / 2 <= y0 <= hi,
            "exact_centre": float(vals[0]),
            "exact_least_of_five": float(min(vals)),
            "all_five_ge_bound": all(v >= bound for v in vals),
            "all_five_ge_1": all(v >= 1 for v in vals),
        })
    out["tightest_leaves"] = {
        "directions": len(leaves),
        "all_five_ge_bound": all(x["all_five_ge_bound"] for x in leaves),
        "all_five_ge_1": all(x["all_five_ge_1"] for x in leaves),
        "all_centres_in_quadrant": all(x["centre_in_quadrant"] for x in leaves),
        "least_exact": min(x["exact_least_of_five"] for x in leaves),
        "rows": leaves,
    }
    need(out["tightest_leaves"]["all_five_ge_bound"] and out["tightest_leaves"]["all_five_ge_1"], "leaves")

    ru = resource.getrusage(resource.RUSAGE_SELF)
    out["cpu_seconds"] = ru.ru_utime + ru.ru_stime
    out["wall_seconds"] = time.time() - t0
    out["problems"] = problems
    out["status"] = "SOURCE_RECORDS_CONSISTENT" if not problems else "INCONSISTENT"
    text = json.dumps(out, indent=1)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
