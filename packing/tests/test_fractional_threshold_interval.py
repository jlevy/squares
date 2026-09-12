"""Controls for the interval-certified decision of threshold certificates.

The exact sweep and this route must agree, and agreement alone is not the control: two
decisions that could only fail the same way would agree while both wrong. So the bounds
are checked against exact rational membership counts at sampled centres, the enclosure
is held to the sweep's minimum and to the direct count grid at every direction of a
doubled net, a lowered weight is watched being refused, the drop-rather-than-assume rule
is exercised on a box a threshold atom only partly resolves, the one thing the method
cannot decide -- a threshold atom's own seam -- is exhibited and reported as undecided,
and a pure point certificate is shown to take, number for number, the point route's own
path.
"""

# These tests exercise the private scheduler because completion order and cleanup are
# intentionally not part of the public verdict API.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import random
import sys
import threading
from collections.abc import Callable
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor
from fractions import Fraction
from itertools import combinations
from multiprocessing.process import BaseProcess
from typing import Literal, cast
from unittest.mock import patch

import numpy as np
import pytest

from cases.n11_fractional_certificate.replay import STROMQUIST_RUNG_PATH
from cases.n11_fractional_certificate.replay import load as load_n11
from sqpack.fractional import threshold_interval
from sqpack.fractional.certificate import d4_images
from sqpack.fractional.generate import net_half_tangents
from sqpack.fractional.interval import (
    BATCH,
    DirectionOutcome,
    IntervalInputError,
    Rotation,
    doubled_net,
    verify_by_intervals,
)
from sqpack.fractional.model import Atom, Direction, rotation_from_half_tangent
from sqpack.fractional.threshold import (
    ThresholdAtom,
    ThresholdCertificate,
    charge_grid_direct,
    exact_charge,
    minimum_charge,
    threshold_weight_scale,
)
from sqpack.fractional.threshold_interval import (
    CONDITION_5,
    MAX_MEMBER_SLOTS,
    ThresholdAtomData,
    ThresholdDirectionSearch,
    exact_charge_at_witness,
    exact_rotation,
    scaled_threshold_masses,
    threshold_searches,
    verify_threshold_by_intervals,
)

SIDE = Fraction(3)
SQUARE = Fraction(9, 10)
NET = net_half_tangents(Fraction(207107, 500000), 6)
DOUBLED = tuple(str(k) for k in range(7)) + tuple(f"{k}'" for k in range(1, 7))

# A sub-net of the 19/5 rung's doubled net: both ends, an oblique direction and its
# reflection. A control, not a claim; it keeps the pure-point comparison quick.
POINT_SUB_NET = ("0", "57", "1'", "180'")

# Coordinates are placed on an odd prime denominator so that no two atom points sit at
# distance exactly B = 9/10 along an axis, which is the seam the method cannot close.
DENOMINATOR = 9973


def _search(certificate: ThresholdCertificate, label: str) -> ThresholdDirectionSearch:
    for search in threshold_searches(certificate, ThresholdAtomData.of(certificate)):
        if search.label == label:
            return search
    raise KeyError(label)


def _direction(certificate: ThresholdCertificate, label: str) -> Direction:
    cosine, sine = exact_rotation(certificate, label)
    return Direction(label, cosine, sine, -sine, cosine)


def _membership(
    certificate: ThresholdCertificate, label: str, centre: tuple[Fraction, Fraction]
) -> Callable[[Fraction, Fraction], bool]:
    """The exact closed-core membership test at a centre in the rotated frame."""
    cosine, sine = exact_rotation(certificate, label)
    u, v = centre
    half = certificate.square_side / 2

    def contains(x: Fraction, y: Fraction) -> bool:
        return abs(cosine * x + sine * y - u) <= half and abs(cosine * y - sine * x - v) <= half

    return contains


# --- fixtures ----------------------------------------------------------------------


def _cluster_certificate(
    *, seed: int = 20260909, weight: Fraction = Fraction(1, 4)
) -> ThresholdCertificate:
    """Thirty-six threshold atoms of mixed shape whose clusters cover every core.

    Cluster centres sit on the D4-symmetric grid ``1/2 + 2i/5``, ``i = 0..5``; each
    cluster's points are jittered by at most ``1/20``. Any admissible centre at any
    direction is within ``1/5`` per axis of some cluster centre, so every point of that
    cluster is within ``0.354 < 9/20`` of it and inside the core: the least charge is
    positive everywhere, and it is a threshold atom that carries it. Six orbit
    representatives of shapes 2-of-3, 3-of-4, 2-of-5, 3-of-5 and 4-of-5 are expanded to
    their D4 orbits, with one D4 orbit of point atoms beside them.
    """
    rng = random.Random(seed)
    grid = [Fraction(1, 2) + Fraction(2, 5) * i for i in range(6)]
    representatives = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
    shapes = ((3, 2), (4, 3), (5, 2), (3, 2), (4, 3), (5, 4))
    seen: dict[tuple[tuple[tuple[Fraction, Fraction], ...], int], ThresholdAtom] = {}
    for (i, j), (size, threshold) in zip(representatives, shapes, strict=True):
        points: list[tuple[Fraction, Fraction]] = []
        while len(points) < size:
            point = (
                grid[i] + Fraction(rng.randint(-498, 498), DENOMINATOR),
                grid[j] + Fraction(rng.randint(-498, 498), DENOMINATOR),
            )
            if point not in points:
                points.append(point)
        for image in ThresholdAtom(tuple(points), threshold, weight).orbit(SIDE):
            seen.setdefault(image.key, image)
    sites = {
        image: Fraction(1, 3)
        for image in d4_images(Fraction(1, 2), Fraction(3, 4) + Fraction(1, DENOMINATOR), SIDE)
    }
    atoms = tuple(Atom(f"{k}", x, y, w) for k, ((x, y), w) in enumerate(sorted(sites.items())))
    return ThresholdCertificate(
        n=100,
        outer_side=SIDE,
        square_side=SQUARE,
        atoms=atoms,
        threshold_atoms=tuple(seen.values()),
        half_tangents=NET,
    )


