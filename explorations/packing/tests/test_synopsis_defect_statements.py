"""Behavioral checks for the every-occurrence unprotected-fix rule (D-326)."""

from __future__ import annotations

from devtools.check_synopsis import check_unprotected_statements


def test_one_stale_statement_fails_even_beside_a_correct_one() -> None:
    text = (
        "7 fixes left no regression check behind.\n"
        "Later prose repeats it: 6 fixes left no regression check behind.\n"
    )

    problems = check_unprotected_statements(text, 7)

    assert problems, "a stale second statement must fail, not hide behind a correct one"
    assert "at every occurrence" in problems[0]


def test_every_correct_statement_passes_in_digit_or_spelled_form() -> None:
    text = (
        "7 fixes left no regression check behind.\n"
        "Seven fixes left no regression check behind, restated.\n"
    )

    assert check_unprotected_statements(text, 7) == []


def test_a_document_with_no_statement_fails() -> None:
    assert check_unprotected_statements("no aggregate here", 7)
