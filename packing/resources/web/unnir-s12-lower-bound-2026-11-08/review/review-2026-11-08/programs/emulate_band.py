"""The producer's core (Daniel's endpoint sigma_k and centre box, rounded down to 1e-6)
over a range of bins, computed by this lane's own sweep (controls.producer_core_min).

Written in the reconcile phase, after the blind findings were frozen and after the
producer's Rust source had been read.  Decides nothing about the bound: it measures where
Daniel's core, without his f64 padding of the V-range, reaches exactly W.

Usage: python -I emulate_band.py CERT K_LO K_HI
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import controls  # noqa: E402
import decide_bins as db  # noqa: E402


def main():
    side, d, w, pts = db.read_certificate(sys.argv[1])
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    res = {}
    for k in range(lo, hi + 1):
        m, info = controls.producer_core_min(pts, side, d, k)
        res[k] = m - w
    at0 = [k for k, v in res.items() if v == 0]
    print(json.dumps({
        "bins": [lo, hi],
        "margins": res,
        "bins_at_margin_0": at0,
        "least_margin": min(res.values()),
    }, indent=1))


if __name__ == "__main__":
    main()