def rescaled(certificate: ThresholdCertificate, factor: Fraction) -> ThresholdCertificate:
    return ThresholdCertificate(
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
        atoms=tuple(Atom(a.label, a.x, a.y, a.weight * factor) for a in certificate.atoms),
        threshold_atoms=tuple(
            ThresholdAtom(t.points, t.threshold, t.weight * factor)
            for t in certificate.threshold_atoms
        ),
        half_tangents=certificate.half_tangents,
    )


def _exact_minimum(certificate: ThresholdCertificate) -> tuple[Fraction, str]:
    worst: Fraction | None = None
    label = ""
    for name in DOUBLED:
        value, _ = minimum_charge(
            certificate.atoms,
            certificate.threshold_atoms,
            _direction(certificate, name),
            certificate.outer_side,
            certificate.square_side,
        )
        if worst is None or value < worst:
            worst, label = value, name
    assert worst is not None
    return worst, label


def tight_certificate() -> ThresholdCertificate:
    """The cluster certificate with its weights scaled so the least charge is exactly 1."""
    certificate = _cluster_certificate()
    minimum, _ = _exact_minimum(certificate)
    assert minimum > 0
    return rescaled(certificate, 1 / minimum)


def _tiling(overlap: Fraction) -> ThresholdCertificate:
    """2-of-3 atoms whose points sit at spacing ``B/2`` along ``x``, tiled over a small
    container, with rows along ``y``.

    With ``B = 1/2`` an atom at ``a`` with points ``a, a + 1/4, a + 1/2 - overlap`` is
    charged for every centre ``x`` in ``[a, a + 1/2]``: on the first half by its first two
    points and on the second by its last two. At ``overlap = 0`` the first point leaves
    the core exactly where the third enters -- a seam across which the charge is constant
    at 1 and no enclosure can close; at a positive ``overlap`` the two regions overlap by
    that much and every box resolves. Atoms start every ``1/2 - overlap`` so adjacent
    ones overlap by the same amount, and rows are spaced ``1/4 - 1/97`` so that no
    region edge lies on the domain edge.
    """
    epsilon = Fraction(1, 97)
    side, square = Fraction(3, 2), Fraction(1, 2)
    starts = [5 * epsilon + i * (square - overlap) for i in range(3)]
    rows = [square / 2 + r * (square / 2 - epsilon) for r in range(5)]
    atoms: list[ThresholdAtom] = []
    for y in rows:
        for a in starts:
            points = ((a, y), (a + square / 2, y), (a + square - overlap, y))
            atoms.append(ThresholdAtom(points, 2, Fraction(1)))
    return ThresholdCertificate(
        n=1000,
        outer_side=side,
        square_side=square,
        atoms=(),
        threshold_atoms=tuple(atoms),
        half_tangents=(Fraction(0), Fraction(1, 2)),
    )


def _as_threshold(certificate) -> ThresholdCertificate:
    """A point certificate carried unchanged into the threshold representation."""
    return ThresholdCertificate(
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
        atoms=certificate.atoms,
        threshold_atoms=(),
        half_tangents=certificate.half_tangents,
    )


# --- the bounds, against exact arithmetic ------------------------------------------


def test_box_bounds_bracket_the_exact_charge_at_sampled_centres() -> None:
    """A lower bound over a box and an upper bound at a point, both exact-checked.

    The sampled centres are floats, so their positions are exact rationals and the
    charge there is a membership count in ``Fraction`` arithmetic through
    `threshold.exact_charge`, the theorem's own definition. The interval lower bound of
    any small box around the point must not exceed it, and the point upper bound must
    not fall below it.
    """
    certificate = _cluster_certificate()
    rng = np.random.default_rng(11)
    for label in ("0", "3", "3'", "6'"):
        search = _search(certificate, label)
        low = search.initial[0]
        us = rng.uniform(low[0], low[1], 150)
        vs = rng.uniform(low[2], low[3], 150)
        radius = rng.uniform(0, 0.02, 150)
        boxes = np.stack([us - radius, us + radius, vs - radius, vs + radius], axis=1)
        lower = search.lower_bound(boxes)
        upper = search.upper_bound_at(us, vs)
        admissible = 0
        for k in range(150):
            centre = (Fraction(us[k]), Fraction(vs[k]))
            exact = exact_charge(
                certificate.atoms,
                certificate.threshold_atoms,
                _membership(certificate, label, centre),
            )
            assert Fraction(int(lower[k]), search.scale) <= exact
            assert exact <= Fraction(int(upper[k]), search.scale)
            # The samples fill the domain's bounding box, which at an oblique direction
            # reaches outside the container; every admissible core holds a whole cluster.
            if exact_charge_at_witness(certificate, label, (us[k], vs[k])).admissible:
                admissible += 1
                assert exact > 0
        assert admissible > 60


