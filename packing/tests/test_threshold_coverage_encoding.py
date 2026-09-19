"""Frozen U025 closed-core coverage is linear in orbit weights."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from fractions import Fraction

import numpy as np

from sqpack.fractional.certificate import d4_images
from sqpack.fractional.model import Atom
from sqpack.fractional.sweep import _cell_witness, centre_domain, reduce_to_spans
from sqpack.fractional.threshold import (
    ThresholdAtom,
    ThresholdCertificate,
    exact_charge,
    minimum_charge,
)
from sqpack.fractional.threshold_compression import inventory_certificate
from sqpack.fractional.threshold_coverage_encoding import (
    FrozenCoverageEncoding,
    _paint,
    encode_frozen_coverage,
    frozen_coverage_geometry,
    minimum_encoded_charge,
    orbit_weights,
    pareto_minimal_rows,
    solve_feasibility_mip,
    unique_rows,
)


def _tiny_certificate() -> ThresholdCertificate:
    outer_side = Fraction(4)
    point = (Fraction(1, 3), Fraction(2, 3))
    point_weight = Fraction(1, 7)
    threshold_weight = Fraction(2, 11)
    atoms = tuple(
        Atom(f"p{index}", x, y, point_weight)
        for index, (x, y) in enumerate(sorted(set(d4_images(*point, outer_side))))
    )
    seed = ThresholdAtom(
        ((Fraction(1, 2), Fraction(3, 4)), (Fraction(5, 4), Fraction(7, 6))),
        2,
        threshold_weight,
        (1, 2),
    )
    threshold_atoms = tuple(
        ThresholdAtom(
            tuple((x, y) for x, y, _ in key[0]),
            key[1],
            threshold_weight,
            tuple(count for _, _, count in key[0]),
        )
        for key in sorted({image.key for image in seed.images(outer_side)})
    )
    return ThresholdCertificate(
        n=11,
        outer_side=outer_side,
        square_side=Fraction(9, 10),
        atoms=atoms,
        threshold_atoms=threshold_atoms,
        half_tangents=(Fraction(0), Fraction(1, 5)),
    )


def test_unique_and_pareto_rows_drop_duplicates_and_dominated_covers() -> None:
    rows = np.array([[1, 2], [1, 2], [2, 2], [1, 1], [0, 3]], dtype=np.uint8)
    unique = unique_rows(rows)
    assert unique.shape[0] == 4
    pareto = pareto_minimal_rows(rows)
    kept = {tuple(int(value) for value in row) for row in pareto}
    assert kept == {(1, 1), (0, 3)}


def test_tiny_cell_row_matches_exact_membership_charge() -> None:
    certificate = _tiny_certificate()
    inventory = inventory_certificate(certificate)
    geometry = frozen_coverage_geometry(inventory)
    weights = orbit_weights(inventory)
    direction = certificate.directions[0]
    reduction = reduce_to_spans(
        geometry.event_atoms, direction, inventory.outer_side, inventory.square_side
    )
    u_index = {value: index for index, value in enumerate(reduction.u_events)}
    v_index = {value: index for index, value in enumerate(reduction.v_events)}
    width, height = len(reduction.u_events), len(reduction.v_events)
    i, j0, j1 = reduction.spans[len(reduction.spans) // 2]
    j = (j0 + j1) // 2
    row = np.zeros(inventory.orbit_count, dtype=np.int32)
    orbit_index = 0
    for members in geometry.point_orbits:
        grid = np.zeros((width, height), dtype=np.int32)
        for event_index in members:
            _paint(grid, u_index, v_index, reduction.rectangles[event_index], 1)
        np.cumsum(grid, axis=1, out=grid)
        np.cumsum(grid, axis=0, out=grid)
        row[orbit_index] = grid[i, j]
        orbit_index += 1
    for members in geometry.threshold_orbits:
        grid = np.zeros((width, height), dtype=np.int32)
        for member in members:
            counts = np.zeros((width, height), dtype=np.int32)
            for event_index, multiplicity in member.sites:
                _paint(
                    counts,
                    u_index,
                    v_index,
                    reduction.rectangles[event_index],
                    multiplicity,
                )
            np.cumsum(counts, axis=1, out=counts)
            np.cumsum(counts, axis=0, out=counts)
            grid += counts >= member.threshold
        row[orbit_index] = grid[i, j]
        orbit_index += 1
    witness = _cell_witness(
        centre_domain(inventory.outer_side, inventory.square_side, direction),
        reduction.u_events[i],
        reduction.u_events[i + 1],
        reduction.v_events[j],
        reduction.v_events[j + 1],
    )
    half = inventory.square_side / 2

    def contains(x: Fraction, y: Fraction) -> bool:
        return (
            abs(direction.ux * x + direction.uy * y - witness[0]) <= half
            and abs(direction.vx * x + direction.vy * y - witness[1]) <= half
        )

    membership = exact_charge(certificate.atoms, certificate.threshold_atoms, contains)
    encoded = sum(
        (int(coefficient) * weight for coefficient, weight in zip(row, weights, strict=True)),
        start=Fraction(0),
    )
    assert encoded == membership


def test_tiny_encoding_matches_exact_minimum_charge() -> None:
    certificate = _tiny_certificate()
    inventory = inventory_certificate(certificate)
    encoding = encode_frozen_coverage(inventory)
    encoded = minimum_encoded_charge(encoding.pareto_rows, orbit_weights(inventory))
    true_mins = [
        minimum_charge(
            certificate.atoms,
            certificate.threshold_atoms,
            direction,
            certificate.outer_side,
            certificate.square_side,
        )[0]
        for direction in certificate.directions
    ]
    assert encoded == min(true_mins)


def test_omitting_a_tiny_orbit_matches_zero_weight_on_the_frozen_rows() -> None:
    certificate = _tiny_certificate()
    inventory = inventory_certificate(certificate)
    encoding = encode_frozen_coverage(inventory)
    dropped = inventory.threshold_orbits[0]
    kept = tuple(
        atom for atom in certificate.threshold_atoms if atom.key not in set(dropped.members)
    )
    omitted = ThresholdCertificate(
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
        atoms=certificate.atoms,
        threshold_atoms=kept,
        half_tangents=certificate.half_tangents,
    )
    zeroed = list(orbit_weights(inventory))
    zeroed[len(inventory.point_orbits)] = Fraction(0)
    encoded = minimum_encoded_charge(encoding.pareto_rows, zeroed)
    true_mins = [
        minimum_charge(
            omitted.atoms,
            omitted.threshold_atoms,
            direction,
            omitted.outer_side,
            omitted.square_side,
        )[0]
        for direction in omitted.directions
    ]
    assert encoded == min(true_mins)


def test_feasibility_mip_finds_a_one_orbit_cover_and_does_not_reject_infeasibility() -> None:
    encoding = FrozenCoverageEncoding(
        orbit_count=1,
        direction_count=1,
        reachable_cells=1,
        direction_unique_rows=1,
        pareto_rows=np.array([[1]], dtype=np.uint8),
        budget_coefficients=(1,),
        rows_sha256="0" * 64,
    )
    feasible = solve_feasibility_mip(encoding, max_orbits=1, budget_below=11)
    assert feasible.status == "feasible_unverified"
    assert feasible.n_plus == 1
    infeasible = FrozenCoverageEncoding(
        orbit_count=2,
        direction_count=1,
        reachable_cells=2,
        direction_unique_rows=2,
        pareto_rows=np.array([[1, 0], [0, 1]], dtype=np.uint8),
        budget_coefficients=(1, 1),
        rows_sha256="0" * 64,
    )
    blocked = solve_feasibility_mip(infeasible, max_orbits=1, budget_below=11)
    assert blocked.status == "float_infeasible_unresolved"
    assert blocked.n_plus is None
