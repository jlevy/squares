"""Synthetic controls and the target determination for the H-265 identification tool."""

from __future__ import annotations

import json
from fractions import Fraction as Q
from pathlib import Path

import pytest
from sympy import Poly, Symbol

from devtools.check_n17_catalogue_polynomial import (
    CATALOGUE,
    CERTIFICATE,
    CHECKER,
    RefusalError,
    Terms,
    chart_poly,
    determine,
    first_irreducible_prime,
    formula_polynomials,
    irreducible_mod_p,
    load_catalogue,
    main,
    parse_catalogue_polynomial,
    root_free,
    side_interval,
    taylor,
)

# b = t and (3t^2 + b - 1)(b - 2t) = 0 meet at t = 0 and at 3t^2 + t - 1 = 0. Under
# S = (6 + 4t)/(1 + 2t - t^2) these map to S = 6 and, by hand, to S^2 - 2S - 12 = 0,
# so the root t* = (sqrt(13) - 1)/6 ~ 0.43426 has side S* = 1 + sqrt(13) ~ 4.60555.
TOY_P2: Terms = {(0, 1): 1, (1, 0): -1}
TOY_P3: Terms = {(3, 0): -6, (2, 1): 3, (1, 1): -2, (0, 2): 1, (1, 0): 2, (0, 1): -1}
TOY_BOX = (Q(434, 1000), Q(435, 1000))
TOY_SIDE = [1, -2, -12]


def test_toy_chart_terms_are_the_stated_product() -> None:
    t, b = Symbol("t"), Symbol("b")
    assert chart_poly(TOY_P3) == Poly((3 * t**2 + b - 1) * (b - 2 * t), t, b, domain="ZZ")


def test_toy_root_is_identified_with_its_hand_derived_side_polynomial() -> None:
    result = determine(TOY_P2, TOY_P3, TOY_BOX, TOY_SIDE)
    assert result["criterion_passed"], result["failures"]
    assert result["vanishing_factor"]["coefficients"] == TOY_SIDE
    assert result["comparison"] == {"equal_up_to_unit": True, "unit": "1"}
    assert [row["degree"] for row in result["side_polynomial"]["factors"]] == [1, 2]
    assert result["side_polynomial"]["factors"][0]["coefficients"] == [1, -6]
    assert result["irreducibility"]["rabin_prime"] == 5
    assert result["second_route"]["catalogue_sign_at_side_interval"] == [-1, 1]
    lo, hi = (Q(value) for value in result["root_enclosure"])
    assert 0 < hi - lo <= Q(1, 10**40)
    assert (lo - 1) ** 2 < 13 < (hi - 1) ** 2


def test_unit_multiple_of_the_side_polynomial_is_accepted() -> None:
    result = determine(TOY_P2, TOY_P3, TOY_BOX, [-3, 6, 36])
    assert result["criterion_passed"], result["failures"]
    assert result["comparison"]["unit"] == "-1/3"


@pytest.mark.parametrize("perturbed", [[1, -2, -11], [1, -2, -13], [1, -6]])
def test_toy_perturbed_catalogue_polynomial_is_refused(perturbed: list[int]) -> None:
    result = determine(TOY_P2, TOY_P3, TOY_BOX, perturbed)
    assert not result["criterion_passed"]
    assert "the vanishing factor differs from the catalogue polynomial" in result["failures"]
    assert any(failure.startswith("second route") for failure in result["failures"])


def test_box_carrying_no_root_is_refused() -> None:
    result = determine(TOY_P2, TOY_P3, (Q(40, 100), Q(41, 100)), TOY_SIDE)
    assert "the side interval does not isolate one root of one factor" in result["failures"]
    assert not result["criterion_passed"]


def test_formula_mismatch_and_degree_mismatch_are_reported() -> None:
    other = chart_poly(TOY_P3), chart_poly(TOY_P2)
    result = determine(TOY_P2, TOY_P3, TOY_BOX, TOY_SIDE, recorded_degree=3, formulas=other)
    assert "certificate polynomials differ from the H-255 formulas" in result["failures"]
    assert "the recorded algebraic degree differs from the polynomial's" in result["failures"]


def test_side_interval_is_outward_and_refuses_unproved_monotonicity() -> None:
    lo, hi = side_interval(*TOY_BOX, digits=6)
    exact = [(6 + 4 * t) / (1 + 2 * t - t * t) for t in TOY_BOX]
    assert lo <= exact[1] < exact[0] <= hi
    assert hi - lo < Q(1, 1000)
    with pytest.raises(RefusalError, match="decreasing"):
        side_interval(Q(6, 10), Q(7, 10))
    with pytest.raises(RefusalError, match="positive width"):
        side_interval(Q(1, 2), Q(1, 2))


def test_taylor_shift_and_root_exclusion() -> None:
    square_two = [Q(1), Q(0), Q(-2)]
    assert taylor(square_two, Q(1)) == [Q(-1), Q(2), Q(1)]
    assert root_free(square_two, Q(3, 2), Q(2))
    assert not root_free(square_two, Q(14, 10), Q(15, 10))


