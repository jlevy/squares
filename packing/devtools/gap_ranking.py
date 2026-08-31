#!/usr/bin/env python3
"""Rank every open case by its verified gap: reported upper minus verified lower.

`BC-088`'s entry recorded the impression that this gap "is about 0.5 for every open
case", so ranking by it ranks nothing (D-405). Measured, the spread is a factor of ten
-- 0.056 at `n = 97` to 0.536 at `n = 51` -- and the ranking is structured: writing
`n = m^2 - k`, the gap shrinks as `k` falls and as `m` rises, so the open `k = 3` line
(61, 78, 97) and `n = 11` head the table, then the `k = 4` line. A narrow gap is not a
difficulty estimate -- Nagamochi's closed form is simply tighter relative to `m` there
-- but which stratum of the table a case occupies is what a proof-lane sequencing
decision needs, and X-010 sequences on it.

Usage, from `packing/`:
    uv run --frozen python -m devtools.gap_ranking [--limit N]
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from decimal import Decimal, localcontext
from pathlib import Path

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"

#: Matches `check_nagamochi_bounds`: enough digits to absorb any recorded decimal, and
#: pinned locally because `decimal`'s context is process-global.
DIGITS = 80

#: Label `n = m^2 - k` only while the family reading is meaningful; past this the
#: nearest perfect square stops saying anything about the case.
MAX_FAMILY_OFFSET = 6


@dataclass(frozen=True)
class OpenCase:
    n: int
    upper: Decimal
    lower: Decimal
    gap: Decimal
    method: str

    @property
    def family(self) -> str:
        root = math.isqrt(self.n)
        for m in (root, root + 1):
            k = m * m - self.n
            if 0 <= k <= MAX_FAMILY_OFFSET:
                return f"{m}^2 - {k}"
        return "-"


def open_cases() -> list[OpenCase]:
    found: list[OpenCase] = []
    for path in sorted(FRONTIER.glob("n-*.md")):
        payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        if payload.get("reported_status") != "open":
            continue
        upper = (payload.get("reported_upper_bound") or {}).get("value")
        lower = (payload.get("verified_lower_bound") or {}).get("value")
        if upper is None or lower is None:
            continue
        method = (payload.get("reported_upper_bound") or {}).get("construction_method") or "?"
        with localcontext() as context:
            context.prec = DIGITS
            upper_value = Decimal(str(upper))
            lower_value = Decimal(str(lower))
            found.append(
                OpenCase(
                    n=payload["n"],
                    upper=upper_value,
                    lower=lower_value,
                    gap=upper_value - lower_value,
                    method=method,
                )
            )
    return sorted(found, key=lambda case: case.gap)


def main() -> int:
    summary = (__doc__ or "").splitlines()[0]
    parser = argparse.ArgumentParser(description=summary)
    parser.add_argument("--limit", type=int, default=None, help="show only the first N rows")
    arguments = parser.parse_args()

    cases = open_cases()
    shown = cases if arguments.limit is None else cases[: arguments.limit]
    print(f"{len(cases)} open cases, narrowest verified gap first")
    columns = ["reported upper", "verified lower"]
    print(f"{'n':>4} {'gap':>8} {columns[0]:>16} {columns[1]:>16}  {'form':<8} method")
    for case in shown:
        integral = case.upper == case.upper.to_integral_value()
        upper = f"{case.upper:.0f}" if integral else f"{case.upper:.6f}"
        print(
            f"{case.n:>4} {case.gap:>8.4f} {upper:>16} {case.lower:>16.6f}  "
            f"{case.family:<8} {case.method}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
