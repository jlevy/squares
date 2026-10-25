"""Exact captures at the poses the source's logs name, by this review's own evaluator.

Usage: python3 -I source_log_points.py CANDIDATE RUN_LOG CONTROL_LOG COUNT OUTPUT.json

Decides, at single poses only (no coverage):

- the axis row (direction 0): the exact capture at its logged argmin vertex, against the
  row's certified least bound; and the same pose under the 197/200 control, which the
  control log refuses by the sweep's value rather than by an exact witness;
- the COUNT directions with the smallest least certified bound: the exact capture at two
  points of each row's least-bound box, (x, y) and (x + dx/2, y + dy/2), both in the box
  whichever corner convention the log uses; each must be at least the row's certified
  bound, since that bound holds over the whole box;
- every oblique refusal of the control log: the exact capture of the 197/200 measure at
  the logged witness, which must be below one, and of the original measure, which must
  be at least one, with the witness inside the exact per-bin domain.

Binary64 numbers in the logs are converted to the rationals they denote. The evaluator is
n31_brute (Sutherland-Hodgman clipping in Fractions over the merged D4 expansion).
"""

from __future__ import annotations

import gzip
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import n31_brute as nb  # noqa: E402
import n31_exact as nx  # noqa: E402


def angle(j, step):
    if j == 0:
        return Fraction(1), Fraction(0)
    c, s, e = nx.direction(j, step)
    return Fraction(c, e), Fraction(s, e)


def in_domain(j, x, y, cand):
    step, side = cand["step"], cand["L"]
    r = nx.r_of(max(Fraction(0), j * step - step / 2))
    return r <= x <= side - r and r <= y <= side - r


def as_fraction(v):
    if isinstance(v, str):
        return Fraction(v)
    return Fraction(v)


def main() -> int:
    start = time.process_time()
    cand = nx.read_candidate(Path(sys.argv[1]))
    run = [json.loads(x) for x in gzip.open(sys.argv[2], "rt")]
    ctrl = [json.loads(x) for x in gzip.open(sys.argv[3], "rt")]
    count = int(sys.argv[4])
    out_path = Path(sys.argv[5])
    merged = nx.expand(cand["rectangles"], cand["L"])
    scaled = {k: v * Fraction(197, 200) for k, v in merged.items()}
    core, step = cand["B"], cand["step"]
    rows = {r["r"]: r for r in run if "r" in r}
    report: dict[str, object] = {}
    ok = True

    axis = rows[0]
    ax_x, ax_y = (as_fraction(v) for v in axis["argmin"])
    cap = nb.capture(merged, ax_x, ax_y, core, Fraction(1), Fraction(0))
    cap_c = cap * Fraction(197, 200)
    report["axis"] = {
        "argmin": [str(ax_x), str(ax_y)], "in_domain": in_domain(0, ax_x, ax_y, cand),
        "certified_bound": axis["min_certified_lower_bound"],
        "exact_capture": str(cap), "exact_capture_float": float(cap),
        "bound_below_exact": float(cap) >= axis["min_certified_lower_bound"] - 1e-15,
        "control_197_200_exact": float(cap_c), "control_below_one": cap_c < 1,
    }
    ok = ok and report["axis"]["in_domain"] and cap >= 1 and cap_c < 1

    tight = sorted((r for r in run if "r" in r and r.get("least_bound_box")),
                   key=lambda r: r["min_certified_lower_bound"])[:count]
    tight_rows = []
    for r in tight:
        j = r["r"]
        box = r["least_bound_box"]
        x, y = Fraction(box["x"]), Fraction(box["y"])
        dx, dy = Fraction(box["dx"]), Fraction(box["dy"])
        cos, sin = angle(j, step)
        pts = []
        for px, py in ((x, y), (x + dx / 2, y + dy / 2)):
            capj = nb.capture(merged, px, py, core, cos, sin)
            good = capj >= Fraction(r["min_certified_lower_bound"])
            pts.append({"point": [float(px), float(py)], "exact_capture": float(capj),
                        "at_least_certified_bound": good,
                        "in_domain": in_domain(j, px, py, cand)})
            ok = ok and good
        tight_rows.append({"j": j, "certified_bound": r["min_certified_lower_bound"],
                           "points": pts})
    report["tightest"] = tight_rows

    ctrl_rows = []
    for r in ctrl:
        if "r" not in r or r.get("method") != "interval-branch-and-bound":
            continue
        w = r.get("witness") or {}
        centre = w.get("exact_pose")
        if centre is None:
            ctrl_rows.append({"j": r["r"], "witness_keys": sorted(w)})
            ok = False
            continue
        px, py = (as_fraction(v) for v in centre)
        cos, sin = angle(r["r"], step)
        cap_s = nb.capture(scaled, px, py, core, cos, sin)
        cap_o = cap_s * Fraction(200, 197)
        logged = w.get("exact_coverage")
        row = {"j": r["r"], "witness": [float(px), float(py)],
               "in_domain": in_domain(r["r"], px, py, cand),
               "scaled_capture": float(cap_s), "scaled_below_one": cap_s < 1,
               "equals_logged_exact_coverage": (logged is not None
                                                and cap_s == Fraction(logged)),
               "original_capture": float(cap_o), "original_at_least_one": cap_o >= 1}
        ok = (ok and row["in_domain"] and cap_s < 1 and cap_o >= 1
              and row["equals_logged_exact_coverage"])
        ctrl_rows.append(row)
    report["control_witnesses"] = ctrl_rows
    report["status"] = "CONSISTENT" if ok else "INCONSISTENT"
    report["kind"] = "review-2026-10-23-n31-source-log-points/v1"
    report["program_sha256"] = nx.sha256_file(Path(__file__))
    report["brute_sha256"] = nx.sha256_file(Path(nb.__file__))
    report["cpu_seconds"] = round(time.process_time() - start, 3)
    out_path.write_text(json.dumps(report, indent=1) + "\n")
    print(report["status"], "axis", report["axis"]["exact_capture_float"],
          "tightest", len(tight_rows), "control witnesses", len(ctrl_rows),
          f"cpu {report['cpu_seconds']} s")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
