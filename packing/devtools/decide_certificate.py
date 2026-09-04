#!/usr/bin/env python3
"""Decide a certificate file by both routes, and refuse it unless both accept.

This is the retention gate. A rung joins the record only when the bytes on disk
-- not an object in memory, not a lane's report -- are accepted by the exact
event-cell sweep and by the interval branch and bound. The two routes share the
certificate and theorem contract but decide C4 by different methods with different
failure modes. Reading the file back is half the point: a
generator that rewrites its own output between verification and retention has
happened here, turning 1032 atoms into 1121 under a path someone was about to
read.

The two routes are also asked to agree on the number, not merely on the verdict.
In minimisation mode the interval run encloses the least covered mass, and that
enclosure must have width zero and equal the sweep's value exactly; a verdict
that agreed while the values differed would mean one of them is deciding a
different object.

Usage:
    uv run --frozen python -m devtools.decide_certificate <path>...
    uv run --frozen python -m devtools.decide_certificate --quick <path>...

``--quick`` runs only the interval route, which is minutes faster on a large
certificate and is enough to reject a candidate. It is never enough to retain
one, and the tool says so in its own output rather than leaving the reader to
remember.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Never, cast

from sqpack.fractional.certificate import (
    Certificate,
    ceiling_side,
    least_size_certified,
    verify,
)
from sqpack.fractional.interval import verify_by_intervals
from sqpack.fractional.model import Atom

RATIONAL = re.compile(r"^-?[0-9]+(/[1-9][0-9]*)?$")


class CertificateFormatError(ValueError):
    """The JSON cannot be interpreted as an exact certificate record."""


def _object_without_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    record: dict[str, object] = {}
    for key, value in pairs:
        if key in record:
            raise CertificateFormatError(f"duplicate JSON object key {key!r}")
        record[key] = value
    return record


def _reject_inexact_json_number(text: str) -> Never:
    raise CertificateFormatError(
        f"inexact JSON number {text!r}; use an exact rational string"
    )


def _required(record: dict[str, object], key: str) -> object:
    if key not in record:
        raise CertificateFormatError(f"missing required field {key!r}")
    return record[key]


def _exact_integer(record: dict[str, object], key: str) -> int:
    value = _required(record, key)
    # bool is an int subclass, and int(...) would also accept strings and truncate floats.
    if type(value) is not int:
        raise CertificateFormatError(
            f"field {key!r} must be a JSON integer, got {value!r}"
        )
    return cast(int, value)


def _exact_string(record: dict[str, object], key: str) -> str:
    value = _required(record, key)
    if not isinstance(value, str):
        raise CertificateFormatError(f"field {key!r} must be a string, got {value!r}")
    return value


def _rational(value: object, *, field: str) -> Fraction:
    if not isinstance(value, str) or RATIONAL.fullmatch(value) is None:
        raise CertificateFormatError(
            f"field {field!r} must be an exact rational string, got {value!r}"
        )
    return Fraction(value)


def _exact_rational(record: dict[str, object], key: str) -> Fraction:
    return _rational(_required(record, key), field=key)


def load(path: Path) -> tuple[Certificate, dict[str, object]]:
    """Rebuild a certificate from a record's own bytes, trusting none of its summary."""

    try:
        decoded = cast(
            object,
            json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=_object_without_duplicate_keys,
                parse_float=_reject_inexact_json_number,
                parse_constant=_reject_inexact_json_number,
            ),
        )
    except CertificateFormatError:
        raise
    except (UnicodeError, ValueError, RecursionError) as error:
        raise CertificateFormatError(str(error)) from None
    if not isinstance(decoded, dict):
        raise CertificateFormatError("top-level JSON value must be an object")
    record = cast(dict[str, object], decoded)

    n = _exact_integer(record, "n")
    steps = _exact_integer(record, "direction_steps")
    if steps < 1:
        raise CertificateFormatError("field 'direction_steps' must be at least 1")
    limit = _exact_rational(record, "angle_limit")
    outer_side = _exact_rational(record, "outer_side")
    square_side = _exact_rational(record, "square_side")
    _exact_string(record, "id")
    _exact_string(record, "claim")
    _exact_rational(record, "total_mass")
    symmetry = _exact_string(record, "symmetry")
    if "least_cell_mass" in record:
        _exact_rational(record, "least_cell_mass")

    atoms_record = _required(record, "atoms")
    if not isinstance(atoms_record, list):
        raise CertificateFormatError("field 'atoms' must be a JSON array")
    atoms: list[Atom] = []
    for index, atom_record in enumerate(atoms_record):
        if not isinstance(atom_record, list) or len(atom_record) != 3:
            raise CertificateFormatError(
                f"atoms[{index}] must be a three-element JSON array"
            )
        x, y, weight = (
            _rational(value, field=f"atoms[{index}][{coordinate}]")
            for coordinate, value in enumerate(atom_record)
        )
        atoms.append(Atom(f"{index:04d}", x, y, weight))

    try:
        certificate = Certificate(
            n=n,
            outer_side=outer_side,
            square_side=square_side,
            atoms=tuple(atoms),
            half_tangents=tuple(limit * k / steps for k in range(steps + 1)),
            symmetry=symmetry,
        )
    except ValueError as error:
        raise CertificateFormatError(f"invalid certificate precondition: {error}") from None
    return certificate, record


