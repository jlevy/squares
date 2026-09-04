"""The integer sweep agrees with the independently retained Fraction sweep.

`minimum_covered_mass` decides in ``int64`` on the weights' common scale and
falls back to ``Fraction`` arithmetic when that scale does not fit. The
``Fraction`` route retains independent cell-reduction and arithmetic paths from the
pre-optimization verifier; these tests hold the two to the same value and witness,
direction by direction, and hold the parallel direction loop to the serial one. The
performance figures in Agenda 020 are unretained operator reports, not benchmarks.
"""

# This module deliberately exercises the private scheduling bounds as unit-level
# safety contracts; their public effect is otherwise too expensive to isolate.
# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from fractions import Fraction

import pytest

import sqpack.fractional.certificate as certificate_module
from cases.n11_fractional_certificate.replay import FIRST_RUNG_PATH as N11_FIRST_RUNG
from cases.n11_fractional_certificate.replay import load as n11_load
from sqpack.fractional import sweep
from sqpack.fractional.certificate import Certificate, sweep_all_directions
from sqpack.fractional.model import Atom, Direction
from sqpack.fractional.sweep import (
    minimum_covered_mass,
    minimum_covered_mass_fraction,
    minimum_covered_mass_integer,
    reduce_to_cells,
    reduce_to_spans,
    weight_scale,
)


def _small_certificate() -> Certificate:
    """A D4-closed handful of atoms at odd weights, so the scale is not a round number."""

    side = Fraction(3)
    centre = side / 2
    seeds = (
        (Fraction(1, 2), Fraction(3, 4), Fraction(3, 7)),
        (Fraction(1), Fraction(5, 4), Fraction(2, 3)),
        (Fraction(3, 2), Fraction(3, 2), Fraction(5, 11)),
    )
    atoms: dict[tuple[Fraction, Fraction], Fraction] = {}
    for x, y, w in seeds:
        dx, dy = x - centre, y - centre
        for px, py in ((dx, dy), (-dy, dx), (-dx, -dy), (dy, -dx)):
            for qx, qy in ((px, py), (-px, py)):
                atoms[(centre + qx, centre + qy)] = w
    limit, steps = Fraction(207107, 500000), 12
    return Certificate(
        n=6,
        outer_side=side,
        square_side=Fraction(9977, 10000),
        atoms=tuple(Atom(f"{k:03d}", x, y, w) for k, ((x, y), w) in enumerate(atoms.items())),
        half_tangents=tuple(limit * k / steps for k in range(steps + 1)),
        symmetry="D4",
    )


def test_the_weight_scale_is_the_common_denominator() -> None:
    certificate = _small_certificate()
    scale = weight_scale(certificate.atoms)
    assert scale == 3 * 7 * 11
    assert all((atom.weight * scale).denominator == 1 for atom in certificate.atoms)


def test_integer_and_fraction_sweeps_agree_on_every_direction_of_a_small_net() -> None:
    """Value and witness, at every direction, on a certificate whose scale is 231."""

    certificate = _small_certificate()
    scale = weight_scale(certificate.atoms)
    for direction in certificate.directions:
        reference = minimum_covered_mass_fraction(
            certificate.atoms, direction, certificate.outer_side, certificate.square_side
        )
        fast = minimum_covered_mass_integer(
            certificate.atoms, direction, certificate.outer_side, certificate.square_side, scale
        )
        assert fast == reference, direction.label


@pytest.mark.parametrize("index", [0, 1, 37, 90, 137, 180])
def test_integer_and_fraction_sweeps_agree_on_a_retained_rung(index: int) -> None:
    """The 373-atom n = 11 rung, at six directions including both ends of the net.

    All 181 directions were run once on 2026-09-04 with no mismatch in 145 s;
    six are enough to keep in the fast tier, and the ends of the net are where
    the rotated frame is furthest from the axis-aligned one.
    """

    certificate = n11_load(N11_FIRST_RUNG)
    direction = certificate.directions[index]
    reference = minimum_covered_mass_fraction(
        certificate.atoms, direction, certificate.outer_side, certificate.square_side
    )
    fast = minimum_covered_mass(
        certificate.atoms, direction, certificate.outer_side, certificate.square_side
    )
    assert fast == reference


def test_the_span_reduction_matches_the_independent_legacy_cell_reduction() -> None:
    """The optimized span geometry equals the independently retained cell geometry."""

    certificate = n11_load(N11_FIRST_RUNG)
    direction = certificate.directions[53]
    spans = reduce_to_spans(
        certificate.atoms, direction, certificate.outer_side, certificate.square_side
    )
    cells = reduce_to_cells(
        certificate.atoms, direction, certificate.outer_side, certificate.square_side
    )
    assert cells.u_events == spans.u_events and cells.v_events == spans.v_events
    expanded = [(i, j) for i, j0, j1 in spans.spans for j in range(j0, j1 + 1)]
    assert list(cells.cells) == expanded
    assert all(j0 <= j1 for _, j0, j1 in spans.spans)


