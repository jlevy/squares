"""The synopsis headline cannot omit a result, reorder one, or misquote the rubric.

A result is registered, its rungs are re-derived, a reviewer scores its significance --
and then a reader opens `SYNOPSIS.md` and learns none of it. That happened: agenda 016
registered `T-014`, `T-015` and `T-016`, scored all three, and published a synopsis
whose opening section named no result at all. Nothing failed, because nothing was
checking the presentation of a complete record.

These are the properties that make that impossible. The first is the one that would
have caught it: every result in `frontier/results.yaml` is a row in the block, so a
result cannot be registered and go unpresented. The rest keep the block honest once it
exists -- the register's reading order, the rubric's own wording, and the round trip
with the Markdown formatter that owns the document this block lives in.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from devtools import render_results_headline as headline_view
from devtools.significance import anchors, by_significance, load

PROJECT_ROOT = Path(__file__).resolve().parents[1]

APOSTROPHE = "\u2019"
ELLIPSIS = "\u2026"


def committed_block() -> str:
    """The block as `SYNOPSIS.md` currently carries it."""
    return headline_view.block(headline_view.SYNOPSIS.read_text(encoding="utf-8"))


def row_ids(block: str) -> list[str]:
    """The result ids the block's table rows name, in the order they are written."""
    return re.findall(r"^\| \[(T-\d+)\]", block, re.MULTILINE)


def legend(block: str) -> dict[int, str]:
    """The rubric anchors the block's legend states, by score."""
    found = re.findall(r"^\| `S(\d)` \| (.+?) \|$", block, re.MULTILINE)
    return {int(score): anchor for score, anchor in found}


def document(body: str) -> str:
    """A minimal host document, so no test writes to the real synopsis."""
    return (
        "## The Program at a Glance\n\nFraming prose a person owns.\n\n"
        f"{headline_view.BEGIN}\n\n{body}\n\n{headline_view.END}\n\nProse below.\n"
    )


def test_every_registered_result_reaches_the_synopsis() -> None:
    """The guarantee: no result can be registered, scored, and left unpresented.

    Asserted as a set equality against the register rather than a count, so a row
    silently swapped for another still fails, and against the committed document rather
    than a fresh render, so a stale synopsis fails here and not only in the gate.
    """
    registered = {record["id"] for record in load()}

    assert set(row_ids(committed_block())) == registered
    assert len(row_ids(committed_block())) == len(registered)


def test_rows_stand_in_the_registers_reading_order() -> None:
    """Reading order is what the significance score is for, so it is not the renderer's.

    `by_significance` is the one place that knows it, shared with `RESULTS.md` and the
    pull-request description. A second ordering here would be a second opinion about
    which result matters most, published above all the others.
    """
    assert row_ids(committed_block()) == [record["id"] for record in by_significance(load())]


def test_the_legend_quotes_the_rubric_epistemics_currently_states() -> None:
    """The policy's wording, read live, not a copy of it that can drift.

    `epistemics.md` owns the significance vocabulary. A rubric anchor edited there and
    not carried through fails here, which is the same failure `D-010`, `D-017` and
    `D-022` are: a hand-maintained view still stating what its source used to say.
    """
    block = committed_block()
    awarded = {record["significance"]["score"] for record in load()}

    assert legend(block) == {score: anchors()[score] for score in awarded}


def test_the_legend_covers_only_the_scores_the_table_awards() -> None:
    """An anchor for a score nobody has awarded would claim a range the register lacks.

    Driven from a subset of the live register rather than from what the document shows,
    so the property holds for a register whose awarded scores are not today's.
    """
    rubric = anchors()
    only_s2 = [record for record in load() if record["significance"]["score"] == 2]

    assert only_s2, "the register no longer awards S2; pick another score for this case"
    assert headline_view.legend_rows(only_s2)[2:] == [f"| `S2` | {rubric[2]} |"]


