"""Threshold atoms: the inclusion--exclusion grid is the direct count grid, cell for cell.

`threshold.charge_grid` adds a threshold atom to the sweep's difference array as signed
rectangle terms; `threshold.charge_grid_direct` thresholds one count grid per atom and
shares nothing with it past the event grid. These tests hold the two equal on random
instances, hold point atoms written as ``1-of-1`` threshold atoms to
`sweep.minimum_covered_mass` value and witness, and check the refusals and the symmetry
condition the theorem needs.
"""

from __future__ import annotations

import random
import sys
import threading
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from fractions import Fraction
from math import comb

import pytest

from sqpack.fractional import threshold as threshold_module
from sqpack.fractional.certificate import Certificate, d4_images, verify
from sqpack.fractional.generate import net_half_tangents
from sqpack.fractional.model import Atom, rotation_from_half_tangent
from sqpack.fractional.sweep import minimum_covered_mass
from sqpack.fractional.threshold import (
    MAX_EXPANSION_SUBSETS,
    ThresholdAtom,
    ThresholdCertificate,
    charge_grid,
    charge_grid_direct,
    closed_form_threshold_conditions,
    exact_charge,
    expansion_terms,
    least_charged_cells,
    least_charged_slabs,
    minimum_charge,
    preflight_expansion,
    rectangle_terms,
    sweep_all_threshold_directions,
    sweep_slabs,
    threshold_weight_scale,
    verify_threshold,
)

SIDE = Fraction(3)
SQUARE = Fraction(9, 10)
NET = net_half_tangents(Fraction(207107, 500000), 6)
DIRECTIONS = tuple(rotation_from_half_tangent(str(k), t) for k, t in enumerate(NET))


def _point(rng: random.Random) -> tuple[Fraction, Fraction]:
    return Fraction(rng.randint(2, 28), 10), Fraction(rng.randint(2, 28), 10)


def _instance(seed: int) -> tuple[tuple[Atom, ...], tuple[ThresholdAtom, ...]]:
    rng = random.Random(seed)
    atoms = tuple(
        Atom(f"{k}", *_point(rng), Fraction(rng.randint(1, 9), 12)) for k in range(12)
    )
    shapes = ((3, 2), (4, 3), (5, 2), (5, 3), (5, 4), (2, 1), (4, 2), (6, 4))
    threshold_atoms = []
    for size, threshold in shapes:
        points: list[tuple[Fraction, Fraction]] = []
        while len(points) < size:
            candidate = _point(rng)
            if candidate not in points:
                points.append(candidate)
        threshold_atoms.append(
            ThresholdAtom(tuple(points), threshold, Fraction(rng.randint(1, 9), 8))
        )
    return atoms, tuple(threshold_atoms)


