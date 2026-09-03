#!/usr/bin/env python3
"""Put the results register where a reader arrives, not four hundred lines in.

A result is registered in `frontier/results.yaml`, its rungs are re-derived by
`devtools/check_results.py`, a reviewer scores its significance, and
`devtools/render_results.py` renders it into `frontier/RESULTS.md`. None of that reaches
someone who opens the front document: agenda 016 registered `T-014`, `T-015` and `T-016`,
scored all three, and published a synopsis whose first mention of a significance score
was four hundred lines in and whose opening section named no result at all. The record
was complete and the presentation was not, and the presentation is what a reader gets.

So the glance section carries every registered result, generated rather than curated.
Omission is the failure this closes: a result in the register is a row here, in the
order `devtools/significance.py` ranks them, or the gate fails. The rubric legend is
read from `epistemics.md` at render time for the reason that module gives -- a rubric
restated in code drifts from the policy it claims to quote, which is `D-010`, `D-017`
and `D-022`.

The framing prose around the block stays outside the markers. The judgement about why
a reader should care is a person's and revisable; the facts are the register's and are
not. That is the same split `devtools/render_document_map.py` already makes lower down
in this document.

Staleness is decided on what the block *says*, not on its bytes, because `SYNOPSIS.md`
is prose the Markdown formatter owns and the claims are written in ASCII it rewrites in
place. A byte-exact generated block inside a formatted file fights the formatter forever
-- the failure `.flowmarkignore` records for `ledger.md` and `defects.md`, and the one
`devtools/render_research_tables.py` already solved for the research tables, whose
`fold` and `keep_document_typography` this reuses rather than re-deriving.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.render_results_headline
    uv run --frozen --all-extras --group dev python -m devtools.render_results_headline --check
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from strif import atomic_output_file

from devtools.render_research_tables import fold, keep_document_typography
from devtools.significance import anchors, by_significance, headline, load, scope_label

ROOT = Path(__file__).resolve().parents[1]
# The repository root. The reader-facing documents live there, not under packing/.
REPO = ROOT.parent
SYNOPSIS = REPO / "SYNOPSIS.md"
BEGIN = "<!-- BEGIN GENERATED: results-headline (devtools.render_results_headline) -->"
END = "<!-- END GENERATED: results-headline -->"

# Link targets are repository-relative because SYNOPSIS.md sits at the repository root.
POLICY = "epistemics.md"
VERIFICATION = f"{POLICY}#verification"
CONFIRMATION = f"{POLICY}#confirmation"
SIGNIFICANCE = f"{POLICY}#significance-and-novelty"
REGISTER_VIEW = "packing/frontier/RESULTS.md"

# An ASCII ellipsis is the one thing a claim can carry that the formatter rewrites into a
# form `fold` does not fold back. Measured on the pinned flowmark-rs 0.3.2, 2026-09-03:
# `3.877083590022814...` in T-011's claim becomes the same digits, a space, and U+2026,
# and `fold` maps that character while leaving the inserted space. Rendering the
# formatter's own form makes the block a fixed point; `says` below folds the space away
# too, so a later change to that rule costs a rewrite rather than a check nobody can clear.
#
# The character is written as an escape, for the reason
# `tests/test_generated_table_typography.py` states: a literal one is invisible in a diff
# and ambiguous on sight.
_ASCII_ELLIPSIS = re.compile(r"\s*\.\.\.")
_ELLIPSIS = " \u2026"


def cell(text: str) -> str:
    """One table cell: a pipe inside a claim would end the row it appears in."""
    collapsed = " ".join(text.split()).replace("|", r"\|")
    return _ASCII_ELLIPSIS.sub(_ELLIPSIS, collapsed)


def says(block: str) -> list[str]:
    """What a block's lines state, with formatter-owned typography folded away."""
    return [fold(line).replace(" ...", "...") for line in block.splitlines() if line.strip()]


def table_rows(results: list[dict]) -> list[str]:
    """Every registered result, in the register's own reading order."""
    rows = [
        (
            f"| Result | `n` | [`V`]({VERIFICATION}) | [`C`]({CONFIRMATION}) "
            f"| [`S`]({SIGNIFICANCE}) | [Novelty]({SIGNIFICANCE}) | What it establishes |"
        ),
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    rows.extend(
        f"| [{record['id']}]({REGISTER_VIEW}) | {scope_label(record)} "
        f"| `{record['verification']}` | `{record['confirmation']}` "
        f"| `S{record['significance']['score']}` | `{record['novelty']}` "
        f"| {cell(headline(record))} |"
        for record in results
    )
    return rows


def legend_rows(results: list[dict]) -> list[str]:
    """The rubric anchors for exactly the scores the table above awards.

    Scores nobody has awarded are left out: a legend covering all five would assert
    that the register spans them, which is not a fact this block has.
    """
    rubric = anchors()
    scores = sorted({record["significance"]["score"] for record in results}, reverse=True)
    missing = [score for score in scores if score not in rubric]
    if missing:
        rendered = ", ".join(f"S{score}" for score in missing)
        raise SystemExit(f"epistemics.md defines no anchor for {rendered}")
    return [
        f"| Significance | What [`epistemics.md`]({SIGNIFICANCE}) anchors it to |",
        "| --- | --- |",
        *(f"| `S{score}` | {rubric[score]} |" for score in scores),
    ]


def render_lines(results: list[dict]) -> list[str]:
    """The block body.

    Every line is a table row on purpose. The formatter rewraps prose it owns, and a
    generated line it has rewrapped is drift no re-render can settle; a table row stays
    one line however long it grows.
    """
    return [*table_rows(results), "", *legend_rows(results)]


def block(text: str) -> str:
    """The current block body, refusing a document whose markers cannot be trusted."""
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        message = "SYNOPSIS.md needs exactly one ordered results-headline marker pair"
        raise ValueError(message)
    start = text.index(BEGIN) + len(BEGIN)
    end = text.index(END, start)
    return text[start:end]


def expected_synopsis(text: str, results: list[dict]) -> str:
    """Replace the one generated block while preserving editorial prose around it.

    A row that still says what the document says is written back as the document has
    it, so a render over an unchanged tree is an empty diff even after the formatter
    has curled the quotes in these rows.
    """
    kept = keep_document_typography(block(text), render_lines(results))
    start = text.index(BEGIN)
    end = text.index(END, start) + len(END)
    body = "\n".join(kept)
    return text[:start] + f"{BEGIN}\n\n{body}\n\n{END}" + text[end:]


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--check", action="store_true", help="fail if SYNOPSIS.md is stale")
    return command


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    results = by_significance(load())
    current = SYNOPSIS.read_text(encoding="utf-8")
    if arguments.check:
        if says(block(current)) != says("\n".join(render_lines(results))):
            print("SYNOPSIS.md results headline is stale", file=sys.stderr)
            print(
                "  run: uv run --frozen python -m devtools.render_results_headline",
                file=sys.stderr,
            )
            return 1
        print(f"  synopsis headline carries all {len(results)} registered results")
        return 0
    expected = expected_synopsis(current, results)
    if current != expected:
        with atomic_output_file(SYNOPSIS) as temporary:
            temporary.write_text(expected, encoding="utf-8")
        print(f"rendered synopsis results headline ({len(results)} results)")
    else:
        print("synopsis results headline already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
