#!/usr/bin/env python3
"""Goebel's family reaches twelve sizes below 100 and is optimal at four of them.

`D-389` records this project pricing a route to an exact `n = 40` construction while the
construction sat published in a source the repository had already transcribed. The
correction was specific to `n = 40`. This asks the general question the correction implies:
**which sizes does that family reach, and where is what it gives already the best known?**

Goebel's rule, as `[Friedman DS7]` states it: for integers `a, b` with
`a - 1 < b / sqrt(2) < a + 1`, exactly `2a^2 + 2a + b^2` unit squares pack into a square of
side `a + 1 + b / sqrt(2)`, by setting a `b` by `b` block at forty-five degrees in the
middle of a frame `a` squares deep.

Twelve `(a, b)` pairs reach an `n` at most 100. At four of them the side is *exactly* the
best known this repository retains: `n = 5`, `40`, `65` and `89`. Two of those already have
exact constructions here. **The other two do not** -- `n = 65` and `n = 89` retain
`numerical-multiprecision` witnesses and no case package, and this tool builds and verifies
both exactly in seconds.

The near miss is the interesting one. At `a = 2, b = 4` the family gives `n = 28` in side
`3 + 2 sqrt(2) = 5.8284...`, and the best known is `5.8244...` -- better by `0.0040`, at
algebraic degree 6. So `n = 28`'s optimum is *not* in this family, which is why no exact
construction is retained for it and why the answer for `n = 40` does not carry over. That
is worth having written down: it forecloses the obvious next guess.

Nothing here is promoted. The constructions are verified feasible at the retained side, not
shown optimal, and moving `n = 65` or `n = 89` to an exact witness is a change to those
records that this tool only makes possible.

Usage:
    uv run --frozen python -m devtools.price_gobel_family
    uv run --frozen python -m devtools.price_gobel_family --check
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from typing import Any

from strif import atomic_output_file

from cases.gobel40.packing import corners, overlaps
from sqpack.field import NumberField
from sqpack.verify import exact_sign, verify_packing
from sqpack.yamlio import safe_load

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
RESULTS = ROOT / "campaign" / "series" / "series-000-smoke-and-calibration" / "results"
OUT = RESULTS / "bc-049-gobel-family-coverage.json"

CEILING = 100
"""The frontier's own horizon: records run n = 1 to 100, so the family is asked no further."""

AGREEMENT = 1e-11
"""How close the family's side must sit to a retained value to count as the same number.

The retained values are decimals of about fifteen digits, so this is a comparison at their
precision and not a tolerance on the mathematics. Where it fires, the record separately
carries an `exact_form` in `Q(sqrt 2)` that matches the family's side symbolically, which
is what actually settles it.
"""


def build(a: int, b: int):
    """Goebel's construction at `(a, b)`: exact corners, side, and the field.

    The generalization of `cases/gobel40`, which is this at `a = 3, b = 4`. The block sits
    centred in the container and the frame is the `2a` by `2a` lattice of wall-hugging
    positions minus the ones the block occupies -- computed by the same exact overlap test
    rather than transcribed, so a wrong `(a, b)` produces a wrong count rather than a
    plausible picture.
    """
    field = NumberField((1, 0, -2), (1, 2))
    root = field.alpha
    q = field.rational
    half = q(1) / q(2)
    diagonal = root / q(4)
    side = q(a + 1) + q(b) * root / q(2)
    centre = side / q(2)

    tilted = []
    for u in range(b):
        for v in range(b):
            cx = centre + q(2 * (u + v) - 2 * (b - 1)) * root / q(4)
            cy = centre + q(2 * (v - u)) * root / q(4)
            tilted.append(corners((cx, cy), (diagonal, diagonal), (-diagonal, diagonal)))

    offsets = [q(2 * k + 1) / q(2) for k in range(a)]
    offsets += [side - value for value in offsets]
    axis = [
        square
        for cx in offsets
        for cy in offsets
        for square in [corners((cx, cy), (half, q(0)), (q(0), half))]
        if not any(overlaps(square, block) for block in tilted)
    ]
    return axis + tilted, side, field


def parameters() -> list[tuple[int, int]]:
    """Every `(a, b)` satisfying Goebel's condition and reaching `n <= CEILING`."""
    found = []
    for a in range(1, CEILING):
        for b in range(1, CEILING):
            if not (a - 1 < b / math.sqrt(2) < a + 1):
                continue
            if 2 * a * a + 2 * a + b * b <= CEILING:
                found.append((a, b))
    return sorted(found, key=lambda pair: 2 * pair[0] ** 2 + 2 * pair[0] + pair[1] ** 2)


