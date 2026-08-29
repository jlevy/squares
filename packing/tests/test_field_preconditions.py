#!/usr/bin/env python3
"""Behavior checks for exact number-field preconditions."""

from __future__ import annotations

from sqpack.field import FieldPreconditionError, NumberField


def require_rejection(
    polynomial: tuple[int, ...], interval: tuple[int, int], phrase: str
) -> None:
    """Require a malformed field declaration to fail with a useful reason."""
    try:
        NumberField(polynomial, interval)
    except FieldPreconditionError as error:
        assert phrase in str(error), error
    else:
        raise AssertionError(f"accepted malformed field {polynomial} on {interval}")


def main() -> int:
    sqrt2 = NumberField((1, 0, -2), (1, 2))
    certificate = sqrt2.precondition_certificate()
    assert certificate["irreducible_over_q"] is True
    assert certificate["root_count_in_open_interval"] == 1
    assert certificate["irreducibility_method"] == "irreducible-reduction-mod-prime"
    assert isinstance(certificate["irreducibility_prime"], int)

    # Biquadratic quartics can be irreducible over Q without having an irreducible
    # reduction modulo any prime.  The complete quartic fallback covers the two
    # composita used by the Stromquist exact replay.
    for polynomial, interval in (
        ((1, 0, -14, 0, 9), (3, 4)),
        ((1, 0, -1668, 0, 678976), (31, 32)),
    ):
        compositum = NumberField(polynomial, interval)
        compositum_certificate = compositum.precondition_certificate()
        assert (
            compositum_certificate["irreducibility_method"]
            == "monic-integer-quartic-factor-exclusion"
        )
        assert compositum_certificate["irreducibility_prime"] is None

    # Degree one is the rational field case and needs no modular witness.
    rational = NumberField((1, -1), (0, 2))
    assert rational.precondition_certificate()["irreducibility_method"] == "degree-one"
    assert rational.alpha == rational.rational(1)

    # A sign change alone used to accept both of these unsound declarations.
    require_rejection((1, 0, -1), (0, 2), "irreducibility")
    require_rejection((1, 0, -5, 0, 6), (1, 2), "reducible over Q")
    require_rejection((1, 0, -2), (-2, 2), "exactly one real root")

    # Endpoint roots make the open isolating interval ambiguous for refinement.
    require_rejection((1, -1), (1, 2), "endpoint")

    print("number-field precondition contract selftest passed")
    return 0


def test_number_field_preconditions() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
