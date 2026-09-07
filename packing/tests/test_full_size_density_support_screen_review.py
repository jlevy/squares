"""Independent BC-254 readiness controls; never generate Trump rows or solve its LP."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from typing import Any

import pytest

import devtools.check_full_size_density_support_ceiling as checker
import sqpack.full_size_density.support_ceiling as ceiling
import sqpack.full_size_density.support_screen as screen
from devtools.run_full_size_density_support_screen import source_control
from sqpack.full_size_density.support_ceiling import SupportError


@pytest.fixture
def rational_packet() -> dict[str, Any]:
    seeds, side = checker.load_source("toy-rational-v1")
    bound = screen.bind_source(seeds, side)
    return screen.make_packet("toy-rational-v1", bound, screen.solve_screen(bound))


def test_trump_source_control_preserves_all_preimages_without_rows_or_solves(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("source control must not generate target rows or solve an LP")

    monkeypatch.setattr(screen, "initial_rows", forbidden)
    monkeypatch.setattr(screen, "extend_rows", forbidden)
    monkeypatch.setattr(screen, "solve_control_lp", forbidden)
    monkeypatch.setattr(checker, "initial_rows", forbidden)
    monkeypatch.setattr(checker, "extend_rows", forbidden)
    receipt = source_control("trump11-v1")
    metadata = receipt["support"]
    assert receipt["labelled_images"] == 88
    assert receipt["distinct_placements"] == 60
    assert receipt["uniform_mass"] == "11"
    assert receipt["target_lp_invoked"] is False
    assert metadata["sizes"] == [4, 8, 8, 8, 8, 8, 8, 8]
    assert metadata["original_counts"] == [3, 1, 2, 1, 1, 1, 1, 1]
    weights = tuple(Fraction(value) for value in metadata["uniform_weights"])
    assert weights == (Fraction(3, 4), Fraction(1, 8), Fraction(1, 4)) + (Fraction(1, 8),) * 5
    assert (
        sorted(len(item["labels"]) for item in metadata["preimages"])
        == [1] * 48 + [2] * 8 + [6] * 4
    )


def test_noncanonical_exponent_is_refused_before_fraction_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seeds, side = checker.load_source("toy-rational-v1")
    bound = screen.bind_source(seeds, side)
    packet = screen.make_packet("toy-rational-v1", bound, screen.solve_screen(bound))
    mutated = deepcopy(packet)
    text = "1e1000000000"
    mutated["rows"][0]["radius"] = text
    original = checker.checked_rational

    def guarded(value: object) -> Fraction:
        # Never construct the huge integer. Detect whether lexical rejection precedes it.
        if value == text:
            raise AssertionError("noncanonical exponent reached Fraction construction")
        return original(value)

    monkeypatch.setattr(checker, "checked_rational", guarded)
    with pytest.raises(SupportError, match="canonical"):
        checker.replay_packet(mutated)


@pytest.mark.parametrize(
    "text",
    [
        "1e1000000000",
        "1e-1000000000",
        "1E+1000000000",
        "1.0",
        ".5",
        "+1",
        " 1",
        "1 ",
        "1\n",
        "1_000",
        "01",
        "-01",
        "1/02",
        "1/-2",
        "1/0",
        "1/ 2",
        "\u0661",
        "\uff11",
        "",
        "1" * 4097,
    ],
)
def test_unsafe_lexical_forms_never_reach_rational_conversion(
    monkeypatch: pytest.MonkeyPatch, text: str, rational_packet: dict[str, Any]
) -> None:
    original = checker.checked_rational

    def guarded(value: object) -> Fraction:
        if value == text:
            raise AssertionError("invalid lexical form reached Fraction construction")
        return original(value)

    rational_packet["rows"][0]["radius"] = text
    monkeypatch.setattr(checker, "checked_rational", guarded)
    with pytest.raises(SupportError, match="canonical"):
        checker.replay_packet(rational_packet)


@pytest.mark.parametrize("text", ["-0", "0/3", "1/1", "2/4", "-2/4"])
def test_lexically_bounded_but_noncanonical_rationals_are_refused(
    text: str, rational_packet: dict[str, Any]
) -> None:
    rational_packet["rows"][0]["radius"] = text
    with pytest.raises(SupportError, match="canonical"):
        checker.replay_packet(rational_packet)


@pytest.mark.parametrize("text", ["0", "1", "-1", "1/2", "-1/2"])
def test_canonical_exact_rationals_reach_the_separate_geometry_guard(
    text: str, rational_packet: dict[str, Any]
) -> None:
    rational_packet["rows"][0]["radius"] = text
    # These strings are canonical, although none is a valid radius for this row.
    with pytest.raises(SupportError, match=r"neighborhood|boundary"):
        checker.replay_packet(rational_packet)


def test_determinant_upper_replay_does_not_use_producer_geometry_or_solver(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seeds, side = checker.load_source("toy-algebraic-v1")
    bound = screen.bind_source(seeds, side)
    result = screen.solve_screen(bound)

    def forbidden(*_args, **_kwargs):
        raise AssertionError("determinant replay reached a producer geometry or solver path")

    monkeypatch.setattr(ceiling, "_images", forbidden)
    monkeypatch.setattr(ceiling, "necessary_row", forbidden)
    monkeypatch.setattr(screen, "necessary_row", forbidden)
    monkeypatch.setattr(screen, "solve_control_lp", forbidden)
    monkeypatch.setattr(ceiling, "solve", forbidden)
    assert (
        checker.replay_upper(seeds, bound.support, result.rows, result.solution.multipliers)
        == 1
    )

    row = result.rows[0]
    wrong_count = replace(row, coefficients=(row.coefficients[0] - 1,))
    with pytest.raises(SupportError, match="incidence"):
        checker.replay_upper(seeds, bound.support, (wrong_count,), result.solution.multipliers)
    oversized = replace(row, radius=Fraction(2))
    with pytest.raises(SupportError, match="boundary"):
        checker.replay_upper(seeds, bound.support, (oversized,), result.solution.multipliers)