def test_default_and_explicit_worker_counts_obey_cpu_and_memory_caps(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A high-core host cannot allocate one dense event grid per direction."""
    certificate = n11_load(N11_FIRST_RUNG)
    one_grid = certificate_module._estimated_grid_bytes(len(certificate.atoms))
    monkeypatch.setattr(certificate_module.os, "process_cpu_count", lambda: 64)
    monkeypatch.setattr(certificate_module, "_MAX_PARALLEL_WORKERS", 8)
    monkeypatch.setattr(certificate_module, "_PARALLEL_GRID_BUDGET_BYTES", 2 * one_grid)
    assert certificate_module._worker_count(certificate, None) == 2
    assert certificate_module._worker_count(certificate, 99) == 2
    assert certificate_module._worker_count(certificate, 1) == 1


def test_a_single_grid_over_the_parallel_budget_never_multiplies(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The budget caps concurrent grids without rejecting a supported certificate."""

    certificate = n11_load(N11_FIRST_RUNG)
    one_grid = certificate_module._estimated_grid_bytes(len(certificate.atoms))
    monkeypatch.setattr(certificate_module.os, "process_cpu_count", lambda: 64)
    monkeypatch.setattr(certificate_module, "_MAX_PARALLEL_WORKERS", 8)
    monkeypatch.setattr(certificate_module, "_PARALLEL_GRID_BUDGET_BYTES", one_grid - 1)
    assert certificate_module._worker_count(certificate, 99) == 1
    monkeypatch.setattr(certificate_module, "_PARALLEL_GRID_BUDGET_BYTES", 2 * one_grid - 1)
    assert certificate_module._worker_count(certificate, 99) == 1
    monkeypatch.setattr(certificate_module, "_PARALLEL_GRID_BUDGET_BYTES", 2 * one_grid)
    assert certificate_module._worker_count(certificate, 99) == 2


def test_a_scale_too_large_for_int64_falls_back_to_fractions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Past the limit the integer route declines and the Fraction route decides.

    The limit is patched down rather than a certificate built up to it: a
    certificate whose scaled mass exceeds 2**60 would not fit in the fast tier.
    """

    certificate = _small_certificate()
    direction = certificate.directions[5]
    args = (certificate.atoms, direction, certificate.outer_side, certificate.square_side)
    expected = minimum_covered_mass_fraction(*args)
    monkeypatch.setattr(sweep, "_INTEGER_MASS_LIMIT", 1)
    calls: list[str] = []
    original = sweep.minimum_covered_mass_integer

    def spy(*a: object, **k: object) -> object:
        calls.append("integer")
        return original(*a, **k)  # type: ignore[arg-type]

    monkeypatch.setattr(sweep, "minimum_covered_mass_integer", spy)
    assert minimum_covered_mass(*args) == expected
    assert calls == [], "the integer route ran past its own limit"


def test_the_public_integer_entry_point_refuses_an_overflowing_scaled_total() -> None:
    """A direct call cannot bypass the int64 proof obligation."""

    atoms = (
        Atom("a", Fraction(1), Fraction(1), Fraction(2**62)),
        Atom("b", Fraction(1), Fraction(1), Fraction(2**62)),
    )
    direction = _small_certificate().directions[0]
    with pytest.raises(ValueError, match="safe int64 limit"):
        minimum_covered_mass_integer(atoms, direction, Fraction(3), Fraction(1), 1)


@pytest.mark.parametrize("main_file", [None, "<stdin>", "<string>"])
def test_a_nonimportable_main_module_forces_the_safe_serial_schedule(
    monkeypatch: pytest.MonkeyPatch,
    main_file: str | None,
) -> None:
    """Library code never forces ``fork`` merely to support a stdin caller."""

    certificate = _small_certificate()
    main = certificate_module.sys.modules["__main__"]
    if main_file is None:
        monkeypatch.delattr(main, "__file__", raising=False)
    else:
        monkeypatch.setattr(main, "__file__", main_file)

    class RefusePool:
        def __init__(self, *args: object, **kwargs: object) -> None:
            raise AssertionError("process pool should not start without an importable __main__")

    monkeypatch.setattr(certificate_module, "ProcessPoolExecutor", RefusePool)
    assert sweep_all_directions(certificate, workers=3) == sweep_all_directions(
        certificate, workers=1
    )


def test_the_parallel_direction_loop_matches_the_serial_one() -> None:
    """Same minima, same order, same first-attaining label, whatever the schedule."""

    certificate = n11_load(N11_FIRST_RUNG)
    serial = sweep_all_directions(certificate, workers=1)
    parallel = sweep_all_directions(certificate, workers=3)
    assert parallel == serial
    assert [label for _, label in serial] == [d.label for d in certificate.directions]


def test_the_parallel_branch_uses_the_bounded_executor_and_preserves_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The schedule-equivalence test must actually cross the executor boundary."""

    certificate = _small_certificate()
    expected = sweep_all_directions(certificate, workers=1)
    calls: list[object] = []

    class FakeExecutor:
        def __init__(self, *, max_workers: int) -> None:
            calls.append(("workers", max_workers))

        def __enter__(self) -> FakeExecutor:
            calls.append("enter")
            return self

        def __exit__(self, *args: object) -> None:
            calls.append("exit")

        def map(
            self,
            function: Callable[[Direction], tuple[Fraction, str]],
            directions: Iterable[Direction],
        ) -> Iterator[tuple[Fraction, str]]:
            direction_tuple = tuple(directions)
            calls.append(("map", tuple(d.label for d in direction_tuple)))
            return (function(direction) for direction in direction_tuple)

    monkeypatch.setattr(certificate_module.os, "process_cpu_count", lambda: 8)
    monkeypatch.setattr(certificate_module, "_process_pool_is_safe", lambda: True)
    monkeypatch.setattr(certificate_module, "ProcessPoolExecutor", FakeExecutor)

    actual = sweep_all_directions(certificate, workers=3)

    assert actual == expected
    assert calls == [
        ("workers", 3),
        "enter",
        ("map", tuple(direction.label for direction in certificate.directions)),
        "exit",
    ]
