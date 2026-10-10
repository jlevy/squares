"""The result overview: every part present, every link resolving, nothing borrowed from
the popover that will hold it."""

from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import replace
from decimal import ROUND_FLOOR, Decimal
from unittest.mock import patch
from urllib.parse import urljoin

import pytest

from devtools import (
    overview_data,
    overview_sections,
    register_prose,
    render_case_pages,
    render_frontier_page,
    render_overview,
    repo_links,
    result_overview,
    site_assets,
    site_urls,
)
from devtools.render_case_pages import BROAD_RESULT
from devtools.render_recent_results import HOLDS, NO_STANDING, SUPERSEDED
from devtools.repo_links import DEFAULT_BRANCH, REPO, REPO_URL
from sqpack.yamlio import safe_load
from tests import site_renders

#: The three results the tests read part by part: one that settles a case, the result it
#: superseded on the same case, and one about 49 cases.
SETTLED, EARLIER, BROAD = "T-060", "T-037", "T-056"

HREF = re.compile(r'href="([^"]+)"')
LINE_LINK = re.compile(re.escape(REPO_URL) + r"/blob/main/([^\"?#]+)\?plain=1#L(\d+)")
STEP = re.compile(
    r'<li class="site-result-step" data-step="(t-\d{3})" data-standing="([a-z-]*)"'
)


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


@pytest.fixture(scope="module")
def bodies() -> dict[str, str]:
    """Every register result's overview, rendered once: that none fails is the first check."""
    return site_renders.result_bodies()


@pytest.fixture(scope="module")
def complete_pages() -> dict[str, str]:
    """The complete registered documents, shared with the head-contract tests."""
    return {page.name: page.html for page in site_renders.result_pages()}


def _result(overview: overview_data.Overview, result_id: str) -> overview_data.Result:
    return next(result for result in overview.results if result.id == result_id)


def test_every_register_result_has_an_overview(bodies: dict[str, str]) -> None:
    register = safe_load(overview_data.RESULTS.read_text(encoding="utf-8"))["results"]
    assert set(bodies) == {record["id"] for record in register}
    for result_id, body in bodies.items():
        assert body.startswith(
            f'<div class="site-result" data-result-overview="{result_id.lower()}">'
        )
        assert body.endswith("</div>")
        # The body is placed in a Markdown HTML block, which a blank line would end.
        assert "\n\n" not in body, result_id
        assert not re.search(r"\{\{[A-Z_]+\}\}", body), result_id


