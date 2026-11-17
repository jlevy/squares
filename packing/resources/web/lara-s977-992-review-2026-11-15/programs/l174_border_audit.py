"""Lane L174, after the freeze: where Friedman's L-border on Göbel's families undercuts the module.

Usage (from ``packing/``): ``python -I -B l174_border_audit.py OUT.json``

Decides nothing about #992.  For every count from 325 to 2000 it takes the least side of
any member of ``devtools.goebel_construction.families`` (to a build of 4000) carrying 0 to
3 L-border layers (side s + k, count n + sum_{j<k} (2 floor(s + j) + 1), the lemma
``devtools.construction_checker`` states), at that count or above, and compares it
exactly with the module's own side ``goebel_construction.side``.  It lists the counts where
the bordered side is strictly smaller, and every row of ``frontier/source-coverage.yaml``
``beyond_horizon_claims`` at those counts whose printed value lies at or above the
bordered side and below the module's side, by an exact comparison of the 12-place print
with p + q sqrt 2 (40-digit decimal sqrt 2, far from every tie here).
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
LOW, HIGH, BUILD = 325, 2000, 4000


def value(form: goebel.Form) -> Decimal:
    return Decimal(form.p.numerator) / form.p.denominator + (
        Decimal(form.q.numerator) / form.q.denominator
    ) * ROOT2


def main(argv: list[str]) -> int:
    extended: list[tuple[goebel.Form, str]] = []
    for f in goebel.families(BUILD):
        s_floor = int(f.p) + math.isqrt(math.floor(2 * f.q * f.q))
        n = f.count
        for k in range(4):
            extended.append(
                (goebel.Form(f.p + k, f.q, f.family, n), f"{f.family} n={f.count} {f.text()} + {k} L")
            )
            n += 2 * (s_floor + k) + 1
    extended.sort(key=lambda item: -item[0].count)
    least: dict[int, tuple[goebel.Form, str]] = {}
    best: tuple[goebel.Form, str] | None = None
    idx = 0
    for m in range(BUILD, LOW - 1, -1):
        while idx < len(extended) and extended[idx][0].count >= m:
            cand = extended[idx]
            if best is None or goebel.less(cand[0], best[0]):
                best = cand
            idx += 1
        if m <= HIGH and best is not None:
            least[m] = best
    gaps: dict[int, dict[str, object]] = {}
    for m in range(LOW, HIGH + 1):
        mod = goebel.side(m)
        bordered, label = least[m]
        if goebel.less(bordered, mod):
            gaps[m] = {
                "bordered": label,
                "bordered_side": bordered.text(),
                "bordered_value": f"{value(bordered):.12f}",
                "module_side": mod.text(),
                "module_value": f"{value(mod):.12f}",
            }
    data = yaml.safe_load(Path("frontier/source-coverage.yaml").read_text(encoding="utf-8"))
    between: list[dict[str, object]] = []
    for row in data["beyond_horizon_claims"]:
        m = int(row["n"])
        if m in gaps:
            v = Decimal(str(row["value"]))
            lo = Decimal(str(gaps[m]["bordered_value"]))
            if value(least[m][0]) <= v < value(goebel.side(m)) and lo > 0:
                between.append(
                    {
                        "n": m,
                        "value": str(row["value"]),
                        "source_id": row["source_id"],
                        "disposition": row.get("disposition"),
                    }
                )
    out = {
        "range": [LOW, HIGH],
        "counts_where_borders_undercut_module": len(gaps),
        "gaps": {str(k): v for k, v in gaps.items()},
        "rows_at_or_above_bordered_and_below_module": between,
    }
    Path(argv[1]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"counts": len(gaps), "first": list(gaps)[:40], "rows_between": between}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
