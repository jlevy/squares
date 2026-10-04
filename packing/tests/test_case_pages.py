"""The case records: one record per case at an address of its own, `cases/11.html`,
shown by the record page (`cases/`) and opened the same way, in one case popover, from
the overview's atlas grid and from the frontier table's rows (think-t21m)."""

from __future__ import annotations

import html
import re
from pathlib import Path

import pytest

from devtools import overview_sections, render_case_pages, render_overview
from devtools import render_research_tables as tables
from devtools.render_overview import assert_self_contained
from devtools.repo_links import DEFAULT_BRANCH, REPO_URL, hash_pinned_links
from sqpack.probes import probe
from tests import site_renders

PROBES = Path(__file__).resolve().parent / "probes"

#: The record page carries the site's shell, the account and the index, and no record:
#: it fetches each record file. Measured at about 1.9 MB on 2026-10-03.
PAGE_CEILING_BYTES = 2_500_000
#: One record file is the record alone, with no styles or shell. Measured on 2026-10-03:
#: from 16 KB (n = 1) to 217 KB (n = 11, whose prose and results are the longest, and
#: n = 17 close behind), 10.4 MB for all 324.
RECORD_CEILING_BYTES = 300_000


@pytest.fixture(scope="module")
def page() -> str:
    return site_renders.html(render_case_pages.CASES_PAGE)


@pytest.fixture(scope="module")
def records() -> dict[str, str]:
    return site_renders.case_records()


@pytest.fixture(scope="module")
def frontier() -> str:
    return site_renders.html("frontier.html")


@pytest.fixture(scope="module")
def overview() -> str:
    return site_renders.html("index.html")


@pytest.fixture(scope="module")
def numbers() -> list[int]:
    return sorted(int(path.stem.split("-")[1]) for path in tables.FRONTIER.glob("n-*.md"))


def _record(records: dict[str, str], n: int) -> str:
    """Case `n`'s record, the one article its record file carries."""
    text = records[render_case_pages.case_url(n)]
    start = text.index('<article class="site-case"')
    return text[start : text.rindex("</article>") + len("</article>")]


def test_every_case_has_a_record_file_at_its_own_address(
    records: dict[str, str], numbers: list[int]
) -> None:
    assert render_case_pages.case_url(11) == "cases/11.html"
    assert sorted(records) == sorted(f"cases/{n}.html" for n in numbers)
    for n in numbers:
        record = _record(records, n)
        assert record.startswith(f'<article class="site-case" data-case="{n}" '), n
        assert record.count('<article class="site-case"') == 1, n


def test_the_record_page_is_served_and_the_old_page_forwards_to_it() -> None:
    assert render_case_pages.CASES_PAGE == "cases/index.html"
    assert render_case_pages.CASES_PAGE in render_overview.SITE_PAGES
    assert render_case_pages.CASES_PAGE in render_overview.PAGES
    assert "cases.html" not in render_overview.SITE_PAGES
    assert ("cases.html", render_case_pages.CASES_PAGE) in render_overview.MOVED_PAGES
    assert render_overview.canonical_url(render_case_pages.CASES_PAGE).endswith("/cases/")


def test_a_record_file_names_itself_and_sends_a_reader_with_scripts_on(
    records: dict[str, str],
) -> None:
    """A record file has its own title, description, canonical address and link
    preview, so a shared link to a case reads as that case; its one script sends a
    reader on to the record page, and it carries no styles or shell."""
    text = records["cases/29.html"]
    assert '<html lang="en" data-case="29">' in text
    assert "<title>n = 29 · Case Records · The Squares Project</title>" in text
    canonical = render_overview.canonical_url("cases/29.html")
    assert f'<link rel="canonical" href="{canonical}">' in text
    assert f'<meta property="og:url" content="{canonical}">' in text
    assert "Packing 29 unit squares in the smallest square" in text
    forward = render_case_pages.CASE_FORWARD_SCRIPT.read_text(encoding="utf-8")
    assert text.count("<script>") == 1
    assert forward.strip() in text
    # One small style of its own, for a plain reading, and none of the site's.
    assert text.count("<style>") == 1
    assert ".kpress-math-render{display:none}" in text
    assert "kpress-shell" not in text
    assert_self_contained("cases/29.html", text)


