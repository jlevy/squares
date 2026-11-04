"""Sampled exact captures at the certificate's directions; decides no direction.

Usage: dm_sample.py CERTIFICATE.json.gz HOSONO.json.gz CENSUS_CAPTURE.jsonl.gz OUT_DIR

Three samples, each a necessary condition that a wrong `verified` could fail:

A. Every oblique direction (1 to 599): the census capture's least-bound leaf is a box
   C = [x +- dx] x [y +- dy] on which the crate certified F_r >= its least bound. This
   program evaluates F_r exactly (dmlib method 1) at the box's centre and four corners
   and requires each to be at least that bound, and at least 1. Rows go to
   `leaf-poses.jsonl`, one a direction.

B. Chosen directions (the least-bound direction 277; 144; the ends 1, 2, 3, 597, 598,
   599; the new directions around the middle, 298, 299, 301; and eight drawn with a fixed
   seed among the 400 new ones): a binary64 search for the least capture on the quadrant
   [L/2, U_r]^2, by a 90 x 90 grid, two strips along the walls x = U_r and y = U_r
   (the region the dilation adds, in Hosono's coordinates, is a strip of width below
   0.0011 there), and Nelder-Mead from the lowest grid and strip points; then the three
   lowest poses found are evaluated exactly. The least exact capture found must be at
   least the direction's certified bound and at least 1.

C. The dilation's carry, exactly: at directions 3k shared with Hosono's net, the
   dilated certificate's capture at c equals Hosono's mixed_n94_L995 capture at Hosono's
   direction k and c / lambda.
"""

from __future__ import annotations

import gzip
import json
import math
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dmlib  # noqa: E402

CHOSEN = [1, 2, 3, 144, 277, 298, 299, 301, 597, 598, 599]


def census_rows(path: Path) -> dict[int, dict]:
    rows = {}
    with gzip.open(path, "rt") as stream:
        for line in stream:
            row = json.loads(line)
            if "r" in row:
                rows[int(row["r"])] = row
    return rows


