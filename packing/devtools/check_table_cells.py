#!/usr/bin/env python3
"""Refuse a Markdown table row the pinned formatter would cut short.

The commit hook formats the whole repository with the pinned `flowmark-rs==0.4.0`, and
that formatter reads a table row's cells the way a GFM table does: every `|` that is not
escaped is a column separator. A row with more cells than its header keeps the header's
count and silently loses the rest. Review A of #879 found nine rows of
`review-2026-11-02-ryu-quarter-cube-strongest-tier.md` whose absolute-value bars, `$|x|$`,
had been read as separators and their Verdict cells dropped in the first commit
(think-7y5x). The hook gave no sign, since a formatter that rewrites is working as asked.

Measured on 2 November 2026 with the Makefile's pinned command on copies, and recorded
in `MEASURED`, which `--measure` re-runs:

- **Split**, so the cell is cut: a bar inside `$...$` or `$$...$$`, inside a link's text
  or address, inside emphasis, between two HTML tags (`<code>a|b</code>`), after an
  escaped backslash (`\\|`), or after a backtick no later run closes.
- **Kept**, as text: `\\|`, a bar inside a code span (`` `a|b` ``, which GitHub's own
  renderer still splits), inside an autolink, inside an HTML tag's attribute or an HTML
  comment, and the entity `&#124;`.
- A row with fewer cells than its header is padded with empty ones, which loses nothing;
  a header whose cells differ in number from its delimiter row is not a table, and is
  left alone.
- **Unless a dropped cell holds a code span or a `$` pair**: then the formatter leaves
  the *whole file* as written, prose and every other table included, and says nothing
  (`UNTOUCHED`). The row survives in the source, GitHub still shows it cut, and the file
  silently stops being formatted. Two files on `main` were in that state when this check
  was written, with 2,522 lines of formatting held back between them.

`cells` is that splitter. It errs one way only: a bar it calls a separator and the
formatter keeps as text is a refusal that `\\|` answers, while the reverse would be a
row lost again. The one divergence measured is of the safe kind -- the formatter keeps a
bar between backslash-escaped backticks, which this splitter splits. A row the fallback
spares is refused like any other, since an edit that removes the protecting cell, here
or anywhere in the file, cuts it at the next commit.

The check reads what the formatter formats, less what `.flowmarkignore` names and the
vendored trees, which the formatter never rewrites. It runs before the formatter in the
commit hook, as a prerequisite of `make format`, so a commit that would lose a cell fails
with the file and line instead; there it passes `--untracked`, since `flowmark --auto .`
also rewrites every Markdown file git does not ignore, and an untracked draft lost a cell
while a tracked-only check said ok (review A1 of #882). It also runs on every pull
request, on tracked files only, since a row committed without the hook is cut at the next
commit anyone makes; a step writing Markdown beside it cannot change that verdict. It
prints its own wall time.

Usage, from `packing/`:

    uv run --frozen --group dev python -m devtools.check_table_cells
    uv run --frozen --group dev python -m devtools.check_table_cells --untracked
    uv run --frozen --group dev python -m devtools.check_table_cells --measure

Exits 1 on a row the formatter would cut, or with `--measure` on a row the pinned
formatter now writes back differently from the record, or when it cannot run.
"""

from __future__ import annotations

import argparse
import re
import shlex
import sys
import tempfile
import time
from collections.abc import Sequence
from functools import cache
from itertools import pairwise
from pathlib import Path

from devtools.check_math_spans import format_copy, pinned_formatter
from devtools.repo_scope import (
    excluded_by,
    flowmark_exclusions,
    tracked_markdown,
    vendored_directories,
)

REPO = Path(__file__).resolve().parents[2]