def test_every_record_file_is_small(records: dict[str, str]) -> None:
    sizes = {name: len(text.encode()) for name, text in records.items()}
    assert max(sizes.values()) < RECORD_CEILING_BYTES, max(sizes, key=sizes.__getitem__)


def test_a_records_links_are_written_from_its_own_directory(
    records: dict[str, str],
) -> None:
    """Every relative link in a record file resolves from `cases/`, where the record
    page that shows it also stands: a site page climbs out (`../frontier.html`), a
    neighbouring record does not (`12.html`), and every case is `./`. A host page
    elsewhere rebases them against the record file's own address
    (`overview/case-popover.js`)."""
    record = _record(records, 11)
    assert 'href="../frontier.html#n-11"' in record
    assert 'href="../all-results.html#t-018"' in record
    assert 'href="10.html" rel="prev" data-case-step="10"' in record
    assert 'href="12.html" rel="next" data-case-step="12"' in record
    assert 'href="./" data-case-index' in record
    relative = [
        html.unescape(url)
        for url in re.findall(r'\s(?:href|src)="([^"]*)"', record)
        if not re.match(r"#|[a-zA-Z][a-zA-Z0-9+.-]*:|/", url)
    ]
    served = {f"../{name}" for name in render_overview.SITE_PAGES} | {"./", "../"}
    cases = {f"{n}.html" for n in site_renders.overview().cases}
    for url in relative:
        target = url.partition("#")[0].partition("?")[0]
        assert target in served or target in cases, url


@pytest.mark.parametrize(
    ("url", "moved"),
    [
        ("frontier.html#n-11", "../frontier.html#n-11"),
        ("cases/12.html", "12.html"),
        ("cases/12.html#n-3", "12.html#n-3"),
        ("cases/", "./"),
        ("./", "../"),
        ("papers/x.html?y=1#z", "../papers/x.html?y=1#z"),
        ("#fn-1", "#fn-1"),
        ("https://github.com/jlevy/squares", "https://github.com/jlevy/squares"),
        ("mailto:a@b.c", "mailto:a@b.c"),
        ("", ""),
    ],
)
def test_a_link_from_the_root_is_written_again_from_the_records_directory(
    url: str, moved: str
) -> None:
    assert render_case_pages.rebase_link(url, render_case_pages.CASES_DIR) == moved


def test_rebasing_leaves_scripts_and_styles_alone() -> None:
    script = probe(PROBES, "case_pages/attribute_text")
    style = '<style>a[href="b.html"] {}</style>'
    markup = (
        f'<a href="frontier.html">x</a><script>{script}</script>{style}<img src="poster.png">'
    )
    assert render_case_pages.rebase_links(markup, "cases") == (
        f'<a href="../frontier.html">x</a><script>{script}</script>{style}'
        '<img src="../poster.png">'
    )