def retained() -> dict[int, dict[str, Any]]:
    """The best known side and its exact form, per size, from the frontier records."""
    table: dict[int, dict[str, Any]] = {}
    for path in sorted(FRONTIER.glob("n-*.md")):
        payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
        packing = payload["packing"]
        table[int(packing["n"])] = {
            "value": float(packing["reported_upper_bound"]["value"]),
            "exact_form": packing["reported_upper_bound"].get("exact_form"),
            "algebraic_degree": packing["reported_upper_bound"].get("algebraic_degree"),
        }
    return table


BUILT_HERE = [5, 40, 65, 89]
"""The sizes whose exact construction this repository holds.

`n = 5` and `n = 40` have their own case packages; `n = 65` and `n = 89` are built by
`cases/gobel_family`, which session-046 added. This was a literal `[5, 40]` until then,
and stayed a literal for one session after -- long enough for the record to print "exact
and unbuilt at [65, 89]" about two constructions the gate was already running. See
`D-398`, which is the same staleness in the frontier records.
"""


def assess() -> dict[str, Any]:
    table = retained()
    rows: list[dict[str, Any]] = []
    for a, b in parameters():
        n = 2 * a * a + 2 * a + b * b
        side = a + 1 + b / math.sqrt(2)
        known = table.get(n)
        row: dict[str, Any] = {
            "n": n,
            "a": a,
            "b": b,
            "side": f"{a + 1} + {b}/sqrt(2)",
            "side_value": round(side, 12),
            "best_known": known["value"] if known else None,
            "matches_best_known": bool(known and abs(side - known["value"]) < AGREEMENT),
        }
        if known and not row["matches_best_known"]:
            row["worse_by"] = round(side - known["value"], 12)
            row["best_known_degree"] = known["algebraic_degree"]
        if row["matches_best_known"]:
            squares, exact_side, _field = build(a, b)
            report = verify_packing(squares, exact_side, sign=exact_sign)
            row["verified"] = {
                "squares": report.n,
                "pairs_tested": report.pairs_tested,
                "valid": report.valid,
            }
        rows.append(row)

    optimal = [row for row in rows if row["matches_best_known"]]
    return {
        "schema_version": 1,
        "subject": {
            "commitment": "BC-049",
            "question": (
                "which sizes Goebel's centred-diagonal-block family reaches below n = 100, "
                "and where what it gives is already the best known"
            ),
            "why": (
                "D-389 recorded this project pricing a route to an exact n = 40 pose while "
                "the construction sat published in a source already transcribed here. That "
                "correction was specific to n = 40; this asks the question it implies"
            ),
            "promotes_nothing": (
                "the constructions are verified feasible at the retained side, not shown "
                "optimal. Moving n = 65 or n = 89 to an exact witness is a change to those "
                "records that this only makes possible"
            ),
        },
        "family": rows,
        "reached": len(rows),
        "optimal_at": [row["n"] for row in optimal],
        "already_built_here": BUILT_HERE,
        "buildable_and_not_built": [row["n"] for row in optimal if row["n"] not in BUILT_HERE],
        "the_near_miss": {
            "n": 28,
            "family_side": "3 + 4/sqrt(2) = 5.828427...",
            "best_known": "5.824444...",
            "worse_by": 0.003982,
            "why_it_matters": (
                "n = 28's optimum is at algebraic degree 6 and is not in this family, so "
                "the n = 40 answer does not carry over to it. That is why no exact "
                "construction is retained there, and it forecloses the obvious next guess"
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="compare against the retained record"
    )
    args = parser.parse_args()

    built = assess()
    if args.check:
        if not OUT.exists():
            print(f"  {OUT.name} is missing", file=sys.stderr)
            return 1
        if json.loads(OUT.read_text(encoding="utf-8")) != built:
            print(f"  {OUT.name} has drifted from a fresh assessment", file=sys.stderr)
            return 1
        print(
            f"  Goebel family reproduces: {built['reached']} sizes below {CEILING}, "
            f"optimal at {built['optimal_at']}, "
            f"exact and unbuilt at {built['buildable_and_not_built']}"
        )
        return 0

    with atomic_output_file(OUT) as tmp:
        tmp.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
