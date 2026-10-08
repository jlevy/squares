#!/usr/bin/env python3
"""The overview of one registered result: the body of the popover its row opens.

A result's row, in Recent Results on the homepage and in the table on
`all-results.html`, opens a popover with everything the site knows about the result.
This module writes that popover's body, `result_popover_html(result, overview)`; the
popover around it, with the result's id as its caps label and its summary as its
headline, and the row that opens it, belong to the pages that list results
(`overview_sections.result_row`). Nothing here depends on that mechanism: the body is
one `.site-result` block with no ids, so it can be placed anywhere, as often as a page
needs it. It is written once a result, as a file beside the pages
(`render_overview.result_fragments`), and a row's popover fetches its own. It has four
parts.

1. **The head**: the rung chips and standing as the tables show them
   (`overview_sections.status_chips`), the date and credit as the register states
   them (`result_credit`, through `overview_data.Result`), and the claim, its
   mathematics set as the site sets it (`overview_data.tex_bounds`).
2. **The case**: for a result about one case, or a few (`render_case_pages.BROAD_RESULT`
   or fewer), each case's visual summary as its record opens with it
   (`render_case_pages.visual_summary`): the known-best packing drawn from the atlas,
   then the film's panel, the gap bar, the bound as one statement, the badges, the
   citation and what is open. The facts are the film's own
   (`overview_sections.atlas_film_facts`), placed here at render time (`gap_bar`,
   `GAP_INSET`, `GAP_SPAN`). Under it, the case record's verified and reported bounds
   and the gap. A result about more cases than that, such as Couzo's 49 packings, gets
   a compact list instead, one row per case linking to its record, and says so.
3. **The chain**: every register result on the same case, oldest first, each with what
   it established, its rungs and standing, and its citations and sources linked.
4. **The links**: the case record, the frontier row and the result's row on this site,
   and on GitHub, always on `main` (`repo_links`): the register entry and each evidence
   entry at its line, the source packet, the artifacts, the review, the case file and
   its frontmatter bounds, and each cited source's bibliography entry. Every link is
   checked when the body is rendered, against the working tree for a repository path
   and against the record for a page fragment, and a missing target fails the render.

The design is `templates/paper-design.md`, Result Overview, and its styles are
`templates/site-result.css`.

`--audit` renders every result's overview, counts its links against the tree at `HEAD`
and reports the overviews' sizes. From `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.result_overview --audit
"""

from __future__ import annotations

import argparse
import html
import math
import re
import sys
from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import replace
from decimal import Decimal
from functools import cache
from pathlib import Path
from typing import Any, NamedTuple, cast
from urllib.parse import urlsplit

from devtools import repo_links
from devtools.overview_data import (
    BIBLIOGRAPHY,
    EVIDENCE,
    FRONTIER,
    PACKING,
    REPO,
    RESULTS,
    Overview,
    Result,
    math_html,
    prose_html,
    tex_bounds,
)
from devtools.repo_links import path_kind, repo_url

#: The film's gap bar, as every case's visual summary draws it (`gap_bar`; the atlas
#: popover's script drew its own until 2026-10-03): the inset at each end, in percent of
#: the bar, and the span the bar covers, from one below the grid bound.
GAP_INSET = 5
GAP_SPAN = 2
#: Two values on the bar closer than this, in percent of it, would overlap centred on
#: their marks; the lower is then set before its mark and the upper after it.
GAP_CROWDED = 18

#: A result about this many cases or fewer names them; one about more counts them.
CASES_NAMED = 4
#: More artifacts than this open on request.
ARTIFACTS_OPEN = 4

#: A link to a page of this site, as its page and fragment, which `check_links` checks.
SITE_LINK = re.compile(r'href="(?!https://)([^"#?]*)(?:\?[^"#]*)?(?:#([^"]*))?"')

#: What the overview puts between the links of a line.
DOT = " \u00b7 "


def _esc(text: object) -> str:
    return html.escape(str(text), quote=True)


# ---------- What the record says about a result ----------


def scope(result: Result) -> list[int]:
    """Every case a result concerns, in order."""
    record_scope = result.record["scope"]
    if "n_values" in record_scope:
        return sorted(record_scope["n_values"])
    return list(range(record_scope["n_min"], record_scope["n_max"] + 1))


def is_broad(cases: Sequence[int]) -> bool:
    """Whether a result is about too many cases to draw each: the case records' rule."""
    from devtools.render_case_pages import BROAD_RESULT  # noqa: PLC0415

    return len(cases) > BROAD_RESULT


def _resolve(path: str) -> Path | None:
    """A path a record names, repository-relative or packing-relative, if the repository
    has it. Whether it does is `repo_links.path_kind`'s to say, here and in every test
    below of a file or a directory: the deployed site is rendered from a checkout
    without the archive's and the campaign's directories, and their links must not
    depend on which checkout rendered the page."""
    for base in (REPO, PACKING):
        candidate = base / path
        if path_kind(candidate) is not None:
            return candidate
    return None


def _line_url(path: Path, line: int) -> str:
    """A link on `main` to one line of a file, which GitHub opens in its code view."""
    return repo_url(path, f"?plain=1#L{line}")


def _lines(path: Path, pattern: str) -> dict[str, int]:
    """Each first line of `path` that `pattern` matches whole, by its first group."""
    found: dict[str, int] = {}
    compiled = re.compile(pattern)
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = compiled.fullmatch(line)
        if match and match.group(1) not in found:
            found[match.group(1)] = number
    return found


@cache
def result_lines() -> dict[str, int]:
    """Each result's line in `results.yaml`, `- id: T-NNN`."""
    return _lines(RESULTS, r"  - id: (T-\d{3})")


@cache
def evidence_lines() -> dict[str, int]:
    """Each evidence entry's line in `evidence.yaml`."""
    return _lines(EVIDENCE, r"  - id: (E-[a-z0-9-]+)")


@cache
def bibliography_lines() -> dict[str, int]:
    """Each source's line in `bibliography.yaml`, by its key, brackets included."""
    return _lines(BIBLIOGRAPHY, r"  - key: '(\[.+\])'")


