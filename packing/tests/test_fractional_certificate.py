"""Controls for the weighted fractional unavoidable-set instrument.

The positive control is the published one: Massaccesi's retained n = 17
certificate must be accepted, and the side it bounds must be the 4.5058 the
source reports. That number is the whole point of the control -- an earlier
reading of the theorem divided by the shrunken side and would have claimed
4.51799, overstating a published result.
"""

from __future__ import annotations

import hashlib
import json
import runpy
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from cases.n11_fractional_certificate.__main__ import replay as replay_n11
from cases.n11_fractional_certificate.replay import CERTIFICATE_PATH as N11_CERTIFICATE_PATH
from cases.n11_fractional_certificate.replay import FIRST_RUNG_PATH as N11_FIRST_RUNG
from cases.n11_fractional_certificate.replay import STROMQUIST_RUNG_PATH
from cases.n11_fractional_certificate.replay import declared as n11_declared
from cases.n11_fractional_certificate.replay import load as n11_load
from cases.n12_fractional_certificate.replay import FIRST_RUNG_PATH, declared, load
from cases.n17_fractional_certificate.replay import declared as n17_declared
from cases.n17_fractional_certificate.replay import load as n17_load
from cases.n17_weighted_certificate.fixture import load_retained_fixture
from sqpack.fractional.certificate import Certificate, verify
from sqpack.fractional.generate import build_site_grid, rationalise
from sqpack.fractional.model import Atom, Direction, rotation_from_half_tangent
from sqpack.fractional.sweep import minimum_covered_mass, reduce_to_cells

MASSACCESI_LIMIT = Fraction(207107, 500000)


def retained_certificate(steps: int | None = None) -> Certificate:
    """The retained n = 17 data, re-encoded into the first-party types."""
    fixture = load_retained_fixture()
    scale = Fraction(fixture.weight_scale)
    atoms = tuple(
        Atom(atom.label, atom.x, atom.y, atom.weight / scale) for atom in fixture.atoms
    )
    count = fixture.direction_steps if steps is None else steps
    tangents = tuple(fixture.angle_limit * k / count for k in range(count + 1))
    return Certificate(
        n=17,
        outer_side=fixture.outer_side,
        square_side=fixture.square_side,
        atoms=atoms,
        half_tangents=tangents,
    )


def test_the_retained_certificate_bounds_the_side_its_source_reports() -> None:
    certificate = retained_certificate()
    assert certificate.bounded_side == Fraction(22529, 5000)
    assert float(certificate.bounded_side) == pytest.approx(4.5058)
    assert certificate.total_mass == Fraction(203, 12)
    assert certificate.total_mass < 17


def test_a_coarse_net_still_accepts_the_retained_atoms() -> None:
    """C4 on a sub-net of the published one: the atoms cover it too."""
    verdict = verify(retained_certificate(steps=6))
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass >= 1


@pytest.mark.exhaustive_exact
def test_the_full_retained_certificate_is_accepted() -> None:
    verdict = verify(retained_certificate())
    assert verdict.accepted, verdict.failures
    assert verdict.minimum_cell_mass == 1


def test_mass_reaching_n_is_refused() -> None:
    """C1 is strict: a total that only reaches n proves nothing."""
    base = retained_certificate(steps=6)
    inflated = Fraction(17, len(base.atoms))
    heavy = Certificate(
        n=17,
        outer_side=base.outer_side,
        square_side=base.square_side,
        atoms=tuple(Atom(a.label, a.x, a.y, inflated) for a in base.atoms),
        half_tangents=base.half_tangents,
    )
    assert heavy.total_mass == 17
    assert "C1 total mass below n" in verify(heavy).failures


def test_signed_weight_counterexample_is_refused_before_verification() -> None:
    """Signed mass satisfies C0--C4 here even though one unit square fits.

    The centre has weight 2 and the four corners weight -1. Every contained
    side-3/5 square at the two net directions covers mass at least 1, while the
    total is -2. Nonnegative weights must therefore be a construction
    precondition, before either the verifier or its open-cell sweep can run.
    """
    outer_side = Fraction(11, 10)
    atoms = (
        Atom("centre", Fraction(11, 20), Fraction(11, 20), Fraction(2)),
        Atom("lower-left", Fraction(0), Fraction(0), Fraction(-1)),
        Atom("lower-right", outer_side, Fraction(0), Fraction(-1)),
        Atom("upper-left", Fraction(0), outer_side, Fraction(-1)),
        Atom("upper-right", outer_side, outer_side, Fraction(-1)),
    )

    with pytest.raises(ValueError, match="atom weights must be nonnegative"):
        Certificate(
            n=1,
            outer_side=outer_side,
            square_side=Fraction(3, 5),
            atoms=atoms,
            half_tangents=(Fraction(0), Fraction(1, 2)),
        )
    with pytest.raises(ValueError, match="atom weights must be nonnegative"):
        reduce_to_cells(
            atoms,
            rotation_from_half_tangent("counterexample", Fraction(0)),
            outer_side,
            Fraction(3, 5),
        )