def test_the_atlas_grid_and_the_frontier_table_open_the_same_record(
    numbers: list[int], frontier: str
) -> None:
    """Both entry points name each case's record file and open it in the one case
    popover: the atlas grid's cells and the frontier table's `n` are links marked
    `data-case`, and a frontier row names its record for the popover to open. A case's
    regularized tile, its second drawing, links the same record as its house tile."""
    grid = overview_sections.atlas_grid()
    house, regularized = grid.split("<template data-atlas-regularized>", 1)
    link = r'href="cases/(\d+)\.html" data-case="(\d+)" data-atlas-n="(\d+)"'
    cells = re.findall(link, house)
    assert [int(n) for n, _, _ in cells] == numbers
    assert all(a == b == c for a, b, c in cells)
    second = re.findall(link, regularized)
    assert [int(n) for n, _, _ in second] == list(overview_sections.atlas_regularized())
    assert all(a == b == c for a, b, c in second)
    assert grid.count(render_case_pages.case_popover()) == 1
    links = re.findall(
        r'<a aria-label="n = \d+: open its case record" href="cases/(\d+)\.html" '
        r'data-case="(\d+)"',
        frontier,
    )
    assert [int(n) for n, _ in links] == numbers
    assert all(a == b for a, b in links)
    rows = re.findall(r'data-case-row="(\d+)" data-case-href="cases/(\d+)\.html"', frontier)
    assert [int(n) for n, _ in rows] == numbers
    assert all(a == b for a, b in rows)
    assert frontier.count(render_case_pages.case_popover()) == 1


def test_the_frontier_rows_minimal_popovers_are_gone(frontier: str) -> None:
    """The popover each frontier row opened until 2026-10-03, its construction, lower
    bound kind and verification notes, went with think-necq: a row opens the case's
    record, which carries all of that."""
    assert "pop-frontier-n-" not in frontier
    assert not re.search(r"<tr\b[^>]*\sdata-row-popover", frontier)
    assert render_overview.ROW_POPOVER_SCRIPT.read_text(encoding="utf-8") not in frontier
    assert "site-pairs" not in frontier


def test_both_entry_pages_carry_the_case_popover_script(overview: str, frontier: str) -> None:
    case_popover = render_case_pages.CASE_POPOVER_SCRIPT.read_text(encoding="utf-8")
    assert case_popover in overview
    assert case_popover in frontier
    assert render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8") in overview
    assert "data-atlas-facts" not in overview
    assert 'id="pop-atlas"' not in overview


def test_the_popover_fetches_the_record_and_opens_its_address() -> None:
    markup = render_case_pages.case_popover()
    assert 'id="pop-case" popover' in markup
    assert "data-case-popover" in markup
    assert "data-case-body" in markup
    assert 'data-case-open href="cases/"' in markup
    assert "<iframe" not in markup


def test_the_record_page_reads_one_record_at_a_time(page: str, numbers: list[int]) -> None:
    """The record page holds no record: its reader fetches the one the address names,
    and its index links every record file."""
    assert render_case_pages.CASE_PAGE_SCRIPT.read_text(encoding="utf-8") in page
    assert "data-case-reader hidden" in page
    assert '<article class="site-case"' not in page
    index = page.split('<nav class="site-case-index', 1)[1].split("</nav>", 1)[0]
    assert "data-case-index" in index
    links = re.findall(r'href="(\d+)\.html" data-case="(\d+)"', index)
    assert [int(n) for n, _ in links] == numbers
    # The page stands in `cases/`: its bar climbs out to the site's root.
    assert 'href="../all-results.html"' in page
    assert 'href="../frontier.html"' in page


def test_the_page_is_self_contained_and_under_its_ceiling(page: str) -> None:
    assert_self_contained(render_case_pages.CASES_PAGE, page)
    assert len(page.encode()) < PAGE_CEILING_BYTES


def test_every_record_opens_with_its_visual_summary(
    records: dict[str, str], numbers: list[int]
) -> None:
    """The visual summary comes first, under the record's head: the drawing, then the
    number line of the bounds, then the bound as one statement; the record's further
    data and the case file's prose follow it."""
    for n in numbers:
        record = _record(records, n)
        order = [
            record.index('<header class="site-case-head"'),
            record.index('<section class="site-case-summary'),
            record.index('<figure class="site-case-figure'),
            record.index('<div class="site-atlas-gap"'),
            record.index('<p class="site-atlas-pop-bound"'),
            record.index('<div class="site-case-data"'),
            record.index('<div class="site-case-prose"'),
        ]
        assert order == sorted(order), n
        assert "<svg " in record, n
        assert f"s({n})" in record, n
        assert "data-kpress-math" in record, n