#: The four bounds a case record's frontmatter carries, in the order a reader compares
#: them, with what the overview calls each.
CASE_BOUNDS: tuple[tuple[str, str], ...] = (
    ("verified_lower_bound", "verified lower"),
    ("verified_upper_bound", "verified upper"),
    ("reported_lower_bound", "reported lower"),
    ("reported_upper_bound", "reported upper"),
)


def case_file(n: int) -> Path:
    return FRONTIER / f"n-{n:03d}.md"


@cache
def case_bound_lines(n: int) -> dict[str, int]:
    """The line of each bound in case `n`'s frontmatter, its `SquarePackingCase/v2`
    record, so a link opens the record at the field."""
    text = case_file(n).read_text(encoding="utf-8")
    front = text.split("\n---\n", 1)[0]
    found = {
        match.group(1): front.count("\n", 0, match.start()) + 1
        for match in re.finditer(r"^  ([a-z_]+_bound):", front, flags=re.MULTILINE)
    }
    missing = [key for key, _ in CASE_BOUNDS if key not in found]
    if missing:
        raise SystemExit(f"{case_file(n).name}: no frontmatter line for {', '.join(missing)}")
    return found


@cache
def _evidence() -> dict[str, dict[str, Any]]:
    from sqpack.yamlio import safe_load  # noqa: PLC0415

    entries = safe_load(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    return {entry["id"]: entry for entry in entries}


def cited_keys(result: Result) -> list[str]:
    """The sources a result cites: its attribution's, then its evidence's, each once."""
    keys = list((result.record.get("attribution") or {}).get("source_keys") or [])
    evidence = _evidence()
    for item in result.record["evidence"]:
        key = (evidence.get(item) or {}).get("source_key")
        if key:
            keys.append(key)
    return list(dict.fromkeys(keys))


_PACKET = re.compile(r"packing/resources/(?:web|private-correspondence)/[^/]+")


def packets(result: Result) -> list[Path]:
    """The source packets a result's artifacts sit in, each its README where it has one."""
    found: list[Path] = []
    for path in result.record["artifacts"]:
        match = _PACKET.match(path)
        if match is None:
            continue
        directory = REPO / match.group(0)
        readme = directory / "README.md"
        target = readme if path_kind(readme) == "blob" else directory
        if path_kind(target) is not None and target not in found:
            found.append(target)
    return found


def _local_copy(local: str) -> Path | None:
    """A case resource's retained copy: a packet's README, or a paper's clean
    transcription, else its PDF. `local` is resources-relative or repository-relative."""
    for base in (REPO, PACKING / "resources"):
        path = base / local
        if path_kind(path) == "tree":
            readme = path / "README.md"
            return readme if path_kind(readme) == "blob" else path
        for candidate in (
            path,
            path.with_name(path.name + ".md"),
            path.with_name(path.name + ".pdf"),
        ):
            if path_kind(candidate) == "blob":
                return candidate
    return None


def resources(
    cases: Iterable[dict[str, Any]], keys: Iterable[str]
) -> dict[str, dict[str, Any]]:
    """The first resource entry each key has in the case records, by key."""
    wanted = set(keys)
    found: dict[str, dict[str, Any]] = {}
    for case in cases:
        for resource in case.get("resources") or []:
            key = resource.get("key")
            if key in wanted and key not in found:
                found[key] = resource
    return found


# ---------- The film's panel, filled here ----------


@cache
def film_facts() -> dict[int, dict[str, Any]]:
    """What the ascent film's panel says about each case, read as the atlas grid reads it."""
    from devtools.overview_sections import atlas_film_facts  # noqa: PLC0415

    return {cast("int", fact["n"]): cast("dict[str, Any]", fact) for fact in atlas_film_facts()}


def grid_floor(n: int) -> int:
    """One below the grid bound, `ceil(sqrt(n)) - 1`: where the film's bar starts."""
    root = math.isqrt(n)
    return root - 1 if root * root == n else root


def bar_at(value: float, low: int) -> float:
    """Where `value` falls on the bar, in percent of its width (atlas-grid.js `at`)."""
    return GAP_INSET + min(1.0, max(0.0, (value - low) / GAP_SPAN)) * (100 - 2 * GAP_INSET)


def bar_number(value: float) -> str:
    """A value as the bar prints it: whole numbers plain, the rest to three places."""
    return str(int(value)) if float(value).is_integer() else f"{value:.3f}"


def _placed(classes: str, text: str, percent: float, anchor: str = "") -> str:
    attributes = f' class="{classes}"' if classes else ""
    if anchor:
        attributes += f' data-anchor="{anchor}"'
    return f'<span{attributes} style="left: {percent:.3f}%">{text}</span>'


def gap_bar(fact: dict[str, Any]) -> str:
    """The film's gap bar for one case, as `atlas-grid.js` (`drawGap`) draws it: a number
    line from one below the grid bound to two above it, the integers and the values of
    `sqrt(n)` and `sqrt(n) + 1` marked, the two bounds as bold rules with their values
    above, and the span between them shaded."""
    n = int(fact["n"])
    upper = float(fact["upper"])
    lower = upper if fact["lower"] is None else float(fact["lower"])
    root = math.sqrt(n)
    low = grid_floor(n)
    marks: list[float] = []
    for value in (low, low + 1, low + 2, root, root + 1):
        if value not in marks:
            marks.append(float(value))
    rail = ['<span class="site-atlas-gap-track"></span>']
    start, end = bar_at(lower, low), bar_at(upper, low)
    rail.append(
        f'<span class="site-atlas-gap-open" style="left: {start:.3f}%; '
        f'width: {max(0.0, end - start):.3f}%"></span>'
    )
    integers: list[str] = []
    roots: list[str] = []
    for value in marks:
        whole = value.is_integer()
        at = bar_at(value, low)
        rail.append(_placed("site-atlas-gap-tick" + ("" if whole else " is-root"), "", at))
        (integers if whole else roots).append(_placed("", bar_number(value), at))
    values: list[str] = []
    crowded = fact["lower"] is not None and end - start < GAP_CROWDED
    if fact["lower"] is not None:
        rail.append(_placed("site-atlas-gap-rule", "", start))
        values.append(_placed("is-lower", bar_number(lower), start, "end" if crowded else ""))
    rail.append(_placed("site-atlas-gap-rule", "", end))
    values.append(_placed("is-upper", bar_number(upper), end, "start" if crowded else ""))
    formulas = "".join(
        _placed("site-atlas-gap-formula", math_html(tex), bar_at(value, low))
        for tex, value in ((r"\sqrt{n}", root), (r"\sqrt{n} + 1", root + 1))
    )
    return (
        '<div class="site-atlas-gap">'
        f'<div class="site-atlas-gap-values">{"".join(values)}</div>'
        f'<div class="site-atlas-gap-rail">{"".join(rail)}</div>'
        f'<div class="site-atlas-gap-row">{"".join(integers)}</div>'
        f'<div class="site-atlas-gap-row">{"".join(roots)}</div>'
        f'<div class="site-atlas-gap-row site-atlas-gap-formulas">{formulas}</div></div>'
    )


def film_bound(fact: dict[str, Any]) -> str:
    """The bound as one statement, as the film writes it (`drawBound`): the proved lower
    bound and the best known side in their colours, or the exact value, after the star a
    recent lower bound earns."""
    n = int(fact["n"])
    star = "\u2605" if fact["star"] else ""
    parts = [f'<span class="site-atlas-pop-star" aria-hidden="true">{star}</span>']
    if fact["exact"]:
        parts.append(math_html(f"s({n}) = {fact['upper']}"))
    else:
        if fact["lower"] is not None:
            parts.append(f'<span class="is-lower">{math_html(str(fact["lower"]))}</span>')
        middle = rf"s({n}) \le{{}}" if fact["lower"] is None else rf"{{}}\le s({n}) \le{{}}"
        parts.append(math_html(middle))
        parts.append(f'<span class="is-upper">{math_html(str(fact["upper"]))}</span>')
    return f'<p class="site-atlas-pop-bound">{"".join(parts)}</p>'


def badge_glyph(glyph: str, style: str, text: str, *, named: bool = False) -> str:
    """One of the film's badges, the site's one mark for a property of a case (optimal,
    exact, numerical, rigid, a new result, something open): its glyph in a small square,
    solid or outlined (`.site-atlas-badge`). `named`, where no word follows it, gives it
    its word as its name and its tooltip."""
    name = (
        f'role="img" aria-label="{_esc(text)}" title="{_esc(text)}"'
        if named
        else 'aria-hidden="true"'
    )
    return (
        f'<span class="site-atlas-badge" data-style="{_esc(style)}" {name}>{_esc(glyph)}</span>'
    )


def _badge(glyph: str, style: str, text: str, classes: str = "") -> str:
    item = f"site-atlas-pop-item {classes}".strip()
    return f'<li class="{item}">{badge_glyph(glyph, style, text)}{_esc(text)}</li>'


def case_badges(n: int) -> str:
    """Case `n`'s property badges as the film draws them, each named, in a row of their
    own and without their words: the same marks the visual summary lists with words,
    where a case is one line, as in a table's row or a record's head (think-7cbx)."""
    marks = "".join(
        badge_glyph(glyph, style, text, named=True)
        for glyph, style, text in film_facts()[n]["badges"]
    )
    return f'<span class="site-case-badges">{marks}</span>' if marks else ""


def film_facts_html(fact: dict[str, Any]) -> str:
    """The badges, the citation and what is open, as the film lists them (`drawFacts`)."""
    badges = [_badge("\u2605", "star", "new result", "is-new-result")] if fact["star"] else []
    badges.extend(_badge(glyph, style, text) for glyph, style, text in fact["badges"])
    cites = []
    for which in ("lower", "upper"):
        line = fact["cite"][which]
        if line is None:
            continue
        # A lower bound standing in for a published result found unsound names that
        # work, `corrects Nagamochi 2005`, between its reference and its note.
        corrects = (
            f' <span class="site-corrects">{_esc(line["corrects"])}</span>'
            if line.get("corrects")
            else ""
        )
        note = (
            f' <span class="site-atlas-pop-note">{_esc(line["note"])}</span>'
            if line["note"]
            else ""
        )
        cites.append(
            f'<p class="site-atlas-pop-cite"><span class="site-atlas-pop-which is-{which}">'
            f"{which}</span>{_esc(line['text'])}{corrects}{note}</p>"
        )
    citation = (
        '<p class="site-atlas-pop-head">Citation <span class="site-atlas-pop-record">record '
        f"{_esc(fact['record'])}</span></p>{''.join(cites)}"
        if cites
        else ""
    )
    open_items = "".join(_badge("?", "query", text) for text in fact["open"])
    # `data-atlas-open` is what site.css keys the open items' quiet style on.
    opened = (
        '<div data-atlas-open><p class="site-atlas-pop-head">Open</p>'
        f'<ul class="site-atlas-pop-badges">{open_items}</ul></div>'
        if open_items
        else ""
    )
    return f'<ul class="site-atlas-pop-badges">{"".join(badges)}</ul>{citation}{opened}'


def _cell(content: str, role: str = "cell", classes: str = "") -> str:
    attributes = f' class="{classes}"' if classes else ""
    return f'<span role="{role}"{attributes}>{content}</span>'


def _grid_row(cells: Sequence[str], attributes: str = "") -> str:
    return f'<div role="row"{attributes}>{"".join(cells)}</div>'


def bounds_table(case: dict[str, Any]) -> str:
    """The case record's four bounds and its gap, each value linked to its field in the
    case file's frontmatter on GitHub.

    It is a grid marked with table roles rather than a `<table>`: kpress restyles every
    table on a page as its own component, and a results table's script counts the rows
    it finds inside it, so an overview shown from a table row must not add any."""
    from devtools import render_frontier_page as frontier  # noqa: PLC0415

    n = int(case["n"])
    lines = case_bound_lines(n)
    path = case_file(n)

    def bound(key: str) -> str:
        value = frontier.value_html(case[key])
        return _cell(f'<a href="{_esc(_line_url(path, lines[key]))}">{value}</a>')

    gap_html, _ = frontier.gap(case)
    note = (
        ' <span class="site-cell-quiet">solved: the verified bounds meet</span>'
        if case["status"] == "proved"
        else ""
    )
    return (
        '<div class="site-result-bounds" role="table" aria-label="Bounds in the case record">'
        + _grid_row(
            [
                _cell("", "columnheader"),
                _cell("Lower", "columnheader"),
                _cell("Upper", "columnheader"),
            ]
        )
        + _grid_row(
            [
                _cell("Verified", "rowheader"),
                bound("verified_lower_bound"),
                bound("verified_upper_bound"),
            ]
        )
        + _grid_row(
            [
                _cell("Reported", "rowheader"),
                bound("reported_lower_bound"),
                bound("reported_upper_bound"),
            ]
        )
        + _grid_row(
            [_cell("Gap", "rowheader"), _cell(gap_html + note, classes="site-result-gap")]
        )
        + "</div>"
    )


def case_panel(n: int, overview: Overview, *, label: bool) -> str:
    """One case as its record opens, the visual summary (`render_case_pages.
    visual_summary`, the drawing at the atlas's size), with the record's bounds under it
    and its own link to the record among the overview's links."""
    from devtools.overview_sections import ATLAS_UNITS  # noqa: PLC0415
    from devtools.render_case_pages import visual_summary  # noqa: PLC0415

    case = overview.cases[n]
    # The case's n heads its panel as a case record's title does: a caps label would
    # set the n of its formula in capitals too.
    head = (
        '<p class="site-popover-value site-result-case-n" data-math-face="serif">'
        f"{math_html(f'n = {n}')}</p>"
        if label
        else ""
    )
    return (
        f'<div class="site-atlas-pop site-result-film" data-overview-case="{n}">{head}'
        f"{visual_summary(n, units=ATLAS_UNITS)}"
        f'<p class="site-atlas-pop-head">The case record</p>{bounds_table(case)}</div>'
    )


def _case_table(rows: Sequence[tuple[int, Sequence[str]]]) -> str:
    """Native cells share only consecutive, exactly equal bounds or status markup.

    Case identifiers and record links always have their own cell. Row spans retain all
    six logical cells of each case without repeating identical badges and bounds."""
    spans = [[1] * 6 for _ in rows]
    for column in range(1, 5):
        start = 0
        while start < len(rows):
            end = start + 1
            while end < len(rows) and rows[end][1][column] == rows[start][1][column]:
                end += 1
            spans[start][column] = end - start
            for index in range(start + 1, end):
                spans[index][column] = 0
            start = end
    body = []
    for (n, cells), counts in zip(rows, spans, strict=True):
        rendered = []
        for column, (content, count) in enumerate(zip(cells, counts, strict=True)):
            if not count:
                continue
            rowspan = f' rowspan="{count}"' if count > 1 else ""
            name = {1: "lower", 2: "upper", 5: "records"}.get(column)
            classes = f' class="{name}"' if name else ""
            rendered.append(f"<td{classes}{rowspan}>{content}</td>")
        body.append(f'<tr data-overview-case="{n}">{"".join(rendered)}</tr>')
    headings = ("n", "Proved lower", "Best known", "Gap", "Status", "Records")
    head = "".join(f'<th scope="col">{heading}</th>' for heading in headings)
    return (
        '<table class="site-result-cases" aria-label="The cases of this result">'
        f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"
    )


def case_list(cases: Sequence[int], overview: Overview) -> str:
    """A broad result's cases, one compact row each: the film's two bounds and the gap,
    the case's status, and its record on this site, its row in the frontier atlas and
    its case file on GitHub."""
    from devtools import render_frontier_page as frontier  # noqa: PLC0415
    from devtools.overview_sections import case_status_chip  # noqa: PLC0415
    from devtools.render_case_pages import case_url  # noqa: PLC0415

    facts = film_facts()
    rows = []
    for n in cases:
        fact = facts[n]
        case = overview.cases[n]
        lower = fact["lower"] if fact["lower"] is not None else fact["upper"]
        _, gap_value = frontier.gap(case)
        gap = frontier.decimal_text(Decimal(gap_value).normalize()) if gap_value != "0" else "0"
        status = case["status"]
        star = (
            '<span class="site-star" title="Recent lower bound">\u2605</span>'
            if fact["star"]
            else ""
        )
        rows.append(
            (
                n,
                [
                    f'<a href="{case_url(n)}">{n}</a>',
                    _esc(lower) + star,
                    _esc(fact["upper"]),
                    _esc(gap),
                    case_status_chip(status) + case_badges(n),
                    (
                        f'<a href="frontier.html#n-{n}">frontier</a> '
                        f'<a href="{_esc(repo_url(case_file(n)))}">'
                        f"{_esc(case_file(n).name)}</a>"
                    ),
                ],
            )
        )
    return (
        f'<p class="site-result-note">This result concerns {len(cases)} cases, too many '
        "to draw one by one. Each is listed with the film\u2019s bounds, the proved lower "
        "bound and the best known side, and links to its case record, where its packing "
        "and number line are drawn.</p>"
        f'<div class="site-result-case-list">{_case_table(rows)}</div>'
    )


# ---------- The parts of the overview ----------


def where(cases: Sequence[int]) -> str:
    """A result's cases as the head states them: `n = 11`, or a range and a count."""
    if len(cases) == 1:
        return math_html(f"n = {cases[0]}")
    if len(cases) <= CASES_NAMED:
        return math_html("n = " + ", ".join(map(str, cases)))
    return f"{len(cases)} cases, {math_html(f'n = {cases[0]}')} to {cases[-1]}"


def head(result: Result, cases: Sequence[int]) -> str:
    """The chips, the date and credit, the claim, and what a later result its entry
    declares implies of it (`superseded_by`). The date leads and what it dates follows,
    as a table's date cell sets it (`overview_sections.date_cell`). The id and the
    headline are the popover's own, above the body (`overview_sections.result_row`)."""
    from devtools.overview_sections import (  # noqa: PLC0415
        date_cell,
        novelty_labels,
        result_url,
        status_chips,
    )

    record = result.record
    claim = prose_html(record["claim"], between='</p><p class="site-result-claim">')
    # A later result its entry declares implies it says what it implies, under the
    # claim it bears on; a superseded bound's chip names its successors, which need no
    # sentence, since their bounds are the case's.
    superseded = "".join(
        '<p class="site-result-claim site-result-superseded"><strong>'
        f"{'Superseded' if item['extent'] == 'whole' else 'Superseded in part'} by "
        f'<a href="{_esc(result_url(str(item["result"])))}">{_esc(str(item["result"]))}</a>.'
        f"</strong> {prose_html(item['what'])}</p>"
        for item in record.get("superseded_by") or []
    )
    more = [
        ("Significance", record["significance"]["rationale"]),
        ("Composition", record.get("composition")),
        ("Next rung", record.get("next_rung")),
    ]
    rows = "".join(
        f"<dt>{label}</dt><dd>{prose_html(text)}</dd>" for label, text in more if text
    )
    meaning = novelty_labels().get(result.novelty, "")
    rows += (
        f'<dt>Novelty</dt><dd><span class="site-chip" data-novelty="{_esc(result.novelty)}">'
        f"{_esc(result.novelty)}</span> {_esc(meaning)}</dd>"
    )
    return (
        '<header class="site-result-head">'
        f'<p class="site-result-status">{status_chips(result)}</p>'
        f'<p class="site-result-meta">{date_cell(result)} \u00b7 {_esc(result.credit)} '
        f"\u00b7 {where(cases)}</p>"
        f'<p class="site-result-claim">{claim}</p>'
        f"{superseded}"
        '<details class="site-result-more"><summary>Significance, composition and next '
        f'rung</summary><dl class="site-detail">{rows}</dl></details>'
        "</header>"
    )


def case_section(result: Result, overview: Overview, cases: Sequence[int]) -> str:
    """The case drawn and its number line, or, for a broad result, the compact list."""
    for n in cases:
        if n not in overview.cases:
            raise SystemExit(f"{result.id}: case {n} has no record")
    if is_broad(cases):
        body = case_list(cases, overview)
        title = "The cases"
    else:
        body = "".join(case_panel(n, overview, label=len(cases) > 1) for n in cases)
        title = "The case" if len(cases) == 1 else "The cases"
    return (
        f'<section class="site-result-section"><h3 class="site-result-heading">{title}</h3>'
        f"{body}</section>"
    )


def _link(url: str, label: str, title: str = "") -> str:
    titled = f' title="{_esc(title)}"' if title and title not in url else ""
    return f'<a href="{_esc(url)}"{titled}>{label}</a>'


def bibliography_link(key: str) -> str:
    """A cited source's entry in `bibliography.yaml`, its softschema record, at its line."""
    line = bibliography_lines().get(key)
    if line is None:
        return f'<span class="site-cell-quiet">{_esc(key.strip("[]"))}</span>'
    return _link(_line_url(BIBLIOGRAPHY, line), _esc(key.strip("[]")), "bibliography.yaml")


def register_line(result: Result) -> int:
    """The line of a result's entry in `results.yaml`, which its link opens."""
    line = result_lines().get(result.id)
    if line is None:
        raise SystemExit(f"{result.id} has no line in {RESULTS.name}")
    return line


def register_link(result: Result, label: str = "register") -> str:
    title = f"{result.id} in results.yaml"
    return _link(_line_url(RESULTS, register_line(result)), label, title)


@cache
def _records() -> Any:
    from devtools.render_recent_results import load_records  # noqa: PLC0415

    return load_records()


def standing_on(other: Result, cases: Sequence[int]) -> str:
    """A result's standing on `cases` alone: `render_recent_results.standing`, the rule
    the register's views use, asked of the result with its scope cut to those cases.

    A result about many cases can be the current best at some and superseded at others,
    and its row states the first. A chain is about its own cases, so it says both."""
    return _standing_on(other.id, tuple(cases))


@cache
def _standing_on(result_id: str, cases: tuple[int, ...]) -> str:
    """`standing_on`, kept: every result on a case shows the same chain."""
    from devtools.render_recent_results import standing  # noqa: PLC0415

    records = _records()
    record = records.results[result_id]
    return standing({**record, "scope": {"n_values": list(cases)}}, records)


def supersessions_on(other: Result, cases: Sequence[int]) -> tuple[Any, ...]:
    """A result's marks of supersession on `cases` alone
    (`render_recent_results.supersessions`), asked of the result with its scope cut to
    those cases, as `standing_on` asks its standing: a bound superseded on several cases
    names, on a chain about some of them, only the results that hold those."""
    return _supersessions_on(other.id, tuple(cases))


@cache
def _supersessions_on(result_id: str, cases: tuple[int, ...]) -> tuple[Any, ...]:
    """`supersessions_on`, kept, as `_standing_on` is."""
    from devtools.render_recent_results import standing, supersessions  # noqa: PLC0415

    records = _records()
    cut = {**records.results[result_id], "scope": {"n_values": list(cases)}}
    return tuple(supersessions(cut, standing(cut, records), records))


def citations(other: Result) -> list[str]:
    """A result's citations and sources, as a chain step links them: each source's
    bibliography entry, the packet its artifacts sit in, the proof source and review the
    register's records name, and the register entry itself."""
    keys = (other.record.get("attribution") or {}).get("source_keys") or []
    return [
        *(bibliography_link(key) for key in keys),
        *(
            _link(repo_url(packet), "packet", repo_links.relative(packet))
            for packet in packets(other)
        ),
        *(
            _link(link.url, _esc(link.label), link.title)
            for link in other.records
            if link.label.split()[0] in {"source", "review"}
        ),
        register_link(other),
    ]


def step(other: Result, current: Result, cases: Sequence[int]) -> str:
    """One result in the chain: when, which, what it established, how it stands, and its
    citations and sources. Its date leads and what it dates follows, as in the tables
    (`overview_sections.date_cell`).

    A broad result's chain runs to dozens of results, so a step there keeps its kind and
    status and leaves its rungs to its own row. A superseded result's step names the
    results that supersede it on these cases alone (`supersessions_on`)."""
    from devtools.overview_sections import (  # noqa: PLC0415
        date_cell,
        kind_and_status,
        result_url,
        standing_key,
        status_chips,
        superseder_link,
    )
    from devtools.render_recent_results import (  # noqa: PLC0415
        NO_STANDING,
        SUPERSEDED,
        listed,
        superseded,
    )

    wanted = set(cases)
    shared = [n for n in scope(other) if n in wanted]
    on = ""
    if len(cases) > 1:
        if len(shared) > CASES_NAMED:
            on = DOT + f"{len(shared)} of these cases"
        elif is_broad(cases):
            label = "case " if len(shared) == 1 else "cases "
            on = DOT + label + ", ".join(map(str, shared))
        else:
            on = DOT + math_html("n = " + ", ".join(map(str, shared)))
    current_mark, this = "", ""
    if other.id == current.id:
        current_mark = ' data-current=""'
        this = ' <span class="site-result-this">this result</span>'
    here = standing_on(other, shared)
    marks = supersessions_on(other, shared)
    # Where the result stands here as it does as a whole, its marks name only the
    # results on these cases; where it stands differently, its chips are the whole
    # result's, as its row's are, and a note says how it stands here.
    shown = replace(other, supersessions=marks) if here == other.standing else other
    chips = kind_and_status(shown) if is_broad(cases) else status_chips(shown)
    if here != other.standing:
        on_case = "on this case" if len(cases) == 1 else "on these cases"
        said = _esc(here)
        by = [mark for mark in marks if mark.mark == SUPERSEDED and mark.by]
        if by:
            links = [superseder_link(item, by[0].reported) for item in by[0].by]
            said += f" by {listed(links)}"
        chips += f' <span class="site-cell-quiet">{on_case}, {said}</span>'
    chip_line = f'<p class="site-result-step-chips">{chips}</p>'
    cites = [_esc(other.credit), *citations(other)]
    # A step is set back where its result is superseded here as its row would be
    # (`render_recent_results.superseded`): a bound no case bound here rests on, or a
    # result its entry declares superseded as a whole, whatever its standing. A result
    # of another kind that derives `superseded` from the bound it cites (T-003, a
    # method's limit) is current, and its step is not set back.
    if any(mark.mark == SUPERSEDED for mark in marks):
        dimmed = SUPERSEDED
    elif here == SUPERSEDED and not superseded(other.record, here):
        dimmed = NO_STANDING
    else:
        dimmed = here
    return (
        f'<li class="site-result-step" data-step="{_esc(other.id.lower())}" '
        f'data-standing="{_esc(standing_key(dimmed))}"{current_mark}>'
        f'<p class="site-result-step-head">{date_cell(other)} '
        f'<a href="{_esc(result_url(other.id))}">{_esc(other.id)}</a>{this}'
        f"{on}</p>"
        f'<p class="site-result-step-summary">{tex_bounds(other.summary)}</p>'
        f"{chip_line}"
        f'<p class="site-result-step-cite">{DOT.join(cites)}</p></li>'
    )


def chain(overview: Overview, cases: Sequence[int]) -> list[Result]:
    """Every register result on any of `cases`, oldest first by the date its row shows."""
    wanted = set(cases)
    members = [other for other in overview.results if wanted & set(scope(other))]
    return sorted(members, key=lambda other: (other.dated[1], other.id))


def chain_section(result: Result, overview: Overview, cases: Sequence[int]) -> str:
    """The proofs and results for the case as a chain, oldest first."""
    members = chain(overview, cases)
    items = "".join(step(other, result, cases) for other in members)
    listing = f'<ol class="site-result-chain">{items}</ol>'
    count = len(members)
    results = f"{count} result{'s' if count != 1 else ''} in the register"
    if is_broad(cases):
        listing = (
            f'<details class="site-result-chain-more"><summary>{results} on these cases, '
            f"oldest first</summary>{listing}</details>"
        )
        note = ""
    else:
        note = (
            f'<p class="site-result-note">{results} on {where(cases)}, oldest first, each '
            "with what it established and how it stands now.</p>"
        )
    # The heading is a caps label, which would set a formula's letters in capitals, so
    # the case's n is in the note under it.
    title = "Results on the case" if len(cases) == 1 else "Results on these cases"
    return (
        f'<section class="site-result-section"><h3 class="site-result-heading">{title}</h3>'
        f"{note}{listing}</section>"
    )


def _row(label: str, links: Sequence[str]) -> str:
    return f"<dt>{label}</dt><dd>{DOT.join(links)}</dd>" if links else ""


def _path_link(path: Path, label: str = "") -> str:
    rel = repo_links.relative(path)
    shown = label or f"<code>{_esc(rel.removeprefix('packing/'))}</code>"
    return _link(repo_url(path), shown, rel)


def links_section(result: Result, overview: Overview, cases: Sequence[int]) -> str:
    """Where to read more: this site's pages, and the record on GitHub at `main`.

    A result on eleven squares links both papers on that case, the one on the result
    that stands first: the optimality paper, which explains T-060, then the explainer,
    which proves the lower bounds T-060 superseded."""
    from devtools.overview_sections import (  # noqa: PLC0415
        LOWER_BOUNDS_PAPER,
        OPTIMALITY_PAPER,
        result_url,
    )
    from devtools.render_case_pages import CASES_HOME, case_url  # noqa: PLC0415

    record = result.record
    site: list[str] = []
    if is_broad(cases):
        site.append(_link("frontier.html", "The frontier survey"))
        site.append(_link(CASES_HOME, "Every case record"))
    else:
        for n in cases:
            site.append(_link(case_url(n), f"Case record, {math_html(f'n = {n}')}"))
            site.append(_link(f"frontier.html#n-{n}", f"Frontier row, {math_html(f'n = {n}')}"))
    site.append(_link(result_url(result.id), f"{_esc(result.id)} in the results table"))
    if 11 in cases:
        site.append(_link(OPTIMALITY_PAPER, f"The {math_html('n = 11')} optimality paper"))
        site.append(_link(LOWER_BOUNDS_PAPER, f"The {math_html('n = 11')} explainer"))

    evidence_rows: list[str] = []
    files: list[str] = []
    entries = _evidence()
    for item in record["evidence"]:
        line = evidence_lines().get(item)
        if line is None:
            raise SystemExit(f"{result.id}: evidence {item} is not in {EVIDENCE.name}")
        evidence_rows.append(_link(_line_url(EVIDENCE, line), f"<code>{_esc(item)}</code>"))
        entry = entries[item]
        proof = entry.get("proof") or {}
        for label, path in (
            ("certificate", entry.get("certificate")),
            ("proof", proof.get("source")),
            ("audit", proof.get("audit_record")),
        ):
            resolved = _resolve(path) if isinstance(path, str) else None
            if resolved is not None:
                link = f"{label} {_path_link(resolved, f'<code>{_esc(resolved.name)}</code>')}"
                if link not in files:
                    files.append(link)

    sources: list[str] = []
    keys = cited_keys(result)
    found = resources((overview.cases[n] for n in cases), keys)
    for key in keys:
        resource = found.get(key) or {}
        beside = []
        if resource.get("url"):
            beside.append(_link(str(resource["url"]), "its own site", str(resource["url"])))
        copy = _local_copy(str(resource["local"])) if resource.get("local") else None
        if copy is not None:
            beside.append(_path_link(copy, "retained copy"))
        sources.append(bibliography_link(key) + (f" ({', '.join(beside)})" if beside else ""))

    packet_links = [_path_link(packet) for packet in packets(result)]
    artifacts = [
        _path_link(resolved)
        for path in [*record["artifacts"], *(record.get("controls") or [])]
        if (resolved := _resolve(path)) is not None
    ]
    shown_artifacts = artifacts
    if len(artifacts) > 20:
        paths = [
            resolved
            for path in [*record["artifacts"], *(record.get("controls") or [])]
            if (resolved := _resolve(path)) is not None
        ]
        directories = sorted({path.parent for path in paths})
        shown_artifacts = [
            f"<p>{len(artifacts)} artifacts and controls in {len(directories)} directories. "
            f"{register_link(result, 'Complete artifact list in the result entry')}. "
            + " ".join(
                _link(repo_url(directory, kind="tree"), _esc(repo_links.relative(directory)))
                for directory in directories
            )
            + "</p>"
        ]
    elif len(artifacts) > ARTIFACTS_OPEN:
        summary = f"{len(artifacts)} artifacts and controls"
        shown_artifacts = [
            f'<details class="site-result-artifacts"><summary>{summary}</summary>'
            + " ".join(artifacts)
            + "</details>"
        ]
    review = record.get("review_artifact")
    reviewed = _resolve(review) if review else None

    case_files: list[str] = []
    if not is_broad(cases):
        for n in cases:
            lines = case_bound_lines(n)
            fields = [
                _link(_line_url(case_file(n), lines[key]), label) for key, label in CASE_BOUNDS
            ]
            case_files.append(f"{_path_link(case_file(n))} ({', '.join(fields)})")
    else:
        case_files.append("each case\u2019s file is linked from its row above")

    github = (
        _row(
            "Register",
            [
                register_link(
                    result,
                    f"{_esc(result.id)} in <code>results.yaml</code>, "
                    f"line {register_line(result)}",
                )
            ],
        )
        + _row("Evidence", evidence_rows)
        + _row("Proofs and certificates", files)
        + _row("Sources", sources)
        + _row("Source packet", packet_links)
        + _row("Artifacts", shown_artifacts)
        + _row("Review", [_path_link(reviewed)] if reviewed else [])
        + _row("Case file", case_files)
    )
    return (
        '<section class="site-result-section site-result-links">'
        '<h3 class="site-result-heading">Links</h3>'
        f'<dl class="site-detail"><dt>On this site</dt><dd>{DOT.join(site)}</dd></dl>'
        '<p class="site-result-subhead">On GitHub, at <code>main</code></p>'
        f'<dl class="site-detail">{github}</dl></section>'
    )


# ---------- The body, and its links checked ----------


def check_links(result_id: str, body: str, overview: Overview) -> None:
    """Refuse a body with a link to nothing: a repository path the working tree lacks, a
    commit-pinned repository link, a page the site does not serve, or a fragment no row
    or record carries."""
    from devtools.overview_sections import result_fragment  # noqa: PLC0415
    from devtools.render_case_pages import CASES_HOME, case_url  # noqa: PLC0415
    from devtools.render_overview import SITE_PAGES  # noqa: PLC0415

    pinned = repo_links.hash_pinned_links(body)
    if pinned:
        raise SystemExit(f"{result_id}: links a commit rather than main: {pinned[:3]}")
    missing = []
    for kind, path in sorted(repo_links.branch_paths(body)):
        if path_kind(path) != ("tree" if kind == "tree" else "blob"):
            missing.append(f"{kind}/{path}")
    ids = {other.id.lower() for other in overview.results}
    fragments = {
        "frontier.html": {f"n-{n}" for n in overview.cases},
        "all-results.html": ids,
    }
    served = {
        *SITE_PAGES,
        CASES_HOME,
        *(case_url(n) for n in overview.cases),
        *(result_fragment(result.id) for result in overview.results),
    }
    for page, fragment in SITE_LINK.findall(body):
        if page not in served:
            missing.append(page)
        elif fragment and fragment not in fragments.get(page, set()):
            missing.append(f"{page}#{fragment}")
    if missing:
        raise SystemExit(
            f"{result_id}: the overview links targets that do not exist: {missing}"
        )


def compatibility_notices(
    result: Result,
    amendments: Sequence[Mapping[str, Any]],
    *,
    registered_paths: Collection[str],
) -> str:
    """Explain an amended address inside the article that readers may fetch."""
    notices = []
    for amendment in amendments:
        target = amendment.get("historical_target")
        if not target:
            continue
        if not isinstance(target, str):
            raise TypeError(f"{result.id}: historical target is not a local path")
        url = urlsplit(target)
        if (
            target not in registered_paths
            or url.scheme
            or url.netloc
            or url.query
            or url.fragment
            or target.startswith("/")
            or any(part in {"", ".", ".."} for part in target.split("/"))
            or "\\" in target
        ):
            raise ValueError(f"{result.id}: unregistered local historical target {target!r}")
        title = amendment.get("historical_title")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"{result.id}: historical target has no reader title")
        kind = str(result.record["kind"]).replace("-", " ")
        updated = _esc(amendment["date"])
        notices.append(
            '<aside class="site-result-section site-result-compatibility" '
            'aria-label="Earlier result at this address"><p><strong>Earlier result at '
            "this address.</strong> Earlier links referred to "
            f'<a href="{_esc(target)}">{_esc(title)}</a>. This page now holds '
            f"a separate {_esc(kind)} result by {_esc(result.credit)}. "
            f'<span class="site-cell-quiet">Address updated '
            f'<time datetime="{updated}">{updated}</time>.</span></p></aside>'
        )
    return "".join(notices)