#: The constructs whose bars the formatter keeps as text, from `<`: an autolink, an HTML
#: open or closing tag, and an HTML comment, as CommonMark defines each. A construct
#: measured nowhere is left out, so that a bar inside it is read as a separator.
_HTML = re.compile(
    r"<[A-Za-z][A-Za-z0-9.+-]{1,31}:[^<>\x00-\x20]*>"
    r"|<[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*>"
    r"|<[A-Za-z][A-Za-z0-9-]*"
    r"(?:\s+[A-Za-z_:][A-Za-z0-9_.:-]*(?:\s*=\s*(?:[^\s\"'=<>`]+|'[^']*'|\"[^\"]*\"))?)*"
    r"\s*/?>"
    r"|</[A-Za-z][A-Za-z0-9-]*\s*>"
    r"|<!--.*?-->"
)
#: What `_bars` stops at: an escape and the character it escapes, a backtick run, a `<`
#: that may open a tag or an autolink, and a bar.
_TOKEN = re.compile(r"\\.|`+|<|\|", re.DOTALL)
#: A GFM delimiter row: dashes, optionally colon-aligned, between bars.
_DELIMITER = re.compile(r"\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?")
#: A block quote's markers and a list item's indentation, before a table's first bar.
_CONTAINER = " \t>"
#: A code fence; a backtick fence's info string holds no backtick, so "```a|b```" at the
#: start of a line is inline code rather than a fence.
_FENCE = re.compile(r"(?P<fence>`{3,}(?=[^`]*$)|~{3,})")

#: The formatter `MEASURED` and `UNTOUCHED` were taken with, and the only one `cells` is
#: known to match. A fast test fails when the Makefile pins another (review A2 of #882):
#: re-run `--measure` against the new pin and update both records and this.
MEASURED_WITH = "flowmark-rs==0.4.0"
#: Rows of a table headed `| Case | A | B |` as written, and as the pinned formatter
#: wrote each back on 2 November 2026. `--measure` formats them again.
MEASURED: tuple[tuple[str, str], ...] = (
    ("| plain | one | two |", "| plain | one | two |"),
    ("| escaped | x \\| y | two |", "| escaped | x \\| y | two |"),
    ("| code | `a|b` | two |", "| code | `a|b` | two |"),
    ("| code-escaped | `a\\|b` | two |", "| code-escaped | `a\\|b` | two |"),
    ("| double-code | ``a|b`` | two |", "| double-code | ``a|b`` | two |"),
    ("| two-codes | `a|b` | `c|d` |", "| two-codes | `a|b` | `c|d` |"),
    ("| math-in-code | `$|x|$` | two |", "| math-in-code | `$|x|$` | two |"),
    ("| code-in-math | $`a|b`$ | two |", "| code-in-math | $`a|b`$ | two |"),
    ("| math | $|x|$ | two |", "| math | $ | x |"),
    ("| math-escaped | $\\|x\\|$ | two |", "| math-escaped | $\\|x\\|$ | two |"),
    ("| display | $$|x|$$ | two |", "| display | $$ | x |"),
    ("| link-text | [a|b](https://e.com) | two |", "| link-text | [a | b](https://e.com) |"),
    ("| link-url | [t](https://e.com/a|b) | two |", "| link-url | [t](https://e.com/a | b) |"),
    ("| autolink | <https://e.com/a|b> | two |", "| autolink | <https://e.com/a|b> | two |"),
    ("| email | <a|b@e.com> | two |", "| email | <a|b@e.com> | two |"),
    ('| attribute | <a href="x|y">t</a> | two |', '| attribute | <a href="x|y">t</a> | two |'),
    ("| comment | <!-- a|b --> | two |", "| comment | <!-- a|b --> | two |"),
    ("| element | <code>a|b</code> | two |", "| element | <code>a | b</code> |"),
    ("| kbd | <kbd>a|b</kbd> | two |", "| kbd | <kbd>a | b</kbd> |"),
    ("| after-tag | a<br>b|c | two |", "| after-tag | a<br>b | c |"),
    ("| emphasis | *a|b* | two |", "| emphasis | *a | b* |"),
    ("| entity | a &#124; b | two |", "| entity | a &#124; b | two |"),
    ("| double-escape | a \\\\| b | two |", "| double-escape | a \\\\ | b |"),
    ("| unclosed | `x | y | two |", "| unclosed | `x | y |"),
    ("| code-backslash | `a\\`|b | two |", "| code-backslash | `a\\` | b |"),
    ("| less-than | a < b|c | two |", "| less-than | a < b | c |"),
    ("| fewer | only |", "| fewer | only |  |"),
    ("| more | one | two | three |", "| more | one | two |"),
    ("| empty | | two |", "| empty |  | two |"),
    ("| trailing-escape | one | two \\|", "| trailing-escape | one | two \\| |"),
    ("| no-trailing-bar | two | three", "| no-trailing-bar | two | three |"),
)
MEASURED_HEADER = "| Case | A | B |\n| --- | --- | --- |\n"
#: A file whose first table would lose a code span: the pinned formatter wrote it back
#: byte for byte on 2 November 2026, the prose it would retype and the second table's
#: row it would cut included, and exited 0.
UNTOUCHED = (
    'Prose with "straight quotes" and dots... that the formatter retypes.\n\n'
    "| Case | A |\n| --- | --- |\n| a | b | `y` |\n\n"
    "| Case | A |\n| --- | --- |\n| more | one | two |\n"
)


