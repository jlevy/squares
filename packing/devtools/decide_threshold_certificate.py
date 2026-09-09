#!/usr/bin/env python3
"""Decide a threshold-certificate file by both routes, and refuse it unless both accept.

A threshold certificate is a point certificate plus *threshold atoms* ``(S, k, w)``:
weight ``w`` to every core containing at least ``k`` of the points of ``S``, budget
``w floor(|S| / k)``. The theorem and its five conditions are in
`sqpack.fractional.threshold`. This tool reads the frozen bytes, refuses anything that is
not an exact rational record, decides Conditions 1', 2', 3 and 4 in closed form, and then
decides ``Condition 5'`` twice, by two methods with different failure modes:

* the interval branch and bound of `sqpack.fractional.threshold_interval`, over boxes of
  centres on the doubled net, with the least charge enclosed and the enclosure required
  to have width zero;
* the exact event-cell sweep of `sqpack.fractional.threshold`, with the inclusion--exclusion
  terms, read two ways -- the dense grid and the slab sweep -- that must agree at every
  direction, and the least charge re-evaluated at its witness by membership counting.

The two routes share the ``ThresholdCertificate`` object and the closed-form conditions;
they share no part of the ``Condition 5'`` decision. They are asked to agree on the number,
not merely on the verdict: the interval enclosure must equal the sweep's least charge
exactly, or one of them is deciding a different object. ``RETAINABLE`` is printed only
when both accept and agree; before it the named path is reread, its bytes are required
to be unchanged, and their SHA-256 is printed, because the digest and not a mutable
pathname is the identity of the accepted artifact.

Usage:
    uv run --frozen python -m devtools.decide_threshold_certificate <path>...
    uv run --frozen python -m devtools.decide_threshold_certificate --quick <path>...
    uv run --frozen python -m devtools.decide_threshold_certificate --exact-only <path>...
    PACK_JOBS=3 uv run --frozen python -m devtools.decide_threshold_certificate <path>

``--quick`` runs only the interval route, which is enough to reject a candidate and never
enough to retain one; the tool says so in its own output. ``--exact-only`` is the spike
tool this gate grew out of: the one exact route alone, whose positive verdict is worded
``ACCEPTED (one exact route; retention wants an independent verifier)``. Closed-form
failures refuse a record before either route runs, whichever mode is asked for.

Schema: the point certificate's fields (``n``, ``outer_side``, ``square_side``,
``angle_limit``, ``direction_steps``, ``atoms`` as ``[x, y, w]`` rational strings) plus
``threshold_atoms``: a list of ``{"points": [[x, y], ...], "threshold": k,
"weight": w}`` with rational strings and an integer ``k``. Optional declarations are
checked when present: ``total_budget``, ``claim`` (which must read ``s(n) >= L``),
``least_cell_charge`` (which both routes must reproduce), and ``variant``, which must be
``threshold`` if it is declared at all -- a record declaring anything else is refused by
name, because this gate implements only these conditions.
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
from typing import Literal, Never, cast

from sqpack.fractional.interval import IntervalInputError
from sqpack.fractional.model import Atom
from sqpack.fractional.threshold import (
    DENSE_CELL_LIMIT,
    ThresholdAtom,
    ThresholdCertificate,
    closed_form_threshold_conditions,
    exact_charge,
    minimum_charge,
)
from sqpack.fractional.threshold_interval import (
    exact_charge_at_witness,
    verify_threshold_by_intervals,
)

RATIONAL = re.compile(r"^-?[0-9]+(/[1-9][0-9]*)?$")
MAX_BYTES = 32 * 1024 * 1024
VARIANT = "threshold"

Mode = Literal["both", "quick", "exact-only"]


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


def _read_bounded(path: Path) -> bytes:
    """Read one candidate without letting its size drive allocation."""
    with path.open("rb") as source:
        data = source.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise FormatError(f"file exceeds the {MAX_BYTES}-byte limit")
    return data


def _unchanged_sha256(path: Path, frozen: bytes) -> tuple[str | None, str | None]:
    """Bind a positive verdict to bytes that still occupy the named path."""
    try:
        current = _read_bounded(path)
    except (FormatError, OSError) as error:
        return None, f"cannot reread accepted path: {error}"
    if current != frozen:
        return None, "the certificate path changed while the decision was running"
    return hashlib.sha256(frozen).hexdigest(), None


def _declarations(
    certificate: ThresholdCertificate, record: dict[str, object]
) -> tuple[list[str], Fraction | None]:
    """Every optional declaration the record makes, checked against the object."""
    problems: list[str] = []
    variant = record.get("variant", VARIANT)
    if variant != VARIANT:
        problems.append(
            f"variant {variant!r} is declared, and this gate decides only {VARIANT!r} "
            "certificates; nothing else can be printed RETAINABLE here"
        )
    declared_budget = record.get("total_budget")
    if declared_budget is not None:
        try:
            if _rational(declared_budget, "total_budget") != certificate.total_budget:
                problems.append(
                    f"declared total_budget {declared_budget} != recomputed "
                    f"{certificate.total_budget}"
                )
        except FormatError as error:
            problems.append(str(error))
    claim = record.get("claim")
    expected_claim = f"s({certificate.n}) >= {certificate.outer_side}"
    if claim is not None and claim != expected_claim:
        problems.append(f"declared claim {claim!r} != theorem conclusion {expected_claim!r}")
    declared_least: Fraction | None = None
    if "least_cell_charge" in record:
        try:
            declared_least = _rational(record["least_cell_charge"], "least_cell_charge")
        except FormatError as error:
            problems.append(str(error))
    return problems, declared_least


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


def _print_refusals(path: Path, problems: list[str]) -> bool:
    for problem in problems:
        print(f"{path}: REFUSED: {problem}", flush=True)
    return False


def _interval_route(
    certificate: ThresholdCertificate, *, workers: int
) -> tuple[Fraction | None, list[str]]:
    """Run the interval route; return the pinned least charge and every objection."""
    problems: list[str] = []
    start = time.perf_counter()
    try:
        verdict = verify_threshold_by_intervals(certificate, enclose=True, workers=workers)
    except IntervalInputError as error:
        return None, [f"the interval route could not decide it: {error}"]
    boxes = sum(o.boxes for o in verdict.directions)
    stalled = sum(o.stalled for o in verdict.directions)
    exhausted = sum(o.budget_exhausted for o in verdict.directions)
    enclosure = verdict.enclosure
    print(
        f"  interval accepted={verdict.accepted} enclosure={enclosure} "
        f"directions={len(verdict.directions)} boxes={boxes} stalled={stalled} "
        f"budget-exhausted={exhausted} ({time.perf_counter() - start:.1f}s)",
        flush=True,
    )
    for condition in verdict.conditions:
        print(f"    {condition.status}: {condition.name}: {condition.detail}", flush=True)
    worst = min(
        (o for o in verdict.directions if o.upper is not None),
        key=lambda o: o.upper or 0,
        default=None,
    )
    if worst is not None and worst.witness is not None:
        witness = exact_charge_at_witness(certificate, worst.label, worst.witness)
        print(
            f"    least point charge at direction {worst.label}, witness (rotated frame) "
            f"{worst.witness}: exact charge by membership counting {witness.charge} = "
            f"{float(witness.charge):.9f}, admissible {witness.admissible}",
            flush=True,
        )
    for refutation in verdict.refutations:
        print(
            f"    REFUTING WITNESS at direction {refutation.label}: {refutation.witness}, "
            f"exact charge {refutation.charge} = {float(refutation.charge):.9f}, "
            f"admissible {refutation.admissible}",
            flush=True,
        )
    if not verdict.accepted:
        problems.append(f"the interval route refused it: {verdict.failures}")
    if stalled:
        problems.append(f"{stalled} boxes stalled; the interval route decided nothing there")
    if exhausted:
        problems.append(f"{exhausted} directions exhausted the box budget")
    if enclosure is None:
        problems.append("the interval route returned no enclosure to compare")
        return None, problems
    if enclosure[0] != enclosure[1]:
        problems.append(f"the enclosure has width: {enclosure}")
        return None, problems
    return enclosure[0], problems


def _exact_route(
    certificate: ThresholdCertificate, *, workers: int
) -> tuple[Fraction | None, list[str]]:
    """Run the exact sweep two ways; return the least charge and every objection."""
    problems: list[str] = []
    start = time.perf_counter()
    directions = certificate.directions
    if workers > 1:
        with ProcessPoolExecutor(
            max_workers=workers, mp_context=mp.get_context("fork")
        ) as pool:
            results = list(
                pool.map(partial(_dense_and_slab, certificate), range(len(directions)))
            )
    else:
        results = [_dense_and_slab(certificate, k) for k in range(len(directions))]
    worst: Fraction | None = None
    worst_at: tuple[int, tuple[Fraction, Fraction]] | None = None
    disagreements = 0
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
        return None, ["the exact sweep decided no direction"]
    contains = _placement_membership(certificate, worst_at[0], worst_at[1])
    at_witness = exact_charge(certificate.atoms, certificate.threshold_atoms, contains)
    print(
        f"  exact    least cell charge {worst} = {float(worst):.9f} at direction "
        f"{worst_at[0]}; charge re-evaluated at the witness by membership counting "
        f"{at_witness} ({'agrees' if at_witness == worst else 'DISAGREES'}); dense/slab "
        f"disagreements {disagreements} ({time.perf_counter() - start:.1f}s)",
        flush=True,
    )
    if worst < 1:
        problems.append(f"the exact sweep refused it: least cell charge {worst} < 1")
    if disagreements:
        problems.append(f"dense grid and slab sweep disagree at {disagreements} directions")
    if at_witness != worst:
        problems.append(f"the witness re-evaluation {at_witness} != least cell charge {worst}")
    return worst, problems


def decide(path: Path, *, workers: int, mode: Mode = "both") -> bool:
    started = time.perf_counter()
    try:
        frozen = _read_bounded(path)
        certificate, record = load(frozen)
    except (FormatError, OSError) as error:
        return _print_refusals(path, [str(error)])
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
    problems, declared_least = _declarations(certificate, record)
    if declared_least is None:
        print(
            "  no least_cell_charge is declared; the routes are compared to each other",
            flush=True,
        )
    for report in closed_form_threshold_conditions(certificate):
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
        interval_least, problems = _interval_route(certificate, workers=workers)
        if (
            declared_least is not None
            and interval_least is not None
            and declared_least != interval_least
        ):
            problems.append(
                f"declared least_cell_charge {declared_least} != interval enclosure "
                f"{interval_least}"
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

    exact_least, problems = _exact_route(certificate, workers=workers)
    if exact_least is not None:
        if interval_least is not None and interval_least != exact_least:
            problems.append(
                f"the two routes disagree on the least charge: sweep {exact_least} against "
                f"interval enclosure {interval_least}"
            )
        if declared_least is not None and declared_least != exact_least:
            problems.append(f"declared least_cell_charge {declared_least} != {exact_least}")
    digest, changed = _unchanged_sha256(path, frozen)
    if changed is not None:
        problems.append(changed)
    if problems:
        return _print_refusals(path, problems)
    elapsed = time.perf_counter() - started
    verdict = (
        f"ACCEPTED (one exact route; retention wants an independent verifier); "
        f"least cell charge {exact_least}"
        if mode == "exact-only"
        else f"RETAINABLE: both routes accept and agree at {exact_least}"
    )
    print(f"{path}: {verdict}; sha256 {digest}; {elapsed:.1f}s", flush=True)
    return True


def _dense_and_slab(certificate: ThresholdCertificate, k: int):
    """The exact sweep at one direction, read from the dense grid and from the slabs."""
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
    routes = parser.add_mutually_exclusive_group()
    routes.add_argument(
        "--quick", action="store_true", help="interval route only; cannot retain"
    )
    routes.add_argument(
        "--exact-only",
        action="store_true",
        help="the exact sweep only, as the spike tool ran it; cannot retain",
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
