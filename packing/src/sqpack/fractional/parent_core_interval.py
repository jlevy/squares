"""Method-distinct interval coverage for the adaptive parent-core theorem.

The search never builds event slabs or a signed threshold expansion. It counts
sites surely captured throughout centre boxes, splits unresolved boxes, and
reports any unresolved boundary or work limit as undecided. Exact rational
premises and the complete row inventory are separate from this numerical search.
"""

from __future__ import annotations

import multiprocessing as mp
from collections.abc import Callable, Iterable
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from fractions import Fraction
from math import ceil
from time import monotonic
from typing import ClassVar

from sqpack.fractional.interval import DirectionOutcome, Interval, Rotation
from sqpack.fractional.parent_core import (
    ParentCoreCertificate,
    ParentCorePremises,
    validate_parent_core,
)
from sqpack.fractional.threshold_interval import ThresholdAtomData, ThresholdDirectionSearch


@dataclass(frozen=True, slots=True)
class ParentCoreWitness:
    row: int
    rotated_centre: tuple[float, float]
    charge: Fraction
    admissible: bool


def exact_parent_charge(
    certificate: ParentCoreCertificate, index: int, witness: tuple[float, float]
) -> ParentCoreWitness:
    """Check a reported point using exact parent-domain and core-membership arithmetic."""
    row = certificate.rows[index]
    cosine, sine = row.rotation
    u, v = map(Fraction, witness)
    x, y = cosine * u - sine * v, sine * u + cosine * v
    margin = row.centre_margin(certificate.parent_side)
    far = certificate.outer_side - margin
    half = row.core_side / 2

    def inside(point: tuple[Fraction, Fraction]) -> bool:
        px, py = point
        return (
            abs(cosine * px + sine * py - u) <= half
            and abs(-sine * px + cosine * py - v) <= half
        )

    charge = sum(
        (atom.weight for atom in certificate.atoms if inside((atom.x, atom.y))), Fraction(0)
    )
    for atom in certificate.threshold_atoms:
        count = sum(
            multiplicity
            for point, multiplicity in zip(atom.points, atom.multiplicities, strict=True)
            if inside(point)
        )
        if count >= atom.threshold:
            charge += atom.weight
    return ParentCoreWitness(index, witness, charge, margin <= x <= far and margin <= y <= far)


@dataclass(frozen=True, slots=True)
class ParentCoreIntervalVerdict:
    premises: ParentCorePremises
    indices: tuple[int, ...]
    directions: tuple[DirectionOutcome, ...]
    scale: int
    threshold_units: int
    refutations: tuple[ParentCoreWitness, ...]
    row_seconds: tuple[float, ...]

    @property
    def complete(self) -> bool:
        return (
            len(self.directions) == len(self.indices) == self.premises.rows
            and sorted(self.indices) == list(range(self.premises.rows))
            and all(
                outcome.label == str(index)
                for index, outcome in zip(self.indices, self.directions, strict=True)
            )
        )

    @property
    def covered(self) -> bool:
        return bool(self.directions) and all(
            outcome.status == "certified"
            and not outcome.budget_exhausted
            and outcome.stalled == 0
            and outcome.lower is not None
            and outcome.lower >= self.threshold_units
            for outcome in self.directions
        )

    @property
    def accepted(self) -> bool:
        return self.complete and self.covered


def parent_core_search(
    certificate: ParentCoreCertificate, data: ThresholdAtomData, index: int
) -> ThresholdDirectionSearch:
    """Build one row with independent exact core side and parent-centre margin."""
    row = certificate.rows[index]
    cosine, sine = row.rotation
    return ThresholdDirectionSearch(
        data,
        Rotation(str(index), Interval.of(cosine), Interval.of(sine)),
        Interval.of(certificate.outer_side),
        Interval.of(row.core_side),
        centre_margin=Interval.of(row.centre_margin(certificate.parent_side)),
    )


def _decide_row(
    certificate: ParentCoreCertificate, data: ThresholdAtomData, index: int, threshold: int
) -> tuple[DirectionOutcome, ParentCoreWitness | None, float]:
    started = monotonic()
    outcome = parent_core_search(certificate, data, index).search(prune_at=threshold)
    witness: ParentCoreWitness | None = None
    if outcome.status == "refuted":
        if outcome.witness is None:
            raise ArithmeticError("interval refutation has no witness")
        witness = exact_parent_charge(certificate, index, outcome.witness)
        if not witness.admissible or witness.charge >= certificate.minimum_charge:
            raise ArithmeticError("exact parent-domain witness rejects the interval refutation")
    return outcome, witness, monotonic() - started


class _WorkerState:
    inputs: ClassVar[tuple[ParentCoreCertificate, ThresholdAtomData, int] | None] = None


def _prepare_worker(
    certificate: ParentCoreCertificate, data: ThresholdAtomData, threshold: int
) -> None:
    _WorkerState.inputs = certificate, data, threshold


def _worker_row(index: int) -> tuple[DirectionOutcome, ParentCoreWitness | None, float]:
    if _WorkerState.inputs is None:
        raise RuntimeError("parent-core worker is uninitialized")
    certificate, data, threshold = _WorkerState.inputs
    return _decide_row(certificate, data, index, threshold)


def verify_parent_core_rows(
    certificate: ParentCoreCertificate,
    indices: Iterable[int] | None = None,
    *,
    batch_size: int = 2048,
    workers: int = 1,
    progress: Callable[[int, DirectionOutcome, float], None] | None = None,
) -> ParentCoreIntervalVerdict:
    """Decide all requested rows; only a complete successful catalogue is accepted.

    A partial pilot has ``covered=True`` when its rows all finish, but can never
    yield ``accepted=True``. An exact witness independently checks every refutation.
    """
    premises = validate_parent_core(certificate)
    selected = tuple(range(len(certificate.rows))) if indices is None else tuple(indices)
    if (
        not selected
        or len(set(selected)) != len(selected)
        or any(
            type(index) is not int or not 0 <= index < len(certificate.rows)
            for index in selected
        )
    ):
        raise ValueError("row selection must contain distinct valid integer indices")
    data = ThresholdAtomData.of(certificate, batch_size=batch_size)
    threshold = ceil(certificate.minimum_charge * data.scale)
    if type(workers) is not int or workers not in (1, 2):
        raise ValueError("workers must be one or two")
    outcomes: list[DirectionOutcome] = []
    refutations: list[ParentCoreWitness] = []
    row_seconds: list[float] = []

    def collect(
        results: Iterable[tuple[DirectionOutcome, ParentCoreWitness | None, float]],
    ) -> None:
        for index, (outcome, witness, elapsed) in zip(selected, results, strict=True):
            if witness is not None:
                refutations.append(witness)
            outcomes.append(outcome)
            row_seconds.append(elapsed)
            if progress is not None:
                progress(index, outcome, elapsed)

    if workers == 1:
        collect(_decide_row(certificate, data, index, threshold) for index in selected)
    else:
        with ProcessPoolExecutor(
            max_workers=workers,
            mp_context=mp.get_context("spawn"),
            initializer=_prepare_worker,
            initargs=(certificate, data, threshold),
        ) as pool:
            # Python 3.14 bounds submitted work here: catalogue size cannot
            # cause thousands of outstanding pickled certificate tasks.
            collect(pool.map(_worker_row, selected, buffersize=workers))
    return ParentCoreIntervalVerdict(
        premises,
        selected,
        tuple(outcomes),
        data.scale,
        threshold,
        tuple(refutations),
        tuple(row_seconds),
    )
