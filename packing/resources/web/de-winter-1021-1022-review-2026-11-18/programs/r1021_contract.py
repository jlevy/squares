"""Option D's quantities for lane r1021-1118, exactly.

A certificate is shrunk by scaling every centre by one factor lambda about the
origin, each square keeping its size and angle.  A pair keeps disjoint interiors
exactly while lambda >= f, its contact factor H / max_w |d . w| (r1021_geom), so the
squares first touch at lambda* = max f over all pairs.  The shrunk side is the side
of the smallest square box holding the shrunk packing, the larger of its width and
height; the contraction margin is the certificate's side less the shrunk side.  It is
the box's slack at scale 1 (side less extent) plus what the contraction closes.

The owner's option D (think-b0w5, 17 November 2026): a successor is a new result over
its predecessor only if its side is below the predecessor's shrunk side.  The test is
one comparison of two exact fractions.
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this packet's programs/, run with -I

from fractions import Fraction

import r1021_geom as geom


def contraction(poses, side: Fraction) -> dict:
    ints = [geom.int_pose(p) for p in poses]
    factors = geom.contact_factors(ints)
    pairs = geom.pair_index(len(poses))
    best = None
    for f in factors:
        if f is None:
            raise ValueError("coincident centres")
        if best is None or f[0] * best[1] > best[0] * f[1]:
            best = f
    lam = Fraction(best[0], best[1])
    binding = [pairs[k] for k, f in enumerate(factors) if f[0] * best[1] == best[0] * f[1]]
    below = [Fraction(f[0], f[1]) for f in factors if f[0] * best[1] < best[0] * f[1]]
    next_factor = max(below) if below else None
    e = [geom.half_extent(p) for p in poses]
    xlo = min(lam * p[0] - h for p, h in zip(poses, e, strict=True))
    xhi = max(lam * p[0] + h for p, h in zip(poses, e, strict=True))
    ylo = min(lam * p[1] - h for p, h in zip(poses, e, strict=True))
    yhi = max(lam * p[1] + h for p, h in zip(poses, e, strict=True))
    width, height = xhi - xlo, yhi - ylo
    shrunk = max(width, height)
    xs_lo = min(p[0] - h for p, h in zip(poses, e, strict=True))
    xs_hi = max(p[0] + h for p, h in zip(poses, e, strict=True))
    ys_lo = min(p[1] - h for p, h in zip(poses, e, strict=True))
    ys_hi = max(p[1] + h for p, h in zip(poses, e, strict=True))
    extent = max(xs_hi - xs_lo, ys_hi - ys_lo)
    shrunk_poses = [(lam * p[0] - xlo, lam * p[1] - ylo, p[2], p[3]) for p in poses]
    return {
        "lambda": lam,
        "one_less_lambda": 1 - lam,
        "binding": binding,
        "next_factor": next_factor,
        "factors": factors,
        "shrunk_side": shrunk,
        "shrunk_width": width,
        "shrunk_height": height,
        "margin": side - shrunk,
        "slack": side - extent,
        "closed_by_contraction": extent - shrunk,
        "shrunk_poses": shrunk_poses,
        "offset": (xlo, ylo),
    }


def option_d(pred_side: Fraction, pred_contr: dict, succ_side: Fraction) -> dict:
    gain = pred_side - succ_side
    margin = pred_contr["margin"]
    below = pred_contr["shrunk_side"] - succ_side
    return {
        "gain": gain,
        "predecessor_margin": margin,
        "gain_over_margin": (gain / margin) if margin else None,
        "successor_below_shrunk_predecessor_by": below,
        "new_under_option_d": succ_side < pred_contr["shrunk_side"],
    }
