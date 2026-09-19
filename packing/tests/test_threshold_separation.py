"""2-of-3 separation: a violated triangle is found, a graph with no triangle is not.

The producer is a different file; this holds the in-tree FamilyGeometry to the geometry
the covering loop will call, including that the library module does not print and does
not import agenda-034 scratch.
"""

from __future__ import annotations

import ast
from fractions import Fraction
from pathlib import Path

import numpy as np

from sqpack.fractional.ceiling import CeilingCertificate, Placement
from sqpack.fractional.threshold import ThresholdAtom
from sqpack.fractional.threshold_separation import (
    FamilyGeometry,
    atom_columns,
    family_from_dual,
)

LIBRARY = Path(__file__).resolve().parents[1] / "src/sqpack/fractional/threshold_separation.py"
NET = (Fraction(0), Fraction(1, 5))
SIDE = Fraction(6)
SQUARE = Fraction(2)


def _upright(x: Fraction, y: Fraction, weight: Fraction) -> Placement:
    return Placement(Fraction(0), x, y, weight, SQUARE)


def _family(*placements: Placement) -> CeilingCertificate:
    return CeilingCertificate(2, SIDE, SQUARE, NET, placements)


def _has_print(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "print":
                return True
    return False


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            names.add(node.module)
    return names


def test_three_pairwise_overlapping_squares_yield_a_violated_2of3() -> None:
    """Three closed squares, every pair overlapping, weight 1/2: charge 3/2 > 1."""

    family = _family(
        _upright(Fraction(2), Fraction(2), Fraction(1, 2)),
        _upright(Fraction(3), Fraction(2), Fraction(1, 2)),
        _upright(Fraction(5, 2), Fraction(14, 5), Fraction(1, 2)),
    )
    geometry = FamilyGeometry(family)
    assert len(geometry.edges) == 3
    assert len(geometry.triangles()) == 1
    found = geometry.violated_2of3(outer_side=SIDE)
    assert found
    heaviest = found[0]
    assert heaviest.threshold == 2
    assert len(set(heaviest.points)) == 3
    assert heaviest.charge > 1
    atom = heaviest.atom()
    assert isinstance(atom, ThresholdAtom)
    assert atom.size == 3
    assert atom.threshold == 2


def test_two_placements_with_no_triple_overlap_yield_no_2of3() -> None:
    family = _family(
        _upright(Fraction(2), Fraction(2), Fraction(1, 2)),
        _upright(Fraction(3), Fraction(2), Fraction(1, 2)),
    )
    geometry = FamilyGeometry(family)
    assert len(geometry.edges) == 1
    assert len(geometry.triangles()) == 0
    assert geometry.violated_2of3(outer_side=SIDE) == []


def test_a_disjoint_pair_has_no_edge_and_no_violation() -> None:
    family = _family(
        _upright(Fraction(2), Fraction(2), Fraction(1)),
        _upright(Fraction(5), Fraction(5), Fraction(1)),
    )
    geometry = FamilyGeometry(family)
    assert geometry.edges == []
    assert geometry.violated_2of3(outer_side=SIDE) == []


def test_atom_column_cost_is_orbit_size_times_floor_size_over_k() -> None:
    atom = ThresholdAtom(
        (
            (Fraction(2), Fraction(2)),
            (Fraction(3), Fraction(2)),
            (Fraction(5, 2), Fraction(14, 5)),
        ),
        2,
        Fraction(1),
    )
    orbit = atom.orbit(SIDE)
    columns, costs = atom_columns(
        (orbit,),
        [(0, Fraction(3), Fraction(3))],
        NET,
        SQUARE,
    )
    assert columns.shape == (1, 1)
    assert costs.shape == (1,)
    assert costs[0] == len(orbit) * (atom.size // atom.threshold)


def test_empty_dual_is_not_a_family() -> None:
    assert (
        family_from_dual(
            [(0, Fraction(1), Fraction(1))],
            np.zeros(1),
            half_tangents=NET,
            outer_side=SIDE,
            square_side=SQUARE,
            n=2,
        )
        is None
    )


def test_library_module_has_no_print() -> None:
    assert not _has_print(LIBRARY)


def test_library_does_not_import_scratch() -> None:
    names = _imported_modules(LIBRARY)
    joined = " ".join(names)
    assert "sepcore" not in joined
    assert "lp383" not in joined
    assert ".py.txt" not in joined
    assert ".txt" not in joined
