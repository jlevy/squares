"""The contact-shade census reproduces both atlas rules and diagnoses light faces by hand.

The synthetic packings below are small enough that every contact and every face cause
can be written down before the tool runs: a full 2 x 2 grid (all dark), a slid column
(slack), a staggered row (offset), a square beside a 45-degree neighbour with an open
face above it (tilted neighbour and hole), the 2 x 2 grid less one square (the k^2 - 1
vacancy), and the two precision-scale cases, a gap and a sideways shift inside and
outside ten times the house tolerance.

The retained document is held to its witnesses here by recomputing a handful of records
-- three of the owner's named cases and one k^2 - 1 grid -- and to itself by rebuilding
every summary total from the retained entry rows. The byte-for-byte `--check` over all
324 records is a gate step rather than a test.
"""

from __future__ import annotations

import gzip
import json
import math
from collections import defaultdict
from functools import cache
from pathlib import Path
from typing import Any

import mpmath as mp
import pytest

from devtools.census_atlas_contact_shades import (
    OUTPUT,
    ROOT,
    RULES,
    Case,
    RuleResult,
    Scratch,
    apply_rule,
    atlas_slots,
    centre_rule_contacts,
    edge_rule_contacts,
    expected_document,
    json_differences,
    load_case,
    make_square,
    manifest_entries,
    packings_from_witness,
    project_sin_cos,
    square_kind,
    sweep_into,
    totals,
    vacancy_family,
    witness_shades,
)

HOUSE, STAGE, _STUDIO = RULES
ROOT2 = math.sqrt(2)
SAMPLE = (99, 102, 206, 268)
"""Three of the owner's named cases and the k = 10 grid less a corner."""


@cache
def retained() -> dict[str, Any]:
    return json.loads(OUTPUT.read_text(encoding="utf-8"))


@cache
def recomputed() -> dict[str, Any]:
    return expected_document([entry for entry in manifest_entries() if entry["n"] in SAMPLE])


def witness(side: float, squares: list[tuple[float, float, float]]) -> dict[str, Any]:
    """A center-angle Witness/v2 body in radians, with decimal strings as the corpus has."""
    return {
        "side": repr(side),
        "representation": "center-angle",
        "coordinates": {"angle_unit": "radians"},
        "squares": [
            {"id": index + 1, "center": [repr(x), repr(y)], "angle": repr(angle)}
            for index, (x, y, angle) in enumerate(squares)
        ],
    }


def case_of(side: float, squares: list[tuple[float, float, float]]) -> Case:
    """A case whose rendering is what the house renderer would draw: hue 0 for squares
    within its angle tolerance of the axes, shade four less its edge contacts."""
    exact, frame, degrees = packings_from_witness(witness(side, squares))
    contacts = edge_rule_contacts(exact, HOUSE)
    rendering = tuple(
        {
            "data-hue-index": "0" if abs(square.tilt) <= HOUSE.angle_tolerance else "2",
            "data-shade-index": str(4 - len(found)),
            "data-contact-sides": str(len(found)),
        }
        for square, found in zip(exact.squares, contacts, strict=True)
    )
    entry = {
        "n": len(squares),
        "source": {"kind": "synthetic"},
        "witness": {"method": "synthetic", "coordinate_provenance": "synthetic"},
    }
    return Case(len(squares), entry, exact, frame, degrees, rendering)


def results_of(case: Case) -> dict[str, RuleResult]:
    scratch = Scratch.of(case)
    return {rule.name: apply_rule(case, rule, scratch) for rule in RULES}


def causes(result: RuleResult, index: int) -> dict[str, str]:
    return {face: cause for face, (cause, _) in result.faces[index].items()}


def test_a_full_grid_is_dark_under_every_rule() -> None:
    case = case_of(2.0, [(0.5, 0.5, 0.0), (1.5, 0.5, 0.0), (0.5, 1.5, 0.0), (1.5, 1.5, 0.0)])
    for rule, result in results_of(case).items():
        assert result.counts == [4, 4, 4, 4], rule
        assert result.faces == {}, rule


def test_a_column_slid_two_hundredths_away_leaves_slack_faces() -> None:
    case = case_of(2.02, [(0.5, 0.5, 0.0), (1.52, 0.5, 0.0), (0.5, 1.5, 0.0), (1.52, 1.5, 0.0)])
    results = results_of(case)
    house = results[HOUSE.name]
    assert house.counts == [3, 3, 2, 2]
    assert causes(house, 0) == {"+x": "slack"}
    sweep = house.faces[0]["+x"][1]
    assert sweep.obstacle == "square"
    assert sweep.obstacle_id == "2"
    assert sweep.clearance == pytest.approx(0.02, abs=1e-12)
    assert causes(house, 2) == {"+x": "slack", "+y": "slack"}
    assert house.faces[2]["+y"][1].obstacle_id == "wall-top"
    assert {square_kind(causes(house, i).values()) for i in range(4)} == {"slack"}
    # The stage's 0.01 gap does not reach 0.02 either, but 0.02 is inside its tenfold band.
    stage = results[STAGE.name]
    assert stage.counts == [3, 3, 2, 2]
    assert causes(stage, 0) == {"+x": "near-miss"}
    assert square_kind(causes(stage, 0).values()) == "within-band"