def search(fm: dmlib.FloatMeasure, index: int, lo: float, hi: float) -> dict:
    """Binary64 search for low captures on [lo, hi]^2; returns candidate poses."""
    grid = np.linspace(lo, hi, 90)
    values = np.array([[fm.capture(index, x, y) for y in grid] for x in grid])
    order = np.argsort(values, axis=None)[:10]
    starts = [(float(grid[i // 90]), float(grid[i % 90])) for i in order]
    width = 0.0015
    strip = np.linspace(hi - width, hi, 7)
    along = np.linspace(lo, hi, 300)
    wall_x = [(fm.capture(index, float(x), float(y)), float(x), float(y)) for x in strip for y in along]
    wall_y = [(fm.capture(index, float(x), float(y)), float(x), float(y)) for y in strip for x in along]
    wall_x.sort()
    wall_y.sort()
    starts += [(x, y) for _, x, y in wall_x[:2]] + [(x, y) for _, x, y in wall_y[:2]]
    found = []
    spacing = (hi - lo) / 89
    for x0, y0 in starts:
        simplex = np.array([[x0, y0], [min(x0 + spacing, hi), y0], [x0, min(y0 + spacing, hi)]])
        result = minimize(
            lambda p: fm.capture(index, float(p[0]), float(p[1])),
            np.array([x0, y0]),
            method="Nelder-Mead",
            bounds=[(lo, hi), (lo, hi)],
            options={"xatol": 1e-11, "fatol": 1e-14, "maxfev": 500, "initial_simplex": simplex},
        )
        found.append((float(result.fun), float(result.x[0]), float(result.x[1])))
    found.sort()
    return {
        "grid_least": float(values.min()),
        "wall_x_least": wall_x[0],
        "wall_y_least": wall_y[0],
        "refined": found,
    }


def main() -> None:
    cert_path, hosono_path, census_path, out_dir = (Path(a) for a in sys.argv[1:5])
    started = time.process_time()
    cert = dmlib.certificate(dmlib.read_gzip_json(cert_path).data)
    images = dmlib.expand(cert)
    exact = dmlib.ExactMeasure.of(cert, images)
    fm = dmlib.FloatMeasure.of(cert, images)
    rows = census_rows(census_path)
    failures: list[str] = []

    # A. every oblique direction's least-bound leaf
    leaf_lines = []
    least_margin = None
    for index in range(1, cert.count):
        row = rows[index]
        box = row["least_bound_box"]
        bound = Fraction(row["min_certified_lower_bound"])
        poses = [(box["x"], box["y"])] + [
            (box["x"] + sx * box["dx"], box["y"] + sy * box["dy"]) for sx in (-1, 1) for sy in (-1, 1)
        ]
        captures = [
            dmlib.fraction_of(dmlib.capture_exact(exact, index, dmlib.exact_of_float(x), dmlib.exact_of_float(y))[0])
            for x, y in poses
        ]
        low = min(captures)
        ok = low >= bound and low >= 1
        if not ok:
            failures.append(f"leaf at r {index}: exact {float(low)} below bound {float(bound)}")
        margin = low - bound
        if least_margin is None or margin < least_margin[0]:
            least_margin = (margin, index)
        leaf_lines.append(
            json.dumps(
                {
                    "r": index,
                    "certified_bound": float(bound),
                    "exact_centre": float(captures[0]),
                    "exact_least_of_centre_and_corners": float(low),
                    "ok": ok,
                },
                separators=(",", ":"),
            )
        )
    (out_dir / "leaf-poses.jsonl").write_text("\n".join(leaf_lines) + "\n")
    part_a = {
        "directions": cert.count - 1,
        "poses_evaluated_exactly": 5 * (cert.count - 1),
        "all_at_least_their_certified_bound_and_1": not failures,
        "least_exact_minus_bound": [float(least_margin[0]), least_margin[1]] if least_margin else None,
        "cpu_seconds_so_far": round(time.process_time() - started, 1),
    }

    # B. chosen directions: search, then exact
    rng = random.Random(20261103)
    new = [r for r in range(1, cert.count) if r % 3 and r not in CHOSEN]
    drawn = sorted(rng.sample(new, 8))
    part_b = []
    lowest_overall = None
    for index in CHOSEN + drawn:
        low, high = dmlib.domain(cert, index)
        # The largest binary64 values inside the exact quadrant's ends.
        lo = float(cert.side / 2)
        if Fraction(lo) < cert.side / 2:
            lo = math.nextafter(lo, math.inf)
        hi = float(high)
        if Fraction(hi) > high:
            hi = math.nextafter(hi, -math.inf)
        found = search(fm, index, lo, hi)
        exacts = []
        for value, x, y in found["refined"][:3]:
            x = min(max(x, lo), hi)
            y = min(max(y, lo), hi)
            ex, ey = dmlib.exact_of_float(x), dmlib.exact_of_float(y)
            inside = all(low <= dmlib.fraction_of(v) <= high for v in (ex, ey))
            cap = dmlib.fraction_of(dmlib.capture_exact(exact, index, ex, ey)[0])
            exacts.append({"pose": [x, y], "in_domain": inside, "at_wall": max(x, y) == hi, "binary64": value, "exact": float(cap), "exact_minus_1": float(cap - 1)})
            if not inside:
                failures.append(f"search pose outside the domain at r {index}")
            if lowest_overall is None or cap < lowest_overall[0]:
                lowest_overall = (cap, index, x, y)
        bound = float(rows[index]["min_certified_lower_bound"])
        least = min(e["exact"] for e in exacts)
        if least < bound or least < 1:
            failures.append(f"search at r {index} found exact {least} below {bound} or 1")
        part_b.append(
            {
                "r": index,
                "new_direction": index % 3 != 0,
                "U_r": str(high),
                "U_r_float": float(high),
                "certified_bound": bound,
                "grid_least": found["grid_least"],
                "wall_x_least": found["wall_x_least"],
                "wall_y_least": found["wall_y_least"],
                "lowest_found_exact": exacts,
            }
        )

    # C. the dilation's carry at shared directions, exactly
    base = dmlib.certificate(dmlib.read_gzip_json(hosono_path).data, require_net=False)
    base_exact = dmlib.ExactMeasure.of(base, dmlib.expand(base))
    lam = cert.side / base.side
    carry = []
    for k in (1, 50, 92, 199):
        r = 3 * k
        _, high = dmlib.domain(base, k)
        for _ in range(2):
            ox = float(base.side / 2) + rng.random() * float(high - base.side / 2)
            oy = float(base.side / 2) + rng.random() * float(high - base.side / 2)
            old_c = (dmlib.exact_of_float(ox), dmlib.exact_of_float(oy))
            new_c = tuple(v * dmlib.q(lam) for v in old_c)
            old_cap = dmlib.capture_exact(base_exact, k, *old_c)[0]
            new_cap = dmlib.capture_exact(exact, r, *new_c)[0]
            carry.append({"hosono_k": k, "r": r, "hosono_pose": [ox, oy], "capture": float(old_cap), "equal": old_cap == new_cap})
            if old_cap != new_cap:
                failures.append(f"dilation identity fails at k {k}")

    report = {
        "program": "dm_sample.py",
        "program_sha256": dmlib.sha256_file(Path(__file__)),
        "dmlib_sha256": dmlib.sha256_file(Path(dmlib.__file__)),
        "certificate_file_sha256": dmlib.sha256_file(cert_path),
        "census_capture_sha256": dmlib.sha256_file(census_path),
        "A_least_bound_leaves": part_a,
        "B_searched_directions": part_b,
        "B_lowest_exact_capture_found": None
        if lowest_overall is None
        else {
            "r": lowest_overall[1],
            "pose": [lowest_overall[2], lowest_overall[3]],
            "exact": str(lowest_overall[0]),
            "exact_float": float(lowest_overall[0]),
        },
        "C_dilation_identity": carry,
        "failures": failures,
        "status": "CONSISTENT" if not failures else "INCONSISTENT",
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    (out_dir / "sample.json").write_text(dmlib.dumps(report) + "\n")
    print(json.dumps({"status": report["status"], "failures": failures, "A": part_a, "lowest": report["B_lowest_exact_capture_found"], "cpu_seconds": report["cpu_seconds"]}, indent=1))


if __name__ == "__main__":
    main()
