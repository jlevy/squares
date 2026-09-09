#!/usr/bin/env python3
"""Decide a threshold-certificate file exactly, and report every condition.

A threshold certificate is a point certificate plus *threshold atoms* ``(S, k, w)``:
weight ``w`` to every core containing at least ``k`` of the points of ``S``, budget
``w floor(|S| / k)``. The theorem and its five conditions are in
`sqpack.fractional.threshold`; this tool reads the frozen bytes, refuses anything that is
not an exact rational record, and decides Conditions 1', 2', 3, 4 and 5' by the exact
event-cell sweep with the inclusion--exclusion terms. Two readings of the same terms --
the dense grid and the slab sweep -- are asked to agree at every direction, and the least
charge is re-evaluated at its witness placement by direct membership counting.

This is a spike tool, not the retention gate: a positive verdict here is one exact
route, and retention wants an independent verifier as well.

Usage:
    uv run --frozen python -m devtools.decide_threshold_certificate <path>...
    PACK_JOBS=4 uv run --frozen python -m devtools.decide_threshold_certificate <path>

Schema: the point certificate's fields (``n``, ``outer_side``, ``square_side``,
``angle_limit``, ``direction_steps``, ``atoms`` as ``[x, y, w]`` rational strings) plus
``threshold_atoms``: a list of ``{"points": [[x, y], ...], "threshold": k,
"weight": w}`` with rational strings and an integer ``k``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from functools import partial
from pathlib import Path
from typing import Never, cast

from sqpack.fractional.model import Atom
from sqpack.fractional.threshold import (
    DENSE_CELL_LIMIT,
    ThresholdAtom,
    ThresholdCertificate,
    closed_form_threshold_conditions,
    exact_charge,
    minimum_charge,
)

RATIONAL = re.compile(r"^-?[0-9]+(/[1-9][0-9]*)?$")
MAX_BYTES = 32 * 1024 * 1024


class FormatError(ValueError):
    """The JSON cannot be read as an exact threshold-certificate record."""


def _no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    record: dict[str, object] = {}
    for key, value in pairs:
        if key in record:
            raise FormatError(f"duplicate JSON object key {key!r}")
        record[key] = value
    return record


def _inexact(text: str) -> Never:
    raise FormatError(f"inexact JSON number {text!r}; use an exact rational string")


def _rational(value: object, field: str) -> Fraction:
    if not isinstance(value, str) or RATIONAL.fullmatch(value) is None:
        raise FormatError(f"field {field!r} must be an exact rational string, got {value!r}")
    return Fraction(value)


def _integer(value: object, field: str) -> int:
    if type(value) is not int:
        raise FormatError(f"field {field!r} must be a JSON integer, got {value!r}")
    return cast(int, value)


def load(data: bytes) -> tuple[ThresholdCertificate, dict[str, object]]:
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
    record = cast(dict[str, object], decoded)
    n = _integer(record.get("n"), "n")
    steps = _integer(record.get("direction_steps"), "direction_steps")
    limit = _rational(record.get("angle_limit"), "angle_limit")
    outer_side = _rational(record.get("outer_side"), "outer_side")
    square_side = _rational(record.get("square_side"), "square_side")
    atoms_record = record.get("atoms")
    if not isinstance(atoms_record, list):
        raise FormatError("field 'atoms' must be a JSON array")
    atoms: list[Atom] = []
    for index, entry in enumerate(cast(list[object], atoms_record)):
        if not isinstance(entry, list) or len(entry) != 3:
            raise FormatError(f"atoms[{index}] must be a three-element JSON array")
        values = cast(list[object], entry)
        x, y, w = (_rational(v, f"atoms[{index}][{c}]") for c, v in enumerate(values))
        atoms.append(Atom(f"{index:04d}", x, y, w))
    thresholds_record = record.get("threshold_atoms", [])
    if not isinstance(thresholds_record, list):
        raise FormatError("field 'threshold_atoms' must be a JSON array")
    threshold_atoms: list[ThresholdAtom] = []
    for index, entry in enumerate(cast(list[object], thresholds_record)):
        if not isinstance(entry, dict):
            raise FormatError(f"threshold_atoms[{index}] must be a JSON object")
        item = cast(dict[str, object], entry)
        points_record = item.get("points")
        if not isinstance(points_record, list):
            raise FormatError(f"threshold_atoms[{index}].points must be a JSON array")
        points: list[tuple[Fraction, Fraction]] = []
        for p, point in enumerate(cast(list[object], points_record)):
            if not isinstance(point, list) or len(point) != 2:
                raise FormatError(f"threshold_atoms[{index}].points[{p}] must be [x, y]")
            pair = cast(list[object], point)
            points.append(
                (
                    _rational(pair[0], f"threshold_atoms[{index}].points[{p}][0]"),
                    _rational(pair[1], f"threshold_atoms[{index}].points[{p}][1]"),
                )
            )
        try:
            threshold_atoms.append(
                ThresholdAtom(
                    tuple(points),
                    _integer(item.get("threshold"), f"threshold_atoms[{index}].threshold"),
                    _rational(item.get("weight"), f"threshold_atoms[{index}].weight"),
                )
            )
        except ValueError as error:
            raise FormatError(f"threshold_atoms[{index}]: {error}") from None
    try:
        certificate = ThresholdCertificate(
            n=n,
            outer_side=outer_side,
            square_side=square_side,
            atoms=tuple(atoms),
            threshold_atoms=tuple(threshold_atoms),
            half_tangents=tuple(limit * k / steps for k in range(steps + 1)),
        )
    except ValueError as error:
        raise FormatError(f"invalid certificate precondition: {error}") from None
    return certificate, record


def _placement_membership(
    certificate: ThresholdCertificate, direction_index: int, witness: tuple[Fraction, Fraction]
):
    direction = certificate.directions[direction_index]
    half = certificate.square_side / 2
    cu, cv = witness

    def contains(x: Fraction, y: Fraction) -> bool:
        u = direction.ux * x + direction.uy * y
        v = direction.vx * x + direction.vy * y
        return abs(u - cu) <= half and abs(v - cv) <= half

    return contains


def decide(path: Path, *, workers: int) -> bool:
    started = time.perf_counter()
    frozen = path.read_bytes()
    try:
        certificate, record = load(frozen)
    except FormatError as error:
        print(f"{path}: REFUSED: {error}", flush=True)
        return False
    print(
        f"{path}: n = {certificate.n}, L = {certificate.outer_side} = "
        f"{float(certificate.outer_side):.6f}, B = {certificate.square_side}, "
        f"{len(certificate.atoms)} point atoms (mass {certificate.point_mass} = "
        f"{float(certificate.point_mass):.9f}), {len(certificate.threshold_atoms)} threshold "
        f"atoms (budget {certificate.threshold_budget} = "
        f"{float(certificate.threshold_budget):.9f}), total budget "
        f"{certificate.total_budget} = {float(certificate.total_budget):.9f}",
        flush=True,
    )
    declared = record.get("total_budget")
    if declared is not None and _rational(declared, "total_budget") != certificate.total_budget:
        print(f"{path}: REFUSED: declared total_budget {declared} != recomputed", flush=True)
        return False
    reports = list(closed_form_threshold_conditions(certificate))
    for report in reports:
        print(
            f"  {'holds' if report.holds else 'FAILS'}: {report.name}: {report.detail}",
            flush=True,
        )

    worst: Fraction | None = None
    worst_at: tuple[int, tuple[Fraction, Fraction]] | None = None
    disagreements = 0
    directions = certificate.directions
    if workers > 1:
        with ProcessPoolExecutor(
            max_workers=workers, mp_context=mp.get_context("fork")
        ) as pool:
            results = list(pool.map(partial(_both_routes, certificate), range(len(directions))))
    else:
        results = [_both_routes(certificate, k) for k in range(len(directions))]
    for k, (dense, slab) in enumerate(results):
        if dense != slab:
            disagreements += 1
            print(
                f"  DISAGREEMENT at direction {k}: dense {dense[0]} vs slab {slab[0]}",
                flush=True,
            )
        if worst is None or dense[0] < worst:
            worst, worst_at = dense[0], (k, dense[1])
    if worst is None or worst_at is None:
        raise RuntimeError("no direction was decided")
    contains = _placement_membership(certificate, worst_at[0], worst_at[1])
    at_witness = exact_charge(certificate.atoms, certificate.threshold_atoms, contains)
    print(
        f"  Condition 5' least cell charge {worst} = {float(worst):.9f} at direction "
        f"{worst_at[0]}, witness (rotated frame) {worst_at[1]}; charge re-evaluated at the "
        f"witness by membership counting {at_witness} "
        f"({'agrees' if at_witness == worst else 'DISAGREES'}); "
        f"dense/slab disagreements {disagreements}",
        flush=True,
    )
    accepted = (
        all(r.holds for r in reports)
        and worst >= 1
        and disagreements == 0
        and at_witness == worst
    )
    digest = hashlib.sha256(frozen).hexdigest()
    verdict = (
        "ACCEPTED (one exact route; retention wants an independent verifier)"
        if accepted
        else "REJECTED"
    )
    print(
        f"{path}: {verdict}; sha256 {digest}; {time.perf_counter() - started:.1f}s", flush=True
    )
    return accepted


def _both_routes(certificate: ThresholdCertificate, k: int):
    direction = certificate.directions[k]
    dense = minimum_charge(
        certificate.atoms,
        certificate.threshold_atoms,
        direction,
        certificate.outer_side,
        certificate.square_side,
        dense_cell_limit=DENSE_CELL_LIMIT,
    )
    slab = minimum_charge(
        certificate.atoms,
        certificate.threshold_atoms,
        direction,
        certificate.outer_side,
        certificate.square_side,
        dense_cell_limit=0,
    )
    return dense, slab


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--workers", type=int, default=int(os.environ.get("PACK_JOBS", "1")))
    args = parser.parse_args(argv)
    ok = True
    for path in args.paths:
        ok = decide(path, workers=max(1, args.workers)) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