def test_the_witness_charge_is_the_theorem_definition_at_a_float_centre() -> None:
    """`exact_charge_at_witness` and `threshold.exact_charge` count the same thing."""
    certificate = _cluster_certificate()
    rng = random.Random(4)
    for label in ("0", "2", "5'"):
        search = _search(certificate, label)
        low = search.initial[0]
        for _ in range(40):
            witness = (rng.uniform(low[0], low[1]), rng.uniform(low[2], low[3]))
            centre = (Fraction(witness[0]), Fraction(witness[1]))
            expected = exact_charge(
                certificate.atoms,
                certificate.threshold_atoms,
                _membership(certificate, label, centre),
            )
            assert exact_charge_at_witness(certificate, label, witness).charge == expected


def test_exact_rotations_are_the_net_and_its_reflection() -> None:
    certificate = _cluster_certificate()
    for index, tangent in enumerate(NET):
        direction = rotation_from_half_tangent(str(index), tangent)
        assert exact_rotation(certificate, str(index)) == (direction.ux, direction.uy)
        assert exact_rotation(certificate, f"{index}'") == (direction.uy, direction.ux)


def test_a_partly_resolved_point_is_dropped_rather_than_assumed() -> None:
    """A 2-of-3 atom counts for a box only when two of its points surely lie in every
    core of the box; a point whose region the box straddles is not one of them.

    At direction 0 the rotation is exact, so the regions are ``[x - 9/20, x + 9/20]``
    to within an ulp. The atom's points sit at ``x = 1, 3/2, 2`` on the line ``y = 1``.
    """
    points = (
        (Fraction(1), Fraction(1)),
        (Fraction(3, 2), Fraction(1)),
        (Fraction(2), Fraction(1)),
    )
    atom = ThresholdAtom(points, 2, Fraction(1))
    loose = ThresholdAtom(atom.points, 1, Fraction(1))
    certificate = ThresholdCertificate(
        n=10,
        outer_side=SIDE,
        square_side=SQUARE,
        atoms=(),
        threshold_atoms=(atom,),
        half_tangents=NET,
    )
    search = _search(certificate, "0")
    boxes = np.array(
        [
            # Inside the first point's region [0.55, 1.45], across the second's enter
            # edge at 1.05, outside the third's: one point resolved, so no charge.
            [1.00, 1.10, 0.90, 1.10],
            # Inside the first two regions: charged.
            [1.10, 1.20, 0.90, 1.10],
            # Across the first point's leave edge at 1.45 with the second inside: one.
            [1.40, 1.50, 0.90, 1.10],
            # Inside the second and third regions: charged.
            [1.60, 1.90, 0.90, 1.10],
            # Straddling the atom's line in v is fine; straddling a region's v edge is not.
            [1.10, 1.20, 1.40, 1.50],
        ]
    )
    assert search.lower_bound(boxes).tolist() == [0, 1, 0, 1, 0]
    # The same atom at threshold 1 charges the first and third boxes: one resolved
    # point is enough, which is exactly what makes the point route a special case.
    loose_search = _search(
        ThresholdCertificate(
            n=10,
            outer_side=SIDE,
            square_side=SQUARE,
            atoms=(),
            threshold_atoms=(loose,),
            half_tangents=NET,
        ),
        "0",
    )
    assert loose_search.lower_bound(boxes).tolist() == [1, 1, 1, 1, 0]
    # At a point the outer regions decide: a centre on the second region's enter edge
    # sees two points, one inside the first two regions sees two, one inside only the
    # first sees one and is not charged.
    us, vs = np.array([1.05, 1.2, 1.0]), np.array([1.0, 1.0, 1.0])
    assert search.upper_bound_at(us, vs).tolist() == [1, 1, 0]


# --- agreement with the exact decision -------------------------------------------------


def test_the_enclosure_pins_the_sweep_minimum_at_every_doubled_net_direction() -> None:
    """Lower and upper bounds meet at the exact minimum, direction by direction.

    The sweep's `minimum_charge` is the inclusion--exclusion route and
    `charge_grid_direct` the thresholded count grids; the enclosure must equal both, at
    the forward directions and at the reflected ones the sweep never sees in a verdict.
    """
    certificate = _cluster_certificate()
    scale = threshold_weight_scale(certificate.atoms, certificate.threshold_atoms)
    for label in DOUBLED:
        search = _search(certificate, label)
        outcome = search.search(prune_at=None)
        assert outcome.status == "certified", label
        assert outcome.stalled == 0
        assert outcome.lower is not None
        assert outcome.upper is not None
        direction = _direction(certificate, label)
        exact, _ = minimum_charge(
            certificate.atoms,
            certificate.threshold_atoms,
            direction,
            certificate.outer_side,
            certificate.square_side,
        )
        grid = charge_grid_direct(
            certificate.atoms,
            certificate.threshold_atoms,
            direction,
            certificate.outer_side,
            certificate.square_side,
            scale=scale,
        )
        direct = min(int(grid.grid[i, j0 : j1 + 1].min()) for i, j0, j1 in grid.reduction.spans)
        assert Fraction(direct, scale) == exact
        assert Fraction(outcome.lower, search.scale) == exact
        assert Fraction(outcome.upper, search.scale) == exact
        assert exact > 0


