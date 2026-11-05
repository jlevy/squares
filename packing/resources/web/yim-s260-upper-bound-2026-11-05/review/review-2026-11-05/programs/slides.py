#!/usr/bin/env python3
"""Slide the large movers back: does #895's side need the moves beyond a tenth?

A measurement for the review. The pairing is row for row. For each square of #895's
packing that moved beyond --tau from T-257's pose (box-centred), it moves the square
back toward T-257's pose in #895's box and decides the result exactly at #895's side:

- `x-only`: the square takes T-257's box-centred abscissa, keeping #895's ordinate and
  tangent (the moves are along rows);
- `full`: the square takes T-257's box-centred centre and tangent.

Each square is tried alone (only its own walls and its 259 pairs change, and those are
decided by certcheck.py's methods A and B), then every square for which the x-only
slide is accepted alone is slid back together and the whole packing is decided over
every wall and pair by both methods. The same is done forward in T-257's packing (each
square taking #895's abscissa at T-257's side). It also prints, for each horizontal
row of upright squares holding a mover, the squares in x order with their abscissae
and the gaps between neighbours in both packings.

Usage: python -I slides.py --yim CERT --t257 CERT --out RECEIPT.json [--tau 0.1]
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

ONE_DEGREE_T = F(87266, 10**7)  # tan(0.5 degree) ~ 0.0087266: |t| below this is within 1 degree


def with_rows(cert, changes):
    squares = [dict(s) for s in cert["squares"]]
    for i, (x, y, t) in changes.items():
        squares[i] = {"row": i + 1, "line": i + 3, "x": x, "y": y, "t": t, "tokens": []}
    return {"n": cert["n"], "side": cert["side"], "squares": squares}


def decide_local(cert, i):
    """Decide square i's walls and its pairs by both methods (the other pairs are unchanged)."""
    n = cert["n"]
    pairs = [(min(i, j), max(i, j)) for j in range(n) if j != i]
    res = cc.decide(cert, "ccw", "AB", pairs)
    a_wall_ok = all(min(w) >= 0 for w in [res["_walls"][i]])
    gaps = res["_gaps"]
    least = min(gaps.values())
    b = res["B"]
    # B's wall verdict covers every square; the others are unchanged and were inside
    return {
        "A": a_wall_ok and res["A"]["pairs_accepted"],
        "B": b["pairs_accepted"] and not any(f[0] == i + 1 for f in b["wall_failures"]) and (i + 1) not in b["own_area_not_one"],
        "least_pair_gap": float(least),
        "least_wall": float(min(res["_walls"][i])),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yim", required=True)
    ap.add_argument("--t257", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tau", type=float, default=0.1)
    args = ap.parse_args(argv)
    t0 = time.time()
    Y = cc.parse_cert(args.yim)
    T = cc.parse_cert(args.t257)
    hy, ht = Y["side"] / 2, T["side"] / 2
    n = Y["n"]
    movers = []
    for i in range(n):
        a, b = Y["squares"][i], T["squares"][i]
        dx = (a["x"] - hy) - (b["x"] - ht)
        dy = (a["y"] - hy) - (b["y"] - ht)
        if float(dx) ** 2 + float(dy) ** 2 > args.tau**2:
            movers.append(i)
    out: dict = {"program": "slides.py", "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 "certcheck_sha256": cc.program_digest(), "python": platform.python_version(),
                 "inputs": {"yim": Y["sha256"], "t257": T["sha256"]}, "tau": args.tau,
                 "movers": [i + 1 for i in movers], "alone": []}
    back_ok_x = []
    fwd_ok_x = []
    for i in movers:
        a, b = Y["squares"][i], T["squares"][i]
        x_back = b["x"] - ht + hy
        y_back = b["y"] - ht + hy
        x_fwd = a["x"] - hy + ht
        rec = {"row": i + 1}
        rec["back_x_only"] = decide_local(with_rows(Y, {i: (x_back, a["y"], a["t"])}), i)
        rec["back_full"] = decide_local(with_rows(Y, {i: (x_back, y_back, b["t"])}), i)
        rec["forward_x_only"] = decide_local(with_rows(T, {i: (x_fwd, b["y"], b["t"])}), i)
        out["alone"].append(rec)
        if rec["back_x_only"]["A"] and rec["back_x_only"]["B"]:
            back_ok_x.append(i)
        if rec["forward_x_only"]["A"] and rec["forward_x_only"]["B"]:
            fwd_ok_x.append(i)
        print(f"row {i + 1:3d}: back x-only A {rec['back_x_only']['A']} B {rec['back_x_only']['B']} "
              f"gap {rec['back_x_only']['least_pair_gap']:+.3e} wall {rec['back_x_only']['least_wall']:+.3e} | "
              f"back full A {rec['back_full']['A']} gap {rec['back_full']['least_pair_gap']:+.3e} "
              f"wall {rec['back_full']['least_wall']:+.3e} | fwd x-only A {rec['forward_x_only']['A']} "
              f"gap {rec['forward_x_only']['least_pair_gap']:+.3e}")
    # all accepted x-only slides together, decided over every wall and pair
    together = with_rows(Y, {i: (T["squares"][i]["x"] - ht + hy, Y["squares"][i]["y"], Y["squares"][i]["t"])
                             for i in back_ok_x})
    res = cc.decide(together, "ccw", "AB")
    out["back_x_only_together"] = {
        "rows": [i + 1 for i in back_ok_x], "accepted_by_A": res["accepted_by_A"], "accepted_by_B": res["accepted_by_B"],
        "methods_agree_on_pairs": res["methods_agree_on_pairs"], "least_pairs": res["A"]["least_pairs"][:5],
        "overlapping_pairs": res["A"]["overlapping_pairs"][:20],
        "walls": {k: v["least_float"] for k, v in res["A"]["walls"].items()},
    }
    together_f = with_rows(T, {i: (Y["squares"][i]["x"] - hy + ht, T["squares"][i]["y"], T["squares"][i]["t"])
                               for i in fwd_ok_x})
    res_f = cc.decide(together_f, "ccw", "AB")
    out["forward_x_only_together"] = {
        "rows": [i + 1 for i in fwd_ok_x], "accepted_by_A": res_f["accepted_by_A"], "accepted_by_B": res_f["accepted_by_B"],
        "methods_agree_on_pairs": res_f["methods_agree_on_pairs"], "least_pairs": res_f["A"]["least_pairs"][:5],
        "overlapping_pairs": res_f["A"]["overlapping_pairs"][:20],
    }
    print("back together:", out["back_x_only_together"]["accepted_by_A"], out["back_x_only_together"]["accepted_by_B"],
          len(back_ok_x), out["back_x_only_together"]["least_pairs"][:2], out["back_x_only_together"]["overlapping_pairs"][:6])
    print("forward together:", out["forward_x_only_together"]["accepted_by_A"], out["forward_x_only_together"]["accepted_by_B"],
          len(fwd_ok_x), out["forward_x_only_together"]["overlapping_pairs"][:6])

    # rows of upright squares holding a mover: abscissae and neighbour gaps in both packings
    rows_report = []
    upright = [i for i in range(n) if abs(T["squares"][i]["t"]) < ONE_DEGREE_T or abs(T["squares"][i]["t"] - 1) < ONE_DEGREE_T]
    seen = set()
    for i in movers:
        yi = float(T["squares"][i]["y"])
        key = round(yi, 6)
        if key in seen or i not in upright:
            continue
        seen.add(key)
        members = sorted((j for j in upright if abs(float(T["squares"][j]["y"]) - yi) < 1e-6),
                         key=lambda j: T["squares"][j]["x"])
        line = []
        for k, j in enumerate(members):
            xt = float(T["squares"][j]["x"])
            xy = float(Y["squares"][j]["x"] - hy + ht)
            gt = float(T["squares"][members[k + 1]]["x"] - T["squares"][j]["x"] - 1) if k + 1 < len(members) else None
            gy = float(Y["squares"][members[k + 1]]["x"] - Y["squares"][j]["x"] - 1) if k + 1 < len(members) else None
            line.append({"row": j + 1, "x_t257": xt, "x_yim_in_t257_box": xy, "gap_next_t257": gt, "gap_next_yim": gy,
                         "mover": j in movers})
        rows_report.append({"y_t257": yi, "squares": line})
    out["upright_rows_with_movers"] = rows_report
    for r in rows_report:
        print(f"y={r['y_t257']:.6f}: " + " ".join(
            f"{s['row']}{'*' if s['mover'] else ''}@{s['x_t257']:.3f}->{s['x_yim_in_t257_box']:.3f}" for s in r["squares"]))
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["cpu_seconds_total"] = round(usage.ru_utime + usage.ru_stime, 3)
    out["wall_seconds"] = round(time.time() - t0, 3)
    Path(args.out).write_text(json.dumps(out, indent=1, default=str) + "\n")
    print("cpu", out["cpu_seconds_total"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
