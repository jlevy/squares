#!/usr/bin/env python3
"""Decide a relational-certificate file by both exact routes, or a T-025 record by proxy.

Relational records (`variant: relational/v1`) carry point atoms, threshold atoms
(`ThresholdAtom`, including weighted-majority / k-of-S), and floor atoms. This tool
refuses a malformed record before any coverage, decides Conditions 1', 2', 3 and 4 in
closed form, then decides Condition 5' twice:

* the exact event-cell count-grid of `sqpack.fractional.relational`;
* the independently structured Fraction interval-box route on the event arrangement.

``RETAINABLE`` is printed only when both accept and agree. A T-id in this class still
waits on two-route C4 against the floating-point interval verifier; these two exact
routes are the admission gate.

Ordinary T-025-shaped records (`variant: threshold`, unweighted 2-of-3 atoms, no floor
field) are delegated to `devtools.decide_threshold_certificate.load` and `.decide`. This
module does not copy `verify_claim.py` and does not reread T-025 or T-026 bytes as floor
atoms.

Usage:
    uv run --frozen python -m devtools.decide_relational_certificate PATH
    uv run --frozen python -m devtools.decide_relational_certificate --exact-only PATH
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Literal, Never, cast

from strif import atomic_write_text

from devtools.decide_threshold_certificate import FormatError as ThresholdFormatError
from devtools.decide_threshold_certificate import decide as decide_threshold
from devtools.decide_threshold_certificate import load as load_threshold
from sqpack.fractional.relational import (
    RELATIONAL_VARIANT,
    FloorCertificate,
    closed_form_relational_conditions,
    exact_relational_charge,
    minimum_charge_event_cell,
    minimum_charge_interval_boxes,
)

RATIONAL = re.compile(r"^-?[0-9]+(/[1-9][0-9]*)?$")
MAX_BYTES = 32 * 1024 * 1024
THRESHOLD_VARIANT = "threshold"
Mode = Literal["both", "quick", "exact-only"]


class FormatError(ValueError):
    """The JSON cannot be read as an exact relational-certificate record."""


def _no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    record: dict[str, object] = {}
    for key, value in pairs:
        if key in record:
            raise FormatError(f"duplicate JSON object key {key!r}")
        record[key] = value
    return record


def _inexact(text: str) -> Never:
    raise FormatError(f"inexact JSON number {text!r}; use an exact rational string")


def _decode(data: bytes) -> dict[str, object]:
    if len(data) > MAX_BYTES:
        raise FormatError(f"file exceeds the {MAX_BYTES}-byte limit")
    try:
        decoded = cast(
            object,
            json.loads(
                data,
                object_pairs_hook=_no_duplicates,
                parse_float=_inexact,
                parse_constant=_inexact,
            ),
        )
    except FormatError:
        raise
    except (UnicodeError, ValueError, RecursionError) as error:
        raise FormatError(str(error)) from None
    if not isinstance(decoded, dict):
        raise FormatError("top-level JSON value must be an object")
    return cast(dict[str, object], decoded)


def _threshold_atom_is_weighted(entry: object) -> bool:
    if not isinstance(entry, dict):
        return False
    return any(key in entry for key in ("variant", "weighted_points", "multiplicities"))


def is_ordinary_threshold_record(record: dict[str, object]) -> bool:
    """True for a T-025-shaped record the preserved threshold loader must decide."""

    if "floor_atoms" in record:
        return False
    variant = record.get("variant", THRESHOLD_VARIANT)
    if variant != THRESHOLD_VARIANT:
        return False
    atoms = record.get("threshold_atoms", [])
    if not isinstance(atoms, list):
        return False
    return not any(_threshold_atom_is_weighted(entry) for entry in atoms)


def _read_bounded(path: Path) -> bytes:
    with path.open("rb") as source:
        data = source.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise FormatError(f"file exceeds the {MAX_BYTES}-byte limit")
    return data


def load(data: bytes) -> tuple[FloorCertificate, dict[str, object]]:
    """Load a relational record. Ordinary threshold bytes are not this loader's job."""

    record = _decode(data)
    if is_ordinary_threshold_record(record):
        raise FormatError(
            "ordinary threshold records are decided by the preserved threshold loader; "
            "this reader does not reinterpret T-025 bytes"
        )
    try:
        certificate = FloorCertificate.from_record(record)
    except (TypeError, ValueError) as error:
        raise FormatError(str(error)) from None
    return certificate, record


def write_record(path: Path, record: dict[str, object]) -> None:
    """Publish one JSON record atomically."""

    atomic_write_text(path, json.dumps(record, indent=1) + "\n", make_parents=True)


