"""What the Kingbird SVG reader takes from a picture, and what its checks refuse.

The two catalogue pictures this repository retains verbatim, `square-11.svg` and
`square-29.svg` (`resources/papers/`), are the realistic inputs: one carries its side as
a `Root` object and the other a `FindRoot` system. Nothing here reaches the network.
"""

from __future__ import annotations

import hashlib
import json
import random
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import extract_kingbird_svg_exact as tool
from devtools.backfill_algebraic_facts import backfilled
from devtools.derive_kingbird_facts import DerivationRefusedError
from devtools.extract_kingbird_svg_exact import (
    ExtractionError,
    IsolatedRoot,
    RecordRefusedError,
    Reference,
    agreement,
    check_polynomial,
    degree_pattern,
    irreducibility_certificate,
    read_pure_function,
    read_svg,
    record_with_polynomial,
)
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
SVG_11 = ROOT / "resources/papers/kingbird-square-11-provenance.svg"
SVG_29 = ROOT / "resources/papers/kingbird-square-29-provenance.svg"
SIDE_11 = "3.87708359002281417730789706010096"
#: As `frontier/n-011.md` records it, from the catalogue.
POLYNOMIAL_11 = "s^8 - 20s^7 + 178s^6 - 842s^5 + 1923s^4 - 496s^3 - 6754s^2 + 12420s - 6865 = 0"
COEFFICIENTS_11 = (1, -20, 178, -842, 1923, -496, -6754, 12420, -6865)


def _upper(text: str) -> dict[str, object]:
    return safe_load(text.split("---", 2)[1])["packing"]["reported_upper_bound"]


# --------------------------------------------------------------------------- reading


def test_reads_the_side_root_of_the_retained_n11_picture() -> None:
    content = read_svg(SVG_11.read_text(encoding="utf-8"))
    (side,) = content.side_roots()
    assert side.index == 2
    assert side.coefficients == COEFFICIENTS_11
    assert side.polynomial == POLYNOMIAL_11
    assert (
        side.polynomial
        == _upper((ROOT / "frontier/n-011.md").read_text())["minimal_polynomial"]
    )


def test_records_why_a_radical_coefficient_root_is_not_read() -> None:
    content = read_svg(SVG_11.read_text(encoding="utf-8"))
    (rule,) = [root for root in content.roots if root.assigned_to == "z"]
    assert rule.coefficients is None
    assert rule.problem is not None
    assert "Sqrt" in rule.problem


def test_reads_the_n11_attribution_entities_and_solves() -> None:
    content = read_svg(SVG_11.read_text(encoding="utf-8"))
    assert content.credits[0].startswith("First found by Walter Trump")
    assert content.entity("s") == SIDE_11
    (x0,) = [entity for entity in content.entities if entity.name == "x0"]
    assert x0.notes[0] == "1+2*Sec[a]-(s-2)*Tan[a]"
    solves = [call for call in content.solver_calls if call.solver == "Solve"]
    assert [call.unknowns for call in solves] == [("s", "a"), ("s", "a"), ("s",)]
    assert [len(call.equations) for call in solves] == [2, 2, 1]


def test_reads_the_n29_findroot_system() -> None:
    content = read_svg(SVG_29.read_text(encoding="utf-8"))
    (system,) = [call for call in content.solver_calls if call.solver == "FindRoot"]
    assert system.equations == tuple(f"f{k}==0" for k in range(1, 7))
    assert system.unknowns == ("s", "a", "b", "c", "d", "i")
    assert system.working_precision == 200
    assert not content.roots
    side = content.entity("s")
    assert side is not None
    assert len(side) == 101
    assert any(
        statement.startswith("f6 = RotationTransform[c]") for statement in content.statements
    )


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("-6865 + 12420*# - 6754*#^2 + #^3", (1, -6754, 12420, -6865)),
        ("#1^2 - 2", (1, 0, -2)),
        ("3 #^2 + 72 # - 1 &", (3, 72, -1)),
        ("5*#^4 - 12*#\\\n   + 7", (5, 0, 0, -12, 7)),
        ("-#^3 + #^3 + 2*#", (2, 0)),
    ],
)
def test_reads_integer_pure_functions(body: str, expected: tuple[int, ...]) -> None:
    assert read_pure_function(body.removesuffix("&")) == expected


@pytest.mark.parametrize(
    "body",
    ["3/2*#^2 - 1", "2*Sqrt[2]*# - 1", "#^2 3", "", "7", "#^2 + (# - 1)^2", "2*#^2 -"],
)
def test_refuses_what_is_not_an_integer_polynomial(body: str) -> None:
    with pytest.raises(ExtractionError):
        read_pure_function(body)


def test_elides_a_long_root_body_from_the_statements() -> None:
    terms = " + ".join(f"{10**30 + k}*#^{k}" for k in range(1, 12))
    svg = f"<!--\n    Credit line.\n\n    s = Root[{terms} - 1, 3]\n-->\n<svg/>"
    content = read_svg(svg)
    (statement,) = content.statements
    assert statement == "s = Root[<degree-11 polynomial, in roots>, 3]"
    assert content.side_roots()[0].degree == 11


