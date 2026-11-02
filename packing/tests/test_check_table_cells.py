"""Controls for `devtools.check_table_cells`, the guard against the formatter's cell loss.

The pinned flowmark-rs 0.4.0 reads every unescaped `|` in a table row as a column
separator, except inside a code span, an autolink or an HTML tag or comment, and drops
each cell past the header's count. Review A of #879 found nine rows cut short that way,
silently, at commit (think-7y5x). The splitter is pinned here against the rows the
formatter was measured on; the check, its scope and its place before the formatter in
the commit hook are pinned on repositories built in `tmp_path`.
"""

from __future__ import annotations

import os
import re
import shlex
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from devtools import check_table_cells
from devtools.check_math_spans import pinned_formatter
from devtools.check_table_cells import (
    MEASURED,
    MEASURED_WITH,
    UNTOUCHED,
    cells,
    lossy_rows,
    main,
    scope,
)
from sqpack.cli import validate

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


#: The rows of review A of #879's finding, in miniature: absolute-value bars in math.
TRUNCATED = textwrap.dedent(
    """\
    # Review

    | Case | Bound | Verdict |
    | --- | --- | --- |
    | n=11 | $|x| < 1$ | confirmed |
    | n=12 | $\\|x\\| < 1$ | confirmed |
    """
)


@pytest.mark.parametrize(("written", "formatted"), MEASURED, ids=lambda row: row[:24])
def test_each_measured_row_splits_as_the_pinned_formatter_split_it(
    written: str, formatted: str
) -> None:
    """What the formatter wrote back is the row's first three cells, padded with empty
    ones: the splitter puts every separator where flowmark-rs 0.4.0 did."""
    kept = cells(written)[:3]
    assert [*kept, *[""] * (3 - len(kept))] == cells(formatted)


def test_a_row_with_more_cells_than_its_header_is_refused_by_line() -> None:
    """The first row splits at the bars of `|x|` into five cells and would lose two; the
    escaped bars of the second are text, and it keeps its three."""
    [(line, width, found)] = lossy_rows(TRUNCATED)
    assert (line, width) == (5, 3)
    assert found == ["n=11", "$", "x", "< 1$", "confirmed"]


def test_a_row_the_formatters_fallback_spares_is_refused_too() -> None:
    """The formatter leaves a file whole when a cut would drop a code span, so the second
    table's row survives only while the first table's does; removing the code span, or
    escaping its row, would let the next commit cut the other. Both are refused."""
    assert [line for line, _, _ in lossy_rows(UNTOUCHED)] == [5, 9]


@pytest.mark.parametrize(
    "row",
    [
        "| a | `x|y` | b |",
        "| a | ``x|y`` | b |",
        "| a | <https://e.com/x|y> | b |",
        '| a | <span title="x|y">t</span> | b |',
        "| a | <!-- x|y --> | b |",
        "| a | x \\| y | b |",
        "| a | b |",
    ],
)
def test_bars_the_formatter_keeps_are_not_findings(row: str) -> None:
    assert lossy_rows(f"| A | B | C |\n| --- | --- | --- |\n{row}\n") == []


@pytest.mark.parametrize(
    "text",
    [
        "```\n| A |\n| --- |\n| $|x|$ |\n```\n",
        "---\ntitle: a | b\n---\n\nprose\n",
        "| A | $|x|$ |\n| --- | --- |\n| a | b |\n",
        "| A | B |\n| --- | --- |\n| a | b |\n\n| a | $|x|$ | c |\n",
    ],
    ids=["fenced", "frontmatter", "not a table", "after the table"],
)
def test_only_table_rows_are_read(text: str) -> None:
    """Code, frontmatter, a header the delimiter row does not match (which the formatter
    leaves alone) and a line after the table's blank line are not table rows."""
    assert lossy_rows(text) == []


@pytest.mark.parametrize("prefix", ["> ", "  "], ids=["block quote", "list item"])
def test_a_table_inside_a_container_is_read(prefix: str) -> None:
    table = "| A | B |\n| --- | --- |\n| a | $|x|$ |\n"
    text = "".join(f"{prefix}{line}\n" for line in table.splitlines())
    assert [line for line, _, _ in lossy_rows(text)] == [3]


