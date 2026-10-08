"""The case records: one record per case at an address of its own, `cases/11.html`,
shown by the record page (`cases/`) and opened the same way, in one case popover, from
the overview's atlas grid and from the frontier table's rows (think-t21m)."""

from __future__ import annotations

import html
import re
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import overview_sections, render_case_pages, render_overview, site_assets
from devtools import render_frontier_page as frontier_page
from devtools import render_research_tables as tables
from devtools.render_overview import assert_fetches_only_assets
from devtools.repo_links import DEFAULT_BRANCH, REPO_URL, hash_pinned_links
from sqpack.probes import probe
from tests import site_renders

PROBES = Path(__file__).resolve().parent / "probes"

#: The record page carries the account and the index, and no record: it fetches each
#: record file. Measured at about 1.9 MB on 2026-10-03, when it carried the site's shell
#: inline, its faces and math, as every page did; at 40,771 bytes on 2026-10-04, once it
#: linked the shell from the site's shared assets (`site_assets`) instead.
PAGE_CEILING_BYTES = 100_000
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
def served() -> dict[str, str]:
    """The three pages above as a reader's browser assembles them, with every shared
    asset they link put back in them (`tests.site_renders.served`), by name."""
    names = (render_case_pages.CASES_PAGE, "frontier.html", "index.html")
    return {name: site_renders.served(name) for name in names}


@pytest.fixture(scope="module")
def numbers() -> list[int]:
    return sorted(int(path.stem.split("-")[1]) for path in tables.FRONTIER.glob("n-*.md"))


def _program_tag(path: Path, name: str) -> str:
    """The element by which the page `name` loads `path`, a page program: a file of the
    site's shared assets named by its content (`site_assets`)."""
    return site_assets.script_tag(site_assets.shared().assets.script_file(path), name)


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


def test_a_record_file_is_a_complete_styled_canonical_page(records: dict[str, str]) -> None:
    """Scripts and no-script readers get the same complete record at its own address."""
    text = records["cases/29.html"]
    assert "<title>29 Unit Squares in a Square: Bounds and Best Packing" in text
    canonical = render_overview.canonical_url("cases/29.html")
    assert f'<link rel="canonical" href="{canonical}">' in text
    assert f'<meta property="og:url" content="{canonical}">' in text
    assert "Packing 29 unit squares:" in text
    assert text.count("<h1 ") == 1
    assert "<main " in text
    assert 'class="kpress-site-header"' in text
    assert 'rel="stylesheet"' in text
    assert "BreadcrumbList" in text
    assert "case-forward" not in text
    assert 'data-kpress-math-rendered="true"' in text
    assert_fetches_only_assets("cases/29.html", text)
    assert f"{site_assets.ASSETS_DIR}/" in text


