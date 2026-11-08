"""Driver for decide_bins: decide a list or a range of net bins, optionally one
shard of a range, and append one compact JSON record per bin.

decide_bins.py is used unchanged (its digest was recorded before the producer's
checker sources were read); this file only does plumbing.

Usage:
  python -I run_bins.py CERT N_NET OUT.jsonl --bins-file FILE [--exact-angles]
  python -I run_bins.py CERT N_NET OUT.jsonl --range LO HI [--shard I --shards S]

Bins already present in OUT.jsonl are skipped, so a stopped run resumes.
"""

import argparse
import json
import math
import os
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decide_bins as db  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("net", type=int)
    ap.add_argument("out")
    ap.add_argument("--bins-file")
    ap.add_argument("--range", nargs=2, type=int)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--shards", type=int, default=1)
    ap.add_argument("--max-depth", type=int, default=8)
    ap.add_argument("--exact-angles", action="store_true")
    args = ap.parse_args()

    if args.bins_file:
        bins = [int(v) for v in open(args.bins_file).read().split()]
    else:
        lo, hi = args.range
        bins = [k for k in range(lo, hi + 1) if k % args.shards == args.shard]
    done = set()
    if os.path.exists(args.out):
        for line in open(args.out):
            if line.strip():
                done.add(json.loads(line)["bin"])
    side, d, w, pts = db.read_certificate(args.cert)
    with open(args.out, "a") as out:
        for k in bins:
            if k in done:
                continue
            t0 = time.process_time()
            t_lo, t_hi = Fraction(k, args.net), Fraction(k + 1, args.net)
            log = []
            ok, m = db.decide_interval(pts, side, d, w, t_lo, t_hi, 0, args.max_depth, log)
            rec = {
                "bin": k,
                "decided": ok,
                "min_over_leaves": m,
                "root_core_min": log[0]["core_min"],
                "nodes": len(log),
                "max_depth_used": max(r["depth"] for r in log),
                "root_witness_centre": (log[0].get("witness") or {}).get("centre_float"),
            }
            if args.exact_angles:
                ex = {}
                for name, t in (("lo", t_lo), ("mid", (t_lo + t_hi) / 2), ("hi", t_hi)):
                    mm, info = db.exact_angle_min(pts, side, d, t)
                    ex[name] = mm
                rec["exact_angle_min"] = ex
            rec["cpu_s"] = round(time.process_time() - t0, 3)
            out.write(json.dumps(rec) + "\n")
            out.flush()
    print(json.dumps({"bins_requested": len(bins), "skipped_already_done": len(done & set(bins))}))


if __name__ == "__main__":
    main()
