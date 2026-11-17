"""Decide the house witness at 179 with the frozen methods, after the freeze.

Usage: python -I -B l101_house.py HOUSE.yaml OUT.json

The house is a center-basis rational witness; each square becomes corners
c - (b + b_perp)/2, then + b, + b_perp, with b its exact basis (cos, sin). The frozen
l101_check.decide then decides every square, wall and pair. A touching pair whose centres
differ along its separating axis leaves no uniform-contraction margin: scaling the centres
by any lambda < 1 closes that gap.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.set_int_max_str_digits(0)

import yaml  # noqa: E402

import l101_geom as geom  # noqa: E402
from l101_check import decide, sha256_file, summarize  # noqa: E402


def main() -> int:
    house, out = Path(sys.argv[1]), Path(sys.argv[2])
    w = yaml.safe_load(house.read_text(encoding="utf-8"))["witness"]
    assert w["representation"] == "center-basis" and w["scalar"]["kind"] == "rational"
    assert w["coordinates"]["origin"] == "lower-left"
    side = F(str(w["side"]))
    squares = []
    for k, sq in enumerate(w["squares"]):
        assert sq["id"] == k + 1
        cx, cy = (F(str(v)) for v in sq["center"])
        c, s = (F(str(v)) for v in sq["basis"])
        p0 = (cx - (c - s) / 2, cy - (s + c) / 2)
        squares.append(geom.square_from(p0, (c, s), 1))
    r = decide((side.numerator, side.denominator), squares, keep_margins=True)
    receipt = {
        "program": "l101_house.py",
        "house_sha256": sha256_file(house),
        "house_id": w["id"],
        "n": len(squares),
        **{k: v for k, v in summarize(r).items() if k not in {"wall_clearances", "near_pairs_exact"}},
        "near_pairs_count": sum(1 for m, _, _ in r["margins"] if m < F(1, 10**12)),
    }
    out.write_text(json.dumps(receipt, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(receipt["verdict"], "touching", receipt["touching_pairs"], "walls", len(receipt["wall_contacts"]),
          "least", receipt.get("least_pair_margin", {}).get("approx"), "below", receipt.get("pairs_below"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
