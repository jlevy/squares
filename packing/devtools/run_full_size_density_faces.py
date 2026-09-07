"""Produce bounded complete-face receipts for an explicitly selected fixed family.

The exp-113 mode is a target and requires a separately frozen experiment. Neither
the 120-second implementation ceiling nor a successful toy control authorizes it.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from fractions import Fraction
from typing import Any

from devtools.check_full_size_density_faces import (
    SEMANTICS,
    add_mode_arguments,
    bounded_child,
    bounded_worker,
    candidate_invariants,
    explicit_source,
    validate_timeout,
)
from devtools.check_full_size_density_pair_separator import (
    CANDIDATE_WEIGHTS,
    bind_parent,
    control_family,
    family_signature,
)
from devtools.check_full_size_density_support_ceiling import load_packet, load_source
from devtools.density_face_verifier import verify_density
from sqpack.full_size_density.pair_separator import PairFamily, make_family
from sqpack.full_size_density.support_ceiling import SupportError
from sqpack.full_size_density.support_screen import bind_source, support_metadata


def source_family(*, control: str | None, parent: Any) -> PairFamily:
    """Use iterative D4 for source families; the reader reconstructs direct D4."""
    if control is not None and control != "trump-uniform-control-v1":
        return control_family(control)
    seeds, side = load_source("trump11-v1")
    bound = bind_source(seeds, side)
    if control is None:
        bind_parent(parent, support_metadata(bound))
        orbit_weights = CANDIDATE_WEIGHTS
    else:
        orbit_weights = tuple(
            Fraction(value) for value in support_metadata(bound)["uniform_weights"]
        )
    family = make_family(
        tuple(square for orbit in bound.support.orbits for square in orbit),
        side,
        tuple(
            weight
            for orbit, weight in zip(bound.support.orbits, orbit_weights, strict=True)
            for _ in orbit
        ),
    )
    if control is None:
        candidate_invariants(family)
    return family


def produce(*, control: str | None = None, parent: Any = None) -> dict[str, Any]:
    source = explicit_source(control, parent)
    family = source_family(control=control, parent=parent)
    checked = verify_density(
        tuple(item.square for item in family.placements),
        family.side,
        tuple(item.weight for item in family.placements),
    )
    witness = checked.witness
    if checked.maximum > 1 and witness is None:
        raise SupportError("excess maximum has no strict box")
    result: dict[str, Any] = {"kind": "complete-ae-maximum", "maximum": str(checked.maximum)}
    if witness is not None:
        result = {
            "kind": "strict-excess-box",
            "point": [
                [str(value) for value in coordinate.coeffs] for coordinate in witness.point
            ],
            "radius": str(witness.radius),
            "members": list(witness.members),
            "excess": str(witness.excess),
        }
    return {
        "version": 1,
        "source": source,
        "semantics": SEMANTICS,
        "family": family_signature(family),
        "mass": str(sum((item.weight for item in family.placements), Fraction())),
        "result": result,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_mode_arguments(parser)
    args = parser.parse_args(argv)
    validate_timeout(parser, args.timeout_seconds)
    try:
        if args.worker:
            return bounded_worker(
                lambda: produce(
                    control=args.control,
                    parent=None if args.candidate is None else load_packet(args.candidate),
                ),
                args.timeout_seconds,
            )
        arguments = ["--timeout-seconds", str(args.timeout_seconds)]
        arguments.extend(
            ["--candidate", str(args.candidate)]
            if args.candidate is not None
            else ["--control", args.control]
        )
        return bounded_child(
            "devtools.run_full_size_density_faces", arguments, args.timeout_seconds
        )
    except subprocess.TimeoutExpired, TimeoutError:
        print("unresolved: process wall cap expired", file=sys.stderr)
        return 1
    except (SupportError, OSError, ValueError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