def test_a_result_about_one_case_shows_the_same_visual_summary() -> None:
    body = site_renders.result_bodies()["T-060"]
    assert '<section class="site-case-summary' in body
    assert body.index('<figure class="site-case-figure') < body.index(
        '<div class="site-atlas-gap"'
    )


def test_no_math_is_left_as_source_text(records: dict[str, str]) -> None:
    for name, text in records.items():
        assert not re.search(r"\{\{[A-Z0-9_]+\}\}", text), name
        article = re.sub(r"<script.*?</script>", "", text, flags=re.DOTALL)
        assert not re.search(r"(?<![\w\\])\$[^$\s][^$<]*\$", article), name
    record = _record(records, 11)
    # The case files' formulas, which they write in code spans, are set as math.
    assert "<code>s(11)</code>" not in record
    assert "<code>31/8</code>" not in record


def test_case_11_carries_its_polynomial_results_verification_and_links(
    records: dict[str, str],
) -> None:
    record = _record(records, 11)
    assert "Minimal polynomial, degree 8" in record
    assert "s^8 - 20s^7" in record
    for result in ("T-018", "T-026", "T-033"):
        assert f'<a href="../all-results.html#{result.lower()}">{result}</a>' in record
    assert '<a href="../frontier.html#n-11">' in record
    branch = f"{REPO_URL}/blob/{DEFAULT_BRANCH}/"
    assert f'class="site-case-github" href="{branch}packing/frontier/n-011.md"' in record
    # What the frontier row's popover said until 2026-10-03 is the record's now.
    assert '<span class="site-card-label">Verification</span>' in record


def test_a_case_records_results_list_significance_first(records: dict[str, str]) -> None:
    """Each result in a case record shows its rungs after its id as the tables do: S,
    then V, then C (`overview_sections.rung_chips`)."""
    results = {result.id: result for result in site_renders.overview().results}
    heads = re.findall(
        r'<li class="site-case-result" data-result="(T-\d{3})">'
        r'<p class="site-case-result-head"><a [^>]*>T-\d{3}</a> (.*?) '
        r'<span class="site-credit">',
        _record(records, 11),
    )
    assert {"T-018", "T-026", "T-033"} <= {result_id for result_id, _ in heads}
    for result_id, chips in heads:
        assert chips == overview_sections.rung_chips(results[result_id]), result_id
        assert [label[0] for label in re.findall(r">([SVC]\d)</span>", chips)] == list("SVC")


def test_every_repository_link_names_main(page: str, records: dict[str, str]) -> None:
    from devtools.check_published_site import repository_links  # noqa: PLC0415

    for text in (page, *records.values()):
        assert not hash_pinned_links(text)
    links = [link for text in records.values() for link in repository_links(text)]
    assert links
    assert {ref for _, ref, _ in links} == {DEFAULT_BRANCH}


def test_a_link_to_another_case_file_opens_its_record(records: dict[str, str]) -> None:
    """`n-013.md` links `n-012.md`; in a record that is case 12's record file."""
    record = _record(records, 13)
    assert 'href="12.html"' in record
    assert 'href="32.html"' in record


@pytest.mark.parametrize(
    ("code", "tex"),
    [
        ("s(11) > 31/8 = 3.875", "s (11) > 31 / 8 = 3.875"),
        ("2 + 4/sqrt(5) = 3.788854\u2026", r"2 + 4 / \sqrt{5} = 3.788854 \ldots"),
        ("18*sqrt(5)/101", r"18 \sqrt{5} / 101"),
        ("\u2308\u221a112\u2309 = 11", r"\lceil\sqrt{112}\rceil = 11"),
        ("cos \u03b8\u2081", r"\cos \theta _{1}"),
        ("n \u2264 100", r"n \le 100"),
        ("10\u207b\u2079", "10 ^{-9}"),
        ("4.85e-30", r"4.85 \times 10^{-30}"),
        ("2 + \u00bd\u221a2", r"2 + \tfrac{1}{2} \sqrt{2}"),
        ("x, y \u2208 {1, 2}", r"x , y \in \{1 , 2\}"),
        ("k", "k"),
    ],
)
def test_a_code_span_that_is_mathematics_becomes_tex(code: str, tex: str) -> None:
    assert render_case_pages.code_tex(code) == tex


