"""Controls for the math-span counter behind the formatter-pin check.

The tool's claim -- that the pinned formatter leaves every `$...$` span whole -- is only
as good as its idea of what a span is. Miscount, and a clean report means nothing. So the
counter is pinned here against the four cases that decide it: a span containing a comma
(the character a rewrapper is most likely to break a line on), a multi-line `$$...$$`
block whose delimiters must not be read as two inline pairs, math inside a fence that is
code rather than a formula, and a lone `$` that is currency.

The formatter itself is never invoked: it is a pinned `uvx` runner, so calling it would
put a network fetch inside the fast test suite. Reading the pin out of the Makefile is
checked here; running it is what the tool does.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from devtools.check_math_spans import (
    MAKEFILE,
    FileResult,
    mask_fences,
    math_spans,
    pinned_formatter,
)

SAMPLE = textwrap.dedent(
    """
    An inline span with a comma: $s_1, s_2 \\in [0, 1]$ and some following prose.

    $$
    \\sum_{i=1}^{n} a_i \\le \\frac{n}{2}
    $$

    A fenced block whose dollars are shell, not math:

    ```bash
    echo $HOME
    awk '{print $1, $2}' file
    ```

    Inline code with a dollar too: `echo $PATH`.

    A lone dollar in prose: the bound costs $5 to state and nothing to check.
    """
).strip()


def test_counts_one_inline_span_and_one_display_block() -> None:
    spans = math_spans(SAMPLE)
    assert len(spans) == 2
    display, inline = spans
    assert display.strip() == "\\sum_{i=1}^{n} a_i \\le \\frac{n}{2}"
    assert inline == "s_1, s_2 \\in [0, 1]"


def test_display_delimiters_are_not_read_as_inline_pairs() -> None:
    """`$$a$$` is one span, not two inline ones sharing the middle text."""
    assert math_spans("$$a + b$$") == ["a + b"]


def test_fenced_and_inline_code_dollars_are_not_math() -> None:
    """The sample's shell dollars would otherwise pair into spurious spans."""
    fenced = "```\n$x$ and $y$\n```\n"
    assert math_spans(fenced) == []
    assert math_spans("Use `$x$` here.") == []


def test_unclosed_fence_masks_to_end_of_file() -> None:
    """What a Markdown parser does, so what the counter must do."""
    assert math_spans("~~~\n$x$\nstill inside $y$\n") == []
    assert mask_fences("```\n$x$\n").strip() == ""


def test_lone_dollar_is_not_a_span() -> None:
    assert math_spans("costs $5 to state") == []


def test_two_prose_dollars_do_pair_which_is_why_the_measure_is_a_difference() -> None:
    """A known over-count, recorded rather than papered over.

    Two currency amounts in one paragraph read as one span, because nothing in the text
    distinguishes them from math. It does not weaken the check: the tool compares the
    same scan before and after formatting, so a span the counter invents is compared
    against itself and only reports if the formatter changed it.
    """
    assert math_spans("$5 and $6 are prices, not math") == ["5 and "]


def test_result_is_clean_only_when_nothing_moved() -> None:
    clean = FileResult(MAKEFILE, before=12, after=12, broken=0, changed=0)
    assert clean.ok
    assert "ok" in clean.line()
    for damaged in (
        FileResult(MAKEFILE, before=12, after=11, broken=0, changed=0),
        FileResult(MAKEFILE, before=12, after=12, broken=1, changed=1),
        FileResult(MAKEFILE, before=12, after=12, broken=0, changed=1),
    ):
        assert not damaged.ok
        assert "FAIL" in damaged.line()


def test_pin_is_read_from_the_makefile() -> None:
    """One statement of the pin: this tool must measure what `make format` runs."""
    command = pinned_formatter()
    assert "flowmark" in command
    assert command in MAKEFILE.read_text(encoding="utf-8")


def test_missing_pin_fails_loudly(tmp_path: Path) -> None:
    """A Makefile without the pin line is a hard stop, not a silent default."""
    makefile = tmp_path / "Makefile"
    makefile.write_text("format:\n\techo nothing\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="FLOWMARK"):
        pinned_formatter(makefile)
