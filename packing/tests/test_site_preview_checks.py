"""The site preview's layout checks, on reports shaped as its probes return them.

`devtools.preview_site` fails a built page on what its probes find, and
`devtools.measure_site_pages cards` prints the same card report as a table, as `space`
does the space around tables and headings and `columns` the columns of the data tables.
All read a probe's output in Python, so the decisions are tested here without a browser.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import render_overview
from devtools.measure_site_pages import (
    card_rows,
    chip_rows,
    column_rows,
    markdown_table,
    space_rows,
)
from devtools.preview_site import (
    LONG_TOKEN,
    SCHEMES,
    SCROLLBAR_PX,
    baseline_problems,
    clip_problem,
    motion_for,
    moved_links,
    off_centre,
    shot_name,
    shot_stem,
    split_problem,
    tabs_problems,
    type_problems,
)


def _section(*rows: tuple[int, float, float]) -> dict[str, object]:
    return {
        "section": "Squares Project Documentation",
        "block_width": 1104,
        "rows": [
            {"cards": n, "sizes": [""] * n, "widths": [264] * n, "start": a, "end": b}
            for n, a, b in rows
        ],
        "headlines": [],
    }


def test_a_row_off_the_centre_of_its_line_is_reported() -> None:
    """A full line and a centred partial line pass; a partial line hanging to the start,
    as a grid's last row does, is named with its two slacks."""
    report = [_section((4, 0, 0), (2, 280, 280), (2, 0, 560))]
    assert off_centre(report) == [
        (
            "a row of 2 cards in Squares Project Documentation is off centre: "
            "0px before it, 560px after"
        )
    ]


def test_a_rounding_pixel_is_not_off_centre() -> None:
    assert off_centre([_section((3, 140, 140.9))]) == []


def test_the_card_table_has_one_line_a_row() -> None:
    report = [{"page": "index.html", "width": 1280, **_section((4, 0, 0), (2, 280, 280))}]
    rows = card_rows(report)
    assert [row["row"] for row in rows] == [1, 2]
    assert rows[1]["widths"] == "264 264"
    assert rows[1]["sizes"] == "- -"
    assert (rows[1]["start"], rows[1]["end"]) == (280, 280)


def _table(above: float, below: float, **over: object) -> dict[str, object]:
    return {
        "page": "index.html",
        "width": 1280,
        "state": "page",
        "kind": "table",
        "table": "table.site-table",
        "section": "Recent Results",
        "component": "div.site-table-wrap",
        "bar": True,
        "above": above,
        "above_to": "p",
        "below": below,
        "below_to": "p.site-more",
        **over,
    }


def _heading(role: str, above: float, below: float, **over: object) -> dict[str, object]:
    return {
        "page": "index.html",
        "width": 1280,
        "state": "page",
        "kind": "heading",
        "role": role,
        "text": "Recent Results",
        "size": 21.6,
        "line_height": 24.8,
        "leading": 1.15,
        "lines": 1,
        "overflow": 0,
        "clips": False,
        "above": above,
        "above_to": "p",
        "below": below,
        "below_to": "p",
        **over,
    }


def test_the_space_table_has_one_line_a_table_and_one_a_heading_role() -> None:
    """Tables come first, each on its own line; headings of one role on one page at one
    width share a line that gives the least and most space found, the most lines one
    takes, and what a clipping box cannot show."""
    report = [
        _heading("h2", 48.6, 27.2),
        _table(32, 32),
        _heading("h2", 48.6, 32, lines=2),
        _heading("span.site-card-value", 3.2, 3.2, overflow=4, clips=True, lines=3),
        _heading("span.site-card-value", 3.2, 3.2, overflow=9, clips=False),
    ]
    rows = space_rows(report)
    assert [row["what"] for row in rows] == [
        "div.site-table-wrap with bar",
        "h2",
        "span.site-card-value",
    ]
    table, section, headline = rows
    assert (table["above"], table["below"], table["where"]) == ("32", "32", "Recent Results")
    assert (section["count"], section["above"], section["below"]) == (2, "48.6", "27.2 to 32")
    assert (section["leading"], section["lines"], section["overflow"]) == ("1.15", 2, 0)
    # Only a box that hides its overflow counts as clipping what it cannot show.
    assert (headline["lines"], headline["overflow"]) == (3, 4)
    assert markdown_table(report).splitlines()[0].startswith("| page | width | state | what |")


