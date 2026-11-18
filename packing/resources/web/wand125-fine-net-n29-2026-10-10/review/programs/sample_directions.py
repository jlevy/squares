"""Run this repository's reviewed sqverify-fast (crate source d97758bb...) at
sampled directions of mixed_n29_L582, compare each row with the source's run log,
and evaluate the leaves and witnesses exactly with fine_net_exact (review
think-1lri).  The binary is the one program here the review did not write; this
driver only runs it and reads its output.  Adapted from the n = 28 and n = 30
review's driver after re-reading it.

- Original: each sampled direction must be `verified`, with the source's node
  count, leaves, depth, least certified bound, least-bound box and method; the
  exact capture at that box's centre and four corners must be at least the bound
  and 1.  The summary's premises are read as the 6 October checklist's item 3 asks.
- Mutant (--mutant-factor, e.g. 99/100): every mass scaled, written to a scratch
  file; each sampled direction must be refused, an oblique witness's exact capture
  of the scaled measure must be below 1, in the per-bin domain and equal to the
  crate's rational, and the axis row's exact capture at its vertex below 1 and
  above its certified bound.

Usage: python3 -I sample_directions.py BINARY CERT_DIR N L --directions a,b,c
       [--mutant-directions d,e] [--mutant-factor 99/100] [--threads 2]
       [--scratch DIR] [--out FILE]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import resource
import subprocess
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fine_net_exact as fx  # noqa: E402


def run_binary(binary, candidate, n, L, dirs, threads):
    cmd = [str(binary), "--candidate", str(candidate), "--n", str(n), "--side", str(L),
           "--directions", ",".join(map(str, dirs)), "--threads", str(threads), "--confirm"]
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    rows = [json.loads(line) for line in r.stdout.splitlines() if line.startswith("{")]
    return r.returncode, rows, time.time() - t, " ".join(cmd[1:]), r.stderr[-2000:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("binary", type=Path)
    ap.add_argument("cert_dir", type=Path)
    ap.add_argument("n", type=int)
    ap.add_argument("L")
    ap.add_argument("--directions", required=True)
    ap.add_argument("--mutant-directions", default="")
    ap.add_argument("--mutant-factor", default="99/100")
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--scratch", type=Path, default=Path("."))
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    t0 = time.time()
    problems: list[str] = []
    cand_path = args.cert_dir / "candidate.json.gz"
    cand = fx.load_candidate(cand_path)
    ims = fx.images(cand)
    h, D, L = cand.h, cand.D, cand.L
    with gzip.open(args.cert_dir / "check2" / "run.jsonl.gz", "rt") as fh:
        source = {r["r"]: r for r in (json.loads(x) for x in fh if x.startswith("{")) if "r" in r}
    dirs = [int(x) for x in args.directions.split(",") if x]
    code, rows, wall, cmd, err = run_binary(args.binary, cand_path, args.n, args.L, dirs, args.threads)
    by = {r["r"]: r for r in rows if "r" in r}
    summ = next((r for r in rows if r.get("kind") == "sqverify-fast-summary/v1"), {})
    out: dict = {"binary_sha256": hashlib.sha256(args.binary.read_bytes()).hexdigest(), "binary_command": cmd,
                 "exit": code, "wall_seconds": wall, "summary": summ, "directions": []}
    keys = ("verdict", "nodes", "leaves", "max_depth", "min_certified_lower_bound", "least_bound_box", "method",
            "mean_boundary_rectangles", "audits", "audit_every")
    for r in dirs:
        mine, theirs = by.get(r, {}), source[r]
        same = {k: mine.get(k) == theirs.get(k) for k in keys}
        rec = {"r": r, "verdict": mine.get("verdict"), "nodes": mine.get("nodes"), "bound": mine.get("min_certified_lower_bound"),
               "cpu_seconds": mine.get("cpu_seconds"), "source_cpu_seconds": theirs.get("cpu_seconds"), "equal_to_source": same}
        if not all(same.values()):
            problems.append(f"direction {r} differs from the source: {[k for k, v in same.items() if not v]}")
        box = mine.get("least_bound_box")
        if box:
            c, s = fx.direction(D, r)
            x0, y0, dx, dy = (F(box[k]) for k in ("x", "y", "dx", "dy"))
            vals = [fx.capture(ims, qx, qy, c, s, h) for qx, qy in
                    ((x0, y0), (x0 - dx, y0 - dy), (x0 + dx, y0 - dy), (x0 - dx, y0 + dy), (x0 + dx, y0 + dy))]
            bound = F(mine["min_certified_lower_bound"])
            rec["exact_centre"] = float(vals[0])
            rec["exact_least_of_five"] = float(min(vals))
            rec["five_ge_bound_and_1"] = all(v >= bound and v >= 1 for v in vals)
            if not rec["five_ge_bound_and_1"]:
                problems.append(f"direction {r}: exact capture below the bound or 1")
        if r == 0 and mine.get("argmin"):
            ax, ay = (F(v) for v in mine["argmin"])
            e = fx.axis_capture(ims, ax, ay, h)
            rec["axis_exact_at_argmin"] = float(e)
            rec["axis_bound_le_exact"] = F(mine["min_certified_lower_bound"]) <= e
        out["directions"].append(rec)
    p = summ.get("premises", {})
    N = cand.last + 1
    out["checklist_item_3"] = {
        "format_M": p.get("format") == "M",
        "centre_domain_per_bin": p.get("centre_domain") == "per-bin",
        "net_origin_proof_net": p.get("net_origin") == "proof_net",
        "D_equals_step": p.get("D") is not None and F(p["D"]) == D,
        "angle_count_equals_last_plus_1": p.get("angle_count") == N,
        "net_last_tangent_equals_(N-1)D": p.get("net_last_tangent") is not None and F(p["net_last_tangent"]) == (N - 1) * D,
        "B_equals_file": p.get("B") is not None and F(p["B"]) == cand.B,
        "shrink_bound_equals_B(1+D)": p.get("shrink_bound") is not None and F(p["shrink_bound"]) == cand.B * (1 + D),
        "mass_exact_n_minus_1e-5_below_n": p.get("mass_exact") is not None and F(p["mass_exact"]) == cand.n - F(1, 100000) < cand.n,
        "expanded_points_segments_0": p.get("expanded_points") == 0 and p.get("expanded_segments") == 0,
        "fault_injected_null": summ.get("fault_injected_at_box", "absent") is None,
        "source_sha256_is_d97758bb": (summ.get("build") or {}).get("source_sha256", "").startswith("d97758bb"),
        "profile_release_rustc_1.98.0": (summ.get("build") or {}).get("profile") == "release"
        and "1.98.0" in (summ.get("build") or {}).get("rustc", ""),
        # The binary reads the retained .gz, so it reports that file's digest
        # (checklist item 4: candidate_sha256 is the retained .gz file's).
        "input_sha256_is_retained_gz": p.get("input_sha256") == hashlib.sha256(cand_path.read_bytes()).hexdigest(),
    }
    for k, v in out["checklist_item_3"].items():
        if v is False:
            problems.append("item 3 " + k)

    mdirs = [int(x) for x in args.mutant_directions.split(",") if x]
    if mdirs:
        factor = F(args.mutant_factor)
        mpath = args.scratch / f"mutant-{args.n}-{factor.numerator}_{factor.denominator}.json"
        mpath.write_text(fx.scaled_copy_text(cand, factor))
        mcode, mrows, mwall, mcmd, merr = run_binary(args.binary, mpath, args.n, args.L, mdirs, args.threads)
        mims = fx.images(cand, factor)
        recs = []
        for r in (x for x in mrows if "r" in x):
            w = r.get("witness") or {}
            rec = {"r": r["r"], "verdict": r["verdict"], "cpu_seconds": r.get("cpu_seconds")}
            if r["r"] == 0:
                ax, ay = (F(v) for v in r["argmin"])
                e = fx.axis_capture(mims, ax, ay, h)
                rec.update({"argmin": r["argmin"], "exact": float(e), "below_1": e < 1, "bound": r["min_certified_lower_bound"],
                            "bound_le_exact": F(r["min_certified_lower_bound"]) <= e, "gap": float(e - F(r["min_certified_lower_bound"]))})
                ok = r["verdict"] != "verified" and rec["below_1"] and rec["bound_le_exact"]
            else:
                px, py = (F(v) for v in w["exact_pose"])
                lo, hi = fx.per_bin_domain(cand, r["r"])
                c, s = fx.direction(D, r["r"])
                e = fx.capture(mims, px, py, c, s, h)
                rec.update({"pose": w["exact_pose"], "exact": float(e), "below_1": e < 1, "in_domain": lo <= px <= hi and lo <= py <= hi,
                            "equals_crate": e == F(w["exact_coverage"])})
                ok = r["verdict"] != "verified" and rec["below_1"] and rec["in_domain"] and rec["equals_crate"]
            if not ok:
                problems.append(f"mutant direction {r['r']}")
            recs.append(rec)
        out["mutant"] = {"factor": str(factor), "exit": mcode, "command": mcmd, "wall_seconds": mwall, "rows": recs,
                         "summary_status": next((x.get("status") for x in mrows if x.get("kind")), None)}
        mpath.unlink()
    ru = resource.getrusage(resource.RUSAGE_SELF)
    rc = resource.getrusage(resource.RUSAGE_CHILDREN)
    out["cpu_seconds_python"] = ru.ru_utime + ru.ru_stime
    out["cpu_seconds_binary"] = rc.ru_utime + rc.ru_stime
    out["wall_seconds_total"] = time.time() - t0
    out["problems"] = problems
    out["status"] = "SAMPLE_AGREES" if not problems else "SAMPLE_DIFFERS"
    text = json.dumps(out, indent=1)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
