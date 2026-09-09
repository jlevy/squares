"""Controls for the generic matched owner-footprint covering instrument."""

from __future__ import annotations

import json
from fractions import Fraction

from devtools.owner_footprints import (
    OUTER_SIDE,
    Polygon,
    full_owner_direction_manifest,
    owner_branch_manifest,
    owner_class_footprints,
)
from devtools.run_owner_footprint_cover import (
    Arm,
    build_arms,
    build_receipt,
    exact_minimum_covered_mass_on_pieces,
    main,
    selected_reflected_directions,
    singleton_site_set,
    solve_program,
)
from sqpack.fractional.colgen import SiteSet, d4_orbit, rationalise_sites
from sqpack.fractional.model import Atom, rotation_from_half_tangent


def test_default_support_and_direction_subset_preserve_declared_provenance() -> None:
    manifest = owner_branch_manifest(full_owner_direction_manifest())
    owner_class = manifest.classes[0]
    sites = singleton_site_set(mark=owner_class.mark)
    assert sites.outer_side == OUTER_SIDE
    assert sites.size == 369
    assert len(sites.orbits) == 369
    assert all(len(orbit) == 1 for orbit in sites.orbits)
    assert set(d4_orbit(*owner_class.mark, OUTER_SIDE)) <= set(sites.positions())

    directions = selected_reflected_directions(manifest)
    assert len(directions) == 9
    selected_entries = tuple(
        entry for entry in manifest.directions.orientations if entry.direction in directions
    )
    assert {source.folded_index for entry in selected_entries for source in entry.sources} == {
        0,
        45,
        90,
        135,
        180,
    }
    assert directions[0].ux == 1
    assert directions[0].uy == 0


def test_four_arms_use_full_net_footprints_and_remove_only_contained_sites() -> None:
    manifest = owner_branch_manifest()
    owner_class = manifest.classes[0]
    directions = selected_reflected_directions(manifest)
    sites = singleton_site_set(grid_count=5, mark=owner_class.mark)
    arms = build_arms(
        owner_class,
        sites,
        directions,
        direction_manifest=manifest,
    )
    assert tuple(arm.label for arm in arms) == (
        "unrestricted",
        "point",
        "triangle",
        "endpoint",
    )
    expected = owner_class_footprints(owner_class, manifest.directions.directions)
    assert arms[0].footprint is None
    assert arms[1].footprint == expected["point"]
    assert arms[2].footprint == expected["triangle"]
    assert arms[3].footprint == expected["endpoint"]
    assert tuple(len(arm.removed_sites) for arm in arms) == (0, 1, 1, 2)
    for arm in arms:
        assert arm.sites.size + len(arm.removed_sites) == sites.size
        assert all(len(orbit) == 1 for orbit in arm.sites.orbits)
        assert len(arm.pieces_by_direction) == len(directions)
        assert all(pieces for pieces in arm.pieces_by_direction)


def test_default_estimate_receipt_freezes_nine_direction_four_arm_settings() -> None:
    receipt, arms, directions = build_receipt()
    assert receipt["status"] == "estimated"
    assert receipt["scientific_target_run"] is False
    settings = receipt["settings"]
    assert isinstance(settings, dict)
    assert settings["grid_count"] == 19
    assert settings["selected_canonical_directions"] == 9
    assert settings["full_owner_orientation_count"] == 361
    assert settings["owner_footprints_derived_from_full_manifest"] is True
    support = receipt["available_support"]
    assert isinstance(support, dict)
    assert support["sites"] == 369
    assert support["all_singletons"] is True
    assert len(arms) == 4
    assert len(directions) == 9
    arm_records = receipt["arms"]
    assert isinstance(arm_records, dict)
    for label in ("unrestricted", "point", "triangle", "endpoint"):
        arm_record = arm_records[label]
        assert isinstance(arm_record, dict)
        assert arm_record["proposal"] is None
        complexity = arm_record["complexity"]
        assert isinstance(complexity, dict)
        assert complexity["maximum"] < 5_000_000
        assert complexity["total_one_round"] < 30_000_000