def test_the_columns_table_has_one_line_a_column() -> None:
    """Each column of each table is a line: its width and share of the table, the widest
    content a cell holds, the most lines a cell takes, how many words a line break
    splits, and the tallest row it sets, a dash where it sets none. A column that is not
    shown has no width."""
    report: list[dict[str, object]] = [
        {
            "page": "all-results.html",
            "width": 1280,
            "table": "site-table.site-results",
            "section": "Every Result",
            "layout": "table",
            "table_width": 1104,
            "frame_width": 1104,
            "scrolls": 0,
            "shown_rows": 61,
            "top": 400,
            "height": 8423,
            "tallest_row": {"row": "t-056", "height": 385.6},
            "columns": [
                {
                    "column": "Result",
                    "width": 412.8,
                    "held": 396.8,
                    "held_by": "t-033",
                    "overflows": [{"row": "t-019", "by": 3.2}],
                    "lines": 3,
                    "broken": [],
                    "tallest": None,
                },
                {
                    "column": "Credit",
                    "width": 102.6,
                    "lines": 9,
                    "broken": ["Ahmed", "Guzhou0806"],
                    "tallest": {"row": "t-048", "height": 238.8, "lines": 9},
                },
                {
                    "column": "site-records",
                    "width": None,
                    "lines": 3,
                    "broken": [],
                    "tallest": None,
                },
            ],
        }
    ]
    result, credit, cards = column_rows(report)
    assert (result["col_width"], result["share"], result["tallest_row"]) == (
        "412.8",
        "37%",
        "-",
    )
    assert (credit["col_width"], credit["share"], credit["max_lines"]) == ("102.6", "9%", 9)
    # The widest content a cell holds and the row that holds it, where the report has
    # them, and how many cells show something past their own box.
    assert (result["held"], credit["held"]) == ("396.8", "-")
    assert (result["held_by"], credit["held_by"]) == ("t-033", "-")
    assert (result["overflows"], credit["overflows"]) == (1, 0)
    assert (credit["broken_words"], credit["tallest_row"]) == (2, "t-048")
    assert (credit["row_height"], credit["its_lines"]) == ("238.8", 9)
    assert (credit["table"], credit["past_frame"], credit["shown"]) == ("1104", "0", 61)
    assert (cards["col_width"], cards["share"]) == ("-", "-")
    head = markdown_table(report).splitlines()[0]
    assert head.startswith("| page | width | section | layout | shown | table | past_frame |")


def test_the_chips_table_has_one_line_a_kind_of_chip_on_a_surface() -> None:
    """Chips of one kind on one surface share a line that gives how many there are, the
    distinct sizes found, the most lines one takes, and the words of each that wraps."""

    def chip(kind: str, text: str, block: float, lines: int) -> dict[str, object]:
        return {
            "page": "all-results.html",
            "width": 1280,
            "state": "page",
            "chip": kind,
            "text": text,
            "surface": "table",
            "font_size": 17.5,
            "line_height": 25.3,
            "inline_size": 98,
            "block_size": block,
            "lines": lines,
            "white_space": "normal",
        }

    report = [
        chip("rung", "S5", 25.3, 1),
        chip("standing", "superseded", 25.3, 1),
        chip("standing", "current best", 50.7, 2),
        chip("standing", "current best", 50.7, 2),
    ]
    rungs, standing = chip_rows(report)
    # A chip's own width is its `inline_size`, so `width` stays the window's.
    assert (rungs["width"], standing["width"]) == (1280, 1280)
    assert (rungs["chip"], rungs["count"], rungs["block_size"], rungs["wrapped"]) == (
        "rung",
        1,
        "25.3",
        "-",
    )
    assert (standing["count"], standing["font_size"], standing["block_size"]) == (
        3,
        "17.5",
        "25.3 50.7",
    )
    assert (standing["max_lines"], standing["wrapped"]) == (2, "current best")
    head = markdown_table(report).splitlines()[0]
    assert head.startswith("| page | width | state | surface | chip | count | font_size |")


def test_a_heading_with_no_resolved_line_height_still_has_a_line() -> None:
    row = _heading("h1", 64, 20, line_height="normal", leading=None, lines=None)
    (only,) = space_rows([row])
    assert (only["line_height"], only["leading"], only["lines"]) == ("", "", 0)


