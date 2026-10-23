# ruff: noqa: RUF001 -- the records under test are prose with curly apostrophes.
"""The sentence a case record owes a source that says AI assisted its work.

`devtools.state_ai_assistance` finds the paragraph that describes the source's result and
appends the source's statement to it. The rules are tested over small hand-written
records, and the committed records are held to having every statement they owe, less a
named list that only shrinks. Each statement a committed record makes is also dropped from
it, and the check must see the drop.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from devtools import state_ai_assistance as assistance

WAND125 = assistance.statement_of("[wand125 rectangle bounds 2026]")
TOKOHARU = assistance.statement_of("[Tokoharu density 2026]")

#: Records still owing a statement. Empty since the n = 68 to 95 records took their
#: Hosono sentence on 2026-09-29, and it may only stay empty: a record added here is a
#: statement not made.
PENDING: frozenset[str] = frozenset()


def _record(front: str, body: str) -> str:
    return f"---\n{front}\n---\n{body}"


INTAKE = """# `s(42)` — open

**External intake, 2026-09-28.** Hosono’s
rectangle-density source reports `s(42) >= 679/100`,
accepted by Tokoharu’s unchanged interval checker.

| a table | naming Hosono |
| --- | --- |

```
Hosono in a code block
```

Open.
"""


def test_prose_paragraphs_leave_out_headings_tables_code_and_comments() -> None:
    _, lines = assistance.split_record(_record("x: 1", INTAKE))
    texts = [paragraph.text for paragraph in assistance.paragraphs(lines)]
    assert texts == [
        (
            "**External intake, 2026-09-28.** Hosono’s rectangle-density source reports "
            "`s(42) >= 679/100`, accepted by Tokoharu’s unchanged interval checker."
        ),
        "Open.",
    ]


def test_the_statement_is_appended_to_the_paragraph_that_describes_the_source() -> None:
    text = _record("sources:\n  - key: '[wand125 rectangle bounds 2026-09-28]'", INTAKE)
    stated = assistance.state(text)
    assert (
        "accepted by Tokoharu’s unchanged interval checker.\n" + WAND125.sentence + "\n\n| a"
    ) in stated
    assert assistance.state(stated) == stated


def test_a_checker_run_on_someone_else_s_certificate_is_not_its_author_s_result() -> None:
    """Tokoharu's checker accepted Hosono's certificate; that paragraph owes Hosono only."""
    text = _record("sources:\n  - key: '[Tokoharu density 2026]'", INTAKE)
    _, lines = assistance.split_record(text)
    assert [
        (statement, paragraph)
        for statement, paragraph, _ in assistance.owed("[Tokoharu density 2026]", lines)
    ] == [(TOKOHARU, None)]
    assert assistance.state(text) == text


def test_a_record_that_does_not_cite_the_source_owes_nothing() -> None:
    text = _record("sources: []", INTAKE)
    assert assistance.state(text) == text


def test_a_marker_already_in_the_paragraph_is_the_statement_made() -> None:
    said = INTAKE.replace(
        "unchanged interval checker.",
        "unchanged interval checker.\nParts had AI assistance under human direction.",
    )
    text = _record("sources:\n  - key: '[wand125 point bounds 2026]'", said)
    assert assistance.state(text) == text


def test_every_committed_record_makes_the_statements_it_owes() -> None:
    missing, _ = assistance.report(assistance.records(None))
    assert {label.split(":", 1)[0] for label in missing} <= PENDING


def _without_marker(text: str, statement: assistance.Statement) -> str:
    """The record with `statement`'s marker taken out of every paragraph anchored to it.

    Each anchored paragraph is rejoined onto one line first, since the formatter may have
    broken the marker across two.
    """
    front, lines = assistance.split_record(text)
    anchored = [
        paragraph
        for paragraph in assistance.paragraphs(lines)
        if statement.anchor.search(paragraph.text)
    ]
    for paragraph in reversed(anchored):
        lines[paragraph.first : paragraph.last + 1] = [
            paragraph.text.replace(statement.marker, "")
        ]
    return text.split("---\n", 2)[0] + "---\n" + front + "---\n" + "\n".join(lines)


@pytest.mark.parametrize(
    "statement",
    assistance.STATEMENTS,
    ids=[min(statement.keys).strip("[]") for statement in assistance.STATEMENTS],
)
def test_each_statement_a_committed_record_makes_is_missed_when_its_marker_is_dropped(
    statement: assistance.Statement, tmp_path: Path
) -> None:
    """Presence alone, as the test above holds it, would pass a check that never looked.

    Every committed record that owes and makes `statement` has the marker dropped from the
    paragraphs anchored to it, and `report()` must list each one as missing that statement:
    not as fine, and not as unanchored. The label names the statement's cited keys, so a
    drop that also takes another statement's marker cannot stand in for this one.
    """
    dropped: set[str] = set()
    citing = [
        path
        for path in assistance.records(None)
        if any(
            key in assistance.split_record(path.read_text(encoding="utf-8"))[0]
            for key in statement.keys
        )
    ]
    if not citing:
        # A statement no record's front matter calls for, such as the tools' (T-058 and
        # T-059 are register entries only): it is owed nowhere, and nothing is missing.
        missing, _ = assistance.report(assistance.records(None), catalogue={})
        assert not [label for label in missing if any(key in label for key in statement.keys)]
        return
    for path in citing:
        text = path.read_text(encoding="utf-8")
        front, lines = assistance.split_record(text)
        if not any(
            owed is statement and paragraph is not None and said
            for owed, paragraph, said in assistance.owed(front, lines)
        ):
            continue
        (tmp_path / path.name).write_text(_without_marker(text, statement), encoding="utf-8")
        cited = ", ".join(sorted(key for key in statement.keys if key in front))
        dropped.add(f"{path.name}: {cited}")
    assert dropped, "no committed record makes this statement, so no drop is measured"
    missing, unanchored = assistance.report(sorted(tmp_path.iterdir()), catalogue={})
    assert dropped <= set(missing)
    assert not dropped & set(unanchored)


CATALOGUE_RECORD = """title: s(7)
packing:
  n: 7
  reported_upper_bound:
    value: '2.5'
    source_key: '[Kingbird]'"""


@dataclass(frozen=True)
class _Entry:
    credit_line: str | None


AI_CREDIT = _Entry(
    "Found by A. Name in August 2026, working with unspecified AI.\n"
    "Optimized by B. Name in September 2026."
)
AI_QUOTE = (
    "In the catalogue’s words: “Found by A. Name in August 2026, working with unspecified AI.”"
)


def test_a_catalogue_record_owes_the_entry_s_ai_statement_quoted_whole() -> None:
    """The catalogue states AI assistance per entry, so the record quotes that sentence."""
    catalogue = {7: AI_CREDIT}
    bare = _record(CATALOGUE_RECORD, "## The packing\n\nFound.\n")
    assert assistance.catalogue_owed(bare, catalogue) == (AI_QUOTE,)

    # Reflowed across lines, as the formatter leaves it, the quotation still counts.
    wrapped = AI_QUOTE.replace(" working with ", "\nworking with ")
    body = f"## The packing\n\nFound by A. Name in 2026.\n{wrapped}\n"
    assert assistance.catalogue_owed(_record(CATALOGUE_RECORD, body), catalogue) == ()


def test_a_quotation_the_formatter_curled_inside_still_counts() -> None:
    """n = 87: the formatter curls the straight quotes the catalogue nests in a sentence."""
    catalogue = {
        7: _Entry('Improved by A. Name in September 2026, working with X, with help from "B".')
    }
    (owed,) = assistance.catalogue_owed(_record(CATALOGUE_RECORD, "Found.\n"), catalogue)
    assert '"B"' in owed
    curled = owed.replace('"B"', "“B”")
    body = f"## The packing\n\nFound.\n{curled}\n"
    assert assistance.catalogue_owed(_record(CATALOGUE_RECORD, body), catalogue) == ()


def test_a_quotation_whose_apostrophes_the_formatter_curled_still_counts() -> None:
    """The formatter curls single quotes and apostrophes as it curls double ones."""
    catalogue = {
        7: _Entry("Improved by A. O'Name in September 2026, working with the 'X' model.")
    }
    (owed,) = assistance.catalogue_owed(_record(CATALOGUE_RECORD, "Found.\n"), catalogue)
    assert "O'Name" in owed
    curled = owed.replace("O'Name", "O’Name").replace("'X'", "‘X’")
    body = f"## The packing\n\nFound.\n{curled}\n"
    assert assistance.catalogue_owed(_record(CATALOGUE_RECORD, body), catalogue) == ()


def test_a_record_reporting_another_source_owes_the_catalogue_nothing() -> None:
    elsewhere = CATALOGUE_RECORD.replace("'[Kingbird]'", "'[Elsewhere 2026]'")
    assert assistance.catalogue_owed(_record(elsewhere, "Found.\n"), {7: AI_CREDIT}) == ()


def test_the_catalogue_records_quote_their_statements_and_the_check_sees_a_drop() -> None:
    """n = 69 owes the catalogue's statement, and dropping it must fail the check.
    n = 179 retains its historical quote but now reports the 7 October SQUISH update;
    the catalogue check holds only records whose reported bound is the catalogue's."""
    entries = assistance.record_catalogue_entries()
    for n in (69, 179):
        text = (assistance.FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
        assert assistance.catalogue_owed(text, entries) == ()
        start = text.index("In the catalogue’s words:")
        end = text.index("”", start) + 1
        missing = assistance.catalogue_owed(text[:start] + text[end:], entries)
        if n == 69:
            (owed,) = missing
            assert owed.startswith("In the catalogue’s words: “")
        else:
            assert missing == ()


def test_the_statements_are_the_bibliography_s_and_keys_that_agree_share_one() -> None:
    """think-j5so: the four keys a hard-coded list lacked are read with the rest, and
    Hosono's seven releases share his README's sentence."""
    assert "[wand125 rectangle bounds 2026-10-01]" in WAND125.keys
    assert len(WAND125.keys) == 7
    for key in (
        "[evand square-packing 2026-10-01]",
        "[franciscouzo square-packing 2026-09-27]",
        "[wand125 tools 2026]",
        "[Ahmed n11 optimality 2026]",
    ):
        statement = assistance.statement_of(key)
        assert statement.marker in statement.sentence
    assert assistance.statement_of("[franciscouzo square-packing 2026-09-27]").counts == {
        102,
        103,
    }
    assert assistance.statement_problems() == []


def test_a_statement_whose_sentence_lacks_its_marker_is_refused(tmp_path: Path) -> None:
    """`--apply` would write it into every record that owes it, and `--check` would still
    call each missing."""
    bibliography = tmp_path / "bibliography.yaml"
    bibliography.write_text(
        "sources:\n"
        "  - key: '[a 2026]'\n"
        "    ai_assistance: {sentence: It says so., marker: AI assistance, anchor: 'A('}\n"
        "  - key: '[b 2026]'\n"
        "    ai_assistance:\n"
        "      {sentence: B used AI assistance., marker: AI assistance, anchor: B}\n",
        encoding="utf-8",
    )
    problems = assistance.statement_problems(bibliography)
    assert [problem.split(":")[0] for problem in problems] == ["[a 2026]", "[a 2026]"]
    assert "lacks its own marker" in problems[1]
    (only,) = [s for s in assistance.load_statements(bibliography) if "[b 2026]" in s.keys]
    assert only.counts is None


def test_a_statement_of_some_counts_is_owed_only_at_them() -> None:
    """Couzo's statement concerns his n = 102 and 103 packings alone: a record of another
    count that describes his packing owes nothing."""
    couzo = assistance.statement_of("[franciscouzo square-packing 2026-09-27]")
    front = "packing:\n  n: {n}\nsources:\n  - key: '[franciscouzo square-packing 2026-09-27]'"
    body = "Francisco Couzo found the earlier packing.\n"
    for n, owes in ((130, False), (102, True)):
        _, lines = assistance.split_record(_record(front.format(n=n), body))
        found = [s for s, _, _ in assistance.owed(front.format(n=n), lines) if s is couzo]
        assert bool(found) is owes, n
