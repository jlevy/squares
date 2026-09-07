"""The new control's loader is replaced by unrelated rational unit-square toys."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

import pytest

from devtools import check_full_size_density_pair_separator as checker
from devtools import run_full_size_density_graph as graph
from devtools.run_full_size_density_pair_separator import make_packet
from sqpack.field import NumberField
from sqpack.full_size_density.pair_separator import separate
from sqpack.full_size_density.support_ceiling import SupportError, axis_square

NAME = "trump-perturbed-control-v1"


def toy_roster():
    field = NumberField((1, 0), (-1, 1))
    q = field.rational
    squares = [
        axis_square(q(Fraction(2 * x + 1, 2)), q(Fraction(2 * y + 1, 2)))
        for y in range(3)
        for x in range(3)
    ]
    squares.insert(3, axis_square(q("1/2"), q("9/2")))
    squares.insert(4, axis_square(q("3/2"), q("9/2")))
    return tuple(squares), q(5)


def test_mocked_negative_has_exact_witness_but_graph_is_only_unresolved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(checker, "load_source", lambda _source: toy_roster())
    family = checker.control_family(NAME)
    assert len(family.placements) == 11
    assert sum(entry.weight for entry in family.placements) == 11
    separated = separate(family)
    assert separated.witness is not None
    assert checker.replay_packet(make_packet(NAME, family, separated)) == "candidate-refuted"
    raw = graph.worker(control=NAME, candidate=None, packet=None, node_limit=100)
    monkeypatch.setattr(graph, "load_packet", lambda _path: raw)
    checked = graph.replay_bound(raw, family, NAME)
    assert checked["status"] == "unresolved"
    assert checked["bound_proved"] is False


@pytest.mark.parametrize("mutation", ["short", "wrong_anchor"])
def test_source_shape_is_bound_before_perturbation(
    mutation: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    squares, side = toy_roster()
    squares = squares[:-1] if mutation == "short" else (*squares[:3], squares[0], *squares[4:])
    monkeypatch.setattr(checker, "load_source", lambda _source: (squares, side))
    with pytest.raises(SupportError, match="perturbed source"):
        checker.control_family(NAME)


def test_graph_declared_degree_preflight_precedes_new_scientific_loader(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: Any, **_kwargs: Any):
        raise AssertionError("scientific loader reached")

    monkeypatch.setattr(graph, "PRODUCER_MAX_FIELD_DEGREE", 4)
    monkeypatch.setattr(graph, "control_family", forbidden)
    with pytest.raises(SupportError, match="declared source degree"):
        graph.worker(control=NAME, candidate=None, packet=None, node_limit=1)