@pytest.mark.parametrize("result_id", [SETTLED, EARLIER, BROAD])
def test_the_head_states_the_result_as_the_site_does(
    result_id: str, overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    """The claim with its math set, the rung and standing chips of the tables, the date
    and what it dates, and the register's credit. The id and the headline are not
    repeated: the popover that holds the body carries them, above it."""
    result = _result(overview, result_id)
    record = result.record
    head = bodies[result_id].split("</header>", 1)[0]
    assert head.startswith(
        f'<div class="site-result" data-result-overview="{result_id.lower()}">'
        '<header class="site-result-head"><p class="site-result-status">'
    )
    assert "site-card-label" not in head
    assert "site-popover-value" not in head
    # One paragraph element for each paragraph of the claim, in order.
    paragraphs = register_prose.paragraphs(record["claim"])
    claim = "".join(
        f'<p class="site-result-claim">{overview_data.tex_bounds(paragraph)}</p>'
        for paragraph in paragraphs
    )
    assert claim in head
    assert head.count('<p class="site-result-claim">') == len(paragraphs)
    assert "kpress-math" in claim
    assert overview_sections.status_chips(result) in head
    # Significance first, then verification and confirmation (think-ucon).
    rungs = (
        f"S{record['significance']['score']}",
        record["verification"],
        record["confirmation"],
    )
    # Significance is its mark, the others chips (`think-m3m4`).
    places = [
        head.index(
            f'<span class="site-significance-label" aria-hidden="true">{rung}</span>'
            if rung[0] == "S"
            else f'data-rung="{rung[0]}" data-level="{rung[1:]}">{rung}</span>'
        )
        for rung in rungs
    ]
    assert places == sorted(places)
    status = head.split('<p class="site-result-status">', 1)[1].split("</p>", 1)[0]
    assert status.startswith(overview_sections.rung_chips(result))
    # A result that still stands draws no standing chip, here as in the tables.
    assert status == overview_sections.status_chips(result)
    assert ">current best<" not in status
    # The date leads and what it dates follows, as a table's date cell sets it.
    kind, dated = result.dated
    meta = head.split('<p class="site-result-meta">', 1)[1].split("</p>", 1)[0]
    assert meta.startswith(f'{dated} <span class="site-date-kind">{kind}</span> \u00b7 ')
    assert overview_sections.date_cell(result) in meta
    assert html.escape(result.credit) in head
    assert "Significance" in head
    assert f'data-novelty="{result.novelty}"' in head


def test_the_head_says_what_a_declared_later_result_implies(bodies: dict[str, str]) -> None:
    """A result whose entry declares a later result that implies it (`superseded_by`)
    says so under its claim, with the later result linked and what it implies: T-060
    implies T-036's bound clause and not its equality clause (think-7df0). A superseded
    bound says nothing there; its chip names its successors."""
    head = bodies["T-036"].split("</header>", 1)[0]
    later = (
        '<p class="site-result-claim site-result-superseded"><strong>Superseded in part by '
        f'<a href="{overview_sections.result_url("T-060")}">T-060</a>.</strong> The first '
        "clause"
    )
    assert later in head
    assert "is not implied, since T-060 makes no claim of uniqueness." in head
    assert head.index(later) > head.index('<p class="site-result-claim">')
    assert head.index(later) < head.index('<details class="site-result-more">')
    assert "site-result-superseded" not in bodies["T-037"]
    successor = f'by <a href="{overview_sections.result_url("T-060")}">T-060</a>'
    assert successor in bodies["T-037"].split("</header>", 1)[0]


@pytest.mark.parametrize("result_id", [SETTLED, EARLIER])
def test_a_single_case_shows_the_films_panel_and_the_packing(
    result_id: str, bodies: dict[str, str]
) -> None:
    """The case is its visual summary, as its record opens (`render_case_pages.
    visual_summary`): the atlas drawing of the case first, then the number line, the
    chained bound, the badges and the citation, from the film's own facts; the case
    record's verified and reported bounds and the gap follow."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    body = bodies[result_id]
    fact = result_overview.film_facts()[11]
    assert body.count('class="site-atlas-pop site-result-film" data-overview-case="11"') == 1
    assert packing_svg(11, units=overview_sections.ATLAS_UNITS) in body
    assert body.index("<svg") < body.index('<div class="site-atlas-gap">')
    # The gap bar: the scale's integers, sqrt(n) and sqrt(n) + 1, and the best known side.
    bar = body.split('<div class="site-atlas-gap">', 1)[1].split("site-atlas-pop-head", 1)[0]
    for label in ("3", "4", "5", "3.317", "4.317"):
        assert f">{label}</span>" in bar, label
    assert '<span class="is-upper" style="left: ' in bar
    assert ">3.877</span>" in bar
    assert bar.count('class="site-atlas-gap-rule"') == 1  # exact: one rule, no lower
    # The chained bound, as the film states it, with its star and badges.
    assert overview_data.math_html("s(11) ={}") in body
    assert (
        '<span class="is-upper is-exact-value">'
        f"{overview_data.math_html(fact['upper'])}</span>" in body
    )
    assert '<span class="site-atlas-pop-star" aria-hidden="true">\u2605</span>' in body
    for _, _, label in fact["badges"]:
        assert f"</span>{label}</li>" in body
    for which in ("lower", "upper"):
        assert html.escape(fact["cite"][which]["text"]) in body
    # The record's four bounds and its gap, each a link into the case file's frontmatter.
    table = body.split('class="site-result-bounds"', 1)[1].split("</div></div></div>", 1)[0]
    assert table.count('role="row"') == 4
    lines = result_overview.case_bound_lines(11)
    for key, _ in result_overview.CASE_BOUNDS:
        assert f"packing/frontier/n-011.md?plain=1#L{lines[key]}" in table
    assert "solved: the verified bounds meet" in table


def test_an_open_case_draws_both_bounds_and_the_span_between(bodies: dict[str, str]) -> None:
    """T-057, de Winter's 211 squares: the proved lower bound and the best known side each
    get a rule and a value, with the open span between them, and the statement chains
    them."""
    body = bodies["T-057"]
    fact = result_overview.film_facts()[211]
    bar = body.split('<div class="site-atlas-gap">', 1)[1].split("site-atlas-pop-head", 1)[0]
    assert bar.count('class="site-atlas-gap-rule"') == 2
    lower = Decimal(fact["lower"])
    gap_lower = lower.quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
    assert f">{gap_lower}</span>" in bar
    assert f">{float(fact['upper']):.3f}</span>" in bar
    assert '<span class="site-atlas-gap-open" style="left: ' in bar
    bound_lower = str(lower.quantize(Decimal("0.00001"), rounding=ROUND_FLOOR))
    assert (
        f'<span class="{result_overview.contribution_class(211, "lower")}">'
        f"{overview_data.math_html(bound_lower)}</span>" in body
    )
    assert overview_data.math_html(r"{}\le s(211) \le{}") in body
    assert (
        f'<span class="{result_overview.contribution_class(211, "upper")}">'
        f"{overview_data.math_html(fact['upper'])}</span>" in body
    )


def _case_cells(body: str) -> dict[int, list[ET.Element]]:
    """Expand native row spans as a reader does, rejecting gaps and excess cells."""
    match = re.search(r'<table class="site-result-cases".*?</table>', body)
    assert match is not None
    table = ET.fromstring(match[0])
    assert table.attrib["aria-label"] == "The cases of this result"
    headings = table.findall("./thead/tr/th")
    assert [heading.text for heading in headings] == [
        "n",
        "Proved lower",
        "Best known",
        "Gap",
        "Status",
        "Records",
    ]
    assert all(heading.attrib == {"scope": "col"} for heading in headings)
    pending: dict[int, tuple[ET.Element, int]] = {}
    expanded = {}
    for row in table.findall("./tbody/tr"):
        n = int(row.attrib["data-overview-case"])
        assert n not in expanded
        physical = iter(row)
        cells = []
        for column in range(6):
            if column in pending:
                cell, left = pending.pop(column)
                if left > 1:
                    pending[column] = cell, left - 1
            else:
                cell = next(physical)
                assert cell.tag == "td"
                assert "colspan" not in cell.attrib
                count = int(cell.attrib.get("rowspan", "1"))
                assert count > 0
                if count > 1:
                    assert 1 <= column <= 4
                    pending[column] = cell, count - 1
            cells.append(cell)
        assert next(physical, None) is None
        expanded[n] = cells
    assert not pending
    return expanded


def _inner(cell: ET.Element) -> str:
    return (cell.text or "") + "".join(ET.tostring(child, encoding="unicode") for child in cell)


def _assert_case_values(cases: list[int], overview: overview_data.Overview, body: str) -> None:
    rows = _case_cells(body)
    assert list(rows) == cases
    facts = result_overview.film_facts()
    for n, cells in rows.items():
        fact, case = facts[n], overview.cases[n]
        lower = fact["lower"] if fact["lower"] is not None else fact["upper"]
        assert cells[0][0].attrib["href"] == f"cases/{n}.html"
        assert cells[0][0].text == str(n)
        assert cells[1].attrib["class"] == result_overview.contribution_class(
            n, "lower"
        ).removeprefix("is-")
        assert cells[1].text == lower
        stars = cells[1].findall("span[@class='site-star']")
        assert bool(stars) is fact["star"]
        if stars:
            assert len(stars) == 1
            assert stars[0].attrib == {"class": "site-star", "title": "Recent result"}
            assert stars[0].text == "★"
        assert cells[2].attrib["class"] == result_overview.contribution_class(
            n, "upper"
        ).removeprefix("is-")
        assert cells[2].text == fact["upper"]
        _, gap = render_frontier_page.gap(case)
        assert cells[3].text == render_frontier_page.decimal_text(Decimal(gap).normalize())
        expected_status = ET.fromstring(
            "<td>"
            + overview_sections.case_status_chip(case["status"])
            + result_overview.case_badges(n)
            + "</td>"
        )
        assert _inner(cells[4]) == _inner(expected_status)
        assert cells[5].attrib["class"] == "records"
        assert [(link.attrib["href"], link.text) for link in cells[5].findall("a")] == [
            (f"atlas.html#n-{n}", "frontier"),
            (repo_links.repo_url(result_overview.case_file(n)), f"n-{n:03d}.md"),
        ]


def test_a_broad_result_lists_its_cases_instead_of_drawing_them(
    overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    """Couzo's 49 packings: no number line and no drawing, a sentence saying so, and one
    row per case linking its record, its frontier row and its case file."""
    body = bodies[BROAD]
    cases = result_overview.scope(_result(overview, BROAD))
    assert len(cases) == 49 > BROAD_RESULT
    assert "site-atlas-gap" not in body
    assert "<svg" not in body
    assert "This result concerns 49 cases, too many to draw one by one." in body
    assert re.findall(r'data-overview-case="(\d+)"', body) == [str(n) for n in cases]
    _assert_case_values(cases, overview, body)


def test_a_broad_report_keeps_its_full_payload_within_the_canonical_page_budget(
    overview: overview_data.Overview,
) -> None:
    """T-124's complete broad report fits without losing cases, chain or source links."""
    result = _result(overview, "T-124")
    cases = result_overview.scope(result)
    assert len(cases) == 178
    body = result_overview.result_popover_html(result, overview)
    _assert_case_values(cases, overview, body)
    assert 'rowspan="' in body
    for paragraph in register_prose.paragraphs(result.record["claim"]):
        assert f'<p class="site-result-claim">{overview_data.tex_bounds(paragraph)}</p>' in body
    for label, value in (
        ("Significance", result.record["significance"]["rationale"]),
        ("Composition", result.record.get("composition")),
        ("Next rung", result.record.get("next_rung")),
    ):
        if value:
            assert f"<dt>{label}</dt><dd>{result_overview.prose_html(value)}</dd>" in body
    members = result_overview.chain(overview, cases)
    assert len(members) >= 67
    assert [identity for identity, _ in STEP.findall(body)] == [
        member.id.lower() for member in members
    ]
    for member in members:
        step = body.split(f'data-step="{member.id.lower()}"', 1)[1].split("</li>", 1)[0]
        assert overview_data.tex_bounds(member.summary) in step
        assert html.escape(member.credit) in step
        shared = [n for n in result_overview.scope(member) if n in cases]
        if len(shared) <= result_overview.CASES_NAMED:
            label = "case " if len(shared) == 1 else "cases "
            assert label + ", ".join(map(str, shared)) in step.split("</p>", 1)[0]
    pages = list(render_overview.iter_result_fragments(result_ids=frozenset({result.id})))
    assert len(pages) == 1
    page = pages[0]
    assert page.name == "result/t-124.html"
    row = next(row for row in site_urls.load_registry() if row.path == page.name)
    assert site_urls.page_budget(row) == 300_000
    assert len(page.html.encode("utf-8")) <= site_urls.page_budget(row)
    article = page.html.split('<article class="site-result"', 1)[1].split("</article>", 1)[0]
    assert re.findall(r'data-overview-case="(\d+)"', article) == [str(n) for n in cases]
    assert STEP.findall(article) == STEP.findall(body)
    expected_links = Counter(html.unescape(link) for link in HREF.findall(body))
    ordered = sorted(overview.results, key=lambda other: other.id)
    index = next(i for i, other in enumerate(ordered) if other.id == result.id)
    for offset, relation in ((-1, "prev"), (1, "next")):
        neighbor_href = re.search(rf'rel="{relation}" href="([^"]+)"', article)
        neighbor_index = index + offset
        if not 0 <= neighbor_index < len(ordered):
            assert neighbor_href is None
            continue
        neighbor = ordered[neighbor_index].id
        target = overview_sections.result_fragment(neighbor)
        expected_links[target] += 1
        assert neighbor_href is not None
        assert urljoin(page.name, html.unescape(neighbor_href[1])) == target
    assert (
        Counter(urljoin(page.name, html.unescape(link)) for link in HREF.findall(article))
        == expected_links
    )


@pytest.mark.parametrize("result_id", [BROAD, "T-124"])
def test_repository_links_keep_explanatory_titles(
    result_id: str, overview: overview_data.Overview
) -> None:
    result = _result(overview, result_id)
    link = result_overview.register_link(result)
    assert f'title="{result_id} in results.yaml"' in link
    assert f"results.yaml?plain=1#L{result_overview.register_line(result)}" in link


def test_repository_links_do_not_repeat_a_title_already_in_the_target(
    overview: overview_data.Overview,
) -> None:
    result = _result(overview, "T-124")
    key = result.record["attribution"]["source_keys"][0]
    link = result_overview.bibliography_link(key)
    line = result_overview.bibliography_lines()[key]
    assert f"bibliography.yaml?plain=1#L{line}" in link
    assert html.escape(key.strip("[]")) in link
    assert "title=" not in link


def test_a_result_about_a_few_cases_draws_each(bodies: dict[str, str]) -> None:
    """T-019 concerns n = 17, 18 and 19: three panels, each headed by its n."""
    body = bodies["T-019"]
    assert re.findall(r'site-result-film" data-overview-case="(\d+)"', body) == [
        "17",
        "18",
        "19",
    ]
    assert body.count('<div class="site-atlas-gap">') == 3
    assert body.count('class="site-popover-value site-result-case-n"') == 3


@pytest.mark.parametrize("result_id", [SETTLED, EARLIER, BROAD])
def test_the_chain_is_every_result_on_the_case_oldest_first(
    result_id: str, overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    """Each step names its result, links its row, and carries its kind and its status;
    the result the overview is about is marked; and each step links the register entry
    at its line."""
    result = _result(overview, result_id)
    cases = set(result_overview.scope(result))
    expected = [
        other for other in overview.results if cases & set(result_overview.scope(other))
    ]
    expected.sort(key=lambda other: (other.dated[1], other.id))
    body = bodies[result_id]
    steps = STEP.findall(body)
    assert [step for step, _ in steps] == [other.id.lower() for other in expected]
    assert len(steps) > 1
    assert body.count('data-current=""') == 1
    current = body.split('data-current=""', 1)[0].rsplit("<li ", 1)[1]
    assert f'data-step="{result_id.lower()}"' in current
    lines = result_overview.result_lines()
    for other in expected:
        step = body.split(f'data-step="{other.id.lower()}"', 1)[1].split("</li>", 1)[0]
        assert f'<a href="all-results.html#{other.id.lower()}">{other.id}</a>' in step
        # A step's date leads and what it dates follows, then the id, as in the tables.
        dated = overview_sections.date_cell(other)
        assert f'<p class="site-result-step-head">{dated} <a href=' in step
        assert not re.search(r'class="site-date-kind">\w+</span> [\d-]+', step)
        assert overview_data.tex_bounds(other.summary) in step
        # Where the result stands here as it does as a whole, its marks name only the
        # results that supersede it on these cases (`result_overview.supersessions_on`).
        shared = sorted(cases & set(result_overview.scope(other)))
        here = result_overview.standing_on(other, shared)
        shown = (
            replace(other, supersessions=result_overview.supersessions_on(other, shared))
            if here == other.standing
            else other
        )
        assert overview_sections.kind_and_status(shown) in step
        assert f"packing/frontier/results.yaml?plain=1#L{lines[other.id]}" in step
        assert html.escape(other.credit) in step
        for key in (other.record.get("attribution") or {}).get("source_keys") or []:
            assert html.escape(key.strip("[]")) in step


def test_the_chain_on_eleven_squares_says_how_each_result_stands_there(
    overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    """T-060 holds the case, and T-037 and T-047 are superseded. T-047 was the current best
    at other cases until 2026-10-02, when wand125's replayed rectangle certificates
    (T-045, T-070) took the last two it held, n = 26 and 29; superseded everywhere, its
    step draws the chip and has nothing to add about this case."""
    steps = dict(STEP.findall(bodies[SETTLED]))
    assert steps["t-060"] == overview_sections.standing_key(HOLDS)
    assert steps["t-037"] == overview_sections.standing_key(SUPERSEDED)
    wide = _result(overview, "T-047")
    assert wide.standing == SUPERSEDED
    assert result_overview.standing_on(wide, [11]) == SUPERSEDED
    step = bodies[SETTLED].split('data-step="t-047"', 1)[1].split("</li>", 1)[0]
    assert overview_sections.is_superseded(wide)
    assert ">superseded<" in step
    assert "on this case" not in step
    assert steps["t-047"] == overview_sections.standing_key(SUPERSEDED)


def test_a_chain_step_says_both_standings_of_a_result_that_holds_elsewhere(
    overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    """T-069 is the current best at other cases and superseded at n = 92 by the source's
    later certificate (T-075), and its step in that chain says both. T-047 on n = 11 was
    this test's case until 2026-10-02, when it stopped holding anywhere, and T-045 on
    n = 32 until 2026-10-05, when T-096's replay took n = 18, the last count it held."""
    steps = dict(STEP.findall(bodies["T-075"]))
    assert steps["t-075"] == overview_sections.standing_key(HOLDS)
    wide = _result(overview, "T-069")
    assert wide.standing == HOLDS
    assert result_overview.standing_on(wide, [92]) == SUPERSEDED
    step = bodies["T-075"].split('data-step="t-069"', 1)[1].split("</li>", 1)[0]
    # A result that still stands draws no chip, so the step has none for its standing
    # elsewhere and says in words how it stands on this case.
    assert not overview_sections.is_superseded(wide)
    assert ">current best<" not in step
    assert ">superseded<" not in step
    # T-075's chain spans several cases, so the words are for all of them.
    assert "on these cases, superseded by <a href=" in step
    assert steps["t-069"] == overview_sections.standing_key(SUPERSEDED)


def test_a_result_superseded_in_part_stays_current_in_its_chain(
    bodies: dict[str, str],
) -> None:
    """T-036, which T-060 supersedes only in part, is current in n = 11's chain, and its
    step says it is superseded in part, by T-060, linked (think-7df0)."""
    steps = dict(STEP.findall(bodies[SETTLED]))
    t060 = f'<a href="{overview_sections.result_url("T-060")}">T-060</a>'
    assert steps["t-036"] != overview_sections.standing_key(SUPERSEDED)
    t036 = bodies[SETTLED].split('data-step="t-036"', 1)[1].split("</li>", 1)[0]
    in_part = 'data-standing="superseded-in-part">superseded</span>'
    assert f'{in_part} <span class="site-cell-quiet">in part by {t060}' in t036


def test_a_result_that_is_no_bound_is_not_set_back_in_its_chain(
    overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    """T-003, the limit of a method, derives `superseded` from the bound it cites, and no
    later bound supersedes a method's limit: its row is current, and its step in n = 17's
    chain is not set back as a superseded step is (`think-rf21`)."""
    limit = _result(overview, "T-003")
    assert limit.standing == SUPERSEDED
    assert not overview_sections.is_superseded(limit)
    steps = dict(STEP.findall(bodies["T-043"]))
    assert steps["t-003"] == overview_sections.standing_key(NO_STANDING)
    assert steps["t-019"] == overview_sections.standing_key(SUPERSEDED)


def test_a_chain_names_only_the_successors_on_its_own_cases(bodies: dict[str, str]) -> None:
    """T-019 is about n = 17 to 19 and superseded on each; on n = 17's chain its step
    names only the result on that case that supersedes it now, T-093, which replaced
    T-043 on 2026-10-05 (think-6zg1), not those that supersede it at n = 18 or 19."""
    step = bodies["T-043"].split('data-step="t-019"', 1)[1].split("</li>", 1)[0]
    chips = step.split('<p class="site-result-step-chips">', 1)[1].split("</p>", 1)[0]
    assert re.findall(r'href="all-results\.html#(t-\d+)"', chips) == ["t-093"]


@pytest.mark.parametrize("result_id", [SETTLED, EARLIER, BROAD])
def test_the_links_reach_the_site_and_the_record(
    result_id: str, overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    result = _result(overview, result_id)
    record = result.record
    links = bodies[result_id].split('class="site-result-section site-result-links"', 1)[1]
    assert f'<a href="all-results.html#{result_id.lower()}">' in links
    if result_id == BROAD:
        assert '<a href="atlas.html#the-frontier-survey">' in links
        assert 'href="cases/"' not in links
    else:
        assert '<a href="cases/11.html">' in links
        assert '<a href="atlas.html#n-11">' in links
        # Both papers on the case, the one on the result that stands first, each where
        # it is served under `papers/`.
        paper = f'<a href="{overview_sections.OPTIMALITY_PAPER}">'
        assert paper in links
        explainer = '<a href="papers/n11-lower-bounds-explainer.html">'
        assert links.index(paper) < links.index(explainer)
        assert f'{REPO_URL}/blob/main/packing/frontier/n-011.md"' in links
    line = result_overview.result_lines()[result_id]
    assert f"packing/frontier/results.yaml?plain=1#L{line}" in links
    assert f"line {line}" in links
    for item in record["evidence"]:
        at = result_overview.evidence_lines()[item]
        assert f"packing/frontier/evidence.yaml?plain=1#L{at}" in links, item
        assert f"<code>{item}</code>" in links
    for key in record["attribution"]["source_keys"]:
        at = result_overview.bibliography_lines()[key]
        assert f"packing/resources/bibliography.yaml?plain=1#L{at}" in links, key
    for path in [*record["artifacts"], *record["controls"]]:
        assert f'{REPO_URL}/blob/main/{path}"' in links, path
    assert "README.md" in links.split("Source packet", 1)[1].split("</dd>", 1)[0]
    if record.get("review_artifact"):
        assert f'{REPO_URL}/blob/main/{record["review_artifact"]}"' in links


def test_every_github_link_names_main_and_a_path_in_the_tree(bodies: dict[str, str]) -> None:
    """No overview links a commit, every repository link is a `blob` or `tree` on `main`,
    and every path is in the tree at `HEAD`, which `main` holds when the site deploys."""
    tree = repo_links.repository_tree()
    on_main = re.compile(re.escape(REPO_URL) + rf"/(?:blob|tree)/{DEFAULT_BRANCH}/")
    total = 0
    for result_id, body in bodies.items():
        assert not repo_links.hash_pinned_links(body), result_id
        github = [
            href
            for href in HREF.findall(body)
            if href.startswith(REPO_URL + "/") and not repo_links.is_report_link(href)
        ]
        assert github, result_id
        total += len(github)
        for href in github:
            assert on_main.match(href), (result_id, href)
        paths = repo_links.branch_paths(body)
        assert paths
        assert not tree.missing(paths), (result_id, tree.missing(paths))
    assert total > 1000


def test_source_reports_do_not_relax_main_pin_or_missing_file_guards(
    overview: overview_data.Overview,
) -> None:
    sample = replace(overview, results=[_result(overview, SETTLED)])
    reports = [
        f"{REPO_URL}/issues/401",
        f"{REPO_URL}/issues/401#issuecomment-6031977107",
        f"{REPO_URL}/discussions/12",
        f"{REPO_URL}/discussions/12#discussioncomment-345",
    ]
    pinned = f"{REPO_URL}/blob/0123456789abcdef0123456789abcdef01234567/README.md"
    non_main = f"{REPO_URL}/tree/review/packing"
    missing = "packing/frontier/no-such-source-report-artifact.md"
    urls = [
        *reports,
        pinned,
        non_main,
        f"{REPO_URL}/blob/main/{missing}",
        f"{REPO_URL}/blob/main/README.md",
    ]
    body = "".join(f'<a href="{url}">citation</a>' for url in urls)
    audit = result_overview.link_audit(sample, {SETTLED: body})
    assert audit.external == 4
    assert audit.github == 4
    assert audit.off_main == [f"{SETTLED}: {pinned}", f"{SETTLED}: {non_main}"]
    assert audit.missing == [f"blob/{missing}"]
    assert repo_links.hash_pinned_links(body) == [pinned]
    assert repo_links.branch_paths(body) == {("blob", missing), ("blob", "README.md")}


def test_every_line_anchor_opens_the_entry_it_names(bodies: dict[str, str]) -> None:
    """A line link into the register, the evidence, the bibliography or a case file lands
    on the entry or the field, read from the files as they are."""
    texts: dict[str, list[str]] = {}
    seen: set[str] = set()
    for result_id, body in bodies.items():
        own = False
        for path, number in LINE_LINK.findall(body):
            if path not in texts:
                texts[path] = (REPO / path).read_text(encoding="utf-8").splitlines()
            line = texts[path][int(number) - 1]
            name = path.rsplit("/", 1)[-1]
            seen.add(name if not name.startswith("n-") else "case file")
            if name == "results.yaml":
                assert re.fullmatch(r"  - id: T-\d{3}", line), (result_id, line)
                own = own or line == f"  - id: {result_id}"
            elif name == "evidence.yaml":
                assert re.fullmatch(r"  - id: E-[a-z0-9-]+", line), (result_id, line)
            elif name == "bibliography.yaml":
                assert re.fullmatch(r"  - key: '\[.+\]'", line), (result_id, line)
            else:
                assert re.fullmatch(r"n-\d{3}\.md", name), path
                assert re.match(r"  (verified|reported)_(lower|upper)_bound:", line), line
        assert own, f"{result_id} does not link its own register entry"
    assert seen == {"results.yaml", "evidence.yaml", "bibliography.yaml", "case file"}


def test_every_site_link_is_a_served_page_and_a_real_fragment(
    overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    rows = {result.id.lower() for result in overview.results}
    cases = {f"n-{n}" for n in overview.cases}
    records = {render_case_pages.case_url(n) for n in overview.cases}
    for result_id, body in bodies.items():
        for href in HREF.findall(body):
            if href.startswith("https://"):
                continue
            page, _, fragment = href.partition("#")
            if page in records or page == render_case_pages.CASES_HOME:
                assert not fragment, href
                continue
            assert page in render_overview.SITE_PAGES, (result_id, href)
            if page == render_overview.RESULTS_PAGE:
                assert fragment in rows, href
            elif page == "atlas.html":
                assert fragment == "the-frontier-survey" or fragment in cases, href
            else:
                assert page in {
                    overview_sections.LOWER_BOUNDS_PAPER,
                    overview_sections.OPTIMALITY_PAPER,
                }, href
                assert not fragment


def test_a_partial_checkout_renders_the_same_records_and_overviews(
    overview: overview_data.Overview,
    bodies: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The deployed site is rendered from a checkout without the literature archive's
    and the campaign's directories (`pages.yml`). Every record link a full checkout
    writes is written there too: a result's source, review and packet in its row, and
    its certificate, proof, retained copy and source packet in its overview. Asking the
    disk alone dropped twenty of them from each results table on the live site."""
    site_renders.leave_out_the_archive_and_the_campaign(monkeypatch)
    partial = overview_data.load()
    for result, there in zip(overview.results, partial.results, strict=True):
        assert there.records == result.records, result.id
    for result_id in (SETTLED, EARLIER, BROAD):
        body = result_overview.result_popover_html(_result(partial, result_id), partial)
        assert body == bodies[result_id], result_id
    assert "resources/web/n11-optimality-2026-09-29/README.md" in bodies[SETTLED]


def test_a_link_to_nothing_fails_the_render(overview: overview_data.Overview) -> None:
    """The check a render runs: a path the tree lacks, a commit, a page the site does not
    serve and a fragment no row carries are each refused."""
    check = result_overview.check_links
    check("T-000", f'<a href="{REPO_URL}/blob/main/README.md">ok</a>', overview)
    refused = (
        f'<a href="{REPO_URL}/blob/main/packing/frontier/n-999.md">x</a>',
        f'<a href="{REPO_URL}/tree/main/README.md">x</a>',
        f'<a href="{REPO_URL}/blob/0123456789abcdef/README.md">x</a>',
        '<a href="nowhere.html">x</a>',
        '<a href="cases/999.html">x</a>',
        '<a href="cases.html#n-11">x</a>',
        '<a href="all-results.html#t-999">x</a>',
    )
    for body in refused:
        with pytest.raises(SystemExit):
            check("T-000", body, overview)


def test_the_overview_depends_on_no_popover(bodies: dict[str, str]) -> None:
    """The body is content alone: no id, popover or script of its own. A broad case
    list's native table has no interactive result-row hooks, so any page may place the
    body more than once. The module calls nothing of the row mechanism that shows it."""
    for result_id, body in bodies.items():
        assert not re.search(r'\sid="', body), result_id
        assert "popover" not in re.sub(r'class="[^"]*"', "", body), result_id
        for tag in ("<script", "<iframe", "<button"):
            assert tag not in body, (result_id, tag)
        assert not re.search(r"\sdata-(result|n|case|atlas-(?!open))[=\s>]", body), result_id
        for tag in re.findall(r"<table[^>]*>", body):
            assert tag == (
                '<table class="site-result-cases" aria-label="The cases of this result">'
            ), result_id
    source = (render_overview.PACKING / "devtools" / "result_overview.py").read_text(
        encoding="utf-8"
    )
    assert "result_row_popover_body" not in source
    assert "import overview_sections" not in source.split('"""', 2)[2].split("\ndef ", 1)[0]


def test_the_gap_bar_keeps_the_films_scale() -> None:
    """The bar is placed here, the one place it is drawn since the atlas popover's script
    stopped drawing its own on 2026-10-03, on the film's scale: from one below the grid
    bound, two units across, inset five percent each side, its values to three places."""
    script = render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8")
    assert "drawGap" not in script
    assert (result_overview.GAP_INSET, result_overview.GAP_SPAN) == (5, 2)
    assert [result_overview.grid_floor(n) for n in (1, 2, 4, 5, 11, 16, 17)] == [
        0,
        1,
        1,
        2,
        3,
        3,
        4,
    ]
    assert result_overview.bar_at(3, 3) == 5
    assert result_overview.bar_at(4, 3) == 50
    assert result_overview.bar_at(5, 3) == 95
    assert result_overview.bar_at(9, 3) == 95
    assert result_overview.bar_number(18.0) == "18"
    assert result_overview.bar_number(3.8770836) == "3.877"


def test_compact_lower_labels_keep_recorded_facts_and_gap_positions() -> None:
    fact = dict(overview_sections.atlas_film_facts()[16])
    original = dict(fact)
    bar = result_overview.gap_bar(fact)
    bound = result_overview.film_bound(fact)
    assert ">4.66</span>" in bar
    assert "4.66044" in bound
    assert "4.660442" not in bound
    at = result_overview.bar_at(float(str(fact["lower"])), result_overview.grid_floor(17))
    assert f"left: {at:.3f}%" in bar
    assert fact == original


def test_two_close_values_sit_either_side_of_their_marks() -> None:
    """Values that would overlap centred on their marks are anchored apart."""
    near = {"n": 17, "exact": False, "upper": "4.675531", "lower": "4.660440"}
    bar = result_overview.gap_bar(near)
    lower = result_overview.contribution_class(17, "lower")
    upper = result_overview.contribution_class(17, "upper")
    assert f'<span class="{lower}" data-anchor="end"' in bar
    assert f'<span class="{upper}" data-anchor="start"' in bar
    far = {"n": 211, "exact": False, "upper": "14.997961", "lower": "14.100000"}
    assert "data-anchor" not in result_overview.gap_bar(far)


def test_the_stylesheet_is_its_own_file_on_the_sites_tokens() -> None:
    """The overview's styles ride every site page after `site.css`, declare no text token
    and no colour of their own, key on no system theme and add no hover timing."""
    css = render_overview.SITE_RESULT_CSS.read_text(encoding="utf-8")
    assert render_overview.SITE_RESULT_CSS.name == "site-result.css"
    # Each is a shared stylesheet the head links, `site.css` first, and the head with
    # them put back in it carries their text in that order.
    head, _ = render_overview.page_assets()
    assets = site_assets.shared().assets
    links = [
        site_assets.stylesheet_tag(assets.stylesheet_file(path), "index.html")
        for path in (render_overview.SITE_CSS, render_overview.SITE_RESULT_CSS)
    ]
    assert [head.count(link) for link in links] == [1, 1]
    assert head.index(links[0]) < head.index(links[1])
    whole = assets.inlined(head)
    site = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert whole.index(site) < whole.index(css)
    assert render_overview.SITE_RESULT_CSS in render_overview.RENDER_INPUTS
    assert "prefers-color-scheme" not in css
    assert "transition" not in css
    for owned in (
        "--kpress-host-font-size-base:",
        "--kpress-measure:",
        "--kpress-font-size-h2:",
    ):
        assert owned not in css
    rules = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|oklch\(|rgb\(|hsl\(", rules)
    assert not re.search(r"^\s*--[a-z-]+:", rules, flags=re.MULTILINE)
    assert ".site-popover:has(.site-result, [data-row-pop-src])" in rules
    # The panel's height has one limit. `max-height` is the same property as
    # `max-block-size` here, and the later of the two in a rule is the one that holds.
    opened = rules.split(
        ".site-popover:has(.site-result, [data-row-pop-src]):popover-open {", 1
    )[1]
    opened = opened.split("}", 1)[0]
    assert "max-block-size: var(--site-popover-max-block);" in opened
    assert "max-height" not in opened
    # A phone keeps the height it had.
    phone = rules.split("@media (max-width: 40rem) {", 1)[1]
    assert "max-block-size: calc(100dvh - 1rem);" in phone.split("@media", 1)[0]
    assert "preview" not in css


def test_the_design_document_describes_the_overview() -> None:
    design = (render_overview.TEMPLATES / "paper-design.md").read_text(encoding="utf-8")
    assert "\n## Result Overview\n" in design
    section = design.split("\n## Result Overview\n", 1)[1].split("\n## ", 1)[0]
    for name in ("site-result.css", "result_overview.py", "atlas_film_facts"):
        assert name in section, name


def test_amended_result_address_notice_is_inside_the_complete_article(
    complete_pages: dict[str, str],
) -> None:
    rows = site_urls.load_registry()
    row = next(row for row in rows if row.path == "result/t-116.html")
    amendment = next(change for change in row.amendments if change.get("historical_target"))
    current = complete_pages[row.path]
    article = current.split('<article class="site-result"', 1)[1].split("</article>", 1)[0]
    notice = article.split('class="site-result-section site-result-compatibility"', 1)[1]
    notice = notice.split("</aside>", 1)[0]
    assert html.escape(amendment["historical_title"]) in notice
    target = html.unescape(HREF.findall(notice)[0])
    assert urljoin(row.path, target) == amendment["historical_target"]
    assert "separate upper bound result" in notice
    assert str(amendment["date"]) in notice
    assert "SQUISH" in article


def test_complete_result_batch_loads_the_address_registry_once(
    overview: overview_data.Overview,
) -> None:
    """Multiple real documents share one validated address registry per render pass."""
    rows = site_urls.load_registry()
    results = [_result(overview, result_id) for result_id in ("T-110", "T-116")]
    with (
        patch.object(overview_data, "load", return_value=replace(overview, results=results)),
        patch.object(site_urls, "load_registry", return_value=rows) as loaded,
    ):
        pages = render_overview.result_fragments()
    assert loaded.call_count == 1
    assert {page.name for page in pages} == {
        overview_sections.result_fragment(result.id) for result in results
    }
    for page in pages:
        assert '<article class="site-result"' in page.html
        assert "</html>" in page.html


def test_address_notice_escapes_titles_and_credit(overview: overview_data.Overview) -> None:
    result = replace(_result(overview, "T-116"), credit='A & "B" <C>')
    notice = result_overview.compatibility_notices(
        result,
        [
            {
                "date": "2026-10-07",
                "historical_target": "result/t-110.html",
                "historical_title": 'Former <claim> & "title"',
            }
        ],
        registered_paths={"result/t-110.html"},
    )
    assert "Former &lt;claim&gt; &amp; &quot;title&quot;" in notice
    assert "A &amp; &quot;B&quot; &lt;C&gt;" in notice
    assert "<claim>" not in notice


@pytest.mark.parametrize(
    "target",
    [
        "../result/t-110.html",
        "https://other.test/t-110.html",
        "javascript:alert(1)",
        "result/t-999.html",
    ],
)
def test_address_notice_requires_a_registered_local_target(
    target: str, overview: overview_data.Overview
) -> None:
    with pytest.raises(ValueError, match="unregistered local historical target"):
        result_overview.compatibility_notices(
            _result(overview, "T-116"),
            [
                {
                    "date": "2026-10-07",
                    "historical_target": target,
                    "historical_title": "Former result",
                }
            ],
            registered_paths={"result/t-110.html"},
        )


def test_recent_upper_lower_and_optimal_marks_follow_independent_contributions() -> None:
    from devtools.result_status import recent_contributions_by_case  # noqa: PLC0415

    flags = recent_contributions_by_case()
    facts = result_overview.film_facts()
    assert (flags[11].upper, flags[11].lower, flags[11].optimal) == (False, True, True)
    assert result_overview.contribution_class(11, "upper") == "is-upper"
    assert result_overview.contribution_class(11, "lower") == "is-lower is-new-result"
    assert result_overview.contribution_class(11, "optimal") == "is-optimal is-new-result"
    badges = result_overview.case_badges(11)
    assert 'data-style="solid" data-recent="true" role="img" aria-label="optimal"' in badges
    assert badges.count('data-recent="true"') == 1
    assert 'class="is-upper is-exact-value"' in result_overview.film_bound(facts[11])
    assert "is-new-result" not in result_overview.film_bound(facts[11])
    assert 'class="is-upper" style=' in result_overview.gap_bar(facts[11])
    assert result_overview.contribution_class(211, "upper") == "is-upper is-new-result"
    assert 'class="is-upper is-new-result"' in result_overview.film_bound(facts[211])
    assert 'data-recent="true"' not in result_overview.case_badges(1)


def test_an_exact_value_uses_its_own_recent_upper_contribution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from devtools import result_status  # noqa: PLC0415

    facts = result_overview.film_facts()
    flags = dict(result_status.recent_contributions_by_case())
    flags[1] = result_status.RecentContributions(upper=True, lower=False, optimal=False)
    monkeypatch.setattr(result_status, "recent_contributions_by_case", lambda: flags)
    bound = result_overview.film_bound(facts[1])
    assert 'class="is-upper is-new-result is-exact-value"' in bound
    assert "is-optimal" not in bound
