#!/usr/bin/env python3
"""Replay the exact grid witnesses and basic bound instantiations in the frontier.

The grid replay is a machine check of a finite rational witness.  The lower-bound
checks only confirm that each case instantiates the exact expression named by its
evidence record; the mathematical force of Nagamochi's inequality still comes from the
scoped published proof recorded in ``frontier/evidence.yaml``.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path

from sqpack.verify import Report, verify_packing
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"


def _sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def _strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _bound(case: Mapping[str, object], name: str) -> Mapping[str, object] | None:
    value = case.get(name)
    return value if isinstance(value, Mapping) else None


def build_grid(n: int) -> tuple[list[list[tuple[Fraction, Fraction]]], Fraction]:
    """Build the row-major rational grid fallback for one positive ``n``."""
    if n < 1:
        raise ValueError("n must be positive")
    root = math.isqrt(n)
    side = root if root * root == n else root + 1
    squares: list[list[tuple[Fraction, Fraction]]] = []
    for index in range(n):
        x = Fraction(index % side)
        y = Fraction(index // side)
        squares.append(
            [
                (x, y),
                (x + 1, y),
                (x + 1, y + 1),
                (x, y + 1),
            ]
        )
    return squares, Fraction(side)


def verify_grid(n: int) -> Report:
    """Verify one grid fallback with exact rational predicate evaluation."""
    squares, side = build_grid(n)
    return verify_packing(squares, side, sign=_sign)


def _nagamochi_form(n: int) -> str:
    side = math.isqrt(n)
    if side * side < n:
        side += 1
    if side * side - n <= 2:
        return str(side)
    return f"sqrt({n} - 2*floor(sqrt({n})) + 1) + 1"


def check_case_basic_bounds(case: Mapping[str, object]) -> list[str]:
    """Check the parametric exact evidence referenced by one case."""
    n = case.get("n")
    if not isinstance(n, int):
        return ["case n is missing or malformed"]
    errors: list[str] = []
    upper = _bound(case, "verified_upper_bound")
    lower = _bound(case, "verified_lower_bound")

    if upper is not None and "E-basic-grid-upper" in _strings(upper.get("evidence")):
        expected = str(math.isqrt(n) if math.isqrt(n) ** 2 == n else math.isqrt(n) + 1)
        if upper.get("exact_form") != expected or upper.get("value") != expected:
            errors.append(
                f"n={n}: grid upper bound must have exact value {expected}, "
                f"got {upper.get('exact_form')!r}"
            )
        report = verify_grid(n)
        if not report.valid or report.n != n:
            errors.append(f"n={n}: exact grid witness replay failed: {report.failures}")

    if lower is not None and "E-basic-area-lower" in _strings(lower.get("evidence")):
        expected = "1" if n == 1 else f"sqrt({n})"
        if lower.get("exact_form") != expected:
            errors.append(
                f"n={n}: area lower bound must have exact form {expected}, "
                f"got {lower.get('exact_form')!r}"
            )

    if lower is not None and "E-nagamochi-lower" in _strings(lower.get("evidence")):
        expected = _nagamochi_form(n)
        if lower.get("exact_form") != expected:
            errors.append(
                f"n={n}: Nagamochi bound must have exact form {expected}, "
                f"got {lower.get('exact_form')!r}"
            )

    if (
        lower is not None
        and "E-n012-monotonicity-lower" in _strings(lower.get("evidence"))
        and (n != 12 or lower.get("exact_form") != "2 + 4/sqrt(5)")
    ):
        errors.append("E-n012-monotonicity-lower must copy the verified n=11 bound")
    return errors


def _load_case(path: Path) -> Mapping[str, object]:
    document = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
    if not isinstance(document, Mapping) or not isinstance(document.get("packing"), Mapping):
        raise TypeError(f"{path}: malformed frontier frontmatter")
    return document["packing"]


def main() -> int:
    paths = sorted(FRONTIER.glob("n-*.md"))
    errors: list[str] = []
    grid_count = 0
    for path in paths:
        case = _load_case(path)
        upper = _bound(case, "verified_upper_bound")
        if upper is not None and "E-basic-grid-upper" in _strings(upper.get("evidence")):
            grid_count += 1
        errors.extend(f"{path.name}: {error}" for error in check_case_basic_bounds(case))
    if errors:
        print("\n".join(errors))
        return 1
    print(
        f"replayed {grid_count} exact rational grid witnesses and "
        f"checked basic bound instantiations for {len(paths)} cases"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