def test_a_clipped_block_is_named_with_how_far_it_runs_past_each_side() -> None:
    """The preview reports a wide block an ancestor cuts off by naming both, each side
    it runs past, and whether it took a scrollbar's width to show it."""
    cut = {"block": "div.site-table-wrap", "frame": "article.kpress", "left": 7.5, "right": 7.5}
    assert clip_problem(cut, scrollbar=SCROLLBAR_PX) == (
        "div.site-table-wrap runs 7.5px past its left edge and 7.5px past its right edge of "
        "article.kpress, which clips it, with a 15px scrollbar"
    )
    count = {"block": "span.site-count", "frame": "article.kpress", "left": 0, "right": 16}
    assert clip_problem(count) == (
        "span.site-count runs 16px past its right edge of article.kpress, which clips it"
    )


def test_a_shot_is_named_for_its_page_and_fragment() -> None:
    assert shot_stem("index.html") == "index"
    assert shot_stem("workbench/index.html") == "workbench"
    assert shot_stem("cases/index.html#n-11") == "cases-n-11"
    assert shot_stem("frontier.html#n-11") == "frontier-n-11"
    assert shot_stem("papers/n11-optimality-review.html") == "papers-n11-optimality-review"


def test_a_shot_is_named_for_its_width_scheme_and_press() -> None:
    """A light shot keeps the name it always had; a dark one says so after the width,
    and a press shot ends in its press, after the scheme."""
    assert shot_name("index.html", 1280) == "index-1280.png"
    assert shot_name("index.html", 390, "light") == "index-390.png"
    assert shot_name("index.html", 390, "dark") == "index-390-dark.png"
    assert shot_name("frontier.html", 1280, "dark", 1) == "frontier-1280-dark-press1.png"
    assert shot_name("cases/index.html#n-11", 1280, "light", 2) == "cases-n-11-1280-press2.png"
    assert SCHEMES == ("light", "dark")


def _header(*, rule: tuple[float, float] | None, tabs: tuple[float, float] | None) -> dict:
    """A `preview_site/header` report: the bar from 16 to 68.59, the rule and the tabs as
    given, each a top and a bottom, and the film 64px under whichever ends lower."""
    foot = max([68.59, *(part[1] for part in (rule, tabs) if part)])
    return {
        "nav": {"top": 16, "bottom": 68.59},
        "rule": rule and {"top": rule[0], "bottom": rule[1], "on": "nav.site-nav"},
        "tabs": tabs and {"top": tabs[0], "bottom": tabs[1], "current": "Film"},
        "first": {"top": foot + 64, "bottom": 900, "block": "figure.site-film-frame"},
    }


def test_section_tabs_under_the_bars_rule_pass_and_tabs_over_it_are_reported() -> None:
    """From the top a page of a section reads bar, rule, tabs, content. Tabs standing
    above the rule, as they did while the rule was the foot of the header that holds
    them, are named with how far; a page with no tabs has nothing to check."""
    assert tabs_problems(_header(rule=(67.59, 68.59), tabs=(79.78, 112.38))) == []
    assert tabs_problems(_header(rule=(67.59, 68.59), tabs=None)) == []
    over = _header(rule=(113.77, 114.77), tabs=(69.98, 102.58))
    over["rule"]["on"] = "header"
    assert tabs_problems(over) == [
        (
            "the section tabs start 44.79px above the foot of the rule under the "
            "navigation bar, which is on header"
        )
    ]
    assert tabs_problems(_header(rule=None, tabs=(79.78, 112.38))) == [
        "the section tabs have no rule over them, under the navigation bar"
    ]
    under = _header(rule=(67.59, 68.59), tabs=(79.78, 112.38))
    under["first"]["top"] = 100.38
    assert tabs_problems(under) == [
        "figure.site-film-frame starts 12px above the foot of the section tabs"
    ]


#: The paper's scale as a page resolves it: the prose base, the sans base beside it, and
#: the three steps under the sans base.
SCALE = {"prose": 18, "sans": 19, "support": 18.05, "note": 17.48, "colophon": 16.15}


def _type(link: float | None, tab: float | None, name: float | None = 19) -> dict:
    """A `preview_site/header` report's type: a link's size, a tab's and the name's."""
    return {"type": {"body": 18, "name": name, "link": link, "tab": tab, "scale": SCALE}}