def test_the_expansion_identity_holds_for_every_trace_size() -> None:
    for size in range(1, 8):
        for threshold in range(1, size + 1):
            terms = expansion_terms(size, threshold)
            for m in range(size + 1):
                value = sum(coefficient * comb(m, j) for j, coefficient in terms)
                assert value == (1 if m >= threshold else 0)


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_inclusion_exclusion_matches_the_direct_count_grid(seed: int) -> None:
    atoms, threshold_atoms = _instance(seed)
    scale = threshold_weight_scale(atoms, threshold_atoms)
    for direction in DIRECTIONS:
        fast = charge_grid(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
        slow = charge_grid_direct(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
        assert fast.reduction == slow.reduction
        assert (fast.grid == slow.grid).all()
        assert fast.grid.min() >= 0


def test_point_atoms_as_threshold_atoms_reproduce_the_sweep() -> None:
    atoms, _ = _instance(7)
    as_threshold = tuple(ThresholdAtom(((a.x, a.y),), 1, a.weight) for a in atoms)
    for direction in DIRECTIONS:
        expected = minimum_covered_mass(atoms, direction, SIDE, SQUARE)
        got = minimum_charge((), as_threshold, direction, SIDE, SQUARE)
        assert got == expected
        mixed = minimum_charge(atoms[:5], as_threshold[5:], direction, SIDE, SQUARE)
        assert mixed == expected


def test_the_minimum_cell_charge_agrees_with_an_exact_membership_count() -> None:
    atoms, threshold_atoms = _instance(11)
    direction = DIRECTIONS[3]
    minimum, (cu, cv) = minimum_charge(atoms, threshold_atoms, direction, SIDE, SQUARE)
    half = SQUARE / 2

    def contains(x: Fraction, y: Fraction) -> bool:
        u = direction.ux * x + direction.uy * y
        v = direction.vx * x + direction.vy * y
        return abs(u - cu) <= half and abs(v - cv) <= half

    assert exact_charge(atoms, threshold_atoms, contains) == minimum


def test_least_charged_cells_are_ordered_and_start_at_the_minimum() -> None:
    atoms, threshold_atoms = _instance(5)
    direction = DIRECTIONS[2]
    scale = threshold_weight_scale(atoms, threshold_atoms)
    grid = charge_grid(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
    minimum, witness = minimum_charge(atoms, threshold_atoms, direction, SIDE, SQUARE)
    found = least_charged_cells(grid, direction, SIDE, SQUARE, keep=5, below=Fraction(100))
    assert len(found) == 5
    assert found[0] == (minimum, witness)
    assert [f[0] for f in found] == sorted(f[0] for f in found)
    assert least_charged_cells(grid, direction, SIDE, SQUARE, keep=5, below=minimum) == []


def test_budgets_and_refusals() -> None:
    p = tuple((Fraction(k), Fraction(1)) for k in range(5))
    assert ThresholdAtom(p[:3], 2, Fraction(3, 4)).budget == Fraction(3, 4)
    assert ThresholdAtom(p, 2, Fraction(3, 4)).budget == Fraction(3, 2)
    assert ThresholdAtom(p, 3, Fraction(3, 4)).budget == Fraction(3, 4)
    assert ThresholdAtom(p[:1], 1, Fraction(3, 4)).budget == Fraction(3, 4)
    for points, threshold, weight in (
        (p[:3], 2, Fraction(-1, 4)),
        (p[:3], 0, Fraction(1)),
        (p[:3], 4, Fraction(1)),
        ((p[0], p[0], p[1]), 2, Fraction(1)),
        ((), 1, Fraction(1)),
    ):
        try:
            ThresholdAtom(points, threshold, weight)
        except ValueError:
            continue
        raise AssertionError(f"{(points, threshold, weight)} was accepted")


def _symmetric_threshold_certificate(
    weight: Fraction, *, drop_image: bool = False
) -> ThresholdCertificate:
    centre = SIDE / 2
    seeds = (
        (Fraction(1, 2), Fraction(3, 4), Fraction(1, 3)),
        (Fraction(1), Fraction(5, 4), Fraction(1, 2)),
    )
    sites: dict[tuple[Fraction, Fraction], Fraction] = {}
    for x, y, w in seeds:
        for image in d4_images(x, y, SIDE):
            sites[image] = w
    atoms = tuple(Atom(f"{k}", x, y, w) for k, ((x, y), w) in enumerate(sorted(sites.items())))
    base = ThresholdAtom(
        ((Fraction(1, 2), Fraction(1, 2)), (Fraction(1), centre), (centre, Fraction(1))),
        2,
        weight,
    )
    orbit = list(base.orbit(SIDE))
    if drop_image:
        orbit = orbit[:-1]
    return ThresholdCertificate(
        n=12,
        outer_side=SIDE,
        square_side=SQUARE,
        atoms=atoms,
        threshold_atoms=tuple(orbit),
        half_tangents=NET,
    )


def test_symmetry_condition_detects_a_missing_image() -> None:
    whole = _symmetric_threshold_certificate(Fraction(1, 5))
    reports = closed_form_threshold_conditions(whole)
    assert [r.holds for r in reports] == [True, True, True, True, True]
    assert whole.total_budget == whole.point_mass + len(whole.threshold_atoms) * Fraction(1, 5)
    broken = _symmetric_threshold_certificate(Fraction(1, 5), drop_image=True)
    reports = closed_form_threshold_conditions(broken)
    assert not reports[1].holds
    assert "no matching image" in reports[1].detail


def test_zero_weight_threshold_atoms_leave_the_point_verdict_unchanged() -> None:
    certificate = _symmetric_threshold_certificate(Fraction(0))
    point = verify(certificate.point_certificate, workers=1)
    threshold = verify_threshold(certificate)
    assert threshold.minimum_cell_mass == point.minimum_cell_mass
    assert threshold.worst_direction == point.worst_direction
    assert threshold.accepted == point.accepted
    assert threshold.total_mass == point.total_mass


class _ThreadPoolAdapter:
    """Exercise the bounded process scheduler portably with shared-state initialization."""

    def __init__(
        self,
        *,
        max_workers: int,
        mp_context: object,
        initializer: Callable[..., None] | None = None,
        initargs: tuple[object, ...] = (),
    ) -> None:
        del mp_context
        if initializer is not None:
            initializer(*initargs)
        self._pool = ThreadPoolExecutor(max_workers=max_workers)

    def submit(
        self, function: Callable[[int], tuple[int, Fraction, str]], index: int
    ) -> Future[tuple[int, Fraction, str]]:
        return self._pool.submit(function, index)

    def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
        self._pool.shutdown(wait=wait, cancel_futures=cancel_futures)

    def terminate_workers(self) -> None:
        self._pool.shutdown(wait=True, cancel_futures=True)


def test_parallel_threshold_progress_lands_out_of_order_but_returns_net_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _symmetric_threshold_certificate(Fraction(0))
    release_first = threading.Event()
    progress: list[int] = []

    def direction(index: int) -> tuple[int, Fraction, str]:
        if index == 0:
            assert release_first.wait(timeout=2)
        return index, Fraction(index + 1), certificate.directions[index].label

    def landed(index: int, _minimum: Fraction, _label: str) -> None:
        progress.append(index)
        release_first.set()

    monkeypatch.setattr(threshold_module.sys, "platform", "linux")
    monkeypatch.setattr(threshold_module, "ProcessPoolExecutor", _ThreadPoolAdapter)
    monkeypatch.setattr(threshold_module, "_shared_direction_minimum", direction)
    outcomes = sweep_all_threshold_directions(certificate, workers=2, progress=landed)

    assert progress[0] != 0
    assert outcomes == tuple(
        (Fraction(index + 1), direction.label)
        for index, direction in enumerate(certificate.directions)
    )


def test_parallel_threshold_callback_failure_retains_the_completed_batch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _symmetric_threshold_certificate(Fraction(0))
    submitted: list[int] = []
    terminated: list[bool] = []

    class ImmediateExecutor:
        def __init__(self, **_kwargs: object) -> None:
            pass

        def submit(
            self, function: Callable[[int], tuple[int, Fraction, str]], index: int
        ) -> Future[tuple[int, Fraction, str]]:
            del function
            submitted.append(index)
            future: Future[tuple[int, Fraction, str]] = Future()
            future.set_result((index, Fraction(index + 1), str(index)))
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            raise AssertionError(f"unexpected normal shutdown: {wait}, {cancel_futures}")

        def terminate_workers(self) -> None:
            terminated.append(True)

    progress: list[int] = []

    def fail(index: int, _minimum: Fraction, _label: str) -> None:
        progress.append(index)
        raise RuntimeError("checkpoint deadline")

    monkeypatch.setattr(threshold_module.sys, "platform", "linux")
    monkeypatch.setattr(threshold_module, "ProcessPoolExecutor", ImmediateExecutor)
    with pytest.raises(RuntimeError, match="checkpoint deadline"):
        sweep_all_threshold_directions(certificate, workers=2, progress=fail)

    assert submitted == [0, 1, 2, 3]
    assert progress == submitted
    assert terminated == [True]


def test_parallel_threshold_deadline_cancels_the_bounded_window(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _symmetric_threshold_certificate(Fraction(0))
    futures: list[Future[tuple[int, Fraction, str]]] = []
    terminated: list[bool] = []

    class PendingExecutor:
        def __init__(self, **_kwargs: object) -> None:
            pass

        def submit(
            self, function: Callable[[int], tuple[int, Fraction, str]], index: int
        ) -> Future[tuple[int, Fraction, str]]:
            del function, index
            future: Future[tuple[int, Fraction, str]] = Future()
            futures.append(future)
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            raise AssertionError(f"unexpected normal shutdown: {wait}, {cancel_futures}")

        def terminate_workers(self) -> None:
            terminated.append(True)

    monkeypatch.setattr(threshold_module.sys, "platform", "linux")
    monkeypatch.setattr(threshold_module, "ProcessPoolExecutor", PendingExecutor)
    monkeypatch.setattr(
        threshold_module, "wait", lambda *_args, **_kwargs: (set(), set(futures))
    )
    with pytest.raises(threshold_module.ThresholdSweepDeadlineError, match="absolute deadline"):
        sweep_all_threshold_directions(
            certificate,
            workers=2,
            deadline=1.0,
            clock=lambda: 0.0,
        )

    assert len(futures) == 4
    assert all(future.cancelled() for future in futures)
    assert terminated == [True]


def test_bounded_parallel_threshold_sweep_matches_serial(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _symmetric_threshold_certificate(Fraction(0))
    serial = sweep_all_threshold_directions(certificate, workers=1)
    monkeypatch.setattr(threshold_module.sys, "platform", "linux")
    monkeypatch.setattr(threshold_module, "ProcessPoolExecutor", _ThreadPoolAdapter)
    parallel = sweep_all_threshold_directions(certificate, workers=2)
    assert parallel == serial


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="fork pool is Linux-only")
def test_real_forked_threshold_sweep_matches_serial() -> None:
    certificate = _symmetric_threshold_certificate(Fraction(0))
    assert sweep_all_threshold_directions(certificate, workers=2) == (
        sweep_all_threshold_directions(certificate, workers=1)
    )


def test_duplicate_threshold_atoms_are_refused() -> None:
    whole = _symmetric_threshold_certificate(Fraction(1, 5))
    try:
        ThresholdCertificate(
            n=12,
            outer_side=SIDE,
            square_side=SQUARE,
            atoms=whole.atoms,
            threshold_atoms=(*whole.threshold_atoms, whole.threshold_atoms[0]),
            half_tangents=NET,
        )
    except ValueError:
        return
    raise AssertionError("a repeated (points, threshold) was accepted")


def test_the_record_round_trips() -> None:
    whole = _symmetric_threshold_certificate(Fraction(2, 7))
    record = whole.to_record()
    rebuilt = tuple(ThresholdAtom.from_record(r) for r in record["threshold_atoms"])
    assert rebuilt == whole.threshold_atoms
    assert Fraction(record["total_budget"]) == whole.total_budget
    assert isinstance(Certificate, type)


@pytest.mark.parametrize("seed", [4, 8])
def test_the_slab_sweep_reads_the_dense_grid_slab_for_slab(seed: int) -> None:
    atoms, threshold_atoms = _instance(seed)
    scale = threshold_weight_scale(atoms, threshold_atoms)
    for direction in DIRECTIONS:
        grid = charge_grid(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
        terms = rectangle_terms(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
        scores, cells = sweep_slabs(terms)
        for k, (i, j0, j1) in enumerate(grid.reduction.spans):
            column = grid.grid[i, j0 : j1 + 1]
            assert scores[k] == column.min()
            assert tuple(cells[k]) == (i, j0 + int(column.argmin()))
        dense = minimum_charge(atoms, threshold_atoms, direction, SIDE, SQUARE)
        slab = minimum_charge(
            atoms, threshold_atoms, direction, SIDE, SQUARE, dense_cell_limit=0
        )
        assert dense == slab


class _SubsetWorkError(AssertionError):
    """The expansion started enumerating: the refusal came too late."""


def _forbid_expansion(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sentinels on every helper whose cost grows with tokens or subsets (PR157-MATH-05)."""

    def tripped(name: str) -> Callable[..., object]:
        def trip(*_args: object, **_kwargs: object) -> object:
            raise _SubsetWorkError(name)

        return trip

    monkeypatch.setattr(ThresholdAtom, "token_sites", property(tripped("token_sites")))
    for name in ("expansion_terms", "absolute_expansion_sum", "combinations"):
        monkeypatch.setattr(threshold_module, name, tripped(name))


def _all_ones(tokens: int, threshold: int) -> ThresholdAtom:
    """An ordinary unweighted atom on ``tokens`` distinct sites inside the container."""

    points = tuple((Fraction(2 + k % 26, 10), Fraction(2 + k // 26, 10)) for k in range(tokens))
    return ThresholdAtom(points, threshold, Fraction(1, 8))


@pytest.mark.parametrize(
    ("tokens", "threshold", "subsets"),
    [(30, 15, 614_429_672), (40, 20, 618_679_078_298)],
)
def test_the_half_threshold_term_explosion_is_refused_before_enumeration(
    monkeypatch: pytest.MonkeyPatch, tokens: int, threshold: int, subsets: int
) -> None:
    """The finding's modest atoms: they pass the ``int64`` headroom and still emit ``6.1e8``
    and ``6.2e11`` subsets. They are ordinary all-ones atoms, so this is not about weights."""

    atom = _all_ones(tokens, threshold)
    assert sum(comb(tokens, j) for j in range(threshold, tokens + 1)) == subsets
    mass = sum(abs(c) * comb(tokens, j) for j, c in expansion_terms(tokens, threshold))
    assert mass * 8 < 2**60  # the headroom check alone admits it at weight 1/8
    _forbid_expansion(monkeypatch)
    with pytest.raises(ValueError, match=rf"\b{MAX_EXPANSION_SUBSETS}\b"):
        rectangle_terms((), (atom,), DIRECTIONS[0], SIDE, SQUARE, scale=8)


def test_the_subset_cap_admits_atoms_exactly_at_it_and_refuses_one_past() -> None:
    """At the shipped value, summed across atoms: ``(m, 1)`` has ``2^m - 1`` subsets, and
    a one-token atom adds exactly one more."""

    cap = MAX_EXPANSION_SUBSETS
    m = cap.bit_length() - 1
    assert cap == 2**m, "the subset cap is a power of two, so it is reachable exactly"
    wide = _all_ones(m, 1)
    single = ThresholdAtom(((Fraction(29, 10), Fraction(29, 10)),), 1, Fraction(1))
    other = ThresholdAtom(((Fraction(28, 10), Fraction(29, 10)),), 1, Fraction(1))
    assert preflight_expansion((wide,)) == cap - 1
    assert preflight_expansion((wide, single)) == cap
    with pytest.raises(ValueError, match=rf"{cap + 1} token subsets.*\b{cap}\b"):
        preflight_expansion((wide, single, other))
    # Zero-weight atoms enumerate nothing, so they never count against the cap.
    idle = ThresholdAtom(other.points, 1, Fraction(0))
    assert preflight_expansion((wide, single, idle)) == cap


def test_the_subset_cap_is_inclusive_on_the_full_route(monkeypatch: pytest.MonkeyPatch) -> None:
    """A lowered cap, so the full expansion can run at equality: 22 subsets of 6-choose-4."""

    atom = _all_ones(6, 4)
    assert preflight_expansion((atom,)) == 22
    monkeypatch.setattr(threshold_module, "MAX_EXPANSION_SUBSETS", 22)
    at_cap = charge_grid((), (atom,), DIRECTIONS[0], SIDE, SQUARE, scale=8)
    direct = charge_grid_direct((), (atom,), DIRECTIONS[0], SIDE, SQUARE, scale=8)
    assert (at_cap.grid == direct.grid).all()
    monkeypatch.setattr(threshold_module, "MAX_EXPANSION_SUBSETS", 21)
    _forbid_expansion(monkeypatch)
    with pytest.raises(ValueError, match=r"22 token subsets.*\b21\b"):
        charge_grid((), (atom,), DIRECTIONS[0], SIDE, SQUARE, scale=8)


def _explosive_certificate() -> ThresholdCertificate:
    """The symmetric certificate plus one 30-token, threshold-15 atom at the centre."""

    base = _symmetric_threshold_certificate(Fraction(1, 5))
    centre = SIDE / 2
    explosive = ThresholdAtom(((centre, centre),), 15, Fraction(1, 8), (30,))
    return ThresholdCertificate(
        n=base.n,
        outer_side=SIDE,
        square_side=SQUARE,
        atoms=base.atoms,
        threshold_atoms=(*base.threshold_atoms, explosive),
        half_tangents=NET,
    )


def _expanding_routes(certificate: ThresholdCertificate) -> dict[str, Callable[[], object]]:
    """Every public entry point that expands, each applied to the same certificate."""

    atoms, threshold_atoms = certificate.atoms, certificate.threshold_atoms
    direction = DIRECTIONS[0]
    scale = threshold_weight_scale(atoms, threshold_atoms)
    arguments = (atoms, threshold_atoms, direction, SIDE, SQUARE)
    reader = {"keep": 1, "below": Fraction(1)}
    return {
        "preflight_expansion": lambda: preflight_expansion(threshold_atoms),
        "rectangle_terms": lambda: rectangle_terms(*arguments, scale=scale),
        "charge_grid": lambda: charge_grid(*arguments, scale=scale),
        "least_charged_cells": lambda: least_charged_cells(
            charge_grid(*arguments, scale=scale), direction, SIDE, SQUARE, **reader
        ),
        "least_charged_slabs": lambda: least_charged_slabs(
            rectangle_terms(*arguments, scale=scale), direction, SIDE, SQUARE, **reader
        ),
        "minimum_charge": lambda: minimum_charge(*arguments),
        "sweep_all_threshold_directions": lambda: sweep_all_threshold_directions(
            certificate, workers=2
        ),
        "verify_threshold": lambda: verify_threshold(certificate, workers=2),
    }


@pytest.mark.parametrize(
    "route",
    [
        "preflight_expansion",
        "rectangle_terms",
        "charge_grid",
        "least_charged_cells",
        "least_charged_slabs",
        "minimum_charge",
        "sweep_all_threshold_directions",
        "verify_threshold",
    ],
)
def test_every_expanding_route_refuses_before_it_enumerates(
    monkeypatch: pytest.MonkeyPatch, route: str
) -> None:
    """One preflight, reached from every public route that expands.

    The sweep and the verifier must refuse before a single direction runs or a worker pool
    exists, so both are asked for two workers on a platform that would fork them.
    """

    certificate = _explosive_certificate()
    _forbid_expansion(monkeypatch)
    monkeypatch.setattr(threshold_module, "_direction_minimum", _refuse_call("direction"))
    monkeypatch.setattr(threshold_module.sys, "platform", "linux")
    monkeypatch.setattr(threshold_module, "ProcessPoolExecutor", _refuse_call("pool"))
    with pytest.raises(ValueError, match=rf"\b{MAX_EXPANSION_SUBSETS}\b"):
        _expanding_routes(certificate)[route]()


def _refuse_call(name: str) -> Callable[..., object]:
    def refuse(*_args: object, **_kwargs: object) -> object:
        raise _SubsetWorkError(name)

    return refuse


def test_exact_charge_counts_tokens_by_membership_and_expands_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The control for the refusals: the same atom stays usable where it costs O(sites)."""

    certificate = _explosive_certificate()
    explosive = certificate.threshold_atoms[-1]
    centre = SIDE / 2
    _forbid_expansion(monkeypatch)

    def at_centre(x: Fraction, y: Fraction) -> bool:
        return (x, y) == (centre, centre)

    assert exact_charge(certificate.atoms, (explosive,), at_centre) == Fraction(1, 8)
    assert exact_charge((), (explosive,), lambda _x, _y: False) == 0