@pytest.mark.parametrize(
    "code",
    [
        "T-026",
        "V4/C5",
        "n-012.md",
        "reported_lower_bound",
        "minSide 32 = 6",
        "uv run --frozen --group dev packing-validate",
        "280af3d4\u2026e6e5",
        "campaign/series/x.json",
        "D4",
        "",
    ],
)
def test_a_code_span_that_names_something_stays_code(code: str) -> None:
    assert render_case_pages.code_tex(code) is None


def test_the_prose_sets_formulas_and_keeps_names() -> None:
    body = (
        "# Title\n\nA bound `s(11) > 31/8` from [`T-018`](RESULTS.md), in `exact_form`.\n\n"
        "## Section\n\n```\ns(61) > 7\u221a3/2 + 2\u221a2 \u2212 1\n```\n\n"
        "```bash\nuv run x\n```\n"
        "<!-- footer -->\n"
    )
    shown = render_case_pages.prose_markdown(body)
    assert "$s (11) > 31 / 8$" in shown
    assert "[`T-018`](RESULTS.md)" in shown
    assert "`exact_form`" in shown
    assert "### Title" in shown
    assert "#### Section" in shown
    assert "$$\ns (61) > 7 \\sqrt{3} / 2 + 2 \\sqrt{2} - 1\n$$" in shown
    assert "```bash\nuv run x\n```" in shown
    assert "footer" not in shown


def test_a_cases_badges_are_one_mark_wherever_a_case_is_drawn(
    records: dict[str, str], frontier: str
) -> None:
    """The film's badges, optimal, exact, numerical and rigid, are the site's one mark
    for a case's properties (the owner, 2026-10-03, think-7cbx): the visual summary lists
    them with their words, and where a case is one line, a record's head and a frontier
    row, they stand after its status chip as glyphs alone, each named, from one builder
    (`result_overview.case_badges`)."""
    from devtools import result_overview  # noqa: PLC0415

    facts = result_overview.film_facts()
    assert [label for _, _, label in facts[11]["badges"]] == ["optimal", "exact", "rigid"]
    badges = result_overview.case_badges(11)
    for glyph, style, label in facts[11]["badges"]:
        named = result_overview.badge_glyph(glyph, style, label, named=True)
        assert f'role="img" aria-label="{label}" title="{label}">' in named
        assert named in badges
        # The summary's list draws the same square, its word beside it.
        listed = result_overview.badge_glyph(glyph, style, label)
        assert f"{listed}{label}</li>" in _record(records, 11)
    head = _record(records, 11).split("</header>", 1)[0]
    assert badges in head
    row = frontier.split('<tr id="n-11" ', 1)[1].split("</tr>", 1)[0]
    assert badges in row
    # A case with no property the film marks has no row of them.
    plain = [n for n, fact in facts.items() if not fact["badges"]]
    if plain:
        assert result_overview.case_badges(plain[0]) == ""