def test_the_full_doubled_net_accepts_the_tight_certificate_at_exactly_one() -> None:
    certificate = tight_certificate()
    verdict = verify_threshold_by_intervals(certificate, enclose=True)
    assert verdict.accepted, verdict.failures
    assert len(verdict.directions) == len(DOUBLED)
    assert all(o.status == "certified" for o in verdict.directions)
    assert sum(o.stalled for o in verdict.directions) == 0
    assert not any(o.budget_exhausted for o in verdict.directions)
    assert verdict.enclosure == (Fraction(1), Fraction(1))
    assert verdict.refutations == ()
    minimum, _ = _exact_minimum(certificate)
    assert minimum == 1


def test_a_lowered_threshold_weight_is_refused_and_the_witness_is_exact() -> None:
    """Condition 5' is tight at exactly 1, so a ten-thousandth off a threshold atom that
    charges the tightest cell is visible. Symmetry is not what catches it: this verifier
    never checks Condition 1', so the refusal has to come from the charge, and the
    refuting witness is re-evaluated in rational arithmetic before it counts.
    """
    certificate = tight_certificate()
    _, label = _exact_minimum(certificate)
    _, witness = minimum_charge(
        certificate.atoms,
        certificate.threshold_atoms,
        _direction(certificate, label),
        certificate.outer_side,
        certificate.square_side,
    )
    contains = _membership(certificate, label, witness)
    charged = [t for t in certificate.threshold_atoms if t.charge(contains) > 0]
    assert charged, "the tightest cell should be carried by a threshold atom"
    lightened = charged[0]
    threshold_atoms = tuple(
        ThresholdAtom(t.points, t.threshold, t.weight - Fraction(1, 10000))
        if t is lightened
        else t
        for t in certificate.threshold_atoms
    )
    lowered = ThresholdCertificate(
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
        atoms=certificate.atoms,
        threshold_atoms=threshold_atoms,
        half_tangents=certificate.half_tangents,
    )
    verdict = verify_threshold_by_intervals(lowered)
    assert verdict.failures == (CONDITION_5,)
    refuted = verdict.directions[-1]
    assert refuted.status == "refuted"
    assert refuted.upper is not None
    assert Fraction(refuted.upper, verdict.scale) < 1
    assert len(verdict.refutations) == 1
    refutation = verdict.refutations[0]
    assert refutation.label == refuted.label
    assert refutation.admissible
    assert refutation.charge < 1
    assert refutation.charge == Fraction(refuted.upper, verdict.scale)
    # Enclosure mode pins the lowered minimum and still refuses it (the point route's
    # D-435): a width-zero enclosure below 1 is not an acceptance.
    enclosed = verify_threshold_by_intervals(lowered, enclose=True, directions=(refuted.label,))
    assert enclosed.failures == (CONDITION_5,)
    assert not enclosed.accepted
    assert enclosed.directions[0].status == "certified"
    assert len(enclosed.refutations) == 1
    assert enclosed.refutations[0].charge == refutation.charge
    assert enclosed.refutations[0].admissible


def test_a_pure_point_certificate_takes_the_point_route_number_for_number() -> None:
    """On the retained 19/5 rung, with no threshold atom, the two routes are the same
    computation: the same boxes, the same stalls, the same bounds, the same witnesses.
    """
    point = load_n11(STROMQUIST_RUNG_PATH)
    assert len(point.atoms) == 425
    reference = verify_by_intervals(point, enclose=True, directions=POINT_SUB_NET)
    verdict = verify_threshold_by_intervals(
        _as_threshold(point), enclose=True, directions=POINT_SUB_NET
    )
    assert verdict.scale == reference.scale
    assert verdict.total_budget == reference.total_mass == Fraction(43391, 4000)
    assert verdict.directions == reference.directions
    assert (
        verdict.enclosure
        == reference.enclosure
        == (
            Fraction(50003, 50000),
            Fraction(50003, 50000),
        )
    )
    assert not verdict.accepted, "a sub-net run is a control, not a verdict"
    assert verdict.conditions[-1].status == "undecided"


def test_point_atoms_written_as_one_of_one_threshold_atoms_change_nothing() -> None:
    certificate = _cluster_certificate()
    rewritten = ThresholdCertificate(
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
        atoms=(),
        threshold_atoms=(
            *(ThresholdAtom(((a.x, a.y),), 1, a.weight) for a in certificate.atoms),
            *certificate.threshold_atoms,
        ),
        half_tangents=certificate.half_tangents,
    )
    original = verify_threshold_by_intervals(certificate, enclose=True)
    verdict = verify_threshold_by_intervals(rewritten, enclose=True)
    assert verdict.directions == original.directions
    assert verdict.total_budget == original.total_budget
    assert verdict.enclosure == original.enclosure


