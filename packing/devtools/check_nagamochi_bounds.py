#!/usr/bin/env python3
"""Re-derive every lower bound the register attributes to [Nagamochi 2005].

`E-nagamochi-lower` supplies the verified lower bound for 86 of the hundred frontier
cases (88 until 2026-08-31, when the first-party green17 certificate took over `n = 17`
and `n = 18`). The next most-cited evidence record carries two. Nothing checked that the
recorded values were what the theorem gives: `assurance.py` verifies that a bound cites
verified evidence of the right claim and scope, which is a statement about the citation
and not about the arithmetic. A transcription slip in any one of the 86 would have
passed.

Theorem 2, as the evidence record states it and as re-derived here from Theorem 1
(`nu(a, b) < ab - (a + 1 - ceil(a)) - (b + 1 - ceil(b))` for `a, b >= 2`):

- `N` in `{m^2, m^2 - 1, m^2 - 2}` gives `s(N) >= m`. Put `a = b = m` in Theorem 1: it
  yields `nu(m, m) < m^2 - 2`, so `m^2 - 2` unit squares already do not fit strictly
  inside side `m`.
- otherwise `s(N) >= sqrt(N - 2k + 1) + 1` with `k = floor(sqrt(N))`. Put `a = b = k + t`
  and choose `t` so that `(k + t)^2 - 2t = N`; then `k + t` is the bound.

The two collapse to `min(ceil(sqrt(N)), sqrt(N - 2*floor(sqrt(N)) + 1) + 1)`, and this
checks that form against the record rather than assuming it.

Also checks the direction that would be a soundness defect rather than a bookkeeping one:
a lower bound may never exceed the reported upper bound for the same `n`.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_nagamochi_bounds
"""

from __future__ import annotations

import math
import sys
from decimal import Decimal, localcontext
from pathlib import Path

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
RECORD = "E-nagamochi-lower"

#: Enough to compare against any decimal the register carries, and pinned rather than
#: inherited: `decimal`'s context is process-global (see `think-iskp`).
DIGITS = 80


def theorem_two(n: int) -> tuple[Decimal, bool]:
    """The bound Theorem 2 gives for `n`, and whether `n` is one of its exact cases."""
    root = math.isqrt(n)
    exact = any(n == m * m - offset for m in (root, root + 1) for offset in (0, 1, 2))
    with localcontext() as context:
        context.prec = DIGITS
        if exact:
            return Decimal(math.isqrt(n - 1) + 1), True
        return Decimal(n - 2 * root + 1).sqrt() + 1, False


def cases() -> dict[int, dict]:
    found = {}
    for path in sorted(FRONTIER.glob("n-*.md")):
        payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        found[payload["n"]] = payload
    return found


def main() -> int:
    problems: list[str] = []
    checked = 0
    inversions: list[str] = []

    for n, case in sorted(cases().items()):
        lower = case.get("verified_lower_bound") or {}
        if RECORD not in (lower.get("evidence") or []):
            continue
        checked += 1

        expected, is_exact = theorem_two(n)
        recorded = Decimal(str(lower["value"]))
        with localcontext() as context:
            context.prec = DIGITS
            # The record may carry fewer digits than the theorem's value has; it must be a
            # correct rendering of it, not merely close, so compare at the record's places.
            # `exponent` is only an int for a finite Decimal, and a bound that is NaN or
            # infinite is a malformed record rather than a disagreement, so say which.
            exponent = recorded.as_tuple().exponent
            if not isinstance(exponent, int):
                problems.append(
                    f"n={n}: recorded lower bound {recorded} is not a finite number"
                )
                continue
            places = -exponent
            if abs(expected - recorded) > Decimal(1).scaleb(-places):
                problems.append(
                    f"n={n}: record says {recorded}, Theorem 2 gives {expected:.{places + 2}f}"
                )
            if is_exact and recorded != recorded.to_integral_value():
                problems.append(f"n={n}: an exact case should carry an integer, not {recorded}")

        reported = case.get("reported_upper_bound") or {}
        if (upper := reported.get("value")) is not None and recorded > Decimal(str(upper)):
            inversions.append(f"n={n}: lower {recorded} exceeds reported upper {upper}")

    if inversions:
        print("SOUNDNESS: a lower bound exceeds the upper bound it sits under:")
        for line in inversions:
            print(f"  {line}")
        return 1
    if problems:
        print(f"{len(problems)} of {checked} Nagamochi-derived bounds disagree with Theorem 2:")
        for line in problems:
            print(f"  {line}")
        return 1

    print(f"{checked} lower bounds re-derived from Theorem 2, all agreeing, none inverted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