def test_rabin_test_on_known_cases() -> None:
    assert irreducible_mod_p([1, 0, 1], 3)
    assert not irreducible_mod_p([1, 0, 1], 5)
    # Two distinct irreducible cubics mod 2: x^(2^6) = x holds, the gcd condition fails.
    cubics = Poly([1, 0, 1, 1], Symbol("x")) * Poly([1, 1, 0, 1], Symbol("x"))
    assert not irreducible_mod_p([int(c) for c in cubics.all_coeffs()], 2)
    # x^4 + 1 is irreducible over Q but reducible modulo every prime.
    assert first_irreducible_prime([1, 0, 0, 0, 1], limit=200)[0] is None
    with pytest.raises(RefusalError):
        irreducible_mod_p([5, 1, 1], 5)


def test_rabin_agrees_with_modular_factorization_on_the_catalogue() -> None:
    coefficients, _ = load_catalogue(CATALOGUE)
    for p in (3, 7, 11, 13, 103, 167):
        expected = Poly(coefficients, Symbol("s"), modulus=p).is_irreducible
        assert irreducible_mod_p(coefficients, p) is expected


@pytest.mark.parametrize(
    "text",
    [
        "s^2-2s-12",
        "s^22s-12=0",
        "s^2+s^2-1=0",
        "x^2-1=0",
        "5=0",
        "s^2-0s-1=0",
        "s^2-2s-12=0=0",
    ],
)
def test_malformed_catalogue_polynomials_are_refused(text: str) -> None:
    with pytest.raises(RefusalError):
        parse_catalogue_polynomial(text)


def test_catalogue_parser_reads_braced_bare_and_implicit_terms() -> None:
    assert parse_catalogue_polynomial("4s^{3} - s^2 + s - 7 = 0") == [4, -1, 1, -7]
    assert parse_catalogue_polynomial("s^4-1=0") == [1, 0, 0, 0, -1]


def test_recorded_catalogue_polynomial_and_formulas_match_the_certificate() -> None:
    coefficients, degree = load_catalogue(CATALOGUE)
    assert degree == 18
    assert len(coefficients) == 19
    assert (coefficients[0], coefficients[-1]) == (4775, -2631254953)
    certificate = json.loads(CERTIFICATE.read_bytes())
    terms = [{(i, j): int(c) for i, j, c in rows} for rows in certificate["polynomials"]]
    assert (chart_poly(terms[0]), chart_poly(terms[1])) == formula_polynomials()


def test_target_identifies_the_catalogue_polynomial(tmp_path: Path) -> None:
    output = tmp_path / "receipt.json"
    assert main(["--output", str(output)]) == 0
    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["verdict"] == "identical up to a rational unit and irreducible over Q"
    assert receipt["resultant_t"]["degree"] == receipt["side_polynomial"]["degree"] == 28
    rows = receipt["side_polynomial"]["factors"]
    assert [(row["degree"], row["multiplicity"]) for row in rows] == [
        (1, 2),
        (1, 2),
        (1, 2),
        (2, 2),
        (18, 1),
    ]
    assert [len(row["roots_in_interval"]) for row in rows] == [0, 0, 0, 0, 1]
    coefficients, _ = load_catalogue(CATALOGUE)
    assert receipt["vanishing_factor"]["coefficients"] == coefficients
    assert receipt["comparison"]["unit"] == "1"
    assert receipt["irreducibility"]["rabin_prime"] == 7
    assert receipt["second_route"]["degree"] == 60
    assert receipt["second_route"]["cofactor_root_free_on_side_interval"]
    assert set(receipt["inputs"]) == {"certificate", "checker", "catalogue", "module"}


def test_target_refuses_a_perturbed_catalogue_polynomial(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = CATALOGUE.read_text(encoding="utf-8")
    assert text.count("-2631254953=0") == 1
    perturbed = tmp_path / "n-017.md"
    perturbed.write_text(text.replace("-2631254953=0", "-2631254954=0"), encoding="utf-8")
    assert main(["--catalogue", str(perturbed)]) == 1
    receipt = json.loads(capsys.readouterr().out)
    assert "the vanishing factor differs from the catalogue polynomial" in receipt["failures"]
    assert receipt["verdict"] == "not confirmed"


def test_unchecked_or_mismatched_certificate_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    certificate = json.loads(CERTIFICATE.read_bytes())
    certificate["criterion_passed"] = False
    failing = tmp_path / "certificate.json"
    failing.write_text(json.dumps(certificate), encoding="utf-8")
    assert main(["--certificate", str(failing)]) == 2
    assert "did not pass" in json.loads(capsys.readouterr().out)["refused"]

    checker = json.loads(CHECKER.read_bytes())
    checker["q"] = "0"
    mismatched = tmp_path / "checker.json"
    mismatched.write_text(json.dumps(checker), encoding="utf-8")
    assert main(["--checker", str(mismatched)]) == 2
    assert "does not match" in json.loads(capsys.readouterr().out)["refused"]
