"""Write synthetic certificate files for lane r1021-1118's trials; reads no certificate.

Usage: python -I -B r1021_synth.py K DIGITS OUT_DIR

Writes a k x k packing in the two layouts the lane reads, with exact contacts so that
the contact paths are exercised: the bottom row is upright squares touching each
other and the bottom and left walls; the other rows sit on a grid of pitch 21/20
with DIGITS-digit offsets and small rational turns.  The side is the extent.

- synth_exact.json and synth_witness.yaml: a report (form J and form C, ids square-k);
- synth_house.yaml: the same packing as a house file (integer ids, claim, source and
  certificate blocks after the squares).
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this packet's programs/, run with -I

import json
import random
from fractions import Fraction

import r1021_geom as geom
import r1021_read as rd
from r1021_fmt import frac_text


def packing(k: int, digits: int, seed: int = 1021):
    rng = random.Random(seed)
    q = 10**digits
    poses = []
    for gy in range(k):
        for gx in range(k):
            if gy == 0:
                poses.append((Fraction(1, 2) + gx, Fraction(1, 2), Fraction(1), Fraction(0)))
                continue
            x = Fraction(21 * gx, 20) + Fraction(rng.randrange(q // 40), q) + Fraction(3, 5)
            y = Fraction(21 * gy, 20) + Fraction(rng.randrange(q // 40), q) + Fraction(3, 5)
            if rng.random() < 0.5:
                c, s = Fraction(1), Fraction(0)
            else:
                t = Fraction(rng.randrange(q // 1000), q)
                c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
            poses.append((x, y, c, s))
    e = [geom.half_extent(p) for p in poses]
    side = max(max(p[0] + h for p, h in zip(poses, e, strict=True)), max(p[1] + h for p, h in zip(poses, e, strict=True)))
    return poses, side


HEADER = [
    "softschema:", "  contract: packing.squares:Witness/v2", "  schema: synthetic", "  envelope: witness",
    "  status: enforced", "witness:", "  id: W-synthetic", "  n: {n}", "  side: {side}", "  square_size: '1'",
    "  representation: corners", "  scalar:", "    kind: rational", "  coordinates:", "    origin: lower-left",
    "    axes: x-right-y-up", "    angle_unit: not-applicable",
]
CLAIM = ["  claim:", "    coordinate_provenance: reported", "    method: exact-algebraic",
         "    limitations: A synthetic packing for the lane's trials."]
TRAILER = ["  source:", "    path: synthetic.yaml", "  certificate:", "    kind: exact-rational-sat", "    pairs_tested: 1"]


def corners_lines(poses, id_style):
    out = []
    for k, p in enumerate(poses, start=1):
        e = geom.corners_of(p)
        out += [f"  - id: {'square-' + str(k) if id_style == 'square-k' else k}", "    corners:"]
        for x, y in (e[2], e[3], e[0], e[1]):
            out += [f"    - - {frac_text(x)}", f"      - {frac_text(y)}"]
    return out


def main(argv: list[str]) -> int:
    k, digits, out = int(argv[0]), int(argv[1]), argv[2]
    poses, side = packing(k, digits)
    n = len(poses)
    obj = {"n": n, "side": frac_text(side), "square_size": "1", "format": rd.FORMAT_SENTENCE,
           "squares": [[frac_text(v) for v in p] for p in poses]}
    with open(_os.path.join(out, "synth_exact.json"), "w") as f:
        f.write(json.dumps(obj, indent=1) + "\n")
    head = [ln.format(n=n, side=frac_text(side)) for ln in HEADER]
    with open(_os.path.join(out, "synth_witness.yaml"), "w") as f:
        f.write("\n".join(head + CLAIM + ["  squares:"] + corners_lines(poses, "square-k")) + "\n")
    with open(_os.path.join(out, "synth_house.yaml"), "w") as f:
        f.write("\n".join(head + ["  squares:"] + corners_lines(poses, "int") + CLAIM + TRAILER) + "\n")
    print(n, "squares, side", float(side))
    return 0


if __name__ == "__main__":
    _sys.exit(main(_sys.argv[1:]))
