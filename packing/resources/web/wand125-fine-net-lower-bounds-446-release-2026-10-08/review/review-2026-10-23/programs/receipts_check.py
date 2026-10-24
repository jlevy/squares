"""Read the source's retained run and control logs as data and check them exactly.

For each certificate this checks, without running any program of the source:

- the run log: 2,073 direction rows, indices 0..2072 once each, every one ``verified`` at
  threshold 1 with a certified lower bound of at least 1, the axis sweep at index 0 and
  interval branch and bound elsewhere, each rotated tree complete (nodes = 2 leaves - 1),
  and a summary whose totals, premises, input digest and empty refusal list agree;
- at every rotated direction, the exact capture of the core centred at the least-bound
  box's centre (this review's own geometry): at least 1, and at least the source's
  certified bound for that box (which the bound must not exceed);
- at index 0, the exact capture at the sweep's reported argmin against its bound;
- the 197/200 control log: its 32 directions, each refusal's witness pose in the per-bin
  domain, and its exact mutant capture recomputed here and compared with the source's
  rational ``exact_coverage`` as equal fractions;
- the check2 and pre-publication receipts: status, counts and digests.

    python3 -I receipts_check.py --packet PACKET --out outputs/receipts-check.json
"""

from __future__ import annotations

import argparse
import gzip
import json
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from t233lib import (  # noqa: E402
    CERTS,
    cos_sin,
    domain_upper,
    exact_capture,
    expand,
    loose_json,
    read_candidate,
)

FACTOR = Fraction(197, 200)


def lines(path: Path) -> list[dict]:
    with gzip.open(path, "rb") as fh:
        raw = fh.read()
    return [loose_json(line) for line in raw.splitlines() if line.strip()]


def in_domain(cand, r: int, x: Fraction, y: Fraction, slack: Fraction) -> bool:
    lo = cand.L / 2
    hi = domain_upper(cand.L, cand.step, r)
    return lo - slack <= x <= hi + slack and lo - slack <= y <= hi + slack


def check_run(cand, meas, rows: list[dict]) -> dict:
    problems: list[str] = []
    summary = [r for r in rows if r.get("kind") == "sqverify-fast-summary/v1"]
    dirs = [r for r in rows if "r" in r]
    if len(summary) != 1 or rows[-1] is not summary[0]:
        problems.append("summary is not exactly the last line")
    if sorted(r["r"] for r in dirs) != list(range(cand.last + 1)):
        problems.append("direction indices are not exactly 0..last once each")
    s = summary[0] if summary else {}
    if s.get("status") != "VERIFIED" or s.get("refused_directions") != []:
        problems.append("summary is not VERIFIED with no refusal")
    if s.get("directions") != cand.last + 1 or s.get("fault_injected_at_box") is not None:
        problems.append("summary direction count or fault field")
    if s.get("threshold") != "1":
        problems.append("summary threshold is not 1")
    if s.get("premises", {}).get("input_sha256") != cand.raw_sha256:
        problems.append("summary input_sha256 is not the candidate's")
    node_sum = sum(r.get("nodes", 0) for r in dirs)
    if node_sum != s.get("nodes"):
        problems.append(f"node total {node_sum} != summary {s.get('nodes')}")
    cpu_sum = sum(r["cpu_seconds"] for r in dirs)
    if abs(cpu_sum - s.get("direction_cpu_seconds", -1)) > 1e-6 * max(1.0, cpu_sum):
        problems.append("direction CPU total disagrees with the summary")
    h = cand.B / 2
    least_margin = None
    least_true = None
    exact_points = 0
    below_bound = []
    tree_bad = []
    outside = []
    axis = None
    for row in sorted(dirs, key=lambda q: q["r"]):
        r = row["r"]
        if row.get("verdict") != "verified" or row.get("threshold") != "1":
            problems.append(f"direction {r} not verified at threshold 1")
        bound = row.get("min_certified_lower_bound")
        if not isinstance(bound, float) or not bound >= 1.0:
            problems.append(f"direction {r} bound {bound!r} below 1")
        c, s_ = cos_sin(cand.step, r)
        if r == 0:
            if row.get("method") != "axis-vertex-sweep":
                problems.append("direction 0 is not the axis sweep")
            ax, ay = (Fraction(v) for v in row["argmin"])
            cap, _i, _b = exact_capture(meas, ax, ay, c, s_, h)
            axis = {
                "argmin": row["argmin"],
                "argmin_in_domain": in_domain(cand, 0, ax, ay, Fraction(0)),
                "exact_capture_at_argmin": float(cap),
                "certified_bound": bound,
                "exact_minus_bound": float(cap - Fraction(bound)),
                "vertices": row.get("vertices"),
                "x_events": row.get("x_events"),
                "y_events": row.get("y_events"),
            }
            continue
        if row.get("method") != "interval-branch-and-bound":
            problems.append(f"direction {r} method {row.get('method')!r}")
        if row.get("nodes") != 2 * row.get("leaves", -1) - 1:
            tree_bad.append(r)
        box = row["least_bound_box"]
        bx, by = Fraction(box["x"]), Fraction(box["y"])
        if not in_domain(cand, r, bx, by, Fraction(1, 10**9)):
            outside.append(r)
        cap, _i, _b = exact_capture(meas, bx, by, c, s_, h)
        exact_points += 1
        if cap < Fraction(bound):
            below_bound.append(r)
        margin = float(cap - 1)
        if least_true is None or margin < least_true[0]:
            least_true = (margin, r, box["x"], box["y"])
        if least_margin is None or bound - 1 < least_margin[0]:
            least_margin = (bound - 1, r)
    return {
        "direction_rows": len(dirs),
        "node_total": node_sum,
        "direction_cpu_seconds": cpu_sum,
        "threads": s.get("threads"),
        "wall_seconds": s.get("wall_seconds"),
        "build": s.get("build"),
        "least_certified_margin": {"margin": least_margin[0], "r": least_margin[1]},
        "exact_points_at_least_bound_box_centres": exact_points,
        "least_exact_margin_at_those_centres": {
            "margin": least_true[0], "r": least_true[1], "x": least_true[2], "y": least_true[3]
        },
        "exact_capture_below_certified_bound_at": below_bound,
        "incomplete_trees_at": tree_bad,
        "least_bound_box_centre_outside_domain_at": outside,
        "axis": axis,
        "problems": problems,
    }


