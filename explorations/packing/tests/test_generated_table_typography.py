#!/usr/bin/env python3
"""The generated research tables must not fight the Markdown formatter.

`devtools.render_research_tables` renders table rows from the ASCII text stored in
`frontier/`, and the repository's Markdown formatter then curls the quotes in those
rows in place. Re-rendering used to flatten them straight back on every run, in lines
nobody had edited, and `--check` folds typography away so it never saw the damage. The
diff noise attached itself to whatever was committed next and was reverted by hand
twice, once taking a real table update with it.

So these are round-trip contracts: rendering over an unchanged tree must be a no-op
byte for byte, and a row whose content genuinely moved must still be rewritten.

Curly characters are written as escapes here for the same reason the renderer writes
them that way: a literal one is invisible in a diff and ambiguous on sight.
"""

from __future__ import annotations

from pathlib import Path

from devtools.render_research_tables import (
    MAIN,
    extract,
    keep_document_typography,
    load_cases,
    splice,
    tables,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

APOSTROPHE = "\u2019"
OPEN_QUOTE = "\u201c"
CLOSE_QUOTE = "\u201d"
CURLY = (APOSTROPHE, OPEN_QUOTE, CLOSE_QUOTE, "\u2018")

# The block the formatter actually curls in the research document.
BLOCK = "sources-recovered"

STROMQUIST = (
    "| **[Stromquist 1984]** Packing | The author{a}s page; {o}unpublished{c} was its status. |"
)
TRUMP = "| **[Trump 2023]** Packing of 11 | Walter Trump{a}s public author page. |"


def straight(row: str) -> str:
    """A row as this module renders it from the ASCII in `frontier/`."""
    return row.format(a="'", o='"', c='"')


def curled(row: str) -> str:
    """The same row after the Markdown formatter has normalized its typography."""
    return row.format(a=APOSTROPHE, o=OPEN_QUOTE, c=CLOSE_QUOTE)


DOCUMENT = "\n".join(
    [
        "prose above",
        "",
        "<!-- BEGIN GENERATED: demo (devtools.render_research_tables) -->",
        "",
        "| Source | How it was recovered |",
        "| --- | --- |",
        curled(STROMQUIST),
        curled(TRUMP),
        "",
        "<!-- END GENERATED: demo -->",
        "",
        "prose below",
        "",
    ]
)

RENDERED = [
    "| Source | How it was recovered |",
    "| --- | --- |",
    straight(STROMQUIST),
    straight(TRUMP),
]


def test_splice_leaves_a_curled_block_alone_when_nothing_changed() -> None:
    """Straight quotes rendered over their own curled form are not an edit."""
    assert splice(DOCUMENT, "demo", RENDERED) == DOCUMENT


def test_splice_rewrites_only_the_row_whose_content_moved() -> None:
    """A real data change still lands, and its neighbours keep their typography."""
    moved = "| **[Trump 2023]** Packing of 11 | Author page, retrieved. |"

    spliced = splice(DOCUMENT, "demo", [*RENDERED[:3], moved])

    assert moved in spliced
    assert curled(TRUMP) not in spliced
    assert curled(STROMQUIST) in spliced


def test_a_row_with_no_counterpart_is_written_as_rendered() -> None:
    """Nothing to preserve means the rendered text wins, which is how rows appear."""
    kept = keep_document_typography("| a | b |\n", ["| a | b |", "| c | d |"])

    assert kept == ["| a | b |", "| c | d |"]


def test_repeated_rows_are_matched_one_for_one() -> None:
    """Two identical rows consume two document lines, not the same one twice."""
    curly = f"| x{APOSTROPHE}s |"

    assert keep_document_typography(f"{curly}\n{curly}\n", ["| x's |"] * 2) == [curly] * 2


def test_the_research_document_still_carries_curled_generated_rows() -> None:
    """Guard against the round-trip contract below passing vacuously."""
    text = MAIN.read_text(encoding="utf-8")

    curly = [
        name
        for name in tables(load_cases())
        if any(character in extract(text, name) for character in CURLY)
    ]

    assert BLOCK in curly, f"expected curled quotes in the {BLOCK} block; found {curly}"


def test_rendering_over_an_unchanged_tree_is_a_no_op() -> None:
    """The whole point: a render on a clean tree must produce an empty diff."""
    text = MAIN.read_text(encoding="utf-8")

    rendered = text
    for name, rows in tables(load_cases()).items():
        rendered = splice(rendered, name, rows)

    assert rendered == text, (
        f"re-rendering rewrote {MAIN.relative_to(PROJECT_ROOT)} with no upstream change"
    )