@pytest.mark.parametrize(
    ("field", "wrong", "message"),
    [
        ("claim", "s(2) >= 2", "retained claim disagrees"),
        ("total_mass", "0", "retained total mass disagrees"),
        ("least_cell_mass", "2", "retained least cell mass disagrees"),
    ],
)
def test_n11_replay_refuses_declared_value_drift(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    field: str,
    wrong: str,
    message: str,
) -> None:
    """A retained record may not print VERIFIED under stale bookkeeping."""
    record = {
        "id": "small-replay-control",
        "n": 2,
        "outer_side": "1",
        "square_side": "3/5",
        "angle_limit": "1/2",
        "direction_steps": 1,
        "symmetry": "D4",
        "claim": "s(2) >= 1",
        "total_mass": "1",
        "least_cell_mass": "1",
        "atoms": [["1/2", "1/2", "1"]],
    }
    record[field] = wrong
    path = tmp_path / "certificate.json"
    path.write_text(json.dumps(record), encoding="utf-8")

    assert replay_n11(path) == 1
    assert message in capsys.readouterr().out


def test_a_net_short_of_an_eighth_turn_is_refused() -> None:
    """C2: the D4 reduction needs the arc to reach pi/4, and 0.41 does not."""
    base = retained_certificate(steps=6)
    short = Certificate(
        n=17,
        outer_side=base.outer_side,
        square_side=base.square_side,
        atoms=base.atoms,
        half_tangents=tuple(Fraction(41, 100) * k / 6 for k in range(7)),
    )
    assert "C2 net reaches pi/4" in verify(short).failures


def test_a_net_too_coarse_for_containment_is_refused() -> None:
    """C3: with few directions the angular gap outgrows the shrink."""
    base = retained_certificate(steps=2)
    assert "C3 containment B(1 + D) < 1" in verify(base).failures


def test_a_lightened_atom_breaks_the_covering_condition() -> None:
    """C4 is tight on the retained certificate, so any loss is visible."""
    base = retained_certificate(steps=6)
    lightened = (
        Atom(base.atoms[0].label, base.atoms[0].x, base.atoms[0].y, Fraction(0)),
        *base.atoms[1:],
    )
    thin = Certificate(
        n=17,
        outer_side=base.outer_side,
        square_side=base.square_side,
        atoms=lightened,
        half_tangents=base.half_tangents,
    )
    verdict = verify(thin)
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass < 1
    assert "C4 every reachable cell carries mass 1" in verdict.failures


def test_the_half_angle_parametrisation_is_exactly_unit_length() -> None:
    for k in range(13):
        direction = rotation_from_half_tangent(str(k), MASSACCESI_LIMIT * k / 12)
        assert direction.ux**2 + direction.uy**2 == 1


def test_a_direction_off_the_unit_circle_is_refused() -> None:
    with pytest.raises(ValueError, match="unit length"):
        Direction("bad", Fraction(1), Fraction(1), Fraction(-1), Fraction(1))


def test_the_largest_half_gap_tangent_is_exact_on_a_uniform_net() -> None:
    """A uniform half-tangent net has its widest angular gap at zero."""
    certificate = retained_certificate(steps=180)
    assert certificate.largest_half_gap_tangent == MASSACCESI_LIMIT / 180


@pytest.mark.exhaustive_exact
def test_the_retained_n12_certificate_replays_and_is_accepted() -> None:
    """The n = 12 result, replayed from its retained file and re-decided.

    This is the whole claim in one assertion: a certificate whose atoms carry
    D4 symmetry, whose mass is 479713/40000 and so strictly under 12, and whose
    least covered mass is 100003/100000, proves that twelve unit squares do not
    fit in a container of side 197/50.
    """
    certificate = load()
    assert certificate.n == 12
    assert certificate.bounded_side == Fraction(197, 50)
    assert certificate.total_mass == Fraction(479713, 40000)
    assert certificate.total_mass < 12

    verdict = verify(certificate)
    assert verdict.accepted, verdict.failures
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass >= 1

    record = declared()
    assert record["claim"] == "s(12) >= 197/50"
    assert record["total_mass"] == str(certificate.total_mass)
    assert record["least_cell_mass"] == str(verdict.minimum_cell_mass)