def test_the_bars_type_is_one_step_under_the_bodys_and_no_more() -> None:
    """A link in the bar and a section tab are under the prose base and no smaller than
    the first step of the scale under it, whatever those are in pixels; the two are one
    size; and the site's name is at least the body's. The sizes the bar had, 16px links
    and 14.4px tabs under a 16px name, are each named."""
    assert type_problems(_type(17.48, 17.48)) == []
    assert type_problems(_type(17.48, None)) == []
    assert type_problems(_type(None, None, None)) == []
    unscaled = _type(17.48, None)
    unscaled["type"]["scale"] = None
    assert type_problems(unscaled) == []
    wide = "it should be under the body's 18px and no smaller than the step below it, 17.48px"
    assert type_problems(_type(16, 14.4, 16)) == [
        f"a link in the header is 16px: {wide}",
        f"a tab in the header is 14.4px: {wide}",
        "a section tab is 14.4px and a link in the bar 16px",
        "the site's name is 16px, under the body's 18px",
    ]
    # The support size is a step of the scale, but not one under the body.
    assert type_problems(_type(18.05, 18.05)) == [
        f"a link in the header is 18.05px: {wide}",
        f"a tab in the header is 18.05px: {wide}",
    ]
    # A body of another size moves the step with it.
    larger = _type(18.05, 18.05, 20)
    larger["type"]["scale"] = {**SCALE, "prose": 19}
    assert type_problems(larger) == []


def _split(*pieces: str, **over: object) -> dict[str, object]:
    return {
        "word": "".join(pieces),
        "pieces": list(pieces),
        "host": "dd",
        "block": "dd",
        "code": False,
        "prose": False,
        "width": 40.0,
        "line": 320.0,
        "frame": "",
        **over,
    }


def test_a_word_cut_between_two_letters_is_reported() -> None:
    """What `overflow-wrap: anywhere` does to a label in a column squeezed narrower than
    the word: the break falls between two letters, and the report names the pieces, the
    element, and the word's width against the line it was set on."""
    squeezed = _split("low", "er", host="span.site-atlas-pop-which", block="p", line=24.0)
    assert split_problem(squeezed) == (
        '"low | er" is one word on 2 lines in span.site-atlas-pop-which in p: '
        "40px wide on a 24px line"
    )
    letters = _split("l", "o", "w", "e", "r", line=8.0)
    assert split_problem(letters) == (
        '"l | o | w | e | r" is one word on 5 lines in dd: 40px wide on a 8px line'
    )
    digits = _split("3.8770", "8359", width=70.0, line=48.0)
    assert split_problem(digits) is not None


def test_a_name_cut_at_its_hyphen_is_reported_where_the_site_sets_it() -> None:
    """An evidence identifier is one word: a line that ends on one of its hyphens, in a
    popover or a block the site builds, is reported, a framed page's named with its
    frame. The same break in a document's own prose is KPress's and passes."""
    name = _split("E-nagamochi-", "lower", host="code", code=True, width=144.8, line=518.0)
    assert split_problem(name) == (
        '"E-nagamochi- | lower" is one word on 2 lines in code in dd: '
        "144.8px wide on a 518px line"
    )
    framed = split_problem({**name, "block": "p", "frame": "iframe.site-popover-frame"})
    assert framed is not None
    assert "in code in p, framed in iframe.site-popover-frame: 144.8px wide" in framed
    assert split_problem({**name, "prose": True}) is None


def test_an_ordinary_break_is_not_a_split_word() -> None:
    """Running text ends a line on the hyphen of a compound, a path on its slash, and a
    formula written in characters at a bracket; none of them cuts a word."""
    assert split_problem(_split("computer-", "assisted")) is None
    assert split_problem(_split("docs/project/", "reviews", host="code", code=True)) is None
    assert split_problem(_split("T=", "(6u+4)/(1+2u-u^2),")) is None
    assert split_problem(_split("280af3d4\u2026", "e6e5", host="code", code=True)) is None