class _ThreadPoolAdapter:
    """Exercise the bounded parallel path portably without starting child processes."""

    def __init__(self, *, max_workers: int, mp_context: object) -> None:
        del mp_context
        self._pool = ThreadPoolExecutor(max_workers=max_workers)

    def submit(
        self, function: Callable[..., DirectionOutcome], *args: object
    ) -> Future[DirectionOutcome]:
        return self._pool.submit(function, *args)

    def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
        self._pool.shutdown(wait=wait, cancel_futures=cancel_futures)

    def terminate_workers(self) -> None:
        self._pool.shutdown(wait=True, cancel_futures=True)


def _synthetic_outcome(
    label: str, status: Literal["certified", "refuted", "undecided"] = "certified"
) -> DirectionOutcome:
    return DirectionOutcome(label, status, 1, 1, None, 1, 0)


def test_parallel_progress_observes_landings_but_returns_net_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:4]
    release_first = threading.Event()
    progress: list[str] = []

    def search(
        _data: ThresholdAtomData,
        _outer: object,
        _square: object,
        _prune_at: int | None,
        rotation: Rotation,
    ) -> DirectionOutcome:
        label = rotation.label
        if label == rotations[0].label:
            assert release_first.wait(timeout=2)
        return _synthetic_outcome(label)

    def landed(outcome: DirectionOutcome) -> None:
        progress.append(outcome.label)
        release_first.set()

    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", _ThreadPoolAdapter)
    monkeypatch.setattr(threshold_interval, "_search_direction", search)
    outcomes = threshold_interval._search_directions(  # noqa: SLF001
        certificate,
        data,
        rotations,
        prune_at=None,
        workers=2,
        progress=landed,
    )

    assert progress[0] != rotations[0].label
    assert [outcome.label for outcome in outcomes] == [rotation.label for rotation in rotations]


def test_parallel_early_refutation_keeps_the_input_order_prefix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:5]
    submitted: list[str] = []
    progress: list[str] = []
    shutdown: list[tuple[bool, bool]] = []
    terminated: list[bool] = []

    class ImmediateExecutor:
        def __init__(self, *, max_workers: int, mp_context: object) -> None:
            del max_workers, mp_context

        def submit(
            self, function: Callable[..., DirectionOutcome], *args: object
        ) -> Future[DirectionOutcome]:
            del function
            rotation = cast(Rotation, args[-1])
            submitted.append(rotation.label)
            future: Future[DirectionOutcome] = Future()
            status = "refuted" if rotation.label == rotations[1].label else "certified"
            future.set_result(_synthetic_outcome(rotation.label, status))
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            shutdown.append((wait, cancel_futures))

        def terminate_workers(self) -> None:
            terminated.append(True)

    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", ImmediateExecutor)
    outcomes = threshold_interval._search_directions(  # noqa: SLF001
        certificate,
        data,
        rotations,
        prune_at=1,
        workers=2,
        progress=lambda outcome: progress.append(outcome.label),
    )

    assert [outcome.label for outcome in outcomes] == [
        rotations[0].label,
        rotations[1].label,
    ]
    assert submitted == [rotation.label for rotation in rotations[:4]]
    assert progress == submitted
    assert shutdown == []
    assert terminated == [True]


def test_parallel_callback_failure_cancels_pending_work_without_waiting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:5]
    futures: list[Future[DirectionOutcome]] = []
    shutdown: list[tuple[bool, bool]] = []
    terminated: list[bool] = []

    class ControlledExecutor:
        def __init__(self, *, max_workers: int, mp_context: object) -> None:
            del max_workers, mp_context

        def submit(
            self, function: Callable[..., DirectionOutcome], *args: object
        ) -> Future[DirectionOutcome]:
            del function
            rotation = cast(Rotation, args[-1])
            future: Future[DirectionOutcome] = Future()
            if not futures:
                future.set_result(_synthetic_outcome(rotation.label))
            elif len(futures) == 1:
                assert future.set_running_or_notify_cancel()
            futures.append(future)
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            shutdown.append((wait, cancel_futures))

        def terminate_workers(self) -> None:
            terminated.append(True)

    def fail(_outcome: DirectionOutcome) -> None:
        raise RuntimeError("stop after durable checkpoint")

    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", ControlledExecutor)
    with pytest.raises(RuntimeError, match="durable checkpoint"):
        threshold_interval._search_directions(  # noqa: SLF001
            certificate,
            data,
            rotations,
            prune_at=None,
            workers=2,
            progress=fail,
        )

    assert len(futures) == 4
    assert futures[1].running()
    assert all(future.cancelled() for future in futures[2:])
    assert shutdown == []
    assert terminated == [True]