def _unchanged_sha256(path: Path, frozen: bytes) -> tuple[str | None, str | None]:
    try:
        current = _read_bounded(path)
    except (FormatError, OSError) as error:
        return None, f"cannot reread accepted path: {error}"
    if current != frozen:
        return None, "the certificate path changed while the decision was running"
    return hashlib.sha256(frozen).hexdigest(), None


def _declarations(
    certificate: FloorCertificate, record: dict[str, object]
) -> tuple[list[str], Fraction | None]:
    problems: list[str] = []
    variant = record.get("variant", RELATIONAL_VARIANT)
    if variant != RELATIONAL_VARIANT:
        problems.append(
            f"variant {variant!r} is declared, and this gate decides {RELATIONAL_VARIANT!r} "
            "or delegates ordinary threshold records"
        )
    declared_budget = record.get("total_budget")
    if declared_budget is not None:
        if not isinstance(declared_budget, str) or RATIONAL.fullmatch(declared_budget) is None:
            problems.append(
                f"field 'total_budget' must be an exact rational string, "
                f"got {declared_budget!r}"
            )
        elif Fraction(declared_budget) != certificate.total_budget:
            problems.append(
                f"declared total_budget {declared_budget} != recomputed "
                f"{certificate.total_budget}"
            )
    declared_least: Fraction | None = None
    if "least_cell_charge" in record:
        value = record["least_cell_charge"]
        if not isinstance(value, str) or RATIONAL.fullmatch(value) is None:
            problems.append(
                f"field 'least_cell_charge' must be an exact rational string, got {value!r}"
            )
        else:
            declared_least = Fraction(value)
    return problems, declared_least


def _print_refusals(path: Path, problems: list[str]) -> bool:
    for problem in problems:
        print(f"{path}: REFUSED: {problem}", flush=True)
    return False


def _placement_membership(
    certificate: FloorCertificate, direction_index: int, witness: tuple[Fraction, Fraction]
):
    direction = certificate.directions[direction_index]
    half = certificate.square_side / 2
    cu, cv = witness

    def contains(x: Fraction, y: Fraction) -> bool:
        u = direction.ux * x + direction.uy * y
        v = direction.vx * x + direction.vy * y
        return abs(u - cu) <= half and abs(v - cv) <= half

    return contains


def _event_cell_route(certificate: FloorCertificate) -> tuple[Fraction | None, list[str]]:
    problems: list[str] = []
    start = time.perf_counter()
    worst: Fraction | None = None
    worst_at: tuple[int, tuple[Fraction, Fraction]] | None = None
    try:
        for index, direction in enumerate(certificate.directions):
            charge, witness = minimum_charge_event_cell(
                certificate.atoms,
                certificate.threshold_atoms,
                certificate.floor_atoms,
                direction,
                outer_side=certificate.outer_side,
                square_side=certificate.square_side,
            )
            if worst is None or charge < worst:
                worst, worst_at = charge, (index, witness)
    except (TypeError, ValueError) as error:
        return None, [f"the event-cell route could not decide it: {error}"]
    if worst is None or worst_at is None:
        return None, ["the event-cell route decided no direction"]
    contains = _placement_membership(certificate, worst_at[0], worst_at[1])
    at_witness = exact_relational_charge(
        certificate.atoms, certificate.threshold_atoms, certificate.floor_atoms, contains
    )
    print(
        f"  event-cell least cell charge {worst} = {float(worst):.9f} at direction "
        f"{worst_at[0]}; charge re-evaluated at the witness by membership counting "
        f"{at_witness} ({'agrees' if at_witness == worst else 'DISAGREES'}) "
        f"({time.perf_counter() - start:.1f}s)",
        flush=True,
    )
    if worst < 1:
        problems.append(f"the event-cell route refused it: least cell charge {worst} < 1")
    if at_witness != worst:
        problems.append(f"the witness re-evaluation {at_witness} != least cell charge {worst}")
    return worst, problems


def _interval_route(certificate: FloorCertificate) -> tuple[Fraction | None, list[str]]:
    problems: list[str] = []
    start = time.perf_counter()
    worst: Fraction | None = None
    worst_at: tuple[int, tuple[Fraction, Fraction]] | None = None
    try:
        for index, direction in enumerate(certificate.directions):
            charge, witness = minimum_charge_interval_boxes(
                certificate.atoms,
                certificate.threshold_atoms,
                certificate.floor_atoms,
                direction,
                outer_side=certificate.outer_side,
                square_side=certificate.square_side,
            )
            if worst is None or charge < worst:
                worst, worst_at = charge, (index, witness)
    except (TypeError, ValueError) as error:
        return None, [f"the interval route could not decide it: {error}"]
    if worst is None or worst_at is None:
        return None, ["the interval route decided no direction"]
    print(
        f"  interval  least cell charge {worst} = {float(worst):.9f} at direction "
        f"{worst_at[0]} ({time.perf_counter() - start:.1f}s)",
        flush=True,
    )
    if worst < 1:
        problems.append(f"the interval route refused it: least cell charge {worst} < 1")
    return worst, problems


