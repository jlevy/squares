"""Judge one sqverify-fast --continuous run's output against exact arithmetic written here.

Reads the run's standard output (one JSON object per line), the candidate it ran and
the parameters, and decides, with Python's ``fractions`` and an exact oracle of its own
(``bounds_probe.exact_area``):

- the premises line: ``X = L/B``, the counting margin, ``A``, the axis containment margin
  and the mass equal what this review computes from the candidate and the parameters;
- every root line: its index and ``t`` range are the default cut's, a verified root is a
  complete binary cover (``nodes = 2 leaves - 1``) whose least certified bound is at
  least ``tau``, and no line is inherited (``--resume`` was not used);
- every refused root's witness: the pose ``(x, y, t)`` it prints, read as the exact
  rationals of its binary64 values, is legal (the side-``B`` square at angle
  ``2 atan t`` lies in ``[0, L]^2``), the capture there computed here equals the
  ``exact_capture`` the run prints, and whether it is below ``tau`` agrees with
  ``exact_below_threshold``; a refusal counts as a coverage refutation only when the pose
  is legal and the capture computed here is below ``tau``;
- the summary: its status follows from the root lines and the axis patch, its node and
  leaf totals are the sums of the root lines, and its claim is ``s(n) > L/B``.

It prints one JSON receipt and exits 0 when every check holds (a REFUSED run passes when
its refusals are reported faithfully; ``--expect`` names the status the run must have).

Usage::

    python -I judge_run.py RUN.jsonl CANDIDATE.json --core P/Q --tau P/Q --expect VERIFIED|REFUSED
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bounds_probe import exact_area, load_density, rotation, rows_of  # noqa: E402
from premises import EPS, LAST_T, default_axis_side, default_cuts, w_of  # noqa: E402


def capture(rects, x: F, y: F, t: F, core: F) -> F:
    c, s = rotation(t)
    h = core / 2
    reach = core
    total = F(0)
    for ex in rects:
        x1, y1, x2, y2 = ex.rect
        if x2 < x - reach or x1 > x + reach or y2 < y - reach or y1 > y + reach:
            continue
        total += ex.density * exact_area(ex.rect, x, y, c, s, h)
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--core", required=True)
    parser.add_argument("--tau", required=True)
    parser.add_argument("--expect", choices=("VERIFIED", "REFUSED"), required=True)
    args = parser.parse_args()
    core, tau = F(args.core), F(args.tau)
    doc = json.loads(args.candidate.read_text())
    n = int(doc["n"])
    side, rects = load_density(args.candidate)
    mass = sum((F(str(w)) for _, w in rows_of(doc)), F(0))
    a = default_axis_side(core, EPS)
    cuts = default_cuts(EPS, LAST_T)
    ends = [EPS, *cuts, LAST_T]
    roots = list(zip(ends, ends[1:]))
    lines = [json.loads(line) for line in args.run.read_text().splitlines() if line.strip()]
    checks: dict[str, bool] = {}
    notes: dict[str, object] = {}

    prem = next(line for line in lines if line.get("kind") == "premises")["premises"]
    checks["premises equal this review's"] = (
        prem["X"] == str(side / core)
        and prem["counting_margin"] == str(n * tau - mass)
        and prem["A"] == str(a)
        and prem["axis_containment_margin"] == str(core - a * w_of(EPS))
        and prem["mass"] == str(mass)
        and prem["n"] == n
    )
    axis = next(line for line in lines if line.get("kind") == "axis-patch")
    notes["axis_patch"] = {k: axis[k] for k in ("verified", "min_certified_lower_bound", "vertices")}
    root_lines = sorted((line for line in lines if line.get("kind") == "root"), key=lambda r: r["index"])
    checks["one line per root, in the default cuts"] = [r["index"] for r in root_lines] == list(range(len(roots))) and all(
        r["t"] == [str(lo), str(hi)] for r, (lo, hi) in zip(root_lines, roots, strict=True)
    )
    checks["no inherited line"] = all("inherited_from" not in r for r in root_lines)
    verified = [r for r in root_lines if r["verdict"] == "verified"]
    refused = [r for r in root_lines if r["verdict"] != "verified"]
    checks["verified roots are complete binary covers at or above tau"] = all(
        r["nodes"] == 2 * r["leaves"] - 1 and F(r["min_certified_lower_bound"]) >= tau for r in verified
    )
    witnesses = []
    least: F | None = None
    for r in refused:
        w = r["witness"]
        if "exact_pose" not in w:
            witnesses.append({"index": r["index"], "reason": w.get("reason"), "pose": None})
            continue
        x, y, t = (F(v) for v in w["exact_pose"])
        c, s = rotation(t)
        e_t = side / 2 - core / 2 * (c + s)
        legal = abs(x - side / 2) <= e_t and abs(y - side / 2) <= e_t
        value = capture(rects, x, y, t, core)
        equal = value == F(w["exact_capture"])
        below = value < tau
        witnesses.append({
            "index": r["index"],
            "reason": w["reason"],
            "legal": legal,
            "legal_margin": float(min(e_t - abs(x - side / 2), e_t - abs(y - side / 2))),
            "capture_here": float(value),
            "equals_run": equal,
            "below_tau": below,
            "agrees_with_flag": below == w["exact_below_threshold"],
            "counts_as_refutation": legal and below,
        })
        if legal and below and (least is None or value < least):
            least = value
    checks["every witness capture equals the run's exact_capture"] = all(
        x.get("equals_run", True) for x in witnesses)
    checks["every witness flag agrees"] = all(x.get("agrees_with_flag", True) for x in witnesses)
    summary = lines[-1]
    status = "VERIFIED" if (not refused and len(root_lines) == len(roots) and axis["verified"]) else "REFUSED"
    checks["summary status follows from the lines"] = summary["status"] == status
    checks["summary totals are the sums"] = (
        summary["nodes"] == sum(r["nodes"] for r in root_lines)
        and summary["leaves"] == sum(r["leaves"] for r in root_lines)
        and summary["refused_roots"] == [r["index"] for r in refused]
    )
    checks["summary claim"] = summary["claim"] == (f"s({n}) > {side / core}" if status == "VERIFIED" else "")
    checks["status is the expected one"] = summary["status"] == args.expect
    receipt = {
        "run": args.run.name,
        "candidate": args.candidate.name,
        "core": str(core),
        "tau": str(tau),
        "status": summary["status"],
        "nodes": summary["nodes"],
        "leaves": summary["leaves"],
        "roots": len(root_lines),
        "refused_roots": len(refused),
        "min_certified_lower_bound": summary["min_certified_lower_bound"],
        "build": summary["build"],
        "run_key": summary["run_key"],
        "legal_refutations": sum(1 for x in witnesses if x.get("counts_as_refutation")),
        "least_refuting_capture": float(least) if least is not None else None,
        "witnesses": witnesses,
        "notes": notes,
        "checks": checks,
        "all_hold": all(checks.values()),
    }
    json.dump(receipt, sys.stdout, indent=2)
    print()
    return 0 if receipt["all_hold"] else 1


if __name__ == "__main__":
    sys.exit(main())