def check_control(cand, meas, rows: list[dict]) -> dict:
    problems: list[str] = []
    summary = [r for r in rows if r.get("kind") == "sqverify-fast-summary/v1"]
    dirs = [r for r in rows if "r" in r]
    s = summary[0] if summary else {}
    listed = s.get("refused_directions", [])
    if sorted(r["r"] for r in dirs) != sorted(listed) or len(listed) != 32:
        problems.append("control directions are not its 32 refused directions")
    if s.get("status") != "REFUSED":
        problems.append("control summary is not REFUSED")
    prem = s.get("premises", {})
    if prem.get("mass_exact") != str(FACTOR * cand.total_mass).replace(" ", ""):
        want = FACTOR * cand.total_mass
        if prem.get("mass_exact") != f"{want.numerator}/{want.denominator}":
            problems.append("control mass is not 197/200 of the certificate's")
    spread = [round(k * cand.last / 31) for k in range(32)]
    h = cand.B / 2
    witnesses = []
    for row in sorted(dirs, key=lambda q: q["r"]):
        r = row["r"]
        c, s_ = cos_sin(cand.step, r)
        if r == 0:
            ax, ay = (Fraction(v) for v in row["argmin"])
            cap, _i, _b = exact_capture(meas, ax, ay, c, s_, h)
            mut = FACTOR * cap
            witnesses.append({
                "r": 0, "verdict": row.get("verdict"), "exact_mutant_capture": float(mut),
                "below_1": mut < 1, "reported_bound": row.get("min_certified_lower_bound"),
                "in_domain": in_domain(cand, 0, ax, ay, Fraction(0)),
            })
            continue
        w = row.get("witness") or {}
        pose = w.get("exact_pose")
        if row.get("verdict") != "counterexample-candidate" or pose is None:
            problems.append(f"control direction {r}: no exact witness")
            continue
        px, py = Fraction(pose[0]), Fraction(pose[1])
        cap, _i, _b = exact_capture(meas, px, py, c, s_, h)
        mut = FACTOR * cap
        reported = Fraction(w["exact_coverage"])
        witnesses.append({
            "r": r,
            "verdict": row["verdict"],
            "exact_mutant_capture": float(mut),
            "equals_source_fraction": mut == reported,
            "below_1": mut < 1,
            "source_flag_exact_below_threshold": w.get("exact_below_threshold"),
            "in_domain": in_domain(cand, r, px, py, Fraction(0)),
            "original_capture": float(cap),
        })
    exact_equal = sum(1 for w in witnesses if w.get("equals_source_fraction"))
    below = sum(1 for w in witnesses if w["below_1"])
    if any(not w["in_domain"] for w in witnesses):
        problems.append("a control witness lies outside its per-bin domain")
    return {
        "directions": sorted(listed),
        "evenly_spread_round_k_last_over_31": sorted(listed) == spread,
        "witnesses_recomputed": len(witnesses),
        "exact_fraction_equal_to_source": exact_equal,
        "mutant_capture_below_1": below,
        "witnesses": witnesses,
        "problems": problems,
    }