def test_parallel_callback_failure_still_offers_the_whole_landed_batch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:2]
    offered: list[str] = []

    class ImmediateExecutor:
        def __init__(self, *, max_workers: int, mp_context: object) -> None:
            del max_workers, mp_context

        def submit(
            self, function: Callable[..., DirectionOutcome], *args: object
        ) -> Future[DirectionOutcome]:
            del function
            rotation = cast(Rotation, args[-1])
            future: Future[DirectionOutcome] = Future()
            future.set_result(_synthetic_outcome(rotation.label))
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            del wait, cancel_futures

        def terminate_workers(self) -> None:
            return None

    def fail_first(outcome: DirectionOutcome) -> None:
        offered.append(outcome.label)
        if len(offered) == 1:
            raise RuntimeError("deadline after first durable direction")

    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", ImmediateExecutor)
    with pytest.raises(RuntimeError, match="deadline after first"):
        threshold_interval._search_directions(  # noqa: SLF001
            certificate,
            data,
            rotations,
            prune_at=None,
            workers=2,
            progress=fail_first,
        )

    assert offered == [rotation.label for rotation in rotations]


def test_parallel_reverse_refutations_return_the_earliest_net_prefix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:4]
    futures: list[Future[DirectionOutcome]] = []
    progress: list[str] = []

    class ReverseExecutor:
        def __init__(self, *, max_workers: int, mp_context: object) -> None:
            del max_workers, mp_context

        def submit(
            self, function: Callable[..., DirectionOutcome], *args: object
        ) -> Future[DirectionOutcome]:
            del function, args
            future: Future[DirectionOutcome] = Future()
            futures.append(future)
            if len(futures) == 4:
                futures[2].set_result(_synthetic_outcome(rotations[2].label, "refuted"))
                futures[0].set_result(_synthetic_outcome(rotations[0].label))
                futures[1].set_result(_synthetic_outcome(rotations[1].label, "refuted"))
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            del wait, cancel_futures

        def terminate_workers(self) -> None:
            return None

    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", ReverseExecutor)
    outcomes = threshold_interval._search_directions(  # noqa: SLF001
        certificate,
        data,
        rotations,
        prune_at=1,
        workers=2,
        progress=lambda outcome: progress.append(outcome.label),
    )

    assert progress == [rotations[2].label, rotations[0].label, rotations[1].label]
    assert [outcome.label for outcome in outcomes] == [
        rotations[0].label,
        rotations[1].label,
    ]
    assert futures[3].cancelled()


def test_parallel_refill_never_exceeds_twice_the_worker_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:9]
    active = 0
    maximum_active = 0

    class CountingFuture(Future[DirectionOutcome]):
        counted = False

        def result(self, timeout: float | None = None) -> DirectionOutcome:
            nonlocal active
            if not self.counted:
                active -= 1
                self.counted = True
            return super().result(timeout)

    class ImmediateExecutor:
        def __init__(self, *, max_workers: int, mp_context: object) -> None:
            del max_workers, mp_context

        def submit(
            self, function: Callable[..., DirectionOutcome], *args: object
        ) -> Future[DirectionOutcome]:
            nonlocal active, maximum_active
            del function
            rotation = cast(Rotation, args[-1])
            active += 1
            maximum_active = max(maximum_active, active)
            future = CountingFuture()
            future.set_result(_synthetic_outcome(rotation.label))
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            del wait, cancel_futures

        def terminate_workers(self) -> None:
            return None

    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", ImmediateExecutor)
    outcomes = threshold_interval._search_directions(  # noqa: SLF001
        certificate,
        data,
        rotations,
        prune_at=None,
        workers=2,
    )

    assert len(outcomes) == len(rotations)
    assert maximum_active == 4


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="fork pool is Linux-only")
def test_real_forked_callback_failure_requests_and_observes_worker_exit() -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:8]
    worker_processes: list[BaseProcess] = []

    class TrackingExecutor(ProcessPoolExecutor):
        def terminate_workers(self) -> None:
            worker_processes.extend(self._processes.values())
            super().terminate_workers()

    def fail(_outcome: DirectionOutcome) -> None:
        raise RuntimeError("synthetic callback failure")

    with (
        patch.object(threshold_interval, "ProcessPoolExecutor", TrackingExecutor),
        pytest.raises(RuntimeError, match="synthetic callback failure"),
    ):
        threshold_interval._search_directions(  # noqa: SLF001
            certificate,
            data,
            rotations,
            prune_at=None,
            workers=2,
            progress=fail,
        )

    assert worker_processes
    for process in worker_processes:
        process.join(timeout=5)
        assert not process.is_alive()


def test_parallel_worker_failure_retains_other_completed_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:2]
    shutdown: list[tuple[bool, bool]] = []
    terminated: list[bool] = []

    class MixedExecutor:
        def __init__(self, *, max_workers: int, mp_context: object) -> None:
            del max_workers, mp_context

        def submit(
            self, function: Callable[..., DirectionOutcome], *args: object
        ) -> Future[DirectionOutcome]:
            del function
            rotation = cast(Rotation, args[-1])
            future: Future[DirectionOutcome] = Future()
            if rotation.label == rotations[0].label:
                future.set_exception(RuntimeError("worker failed"))
            else:
                future.set_result(_synthetic_outcome(rotation.label))
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            shutdown.append((wait, cancel_futures))

        def terminate_workers(self) -> None:
            terminated.append(True)

    progress: list[str] = []
    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", MixedExecutor)
    with pytest.raises(RuntimeError, match="worker failed"):
        threshold_interval._search_directions(  # noqa: SLF001
            certificate,
            data,
            rotations,
            prune_at=None,
            workers=2,
            progress=lambda outcome: progress.append(outcome.label),
        )

    assert progress == [rotations[1].label]
    assert shutdown == []
    assert terminated == [True]


