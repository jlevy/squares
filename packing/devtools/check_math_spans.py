#!/usr/bin/env python3
"""Prove the pinned Markdown formatter keeps every math span whole.

Flowmark rewraps prose. A rewrap that landed a line break inside a `$...$` span would
defeat `grep`, which is the entire point of keeping the literature archive locally, and
several Markdown math renderers require inline math to stay on one line. The pinned
`flowmark-rs==0.4.0` keeps every one of the archive's 7,618 spans whole; the archive is
excluded in `.flowmarkignore` for other reasons, stated there and in `AGENTS.md`, and
every exclusion there is evidence-based rather than precautionary.

Evidence-based means re-measurable, and a measurement without its instrument is the
failure mode `OR-1` names. This is the instrument: it formats a *copy* of each file with
the pinned formatter and compares the math spans before and after, so "0 of 7,618 spans
break" is a command rather than a memory, and the next pin bump has something to run.

What it counts, in this order, so that a delimiter is never claimed twice:

1. Fenced code blocks and inline code spans are masked out. `$` inside them is shell
   syntax or a literal, not math, and formatters leave code alone anyway.
2. `$$...$$` display blocks.
3. `$...$` inline spans, where neither delimiter is adjacent to another `$`.

A span is *changed* when its content differs after formatting, and *broken* when that
difference introduced a newline -- broken spans are a subset of changed ones, and are
called out separately because they are the specific damage the exclusion exists to
prevent. A change in the number of spans is its own failure: it means a delimiter moved,
so the before and after spans can no longer be paired at all.

The pinned formatter command is read from the `FLOWMARK :=` line of the repository
`Makefile`, so the pin is stated once and this tool cannot drift from `make format`.

Usage, from `packing/`:

    uv run --frozen --group dev python -m devtools.check_math_spans FILE...
    uv run --frozen --group dev python -m devtools.check_math_spans \\
        --flowmark "uvx --from flowmark-rs==0.4.0 flowmark" FILE...

Exits 1 if any span broke, changed, or appeared or vanished; 2 if the pin cannot be read
or the formatter fails. The given files are only ever read.
"""

from __future__ import annotations

import argparse
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
MAKEFILE = REPO / "Makefile"

# The pin, stated once in the Makefile and read from there rather than repeated here.
PIN = re.compile(r"^FLOWMARK\s*:=\s*(?P<command>.+?)\s*$", re.MULTILINE)

# A fenced code block opener: three or more backticks or tildes, indented at most three
# spaces. The fence closes on a line of at least as many of the same character.
FENCE_OPEN = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})")
# Inline code: a run of backticks closed by a run of the same length.
INLINE_CODE = re.compile(r"(?P<ticks>`+)(?!`).*?(?<!`)(?P=ticks)(?!`)", re.DOTALL)
# Display math, taken before inline so its delimiters are never read as an inline pair.
DISPLAY = re.compile(r"\$\$(?P<body>.*?)\$\$", re.DOTALL)
# Inline math: a single `$` not adjacent to another `$`, up to the next such `$`.
INLINE = re.compile(r"(?<!\$)\$(?!\$)(?P<body>[^$]+?)(?<!\$)\$(?!\$)", re.DOTALL)


def _blank(text: str) -> str:
    """`text` with every character but its newlines replaced by a space."""
    return re.sub(r"[^\n]", " ", text)


def _mask(text: str, pattern: re.Pattern[str]) -> str:
    """Blank every match to spaces, preserving length so later offsets still line up."""
    return pattern.sub(lambda match: _blank(match.group(0)), text)


def mask_fences(text: str) -> str:
    """Blank the body and delimiters of every fenced code block, line by line.

    Line-by-line rather than by one big regex because the closing rule is positional --
    a fence closes on the first later line whose run of the same character is at least as
    long -- and an unclosed fence runs to end of file, as it does in a Markdown parser.
    """
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    fence: str | None = None
    for line in lines:
        if fence is None:
            opened = FENCE_OPEN.match(line)
            if opened is None:
                out.append(line)
                continue
            fence = opened.group("fence")
            out.append(_blank(line))
            continue
        out.append(_blank(line))
        closing = FENCE_OPEN.match(line)
        if closing is not None and closing.group("fence").startswith(fence):
            fence = None
    return "".join(out)