def check_receipts(cand, base: Path) -> dict:
    rec = loose_json((base / "check2" / "receipt.json").read_bytes())
    pre = loose_json((base / "verification" / "prepublication-receipt.json").read_bytes())
    ctl = loose_json((base / "check2" / "control.json").read_bytes())
    inner = rec["receipt"]
    checks = {
        "check2_status_verified": rec["status"] == "VERIFIED" and inner["status"] == "VERIFIED",
        "check2_counts": inner["directions_expected"] == inner["directions_checked"]
        == inner["directions_verified"] == cand.last + 1 and inner["directions_failed"] == 0,
        "check2_exit_0": inner["exit"] == 0,
        "check2_digest": rec["candidate_digest"] == inner["candidate_digest"],
        "prepublication_verified": pre["status"] == "VERIFIED" and pre["exit"] == 0
        and pre["directions_verified"] == cand.last + 1,
        "prepublication_same_candidate": pre["candidate_digest"] == rec["candidate_digest"]
        and pre["input_sha256"] == cand.raw_sha256,
        "prepublication_same_source_build_digest": pre["build"]["source_sha256"]
        == inner["verifier"]["source_sha256"],
        "control_refused": ctl["refused"] is True and ctl["tries"][0]["refused"] == 32
        and ctl["tries"][0]["factor"] == "197/200",
    }
    return {
        "checks": checks,
        "check2_seconds": inner["seconds"],
        "check2_threads": inner["threads"],
        "check2_started_utc": inner.get("started_utc"),
        "prepublication_seconds": pre["seconds"],
        "verifier_source_sha256": inner["verifier"]["source_sha256"],
        "verifier_binary_sha256": inner["verifier"].get("binary_sha256"),
        "checked_by_text": rec.get("checked_by"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only", type=int, action="append")
    args = ap.parse_args()
    t0 = time.perf_counter()
    out: dict[str, object] = {"kind": "t233-review-receipts-check/v1", "cases": {}}
    ok_all = True
    for n, (name, _side) in CERTS.items():
        if args.only and n not in args.only:
            continue
        c0 = resource.getrusage(resource.RUSAGE_SELF)
        cand = read_candidate(args.packet, n)
        meas = expand(cand)
        base = args.packet / "release" / "certificates" / name
        run = check_run(cand, meas, lines(base / "check2" / "run.jsonl.gz"))
        ctl = check_control(cand, meas, lines(base / "check2" / "control-197_200.jsonl.gz"))
        rec = check_receipts(cand, base)
        c1 = resource.getrusage(resource.RUSAGE_SELF)
        ok = (
            not run["problems"]
            and not run["exact_capture_below_certified_bound_at"]
            and not run["incomplete_trees_at"]
            and not run["least_bound_box_centre_outside_domain_at"]
            and run["least_exact_margin_at_those_centres"]["margin"] >= 0
            and run["axis"]["exact_minus_bound"] >= 0
            and not ctl["problems"]
            and ctl["exact_fraction_equal_to_source"] == 31
            and ctl["mutant_capture_below_1"] == 32
            and all(rec["checks"].values())
        )
        ok_all = ok_all and ok
        out["cases"][str(n)] = {
            "certificate": name,
            "run": run,
            "control": ctl,
            "receipts": rec,
            "verdict": "RECEIPTS_CONSISTENT" if ok else "RECEIPTS_INCONSISTENT",
            "cpu_seconds": round(c1.ru_utime + c1.ru_stime - c0.ru_utime - c0.ru_stime, 3),
        }
        print(n, out["cases"][str(n)]["verdict"], "least exact margin",
              run["least_exact_margin_at_those_centres"], "control equal",
              ctl["exact_fraction_equal_to_source"], "below1", ctl["mutant_capture_below_1"],
              "cpu", out["cases"][str(n)]["cpu_seconds"], flush=True)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["verdict"] = "ALL_CONSISTENT" if ok_all else "INCONSISTENCY_FOUND"
    out["cpu_seconds"] = round(usage.ru_utime + usage.ru_stime, 3)
    out["wall_seconds"] = round(time.perf_counter() - t0, 3)
    args.out.write_text(json.dumps(out, indent=1, sort_keys=True, default=str) + "\n")
    print(out["verdict"], "cpu", out["cpu_seconds"])
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
