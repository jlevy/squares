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
import math
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
from sqpack.fractional.certificate import (
    Certificate,
    ceiling_side,
    ceiling_side_for_net,
    grid_refutation_order,
    least_size_certified,
    verify,
)
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


def test_the_retained_n12_certificate_replays() -> None:
    """The n = 12 result, read from its retained file and checked against its record.

    What the certificate claims is checked here; that a verifier accepts it is
    the exhaustive test below, and the coarse-net rung test covers the same
    ladder cheaply.
    """
    certificate = load()
    assert certificate.n == 12
    assert certificate.bounded_side == Fraction(79, 20)
    assert certificate.total_mass == Fraction(1197059, 100000)
    assert certificate.total_mass < 12

    record = declared()
    assert record["claim"] == "s(12) >= 79/20"
    assert record["total_mass"] == str(certificate.total_mass)


@pytest.mark.exhaustive_exact
def test_the_retained_n12_certificate_is_accepted() -> None:
    """The 969-atom certificate over 181 directions, decided exactly."""
    certificate = load()
    verdict = verify(certificate)
    assert verdict.accepted, verdict.failures
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass >= 1
    assert declared()["least_cell_mass"] == str(verdict.minimum_cell_mass)


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
    """79/20 beats 2 + 4/sqrt(5), which n = 12 only held by monotonicity."""
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


def test_the_n11_calibration_rung_below_stromquist_also_verifies() -> None:
    """189/50 proves nothing new, which is exactly why it was run first.

    Decided on a coarse net here. What this rung is evidence for -- that the
    instrument returns sane values below the frontier as well as above it --
    does not need all 181 directions to show, and the full decision is the
    exhaustive test below.
    """

    certificate = n11_load(N11_FIRST_RUNG)
    assert certificate.bounded_side == Fraction(189, 50)
    assert (certificate.bounded_side - 2) ** 2 * 5 < 16
    # C4's value, not the whole verdict: a net this coarse fails C3 by
    # construction, since D grows with the gap and B(1 + D) then exceeds 1.
    # What the coarse decision shows is coverage, which is the claim here.
    coarse = Certificate(
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
        atoms=certificate.atoms,
        half_tangents=certificate.half_tangents[::30],
        symmetry=certificate.symmetry,
    )
    verdict = verify(coarse)
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass >= 1


@pytest.mark.exhaustive_exact
def test_the_n11_calibration_rung_verifies_on_the_full_net() -> None:
    """The 373-atom calibration rung over all 181 directions."""
    assert verify(n11_load(N11_FIRST_RUNG)).accepted


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
        "certificate-197-50.json": Fraction(197, 50),
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
    """s(17) >= 459/100 beats the published value, decided from the file.

    22529/5000 = 4.5058 is Massaccesi's published value, adopted here as T-015
    and carried to n = 18 and n = 19 as T-016. This certificate is denser and
    sits at a larger side, so one object moves all three cases. The comparison
    is decided in exact rationals.

    What the certificate claims is checked here; that a verifier accepts it is
    the exhaustive test below, whose current 1184-atom run takes about 25 minutes.
    """
    certificate = n17_load()
    assert certificate.n == 17
    assert certificate.bounded_side == Fraction(459, 100)
    assert certificate.bounded_side > Fraction(22529, 5000)
    assert certificate.total_mass == Fraction(423327, 25000)
    assert certificate.total_mass < 17

    record = n17_declared()
    assert record["claim"] == "s(17) >= 459/100"
    assert record["total_mass"] == str(certificate.total_mass)


@pytest.mark.exhaustive_exact
def test_the_n17_certificate_is_accepted() -> None:
    """The 1184-atom certificate over 181 directions, decided exactly.

    Marked exhaustive: this is about a 25-minute sweep, and the fast test above
    already pins every number the record claims about the same file.
    """
    certificate = n17_load()
    verdict = verify(certificate)
    assert verdict.accepted, verdict.failures
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass >= 1
    assert n17_declared()["least_cell_mass"] == str(verdict.minimum_cell_mass)


def test_the_n17_certificate_does_not_improve_n20() -> None:
    """The scope claim: 459/100 lifts n = 17, 18 and 19, and not n = 20.

    The certificate's own mass carries it upward, so n = 20 does inherit 459/100 --
    but Nagamochi's closed form already gives it 1 + sqrt(13), which is larger.
    Decided in integers: 1 + sqrt(13) > 459/100 iff 13 * 100^2 > (459 - 100)^2.
    """
    assert 13 * 100**2 > (459 - 100) ** 2
    assert n17_load().bounded_side == Fraction(459, 100)