def _print_refusals(problems: list[str]) -> bool:
    for problem in problems:
        print(f"  REFUSED: {problem}", flush=True)
    return False


def decide(path: Path, *, quick: bool) -> bool:
    try:
        certificate, record = load(path)
    except (CertificateFormatError, OSError) as error:
        print(f"{path.name}: REFUSED: cannot load certificate: {error}", flush=True)
        return False
    mass = certificate.total_mass
    side = certificate.outer_side
    print(
        f"{path.name}: n = {certificate.n}, L = {side} = {float(side):.6f}, "
        f"{len(certificate.atoms)} atoms, mass {mass} = {float(mass):.6f}",
        flush=True,
    )

    problems: list[str] = []
    expected_claim = f"s({certificate.n}) >= {side}"
    declared_claim = _exact_string(record, "claim")
    if declared_claim != expected_claim:
        problems.append(
            f"declared claim {declared_claim!r} != theorem conclusion {expected_claim!r}"
        )
    declared_mass = _exact_rational(record, "total_mass")
    if declared_mass != mass:
        problems.append(f"declared total_mass {declared_mass} != recomputed {mass}")
    declared_least: Fraction | None = None
    if not quick:
        try:
            declared_least = _exact_rational(record, "least_cell_mass")
        except CertificateFormatError as error:
            problems.append(str(error))
    ceiling = ceiling_side(certificate.n, certificate.square_side)
    if side > ceiling:
        problems.append(f"side {side} is above the ceiling {ceiling} = ceil(sqrt(n)) * B")
    reach = least_size_certified(mass)
    print(f"  ceiling {float(ceiling):.6f}, certifies every n >= {reach}", flush=True)
    if reach > certificate.n:
        problems.append(f"mass {mass} does not fall below the declared n = {certificate.n}")

    if problems:
        return _print_refusals(problems)

    start = time.time()
    interval = verify_by_intervals(certificate, enclose=True)
    boxes = sum(outcome.boxes for outcome in interval.directions)
    stalled = sum(outcome.stalled for outcome in interval.directions)
    enclosure = interval.enclosure
    print(
        f"  interval accepted={interval.accepted} enclosure={enclosure} "
        f"boxes={boxes} stalled={stalled} ({time.time() - start:.0f}s)",
        flush=True,
    )
    if not interval.accepted:
        problems.append(f"the interval route refused it: {interval.failures}")
    if stalled:
        problems.append(f"{stalled} boxes stalled; the interval route decided nothing there")
    if not quick:
        if enclosure is None:
            problems.append("the interval route returned no enclosure to compare")
        elif enclosure[0] != enclosure[1]:
            problems.append(f"the enclosure has width: {enclosure}")

    if problems:
        return _print_refusals(problems)
    if quick:
        print(
            "  the interval route accepts. NOT ENOUGH TO RETAIN: run without --quick.",
            flush=True,
        )
        return True

    start = time.time()
    exact = verify(certificate)
    print(
        f"  exact    accepted={exact.accepted} least={exact.minimum_cell_mass} "
        f"({time.time() - start:.0f}s)",
        flush=True,
    )
    if not exact.accepted:
        problems.append(f"the exact sweep refused it: {exact.failures}")
    if exact.minimum_cell_mass is None:
        problems.append("the exact sweep returned no least covered mass")
    elif enclosure is not None and enclosure[0] != exact.minimum_cell_mass:
        problems.append(
            f"the two routes disagree on the least covered mass: "
            f"{exact.minimum_cell_mass} against {enclosure[0]}"
        )
    if declared_least != exact.minimum_cell_mass:
        problems.append(
            f"declared least_cell_mass {declared_least} != {exact.minimum_cell_mass}"
        )
    if problems:
        return _print_refusals(problems)
    print(
        f"  RETAINABLE: both routes accept and agree at {exact.minimum_cell_mass}",
        flush=True,
    )
    return True


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument(
        "--quick", action="store_true", help="interval route only; cannot retain"
    )
    args = parser.parse_args(argv)
    ok = True
    for path in args.paths:
        ok = decide(path, quick=args.quick) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
