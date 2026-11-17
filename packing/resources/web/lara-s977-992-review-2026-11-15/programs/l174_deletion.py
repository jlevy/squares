"""Lane L174, after the freeze: what s(977) <= 17 + 21/sqrt 2 implies by deletion.

Usage (from ``packing/``): ``python -I -B l174_deletion.py OUT.json``

Decides nothing about #992, and records nothing: deletion bounds are think-kzme's.  For
every count m from 325 to 982 it takes the standing side as the least of the current
beyond-horizon row in ``frontier/source-coverage.yaml`` (any disposition but
``superseded`` or ``above-classical-construction``), Göbel's construction
(``devtools.goebel_construction.side``) and the grid ceil(sqrt m), and lists the counts
where it exceeds L = 17 + 21/sqrt 2 (40-digit decimal sqrt 2).  Counts at or below 977
are those #992 bounds by deletion; 978 to 982 are those Göbel's (15, 21) with one
L-border bounds (G982).
"""

from __future__ import annotations

import json
import math
import sys
from decimal import Decimal, getcontext
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

import yaml  # noqa: E402

from devtools import goebel_construction as goebel  # noqa: E402

getcontext().prec = 40
ROOT2 = Decimal(2).sqrt()
L = 17 + Decimal(21) / 2 * ROOT2


def gval(form: goebel.Form) -> Decimal:
    return Decimal(form.p.numerator) / form.p.denominator + (
        Decimal(form.q.numerator) / form.q.denominator
    ) * ROOT2


def main(argv: list[str]) -> int:
    data = yaml.safe_load(Path("frontier/source-coverage.yaml").read_text(encoding="utf-8"))
    rows: dict[int, tuple[Decimal, str]] = {}
    for r in data["beyond_horizon_claims"]:
        if r.get("disposition") in {"superseded", "above-classical-construction"}:
            continue
        v = Decimal(str(r["value"]))
        m = int(r["n"])
        if m not in rows or v < rows[m][0]:
            rows[m] = (v, str(r["source_id"]))
    above: list[dict[str, str]] = []
    standing: dict[str, dict[str, str]] = {}
    for m in range(325, 983):
        cands = [(gval(goebel.side(m)), "Göbel " + goebel.side(m).text())]
        grid = math.isqrt(m - 1) + 1
        cands.append((Decimal(grid), f"grid {grid}"))
        if m in rows:
            cands.append((rows[m][0], "row " + rows[m][1]))
        best = min(cands, key=lambda c: c[0])
        if m >= 970:
            standing[str(m)] = {"side": f"{best[0]:.12f}", "by": best[1], "minus_L": f"{best[0] - L:.3E}"}
        if best[0] > L:
            above.append({"n": str(m), "side": f"{best[0]:.12f}", "by": best[1]})
    out = {"L": f"{L:.15f}", "counts_with_standing_side_above_L": above, "standing_970_982": standing}
    Path(argv[1]).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