def test_a_long_token_wider_than_its_line_may_break() -> None:
    """An exact decimal or an identifier of `LONG_TOKEN` characters or more that cannot
    fit on one line has to break somewhere; one that would have fitted does not, and
    neither does anything shorter, however narrow its column."""
    decimal = "3.8770835900228141773078970601009"
    assert len(decimal) >= LONG_TOKEN
    cut = _split(decimal[:-1], decimal[-1], width=283.0, line=270.0)
    assert split_problem(cut) is None
    assert split_problem({**cut, "line": 300.0}) is not None
    name = _split("E-n011-global-optimality-", "independent", host="code", code=True)
    assert split_problem({**name, "width": 317.0, "line": 300.0}) is None
    assert split_problem({**name, "width": 317.0, "line": 518.0}) is not None
    short = _split("E-nagamochi-", "lower", host="code", code=True, width=155.0, line=120.0)
    assert len("E-nagamochi-lower") < LONG_TOKEN
    assert split_problem(short) is not None


def test_the_popover_table_has_one_line_a_popover_with_its_count_of_split_words() -> None:
    """`measure_site_pages popover` prints a popover's box, margins and visible share on
    one line; the broken words themselves are a list, which the JSON report keeps."""
    row = {
        "page": "frontier.html",
        "width": 1280,
        "press": 'a[data-case="79"]',
        "popover": "#pop-case",
        "window_height": 1200,
        "inline": 736,
        "block": 896,
        "above": 152,
        "below": 152,
        "beside": 272,
        "scrolls": "its frame",
        "shown": 710,
        "content": 3070,
        "share": 0.23,
        "split_words": 1,
        "split": ['"E-nagamochi- | lower" is one word on 2 lines in code in dd'],
    }
    head, _, line = markdown_table([row]).splitlines()
    assert head.endswith("| shown | content | share | split_words |")
    assert line.endswith("| its frame | 710 | 3070 | 0.23 | 1 |")


def _labels(
    *lines: tuple[int, float], name: float | None = 46.8, tabs: float | None = None
) -> dict:
    """A `preview_site/baselines` report: two links on each line of the bar, a line given
    as its top and its baseline, the name's baseline, and two tabs on one of theirs. The
    name's line is 25px tall, with the mark centred on it."""
    words = iter(("Overview", "Results", "Papers", "Frontier"))
    return {
        "name": name,
        "name_text": name and {"top": name - 18, "bottom": name + 7},
        "logo": {"top": 32.3, "bottom": 50.3},
        "links": [
            {"label": next(words), "baseline": baseline, "top": top, "current": False}
            for top, baseline in lines
            for _ in range(2)
        ],
        "tabs": [
            {"label": label, "baseline": tabs, "top": 80, "current": label == "Film"}
            for label in (("Film", "Workbench") if tabs else ())
        ],
    }


def test_the_name_and_the_links_stand_on_one_baseline() -> None:
    """The site's name stands on the baseline of the bar's first line of links, within
    half a pixel, and so does each link beside another; a bar that wraps has a baseline
    a line. A name set above the links, as it was while the bar's baseline was the foot
    of its mark, is named with how far; where the name's text is not shown there is
    nothing to hold it to."""
    assert baseline_problems(_labels((25, 46.8))) == []
    assert baseline_problems(_labels((25, 46.8), name=47.2, tabs=102.58)) == []
    assert baseline_problems(_labels((22, 40.78), (50, 68.28), name=None, tabs=119.77)) == []
    assert baseline_problems(_labels((29, 51.3), name=47.8)) == [
        "the site's name stands -3.5px off the baseline of the bar's links",
        "the site's mark is centred -1px off the middle of its name's line",
    ]
    uneven = _labels((25, 46.8), tabs=102.58)
    uneven["links"][1]["baseline"] = 48.0
    uneven["tabs"][1]["baseline"] = 101.5
    assert baseline_problems(uneven) == [
        "the link Results stands +1.2px off the baseline of Overview, beside it",
        "the section tab Workbench stands -1.08px off the baseline of Film, beside it",
    ]


def test_only_a_page_that_starts_a_film_is_opened_under_reduced_motion() -> None:
    """The film's page is opened as for a reader who asks for reduced motion, with any
    fragment, so no tool starts its download; every other page is opened as any reader's,
    the overview among them, whose idle-time formulas did not finish under reduced
    motion."""
    assert motion_for("visualize.html") == "reduce"
    assert motion_for("visualize.html#film") == "reduce"
    for name in (
        "index.html",
        "frontier.html",
        "workbench/index.html",
        "cases/index.html#n-11",
    ):
        assert motion_for(name) == "no-preference", name


