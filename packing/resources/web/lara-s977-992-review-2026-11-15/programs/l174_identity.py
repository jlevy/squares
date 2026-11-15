"""Lane L174, after the freeze: K0 as a subset of the Göbel-type files, square for square.

Usage: ``python -I -B l174_identity.py K0.json G985.json G982.json OUT.json``

Compares exact poses (centre pair in Q(sqrt 2), angle, side) as sets.  Decides nothing
geometric.  Reports which of K0's squares are in G985 (Göbel's (16, 21) taken literally),
which of G985's are not in K0, and the same for G982 (Göbel's (15, 21) with an L-border),
where K0 is also tried translated by (-1, -1) and (0, 0) since G982's inner square sits at
(1, 1).
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path


def poses(path: Path, shift: Fraction = Fraction(0)) -> dict[tuple, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[tuple, str] = {}
    for s in data["squares"]:
        key = (
            Fraction(s["cx"][0]) + shift,
            Fraction(s["cx"][1]),
            Fraction(s["cy"][0]) + shift,
            Fraction(s["cy"][1]),
            int(s["angle"]),
            Fraction(s["size"]),
        )
        out[key] = s["label"]
    return out


def main(argv: list[str]) -> int:
    k0, g985, g982 = (Path(a) for a in argv[1:4])
    a, b = poses(k0), poses(g985)
    c = poses(g982)
    out = {
        "K0_in_G985": sum(1 for k in a if k in b),
        "K0_not_in_G985": sorted(a[k] for k in a if k not in b),
        "G985_not_in_K0": sorted(b[k] for k in b if k not in a),
        "K0_in_G982": sum(1 for k in a if k in c),
        "K0_not_in_G982_count": sum(1 for k in a if k not in c),
        "K0_diamond_in_G982": sum(1 for k, lab in a.items() if lab.startswith("D(") and k in c),
    }
    Path(argv[4]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
