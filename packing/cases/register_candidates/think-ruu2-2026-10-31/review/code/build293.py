"""Write the 293 construction as certificate files, then read them back and decide them.

Usage: python3.14 build293.py INPUTS_DIR OUT_DIR

Copies the 260 rows of s260_1028.cert verbatim (their text, not a re-encoding), appends
the 33 strip rows `x y 0`, and writes `n293-s260-plus-L-<variant>.cert` with the header
`293 S+1`. Each file is then read back with qio and decided on both routes, so the file
on disk, not only the in-memory build, is what passes.
"""

from __future__ import annotations

import hashlib
import sys
from fractions import Fraction
from pathlib import Path

import qio
import route_area
import route_sat


def frac_text(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main() -> None:
    inp, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    src = (inp / "s260_1028.cert").read_text(encoding="utf-8").splitlines()
    data = [ln for ln in src if ln.strip() and not ln.lstrip().startswith("#")]
    n260, s_text = data[0].split()
    assert n260 == "260" and len(data) == 261
    s = qio.rational(s_text)
    src_sha = hashlib.sha256((inp / "s260_1028.cert").read_bytes()).hexdigest()
    for variant in ("17top+16", "16+16+1"):
        strip = qio.l_strip(s, variant)
        lines = [
            "# exact certificate: unit squares, centre (x, y), rotation (c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2));"
            f" the 260 rows of s260_1028.cert (sha256 {src_sha}) verbatim, then an L strip of 33 axis-aligned"
            f" squares ({variant}) in [S,S+1]x[0,S+1] U [0,S+1]x[S,S+1], S the 260 side; built by the stage 4"
            " review of think-ruu2",
            f"293 {frac_text(s + 1)}",
            *data[1:],
            *(f"{frac_text(x)} {frac_text(y)} 0" for x, y, _, _ in strip),
        ]
        path = outdir / f"n293-s260-plus-L-{variant}.cert"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        n, side, sq, _ = qio.read_tcert(path)
        a = route_sat.check(side, sq)["accepted"]
        b = route_area.check(side, sq)["accepted"]
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{path.name}: n={n} side={side} sha256={sha} route A {a} route B {b}")


if __name__ == "__main__":
    main()
