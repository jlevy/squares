"""Small exact endpoint checks for X-045; no search or certificate replay.

Run from the repository root with the project Python 3.14 and
PYTHONPATH=packing:packing/src. The imported exact witness/field and archived
certificate must match the recorded Git revision byte for byte.
"""

from __future__ import annotations

import argparse
import inspect
import json
import platform
import shlex
import signal
import subprocess
import sys
import time
from datetime import UTC, datetime
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

from cases.trump11 import packing as trump
from sqpack import field as exact_field

SOURCES = (
    "packing/cases/trump11/packing.py",
    "packing/src/sqpack/field.py",
    (
        "packing/resources/web/external-square-certificates-2026-09-22/"
        "kleddamag-11/global-certificate.json"
    ),
)


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=15)
    args = parser.parse_args()
    if not 1 <= args.seconds <= 15:
        parser.error("the declared ceiling is between one and fifteen seconds")
    if args.output.exists():
        parser.error("refusing to overwrite a retained receipt")
    if sys.version_info[:2] != (3, 14):
        parser.error("use the project Python 3.14")
    start = time.monotonic()

    def deadline(_signum: int, _frame: object) -> None:
        raise TimeoutError("declared fifteen-second maximum exceeded")

    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(args.seconds)
    repo = args.repo.resolve()
    commit = git(repo, "rev-parse", args.commit).decode().strip()
    frozen = {path: git(repo, "show", f"{commit}:{path}") for path in SOURCES}
    for path, content in frozen.items():
        if (repo / path).read_bytes() != content:
            raise RuntimeError(f"input differs from its recorded Git revision: {path}")
    if Path(inspect.getfile(trump)).resolve() != repo / SOURCES[0]:
        raise RuntimeError("imported witness belongs to a different checkout")
    if Path(inspect.getfile(exact_field)).resolve() != repo / SOURCES[1]:
        raise RuntimeError("imported number field belongs to a different checkout")

    squares, side, field = trump.build()
    rational = field.rational
    zero = field.zero
    field.refine_to(32)

    def describe(value: exact_field.FieldElement) -> dict[str, object]:
        lo, hi = field.enclose(value)
        midpoint = (lo + hi) / 2
        with localcontext() as context:
            context.prec = 28
            approximation = format(
                Decimal(midpoint.numerator) / Decimal(midpoint.denominator), "f"
            )
        return {
            "coefficients_in_u_low_to_high": [str(q) for q in value.coeffs],
            "enclosure": [str(lo), str(hi)],
            "decimal_approximation": approximation,
        }

    def coordinate_min(
        values: list[exact_field.FieldElement],
    ) -> exact_field.FieldElement:
        return min(values)

    corner_names = ("bottom_left", "bottom_right", "top_left", "top_right")
    corner_results = {}
    for name in corner_names:
        by_square = []
        for square in squares:
            values = []
            for x, y in square:
                tx = side - x if "right" in name else x
                ty = side - y if "top" in name else y
                values.append(tx + ty)
            by_square.append(coordinate_min(values))
        minimum = coordinate_min(by_square)
        corner_results[name] = {
            "minimum_penetration": describe(minimum),
            "minimizing_square_labels": [
                index for index, value in enumerate(by_square) if value == minimum
            ],
            "literal_corner_occupants": [
                index for index, value in enumerate(by_square) if value == zero
            ],
            "every_square_penetration": [describe(value) for value in by_square],
        }

    wall_results = {}
    for name in ("left", "right", "bottom", "top"):
        owners = []
        for index, square in enumerate(squares):
            gaps = []
            for x, y in square:
                gaps.append({"left": x, "right": side - x, "bottom": y, "top": side - y}[name])
            if coordinate_min(gaps) == zero:
                owners.append(index)
        wall_results[name] = owners

    source = json.loads(frozen[SOURCES[2]])
    source_side = Fraction(source["L"])
    parent_old = Fraction(source["A"])
    first_row = [Fraction(value) for value in source["entries"][0]]
    core_side = first_row[3]
    parent_at_trump = rational(source_side) / side
    # Area alone makes B <= A necessary for a square core to fit in its parent.
    fixed_row_excess = rational(core_side) - parent_at_trump
    assert fixed_row_excess.sign() > 0
    gamma = Fraction(source["minimum_units"], source["weight_denominator"])
    budget = Fraction(source["budget_units"], source["weight_denominator"])
    h131_envelope = Fraction(3_877_084, 1_000_000)
    assert (rational(h131_envelope) - side).sign() > 0
    # sqrt(2)>7/5 implies 9*eta^2>171/20 for wall-toucher spacing eta.
    # U<97/25 and (97/25-1)^2<171/20 give the exact sufficient cap.
    wall_side_bound = Fraction(97, 25)
    assert (rational(wall_side_bound) - side).sign() > 0
    wall_comparison_slack = Fraction(171, 20) - (wall_side_bound - 1) ** 2
    assert wall_comparison_slack > 0
    assert trump.side_satisfies_published_polynomial(side, field)
    assert [corner_results[name]["literal_corner_occupants"] for name in corner_names] == [
        [0],
        [1],
        [3],
        [],
    ]

    for path, content in frozen.items():
        if (repo / path).read_bytes() != content:
            raise RuntimeError(f"input changed during the audit: {path}")
    elapsed = time.monotonic() - start
    receipt = {
        "exploration": "X-045",
        "workflow": "W3",
        "question": (
            "Exact Trump corner/wall profile and unchanged first-row core transfer to U"
        ),
        "declared_wall_ceiling_seconds": args.seconds,
        "elapsed_seconds": elapsed,
        "workers": 1,
        "python": platform.python_version(),
        "utc": datetime.now(UTC).isoformat(),
        "command": "PYTHONPATH=packing:packing/src " + shlex.join([sys.executable, *sys.argv]),
        "repo": str(repo),
        "source_commit": commit,
        "source_paths": list(SOURCES),
        "source_bytes_match_commit_before_and_after": True,
        "number_field": {
            "minimal_polynomial_high_to_low": list(trump.U_MIN_POLY),
            "root_interval": list(trump.U_INTERVAL),
        },
        "trump_side": describe(side),
        "side_polynomial_verified": True,
        "corner_profile": corner_results,
        "wall_parent_labels": wall_results,
        "h131_envelope": str(h131_envelope),
        "h131_envelope_minus_U": describe(rational(h131_envelope) - side),
        "wall_cap_rational_upper_side": str(wall_side_bound),
        "wall_cap_squared_comparison_slack": str(wall_comparison_slack),
        "source_first_row": [str(value) for value in first_row],
        "source_parent_side": str(parent_old),
        "parent_side_required_at_U": describe(parent_at_trump),
        "first_frozen_core_minus_parent_at_U": describe(fixed_row_excess),
        "area_necessary_side_ceiling_for_first_frozen_core": str(source_side / core_side),
        "area_necessary_side_ceiling_decimal": str(float(source_side / core_side)),
        "source_gamma": str(gamma),
        "source_budget": str(budget),
        "source_11gamma_minus_budget": str(11 * gamma - budget),
        "limits": [
            (
                "Consumes the retained exact feasible witness; does not replay its full "
                "feasibility theorem."
            ),
            "The first-row area obstruction rejects unchanged core geometry at U only.",
            (
                "No replacement core, charge minimization, local-minimum enumeration, "
                "or capture theorem is tested."
            ),
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n")
    signal.alarm(0)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "elapsed_seconds": elapsed,
                "corner_occupants": {
                    key: value["literal_corner_occupants"]
                    for key, value in corner_results.items()
                },
                "first_row_transfer": "refuted_by_core_area",
            }
        )
    )


if __name__ == "__main__":
    main()