def test_a_records_heading_ids_are_its_own(records: dict[str, str]) -> None:
    """Each record's headings take ids counted within the record alone (`_own_ids`), so
    a heading added to one case file never renumbers another record's: the same heading
    has the same id in every record, and none carries a count of the records above."""
    seen: dict[str, set[str]] = {}
    for name, text in records.items():
        ids = re.findall(r'<h[1-6][^>]*\sid="([^"]*)"', text)
        assert len(ids) == len(set(ids)), name
        for heading, found in re.findall(r'<h[1-6][^>]*\sid="([^"]*)"[^>]*>(.*?)</h', text):
            seen.setdefault(re.sub(r"<[^>]+>", "", found).strip(), set()).add(heading)
    assert seen["The packing"] == {"the-packing"}
    assert all(len(ids) == 1 for title, ids in seen.items() if title.startswith("The ")), {
        title: ids for title, ids in seen.items() if len(ids) > 1
    }


def test_a_link_to_a_record_file_is_marked_for_the_case_popover() -> None:
    marked = render_case_pages.mark_case_links(
        '<p><a href="cases/11.html">x</a> <a href="cases/13.html#a">z</a> '
        '<a aria-label="y" href="cases/12.html" data-case="12">y</a> '
        '<a href="frontier.html">f</a></p>'
    )
    assert marked == (
        '<p><a href="cases/11.html" data-case="11">x</a> '
        '<a href="cases/13.html#a" data-case="13">z</a> '
        '<a aria-label="y" href="cases/12.html" data-case="12">y</a> '
        '<a href="frontier.html">f</a></p>'
    )


def test_the_record_page_lists_no_heading_it_does_not_show(page: str) -> None:
    """kpress lists every heading of a page in its page model; the record page's would
    be every record's, about 80 KB of headings it does not show, so its list is empty."""
    model = page.split('<script type="application/json" id="kpress-page-model">', 1)[1]
    assert '"headings": []' in model.split("</script>", 1)[0]


def test_a_record_files_description_has_room(records: dict[str, str]) -> None:
    """Each record file's description is its own and keeps clear of the limit
    `head_tags` refuses past, so a rewording does not fail the render."""
    descriptions = re.findall(
        r'<meta name="description" content="([^"]*)"', "".join(records.values())
    )
    assert len(descriptions) == len(records) == len(set(descriptions))
    assert max(len(text) for text in descriptions) <= render_overview.DESCRIPTION_LIMIT - 15


def test_a_footnote_in_a_case_file_is_refused() -> None:
    """kpress gathers footnotes at the foot of the one render, outside every record, so
    the render refuses one rather than lose it from its record file; the mark it looks
    for is the one kpress writes."""
    from kpress.format.model import DocumentInput, RenderOptions  # noqa: PLC0415
    from kpress.format.render import render_page  # noqa: PLC0415

    markdown = "# T\n\nA note.[^x]\n\n[^x]: The note.\n"
    document = DocumentInput(
        title="t", source_text=markdown, source_path="t.md", body_markdown=markdown
    )
    page = render_page(document, RenderOptions(asset_mode="inline", asset_policy="none")).html
    assert render_case_pages.FOOTNOTE_MARK in page
    with pytest.raises(SystemExit, match="footnote"):
        render_case_pages.refuse_footnotes(page)
    render_case_pages.refuse_footnotes("<p>No note.</p>")


def test_each_record_steps_to_its_neighbours_with_the_sites_arrows(
    records: dict[str, str], numbers: list[int]
) -> None:
    """A record's steps are the site's drawn arrows, left before the previous case and
    right after the next, never the arrow characters the site's face lacks; between
    them, every case."""
    left, right = overview_sections.arrow_icon("left"), overview_sections.arrow_icon("right")
    for n in (numbers[0], 11, numbers[-1]):
        record = _record(records, n)
        steps = record[record.index('<nav class="site-case-steps"') :]
        steps = steps[: steps.index("</nav>")]
        assert "←" not in steps
        assert "→" not in steps
        assert (f'data-case-step="{n - 1}">{left}n = {n - 1}</a>' in steps) == (n != numbers[0])
        assert (f"n = {n + 1}{right}</a>" in steps) == (n != numbers[-1])
        assert '<a href="./" data-case-index>All cases</a>' in steps