def test_a_staggered_row_is_an_offset_face() -> None:
    case = case_of(2.25, [(0.5, 0.5, 0.0), (1.5, 0.5, 0.0), (0.75, 1.5, 0.0), (1.75, 1.5, 0.0)])
    house = results_of(case)[HOUSE.name]
    assert house.counts[0] == 3
    cause, sweep = house.faces[0]["+y"]
    assert cause == "offset"
    assert sweep.obstacle_id == "3"
    assert sweep.across == pytest.approx(0.25)
    assert abs(sweep.clearance) < 1e-12
    # Two upper squares meet the second square's top at once; the wider one is the obstacle.
    assert house.faces[1]["+y"][1].obstacle_id == "4"
    assert square_kind(causes(house, 0).values()) == "structural"


def test_a_tilted_neighbour_and_an_open_face_are_structural() -> None:
    case = case_of(1 + ROOT2, [(0.5, 0.5, 0.0), (1 + ROOT2 / 2, ROOT2 / 2, math.pi / 4)])
    house = results_of(case)[HOUSE.name]
    assert house.counts[0] == 2
    assert causes(house, 0) == {"+x": "tilted-neighbour", "+y": "hole-or-open"}
    tilted = house.faces[0]["+x"][1]
    assert tilted.tilt == pytest.approx(math.pi / 4)
    assert abs(tilted.clearance) < 1e-12
    assert house.faces[0]["+y"][1].clearance == pytest.approx(ROOT2)
    assert 1 not in house.faces, "the tilted square is not green, so it is not diagnosed"


def test_the_squares_beside_a_vacancy_have_three_contacts_and_render_light() -> None:
    case = case_of(2.0, [(0.5, 0.5, 0.0), (1.5, 0.5, 0.0), (0.5, 1.5, 0.0)])
    family = vacancy_family(case, results_of(case))
    assert family is not None
    assert family["vacancies"] == [[1, 1]]
    assert family["vacancy_neighbours"] == 2
    for rule in RULES:
        assert family[rule.name]["light_neighbours"] == 2
        assert family[rule.name]["light_elsewhere"] == 0
        assert family[rule.name]["neighbour_contacts"] == {"3": 2}
        assert family[rule.name]["neighbour_faces"] == {"hole-or-open": 2}


def test_a_gap_inside_ten_house_tolerances_is_a_near_miss_and_dark_on_the_stage() -> None:
    gap = 5e-6
    case = case_of(
        2 + gap,
        [(0.5, 0.5, 0.0), (1.5 + gap, 0.5, 0.0), (0.5, 1.5, 0.0), (1.5 + gap, 1.5, 0.0)],
    )
    results = results_of(case)
    house = results[HOUSE.name]
    assert causes(house, 0) == {"+x": "near-miss"}
    assert house.faces[0]["+x"][1].clearance == pytest.approx(gap, rel=1e-6)
    assert causes(house, 2) == {"+x": "near-miss", "+y": "near-miss"}
    assert {square_kind(causes(house, i).values()) for i in range(4)} == {"within-band"}
    assert results[STAGE.name].counts == [4, 4, 4, 4]


def test_a_sideways_shift_is_misaligned_for_the_house_and_a_contact_on_the_stage() -> None:
    case = case_of(2.0, [(0.5, 0.5, 0.0), (1.5, 0.5, 0.0), (0.503, 1.5, 0.0)])
    results = results_of(case)
    house = results[HOUSE.name]
    cause, sweep = house.faces[0]["+y"]
    assert cause == "misaligned"
    assert sweep.across == pytest.approx(0.003)
    assert causes(house, 2)["-x"] == "slack"
    stage = results[STAGE.name]
    assert stage.counts[0] == 4
    assert stage.counts[2] == 3, "left wall and the square below; top is 0.5 short"


def test_the_sweep_is_exact_and_ignores_a_corner_to_corner_neighbour() -> None:
    mover = make_square("1", 0.5, 0.5, 0.0)
    ahead = make_square("2", 1.8, 0.5, 0.0)
    diagonal = make_square("3", 1.5, 1.5, 0.0)
    diamond = make_square("4", 1.5 + ROOT2 / 2, 0.5, math.pi / 4)
    interval = sweep_into(mover, "+x", ahead)
    assert interval is not None
    assert interval[0] == pytest.approx(0.3)
    assert sweep_into(mover, "+x", diagonal) is None
    reached = sweep_into(mover, "+x", diamond)
    assert reached is not None
    assert reached[0] == pytest.approx(0.5)


