#!/usr/bin/env python3
"""The side of #895's certificate: header, issue fraction, decimal prints, extents and slack.

It measures, exactly:
- that the header side equals the fraction #895 states, in lowest terms, and its prints;
- the packing's extent in x and y from the corners, and so the least side the
  coordinates give (the header side less the least near-wall clearance on the axis
  that sets it);
- the difference to T-257's side at 260, in units of the 12th decimal and of binary64
  spacing, and the 1 + 1e-12 dilation T-257's certificate states in its comment line;
- for each certificate, the least uniform scale lambda of its centres and side about
  the origin, orientations fixed, at which every wall and pair still holds (a pair holds
  at lambda when lambda * |a.d| >= the summed half-widths on one of its four edge
  normals a): lambda * S is the side at which that certificate's own poses reach
  contact, so S - lambda * S is the certificate's own slack.

Usage: python -I side.py --yim CERT --t257 CERT --issue-fraction P/Q --out RECEIPT.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import resource
import sys
import time
from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_HALF_EVEN, Decimal, getcontext
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certcheck as cc  # noqa: E402

getcontext().prec = 80


def dec(x: F, places: int, rounding) -> str:
    q = Decimal(x.numerator) / Decimal(x.denominator)
    return str(q.quantize(Decimal(1).scaleb(-places), rounding=rounding))


def digits(x: F, places: int = 40) -> str:
    return dec(x, places, ROUND_DOWN)


def extents(sq, side):
    xs = [p[0] for s in sq for p in s["P"]]
    ys = [p[1] for s in sq for p in s["P"]]
    return min(xs), max(xs), min(ys), max(ys)


def contact_scale(sq, side):
    """Least lambda (exact) at which the poses scaled about the origin still pack in lambda*S."""
    worst = F(0)
    where = None
    n = len(sq)
    for i, s in enumerate(sq):
        xs = [p[0] - s["x"] for p in s["P"]]
        ys = [p[1] - s["y"] for p in s["P"]]
        hx, hy = max(xs), max(ys)
        for need, label in (
            (hx / s["x"], ("left", i + 1)),
            (hx / (side - s["x"]), ("right", i + 1)),
            (hy / s["y"], ("bottom", i + 1)),
            (hy / (side - s["y"]), ("top", i + 1)),
        ):
            if need > worst:
                worst, where = need, label
    for i in range(n):
        for j in range(i + 1, n):
            a_i, b_i = sq[i]["u"], sq[i]["v"]
            a_j, b_j = sq[j]["u"], sq[j]["v"]
            dx = sq[j]["x"] - sq[i]["x"]
            dy = sq[j]["y"] - sq[i]["y"]
            best = None
            for ax, own_u, own_v, other_u, other_v in (
                (a_i, a_i, b_i, a_j, b_j),
                (b_i, a_i, b_i, a_j, b_j),
                (a_j, a_j, b_j, a_i, b_i),
                (b_j, a_j, b_j, a_i, b_i),
            ):
                proj = abs(ax[0] * dx + ax[1] * dy)
                if proj == 0:
                    continue
                half = F(1, 2) + (abs(ax[0] * other_u[0] + ax[1] * other_u[1]) + abs(ax[0] * other_v[0] + ax[1] * other_v[1])) / 2
                need = half / proj
                if best is None or need < best:
                    best = need
            if best is not None and best > worst:
                worst, where = best, ("pair", i + 1, j + 1)
    return worst, where


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yim", required=True)
    ap.add_argument("--t257", required=True)
    ap.add_argument("--issue-fraction", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    t0 = time.time()
    y = cc.parse_cert(args.yim)
    t = cc.parse_cert(args.t257)
    sy, st = y["side"], t["side"]
    p, q = (int(v) for v in args.issue_fraction.replace(" ", "").split("/"))
    issue = F(p, q)
    out: dict = {"program": "side.py", "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 "certcheck_sha256": cc.program_digest(), "python": platform.python_version()}
    out["header"] = {
        "token": y["side_token"],
        "equals_issue_fraction": sy == issue,
        "issue_fraction_in_lowest_terms": math.gcd(p, q) == 1,
        "header_token_is_issue_fraction_verbatim": y["side_token"] == f"{p}/{q}",
        "digits_40": digits(sy),
        "cut_16": dec(sy, 16, ROUND_DOWN),
        "nearest_16": dec(sy, 16, ROUND_HALF_EVEN),
        "up_16": dec(sy, 16, ROUND_CEILING),
        "up_12": dec(sy, 12, ROUND_CEILING),
        "issue_print": "16.6339825019226141",
    }
    out["header"]["issue_print_is_cut_or_nearest_16"] = out["header"]["issue_print"] in (
        out["header"]["cut_16"], out["header"]["nearest_16"])
    diff = st - sy
    out["t257"] = {
        "side": t["side_token"],
        "digits_40": digits(st),
        "nearest_16": dec(st, 16, ROUND_HALF_EVEN),
        "up_12": dec(st, 12, ROUND_CEILING),
        "comment": t["comments"],
        "undilated_side_if_1e-12_about_origin": digits(st / (1 + F(1, 10**12))),
    }
    ulp = math.ulp(float(sy))
    out["difference"] = {
        "exact": str(diff),
        "digits": digits(diff, 50),
        "float": float(diff),
        "yim_below_t257": diff > 0,
        "units_of_12th_place": float(diff * 10**12),
        "same_12_place_print_rounded_up": out["header"]["up_12"] == out["t257"]["up_12"],
        "binary64_spacing_at_side": ulp,
        "in_binary64_spacings": float(diff) / ulp,
        "t257_dilation_share_of_side": float(st - st / (1 + F(1, 10**12))),
        "difference_over_t257_dilation_share": float(diff / (st - st / (1 + F(1, 10**12)))),
    }
    report = {}
    for name, cert in (("yim", y), ("t257", t)):
        sq = cc.poses(cert, "ccw")
        side = cert["side"]
        x0, x1, y0, y1 = extents(sq, side)
        ext_x, ext_y = x1 - x0, y1 - y0
        least_side = max(ext_x, ext_y)
        lam, where = contact_scale(sq, side)
        report[name] = {
            "min_corner_x": str(x0), "min_corner_x_float": float(x0),
            "far_clearance_x": str(side - x1), "far_clearance_x_float": float(side - x1),
            "min_corner_y": str(y0), "min_corner_y_float": float(y0),
            "far_clearance_y": str(side - y1), "far_clearance_y_float": float(side - y1),
            "extent_x_short_of_side": float(side - ext_x),
            "extent_y_short_of_side": float(side - ext_y),
            "least_side_from_coordinates": str(least_side),
            "least_side_digits": digits(least_side),
            "header_side_minus_least_side": str(side - least_side),
            "header_side_minus_least_side_float": float(side - least_side),
            "contact_scale": str(lam),
            "contact_scale_float_minus_one": float(lam - 1),
            "contact_scale_attained_by": where,
            "side_at_contact_scale_digits": digits(lam * side),
            "slack_of_side_under_scaling": float(side - lam * side),
        }
    out["extents_and_slack"] = report
    out["yim_below_t257_contact_side_by"] = float(F(report["t257"]["contact_scale"]) * st - sy)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["cpu_seconds_total"] = round(usage.ru_utime + usage.ru_stime, 3)
    out["wall_seconds"] = round(time.time() - t0, 3)
    Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1)[:6000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