@cache
def _closing(run: int) -> re.Pattern[str]:
    """A backtick run of exactly `run`, which is what closes a code span opened by one."""
    return re.compile(rf"(?<!`)`{{{run}}}(?!`)")


def _bars(text: str) -> list[int]:
    """The offset of every `|` in `text` that separates cells."""
    bars: list[int] = []
    at = 0
    while token := _TOKEN.search(text, at):
        at = token.end()
        match token.group()[0]:
            case "`":
                # Inside a code span a backslash is text, so the first equal run closes it.
                if close := _closing(len(token.group())).search(text, at):
                    at = close.end()
            case "<":
                if html := _HTML.match(text, token.start()):
                    at = html.end()
            case "|":
                bars.append(token.start())
            case _:  # a backslash and the character it escapes
                pass
    return bars


def cells(row: str) -> list[str]:
    """The cells the pinned formatter reads in one table row, each stripped, before it
    pads or truncates them to the header's count."""
    text = row.strip()
    bars = _bars(text)
    lead = bool(bars) and bars[0] == 0
    trail = bool(bars) and bars[-1] == len(text) - 1 and (len(bars) > 1 or not lead)
    inner = bars[int(lead) : len(bars) - int(trail)]
    edges = [0 if lead else -1, *inner, len(text) - 1 if trail else len(text)]
    return [text[start + 1 : end].strip() for start, end in pairwise(edges)]


def _unwrapped(line: str) -> str:
    """`line` without the block-quote markers or indentation that hold its table."""
    return line.lstrip(_CONTAINER)


def _delimiter_width(line: str) -> int | None:
    text = _unwrapped(line).strip()
    if "|" not in text or _DELIMITER.fullmatch(text) is None:
        return None
    return len(cells(text))


def lossy_rows(text: str) -> list[tuple[int, int, list[str]]]:
    """Each table row with more cells than its header, as (its 1-based line, the header's
    cell count, the row's cells), outside fenced code and the YAML frontmatter."""
    lines = text.splitlines()
    found: list[tuple[int, int, list[str]]] = []
    i = 0
    if lines and lines[0].strip() == "---":
        i = next(
            (at + 1 for at in range(1, len(lines)) if lines[at].strip() in {"---", "..."}), 0
        )
    fence = ""
    while i < len(lines):
        line = _unwrapped(lines[i])
        if fence:
            if line.strip().startswith(fence) and not line.strip().strip(fence[0]):
                fence = ""
            i += 1
            continue
        if opened := _FENCE.match(line):
            fence = opened["fence"]
            i += 1
            continue
        width = _delimiter_width(lines[i + 1]) if "|" in line and i + 1 < len(lines) else None
        if width is None or len(cells(line)) != width:
            i += 1
            continue
        i += 2
        while i < len(lines) and (row := _unwrapped(lines[i]).strip()):
            if _FENCE.match(row):
                break
            # A row between an opening and a closing bar holds at most one cell fewer than
            # it has bars, so a row with no extra bar needs no parse: most rows.
            bounded = row[0] == row[-1] == "|" and row.count("|") - 1 <= width
            if not bounded and len(read := cells(row)) > width:
                found.append((i + 1, width, read))
            i += 1
    return found