def test_exact_reader_keeps_separate_components_and_ignores_zero_area_piece() -> None:
    axis = rotation_from_half_tangent("axis", Fraction(0))
    quarter = Fraction(1, 4)
    left: Polygon = (
        (Fraction(-5, 4), -quarter),
        (Fraction(-3, 4), -quarter),
        (Fraction(-3, 4), quarter),
        (Fraction(-5, 4), quarter),
    )
    right: Polygon = (
        (Fraction(3, 4), -quarter),
        (Fraction(5, 4), -quarter),
        (Fraction(5, 4), quarter),
        (Fraction(3, 4), quarter),
    )
    zero_area: Polygon = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(1)))
    atoms = (
        Atom("left", Fraction(-1), Fraction(0), Fraction(1)),
        Atom("right", Fraction(1), Fraction(0), Fraction(1)),
    )
    result = exact_minimum_covered_mass_on_pieces(
        atoms,
        axis,
        Fraction(1),
        (left, zero_area, right),
    )
    assert result.mass == 1
    assert result.reachable_cells == 2
    without_zero_area = exact_minimum_covered_mass_on_pieces(
        atoms, axis, Fraction(1), (left, right)
    )
    assert without_zero_area == result


def test_small_solver_converges_and_exact_reader_replays_its_rationalisation() -> None:
    axis = rotation_from_half_tangent("axis", Fraction(0))
    domain: Polygon = (
        (Fraction(3, 4), Fraction(3, 4)),
        (Fraction(5, 4), Fraction(3, 4)),
        (Fraction(5, 4), Fraction(5, 4)),
        (Fraction(3, 4), Fraction(5, 4)),
    )
    sites = SiteSet(Fraction(2), (((Fraction(1), Fraction(1)),),))
    arm = Arm("control", None, sites, (), ((domain,),), (None,))
    solution = solve_program(
        arm,
        Fraction(1),
        (axis,),
        max_rounds=4,
        rows_per_direction=1,
        deadline_seconds=10,
        max_event_cells=100,
    )
    assert solution.converged
    assert solution.objective == 1
    atoms = rationalise_sites(sites, solution.weights, scale=1000)
    replay = exact_minimum_covered_mass_on_pieces(atoms, axis, Fraction(1), (domain,))
    assert replay.mass >= 1

    uncovered_sites = SiteSet(Fraction(4), (((Fraction(0), Fraction(0)),),))
    uncovered_domain: Polygon = (
        (Fraction(2), Fraction(2)),
        (Fraction(3), Fraction(2)),
        (Fraction(3), Fraction(3)),
        (Fraction(2), Fraction(3)),
    )
    uncovered_arm = Arm("uncovered", None, uncovered_sites, (), ((uncovered_domain,),), (None,))
    refused = solve_program(
        uncovered_arm,
        Fraction(1, 2),
        (axis,),
        max_rounds=2,
        rows_per_direction=1,
        deadline_seconds=10,
        max_event_cells=100,
    )
    assert refused.stopped == "a placement covers no candidate site"


def test_sub_float_thin_cell_uses_exact_geometry_fallback() -> None:
    axis = rotation_from_half_tangent("axis", Fraction(0))
    epsilon = Fraction(1, 10**20)
    thin: Polygon = (
        (Fraction(2), Fraction(2)),
        (Fraction(2) + epsilon, Fraction(2)),
        (Fraction(2) + epsilon, Fraction(9, 4)),
        (Fraction(2), Fraction(9, 4)),
    )
    assert float(Fraction(2) + epsilon) == float(Fraction(2))
    sites = SiteSet(Fraction(4), (((Fraction(2), Fraction(2)),),))
    arm = Arm("thin", None, sites, (), ((thin,),), (None,))
    solution = solve_program(
        arm,
        Fraction(1),
        (axis,),
        max_rounds=4,
        rows_per_direction=1,
        deadline_seconds=10,
        max_event_cells=100,
    )
    assert solution.converged
    assert solution.objective == 1


def test_estimate_only_cli_writes_no_objective(tmp_path, capsys) -> None:
    output = tmp_path / "estimate.json"
    assert (
        main(
            [
                "--output",
                str(output),
                "--estimate-only",
                "--grid-count",
                "5",
                "--folded-indices",
                "0,180",
            ]
        )
        == 0
    )
    written = json.loads(output.read_text())
    printed = json.loads(capsys.readouterr().out)
    assert written == printed
    assert written["status"] == "estimated"
    assert written["scientific_target_run"] is False
    arm_records = written["arms"]
    assert all(record["proposal"] is None for record in arm_records.values())
