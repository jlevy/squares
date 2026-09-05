#!/usr/bin/env python3
"""Measure what a coarser direction net costs the retained certificate.

Condition 4 ties the net to the shrink: with `D` the largest half-gap tangent, the
shrunken square may have side at most `1 / (1 + D)`, so a coarser net forces a
smaller `B`, and a smaller `B` covers less mass. This holds the atoms fixed,
coarsens the net, gives `B` the largest value Condition 4 then admits, and re-decides
Condition 5. The result is the slope of that trade at one point, not a claim that no
coarser certificate exists: these atoms were optimized against the full net.

The full-net row is measured on the certificate's own net and doubles as the
measurement's control. The result is retained as JSON, one file per certificate
named for its bound (`net-coarsening-381-100.json`), and the page renderer reads
that file rather than recomputing it.

Usage, from `packing/`:

    uv run --frozen python -m devtools.measure_net_coarsening
    uv run --frozen python -m devtools.measure_net_coarsening \
        --certificate cases/n11_fractional_certificate/certificate-19-5.json
"""

from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from itertools import pairwise
from pathlib import Path

from sqpack.fractional.certificate import Certificate, sweep_direction_minimum
from sqpack.fractional.model import Atom

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
CASE = PACKING / "cases" / "n11_fractional_certificate"
DEFAULT_NETS = (10, 30, 60, 90, 180)

# B is reported to this many places; the value used is the largest multiple of
# 10^-DENOM strictly below 1 / (1 + D), so Condition 4 holds with room to state it.
DENOM = 10**7


def largest_admissible_side(half_tangents: tuple[Fraction, ...]) -> tuple[Fraction, Fraction]:
    """`D` for this net, and the largest `B` on the grid that keeps `B(1+D) < 1`."""
    gap = max((right - left) / (1 + left * right) for left, right in pairwise(half_tangents))
    side = Fraction((DENOM * (1 + gap).denominator) // (1 + gap).numerator - 1, DENOM)
    assert side * (1 + gap) < 1
    return gap, side


def measure(certificate_path: Path, nets: tuple[int, ...]) -> list[dict[str, object]]:
    record = json.loads(certificate_path.read_text(encoding="utf-8"))
    limit = Fraction(record["angle_limit"])
    atoms = tuple(
        Atom(f"{index:04d}", Fraction(x), Fraction(y), Fraction(weight))
        for index, (x, y, weight) in enumerate(record["atoms"])
    )
    rows: list[dict[str, object]] = []
    for steps in nets:
        half_tangents = tuple(limit * k / steps for k in range(steps + 1))
        gap, side = largest_admissible_side(half_tangents)
        candidate = Certificate(
            n=int(record["n"]),
            outer_side=Fraction(record["outer_side"]),
            square_side=side,
            atoms=atoms,
            half_tangents=half_tangents,
            symmetry=record["symmetry"],
        )
        started = time.monotonic()
        least = min(
            sweep_direction_minimum(candidate, direction)[0]
            for direction in candidate.directions
        )
        rows.append(
            {
                "K": steps,
                "D": f"{float(gap):.7f}",
                "B": f"{float(side):.6f}",
                "least_mass": f"{float(least):.6f}",
                "least_mass_exact": str(least),
                "passes": least >= 1,
                "seconds": round(time.monotonic() - started, 1),
            }
        )
        print(
            f"K={steps:4d}  B={float(side):.6f}  least={float(least):.6f}  "
            f"{'PASS' if least >= 1 else 'FAIL'}  ({rows[-1]['seconds']}s)",
            flush=True,
        )
    return rows


def output_path(record: dict[str, object]) -> Path:
    """Where a certificate's measurement is retained: named for its bound, as the
    page renderer expects (`net-coarsening-381-100.json`)."""
    side = Fraction(str(record["outer_side"]))
    return CASE / f"net-coarsening-{side.numerator}-{side.denominator}.json"


def repository_relative(path: Path, role: str) -> str:
    """The path as the record states it; a path outside the repository is refused
    before any sweep runs, since the record cannot name it."""
    try:
        return path.relative_to(REPO).as_posix()
    except ValueError:
        raise SystemExit(f"the {role} {path} is not inside the repository") from None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=CASE / "certificate.json")
    parser.add_argument(
        "--output",
        type=Path,
        help="where to write the rows (default: beside the certificate, named for its bound)",
    )
    parser.add_argument("--nets", type=int, nargs="+", default=list(DEFAULT_NETS))
    args = parser.parse_args(argv)

    # Paths are resolved and checked first: a relative `--certificate` used to
    # pass the whole measurement and fail on `relative_to` at the write.
    certificate = args.certificate.resolve()
    record = json.loads(certificate.read_text(encoding="utf-8"))
    output = args.output.resolve() if args.output else output_path(record)
    payload: dict[str, object] = {
        "certificate": repository_relative(certificate, "certificate"),
        "certificate_id": record["id"],
    }
    output_label = repository_relative(output, "output")

    payload["rows"] = measure(certificate, tuple(args.nets))
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output_label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
