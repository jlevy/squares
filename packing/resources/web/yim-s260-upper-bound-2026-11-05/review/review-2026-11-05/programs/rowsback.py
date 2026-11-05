#!/usr/bin/env python3
"""Put whole rows back where T-257 has them, in the upright variant of #895's packing.

A measurement for the review; it decides nothing about #895's bound. The base is
upright.py's variant: #895's certificate with every square turned by less than 1e-9
radians set exactly upright (t = 0), which certcheck.py accepts at #895's side. For each
row of upright squares (same ordinate within 1e-6 in T-257) that holds a square moved
beyond 0.1, every member of the row takes T-257's abscissa, measured from the left wall
or, for a member within 1e-3 of the right wall in T-257, from the right wall; ordinates
stay #895's; a member turned by more than 1e-9 radians in #895's certificate takes
T-257's tangent too. The square of the tilted island that moved beyond 0.1 (row 26) can
be put back as well (--island). Each result is decided at #895's side over every wall
and pair by certcheck.py's methods A and B.

Usage: python -I rowsback.py --yim CERT --t257 CERT --out RECEIPT.json
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certcheck as cc  # noqa: E402

mpmath.mp.dps = 50
TAN_HALF_DEGREE = F(87266, 10**7)


def theta(t: F):
    return 2 * mpmath.atan(mpmath.mpf(t.numerator) / t.denominator)


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
    sy, st = Y["side"], T["side"]
    tiny = {i for i, s in enumerate(Y["squares"]) if abs(theta(s["t"])) < mpmath.mpf("1e-9")}
    base = [dict(s, t=F(0) if i in tiny else s["t"], tokens=[]) for i, s in enumerate(Y["squares"])]
    hy, ht = sy / 2, st / 2
    big = [i for i in range(n) if float(((Y["squares"][i]["x"] - hy) - (T["squares"][i]["x"] - ht)) ** 2
                                         + ((Y["squares"][i]["y"] - hy) - (T["squares"][i]["y"] - ht)) ** 2) > 0.01]
    upright_t = [i for i in range(n) if abs(T["squares"][i]["t"]) < TAN_HALF_DEGREE
                 or abs(T["squares"][i]["t"] - 1) < TAN_HALF_DEGREE]
    rows = {}
    for i in big:
        if i not in upright_t:
            continue
        yi = T["squares"][i]["y"]
        key = round(float(yi), 6)
        rows.setdefault(key, sorted(j for j in upright_t if abs(float(T["squares"][j]["y"] - yi)) < 1e-6))
    island = [i for i in big if i not in upright_t]
    out: dict = {"program": "rowsback.py", "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 "certcheck_sha256": cc.program_digest(), "python": platform.python_version(),
                 "inputs": {"yim": Y["sha256"], "t257": T["sha256"]},
                 "movers_beyond_0.1": [i + 1 for i in big], "rows": {str(k): [j + 1 for j in v] for k, v in rows.items()},
                 "movers_not_in_an_upright_row": [i + 1 for i in island], "variants": {}}

    def put_back(members, full=()):
        sq = [dict(s) for s in base]
        for j in members:
            xt = T["squares"][j]["x"]
            x = xt - (st - sy) if xt + F(1, 2) > st - F(1, 1000) else xt
            sq[j] = dict(sq[j], x=x)
            if j not in tiny:
                sq[j] = dict(sq[j], t=T["squares"][j]["t"])
        for j in full:
            b = T["squares"][j]
            sq[j] = dict(sq[j], x=b["x"] - ht + hy, y=b["y"] - ht + hy, t=b["t"])
        return {"n": n, "side": sy, "squares": sq}

    variants = [("each row alone", None)]
    variants.append(("every such row together", "all"))
    variants.append(("every such row together, and the island square at its T-257 pose", "all+island"))
    for label, mode in variants:
        if mode is None:
            for key, members in rows.items():
                res = cc.decide(put_back(members), "ccw", "AB")
                rec = {"accepted_by_A": res["accepted_by_A"], "accepted_by_B": res["accepted_by_B"],
                       "methods_agree_on_pairs": res["methods_agree_on_pairs"],
                       "A_overlapping_pairs": res["A"]["overlapping_pairs"][:10],
                       "A_wall_failures": res["A"]["wall_failures"][:6],
                       "least_pair": res["A"]["least_pairs"][0]}
                out["variants"][f"row y={key}"] = rec
                print(f"row y={key} ({len(members)} squares): A {rec['accepted_by_A']} B {rec['accepted_by_B']} "
                      f"overlaps {rec['A_overlapping_pairs'][:4]} walls {rec['A_wall_failures'][:2]} "
                      f"least {rec['least_pair']['rows']} {rec['least_pair']['gap_float']:.3e}")
            continue
        members = sorted({j for v in rows.values() for j in v})
        res = cc.decide(put_back(members, island if mode == "all+island" else ()), "ccw", "AB")
        rec = {"squares_put_back": len(members) + (len(island) if mode == "all+island" else 0),
               "accepted_by_A": res["accepted_by_A"], "accepted_by_B": res["accepted_by_B"],
               "methods_agree_on_pairs": res["methods_agree_on_pairs"],
               "methods_agree_on_walls": res["methods_agree_on_walls"],
               "A_overlapping_pairs": res["A"]["overlapping_pairs"][:10],
               "A_wall_failures": res["A"]["wall_failures"][:6], "least_pairs": res["A"]["least_pairs"][:3],
               "walls": {k: v["least_float"] for k, v in res["A"]["walls"].items()},
               "cpu_seconds": res["A"]["cpu_seconds"] + res["B"]["cpu_seconds"]}
        out["variants"][label] = rec
        print(f"{label}: {rec['squares_put_back']} squares: A {rec['accepted_by_A']} B {rec['accepted_by_B']} "
              f"overlaps {rec['A_overlapping_pairs'][:6]} walls {rec['A_wall_failures'][:3]} least "
              f"{rec['least_pairs'][0]['rows']} {rec['least_pairs'][0]['gap_float']:.3e}")
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["cpu_seconds_total"] = round(usage.ru_utime + usage.ru_stime, 3)
    out["wall_seconds"] = round(time.time() - t0, 3)
    Path(args.out).write_text(json.dumps(out, indent=1, default=str) + "\n")
    print("cpu", out["cpu_seconds_total"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