def result_popover_html(
    result: Result,
    overview: Overview,
    *,
    amendments: Sequence[Mapping[str, Any]] = (),
    registered_paths: Collection[str] = (),
) -> str:
    """The overview of one registered result, as its popover's body: the head, the case
    or cases, the chain of results on them, and the links, every one checked."""
    cases = scope(result)
    body = (
        compatibility_notices(result, amendments, registered_paths=registered_paths)
        + head(result, cases)
        + case_section(result, overview, cases)
        + chain_section(result, overview, cases)
        + links_section(result, overview, cases)
    )
    check_links(result.id, body, overview)
    name = _esc(result.id.lower())
    return f'<div class="site-result" data-result-overview="{name}">{body}</div>'


# ---------- The link audit ----------


class LinkAudit(NamedTuple):
    """What every overview links, counted, and what a deploy from `HEAD` would lack."""

    results: int
    github: int
    """Links into the repository's file tree, every one of which must name `main`."""
    github_paths: int
    """The distinct repository paths those links open."""
    site: int
    """Links to pages of this site, each checked as the body was rendered."""
    external: int
    """Source citations off the site, including first-party issue/discussion reports."""
    off_main: list[str]
    missing: list[str]
    """Repository paths the tree at `HEAD` does not hold, as `kind/path`."""
    sizes: dict[str, int]
    """Each overview's size in bytes of UTF-8, by result: what a page that carries every
    overview gains."""


