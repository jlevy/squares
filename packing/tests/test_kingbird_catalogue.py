"""The retained Kingbird catalogue reparses, and the frontier still agrees with it.

These tests exist because `exact_form`, `algebraic_degree` and `minimal_polynomial` are
hand-transcribed and, until `sqpack.kingbird_catalogue`, nothing re-read them. The two
shapes that hid a real miss are pinned by name: the multi-line `\\begin{aligned}` block
at `n = 54` (`think-k5z2`), and the degree lock, which prints no closed form at all and
must not be confused with a source that is silent.
"""

from __future__ import annotations

import re
from decimal import Decimal
from functools import cache
from pathlib import Path

import pytest

from devtools.check_source_coverage import (
    COVERAGE,
    FRONTIER,
    catalogue_transcription_errors,
    parse_case,
    source_by_id,
)
from sqpack.kingbird_catalogue import (
    CatalogueEntry,
    CatalogueParseError,
    agrees_with_printed_decimal,
    catalogue_completeness_bound,
    completeness_bound_from_text,
    cross_check_html,
    default_catalogue_html_path,
    default_catalogue_path,
    evaluate_exact_form,
    exact_form_matches_decimal,
    index_entries,
    normalized_polynomial,
    parse_catalogue,
    parse_entries,
)
from sqpack.known_best import KNOWN_BEST_CORPUS
from sqpack.yamlio import safe_load

#: The case corpus this repository keeps a frontier record for.
#: The hand-authored hundred. Facts about the catalogue relative to that boundary (how
#: many entries lie beyond it, where the stale n=179 form sits) are facts about the page
#: and do not move when the case corpus grows; the reconciliation below follows the corpus.
CASE_MAXIMUM = 100
#: What the reconciliation reached at each corpus: (cases matched to a pictured block,
#: printed facts checked). Pinned so a parser that quietly stopped matching still fails.
GOLDEN_RECONCILED: dict[str, tuple[int, int]] = {
    "n=1..100": (60, 206),
    "n=1..200": (114, 409),
    "n=1..324": (183, 648),
}

#: A block whose printed form uses LaTeX this parser does not read. It must raise rather
#: than record "no closed form", which is exactly how the `n = 54` miss looked.
UNCONVERTIBLE_BLOCK = r"""preamble

54
[](square-54.svg)

$s = 7-{1\over 2}\widehat 2 = \Nn{7.84666719284348}$
Found by David W. Cantrell in October 2005.
"""

#: A heading and a picture with no side line beneath them.
BLOCK_WITHOUT_A_SIDE = """11
[](square-11.svg)

Found by Walter Trump in 1979.
"""

#: Two blocks claiming the same count, which no reading of the page can resolve.
TWO_BLOCKS_FOR_ONE_COUNT = """7, 8
[](square-8.svg)

$s = 3$

8
[](square-8b.svg)

$s = 3$
"""


@cache
def _catalogue_text() -> str:
    return default_catalogue_path().read_text(encoding="utf-8")


@cache
def _entries() -> tuple[CatalogueEntry, ...]:
    return parse_entries(_catalogue_text())


@cache
def _by_n() -> dict[int, CatalogueEntry]:
    return index_entries(_entries())


def test_every_pictured_block_parses_with_a_side_and_a_picture() -> None:
    entries = _entries()

    assert len(entries) == 174
    assert all(entry.catalogue_pictured for entry in entries)
    assert all(entry.svg_path is not None for entry in entries)
    assert all(entry.side_decimal for entry in entries)
    assert all(entry.n == max(entry.listed_n) for entry in entries)
    assert all(entry.n in entry.listed_n for entry in entries)


def test_aligned_block_at_n54_yields_its_closed_form() -> None:
    """The one shape the first transcription pass missed, in the spelling the record uses."""
    entry = _by_n()[54]

    assert entry.exact_form == "7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))"
    assert entry.side_decimal == "7.84666719284348"
    assert entry.algebraic_degree is None
    assert entry.minimal_polynomial is None
    assert agrees_with_printed_decimal(
        evaluate_exact_form(entry.exact_form), entry.side_decimal
    )


def test_degree_lock_at_n11_states_a_degree_and_no_closed_form() -> None:
    entry = _by_n()[11]

    assert entry.algebraic_degree == 8
    assert entry.exact_form is None
    assert entry.catalogue_rigid == "rigid"
    assert normalized_polynomial(entry.minimal_polynomial or "") == (
        1, -20, 178, -842, 1923, -496, -6754, 12420, -6865,
    )  # fmt: skip


def test_minimal_polynomial_at_n51_is_the_degree_twelve_root() -> None:
    entry = _by_n()[51]

    assert entry.algebraic_degree == 12
    assert entry.minimal_polynomial is not None
    coefficients = normalized_polynomial(entry.minimal_polynomial)
    assert len(coefficients) - 1 == 12
    assert coefficients[:4] == (1, -52, 1168, -14808)
    assert coefficients[-1] == -1119939