def test_the_stage_rule_reads_the_pair_in_the_lower_indexed_squares_frame() -> None:
    """`contactFacts` measures along and across in the first square's frame only.

    Tilted 0.4 degrees, the first square sees its neighbour 0.011 across and misses; listed
    the other way round, the axis-aligned square sees 0.004 and counts the contact.
    """
    tilt = 0.4 * math.pi / 180
    packing = packings_from_witness(witness(5.0, [(2.0, 2.0, tilt), (3.0, 1.996, 0.0)]))[1]
    assert [len(found) for found in centre_rule_contacts(packing, STAGE)] == [0, 0]
    swapped = packings_from_witness(witness(5.0, [(3.0, 1.996, 0.0), (2.0, 2.0, tilt)]))[1]
    assert [len(found) for found in centre_rule_contacts(swapped, STAGE)] == [1, 1]


def test_atlas_slots_pin_right_angles_and_diagonals() -> None:
    assert atlas_slots([0.0, 0.3, 89.8, 45.0, 30.0], 0.5) == [0, 0, 0, 1, 2]


def test_the_house_replica_counts_what_the_committed_rendering_draws() -> None:
    entry = next(entry for entry in manifest_entries() if entry["n"] == 102)
    case = load_case(entry)
    counts = [len(found) for found in edge_rule_contacts(case.witness, HOUSE)]
    assert counts == [int(row["data-contact-sides"]) for row in case.rendering]


def test_a_witness_file_is_shaded_as_its_atlas_row_and_read_gzipped(tmp_path: Path) -> None:
    """`--witness` must agree with the census on a record the census holds, so that a pose
    outside the atlas, such as a regularized view, is shaded by the same rule."""
    entry = next(entry for entry in manifest_entries() if entry["n"] == 102)
    source = ROOT / entry["witness"]["path"]
    compressed = tmp_path / "n-102.yaml.gz"
    compressed.write_bytes(gzip.compress(source.read_bytes()))
    rows = {
        rule.name: {row["n"]: row for row in retained()["entries"][rule.name]} for rule in RULES
    }
    expected = {
        "house_green": rows[HOUSE.name][102]["green"],
        "house_light": rows[HOUSE.name][102]["light"],
        "stage_green": rows[STAGE.name][102]["green"],
        "stage_light": rows[STAGE.name][102]["light"],
    }
    assert witness_shades(source) == expected
    assert witness_shades(compressed) == expected


def test_a_sample_of_records_recomputes_to_the_retained_rows() -> None:
    fresh = recomputed()
    for rule in RULES:
        kept = {row["n"]: row for row in retained()["entries"][rule.name]}
        rows = fresh["entries"][rule.name]
        assert [row["n"] for row in rows] == list(SAMPLE)
        for row in rows:
            assert row == kept[row["n"]], (rule.name, row["n"])
    for n in ("102", "206", "268"):
        assert fresh["named_cases"][n] == retained()["named_cases"][n], n
    kept_families = {row["n"]: row for row in retained()["vacancy_families"]}
    assert fresh["vacancy_families"] == [kept_families[99]]
    assert kept_families[99]["atlas-house"]["light_neighbours"] == 2
    assert kept_families[99]["atlas-house"]["light_elsewhere"] == 0


def test_every_summary_total_rebuilds_from_the_retained_entry_rows() -> None:
    document = retained()
    assert document["house_replica"]["squares_disagreeing_with_rendering"] == 0
    for rule in RULES:
        rows = document["entries"][rule.name]
        assert len(rows) == 324
        summary = document["rules"][rule.name]
        assert totals(rows) == summary["totals"], rule.name
        groups: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for row in rows:
            groups["by_source_kind"][row["source_kind"]].append(row)
            groups["by_witness_class"][row["witness_class"]].append(row)
        for key, grouped in groups.items():
            assert {kind: totals(group) for kind, group in grouped.items()} == summary[key]
        regular = document["regularizable"][rule.name]
        assert summary["regularizable_records"] == [row["n"] for row in regular]
        assert summary["regularizable_squares"] == sum(
            row["squares"].get("slack", 0) + row["squares"].get("within-band", 0)
            for row in rows
        )


def test_a_stale_census_names_the_paths_that_moved() -> None:
    assert list(json_differences({"rules": {"x": [0.1]}}, {"rules": {"x": [0.2]}})) == [
        "$.rules.x[0]: retained 0.1, fresh 0.2"
    ]


def test_projection_ignores_platform_libm_and_ambient_precision(monkeypatch) -> None:
    """Both source representations retain their full census geometry across hosts."""
    source = witness(10, [(2, 3, 4 / 13), (6, 6, 5 / 17)])
    corner_source = {
        "side": "10",
        "representation": "corners",
        "coordinates": {"angle_unit": "not-applicable"},
        "squares": [
            {
                "id": 1,
                "corners": [["2", "2"], ["13/5", "14/5"], ["9/5", "17/5"], ["6/5", "13/5"]],
            }
        ],
    }
    baseline = [packings_from_witness(row) for row in (source, corner_source)]

    def wrong_libm(*_args):
        raise AssertionError("platform trig entered the retained diagnostic projection")

    for name in ("cos", "sin", "atan2"):
        monkeypatch.setattr(math, name, wrong_libm)
    project_sin_cos.cache_clear()
    with mp.workdps(5):
        actual = [packings_from_witness(row) for row in (source, corner_source)]
    assert actual == baseline
