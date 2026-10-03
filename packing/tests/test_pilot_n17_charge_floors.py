"""The charge-floor pilot reads R068 as the checkers do and sweeps what it says it sweeps.

These tests hold the pilot to the certificate's own invariants (site and atom counts, the
reconstructed budget), to the replayed ledger (the corner cell at R068's parent side
attains exactly Gamma), and to its own consistency (a direct recount at every witness).
No full angle scan or survivor census runs here; those are the pilot's receipts.
"""

from __future__ import annotations

import math

import pytest

from devtools import pilot_n17_charge_floors as pilot

GAMMA_R068 = 1000026844
BUDGET_R068 = 17000448944


@pytest.fixture(scope="module")
def charge() -> pilot.Charge:
    return pilot.load_charge()


def test_certificate_invariants(charge: pilot.Charge) -> None:
    assert charge.site_count == 20860
    assert charge.atom_count == 49208
    assert charge.budget == BUDGET_R068
    assert math.isclose(pilot.unit_to_container(charge), 4.613 / 4.676)


def test_mobius_expansion_of_two_of_three() -> None:
    expansion = dict(pilot.mobius_expansion([1, 1, 1], 2, []))
    assert expansion == {0b011: 1, 0b101: 1, 0b110: 1, 0b111: -2}


def test_mobius_expansion_of_intersecting_masks() -> None:
    expansion = dict(pilot.mobius_expansion([1, 1, 1], 1, [0b011, 0b101, 0b110]))
    assert expansion == {0b011: 1, 0b101: 1, 0b110: 1, 0b111: -2}


@pytest.mark.parametrize("theta", [0.0, 20.0, 40.0])
def test_corner_cell_attains_gamma_at_r068_parent(charge: pilot.Charge, theta: float) -> None:
    parent = float(charge.parent_side_r068)
    result = pilot.sweep_cell(charge, parent, (0, 0), theta)
    assert result.minimum == GAMMA_R068
    recount = pilot.charge_at_pose(charge, parent, result.x, result.y, math.radians(theta))
    assert recount == GAMMA_R068


@pytest.mark.parametrize("name", list(pilot.CLASS_REPRESENTATIVES))
def test_sweep_minimum_is_a_pose_charge(charge: pilot.Charge, name: str) -> None:
    parent = pilot.unit_to_container(charge)
    result = pilot.sweep_cell(charge, parent, pilot.CLASS_REPRESENTATIVES[name], 20.0)
    recount = pilot.charge_at_pose(charge, parent, result.x, result.y, math.radians(20.0))
    assert recount == result.minimum


def test_cell_classes_partition_the_grid() -> None:
    counts = dict.fromkeys(pilot.CLASS_REPRESENTATIVES, 0)
    for i in range(pilot.GRID):
        for j in range(pilot.GRID):
            counts[pilot.cell_class((i, j))] += 1
    assert counts == {
        "corner": 4,
        "edge-near-corner": 8,
        "edge-middle": 4,
        "interior-corner": 4,
        "interior-edge": 4,
        "centre": 1,
    }
    assert sum(pilot.is_boundary(cell) for cell in pilot.ENDPOINT_CELLS) == 11


def test_class_floor_ceiling_bounds_a_toy_census() -> None:
    census = {"1,0,0,0,0,0": 3, "2,0,0,0,0,0": 7, "0,0,0,0,0,0": 5, "0,1,0,0,0,0": 2}
    result = pilot.class_floor_ceiling(census, (1, 0, 0, 0, 0, 0), seed=1)
    assert result["orbits_with_endpoint_class_counts"] == 3
    assert result["antipodal_pair_lower_bound"] == 3 + min(7, 5)
    assert result["random_search_best_survivors"] >= result["antipodal_pair_lower_bound"]