_HREF = re.compile(r'href="([^"]+)"')


def link_audit(overview: Overview, bodies: Mapping[str, str] | None = None) -> LinkAudit:
    """Render every result's overview and count its links against the tree at `HEAD`,
    which is what `main` holds when the site deploys. Rendering has already checked each
    link against the working tree and the record (`check_links`). `bodies` are the
    overviews by result id where a caller has rendered them already; one it lacks is
    rendered here."""
    tree = repo_links.repository_tree()
    on_main = f"{repo_links.REPO_URL}/"
    branch = re.compile(
        re.escape(repo_links.REPO_URL)
        + r"/(?:blob|tree)/"
        + repo_links.DEFAULT_BRANCH
        + r"(?:/|$)"
    )
    github = site = external = 0
    paths: set[tuple[str, str]] = set()
    off_main: list[str] = []
    sizes: dict[str, int] = {}
    for result in overview.results:
        body = (bodies or {}).get(result.id) or result_popover_html(result, overview)
        sizes[result.id] = len(body.encode("utf-8"))
        for href in _HREF.findall(body):
            if href.startswith(on_main) and not repo_links.is_report_link(href):
                github += 1
                if not branch.match(href):
                    off_main.append(f"{result.id}: {href}")
            elif href.startswith("https://"):
                external += 1
            else:
                site += 1
        paths |= repo_links.branch_paths(body)
    return LinkAudit(
        results=len(overview.results),
        github=github,
        github_paths=len(paths),
        site=site,
        external=external,
        off_main=off_main,
        missing=tree.missing(paths),
        sizes=sizes,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--audit",
        action="store_true",
        help="render every result's overview and count its links against the tree at HEAD",
    )
    args = parser.parse_args(argv)
    if not args.audit:
        parser.error("nothing to do: give --audit")
    status = 0
    if args.audit:
        from devtools import overview_data  # noqa: PLC0415

        audit = link_audit(overview_data.load())
        print(
            f"{audit.results} result overviews: {audit.github} GitHub links to "
            f"{audit.github_paths} paths on {repo_links.DEFAULT_BRANCH}, {audit.site} links "
            f"to pages of this site, {audit.external} links off the site"
        )
        ordered = sorted(audit.sizes.items(), key=lambda item: item[1])
        (small, least), (_, median), (large, most) = (
            ordered[0],
            ordered[len(ordered) // 2],
            ordered[-1],
        )
        print(
            f"sizes: {sum(audit.sizes.values()) // 1024} KB in all, from {least // 1024} KB "
            f"({small}) to {most // 1024} KB ({large}), median {median // 1024} KB"
        )
        for problem in audit.off_main:
            print(f"not on {repo_links.DEFAULT_BRANCH}: {problem}", file=sys.stderr)
        for problem in audit.missing:
            print(f"not in the tree at HEAD: {problem}", file=sys.stderr)
        if audit.off_main or audit.missing:
            status = 1
        else:
            print("every link resolves")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