def test_exact_grid_entry_yields_an_integer() -> None:
    """A trivial packing prints its side as a bare integer, with no `\\Nn` decimal."""
    entry = _by_n()[9]

    assert entry.exact_form == "3"
    assert entry.side_decimal == "3"
    assert evaluate_exact_form(entry.exact_form) == Decimal(3)


def test_one_picture_serves_both_counts_it_lists() -> None:
    """A picture of eight squares settles seven by removing any one of them."""
    catalogue = _by_n()

    assert catalogue[7] is catalogue[8]
    assert catalogue[7].listed_n == (7, 8)
    assert catalogue[7].svg_path == "square-8.svg"
    assert catalogue[2] is catalogue[3]
    assert catalogue[2].listed_n == (2, 3)


def test_completeness_bound_is_read_from_the_page() -> None:
    assert catalogue_completeness_bound() == 324


def test_a_page_without_its_completeness_sentence_is_refused() -> None:
    """Losing the sentence must fail loudly; every reading of source silence rests on it."""
    without = _catalogue_text().replace("For the $n ≤ 324$ not pictured", "For some n")

    with pytest.raises(CatalogueParseError, match="no longer states the bound"):
        completeness_bound_from_text(without)


def test_entries_beyond_the_case_corpus_parse() -> None:
    catalogue = _by_n()
    beyond = [entry for entry in _entries() if entry.n > CASE_MAXIMUM]

    assert len(beyond) == 119
    assert catalogue[101].exact_form == "7 + (5/2)sqrt(2)"
    assert catalogue[107].exact_form == "10 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))"
    assert catalogue[307].side_decimal == "17.98281564631754"
    assert catalogue[307].found_by == (
        "M.Z. Arslanov",
        "S.A. Mustafin",
        "Z.K. Shangitbayev",
    )
    assert catalogue[2043].algebraic_degree == 12


def test_quadratic_field_polynomial_normalises_to_its_rational_norm() -> None:
    """The catalogue prints `n = 37`'s root over `Q(sqrt 2)`; the frontier records its norm."""
    entry = _by_n()[37]

    assert entry.algebraic_degree == 8
    assert entry.minimal_polynomial is not None
    assert "sqrt(2)" in entry.minimal_polynomial
    assert normalized_polynomial(entry.minimal_polynomial) == (
        36, -2496, 59768, -733760, 5289248, -23462672, 63458276, -96673872, 64068561,
    )  # fmt: skip


def test_every_printed_closed_form_matches_its_printed_decimal_except_n179() -> None:
    """The catalogue prints one stale closed form, and the parser must not hide it.

    `n = 179` pairs a January-2025 closed form with a January-2026 decimal it does not
    equal, and says "Not yet analytically optimized" underneath. That is a fact about the
    source, so it is reported rather than raised -- but it is also why nothing downstream
    may read `exact_form` without checking it against `side_decimal`.
    """
    stale = [entry.n for entry in _entries() if not exact_form_matches_decimal(entry)]

    assert stale == [179]
    assert all(n > CASE_MAXIMUM for n in stale)


def test_every_pictured_entry_carries_its_credit_line_verbatim() -> None:
    """The annotation under the picture, as the page writes it, markup and all.

    `construction_method` and `analytically_optimized` are stated nowhere else on the
    page, so a caller that wants them has to read these lines. Kept verbatim because the
    only thing separating the two Göbel families is the page an "Explore group" link
    points at -- its text is identical for both -- so unwrapping the Markdown link would
    throw the distinction away.
    """
    entries = _entries()
    assert all(entry.credit_line for entry in entries)

    assert _by_n()[11].credit_line == (
        "[Rigid.](squares_in_squares__rigid.html)\nFound by Walter Trump\nin 1979."
    )
    assert _by_n()[10].credit_line == (
        "Found by Frits Göbel in early 1979.\n"
        "Proved by Walter Stromquist in 2003.\n"
        "[Explore group](squares_in_squares__Göbel_strips.html)"
    )
    assert _by_n()[179].credit_line == (
        "Found by David Ellsworth in January 2025, using a computer program he wrote.\n"
        "Improved by David Ellsworth in January 2026, using his modified version of "
        "Thomas Schadt's simulated annealing program.\n"
        "Not yet analytically optimized."
    )
    # Every line of the block below the side value, and nothing above it.
    assert all("\\Nn{" not in (entry.credit_line or "") for entry in entries)
    assert not any((entry.credit_line or "").startswith("\n") for entry in entries)


def test_the_credit_line_is_where_the_page_states_analytic_optimization() -> None:
    """The disclaimer exists, it is exact, and it appears only above the case corpus."""
    stated = [
        entry.n
        for entry in _entries()
        if "Not yet analytically optimized." in (entry.credit_line or "")
    ]

    assert len(stated) == 32
    assert all(n > CASE_MAXIMUM for n in stated)
    assert 179 in stated


