#!/usr/bin/env python3
"""Decide a certificate file by both routes, and refuse it unless both accept.

This is the retention gate. A rung joins the record only when the bytes on disk
-- not an object in memory, not a lane's report -- are accepted by the exact
event-cell sweep and by the interval branch and bound. The two routes share the
``Certificate`` representation and Conditions 2--4 but decide Condition 5 by different
methods with different failure modes. Reading the file back is half the point: a
generator that rewrites its own output between verification and retention has
happened here, turning 1032 atoms into 1121 under a path someone was about to
read.

The two routes are also asked to agree on the number, not merely on the verdict.
In minimisation mode the interval run encloses the least covered mass, and that
enclosure must have width zero and equal the sweep's value exactly; a verdict
that agreed while the values differed would mean one of them is deciding a
different object.

Before printing a positive full verdict, the command rereads the named path, requires
its bytes to be unchanged, and prints their SHA-256. The digest, rather than a mutable
pathname by itself, is the identity of the accepted artifact.

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
import hashlib
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
    closed_form_conditions,
    least_size_certified,
    verify,
)
from sqpack.fractional.interval import (
    MAX_INTERVAL_ATOMS,
    IntervalInputError,
    scaled_atom_masses,
    verify_by_intervals,
)
from sqpack.fractional.model import Atom

RATIONAL = re.compile(r"^-?[0-9]+(/[1-9][0-9]*)?$")
MAX_RATIONAL_TEXT = 512
MAX_DIRECTION_STEPS = 10_000
MAX_ATOMS = MAX_INTERVAL_ATOMS
MAX_CERTIFICATE_BYTES = 8 * 1024 * 1024


class CertificateFormatError(ValueError):
    """The JSON cannot be interpreted as an exact certificate record."""


class CandidateRefusalError(ValueError):
    """The named path cannot enter one of the decision routes."""


def _object_without_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    record: dict[str, object] = {}
    for key, value in pairs:
        if key in record:
            raise CertificateFormatError(f"duplicate JSON object key {key!r}")
        record[key] = value
    return record


def _reject_inexact_json_number(text: str) -> Never:
    raise CertificateFormatError(f"inexact JSON number {text!r}; use an exact rational string")


def _required(record: dict[str, object], key: str) -> object:
    if key not in record:
        raise CertificateFormatError(f"missing required field {key!r}")
    return record[key]


def _exact_integer(record: dict[str, object], key: str) -> int:
    value = _required(record, key)
    # bool is an int subclass, and int(...) would also accept strings and truncate floats.
    if type(value) is not int:
        raise CertificateFormatError(f"field {key!r} must be a JSON integer, got {value!r}")
    return cast(int, value)


def _exact_string(record: dict[str, object], key: str) -> str:
    value = _required(record, key)
    if not isinstance(value, str):
        raise CertificateFormatError(f"field {key!r} must be a string, got {value!r}")
    return value


def _rational(value: object, *, field: str) -> Fraction:
    if not isinstance(value, str):
        raise CertificateFormatError(
            f"field {field!r} must be an exact rational string, got {value!r}"
        )
    if len(value) > MAX_RATIONAL_TEXT:
        raise CertificateFormatError(
            f"field {field!r} exceeds the {MAX_RATIONAL_TEXT}-character rational limit"
        )
    if RATIONAL.fullmatch(value) is None:
        raise CertificateFormatError(
            f"field {field!r} must be an exact rational string, got {value!r}"
        )
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise CertificateFormatError(f"field {field!r}: {error}") from None


def _exact_rational(record: dict[str, object], key: str) -> Fraction:
    return _rational(_required(record, key), field=key)


def _load_bytes(data: bytes) -> tuple[Certificate, dict[str, object]]:
    """Rebuild a certificate from one frozen byte string."""
    try:
        decoded = cast(
            object,
            json.loads(
                data,
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
    if steps > MAX_DIRECTION_STEPS:
        raise CertificateFormatError(
            f"field 'direction_steps' exceeds the supported maximum {MAX_DIRECTION_STEPS}"
        )
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
    if len(atoms_record) > MAX_ATOMS:
        raise CertificateFormatError(f"field 'atoms' exceeds the supported maximum {MAX_ATOMS}")
    atoms: list[Atom] = []
    for index, atom_record in enumerate(atoms_record):
        if not isinstance(atom_record, list) or len(atom_record) != 3:
            raise CertificateFormatError(f"atoms[{index}] must be a three-element JSON array")
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


def _read_bounded(path: Path) -> bytes:
    """Read one candidate without allowing its input size to drive allocation."""

    with path.open("rb") as source:
        data = source.read(MAX_CERTIFICATE_BYTES + 1)
    if len(data) > MAX_CERTIFICATE_BYTES:
        raise CertificateFormatError(
            f"file exceeds the {MAX_CERTIFICATE_BYTES}-byte certificate limit"
        )
    return data


def load(path: Path) -> tuple[Certificate, dict[str, object]]:
    """Rebuild a certificate from a record's own bytes, trusting none of its summary."""

    return _load_bytes(_read_bounded(path))