def test_the_first_rung_at_19_5_still_replays() -> None:
    """The smaller certificate the instrument found first is kept and stays true."""
    certificate = load(FIRST_RUNG_PATH)
    assert certificate.bounded_side == Fraction(19, 5)
    assert certificate.total_mass == Fraction(58, 5)
    assert len(certificate.atoms) == 68
    verdict = verify(certificate)
    assert verdict.accepted, verdict.failures
    assert declared(FIRST_RUNG_PATH)["claim"] == "s(12) >= 19/5"


def test_the_n12_certificate_improves_the_inherited_bound() -> None:
    """197/50 beats 2 + 4/sqrt(5), which n = 12 only held by monotonicity."""
    bound = load().bounded_side
    # L > 2 + 4/sqrt(5) iff (L - 2) > 4/sqrt(5) iff (L - 2)^2 * 5 > 16,
    # both sides being positive. Decided in exact rationals, not in floats.
    assert bound > 2
    assert (bound - 2) ** 2 * 5 > 16


def test_breaking_the_symmetry_of_the_n12_atoms_is_refused() -> None:
    """C0 is not decoration: drop one orbit member and the reduction is void."""
    certificate = load()
    maimed = Certificate(
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
        atoms=certificate.atoms[1:],
        half_tangents=certificate.half_tangents[:4],
    )
    assert "C0 atoms carry the declared symmetry" in verify(maimed).failures


def test_the_independent_verifier_agrees_on_the_first_rung() -> None:
    """The reviewer's from-the-theorem verifier, on two directions of the 19/5 rung.

    Kept fast by restricting to the first and last net directions; the full
    181-direction agreement is recorded in the evidence register.
    """
    package = Path(__file__).parents[1] / "cases/n12_fractional_certificate"
    module = runpy.run_path(
        str(package / "independent_verify.py"), run_name="independent_verify"
    )
    certificate = module["load"](str(FIRST_RUNG_PATH))
    accepted, report = module["verify"](certificate, ks=[0, 180], label="19/5")
    assert accepted, report
    assert report["info"]["min_rep"] == Fraction(1)


@pytest.mark.exhaustive_exact
def test_the_independent_verifier_agrees_on_the_full_n11_certificate() -> None:
    """A source-distinct exact decision over all 181 directions of the new bound."""
    package = Path(__file__).parents[1] / "cases/n12_fractional_certificate"
    module = runpy.run_path(
        str(package / "independent_verify.py"), run_name="independent_verify"
    )
    certificate = module["load"](str(N11_CERTIFICATE_PATH))
    accepted, report = module["verify"](
        certificate,
        ks=None,
        label="independent n=11 full net",
        brute_check=3,
    )
    assert accepted, report
    assert report["info"]["min_lower"] == Fraction(4001, 4000)
    assert report["info"]["min_rep"] == Fraction(4001, 4000)


def test_containment_at_exactly_one_is_refused() -> None:
    """C3 must be strict: equality leaves the shrunken squares able to touch,
    and touching closed squares can share an atom, which breaks the count."""
    base = retained_certificate(steps=180)
    gap = base.largest_half_gap_tangent
    touching = Certificate(
        n=17,
        outer_side=base.outer_side,
        square_side=1 / (1 + gap),
        atoms=base.atoms,
        half_tangents=base.half_tangents,
    )
    assert touching.square_side * (1 + gap) == 1
    assert "C3 containment B(1 + D) < 1" in verify(touching).failures


def test_rationalise_rounds_weights_up_never_down() -> None:
    """D-433: the rounding step floored while its docstring said ceil.

    Every coverage row the solver leaves tight sits exactly at 1, so any downward
    rounding refuses a certificate the program had found. Weights that are not
    multiples of 1/scale must land on the next multiple above, never below.
    """
    grid = build_site_grid(Fraction(4), 3, Fraction(1, 2))
    weights = np.array([5.3 / 576, 0.5 / 576, 1000.001 / 576][: len(grid.orbits)])
    atoms = rationalise(grid, weights, scale=576, bump=Fraction(1))
    by_orbit = {}
    for atom in atoms:
        by_orbit.setdefault(atom.weight, 0)
        by_orbit[atom.weight] += 1
    assert Fraction(6, 576) in by_orbit
    assert Fraction(1, 576) in by_orbit
    assert Fraction(1001, 576) in by_orbit
    assert all(w * 576 >= 1 for w in by_orbit)


