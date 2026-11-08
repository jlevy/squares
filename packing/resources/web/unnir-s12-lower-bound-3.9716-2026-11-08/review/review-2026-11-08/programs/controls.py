"""Controls for the L58 decider on the real certificate.

(a) point removal: at a bin whose exact minimum is W, remove the heaviest point
    captured at the minimising centre (and its D4 orbit); the decider must then
    refuse the bin, and the exact-angle mode must produce a brute-force-checked
    centre capturing less than W -- a genuine counterexample for the mutant.
(b) side + 1/D: enlarge the container by one coordinate unit (points unchanged)
    and re-decide the tight band; says whether the minimum touches a wall.
(c) producer-shrink emulation: the minimum of the producer's core (reference at
    the endpoint theta_k, side sigma_k = 1/(cos d + sin d) rounded down to 1e-6,
    centre box from min(cos+sin) over the endpoints rounded down to 1e-6), but
    computed by this program's own sweep.  The producer's Rust log reports the
    global minimum W at k = 39531, the smallest such k; so the emulation must
    give > W below 39531 and exactly W at 39531.  (The Rust also pads its domain
    in V by about 2 coordinate units; the emulation does not, so it can only be
    higher, never lower, than the Rust's value.)

Usage: python -I controls.py CERT
"""

import json
import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decide_bins as db  # noqa: E402

N = 96000


def orbit(x, y, S):
    return {(x, y), (S - x, y), (x, S - y), (S - x, S - y), (y, x), (S - y, x), (y, S - x), (S - y, S - x)}


def producer_core_min(pts, side, d, k):
    NN = N * N
    c0, s0, g0 = NN - k * k, 2 * k * N, NN + k * k
    k2 = k + 1
    c1, s1, g1 = NN - k2 * k2, 2 * k2 * N, NN + k2 * k2
    cd, sd = c0 * c1 + s0 * s1, c0 * s1 - s0 * c1
    sg = Fraction((g0 * g1 * 10**6) // (cd + sd), 10**6)
    wm = Fraction(min(((c0 + s0) * 10**6) // g0, ((c1 + s1) * 10**6) // g1), 10**6)
    return db.min_capture(pts, side, d, Fraction(k, N), sg / 2, wm / 2)


def main():
    side, d, w, pts = db.read_certificate(sys.argv[1])
    S = int(side * d)
    out = {}

    # (a) point removal at bin 39535 (exact minimum W at all three exact angles)
    k = 39535
    t = Fraction(2 * k + 1, 2 * N)
    m, info = db.exact_angle_min(pts, side, d, t)
    cx, cy = info["witness"]["centre_float"]
    cn, sn, Q = db.rotation_of_t(t)
    # recompute the captured set at the witness exactly (closed unit square)
    # the witness is only reported in floats, so re-locate it on the exact grid:
    # use the float centre, which lies deep inside its open cell for this check
    X0, Y0 = Fraction(cx) * d, Fraction(cy) * d
    A = Q * d // 2
    U0, V0 = cn * X0 + sn * Y0, -sn * X0 + cn * Y0
    cap = [(x, y, wt) for x, y, wt in pts if abs(cn * x + sn * y - U0) <= A and abs(-sn * x + cn * y - V0) <= A]
    heavy = max(cap, key=lambda p: p[2])
    orb = orbit(heavy[0], heavy[1], S)
    mutant = [p for p in pts if (p[0], p[1]) not in orb]
    log = []
    ok, mm = db.decide_interval(mutant, side, d, w, Fraction(k, N), Fraction(k + 1, N), 0, 2, log)
    em, einfo = db.exact_angle_min(mutant, side, d, t)
    out["a_point_removal"] = {
        "bin": k, "original_exact_mid_min": m, "captured_at_witness": sum(p[2] for p in cap),
        "removed_point": heavy, "removed_orbit_size": len(orb),
        "mutant_decided": ok, "mutant_min_over_leaves": mm,
        "mutant_exact_mid_min": em, "mutant_witness": einfo.get("witness"),
        "refused_as_required": (not ok) and em < w,
    }

    # (b) side + 1/D, bins of the tight band
    side2 = side + Fraction(1, d)
    res = {}
    for kk in (39520, 39531, 39535, 39540, 39545):
        log = []
        ok2, m2 = db.decide_interval(pts, side2, d, w, Fraction(kk, N), Fraction(kk + 1, N), 0, 0, log)
        res[kk] = m2 - w
    out["b_side_plus_1_over_D_root_core_margin"] = res

    # (c) producer-shrink emulation
    emu = {}
    for kk in list(range(39518, 39533)) + [0, 8000, 39764]:
        m3, info3 = producer_core_min(pts, side, d, kk)
        emu[kk] = {"margin": m3 - w, "centre": (info3.get("witness") or {}).get("centre_float")}
    out["c_producer_shrink_emulation"] = emu
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
