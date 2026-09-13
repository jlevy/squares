"""The plateau reader decides exactly, catches planted violations, and clears feasible ones.

Quick tests run on hand-built families (a single core, pairwise disjoint cores, a planted
non-Helly triple) and on the arithmetic the reader rests on. The 88-core ceiling family
at 191/50 is the retained control and its searches are marked ``slow``; the numbers they
must reproduce are the ones agenda-034 recorded: two-of-three ``5/4`` at memberships
``(4, 8, 8)``, the corner clique of eleven entries at ``11/8`` with ``tau* = 5/3``, the
wall lines at exactly ``3`` of chord at least ``0.99``.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import plateau_reader as pr
from sqpack.fractional.ceiling import CeilingCertificate, Placement

F = Fraction

PACKING = Path(__file__).resolve().parents[1]
CEILING_FAMILY = (
    PACKING
    / "campaign/series/series-000-smoke-and-calibration/results/agenda-034"
    / "ceiling-family-191-50.json"
)


def family(placements: list[Placement], side: str = "3") -> CeilingCertificate:
    return CeilingCertificate(1, F(side), F(1), (F(0), F(1, 2)), tuple(placements))


def square(t: str, x: str, y: str, w: str) -> Placement:
    return Placement(F(t), F(x), F(y), F(w), F(1))


@pytest.fixture
def single_core() -> CeilingCertificate:
    return family([square("0", "1", "1", "1")])


@pytest.fixture
def disjoint_cores() -> CeilingCertificate:
    # Four unit squares tiling the corners of side 3 with gaps: no two share a point.
    return family(
        [
            square("0", "1/2", "1/2", "1"),
            square("0", "5/2", "1/2", "1"),
            square("0", "1/2", "5/2", "1"),
            square("0", "5/2", "5/2", "1"),
        ]
    )


@pytest.fixture
def non_helly() -> CeilingCertificate:
    """Two axis squares meeting on [11/10, 3/2]^2, a rotated one meeting both but not the box.

    Weight 1/2 each: depth at most 1 everywhere, two-of-three charge 3/2.
    """

    return family(
        [
            square("0", "1", "1", "1/2"),
            square("0", "8/5", "8/5", "1/2"),
            square("1/2", "19/10", "7/10", "1/2"),
        ]
    )


@pytest.fixture(scope="module")
def ceiling() -> pr.Arrangement:
    if not CEILING_FAMILY.exists():
        pytest.skip("the retained ceiling family is not in this checkout")
    return pr.read_arrangement(pr.load_family(CEILING_FAMILY))


# ---------------------------------------------------------------------------------
# Arithmetic
# ---------------------------------------------------------------------------------


def test_surd_comparison_is_exact() -> None:
    root = pr.Surd(F(0), F(1))
    assert pr.Surd(F(14, 10)) < root < pr.Surd(F(15, 10))
    assert pr.Surd(F(1414213, 10**6)) < root < pr.Surd(F(1414214, 10**6))
    assert (root * root) == pr.Surd(F(2))
    assert (root - root).sign() == 0
    assert pr.Surd(F(-3), F(2)) < pr.Surd(F(0))
    assert pr.Surd(F(-2), F(2)) > pr.Surd(F(0))
    assert pr.Surd(F(3), F(-2)) > pr.Surd(F(0))
    assert pr.Surd(F(2), F(-2)) < pr.Surd(F(0))


def test_axis_chord_interval_is_the_closed_support() -> None:
    line = pr.LineFamily("horizontal", F(0), F(1))
    core = square("0", "1", "1", "1")
    assert line.chord_interval(core, line.threshold(F(1))) == (
        pr.Surd(F(1, 2)),
        pr.Surd(F(3, 2)),
    )
    assert line.chord_interval(core, line.threshold(F(11, 10))) is None
    assert line.extent_at(core, pr.Surd(F(1))) == pr.Surd(F(1))
    assert line.extent_at(core, pr.Surd(F(2))) is None


def test_diagonal_chord_interval_has_irrational_symmetric_endpoints() -> None:
    line = pr.LineFamily("diagonal x+y", F(1), F(1))
    core = square("0", "1", "1", "1")
    interval = line.chord_interval(core, line.threshold(F(1)))
    assert interval is not None
    lo, hi = interval
    assert lo.b != 0
    assert lo + hi == pr.Surd(F(4))
    assert lo < pr.Surd(F(2)) < hi
    assert pr.Surd(F(1)) < lo
    assert hi < pr.Surd(F(3))
    # The diagonal through the centre has chord sqrt 2, extent 1 in the line parameter.
    assert line.extent_at(core, pr.Surd(F(2))) == pr.Surd(F(1))


def test_integer_membership_agrees_with_fraction_containment(
    non_helly: CeilingCertificate,
) -> None:
    arrangement = pr.read_arrangement(non_helly)
    squares = [pr.IntegerSquare.of(p) for p in non_helly.placements]
    for vertex in arrangement.vertices:
        integer = pr.integer_vertex(vertex)
        for placement, fast in zip(non_helly.placements, squares, strict=True):
            assert fast.contains(integer) == placement.contains(*vertex)


def test_exact_simplex_finds_the_piercing_number_of_a_triangle() -> None:
    # Three cores, candidate points at the three pairwise intersections: tau* = 3/2.
    rows = [0b011, 0b101, 0b110]
    value, packing, measure = pr.exact_packing_simplex(rows, [0, 1, 2])
    assert value == F(3, 2)
    assert sum(packing) == F(3, 2)
    assert sum(measure) == F(3, 2)
    assert all(
        sum(measure[i] for i, row in enumerate(rows) if row >> m & 1) >= 1 for m in range(3)
    )


def test_verify_atom_counts_multiplicities_and_floors() -> None:
    core = square("0", "1", "1", "1")
    fam = family([core, square("0", "5/2", "5/2", "1")])
    points = [pr.WeightedPoint((F(1), F(1)), 2), pr.WeightedPoint((F(5, 2), F(5, 2)), 1)]
    verdict = pr.verify_atom(fam, points, 2, label="test")
    assert verdict.budget == 1
    assert verdict.threshold_charge == 1
    assert verdict.floor_charge == 1
    record = verdict.record()
    assert record["site_count"] == 2
    assert record["token_count"] == 3
    assert "size" not in record
    floor = pr.verify_atom(fam, [pr.WeightedPoint((F(1), F(1)), 4)], 2, label="test")
    assert floor.budget == 2
    assert floor.threshold_charge == 1
    assert floor.floor_charge == 2


# ---------------------------------------------------------------------------------
# Feasible families clear every search
# ---------------------------------------------------------------------------------


def _quick_options() -> pr.ReaderOptions:
    return pr.ReaderOptions(cg_thresholds=(2, 3), time_limit=10.0)


def test_a_single_core_has_no_violated_atom(single_core: CeilingCertificate) -> None:
    report = pr.read_plateau(single_core, _quick_options())
    assert report.refused is None
    assert report.violated == []
    assert report.two_of_three is not None
    assert report.two_of_three.best == 0
    assert report.cliques is not None
    assert report.cliques.maximal_above_one == 0
    assert all(not line.max_slack_violation > 0 for line in report.lines)
    assert all(s.atom is None or not s.atom.violated for s in report.separations)
    assert {s["status"] for s in report.statements} == {"feasible", "never", "bounded"}


def test_disjoint_cores_have_no_violated_atom(disjoint_cores: CeilingCertificate) -> None:
    report = pr.read_plateau(disjoint_cores, _quick_options())
    assert report.refused is None
    assert report.violated == []
    arrangement = report.arrangement
    assert arrangement is not None
    assert report.two_of_three is not None
    assert arrangement.rational(report.two_of_three.best) == 1
    assert report.cliques is not None
    assert report.cliques.edges == 0
    assert report.three_of_five is not None
    assert report.three_of_five.complete
    for line in report.lines:
        assert line.max_slack_violation <= 0
    assert all(s["status"] != "violated" for s in report.statements)


def test_a_family_above_depth_one_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    deep = family([square("0", "1", "1", "1"), square("0", "3/2", "3/2", "1")])
    report = pr.read_plateau(deep)
    assert report.refused is not None
    assert "depth 2" in report.refused
    path = tmp_path / "deep.json"
    path.write_text(json.dumps(deep.to_record()))
    assert pr.main([str(path), "--quiet"]) == 2
    assert "REFUSED" in capsys.readouterr().out


# ---------------------------------------------------------------------------------
# A planted violation is caught by every search that applies
# ---------------------------------------------------------------------------------


def test_the_non_helly_triple_is_caught_by_two_of_three(non_helly: CeilingCertificate) -> None:
    arrangement = pr.read_arrangement(non_helly)
    assert arrangement.max_depth == arrangement.scale
    table = pr.MaskTable(arrangement)
    search = pr.two_of_three_maximum(arrangement, table)
    assert arrangement.rational(search.best) == F(3, 2)
    assert search.complete
    sizes = sorted(arrangement.masks[i].bit_count() for i in search.witnesses[0])
    assert sizes == [2, 2, 2]
    atom = pr.shape_atom(arrangement, search.witnesses[0], 2, "two-of-three")
    assert atom.threshold_charge == F(3, 2)
    assert atom.budget == 1
    assert atom.violated
    depth_first = pr.k_of_search(arrangement, 2, table)
    assert depth_first.complete
    assert depth_first.best == search.best
    three_of_five = pr.k_of_search(arrangement, 3, table)
    assert three_of_five.complete
    assert arrangement.rational(three_of_five.best) == 1


def test_the_non_helly_triple_is_caught_by_the_clique_scan(
    non_helly: CeilingCertificate,
) -> None:
    arrangement = pr.read_arrangement(non_helly)
    scan = pr.clique_scan(arrangement)
    assert scan.edges == 3
    assert scan.maximal_above_one == 1
    assert scan.enumeration_complete
    assert scan.heaviest_rank_one_weight == F(3, 2)
    assert scan.heaviest_rank_one_tau is not None
    assert scan.heaviest_rank_one_tau.exact
    assert scan.heaviest_rank_one_tau.value == F(3, 2)
    assert scan.atom is not None
    assert scan.atom.budget == 1
    assert scan.atom.threshold_charge == F(3, 2)
    assert scan.atom.violated


def test_the_non_helly_triple_is_caught_by_separation(non_helly: CeilingCertificate) -> None:
    arrangement = pr.read_arrangement(non_helly)
    result = pr.cg_separation(arrangement, 2, time_limit=10.0)
    assert result.atom is not None
    assert result.exact_objective == F(1, 2)
    assert result.atom.floor_charge == F(3, 2)
    assert result.atom.budget == 1
    shape = pr.cg_separation(
        arrangement, 3, max_multiplicity=1, total_multiplicity=5, time_limit=10.0
    )
    assert shape.exact_objective is None or shape.exact_objective <= 0


def test_the_non_helly_triple_report_ranks_its_violations(
    non_helly: CeilingCertificate, tmp_path: Path
) -> None:
    report = pr.read_plateau(non_helly, _quick_options())
    assert report.refused is None
    assert report.violated
    assert report.violated[0].floor_violation == F(1, 2)
    families = {atom.family for atom in report.violated}
    assert "two-of-three" in families
    assert any("clique" in name for name in families)
    assert any("Chvátal-Gomory" in name for name in families)
    assert all(line.max_slack_violation <= 0 for line in report.lines)
    statuses = {s["family"]: s["status"] for s in report.statements}
    assert statuses["two-of-three"] == "violated"
    assert statuses["line chords (collinear atoms, continuum form)"] == "never"
    record = report.record()
    assert record["violated_atoms"][0]["floor_violation"] == "1/2"
    path = tmp_path / "triple.json"
    path.write_text(json.dumps(non_helly.to_record()))
    out = tmp_path / "report.json"
    assert (
        pr.main(
            [
                str(path),
                "--quiet",
                "--time-limit",
                "10",
                "--cg-thresholds",
                "2",
                "--out",
                str(out),
            ]
        )
        == 0
    )
    written = json.loads(out.read_text())
    assert written["kind"] == "plateau-reader/v2"
    assert written["k4_two_of_three"]["max_charge"] == "3/2"
    assert written["violated_atoms"]


def test_pruned_clique_enumeration_matches_the_unpruned_one(
    non_helly: CeilingCertificate,
) -> None:
    extra = family(
        [
            *non_helly.placements,
            square("0", "1", "23/10", "1/2"),
            square("1/2", "12/5", "23/10", "1/2"),
            square("0", "5/2", "5/4", "1/4"),
        ]
    )
    arrangement = pr.read_arrangement(extra)
    adjacency = pr.intersection_graph(extra)
    pruned, complete = pr.maximal_cliques_above(arrangement, adjacency, arrangement.scale)
    everything, _ = pr.maximal_cliques_above(arrangement, adjacency, -1)
    assert complete
    assert sorted(pruned) == sorted(
        c for c in everything if arrangement.weight_of(c) > arrangement.scale
    )
    for clique in everything:
        members = arrangement.members(clique)
        assert all(adjacency[a] >> b & 1 for a in members for b in members if a != b)


# ---------------------------------------------------------------------------------
# The retained control: the 88-core ceiling family at 191/50
# ---------------------------------------------------------------------------------


@pytest.mark.slow
def test_ceiling_family_two_of_three_is_exactly_five_quarters(ceiling: pr.Arrangement) -> None:
    assert len(ceiling.masks) == 1541
    assert ceiling.scale == 8
    assert ceiling.max_depth == 8
    search = pr.two_of_three_maximum(ceiling)
    assert search.complete
    assert ceiling.rational(search.best) == F(5, 4)
    sparsest = sorted(ceiling.masks[i].bit_count() for i in search.witnesses[0])
    assert sparsest == [4, 8, 8]
    atom = pr.shape_atom(ceiling, search.witnesses[0], 2, "two-of-three")
    assert atom.threshold_charge == F(5, 4)
    assert atom.budget == 1


def test_ceiling_family_corner_clique_is_eleven_eighths_at_tau_five_thirds(
    ceiling: pr.Arrangement,
) -> None:
    scan = pr.clique_scan(ceiling)
    assert scan.edges == 824
    assert scan.enumeration_complete
    assert scan.maximal_above_one == 52
    assert scan.heaviest_weight == F(11, 8)
    assert scan.heaviest_rank_one_weight == F(11, 8)
    assert scan.heaviest_rank_one_clique is not None
    assert scan.heaviest_rank_one_clique.bit_count() == 11
    assert scan.heaviest_rank_one_tau is not None
    assert scan.heaviest_rank_one_tau.exact
    assert scan.heaviest_rank_one_tau.value == F(5, 3)
    assert scan.atom is not None
    assert scan.atom.budget == 1
    assert scan.atom.threshold_charge >= F(11, 8)
    assert scan.atom.violated


def test_ceiling_family_wall_lines_are_tight_at_three(ceiling: pr.Arrangement) -> None:
    lines = pr.line_chords(ceiling.family, thresholds=(F(99, 100),))
    horizontal = next(line for line in lines if line.direction == "horizontal")
    assert horizontal.max_count == 3
    assert horizontal.max_count_budget == 3
    assert horizontal.max_slack_violation == 0
    assert horizontal.tight_somewhere
    named = {entry["offset"]: entry["weight"] for entry in horizontal.named}
    assert all(named[offset] == "3" for offset in ("1/10", "1/4", "1/2", "3/4"))
    assert named["1/100"] == "9/4"
    for line in lines:
        assert line.max_slack_violation <= 0


@pytest.mark.slow
def test_ceiling_family_separation_is_at_least_the_two_of_three_cut(
    ceiling: pr.Arrangement,
) -> None:
    result = pr.cg_separation(ceiling, 2, time_limit=60.0)
    assert result.atom is not None
    assert result.exact_objective is not None
    assert result.exact_objective >= F(1, 4)