def test_the_sweep_scores_every_cell_it_scored_before() -> None:
    """A guard against the verifier being "repaired" by narrowing its cell set.

    C4 is only as strong as the set of placements it quantifies over, and a
    change that drops cells makes every certificate easier to accept while
    every retained certificate still passes -- so the retained ones cannot
    catch it. These counts are the exact cell sets the accepted n = 12
    certificate was decided on. If a change lowers one, the verifier is
    deciding fewer placements than it used to, and the results registered
    against it no longer mean what they said.
    """
    certificate = load(
        Path(__file__).parents[1] / "cases/n12_fractional_certificate/certificate-77-20.json"
    )
    expected = {0: 1225, 1: 36481, 45: 38733, 90: 37733, 180: 36837}
    for index, count in expected.items():
        direction = rotation_from_half_tangent(str(index), certificate.half_tangents[index])
        reduction = reduce_to_cells(
            certificate.atoms,
            direction,
            certificate.outer_side,
            certificate.square_side,
        )
        assert len(reduction.cells) == count, (
            f"direction {index}: {len(reduction.cells)} cells, was {count}"
        )


def test_minimum_mass_witness_lies_in_feasible_part_of_event_cell() -> None:
    """The raw midpoint of a reachable corner cell can hang outside the container."""
    direction = Direction(
        "three-four-five",
        Fraction(3, 5),
        Fraction(4, 5),
        Fraction(-4, 5),
        Fraction(3, 5),
    )
    atoms = (Atom("cut", Fraction(14, 125), Fraction(227, 125), Fraction(1)),)
    outer_side = Fraction(2)
    square_side = Fraction(1)

    reduction = reduce_to_cells(atoms, direction, outer_side, square_side)
    assert reduction.cells[0] == (0, 0)
    raw_midpoint = (Fraction(1), Fraction(-1, 5))
    raw_y = direction.uy * raw_midpoint[0] + direction.vy * raw_midpoint[1]
    margin = square_side * (direction.ux + direction.uy) / 2
    assert raw_y == Fraction(17, 25) < margin

    mass, witness = minimum_covered_mass(atoms, direction, outer_side, square_side)
    assert mass == 0
    assert witness != raw_midpoint
    i, j = reduction.cells[0]
    assert reduction.u_events[i] < witness[0] < reduction.u_events[i + 1]
    assert reduction.v_events[j] < witness[1] < reduction.v_events[j + 1]
    x = direction.ux * witness[0] + direction.vx * witness[1]
    y = direction.uy * witness[0] + direction.vy * witness[1]
    assert margin <= x <= outer_side - margin
    assert margin <= y <= outer_side - margin


def test_the_retained_atoms_are_refused_in_a_container_they_cannot_cover() -> None:
    """The must-refuse fixture: same atoms, a container too large for them.

    The independent reviewer measured least covered mass 1/10 here. A verifier
    that accepted this would be accepting a certificate whose squares can be
    placed where no atom reaches, which is the failure a narrowed cell set
    produces.
    """
    certificate = load()
    too_large = Certificate(
        n=certificate.n,
        outer_side=Fraction(4),
        square_side=certificate.square_side,
        atoms=certificate.atoms,
        half_tangents=certificate.half_tangents[:8],
    )
    verdict = verify(too_large)
    assert not verdict.accepted
    assert "C4 every reachable cell carries mass 1" in verdict.failures
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass < 1


def test_the_n11_certificate_beats_stromquists_2003_bound() -> None:
    """s(11) >= 381/100, read from its own file.

    2 + 4/sqrt(5) = 3.788854 had stood since Stromquist 2003 and was the only
    bound n = 11 had. The comparison is decided in exact rationals: L > 2 +
    4/sqrt(5) iff (L - 2)^2 * 5 > 16, both sides being positive.

    What the certificate claims is checked here; that a verifier accepts it is
    the exhaustive test below.
    """

    certificate = n11_load()
    assert certificate.n == 11
    assert certificate.bounded_side == Fraction(381, 100)
    assert certificate.total_mass == Fraction(434547, 40000)
    assert certificate.total_mass < 11
    assert (certificate.bounded_side - 2) ** 2 * 5 > 16

    record = n11_declared()
    assert record["claim"] == "s(11) >= 381/100"
    assert record["total_mass"] == str(certificate.total_mass)
    assert hashlib.sha256(N11_CERTIFICATE_PATH.read_bytes()).hexdigest() == (
        "b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a"
    )