def _approx(value: Fraction) -> str:
    """Format a diagnostic float without making float range verdict-bearing."""

    try:
        return f"{float(value):.6f}"
    except OverflowError:
        return "outside-float-range"


def _unchanged_sha256(path: Path, frozen: bytes) -> tuple[str | None, str | None]:
    """Bind a positive verdict to bytes that still occupy the named path."""

    try:
        current = _read_bounded(path)
    except (CertificateFormatError, OSError) as error:
        return None, f"cannot reread accepted path: {error}"
    if current != frozen:
        return None, "the certificate path changed while the decision was running"
    return hashlib.sha256(frozen).hexdigest(), None


def _print_refusals(path: Path, problems: list[str]) -> bool:
    for problem in problems:
        print(f"{path}: REFUSED: {problem}", flush=True)
    return False


def _prepare_candidate(
    path: Path,
) -> tuple[bytes, Certificate, dict[str, object], Fraction]:
    try:
        frozen = _read_bounded(path)
        certificate, record = _load_bytes(frozen)
    except (CertificateFormatError, OSError) as error:
        raise CandidateRefusalError(f"cannot load certificate: {error}") from None
    try:
        # This bounded linear pass protects the exact diagnostic below. The interval
        # verifier deliberately recomputes its own private input data so no mutable
        # prepared state can enter its public verdict boundary.
        scale, _, total = scaled_atom_masses(certificate)
    except IntervalInputError as error:
        raise CandidateRefusalError(f"unsupported interval input: {error}") from None
    return frozen, certificate, record, Fraction(total, scale)


def decide(path: Path, *, quick: bool) -> bool:
    try:
        frozen, certificate, record, mass = _prepare_candidate(path)
    except CandidateRefusalError as error:
        print(f"{path}: REFUSED: {error}", flush=True)
        return False
    side = certificate.outer_side
    print(
        f"{path}: n = {certificate.n}, L = {side} = {_approx(side)}, "
        f"{len(certificate.atoms)} atoms, mass {mass} = {_approx(mass)}",
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
    print(f"  ceiling {_approx(ceiling)}, certifies every n >= {reach}", flush=True)
    problems.extend(
        f"{condition.name} failed: {condition.detail}"
        for condition in closed_form_conditions(certificate)
        if not condition.holds
    )

    if problems:
        return _print_refusals(path, problems)

    start = time.time()
    interval = None
    try:
        interval = verify_by_intervals(certificate, enclose=True)
    except IntervalInputError as error:
        problems.append(f"the interval route could not decide it: {error}")
    enclosure: tuple[Fraction, Fraction] | None = None
    if interval is not None:
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
            problems.append(
                f"{stalled} boxes stalled; the interval route decided nothing there"
            )
        if not quick:
            if enclosure is None:
                problems.append("the interval route returned no enclosure to compare")
            elif enclosure[0] != enclosure[1]:
                problems.append(f"the enclosure has width: {enclosure}")
            elif declared_least != enclosure[0]:
                problems.append(
                    f"declared least_cell_mass {declared_least} != "
                    f"interval enclosure {enclosure[0]}"
                )
    _, changed_after_interval = _unchanged_sha256(path, frozen)
    if changed_after_interval is not None:
        problems.append(changed_after_interval)

    if problems:
        return _print_refusals(path, problems)
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
    digest, changed = _unchanged_sha256(path, frozen)
    if changed is not None:
        problems.append(changed)
    if problems:
        return _print_refusals(path, problems)
    assert digest is not None
    print(
        f"  RETAINABLE: both routes accept and agree at {exact.minimum_cell_mass}; "
        f"sha256 {digest}",
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
    seen: set[Path] = set()
    for path in args.paths:
        if path in seen:
            print(f"{path}: SKIPPED duplicate path", flush=True)
            continue
        seen.add(path)
        ok = decide(path, quick=args.quick) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
