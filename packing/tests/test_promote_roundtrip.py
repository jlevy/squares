"""The exact route closed at `n = 11`, and what closing it actually required.

`discharge` stops at the side: irreducible over `Q`, with an isolating interval holding
the refined value.  That is a claim about a *number*.  The claim the promotion spec wants
is about a *packing*, and the gap between them is the trap it names -- a wrong contact
structure can produce a packing that is perfectly valid and simply not optimal, which
verification cannot see, because verification catches infeasibility.

What closes the gap is rebuilding the packing inside the recovered field and requiring
the side it reconstructs to be the root the field was built on.

**The angles are the obstacle, and `n = 11` is where they are not.**  A pose unknown
`t_i` is an angle, and an angle is transcendental: it has no representation in `Q(s)`, so
"solve every pose unknown exactly" is unsatisfiable while the pose is parameterised that
way.  Trump's construction is already written over `Q(u)` with `u = tan(a/2)`, so every
coordinate is built from `+ - * /` and the question reduces to recovering `u` from `s`.

**And `u` is derived, not searched.**  `Q(s) = Q(u)`, both degree eight, so `u` is a
rational combination of powers of `s`; writing each `s^i` in the power basis of `Q(u)`
turns that into a square rational linear system with one solution.  An integer-relation
search would have returned the same coefficients and would have had to be believed.
This solves for them, and then still requires the recovered `u` to satisfy `u`'s own
minimal polynomial exactly in the new field -- a check a wrong answer cannot pass.

Measured: the loop closes.  Eleven squares, fourteen touching pairs, valid under
`exact_sign`, and the reconstructed side equal to the field generator exactly rather
than to a tolerance.
"""

from __future__ import annotations

from fractions import Fraction

from cases.trump11.packing import S_MIN_POLY, U_INTERVAL, U_MIN_POLY, build_in
from sqpack.field import NumberField
from sqpack.promote.roundtrip import (
    Certificate,
    RoundTripError,
    certify,
    generator_in_powers_of,
)

#: The isolating interval for the published side, which is about 3.877.
S_INTERVAL = ("387/100", "388/100")


def _u_in_powers_of_s() -> tuple[Fraction, ...]:
    field = NumberField(U_MIN_POLY, U_INTERVAL)
    rational = field.rational
    u = field.alpha
    side = (rational(6) * u + rational(4)) / (rational(1) + rational(2) * u - u * u)
    return generator_in_powers_of(field, side)


def the_generator_is_recovered_by_an_exact_solve() -> None:
    """`u` comes back as an exact rational combination of powers of `s`."""
    coefficients = _u_in_powers_of_s()
    assert len(coefficients) == 8, f"expected eight coefficients, got {len(coefficients)}"
    assert all(isinstance(c, Fraction) for c in coefficients), (
        "the recovered coefficients are not exact rationals, so the recovery was not a "
        "solve over Q"
    )
    # Reproducing it inside Q(u) is the cheap half of the check: the combination must
    # return the element it was solved for.
    field = NumberField(U_MIN_POLY, U_INTERVAL)
    rational = field.rational
    u = field.alpha
    side = (rational(6) * u + rational(4)) / (rational(1) + rational(2) * u - u * u)
    rebuilt = field.zero
    power = field.one
    for coefficient in coefficients:
        rebuilt = rebuilt + field.rational(coefficient) * power
        power = power * side
    assert (rebuilt - u).is_zero(), (
        "the recovered combination of powers of s does not reproduce u in the field it "
        "was solved in"
    )


def a_proper_subfield_is_refused_rather_than_approximated() -> None:
    """An element generating less than the whole field gets a typed refusal."""
    field = NumberField(U_MIN_POLY, U_INTERVAL)
    try:
        # A rational is in every subfield and generates none of them, so its powers
        # cannot span an eight-dimensional space.
        generator_in_powers_of(field, field.rational(3))
    except RoundTripError as error:
        assert error.kind == "subfield-too-small", error.kind
        return
    raise AssertionError(
        "a rational was accepted as a field generator, so the solve returns a nearest "
        "fit where it should refuse"
    )