def test_parallel_same_batch_refutation_precedes_speculative_worker_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:4]
    progress: list[str] = []

    class ImmediateExecutor:
        def __init__(self, *, max_workers: int, mp_context: object) -> None:
            del max_workers, mp_context

        def submit(
            self, function: Callable[..., DirectionOutcome], *args: object
        ) -> Future[DirectionOutcome]:
            del function
            rotation = cast(Rotation, args[-1])
            index = rotations.index(rotation)
            future: Future[DirectionOutcome] = Future()
            if index == 3:
                future.set_exception(RuntimeError("speculative worker failed"))
            else:
                status = "refuted" if index == 1 else "certified"
                future.set_result(_synthetic_outcome(rotation.label, status))
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            del wait, cancel_futures

        def terminate_workers(self) -> None:
            return None

    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", ImmediateExecutor)
    outcomes = threshold_interval._search_directions(  # noqa: SLF001
        certificate,
        data,
        rotations,
        prune_at=1,
        workers=2,
        progress=lambda outcome: progress.append(outcome.label),
    )

    assert [outcome.label for outcome in outcomes] == [
        rotations[0].label,
        rotations[1].label,
    ]
    assert progress == [rotation.label for rotation in rotations[:3]]


def test_parallel_cross_batch_refutation_precedes_earlier_speculative_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:5]
    futures: list[Future[DirectionOutcome]] = []
    progress: list[str] = []

    class ControlledExecutor:
        def __init__(self, *, max_workers: int, mp_context: object) -> None:
            del max_workers, mp_context

        def submit(
            self, function: Callable[..., DirectionOutcome], *args: object
        ) -> Future[DirectionOutcome]:
            del function, args
            future: Future[DirectionOutcome] = Future()
            futures.append(future)
            if len(futures) == 4:
                future.set_exception(RuntimeError("speculative worker failed first"))
            elif len(futures) == 5:
                futures[0].set_result(_synthetic_outcome(rotations[0].label))
                futures[1].set_result(_synthetic_outcome(rotations[1].label, "refuted"))
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            del wait, cancel_futures

        def terminate_workers(self) -> None:
            return None

    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", ControlledExecutor)
    outcomes = threshold_interval._search_directions(  # noqa: SLF001
        certificate,
        data,
        rotations,
        prune_at=1,
        workers=2,
        progress=lambda outcome: progress.append(outcome.label),
    )

    assert [outcome.label for outcome in outcomes] == [
        rotations[0].label,
        rotations[1].label,
    ]
    assert progress == [rotation.label for rotation in rotations[:2]]
    assert futures[2].cancelled()
    assert futures[4].cancelled()


@pytest.mark.parametrize("refutation_index", [None, 2])
def test_parallel_worker_failure_is_not_hidden_without_an_earlier_refutation(
    monkeypatch: pytest.MonkeyPatch, refutation_index: int | None
) -> None:
    certificate = _cluster_certificate()
    data = ThresholdAtomData.of(certificate)
    rotations = doubled_net(certificate.half_tangents)[:4]

    class ImmediateExecutor:
        def __init__(self, *, max_workers: int, mp_context: object) -> None:
            del max_workers, mp_context

        def submit(
            self, function: Callable[..., DirectionOutcome], *args: object
        ) -> Future[DirectionOutcome]:
            del function
            rotation = cast(Rotation, args[-1])
            index = rotations.index(rotation)
            future: Future[DirectionOutcome] = Future()
            if index == 1:
                future.set_exception(RuntimeError("retained worker failed"))
            else:
                status = "refuted" if index == refutation_index else "certified"
                future.set_result(_synthetic_outcome(rotation.label, status))
            return future

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            del wait, cancel_futures

        def terminate_workers(self) -> None:
            return None

    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", ImmediateExecutor)
    with pytest.raises(RuntimeError, match="retained worker failed"):
        threshold_interval._search_directions(  # noqa: SLF001
            certificate,
            data,
            rotations,
            prune_at=1,
            workers=2,
        )


def test_bounded_parallel_workers_do_not_change_the_verdict(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = _cluster_certificate()
    serial = verify_threshold_by_intervals(certificate, enclose=True, workers=1)
    monkeypatch.setattr(threshold_interval.sys, "platform", "linux")
    monkeypatch.setattr(threshold_interval, "ProcessPoolExecutor", _ThreadPoolAdapter)
    forked = verify_threshold_by_intervals(certificate, enclose=True, workers=2)
    assert forked.directions == serial.directions
    assert forked.conditions == serial.conditions


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="fork pool is Linux-only")
def test_real_forked_workers_do_not_change_the_verdict() -> None:
    certificate = _cluster_certificate()
    serial = verify_threshold_by_intervals(certificate, enclose=True, workers=1)
    forked = verify_threshold_by_intervals(certificate, enclose=True, workers=2)
    assert forked.directions == serial.directions
    assert forked.conditions == serial.conditions