def test_a_score_the_rubric_does_not_define_is_refused() -> None:
    """A legend with a hole in it is worse than a renderer that stops.

    This is the rubric edit nobody carried through, seen from the other side: a score
    `epistemics.md` no longer anchors must not render as an unexplained row.
    """
    with pytest.raises(SystemExit, match="S9"):
        headline_view.legend_rows([{"significance": {"score": 9}}])


def test_check_fails_on_a_drifted_block_and_clears_after_a_render(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A dropped row is what the gate must catch, and a render must be what fixes it."""
    rendered = headline_view.render_lines(by_significance(load()))
    first_row = next(line for line in rendered if line.startswith("| [T-"))
    dropped = [line for line in rendered if line != first_row]
    synopsis = tmp_path / "SYNOPSIS.md"
    synopsis.write_text(document("\n".join(dropped)), encoding="utf-8")
    monkeypatch.setattr(headline_view, "SYNOPSIS", synopsis)

    assert headline_view.main(["--check"]) == 1
    assert headline_view.main([]) == 0
    assert headline_view.main(["--check"]) == 0
    assert row_ids(headline_view.block(synopsis.read_text(encoding="utf-8"))) == [
        record["id"] for record in by_significance(load())
    ]


def test_the_committed_synopsis_is_current() -> None:
    """The gate step, run in the suite: the record and the front document agree today."""
    assert headline_view.main(["--check"]) == 0


def test_the_formatter_cannot_leave_the_block_stale(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The formatter owns this document, so its typography is not drift.

    Measured on the pinned flowmark-rs 0.4.0: it curls the straight apostrophes these
    claims are written with, in place, inside the generated block. Comparing bytes would
    report that as staleness forever and re-rendering would flatten it back on every run
    -- the fight `.flowmarkignore` records for `ledger.md` and `defects.md`. So a curled
    block is current, and a render over it is an empty diff.
    """
    curled = committed_block().replace("'", APOSTROPHE)
    synopsis = tmp_path / "SYNOPSIS.md"
    synopsis.write_text(document(curled.strip("\n")), encoding="utf-8")
    monkeypatch.setattr(headline_view, "SYNOPSIS", synopsis)
    before = synopsis.read_text(encoding="utf-8")

    assert APOSTROPHE in curled, "expected apostrophes in the claims to curl"
    assert headline_view.main(["--check"]) == 0
    assert headline_view.main([]) == 0
    assert synopsis.read_text(encoding="utf-8") == before


def test_a_rendered_claim_carries_the_ellipsis_the_formatter_would_write() -> None:
    """The one rewrite `fold` does not fold back, so the renderer writes it directly.

    Measured with the same formatter: `...` becomes a space and U+2026, and `fold` maps
    the character while leaving the inserted space. A cell rendered in ASCII would be
    rewritten at every commit and re-flattened at every render.
    """
    assert headline_view.cell("side 3.877083590022814..., with 14 pairs") == (
        f"side 3.877083590022814 {ELLIPSIS}, with 14 pairs"
    )
    assert ELLIPSIS in committed_block()


def test_the_block_is_table_rows_only() -> None:
    """Prose inside the block would be rewrapped by the formatter and never settle.

    A rewrapped generated line is drift no re-render can clear, because the renderer
    emits one line and the formatter splits it. Table rows are immune: Markdown keeps
    a row on one line however long it grows, which is why the legend is a table too.
    """
    body = [line for line in committed_block().splitlines() if line.strip()]

    assert body, "the block is empty"
    assert all(line.startswith("|") and line.endswith("|") for line in body)


def test_every_link_the_block_writes_resolves_from_the_repository_root() -> None:
    """`SYNOPSIS.md` sits at the root, so a `packing/`-relative path here is a dead link.

    `devtools.check_synopsis` would catch it, but only after the block landed in the
    document; the renderer is where the convention is decided, so it is pinned here.
    """
    repository_root = PROJECT_ROOT.parent
    targets = re.findall(r"\]\(([^)]+)\)", committed_block())

    assert targets
    for target in targets:
        path, _, _fragment = target.partition("#")
        assert (repository_root / path).is_file(), f"dead link -> {target}"