def test_the_six_credit_openers_the_page_writes_are_all_read() -> None:
    """Three of them were unread, which left eight entries the page credits uncredited."""
    catalogue = _by_n()
    for n in (123, 129, 177, 206, 266):  # "Found and improved by"
        assert catalogue[n].found_by == ("David Ellsworth",), n
    assert catalogue[230].found_by == ("David Ellsworth",)  # "Found and improved by"
    assert catalogue[154].found_by == ("David Ellsworth",)  # "Originally found by"
    assert catalogue[301].found_by == ("David Ellsworth",)  # "Drafted by"
    assert catalogue[230].found_year == 2025
    assert catalogue[301].found_year == 2025


def test_a_credit_is_read_from_one_sentence_and_not_across_two() -> None:
    """`n = 272` opens "Originally found by Lars Cleemann between 1991 and 1998".

    The sentence names no year in the form this parser reads, and the next four-digit
    year on the page belongs to a different packing two sentences later. A credit is a
    sentence, so an opener whose own sentence dates nothing yields nothing.
    """
    entry = _by_n()[272]

    assert "Originally found by Lars Cleemann" in (entry.credit_line or "")
    assert entry.found_by == ()
    assert entry.found_year is None


def test_a_block_with_no_annotation_has_no_credit_line() -> None:
    """`None` says the page printed nothing, which is not the same as an empty string."""
    (entry,) = parse_entries("9\n[](square-9.svg)\n\n$s = 3$\n")

    assert entry.credit_line is None
    assert entry.found_by == ()


def test_transcription_agrees_with_the_retained_html() -> None:
    """`html2text` must not have dropped, added, or reordered a box."""
    html = default_catalogue_html_path().read_text(encoding="utf-8")

    assert cross_check_html(_entries(), html) == []


def test_an_unconvertible_side_expression_names_its_line() -> None:
    """A form this parser cannot read is loud, never a silent `exact_form: null`."""
    with pytest.raises(CatalogueParseError, match="line 6: unconverted LaTeX") as failure:
        parse_entries(UNCONVERTIBLE_BLOCK)

    assert failure.value.line == 6


def test_a_block_without_a_side_value_names_its_line() -> None:
    with pytest.raises(CatalogueParseError, match=r"line 1: .*prints no side value"):
        parse_entries(BLOCK_WITHOUT_A_SIDE)


def test_a_count_listed_by_two_blocks_is_refused() -> None:
    with pytest.raises(CatalogueParseError, match="n=8 is listed by two blocks"):
        index_entries(parse_entries(TWO_BLOCKS_FOR_ONE_COUNT))


def test_parse_catalogue_reads_the_retained_file_by_default(tmp_path: Path) -> None:
    assert parse_catalogue()[54].source_line == _by_n()[54].source_line

    copied = tmp_path / "catalogue.md"
    copied.write_text(_catalogue_text(), encoding="utf-8")
    assert parse_catalogue(copied)[54].exact_form == _by_n()[54].exact_form


def _frontier_cases() -> dict[int, dict]:
    return {
        case["n"]: case
        for case in (parse_case(path) for path in sorted(FRONTIER.glob("n-[0-9][0-9][0-9].md")))
    }


def _kingbird_source_key() -> str:
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    return str(source_by_id(coverage, "kingbird-current")["source_key"])


def test_frontier_transcription_diverges_nowhere_below_the_case_maximum() -> None:
    """The gate `think-l0vj` exists to hold: zero divergences at n = 1..100."""
    cases = _frontier_cases()
    assert sorted(cases) == list(KNOWN_BEST_CORPUS.numbers)

    errors, compared, facts = catalogue_transcription_errors(
        cases,
        _by_n(),
        _kingbird_source_key(),
        completeness_bound_from_text(_catalogue_text()),
    )

    assert errors == []
    # A parser that quietly stopped matching would agree with every record, so the
    # reconciliation's own reach is asserted alongside its verdict.
    assert (compared, facts) == GOLDEN_RECONCILED[KNOWN_BEST_CORPUS.label]


@pytest.mark.parametrize(
    ("n", "field", "replacement", "expected"),
    [
        (54, "exact_form", None, "n=54: exact_form: record has null"),
        (54, "exact_form", "7 + (1/2)sqrt(2)", "not the decimal 7.84666719284348"),
        (11, "algebraic_degree", None, "n=11: algebraic_degree: record has null"),
        (11, "catalogue_rigid", "not-stated", "n=11: catalogue_rigid"),
        (51, "minimal_polynomial", None, "n=51: minimal_polynomial: record has null"),
        (20, "exact_form", None, "n=20: exact_form: record has null"),
    ],
)
def test_a_perturbed_record_is_refused(
    n: int, field: str, replacement: object, expected: str
) -> None:
    """Each control breaks one transcribed field; the first is the miss that started this."""
    cases = _frontier_cases()
    cases[n]["reported_upper_bound"] = {**cases[n]["reported_upper_bound"], field: replacement}

    errors, _, _ = catalogue_transcription_errors(
        cases,
        _by_n(),
        _kingbird_source_key(),
        completeness_bound_from_text(_catalogue_text()),
    )

    assert [error for error in errors if re.search(re.escape(expected), error)], errors