@pytest.mark.exhaustive_exact
def test_the_n11_certificate_is_accepted() -> None:
    """The 1121-atom certificate over 181 directions, decided exactly."""
    certificate = n11_load()
    verdict = verify(certificate)
    assert verdict.accepted, verdict.failures
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass >= 1
    record = n11_declared()
    assert record["claim"] == "s(11) >= 381/100"
    assert record["total_mass"] == str(certificate.total_mass)
    assert record["least_cell_mass"] == str(verdict.minimum_cell_mass)


def test_the_n11_rung_at_19_5_still_replays() -> None:
    """The value that first passed Stromquist is kept and stays true."""
    certificate = n11_load(STROMQUIST_RUNG_PATH)
    assert certificate.bounded_side == Fraction(19, 5)
    assert certificate.total_mass == Fraction(43391, 4000)
    assert len(certificate.atoms) == 425
    assert n11_declared(STROMQUIST_RUNG_PATH)["claim"] == "s(11) >= 19/5"


@pytest.mark.exhaustive_exact
def test_the_n11_calibration_rung_below_stromquist_also_verifies() -> None:
    """189/50 proves nothing new, which is exactly why it was run first."""

    certificate = n11_load(N11_FIRST_RUNG)
    assert certificate.bounded_side == Fraction(189, 50)
    assert (certificate.bounded_side - 2) ** 2 * 5 < 16
    assert verify(certificate).accepted


def test_every_retained_n12_rung_still_verifies() -> None:
    """The ladder is evidence, not clutter: each rung must still be true.

    Kept cheap by deciding each rung on a coarse sub-net; the full 181-direction
    decision for the top rung is the exhaustive_exact test above.
    """
    package = Path(__file__).parents[1] / "cases/n12_fractional_certificate"
    rungs = {
        "certificate-19-5.json": Fraction(19, 5),
        "certificate-77-20.json": Fraction(77, 20),
        "certificate-97-25.json": Fraction(97, 25),
        "certificate-39-10.json": Fraction(39, 10),
        "certificate-393-100.json": Fraction(393, 100),
    }
    for name, side in rungs.items():
        rung = load(package / name)
        assert rung.bounded_side == side
        assert rung.total_mass < 12
        coarse = Certificate(
            n=rung.n,
            outer_side=rung.outer_side,
            square_side=rung.square_side,
            atoms=rung.atoms,
            half_tangents=rung.half_tangents[::30],
        )
        verdict = verify(coarse)
        assert verdict.minimum_cell_mass is not None
        assert verdict.minimum_cell_mass >= 1, f"{name} lost coverage"


def test_the_n17_certificate_displaces_massaccesis_published_bound() -> None:
    """s(17) >= 451/100 beats the published value, decided from the file.

    22529/5000 = 4.5058 is Massaccesi's published value, adopted here as T-015
    and carried to n = 18 and n = 19 as T-016. This certificate is denser and
    sits at a larger side, so one object moves all three cases. The comparison
    is decided in exact rationals.

    What the certificate claims is checked here; that a verifier accepts it is
    the exhaustive test below, which costs a quarter of an hour.
    """
    certificate = n17_load()
    assert certificate.n == 17
    assert certificate.bounded_side == Fraction(451, 100)
    assert certificate.bounded_side > Fraction(22529, 5000)
    assert certificate.total_mass == Fraction(829681, 50000)
    assert certificate.total_mass < 17

    record = n17_declared()
    assert record["claim"] == "s(17) >= 451/100"
    assert record["total_mass"] == str(certificate.total_mass)


@pytest.mark.exhaustive_exact
def test_the_n17_certificate_is_accepted() -> None:
    """The 708-atom certificate over 181 directions, decided exactly.

    Marked exhaustive: this is a thirteen-minute sweep, and the fast test above
    already pins every number the record claims about the same file.
    """
    certificate = n17_load()
    verdict = verify(certificate)
    assert verdict.accepted, verdict.failures
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass >= 1
    assert n17_declared()["least_cell_mass"] == str(verdict.minimum_cell_mass)


def test_the_n17_certificate_does_not_reach_n20() -> None:
    """The scope claim: 451/100 lifts n = 17, 18 and 19, and not n = 20.

    Monotonicity carries a bound upward, so n = 20 would inherit 451/100 too --
    but Nagamochi's closed form already gives it 1 + sqrt(13), which is larger.
    Decided in integers: 1 + sqrt(13) > 451/100 iff 13 * 100^2 > (451 - 100)^2.
    """
    assert 13 * 100**2 > (451 - 100) ** 2
    assert n17_load().bounded_side == Fraction(451, 100)
