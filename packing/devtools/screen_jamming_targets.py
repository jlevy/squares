#!/usr/bin/env python3
"""Report how jammed the packings a cold search has to reach actually are.

Every inflation, compression and event-driven packing method in the physics literature
stops at a *jam*: it grows the particles until no particle can move, and reports that
state. Whether that termination rule can ever emit a best-known square packing is a
question about the targets, not about the algorithm, and the repository already holds
the answer key in `atlas/known-best/translation-escape-screen.json`.

This joins that screen against the frontier case files and reports, for the cases a
cold search is actually asked to find -- the ones whose best known packing beats the
`ceil(sqrt(n))` grid -- how many squares the screen finds movable, how many can be
pushed clear of everything they touch, and how much slack the container has.

Usage, from `packing/`:
    uv run --frozen python -m devtools.screen_jamming_targets
    uv run --frozen python -m devtools.screen_jamming_targets --max-n 100 --json

A movable square is not automatically a rattler: the screen's own note records that
every square in every retained record touches something, so most movable squares slide
tangentially with a contact staying closed rather than floating in a hole. Separating
squares are the subset that can be pushed clear. Read the two columns as an upper and a
lower bound on how much a jamming criterion would have to tolerate.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
SCREEN = ROOT / "atlas/known-best/translation-escape-screen.json"


@dataclass(frozen=True)
class Target:
    """One case whose best known packing beats the trivial grid, joined to the screen."""

    n: int
    upper: Decimal
    grid: int
    method: str
    screened: bool
    squares: int
    movable: int
    separating: int
    slack: Decimal

    @property
    def margin(self) -> Decimal:
        return Decimal(self.grid) - self.upper


def non_grid_cases(max_n: int) -> list[tuple[int, Decimal, int, str]]:
    """The cases at `n <= max_n` whose reported upper bound beats the trivial grid."""
    found: list[tuple[int, Decimal, int, str]] = []
    for path in sorted(FRONTIER.glob("n-*.md")):
        payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        n = int(payload["n"])
        if n > max_n:
            continue
        bound = payload.get("reported_upper_bound") or {}
        value = bound.get("value")
        if value is None:
            continue
        grid = math.ceil(math.sqrt(n))
        upper = Decimal(str(value))
        if upper >= grid:
            continue
        found.append((n, upper, grid, bound.get("construction_method") or "unknown"))
    return found


def targets(max_n: int) -> list[Target]:
    """Join the non-grid cases against the translation-escape screen."""
    screen = json.loads(SCREEN.read_text(encoding="utf-8"))["screen"]
    by_n: dict[int, dict[str, Any]] = {int(case["n"]): case for case in screen["cases"]}
    rows: list[Target] = []
    for n, upper, grid, method in non_grid_cases(max_n):
        case = by_n.get(n)
        rows.append(
            Target(
                n=n,
                upper=upper,
                grid=grid,
                method=method,
                screened=case is not None,
                squares=int(case["square_count"]) if case else 0,
                movable=int(case["movable_square_count"]) if case else 0,
                separating=int(case["separating_square_count"]) if case else 0,
                slack=abs(Decimal(case["min_container_slack"])) if case else Decimal(0),
            )
        )
    return rows


def summarize(rows: list[Target]) -> dict[str, Any]:
    """The four numbers the report quotes, plus the cases that carry them."""
    screened = [row for row in rows if row.screened]
    immobile = [row.n for row in screened if row.movable == 0]
    return {
        "cases": len(rows),
        "screened": len(screened),
        "excluded": [row.n for row in rows if not row.screened],
        "with_movable_square": sum(1 for row in screened if row.movable > 0),
        "movable_squares": sum(row.movable for row in screened),
        "separating_squares": sum(row.separating for row in screened),
        "fully_immobile": immobile,
        "max_container_slack": str(max((row.slack for row in screened), default=Decimal(0))),
    }


def main(argv: list[str] | None = None) -> int:
    summary_line = (__doc__ or "").splitlines()[0]
    parser = argparse.ArgumentParser(description=summary_line)
    parser.add_argument("--max-n", type=int, default=100, help="highest case to report")
    parser.add_argument("--json", action="store_true", help="emit the rows as JSON")
    options = parser.parse_args(argv)

    rows = targets(options.max_n)
    stats = summarize(rows)
    if options.json:
        payload = [row.__dict__ | {"slack": str(row.slack)} for row in rows]
        print(json.dumps({"summary": stats, "rows": payload}, default=str, sort_keys=True))
        return 0

    print(f"non-grid best-known packings at n <= {options.max_n}: {stats['cases']}")
    print(f"{'n':>4} {'upper':>12} {'margin':>8} {'sq':>4} {'movable':>8} {'clear':>6} method")
    for row in rows:
        if not row.screened:
            print(
                f"{row.n:>4} {row.upper:>12.6f} {row.margin:>8.4f} "
                f"{'-':>4} {'excluded':>8} {'-':>6} {row.method}"
            )
            continue
        print(
            f"{row.n:>4} {row.upper:>12.6f} {row.margin:>8.4f} {row.squares:>4} "
            f"{row.movable:>8} {row.separating:>6} {row.method}"
        )
    print(
        f"screened {stats['screened']}, "
        f"with at least one movable square {stats['with_movable_square']}, "
        f"movable squares {stats['movable_squares']}, "
        f"of which pushed clear {stats['separating_squares']}"
    )
    print(f"no movable square at all: n = {stats['fully_immobile']}")
    print(f"largest container slack among them: {stats['max_container_slack']}")
    if stats["excluded"]:
        print(f"excluded by the screen's shape-residual limit: n = {stats['excluded']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