def scope(root: Path = REPO, *, untracked: bool = False) -> list[str]:
    """The tracked Markdown the formatter rewrites, repository-relative; with `untracked`,
    the Markdown git does not ignore as well, which is all the hook's formatter walks."""
    ignored = flowmark_exclusions(root)
    vendored = vendored_directories(root)
    return [
        path
        for path in tracked_markdown(root, untracked=untracked)
        if not excluded_by(path, ignored)
        and not any(path.startswith(f"{directory}/") for directory in vendored)
    ]


def _quoted(found: Sequence[str]) -> str:
    return " | ".join(f"`{cell}`" for cell in found)


def check(root: Path = REPO, *, untracked: bool = False) -> tuple[list[str], int]:
    """Each row the formatter would cut, as a line naming its file and line, and the
    number of files read."""
    problems: list[str] = []
    paths = scope(root, untracked=untracked)
    for path in paths:
        text = (root / path).read_text(encoding="utf-8")
        if "|" not in text:
            continue
        problems.extend(
            f"{path}:{line}: a row of {len(found)} cells under a header of {width}; the "
            f"formatter keeps {_quoted(found[:width])} and drops {_quoted(found[width:])}, "
            "or leaves the whole file unformatted when a dropped cell holds code or math, "
            "and GitHub shows the row cut either way -- write each `|` that belongs inside "
            "a cell as `\\|`, or as `\\lvert` and `\\rvert` in math"
            for line, width, found in lossy_rows(text)
        )
    return problems, len(paths)


def _formatted(text: str, command: Sequence[str]) -> str:
    with tempfile.TemporaryDirectory(prefix="check-table-cells-") as directory:
        source = Path(directory) / "measured.md"
        source.write_text(text, encoding="utf-8")
        return format_copy(source, list(command))


def measure(command: Sequence[str]) -> list[str]:
    """Format `MEASURED` and `UNTOUCHED` with `command` and name each row written back
    differently from the record, and `UNTOUCHED` if it is no longer left whole."""
    lines = _formatted(
        MEASURED_HEADER + "".join(f"{written}\n" for written, _ in MEASURED), command
    ).splitlines()
    delimiter = MEASURED_HEADER.splitlines()[1]
    rows = lines[lines.index(delimiter) + 1 :] if delimiter in lines else []
    if len(rows) != len(MEASURED):
        return [f"the formatter wrote back {len(rows)} rows of {len(MEASURED)}"]
    differ = [
        f"{written!r}: recorded {formatted!r}, now {got!r}"
        for (written, formatted), got in zip(MEASURED, rows, strict=True)
        if got != formatted
    ]
    if (untouched := _formatted(UNTOUCHED, command)) != UNTOUCHED:
        differ.append(f"UNTOUCHED: recorded unchanged, now {untouched!r}")
    return differ


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_table_cells",
        description="Refuse a Markdown table row the pinned formatter would cut short.",
    )
    parser.add_argument("--root", type=Path, default=REPO, help=argparse.SUPPRESS)
    parser.add_argument(
        "--measure",
        action="store_true",
        help="format the measured rows with the Makefile's pinned formatter and compare",
    )
    parser.add_argument(
        "--untracked",
        action="store_true",
        help="also read Markdown git does not ignore, as the hook's formatter does",
    )
    arguments = parser.parse_args(argv)
    root: Path = arguments.root
    started = time.perf_counter()
    if arguments.measure:
        command = shlex.split(pinned_formatter(root / "Makefile"))
        differ = measure(command)
        for line in differ:
            print(f"  DIFFERS {line}")
        print(
            f"  {len(MEASURED) + 1 - len(differ)} of {len(MEASURED) + 1} measurements (the "
            f"rows and the untouched file, recorded with {MEASURED_WITH}) agree with "
            f"{' '.join(command)}"
        )
        return 1 if differ else 0
    problems, files = check(root, untracked=arguments.untracked)
    for problem in problems:
        print(f"  FAIL {problem}")
    elapsed = time.perf_counter() - started
    if problems:
        print(
            f"FAIL {len(problems)} table row(s) the formatter would cut short "
            f"({files} files, {elapsed:.2f}s); see think-7y5x",
            file=sys.stderr,
        )
        return 1
    print(f"  ok  no table row the formatter would cut short ({files} files, {elapsed:.2f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