def test_every_record_file_is_small(records: dict[str, str]) -> None:
    sizes = {name: len(text.encode()) for name, text in records.items()}
    # These cases preserve their full algebraic proofs and verified result history.
    exceptions = {"cases/11.html": 500_000, "cases/17.html": 500_000, "cases/18.html": 350_000}
    for name, size in sizes.items():
        assert size < exceptions.get(name, RECORD_CEILING_BYTES), (name, size)


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
    `data-case`, and a frontier row names its record for the popover to open. A case
    drawn from its regularized view, the atlas's one tile for it since the House and
    Regularized tabs went (think-k8x9), links the same record, whose drawing is the
    house one."""
    grid = overview_sections.atlas_grid()
    assert "<template data-atlas-regularized>" not in grid
    link = r'href="cases/(\d+)\.html" data-case="(\d+)" data-atlas-n="(\d+)"'
    cells = re.findall(link, grid)
    assert [int(n) for n, _, _ in cells] == numbers
    assert all(a == b == c for a, b, c in cells)
    for n in overview_sections.atlas_regularized():
        tile = re.findall(rf'<a class="site-atlas-cell" href="cases/{n}\.html"[^>]*>', grid)
        assert len(tile) == 1, n
        assert ", regularized view, " in tile[0], n
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


def test_the_frontier_rows_minimal_popovers_are_gone(
    frontier: str, served: dict[str, str]
) -> None:
    """The popover each frontier row opened until 2026-10-03, its construction, lower
    bound kind and verification notes, went with think-necq: a row opens the case's
    record, which carries all of that. Neither its script nor its styles come with the
    page as it is served."""
    assert "pop-frontier-n-" not in frontier
    assert not re.search(r"<tr\b[^>]*\sdata-row-popover", frontier)
    whole = served["frontier.html"]
    assert render_overview.ROW_POPOVER_SCRIPT.read_text(encoding="utf-8") not in whole
    assert "site-pairs" not in whole


def test_both_entry_pages_carry_the_case_popover_script(
    overview: str, frontier: str, served: dict[str, str]
) -> None:
    """Each links the case popover's program, the overview the atlas grid's too, and
    each as it is served carries their text."""
    case_popover = render_case_pages.CASE_POPOVER_SCRIPT
    for name, page in (("index.html", overview), ("frontier.html", frontier)):
        assert page.count(_program_tag(case_popover, name)) == 1, name
        assert case_popover.read_text(encoding="utf-8") in served[name], name
    assert overview.count(_program_tag(render_overview.ATLAS_GRID_SCRIPT, "index.html")) == 1
    grid = render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8")
    assert grid in served["index.html"]
    assert "data-atlas-facts" not in served["index.html"]
    assert 'id="pop-atlas"' not in overview


def test_the_popover_fetches_the_record_and_opens_its_address() -> None:
    markup = render_case_pages.case_popover()
    assert 'id="pop-case" popover' in markup
    assert "data-case-popover" in markup
    assert "data-case-body" in markup
    assert 'data-case-open href="cases/"' in markup
    assert "<iframe" not in markup


def test_the_case_index_links_complete_records_without_fetching(
    page: str, numbers: list[int], served: dict[str, str]
) -> None:
    """The record page holds no record: its reader fetches the one the address names,
    and its index links every record file. The reader is a shared program, which the
    page names from `cases/` (`../assets/js/`)."""
    reader = render_case_pages.CASE_PAGE_SCRIPT
    tag = _program_tag(reader, render_case_pages.CASES_PAGE)
    assert tag.startswith('<script src="../assets/js/case-page.')
    assert page.count(tag) == 1
    assert reader.read_text(encoding="utf-8") in served[render_case_pages.CASES_PAGE]
    assert "data-case-reader" not in page
    assert "fetch(" not in reader.read_text(encoding="utf-8")
    assert '<article class="site-case"' not in page
    index = page.split('<nav class="site-case-index', 1)[1].split("</nav>", 1)[0]
    assert "data-case-index" in index
    links = re.findall(r'href="(\d+)\.html" data-case="(\d+)"', index)
    assert [int(n) for n, _ in links] == numbers
    # The page stands in `cases/`: its bar climbs out to the site's root.
    assert 'href="../all-results.html"' in page
    assert 'href="../frontier.html"' in page


def test_the_page_fetches_only_the_shared_assets_and_is_under_its_ceiling(page: str) -> None:
    """The page fetches nothing but the site's shared assets, each a file the build
    writes, and names every one from `cases/`, where it stands: `../assets/`, never an
    `assets/` beside it that the site does not have."""
    assert_fetches_only_assets(render_case_pages.CASES_PAGE, page)
    assert site_assets.shared().assets.referenced([page])
    assert '="../assets/' in page
    assert not re.search(r'(?:href|src)="assets/', page)
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
        assert f"s({n})" in html.unescape(re.sub(r"<[^>]+>", "", record)), n
        assert "data-kpress-math" in record, n


def test_a_result_about_one_case_shows_the_same_visual_summary() -> None:
    body = site_renders.result_bodies()["T-060"]
    assert '<section class="site-case-summary' in body
    assert body.index('<figure class="site-case-figure') < body.index(
        '<div class="site-atlas-gap"'
    )


def _declarations(css: str, selector: str) -> str:
    """The declarations of every rule in `css` whose selector is exactly `selector`."""
    rules = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    found = re.findall(rf"(?:^|}}|{{)\s*{re.escape(selector)} {{([^}}]*)}}", rules)
    assert found, selector
    return "".join(found)


@pytest.mark.parametrize("units", [1000, overview_sections.ATLAS_UNITS])
def test_the_drawing_fills_the_case_popover_at_its_own_line_weight(units: int) -> None:
    """In the case popover the visual summary's drawing is as wide as the panel, short
    of the panel's height less the room its caption and actions take (`think-u214`), and
    its lines keep the weight they have at 12rem however large it is shown
    (`think-pkz0`): the stylesheet draws them in the page's units (`non-scaling-stroke`)
    at the share of the drawing's width the drawing gives them up to 12rem across. The
    shares are read here from the drawing itself, at the record's units and a result
    overview's, so the stylesheet and the drawing cannot part."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert "inline-size: min(100%, var(--site-popover-max-block) - 8rem);" in _declarations(
        css, ".site-case-pop .site-case-figure"
    )
    figure = _declarations(css, ".site-case-figure")
    assert "container-type: inline-size;" in figure
    assert "--site-case-figure-lines: min(100cqi, 12rem);" in figure
    assert "vector-effect: non-scaling-stroke;" in _declarations(
        css, ".site-case-figure > svg :is(rect, path)"
    )
    # The figure's rules name its drawing alone: a caption's typeset radical is an `svg`.
    assert not re.search(r"\.site-case-figure svg\b", css)
    svg = frontier_page.packing_svg(11, units=units)
    box = re.search(r'viewBox="\S+ \S+ (\S+) \S+"', svg)
    frame = re.search(r'<rect [^>]*stroke-width="([\d.]+)"', svg)
    lines = re.search(r'<g [^>]*stroke-width="([\d.]+)"', svg)
    assert box is not None
    assert frame is not None
    assert lines is not None
    width = Fraction(box.group(1))
    for selector, drawn in (
        (".site-case-figure > svg > rect", frame),
        (".site-case-figure > svg path", lines),
    ):
        share = re.search(
            r"stroke-width: calc\(var\(--site-case-figure-lines\) \* ([\d.]+) / ([\d.]+)\);",
            _declarations(css, selector),
        )
        assert share, selector
        assert (
            Fraction(share.group(1)) / Fraction(share.group(2))
            == Fraction(drawn.group(1)) / width
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
    assert "<msup><mi>s</mi><mn>8</mn></msup>" in record
    assert "<msup><mi>s</mi><mn>7</mn></msup>" in record
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
    assert "kpress-page-model" not in page
    assert "kpress-diagnostics" not in page


def test_a_record_files_description_has_room(records: dict[str, str]) -> None:
    """Each record file's description is its own and keeps clear of the limit
    `head_tags` refuses past, so a rewording does not fail the render."""
    descriptions = re.findall(
        r'<meta name="description" content="([^"]*)"', "".join(records.values())
    )
    assert len(descriptions) == len(records) == len(set(descriptions))
    assert (
        max(len(html.unescape(text)) for text in descriptions)
        <= render_overview.DESCRIPTION_LIMIT
    )


def test_a_record_files_description_counts_its_squares(records: dict[str, str]) -> None:
    """One square is a unit square, and every other count is squares."""
    said = {
        n: re.findall(r'<meta name="description" content="([^"]*)"', records[f"cases/{n}.html"])
        for n in (1, 2, 11)
    }
    assert said[1][0].startswith("Packing 1 unit square:")
    assert said[2][0].startswith("Packing 2 unit squares:")
    assert said[11][0].startswith("Packing 11 unit squares:")


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