# --------------------------------------------------------------------------- modulo p


def test_degree_patterns_agree_with_sympy() -> None:
    sp = pytest.importorskip("sympy")
    from sympy.polys.galoistools import gf_ddf_zassenhaus  # noqa: PLC0415

    generator = random.Random(83)
    compared = 0
    for degree in (2, 5, 9, 16, 23):
        for prime in (100_003, 100_019, 100_043):
            coefficients = [1] + [generator.randrange(-(10**40), 10**40) for _ in range(degree)]
            pattern = degree_pattern(coefficients, prime)
            if pattern is None:
                continue
            reduced = [c % prime for c in coefficients]
            factors = gf_ddf_zassenhaus(reduced, prime, sp.ZZ)
            expected = sorted(
                step for factor, step in factors for _ in range((len(factor) - 1) // step)
            )
            assert list(pattern) == expected
            compared += 1
    assert compared >= 12


def test_a_bad_prime_gives_no_pattern() -> None:
    assert degree_pattern((100_003, 1, 1), 100_003) is None
    assert degree_pattern((1, -2, 1), 100_003) is None


def test_certifies_the_n11_polynomial_irreducible() -> None:
    certificate = irreducibility_certificate(COEFFICIENTS_11)
    assert certificate.irreducible
    assert certificate.patterns


def test_never_certifies_a_product() -> None:
    first = (1, 0, 0, -2)
    second = (1, 0, 0, 0, -1, -1)
    product = [0] * 9
    for i, a in enumerate(first):
        for j, b in enumerate(second):
            product[i + j] += a * b
    certificate = irreducibility_certificate(product, max_primes=10)
    assert not certificate.irreducible
    assert {3, 5} <= set(certificate.open_degrees)


# --------------------------------------------------------------------------- the root


def test_isolates_the_n11_side_and_counts_its_index() -> None:
    check = check_polynomial(
        COEFFICIENTS_11,
        [Reference("entity", SIDE_11), Reference("printed", "3.87708359002281")],
        index=2,
    )
    assert check.verified
    assert check.root is not None
    assert check.root.radius_exponent >= 37
    assert check.index_counted == 2
    assert check.agreements[0].decimals_agreeing >= 32
    assert all(item.truncation_of_root for item in check.agreements)


def test_a_reference_off_in_its_last_places_is_refused() -> None:
    check = check_polynomial(
        COEFFICIENTS_11,
        [Reference("entity", SIDE_11), Reference("off", "3.877083590022814175")],
    )
    assert not check.verified
    assert not check.agreements[1].within_last_place


def test_a_wrong_root_index_is_refused() -> None:
    check = check_polynomial(COEFFICIENTS_11, [Reference("entity", SIDE_11)], index=1)
    assert check.index_counted == 2
    assert not check.verified


def test_a_reference_near_no_root_is_refused() -> None:
    check = check_polynomial((1, 0, -2), [Reference("far", "40.5")])
    assert not check.verified
    assert check.root is None or not check.agreements[0].within_last_place


def test_a_reference_at_a_double_root_isolates_nothing() -> None:
    check = check_polynomial((1, -2, 1), [Reference("double", "1.0")])
    assert check.root is None
    assert check.root_problem is not None
    assert not check.verified


def test_the_reported_interval_still_isolates_the_root() -> None:
    reference = (
        "1.4142135623730950488016887242096980785696718753769480731766797379907324784621"
        "0703885038753432764157273501"
    )
    check = check_polynomial((1, 0, -2), [Reference("sqrt2", reference)])
    assert check.verified
    saved = check.summary()["isolated_root"]
    assert isinstance(saved, dict)
    centre = Fraction(str(saved["centre"]))
    radius = Fraction(str(saved["radius"]))
    below = (centre - radius) ** 2 - 2
    above = (centre + radius) ** 2 - 2
    assert below * above < 0


def test_isolates_a_linear_root() -> None:
    check = check_polynomial((7, -53), [Reference("rational", "7.57142857142857")])
    assert check.verified
    assert check.root is not None
    assert check.root.truncation(14) == "7.57142857142857"


def test_isolates_an_integer_linear_root() -> None:
    check = check_polynomial((1, -7), [Reference("integer", "7.0")])
    assert check.verified
    assert check.root is not None
    assert abs(check.root.centre - 7) <= check.root.radius


def test_reported_difference_bound_rounds_outward() -> None:
    root = IsolatedRoot(112349, 5, 6)
    item = agreement(root, "test", "1.00")
    exact = abs(root.centre - 1) + root.radius
    assert Fraction(item.difference_bound) >= exact


# --------------------------------------------------------------------------- the record


def _record_83(degree: int, side: str = SIDE_11) -> str:
    text = (ROOT / "frontier/n-083.md").read_text(encoding="utf-8")
    assert "    algebraic_degree: 672\n" in text
    assert "    value: '9.63475764863108'\n" in text
    polynomial_start = text.index("    minimal_polynomial: ")
    polynomial_end = text.index("    algebraic_source: ", polynomial_start)
    assert polynomial_end > polynomial_start
    text = text[:polynomial_start] + "    minimal_polynomial: null\n" + text[polynomial_end:]
    return text.replace(
        "    algebraic_degree: 672\n", f"    algebraic_degree: {degree}\n"
    ).replace("    value: '9.63475764863108'\n", f"    value: '{side}'\n")


def test_writes_a_verified_polynomial_as_the_backfill_would() -> None:
    check = check_polynomial(COEFFICIENTS_11, [Reference("entity", SIDE_11)], index=2)
    written = record_with_polynomial(_record_83(8), 83, check)
    upper = _upper(written)
    assert upper["minimal_polynomial"] == POLYNOMIAL_11
    assert upper["algebraic_degree"] == 8
    assert upper["algebraic_source"] == "catalogue"
    assert backfilled(written, 83) == written


def test_refuses_a_record_whose_degree_differs() -> None:
    check = check_polynomial(COEFFICIENTS_11, [Reference("entity", SIDE_11)], index=2)
    with pytest.raises(RecordRefusedError, match="degree 672"):
        record_with_polynomial(_record_83(672), 83, check)


def test_refuses_a_record_whose_side_differs() -> None:
    check = check_polynomial(COEFFICIENTS_11, [Reference("entity", SIDE_11)], index=2)
    with pytest.raises(RecordRefusedError, match="does not agree"):
        record_with_polynomial(_record_83(8, "9.63475764863108"), 83, check)


def test_refuses_an_unverified_polynomial_or_a_filled_record() -> None:
    unverified = check_polynomial(COEFFICIENTS_11, [Reference("off", "3.8770835900228143")])
    with pytest.raises(RecordRefusedError, match="did not verify"):
        record_with_polynomial(_record_83(8), 83, unverified)
    verified = check_polynomial(COEFFICIENTS_11, [Reference("entity", SIDE_11)], index=2)
    filled = (ROOT / "frontier/n-011.md").read_text(encoding="utf-8")
    with pytest.raises(RecordRefusedError):
        record_with_polynomial(filled, 11, verified)


# --------------------------------------------------------------------------- the command


def test_svg_command_keeps_facts_and_never_the_picture(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    data = SVG_11.read_bytes()
    monkeypatch.setattr(
        tool, "fetch_picture", lambda _url: (data, "Tue, 01 Sep 2026 00:00:00 GMT")
    )
    out = tmp_path / "facts.json"
    assert tool.main(["svg", "11", "--out", str(out)]) == 0
    assert [path.name for path in tmp_path.iterdir()] == ["facts.json"]
    facts = json.loads(out.read_text(encoding="utf-8"))
    assert facts["same_as_reading_of_2026_10_05"] is True
    assert facts["read_from"] == "fetched into memory"
    assert facts["checks"][0]["verified"] is True
    (side,) = [root for root in facts["roots"] if root["assigned_to"] == "s"]
    assert side["coefficients"] == list(COEFFICIENTS_11)
    assert side["polynomial"] == POLYNOMIAL_11


def test_svg_command_reports_a_refused_fetch(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def refuse(url: str) -> tuple[bytes, str | None]:
        raise DerivationRefusedError("fetch-failed", f"{url}: Tunnel connection failed: 403")

    monkeypatch.setattr(tool, "fetch_picture", refuse)
    assert tool.main(["svg", "83"]) == 2
    assert "403" in capsys.readouterr().out


@pytest.mark.parametrize("pin", ["missing", "mismatched", "matched"])
def test_svg_record_write_requires_the_retained_source_pin(
    pin: str, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    destination = tmp_path / "packing/frontier"
    destination.mkdir(parents=True)
    original = (ROOT / "frontier/n-011.md").read_text()
    start = original.index("    minimal_polynomial:")
    end = original.index("    algebraic_source:", start)
    unfilled = original[:start] + "    minimal_polynomial: null\n" + original[end:]
    record = destination / "n-011.md"
    record.write_text(unfilled)
    data = SVG_11.read_bytes()
    receipt = (
        None
        if pin == "missing"
        else {"sha256": hashlib.sha256(data if pin == "matched" else data + b"\n").hexdigest()}
    )
    monkeypatch.setattr(tool, "pinned_reading", lambda _n: receipt)
    monkeypatch.setattr(tool, "FRONTIER", destination)
    monkeypatch.setattr(tool, "ROOT", destination.parent)
    result = tool.main(["svg", "11", "--svg", str(SVG_11), "--write-record"])
    if pin == "matched":
        assert result == 0
        assert _upper(record.read_text())["minimal_polynomial"] == POLYNOMIAL_11
    else:
        assert result != 0
        assert record.read_text() == unfilled
        assert tool.main(["svg", "11", "--svg", str(SVG_11)]) == 0