def _decide_relational(path: Path, frozen: bytes, *, mode: Mode) -> bool:
    try:
        certificate, record = load(frozen)
    except FormatError as error:
        return _print_refusals(path, [str(error)])
    print(
        f"{path}: n = {certificate.n}, L = {certificate.outer_side} = "
        f"{float(certificate.outer_side):.6f}, B = {certificate.square_side}, "
        f"{len(certificate.atoms)} point atoms (mass {certificate.point_mass}), "
        f"{len(certificate.threshold_atoms)} threshold atoms (budget "
        f"{certificate.threshold_budget}), {len(certificate.floor_atoms)} floor atoms "
        f"(budget {certificate.floor_budget}), total budget {certificate.total_budget}",
        flush=True,
    )
    problems, declared_least = _declarations(certificate, record)
    for report in closed_form_relational_conditions(certificate):
        print(
            f"  {'holds' if report.holds else 'FAILS'}: {report.name}: {report.detail}",
            flush=True,
        )
        if not report.holds:
            problems.append(f"{report.name} failed: {report.detail}")
    if problems:
        return _print_refusals(path, problems)

    interval_least: Fraction | None = None
    if mode != "exact-only":
        interval_least, problems = _interval_route(certificate)
        if (
            declared_least is not None
            and interval_least is not None
            and declared_least != interval_least
        ):
            problems.append(
                f"declared least_cell_charge {declared_least} != interval {interval_least}"
            )
        _, changed = _unchanged_sha256(path, frozen)
        if changed is not None:
            problems.append(changed)
        if problems:
            return _print_refusals(path, problems)
        if mode == "quick":
            print(
                "  the interval route accepts. NOT ENOUGH TO RETAIN: run without --quick.",
                flush=True,
            )
            return True

    exact_least, problems = _event_cell_route(certificate)
    if exact_least is not None:
        if interval_least is not None and interval_least != exact_least:
            problems.append(
                f"the two routes disagree on the least charge: event-cell {exact_least} "
                f"against interval {interval_least}"
            )
        if declared_least is not None and declared_least != exact_least:
            problems.append(f"declared least_cell_charge {declared_least} != {exact_least}")
    digest, changed = _unchanged_sha256(path, frozen)
    if changed is not None:
        problems.append(changed)
    if problems:
        return _print_refusals(path, problems)
    verdict = (
        f"ACCEPTED (one exact route; a T-id waits on two-route C4); least cell charge "
        f"{exact_least}"
        if mode == "exact-only"
        else (
            f"ACCEPTED by both exact routes at {exact_least}; a T-id in this class still "
            "waits on two-route C4 against the floating-point interval verifier"
        )
    )
    print(f"{path}: {verdict}; sha256 {digest}", flush=True)
    return True


def decide(path: Path, *, workers: int = 1, mode: Mode = "both") -> bool:
    """Decide one path. Ordinary threshold records are delegated, not reinterpreted."""

    try:
        frozen = _read_bounded(path)
        record = _decode(frozen)
    except (FormatError, OSError) as error:
        return _print_refusals(path, [str(error)])
    if is_ordinary_threshold_record(record):
        try:
            load_threshold(frozen)
        except ThresholdFormatError as error:
            return _print_refusals(path, [str(error)])
        print(f"{path}: ordinary threshold record; delegating to the T-025 loader", flush=True)
        return decide_threshold(path, workers=workers, mode=mode)
    return _decide_relational(path, frozen, mode=mode)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--workers", type=int, default=int(os.environ.get("PACK_JOBS", "1")))
    routes = parser.add_mutually_exclusive_group()
    routes.add_argument(
        "--quick", action="store_true", help="interval route only; cannot retain"
    )
    routes.add_argument(
        "--exact-only",
        action="store_true",
        help="the event-cell route only; cannot retain",
    )
    args = parser.parse_args(argv)
    mode: Mode = "quick" if args.quick else "exact-only" if args.exact_only else "both"
    ok = True
    seen: set[Path] = set()
    for path in args.paths:
        if path in seen:
            print(f"{path}: SKIPPED duplicate path", flush=True)
            continue
        seen.add(path)
        ok = decide(path, workers=max(1, args.workers), mode=mode) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
