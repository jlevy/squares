"""The certificate's own squares contracted uniformly, decided exactly by the frozen checker.

Lane L108, blind stage 4 review of jlevy/squares#959. Written after the findings were
frozen. For a rational mu < 1, each square keeps its shape and its centre c moves to
mu * c (every corner p becomes p - (1 - mu) c); the packing is then translated so that
its least corner coordinates are 0, and the side is its greatest corner coordinate.
Both methods decide the result over every square, wall and pair. This measures the
certificate's slack; it registers nothing and claims nothing for the author.

Usage: python -I -B l108_contract.py CERT.yaml CERT.json REPO_ROOT OUT.json DEFICIT [DEFICIT ...]
       (each DEFICIT is 1 - mu, written as a fraction or decimal string)
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l108_check as check  # noqa: E402
import l108_reader as reader  # noqa: E402
import l108_wit as wit  # noqa: E402

mpmath.mp.dps = 60


def contract(cert: reader.Certificate, deficit: Fraction) -> reader.Certificate:
    pts = [[(Fraction(*x), Fraction(*y)) for x, y in raw] for raw in cert.squares]
    moved = []
    for p in pts:
        cx, cy = (p[0][0] + p[2][0]) / 2, (p[0][1] + p[2][1]) / 2
        moved.append([(x - deficit * cx, y - deficit * cy) for x, y in p])
    x0 = min(x for p in moved for x, _y in p)
    y0 = min(y for p in moved for _x, y in p)
    moved = [[(x - x0, y - y0) for x, y in p] for p in moved]
    side = max(max(x, y) for p in moved for x, y in p)
    squares = tuple(tuple(((x.numerator, x.denominator), (y.numerator, y.denominator)) for x, y in p) for p in moved)
    return reader.Certificate(n=cert.n, side=(side.numerator, side.denominator), squares=squares, tree={})  # type: ignore[arg-type]


def main(argv: list[str]) -> int:
    cert = reader.read_paths(Path(argv[1]), Path(argv[2]))
    s70 = wit.load(Path(argv[3]) / "packing/witnesses/known-best/n-070.yaml", "n-070").side
    nevska = mpmath.mpf("13.880960371556")
    rows: list[dict[str, Any]] = []
    for text in argv[5:]:
        deficit = Fraction(text)
        mod = contract(cert, deficit)
        res = check.decide(mod)
        side = Fraction(*mod.side)
        smp = mpmath.mpf(side.numerator) / side.denominator
        rows.append(
            {
                "deficit": text,
                "verdict": res["verdict"],
                "side_20": mpmath.nstr(smp, 20),
                "side_ceil_12": f"{-((-side.numerator * 10**12) // side.denominator) / 10**12:.12f}",
                "side_less_s70_plus_5": mpmath.nstr(smp - s70 - 5, 6),
                "side_less_nevska": mpmath.nstr(smp - nevska, 6),
                "certificate_side_less_this_side": check.dec(Fraction(*cert.side) - side, 6),
                "least_margin": {k: v for k, v in res.get("least_margin", {}).items() if k != "exact"},
                "touching_pairs": res.get("touching_pairs"),
                "overlapping_pair_count": res.get("overlapping_pair_count"),
                "wall_contacts": res.get("wall_contacts"),
                "walls_outside": res.get("walls_outside"),
                "pair_disagreements": res.get("pair_disagreements"),
                "wall_disagreements": res.get("wall_disagreements"),
            }
        )
        print(rows[-1]["deficit"], rows[-1]["verdict"], rows[-1]["side_20"], rows[-1]["least_margin"], flush=True)
    out = {"program": "l108_contract.py", "decider_sha256": check.program_digests(), "rows": rows}
    Path(argv[4]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