def test_a_link_to_a_page_that_moved_is_reported(tmp_path: Path) -> None:
    """A forwarder keeps an old link working, and a page of the site names where the
    reader is going: a built page that links or frames an address in
    `render_overview.MOVED_PAGES` is named with the link, from the root or from a
    directory under it. The forwarders themselves and an address off the site are not."""
    moved = [old for old, _ in render_overview.MOVED_PAGES]
    assert moved[:4] == ["results.html", "status.html", "frontier.html", "defects.html"]
    (tmp_path / "result").mkdir()
    for old in moved:
        (tmp_path / old).parent.mkdir(exist_ok=True)
        (tmp_path / old).write_text('<a href="all-results.html">moved</a>', encoding="utf-8")
    (tmp_path / "all-results.html").write_text(
        '<a href="atlas.html#n-11">a row</a>'
        '<a href="https://example.org/results.html">elsewhere</a>',
        encoding="utf-8",
    )
    assert moved_links(tmp_path) == []
    (tmp_path / "index.html").write_text(
        '<a href="results.html#next-actions">old</a>'
        '<iframe src="defects.html?view=embed"></iframe>'
        '<a href="all-results.html#t-060">new</a>',
        encoding="utf-8",
    )
    (tmp_path / "result" / "t-001.html").write_text(
        '<a href="../status.html">old</a>', encoding="utf-8"
    )
    assert moved_links(tmp_path) == [
        "index.html: defects.html?view=embed",
        "index.html: results.html#next-actions",
        "result/t-001.html: ../status.html",
    ]


def test_a_moved_file_is_copied_to_its_old_address(tmp_path: Path) -> None:
    """A paper's Markdown and PDF cannot forward, so the assembled site serves each at the
    address it had before the papers moved too, as a copy (`render_overview.MOVED_FILES`),
    which is what the workflow's `publish` job does. A file a skipped build would have
    written has no copy, and nothing else in the directory is touched."""
    from devtools.preview_site import copy_moved_files  # noqa: PLC0415

    assert copy_moved_files(tmp_path) == []
    papers = tmp_path / "papers"
    papers.mkdir()
    (papers / "n11-lower-bounds-explainer.md").write_text("explainer", encoding="utf-8")
    (papers / "n11-optimality-review.md").write_text("review", encoding="utf-8")
    (papers / "n11-optimality-review.pdf").write_bytes(b"%PDF review")
    assert copy_moved_files(tmp_path) == [
        "t-018-explainer.md",
        "n11-optimality/t-060-explainer.md",
        "n11-optimality/t-060-explainer.pdf",
    ]
    for old, new in render_overview.MOVED_FILES:
        if (tmp_path / new).is_file():
            assert (tmp_path / old).read_bytes() == (tmp_path / new).read_bytes(), old
    assert not (tmp_path / "t-018-explainer.pdf").exists()
    assert sorted(path.name for path in papers.iterdir()) == [
        "n11-lower-bounds-explainer.md",
        "n11-optimality-review.md",
        "n11-optimality-review.pdf",
    ]


def test_the_builds_are_named_for_what_they_build(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`--skip` takes a paper by its slug, as everything else names it, and every paper
    of the site is a build (`render_overview.PAPERS`): the first, then the site's pages
    and the workbench, then each independent paper, built by its registered renderer
    with its PDF, as its Pages job builds it."""
    from devtools import preview_site  # noqa: PLC0415

    independent = tuple(
        paper
        for paper in render_overview.PAPERS
        if paper.slug != render_overview.N11_LOWER_BOUNDS_EXPLAINER
    )
    assert independent
    assert (
        render_overview.N11_LOWER_BOUNDS_EXPLAINER,
        "pages",
        "workbench",
        *(paper.slug for paper in independent),
    ) == preview_site.BUILDS
    assert tuple(paper.slug for paper in independent) == preview_site.OTHER_PAPERS
    ran: list[tuple[str, ...]] = []
    monkeypatch.setattr(preview_site, "_run", lambda *args: ran.append(args))
    for paper in independent:
        preview_site.build_paper(paper.slug, Path("/site"))
    assert ran == [(paper.module, "--site", "/site", "--pdf") for paper in independent]
