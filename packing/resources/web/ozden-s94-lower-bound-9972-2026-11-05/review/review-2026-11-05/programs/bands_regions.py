"""Region bounds of the strips the dilation adds at shared nodes (decides nothing).

At a node t shared with Hosono's net (step 83/40000), Hosono's per-bin domain had margin
m0(t) = rho(max(0, t - 83/80000)) in his coordinates, which is lambda * m0(t) in the
dilated ones; the dilated certificate's margin is m(t) = rho(max(0, t - D/2)). The strip
U_old = L - lambda m0(t) <= coordinate <= U_r is new. This prints, for each node given,
binary64 regions (outward-rounded) for the top and right strips of the quadrant.

With --width W (an exact rational), the strip at any node r is instead
U_r - W <= coordinate <= U_r; the review used W = lambda * 11/9972, the axis growth in
dilated coordinates, at the new nodes nearest the axis.

Usage: bands_regions.py CERT_GZ [--width W] R [R ...]
"""

from __future__ import annotations

import sys
from pathlib import Path

from gmpy2 import mpq

from bnb import f_down, f_up
from xzcommon import direction, load_certificate, rho_half_width


def main() -> int:
    cert = load_certificate(Path(sys.argv[1]))
    args = sys.argv[2:]
    width = None
    if args and args[0] == "--width":
        width = mpq(args[1])
        args = args[2:]
    lam = mpq(4986, 4975)
    D0 = mpq(83, 40000)
    for r in (int(v) for v in args):
        dr = direction(cert, r)
        if width is not None:
            u_old = dr.U - width
        else:
            j = dr.t / D0
            assert j.denominator == 1, f"{r} is not a shared node"
            m0 = rho_half_width(max(mpq(0), dr.t - D0 / 2))
            u_old = cert.L - lam * m0
        lo, uo, hi = f_down(cert.L / 2), f_down(u_old), f_up(dr.U)
        print(f"{r} top {lo},{hi},{uo},{hi}")
        print(f"{r} right {uo},{hi},{lo},{hi}")
        print(f"# r={r} strip width {float(dr.U - u_old):.6e} (dilated coordinates)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