def math_spans(text: str) -> list[str]:
    """The content of every math span in `text`, display blocks first, then inline.

    Code is masked before either pass: `$5` in a shell example is not a formula, and a
    formatter will not touch it in any case.
    """
    masked = _mask(mask_fences(text), INLINE_CODE)
    display = [match.group("body") for match in DISPLAY.finditer(masked)]
    inline = [match.group("body") for match in INLINE.finditer(_mask(masked, DISPLAY))]
    return display + inline


@dataclass(frozen=True)
class FileResult:
    """One file's before/after span comparison."""

    path: Path
    before: int
    after: int
    broken: int
    changed: int

    @property
    def ok(self) -> bool:
        return self.before == self.after and self.broken == 0 and self.changed == 0

    def line(self) -> str:
        flag = "ok" if self.ok else "FAIL"
        return (
            f"  {self.path.as_posix():<62s} {self.before:>6d} {self.after:>6d} "
            f"{self.broken:>6d} {self.changed:>7d}  {flag}"
        )


def pinned_formatter(makefile: Path = MAKEFILE) -> str:
    """The formatter command pinned in the Makefile, or a loud failure."""
    if not makefile.is_file():
        message = f"no Makefile at {makefile}: cannot read the pinned formatter"
        raise SystemExit(message)
    match = PIN.search(makefile.read_text(encoding="utf-8"))
    if match is None:
        message = (
            f"no `FLOWMARK :=` line in {makefile}: the pin this tool measures against is "
            "stated there and nowhere else"
        )
        raise SystemExit(message)
    return match.group("command")


def format_copy(path: Path, command: list[str]) -> str:
    """Format a copy of `path` in a temporary directory and return the result.

    The original is never touched, and the copy is deliberately outside the repository:
    flowmark reads `.flowmarkignore` relative to its target, so a copy left in place
    would be skipped by exactly the exclusion this tool exists to justify.
    """
    with tempfile.TemporaryDirectory(prefix="check-math-spans-") as directory:
        copy = Path(directory) / path.name
        shutil.copyfile(path, copy)
        completed = subprocess.run(
            [*command, "--auto", str(copy)],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            message = (
                f"formatter failed on {path.as_posix()} "
                f"(exit {completed.returncode}): {completed.stderr.strip()}"
            )
            raise SystemExit(message)
        return copy.read_text(encoding="utf-8")


def check_file(path: Path, command: list[str]) -> FileResult:
    """Compare one file's math spans before and after the pinned formatter."""
    before = math_spans(path.read_text(encoding="utf-8"))
    after = math_spans(format_copy(path, command))
    changed = 0
    broken = 0
    for old, new in zip(before, after, strict=False):
        if old == new:
            continue
        changed += 1
        if "\n" in new and "\n" not in old:
            broken += 1
    return FileResult(path, len(before), len(after), broken, changed)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_math_spans",
        description="Check that the pinned Markdown formatter keeps math spans whole.",
    )
    parser.add_argument("files", nargs="+", type=Path, metavar="FILE")
    parser.add_argument(
        "--flowmark",
        default=None,
        metavar="COMMAND",
        help="formatter command to measure (default: the Makefile's FLOWMARK pin)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    command = shlex.split(arguments.flowmark or pinned_formatter())
    print(f"formatter: {' '.join(command)}")
    print(f"  {'file':<62s} {'before':>6s} {'after':>6s} {'broken':>6s} {'changed':>7s}")

    results: list[FileResult] = []
    for given in arguments.files:
        path = Path(given)
        if not path.is_file():
            print(f"  no such file: {path.as_posix()}", file=sys.stderr)
            return 2
        result = check_file(path, command)
        results.append(result)
        print(result.line())

    spans = sum(result.before for result in results)
    broken = sum(result.broken for result in results)
    changed = sum(result.changed for result in results)
    moved = sum(1 for result in results if result.before != result.after)
    print(
        f"  total: {spans} spans across {len(results)} files, "
        f"{broken} broken, {changed} changed, {moved} files with a span-count change"
    )
    if broken or changed or moved:
        print("  math spans do not survive the pinned formatter", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