# --- what a restricted run can and cannot say ------------------------------------------


def test_a_restricted_run_cannot_accept_but_can_refute() -> None:
    certificate = tight_certificate()
    sample = verify_threshold_by_intervals(certificate, directions=("0", "3'"))
    assert len(sample.directions) == 2
    assert all(o.status == "certified" for o in sample.directions)
    assert not sample.accepted
    assert sample.conditions[-1].status == "undecided"
    hollow = rescaled(certificate, Fraction(9, 10))
    refused = verify_threshold_by_intervals(hollow, directions=("0",))
    assert refused.failures == (CONDITION_5,)
    assert refused.directions[0].status == "refuted"
    assert refused.refutations[0].charge < 1


def test_budget_conditions_are_decided_in_exact_integers() -> None:
    certificate = _cluster_certificate()
    scale, point_masses, threshold_masses, budget = scaled_threshold_masses(certificate)
    assert Fraction(budget, scale) == certificate.total_budget
    assert sum(point_masses) == certificate.point_mass * scale
    assert all(m >= 0 for m in threshold_masses)
    verdict = verify_threshold_by_intervals(certificate, directions=("0",))
    assert verdict.conditions[0].holds
    heavy = ThresholdCertificate(
        n=1,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
        atoms=certificate.atoms,
        threshold_atoms=certificate.threshold_atoms,
        half_tangents=certificate.half_tangents,
    )
    verdict = verify_threshold_by_intervals(heavy, directions=("0",))
    assert "Condition 2' total budget below n" in verdict.failures


# --- refusals ----------------------------------------------------------------------------


def test_a_budget_that_would_wrap_int64_is_refused_before_numpy_sees_it() -> None:
    """Two masses of ``2^61`` fit int64 on their own; a 2-of-5 atom's budget doubles one
    of them and their sum does not. The budget is summed in Python integers and refused
    at ``2^62``, before any array exists."""
    points = tuple((Fraction(k, 10), Fraction(1)) for k in range(5))
    certificate = ThresholdCertificate(
        n=1,
        outer_side=SIDE,
        square_side=SQUARE,
        atoms=(Atom("heavy", Fraction(1), Fraction(1), Fraction(2**61)),),
        threshold_atoms=(ThresholdAtom(points, 2, Fraction(2**61)),),
        half_tangents=NET,
    )
    assert certificate.total_budget == 3 * 2**61
    with pytest.raises(IntervalInputError, match="total scaled budget"):
        ThresholdAtomData.of(certificate)
    with pytest.raises(IntervalInputError, match="total scaled budget"):
        verify_threshold_by_intervals(certificate, directions=("0",))


def test_a_member_table_past_the_gather_cap_is_refused_before_any_allocation() -> None:
    pool = [(Fraction(k, 100), Fraction(1)) for k in range(100)]
    atoms = tuple(
        ThresholdAtom(tuple(pool[i] for i in chosen), 2, Fraction(1, 8))
        for chosen in list(combinations(range(100), 4))[: MAX_MEMBER_SLOTS // 4 + 1]
    )
    assert len(atoms) * 4 > MAX_MEMBER_SLOTS
    certificate = ThresholdCertificate(
        n=10**6,
        outer_side=SIDE,
        square_side=SQUARE,
        atoms=(),
        threshold_atoms=atoms,
        half_tangents=NET,
    )
    with pytest.raises(IntervalInputError, match="member table"):
        ThresholdAtomData.of(certificate)


# --- the limit of the method -------------------------------------------------------------


def test_a_threshold_atoms_own_seam_stalls_the_search_and_is_never_accepted() -> None:
    """Points at spacing exactly ``B/2`` make one point leave the core where the next
    enters, and the charge is constant across that seam. No box straddling it can be
    resolved: the two points are each partly resolved and dropped, the box is bisected
    to the resolution floor, and the direction is reported undecided with the box
    budget intact and no acceptance."""
    verdict = verify_threshold_by_intervals(_tiling(Fraction(0)), directions=("0",))
    assert not verdict.accepted
    outcome = verdict.directions[0]
    assert outcome.status == "undecided"
    assert outcome.stalled > 0
    assert not outcome.budget_exhausted
    assert outcome.boxes < BATCH * 8
    assert outcome.lower == 0
    assert outcome.upper is not None
    assert outcome.upper >= verdict.scale
    assert verdict.conditions[-1].status == "undecided"


def test_overlapping_the_seam_lets_the_same_search_certify() -> None:
    verdict = verify_threshold_by_intervals(_tiling(Fraction(1, 97)), directions=("0",))
    outcome = verdict.directions[0]
    assert outcome.status == "certified"
    assert outcome.stalled == 0
    assert outcome.lower is not None
    assert outcome.lower >= verdict.scale
    # One direction certified is the control's answer; the verdict stays undecided.
    assert not verdict.accepted
    assert verdict.conditions[-1].status == "undecided"