def the_loop_closes_at_n_eleven() -> Certificate:
    """The whole round trip, from the published polynomial back to a verified packing."""
    certificate = certify(
        side_min_poly=S_MIN_POLY,
        side_interval=S_INTERVAL,
        generator_min_poly=U_MIN_POLY,
        generator_in_side=_u_in_powers_of_s(),
        build=build_in,
    )
    assert certificate.generator_certified, (
        "the recovered generator failed its own minimal polynomial in the rebuilt field"
    )
    assert certificate.packing_valid, (
        f"the packing rebuilt from Q(s) did not verify: {certificate.refusal}"
    )
    assert certificate.side_matches, (
        "the reconstructed side is not the root the field was built on, so the "
        "reconstruction is a different packing"
    )
    assert certificate.degree == 8, f"rebuilt in degree {certificate.degree}, not 8"
    assert certificate.squares_verified == 11, (
        f"verified {certificate.squares_verified} squares, not 11"
    )
    assert certificate.closed, "the round trip reported itself unclosed"
    return certificate


def a_wrong_generator_fails_its_own_minimal_polynomial() -> None:
    """The certification is what makes the recovery a derivation rather than a guess."""
    coefficients = list(_u_in_powers_of_s())
    # Perturb one coefficient. The result is still an element of Q(s); what it is not is
    # a root of u's minimal polynomial, and that is the check that has to notice.
    coefficients[3] = coefficients[3] + Fraction(1, 1000)
    certificate = certify(
        side_min_poly=S_MIN_POLY,
        side_interval=S_INTERVAL,
        generator_min_poly=U_MIN_POLY,
        generator_in_side=coefficients,
        build=build_in,
    )
    assert not certificate.generator_certified, (
        "a perturbed generator was certified against u's minimal polynomial, so the "
        "certification cannot tell the recovered value from a nearby one"
    )
    assert not certificate.closed, "a round trip with an uncertified generator was closed"
    assert certificate.refusal is not None and "minimal polynomial" in certificate.refusal, (
        f"the refusal does not name its cause: {certificate.refusal}"
    )


def a_valid_but_suboptimal_reconstruction_is_caught_by_the_side_alone() -> None:
    """The trap the spec names, and the reason validity is not the whole check.

    Rebuild the real packing but hand back a container one unit larger.  Every square
    still fits and nothing overlaps, so `verify_packing` reports it valid -- and it is
    valid.  It is simply not the packing the field describes, and only the comparison
    against the field generator can say so.
    """

    def build_in_a_larger_container(field, generator):
        squares, side = build_in(field, generator)
        return squares, side + field.rational(1)

    certificate = certify(
        side_min_poly=S_MIN_POLY,
        side_interval=S_INTERVAL,
        generator_min_poly=U_MIN_POLY,
        generator_in_side=_u_in_powers_of_s(),
        build=build_in_a_larger_container,
    )
    assert certificate.packing_valid, (
        "the larger container was reported invalid, so this control is not exercising "
        "the case it was written for -- a packing that verifies and is still wrong"
    )
    assert not certificate.side_matches, (
        "a packing in a container one unit too large was accepted as the reconstruction, "
        "so the side comparison is not catching a valid but suboptimal packing"
    )
    assert not certificate.closed, "a round trip with the wrong side was closed"


def main() -> int:
    the_generator_is_recovered_by_an_exact_solve()
    a_proper_subfield_is_refused_rather_than_approximated()
    certificate = the_loop_closes_at_n_eleven()
    a_wrong_generator_fails_its_own_minimal_polynomial()
    a_valid_but_suboptimal_reconstruction_is_caught_by_the_side_alone()
    print(
        "exact round trip closed at n = 11: "
        f"{certificate.squares_verified} squares, "
        f"{certificate.touching_pairs} touching pairs, side exact"
    )
    return 0


def test_promote_roundtrip() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