def test_the_check_reads_what_the_formatter_formats_and_names_file_and_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A file `.flowmarkignore` protects is never formatted, so it is never read."""
    _write(tmp_path, ".flowmarkignore", "# preserved\nreviews/quoted.md\nraw/\n")
    _write(tmp_path, "reviews/quoted.md", TRUNCATED)
    _write(tmp_path, "raw/source.md", TRUNCATED)
    _write(tmp_path, "notes.md", "# Notes\n")
    assert scope(tmp_path) == ["notes.md"]
    assert main(["--root", str(tmp_path)]) == 0
    _write(tmp_path, "docs/review.md", TRUNCATED)
    assert main(["--root", str(tmp_path)]) == 1
    shown = capsys.readouterr().out
    assert "docs/review.md:5: " in shown
    assert "keeps `n=11` | `$` | `x` and drops `< 1$` | `confirmed`" in shown


def _git(root: Path, *arguments: str) -> None:
    subprocess.run(["git", "-C", str(root), *arguments], check=True, capture_output=True)


def test_the_hooks_run_also_reads_untracked_markdown_the_formatter_rewrites(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Review A1 of #882: the hook's `flowmark --auto .` rewrites every Markdown file git
    does not ignore, tracked or not, and an untracked draft lost a cell while the check,
    reading tracked files only, said ok. With `--untracked`, which the hook's target
    passes, it reads those too; `.gitignore` and `.flowmarkignore` still keep a file out.
    The gate reads tracked files only, so a step writing Markdown beside it cannot change
    its verdict."""
    _git(tmp_path, "init", "-q")
    _write(tmp_path, ".gitignore", "scratch/\n")
    _write(tmp_path, ".flowmarkignore", "raw/\n")
    _write(tmp_path, "notes.md", "# Notes\n")
    _git(tmp_path, "add", "notes.md")
    _write(tmp_path, "draft.md", "| Mode | Speed |\n| --- | --- |\n| mode | fast|slow |\n")
    _write(tmp_path, "scratch/ignored.md", TRUNCATED)
    _write(tmp_path, "raw/source.md", TRUNCATED)
    assert scope(tmp_path) == ["notes.md"]
    assert scope(tmp_path, untracked=True) == ["draft.md", "notes.md"]
    assert main(["--root", str(tmp_path)]) == 0
    capsys.readouterr()
    assert main(["--root", str(tmp_path), "--untracked"]) == 1
    assert "draft.md:3: " in capsys.readouterr().out


def test_the_commit_hook_checks_before_it_formats() -> None:
    """The hook runs `make format`; the check is a prerequisite of that target, so a row
    the formatter would cut short fails the commit before anything is rewritten. It reads
    untracked Markdown too, as the formatter does, and the hook's comment says so."""
    makefile = (REPO / "Makefile").read_text(encoding="utf-8")
    target = re.search(r"^format:(?P<prerequisites>[^\n]*)\n", makefile, re.MULTILINE)
    assert target is not None
    assert "table-cells-check" in target["prerequisites"].split()
    rule = re.search(r"^table-cells-check:[^\n]*\n\t(?P<recipe>[^\n]+)", makefile, re.MULTILINE)
    assert rule is not None
    assert "devtools.check_table_cells" in rule["recipe"]
    assert "--untracked" in rule["recipe"].split()
    lefthook = (REPO / "lefthook.yml").read_text(encoding="utf-8")
    assert "make format" in lefthook
    assert "table-cells-check" in lefthook


def test_the_measurement_names_the_formatter_the_makefile_pins() -> None:
    """Review A2 of #882: the splitter is right for the formatter it was measured on, and
    no gate runs `--measure`. A pin bump fails here until the measurement is re-run."""
    pinned = pinned_formatter(REPO / "Makefile")
    assert MEASURED_WITH in shlex.split(pinned), (
        f"the Makefile pins `{pinned}`, but MEASURED was taken with {MEASURED_WITH}: re-run "
        "`python -m devtools.check_table_cells --measure` and update MEASURED and "
        "MEASURED_WITH"
    )


def test_the_check_runs_on_every_pull_request_and_in_the_edit_tier() -> None:
    [step] = [s for s in validate.STEPS if s.action is validate._table_cells]  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert step.fast
    assert not step.broad


def test_the_measurement_reports_a_formatter_that_writes_back_something_else(
    tmp_path: Path,
) -> None:
    """`--measure` formats the measured rows with the pinned formatter and names each row
    it writes back differently. A formatter that changes nothing differs on every row the
    measurement recorded a change for."""
    unchanged = _write(tmp_path, "noop.py", "import sys\n")
    differ = check_table_cells.measure([sys.executable, os.fspath(unchanged)])
    assert len(differ) == sum(1 for written, formatted in MEASURED if written != formatted)
    assert differ
