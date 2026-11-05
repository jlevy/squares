#!/usr/bin/env python3
"""Do the large moves bear on the bound? Exchange the movers' poses between the packings.

A measurement for the review. The pairing is row for row (identity.py shows it is the
nearest-centre and optimal pairing under the identity), and positions are carried
between the boxes box-centred, p -> p - S_from/2 + S_to/2, with the tangent unchanged.

- backward: #895's packing with the squares that moved beyond tau put back at T-257's
  poses, at #895's side. If it still packs, the side reached does not need those moves.
- forward: T-257's packing with those squares at #895's poses, at T-257's side. If it
  still packs, the moves fit T-257's packing as it is, so they lie in its free play.

Each hybrid is decided over every wall and pair by certcheck.py's methods A and B.
The squares that move beyond tau are classified by direction (along x, along y, other)
and by tilt.

Usage: python -I movers.py --yim CERT --t257 CERT --out RECEIPT.json [--tau 0.1 0.01]
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certcheck as cc  # noqa: E402


def moved(Y, T, tau):
    hy, ht = Y["side"] / 2, T["side"] / 2
    out = []
    for i, (a, b) in enumerate(zip(Y["squares"], T["squares"])):
        dx = (a["x"] - hy) - (b["x"] - ht)
        dy = (a["y"] - hy) - (b["y"] - ht)
        if float(dx) ** 2 + float(dy) ** 2 > tau**2:
            out.append((i, dx, dy))
    return out


def hybrid(base, donor, rows):
    """base's certificate with the given rows' poses taken from donor, carried box-centred."""
    hb, hd = base["side"] / 2, donor["side"] / 2
    squares = [dict(s) for s in base["squares"]]
    for i in rows:
        d = donor["squares"][i]
        squares[i] = {"row": i + 1, "line": i + 3, "x": d["x"] - hd + hb, "y": d["y"] - hd + hb, "t": d["t"], "tokens": []}
    return {"n": base["n"], "side": base["side"], "squares": squares}


def summary(res):
    a, b = res["A"], res["B"]
    return {
        "accepted_by_A": res["accepted_by_A"], "accepted_by_B": res["accepted_by_B"],
        "methods_agree_on_pairs": res["methods_agree_on_pairs"],
        "methods_agree_on_walls": res["methods_agree_on_walls"],
        "A_overlapping_pairs": a["overlapping_pair_count"],
        "A_deepest_pairs": a["least_pairs"][:6],
        "A_wall_failures": a["wall_failures"][:6],
        "A_least_walls": {k: v["least_float"] for k, v in a["walls"].items()},
        "B_overlapping_pairs": b["overlapping_pairs"][:6],
        "cpu_seconds_A": a["cpu_seconds"], "cpu_seconds_B": b["cpu_seconds"],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yim", required=True)
    ap.add_argument("--t257", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tau", type=float, nargs="+", default=[0.1, 0.01])
    args = ap.parse_args(argv)
    t0 = time.time()
    Y = cc.parse_cert(args.yim)
    T = cc.parse_cert(args.t257)
    out: dict = {"program": "movers.py", "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 "certcheck_sha256": cc.program_digest(), "python": platform.python_version(),
                 "inputs": {"yim": Y["sha256"], "t257": T["sha256"]}, "runs": {}}
    for tau in args.tau:
        mv = moved(Y, T, tau)
        rows = [i for i, _, _ in mv]
        classes = {"along_x": [], "along_y": [], "other": []}
        for i, dx, dy in mv:
            if abs(dy) <= abs(dx) * F(1, 10**6):
                classes["along_x"].append(i + 1)
            elif abs(dx) <= abs(dy) * F(1, 10**6):
                classes["along_y"].append(i + 1)
            else:
                classes["other"].append(i + 1)
        back = cc.decide(hybrid(Y, T, rows), "ccw", "AB")
        fwd = cc.decide(hybrid(T, Y, rows), "ccw", "AB")
        for r in (back, fwd):
            r.pop("_gaps", None)
            r.pop("_walls", None)
        out["runs"][f"tau={tau:g}"] = {
            "squares": len(rows), "rows": [i + 1 for i in rows], "direction_classes": classes,
            "backward_yim_side_with_t257_poses": summary(back),
            "forward_t257_side_with_yim_poses": summary(fwd),
        }
        print(f"tau={tau:g}: {len(rows)} squares; classes "
              f"{ {k: len(v) for k, v in classes.items()} }")
        for name, r in (("backward", back), ("forward", fwd)):
            s = summary(r)
            print(f"  {name}: A {s['accepted_by_A']} B {s['accepted_by_B']} agree {s['methods_agree_on_pairs']} "
                  f"overlaps {s['A_overlapping_pairs']} deepest {s['A_deepest_pairs'][0]['rows']} "
                  f"{s['A_deepest_pairs'][0]['gap_float']:.3e} walls {s['A_least_walls']} "
                  f"wallfail {s['A_wall_failures'][:3]}")
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["cpu_seconds_total"] = round(usage.ru_utime + usage.ru_stime, 3)
    out["wall_seconds"] = round(time.time() - t0, 3)
    Path(args.out).write_text(json.dumps(out, indent=1, default=str) + "\n")
    print("cpu", out["cpu_seconds_total"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
