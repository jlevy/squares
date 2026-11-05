#!/usr/bin/env python3
"""Does the uniform tiny turn matter? Set the near-upright squares exactly upright.

A measurement for the review. In #895's certificate every near-upright square carries a
turn of about -2.4e-12 radians. This program:

1. sets t = 0 for every square turned by less than 1e-9 radians and decides the result
   at #895's side by certcheck.py's methods A and B;
2. computes the exact least scale lambda of those poses about the origin at which every
   wall and pair holds (side.py's contact_scale), builds that dilation exactly and decides
   it by both methods at contact and 1e-30 below it, and compares lambda * S with #895's
   side and with T-257's;
3. fits, to the turned squares that moved less than 1e-6 from T-257's poses, a
   similarity (scale, small rotation alpha, translation) taking T-257's centres to #895's,
   to see whether the turn is a rotation of the upright block's positions too or a turn
   of each square in place.

Usage: python -I upright.py --yim CERT --t257 CERT --out RECEIPT.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import mpmath
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certcheck as cc  # noqa: E402
import side as sd  # noqa: E402

mpmath.mp.dps = 50
EPS = F(1, 10**30)


def theta(t: F):
    return 2 * mpmath.atan(mpmath.mpf(t.numerator) / t.denominator)


def scaled(cert, lam):
    squares = [dict(s, x=s["x"] * lam, y=s["y"] * lam, tokens=[]) for s in cert["squares"]]
    return {"n": cert["n"], "side": cert["side"] * lam, "squares": squares}


def brief(res):
    return {"accepted_by_A": res["accepted_by_A"], "accepted_by_B": res["accepted_by_B"],
            "methods_agree_on_pairs": res["methods_agree_on_pairs"],
            "methods_agree_on_walls": res["methods_agree_on_walls"],
            "A_overlapping_pairs": res["A"]["overlapping_pair_count"],
            "A_least_pairs": res["A"]["least_pairs"][:4],
            "A_walls": {k: v["least_float"] for k, v in res["A"]["walls"].items()},
            "A_wall_failure_count": res["A"]["wall_failure_count"],
            "B_overlapping_pairs": res["B"]["overlapping_pair_count"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yim", required=True)
    ap.add_argument("--t257", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    t0 = time.time()
    Y = cc.parse_cert(args.yim)
    T = cc.parse_cert(args.t257)
    n = Y["n"]
    tiny = [i for i, s in enumerate(Y["squares"]) if abs(theta(s["t"])) < mpmath.mpf("1e-9")]
    out: dict = {"program": "upright.py", "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 "certcheck_sha256": cc.program_digest(), "python": platform.python_version(),
                 "inputs": {"yim": Y["sha256"], "t257": T["sha256"]}, "tiny_turned": len(tiny)}

    # 1. upright at #895's side
    U = {"n": n, "side": Y["side"], "squares": [dict(s, t=F(0) if i in tiny else s["t"], tokens=[])
                                                 for i, s in enumerate(Y["squares"])]}
    r0 = cc.decide(U, "ccw", "AB")
    out["upright_at_yim_side"] = brief(r0)
    print("upright at S_Y:", json.dumps(out["upright_at_yim_side"])[:900])

    # 2. exact contact scale of the upright poses, and its dilation decided at and below contact
    pose = cc.poses(U, "ccw")
    lam, where = sd.contact_scale(pose, U["side"])
    s_u = lam * Y["side"]
    out["contact_scale"] = {"lambda": str(lam), "lambda_minus_one": float(lam - 1), "attained_by": where,
                            "side": sd.digits(s_u), "above_yim_by": float(s_u - Y["side"]),
                            "below_t257_by": float(T["side"] - s_u)}
    print("contact scale:", out["contact_scale"])
    at = cc.decide(scaled(U, lam), "ccw", "AB")
    below = cc.decide(scaled(U, lam - EPS), "ccw", "AB")
    out["dilation_at_contact"] = brief(at)
    out["dilation_1e-30_below_contact"] = brief(below)
    print("at contact:", at["accepted_by_A"], at["accepted_by_B"], "| 1e-30 below:", below["accepted_by_A"],
          below["accepted_by_B"], below["A"]["overlapping_pair_count"], below["A"]["wall_failure_count"])

    # 3. is the turn also a rotation of the block's positions?
    hy, ht = Y["side"] / 2, T["side"] / 2
    out["block_fit"] = {}
    for limit in (1e-6, 1e-8, 1e-9):
        rows, rhs = [], []
        used = []
        for i in tiny:
            a, b = Y["squares"][i], T["squares"][i]
            dx = (a["x"] - hy) - (b["x"] - ht)
            dy = (a["y"] - hy) - (b["y"] - ht)
            if float(dx) ** 2 + float(dy) ** 2 < limit**2:
                used.append(i)
                px, py = float(b["x"] - ht), float(b["y"] - ht)
                # dx = k*px - alpha*py + bx ; dy = k*py + alpha*px + by
                rows.append([px, -py, 1.0, 0.0])
                rhs.append(float(dx))
                rows.append([py, px, 0.0, 1.0])
                rhs.append(float(dy))
        if len(used) < 3:
            out["block_fit"][f"moved_below_{limit:g}"] = {"squares": len(used)}
            continue
        A = np.array(rows)
        bvec = np.array(rhs)
        sol, *_ = np.linalg.lstsq(A, bvec, rcond=None)
        resid = bvec - A @ sol
        turns = [float(theta(Y["squares"][i]["t"])) for i in used]
        out["block_fit"][f"moved_below_{limit:g}"] = {
            "squares": len(used), "scale_minus_one": float(sol[0]), "alpha_radians": float(sol[1]),
            "translation": [float(sol[2]), float(sol[3])],
            "residual_max": float(np.abs(resid).max()), "residual_rms": float(np.sqrt((resid**2).mean())),
            "displacement_max": float(np.abs(bvec).max()),
            "mean_turn_of_these_squares_radians": float(np.mean(turns)),
            "side_ratio_minus_one": float(Y["side"] / T["side"] - 1)}
        print(f"block fit below {limit:g}:", out["block_fit"][f"moved_below_{limit:g}"])
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["cpu_seconds_total"] = round(usage.ru_utime + usage.ru_stime, 3)
    out["wall_seconds"] = round(time.time() - t0, 3)
    Path(args.out).write_text(json.dumps(out, indent=1, default=str) + "\n")
    print("cpu", out["cpu_seconds_total"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