def test_the_grid_refutation_order_is_the_integer_ceiling_of_the_root() -> None:
    """``m`` is decided by integers, never by a float square root."""
    for n in range(1, 200):
        order = grid_refutation_order(n)
        assert order * order >= n
        assert (order - 1) * (order - 1) < n
    assert [grid_refutation_order(n) for n in (11, 12, 16, 17, 25, 26)] == [4, 4, 4, 5, 5, 6]


def test_every_retained_certificate_sits_below_its_own_ceiling() -> None:
    """``L <= ceil(sqrt(n)) B`` is forced by C1 and C4 together.

    A retained certificate above its ceiling would mean one of the two is wrong,
    so this is a check on the record and not only on the arithmetic.
    """
    for certificate in (n11_load(), load(), n17_load()):
        ceiling = ceiling_side(certificate.n, certificate.square_side)
        assert certificate.outer_side <= ceiling, (
            f"n = {certificate.n} claims {certificate.outer_side} above its ceiling {ceiling}"
        )
        assert ceiling < ceiling_side_for_net(certificate.n, certificate.half_tangents)


def test_the_n12_ceiling_is_the_figure_the_record_carries() -> None:
    """3.99082 is ``4 / (1 + D)`` at 181 directions, not a measured quantity."""
    certificate = load()
    assert certificate.n == 12
    over_the_net = ceiling_side_for_net(12, certificate.half_tangents)
    assert float(over_the_net) == pytest.approx(3.990816, abs=5e-7)
    assert ceiling_side(12, certificate.square_side) == Fraction(4) * certificate.square_side
    # No individual certificate on this finite net can attain the grid endpoint.
    assert over_the_net < 4


def test_uniform_net_ceiling_approaches_the_grid_bound() -> None:
    """The per-certificate ceiling does not rule out a separately proved limit family."""
    endpoint = MASSACCESI_LIMIT
    grid_bound = 4
    for tolerance in (Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000)):
        steps = math.floor(grid_bound * endpoint / tolerance) + 1
        net = tuple(endpoint * k / steps for k in range(steps + 1))
        ceiling = ceiling_side_for_net(12, net)
        assert ceiling == grid_bound / (1 + endpoint / steps)
        assert grid_bound - tolerance < ceiling < grid_bound


def test_the_refuting_grid_fits_and_one_of_its_squares_starves() -> None:
    """The construction behind the ceiling, exhibited on the retained atoms.

    Widen the container just past ``4 B`` and lay the sixteen separated
    ``B``-squares the ceiling argument builds. They must all lie inside the
    container and be pairwise disjoint; and since the certificate carries mass
    11.97, well under sixteen, at least one of them must cover less than 1 --
    which is C4 failing, exactly as the argument says it must.
    """
    certificate = load()
    b = certificate.square_side
    order = grid_refutation_order(certificate.n)
    side = order * b + Fraction(1, 1000)
    gap = (side - order * b) / (order + 1)
    pitch = b + gap

    corners = [(gap + i * pitch, gap + j * pitch) for j in range(order) for i in range(order)]
    assert len(corners) == order * order == 16
    # Inside the container, and separated: the far edge of the last square and
    # the gap between consecutive ones are both decided exactly.
    assert corners[-1][0] + b < side and corners[-1][1] + b < side
    assert pitch - b == gap > 0

    covered = [
        sum(
            (
                atom.weight
                for atom in certificate.atoms
                if x <= atom.x <= x + b and y <= atom.y <= y + b
            ),
            start=Fraction(0),
        )
        for x, y in corners
    ]
    assert sum(covered) <= certificate.total_mass
    assert certificate.total_mass < order * order
    assert min(covered) < 1, "C4 would have to hold on all sixteen for the mass to reach n"


def test_one_atom_set_certifies_every_size_above_its_mass() -> None:
    """``n`` lives only in C1, so a certificate is not tied to the ``n`` it declares.

    T-016 historically carried Massaccesi's bound to n = 18 and n = 19 by
    monotonicity. The current T-019 composition is direct: its own mass is under
    both, so the same atoms decide those cases. The operational consequence is the
    one worth pinning -- a run whose covering value lands between 17 and 18
    raises n = 18 and leaves n = 17 where it was.
    """
    certificate = n17_load()
    assert least_size_certified(certificate.total_mass) == 17
    for size in (17, 18, 19):
        assert certificate.total_mass < size
    # C1 is strict, so mass exactly n certifies n + 1 and not n.
    assert least_size_certified(Fraction(17)) == 18
    assert least_size_certified(Fraction(203, 12)) == 17

    # And the two limits agree without being made to. A side above the ceiling
    # forces the mass past n by C4, which is exactly the size this then refuses.
    for n in (11, 12, 17, 20):
        assert grid_refutation_order(n) ** 2 >= n
        assert least_size_certified(Fraction(grid_refutation_order(n) ** 2)) > n
