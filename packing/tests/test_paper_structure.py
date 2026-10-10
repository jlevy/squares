"""The site's papers share one structure, and cannot drift apart without this failing.

The owner asked on 2026-10-01 that the papers' "formats, formatting, and all structure
should be similar". `devtools.paper_structure` reads each rendered paper on every
structural axis and `devtools.paper_front` writes every paper's front from one record;
these tests render every paper of the site (`render_overview.PAPERS`, the three parts of
the n = 11 series) and hold every form axis of each equal to the first paper's, and hold
the credits of each to the owner's dictated form (think-2cqu) with the series strip
under them (the series plan, 2026-10-05).

A review's renderer is modelled on the optimality review's
(`render_n11_optimality_review`): each is rendered here through the same entry points,
`render`, `ARTICLE`, `render_all_figures` and `render_all_facts`.
"""

from __future__ import annotations

import importlib
from dataclasses import replace
from pathlib import Path
from types import ModuleType

import pytest

from devtools import (
    paper_front,
    paper_structure,
    render_n11_lower_bounds_explainer,
    render_overview,
)
from devtools import render_n11_optimality_review as paper
from devtools.render_overview import (
    N11_THRESHOLD_BOUND_REVIEW,
    PACKING_METHODS,
    PAPERS,
    paper_path,
    paper_record,
)
from sqpack import release

EXPLAINER = render_n11_lower_bounds_explainer.SLUG
THRESHOLD = N11_THRESHOLD_BOUND_REVIEW
REVIEW = paper.SLUG
METHODS = PACKING_METHODS
SERIES = tuple(record for record in PAPERS if record.part is not None)
#: Every review, in reading order: the papers after the first.
REVIEWS = tuple(record.slug for record in PAPERS[1:])
#: Each review's source, as the first two lines of its credits name it.
SOURCES = {
    THRESHOLD: ("Kleddamag", "https://github.com/Kleddamag/11-squares-certified-bound"),
    REVIEW: ("Mannaseh Ahmed", "https://github.com/Queuingtheorydotcom/11SquaresOptimal"),
}
#: Each paper's own version line and dates line, from `sqpack.release`.
VERSIONS = {
    EXPLAINER: release.EXPLAINER_VERSION,
    THRESHOLD: release.THRESHOLD_REVIEW_EDITION,
    REVIEW: release.OPTIMALITY_REVIEW_EDITION,
    METHODS: release.PACKING_METHODS_EDITION,
}
DATES = {
    EXPLAINER: (
        f"First published {release.EXPLAINER_FIRST_PUBLISHED} · "
        f"Last revised {release.EXPLAINER_REVISED}"
    ),
    THRESHOLD: (
        f"First published {release.THRESHOLD_REVIEW_HISTORY[-1].first_published} · "
        f"Original proof {release.THRESHOLD_PROOF_PUBLISHED} · "
        f"Last revised {release.THRESHOLD_REVIEW_REVISED}"
    ),
    REVIEW: (
        f"First published {release.OPTIMALITY_REVIEW_HISTORY[-1].first_published} · "
        f"Original proof {release.OPTIMALITY_PROOF_PUBLISHED} · "
        f"Last revised {release.OPTIMALITY_REVIEW_REVISED}"
    ),
    METHODS: (
        f"First published {release.PACKING_METHODS_FIRST_PUBLISHED} · "
        f"Last revised {release.PACKING_METHODS_REVISED}"
    ),
}


def renderer(slug: str) -> ModuleType:
    """The renderer the site's registry names for the paper `slug`."""
    return importlib.import_module(paper_record(slug).module)


def rendered(slug: str) -> tuple[str, str]:
    """A paper's page and Markdown edition as this checkout renders them."""
    if slug == EXPLAINER:
        found = render_n11_lower_bounds_explainer.render(
            render_n11_lower_bounds_explainer.WALKTHROUGH
        )
        return found.page, found.markdown
    module = renderer(slug)
    return module.render(
        module.ARTICLE.read_text(encoding="utf-8"),
        figures=module.render_all_figures(),
        facts=module.render_all_facts(),
        revision="a" * 40,
    )


@pytest.fixture(scope="module")
def renders() -> dict[str, tuple[str, str]]:
    """Every paper as this checkout renders it, by slug, in reading order."""
    return {record.slug: rendered(record.slug) for record in PAPERS}


@pytest.fixture(scope="module")
def structures(renders: dict[str, tuple[str, str]]) -> dict[str, paper_structure.Structure]:
    """Every paper, read as a reader meets it."""
    return {
        slug: paper_structure.read(slug, html, markdown)
        for slug, (html, markdown) in renders.items()
    }


@pytest.fixture(scope="module")
def rows(structures: dict[str, paper_structure.Structure]) -> list[dict[str, object]]:
    return paper_structure.compare(*structures.values())


def test_the_audit_reads_every_paper_of_the_site_in_reading_order() -> None:
    assert paper_structure.PAPERS == (EXPLAINER, THRESHOLD, REVIEW, METHODS)
    assert paper_structure.CREDIT_KINDS[-1] == "series"


def test_every_form_axis_is_the_same_on_every_paper(rows: list[dict[str, object]]) -> None:
    """The head, the formats row, the title, the credits' weights and links, the version
    and dates lines' form, the series strip, the heading case, the captions, the
    footnotes, the colophon and the Markdown edition's opening: one way on every paper."""
    assert paper_structure.differences(rows) == []
    forms = {str(row["axis"]) for row in rows if row["compared"] == "form"}
    assert {
        "head: title",
        "head: og:type",
        "head: modified is the revised date",
        "formats row",
        "formats row: titles",
        "title: h1",
        "credits: names bold",
        "credits: addresses plain",
        "credits: dates finish with current date",
        "series: strip",
        "sections: h2 case",
        "sections: h3 case",
        "figures: captions",
        "closing: colophon",
        "markdown: opening",
    } <= forms


def test_the_shared_form_is_the_one_the_design_names(rows: list[dict[str, object]]) -> None:
    found = {str(row["axis"]): str(row[EXPLAINER]) for row in rows}
    assert found["head: title"] == "article name"
    assert found["head: og:type"] == "article"
    assert found["formats row"] == (
        "MD → <slug>.md · PDF → <slug>.pdf · GITHUB → https://github.com/jlevy/squares"
    )
    assert found["title: h1"] == "1, Title Case"
    assert found["credits: names bold"] == "yes"
    assert found["credits: addresses plain"] == "yes"
    assert found["credits: dates finish with current date"] == "yes"
    assert found["series: strip"] == (
        "Part N of M, then each other part by number and title, linked"
    )
    assert [
        found_row[slug]
        for found_row in rows
        if found_row["axis"] == "series: part"
        for slug in (EXPLAINER, THRESHOLD, REVIEW)
    ] == [
        "Part I of 3",
        "Part II of 3",
        "Part III of 3",
    ]
    assert found["sections: h2 case"] == "Title Case"
    assert found["sections: h3 case"] == "sentence case"
    assert found["figures: captions"] == "Figure N. lead, numbered from 1"
    assert found["footnotes"] == "a footnotes section"
    assert found["closing: colophon"].startswith(
        "The Squares Project · github.com/jlevy/squares /"
    )


def test_each_papers_credits_follow_the_owners_form(
    structures: dict[str, paper_structure.Structure],
) -> None:
    """Each review credits its source first, by name in bold and address as a plain link,
    then its own credits after a line's space; the explainer, which explains the
    project's own proofs, begins at its own. Every paper: oversight, agents, the version
    plain, the dates, ending with when the paper was last revised, then the series
    strip, which part of three it is and the other two parts by title, each linking its
    paper's page."""
    series_length = len(SERIES)
    for slug, structure in structures.items():
        strip = series_length if paper_record(slug).part is not None else 0
        kinds = [line.kind for line in structure.credits]
        own = list(paper_structure.CREDIT_KINDS[2:-1]) + ["series"] * strip
        assert kinds == (
            list(paper_structure.CREDIT_KINDS[:2]) + own if slug in SOURCES else own
        )
    for slug, (author, address) in SOURCES.items():
        source, shown = structures[slug].credits[:2]
        assert source.text == f"From the original proof by {author}"
        assert source.bold == (author,)
        assert shown.bold == ()
        assert shown.links == ((address.removeprefix("https://"), address),)
    for slug, structure in structures.items():
        lines = structure.credits
        strip = series_length if paper_record(slug).part is not None else 0
        oversight, agents, version, dates = lines[-4 - strip : -strip or None]
        assert oversight.text == "Human oversight: Joshua Levy"
        assert oversight.bold == ("Joshua Levy",)
        assert oversight.links == (("Joshua Levy", "https://x.com/ojoshe"),)
        assert agents.text.startswith("Agents: ")
        assert agents.bold == tuple(
            agents.text.removeprefix("Agents: ")
            .replace(", and ", ", ")
            .replace(" and ", ", ")
            .split(", ")
        )
        assert version.bold == ()
        assert dates.bold == ()
        assert dates.links == ()
        # Each paper's version line is its own version (the owner, 2026-10-01), never the
        # site's edition or the data hash.
        assert release.PUBLICATION_EDITION not in version.text
        assert release.DATA_REVISION[: release.DATA_REVISION_LENGTH] not in version.text
        assert dates.text == DATES[slug], slug
        assert version.text.startswith(VERSIONS[slug]), slug
        # The series strip: which part, then each other part by its title, linked.
        part = paper_record(slug).part
        if part is None:
            assert all(line.kind != "series" for line in lines)
            continue
        head, *others = lines[-strip:]
        assert head.text == f"Part {paper_front.numeral(part)} of {strip} in the n = 11 series"
        assert head.links == head.bold == ()
        assert [line.text for line in others] == [
            f"Part {paper_front.numeral(record.part)}: {record.title}"
            for record in SERIES
            if record.slug != slug and record.part is not None
        ]
        assert [line.links for line in others] == [
            ((record.title, f"{record.slug}.html"),) for record in SERIES if record.slug != slug
        ]
    strip = series_length
    explainer, review = structures[EXPLAINER].credits, structures[REVIEW].credits
    assert explainer[-1 - strip].text.startswith("First published")
    assert explainer[-2 - strip].text == f"{release.EXPLAINER_VERSION} (version history)"
    assert explainer[-2 - strip].links == (("version history", "#version-history"),)
    assert review[-2 - strip].text == f"{release.OPTIMALITY_REVIEW_EDITION} (version history)"
    assert review[-2 - strip].links == (("version history", "#version-history"),)
    methods = structures[METHODS].credits
    assert methods[-2].text == "v0.2.0 (version history)"
    assert methods[-2].links == (("version history", "#version-history"),)


def test_the_markdown_editions_open_as_the_pages_do(
    structures: dict[str, paper_structure.Structure],
) -> None:
    """Each edition opens with the title as a heading and the credits as a list, the
    lines the page shows, in the page's order, with no chip row."""
    for name, structure in structures.items():
        head = structure.markdown_head
        assert head[0].startswith("# "), name
        items = [line.removeprefix("- ") for line in head[1:]]
        assert len(items) == len(structure.credits), name
        for item, line in zip(items, structure.credits, strict=True):
            for bold in line.bold:
                assert f"**{bold}**" in item, (name, item)
            for text, href in line.links:
                # A link to another paper is page-relative on the page and the site's
                # address in the Markdown edition, which is read away from the site.
                address = (
                    render_overview.SITE_URL + paper_path(href.removesuffix(".html"))
                    if line.kind == "series"
                    else href
                )
                assert f"]({address})" in item, (name, item)
                assert text in item, (name, item)
        assert "chip" not in " ".join(head)


def test_the_tool_prints_the_audit_of_a_built_site(
    renders: dict[str, tuple[str, str]],
    structures: dict[str, paper_structure.Structure],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`python -m devtools.paper_structure SITE --markdown` prints the table and exits
    0 when every form axis agrees, names the axes that differ when one does, and
    refuses a site that lacks a paper."""
    for slug, (page, document) in renders.items():
        (tmp_path / paper_path(slug)).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / paper_path(slug)).write_text(page, encoding="utf-8")
        (tmp_path / paper_path(slug, ".md")).write_text(document, encoding="utf-8")
    assert paper_structure.main([str(tmp_path), "--markdown"]) == 0
    out = capsys.readouterr().out
    assert "| axis |" in out
    assert (
        "| head: title | form | article name | article name | "
        "article name | article name | True |" in out
    )
    assert structures[REVIEW].pdf == {}

    # A paper whose credits set a name plain is a form difference, and the tool says so.
    html = renders[REVIEW][0]
    broken = html.replace("<strong>Mannaseh Ahmed</strong>", "Mannaseh Ahmed")
    (tmp_path / paper_path(REVIEW)).write_text(broken, encoding="utf-8")
    assert paper_structure.main([str(tmp_path)]) == 1
    assert "credits: names bold" in capsys.readouterr().err
    # A paper whose series strip drops a part is one too.
    title = paper_record(EXPLAINER).title
    unlisted = html.replace(f'<a href="{EXPLAINER}.html">{title}</a>', title)
    (tmp_path / paper_path(REVIEW)).write_text(unlisted, encoding="utf-8")
    assert paper_structure.main([str(tmp_path)]) == 1
    assert "series: strip" in capsys.readouterr().err
    (tmp_path / paper_path(REVIEW)).unlink()
    with pytest.raises(SystemExit, match=r"has no papers/n11-optimality-review\.html"):
        paper_structure.main([str(tmp_path)])


@pytest.mark.parametrize(
    ("title", "name"),
    [
        (f"A paper{render_overview.TITLE_SEPARATOR}{render_overview.PROJECT_NAME}", "A paper"),
        ("A different paper", "A paper"),
        ("", "A paper"),
        ("A paper", ""),
        ("", ""),
    ],
    ids=["project-suffix", "wrong-title", "missing-title", "missing-name", "both-missing"],
)
def test_article_title_form_refuses_suffixes_mismatches_and_missing_names(
    title: str, name: str
) -> None:
    good = paper_structure.read(
        "good",
        '<head><title>A paper</title><meta property="og:title" content="A paper"></head>',
    )
    assert paper_structure.axes(good)["head: title"] == "article name"
    bad = replace(good, paper="bad", title=title, name=name)
    assert paper_structure.axes(bad)["head: title"] != "article name"
    assert [
        row["axis"] for row in paper_structure.differences(paper_structure.compare(good, bad))
    ] == ["head: title"]


def test_the_pdf_is_read_for_its_title_size_and_dates() -> None:
    pdf = (
        b"%PDF-1.4\n1 0 obj\n<</Title (A paper \\(draft\\))\n/Creator (Chromium)\n"
        b"/CreationDate (D:20261001120000+00'00')\n/ModDate (D:20261001120000+00'00')>>\n"
        b"endobj\n2 0 obj\n<</Type /Pages /Kids [3 0 R 4 0 R]>>\nendobj\n"
        b"3 0 obj\n<</Type /Page /MediaBox [0 0 612 792]>>\nendobj\n"
        b"4 0 obj\n<</Type /Page /MediaBox [0 0 612 792]>>\nendobj\n"
    )
    html = (
        "<html><head><title>A paper (draft)</title>"
        '<meta property="og:title" content="A paper (draft)"></head><body>'
        '<div class="credits centred"><span class="publication-date">'
        "Last revised October 1, 2026</span></div></body></html>"
    )
    found = paper_structure.axes(paper_structure.read("x", html, "", pdf))
    assert found["pdf: page size"] == "612 x 792 pt"
    assert found["pdf: pages"] == "2"
    assert found["pdf: title"] == "the page's title"
    assert found["pdf: dates"] == "the revised date, at noon UTC"
    assert paper_structure.axes(paper_structure.read("x", html))["pdf: pages"] == "no PDF"


@pytest.mark.parametrize(
    ("headings", "case"),
    [
        (("The Result and Proof Roadmap", "From a Continuum of Angles to 181"), "Title Case"),
        (("T-025: a direct certificate at 3.82", "Keeping everything else"), "sentence case"),
        (("The Result", "Keeping everything else"), "mixed"),
        (
            (
                "A Review of the Certified Lower Bound s(11) > 31/8 for 11 Squares",
                "From Points to k-of-m Charges",
            ),
            "Title Case",
        ),
        (("Why k-of-m charges pay", "The bound s(11) > 31/8"), "sentence case"),
        ((), "none"),
    ],
)
def test_heading_case_is_read_as_a_reader_reads_it(
    headings: tuple[str, ...], case: str
) -> None:
    assert paper_structure.heading_case(headings) == case


def test_caption_form_names_what_departs_from_the_lead() -> None:
    assert paper_structure.caption_form(("Figure 1. A", "Figure 2. B")) == (
        "Figure N. lead, numbered from 1"
    )
    assert paper_structure.caption_form(("Figure 1. A", "Figure 3. B")) == "numbered [1, 3]"
    assert paper_structure.caption_form(("Figure 1. A", "B")) == (
        "a caption without a `Figure N.` lead"
    )
    assert paper_structure.caption_form(()) == "no figures"


@pytest.mark.parametrize(
    ("dates", "expected"),
    [
        (
            (("First published", "October 8, 2026"), ("Last revised", "October 8, 2026")),
            "Published October 8, 2026",
        ),
        (
            (("First published", "October 8, 2026"), ("Last revised", "October 08, 2026")),
            "Published October 8, 2026",
        ),
        (
            (("First published", "October 7, 2026"), ("Last revised", "October 8, 2026")),
            "First published October 7, 2026 · Last revised October 8, 2026",
        ),
        (
            (
                ("First published", "October 8, 2026"),
                ("Original proof", "October 8, 2026"),
                ("Last revised", "October 8, 2026"),
            ),
            "Original proof October 8, 2026 · Published October 8, 2026",
        ),
        (
            (("Original proof", "October 8, 2026"), ("Last revised", "October 8, 2026")),
            "Original proof October 8, 2026 · Last revised October 8, 2026",
        ),
        (
            (("Last revised", "October 8, 2026"),),
            "Last revised October 8, 2026",
        ),
    ],
)
def test_publication_dates_share_one_display_rule_without_changing_the_record(
    dates: tuple[tuple[str, str], ...], expected: str
) -> None:
    front = paper.FRONT._replace(dates=tuple(paper_front.Dated(*dated) for dated in dates))
    html = paper_front.credits_html(front)
    markdown = paper_front.credits_markdown(front)
    assert f'<span class="publication-date">{expected}</span>' in html
    assert f"- {expected}\n" in markdown + "\n"
    assert tuple(front.dates) == dates
    assert paper_front.revised(front) == dates[-1][1]


def test_collapsed_date_audit_refuses_conflicting_metadata() -> None:
    front = paper.FRONT._replace(
        dates=(
            paper_front.Dated("First published", "October 8, 2026"),
            paper_front.Dated(paper_front.REVISED, "October 8, 2026"),
        )
    )
    html = paper_front.credits_html(front)
    structure = replace(
        paper_structure.read(front.slug, html),
        published="2026-10-08",
        modified="2026-10-08",
    )
    axis = "credits: dates finish with current date"
    assert paper_structure.axes(structure)[axis] == "yes"
    assert paper_structure.axes(replace(structure, published="2026-10-07"))[axis] == "no"
    assert paper_structure.axes(replace(structure, modified="2026-10-09"))[axis] == "no"
    for malformed in (
        "First published October 8, 2026 · Last revised October 8, 2026",
        "Last revised October 8, 2026 · Published October 8, 2026",
        "Published October 8, 2026 · Published October 8, 2026",
    ):
        date_credits = tuple(
            line._replace(text=malformed) if line.kind == "dates" else line
            for line in structure.credits
        )
        assert paper_structure.axes(replace(structure, credits=date_credits))[axis] == "no"


def test_the_front_record_is_refused_where_it_departs_from_the_form() -> None:
    """`paper_front.check` refuses a record the owner's form has no line for."""
    front = paper.FRONT
    good = paper_front.check(front)
    assert good is front
    series = front.series
    assert series is not None
    for broken, refusal in (
        (front._replace(version="**Draft v0.1.0**"), "plain text"),
        (front._replace(dates=front.dates[:1]), "ends with 'Last revised'"),
        (
            front._replace(dates=(paper_front.Dated(paper_front.REVISED, "2026-10-01"),)),
            "not `October 1, 2026`",
        ),
        (front._replace(oversight=()), "names someone"),
        (front._replace(agents=()), "the agents are named"),
        (front._replace(source=paper_front.Source("Q", "http://example.com")), "https"),
        (front._replace(history="Version History"), "by its id"),
        (front._replace(slug="papers/x"), "slug"),
        (front._replace(series=series._replace(part=1)), "names this paper as its part"),
        (
            front._replace(series=series._replace(parts=series.parts[::-1])),
            "numbered 1, 2",
        ),
        (
            front._replace(
                series=series._replace(
                    parts=tuple(part._replace(title=" ") for part in series.parts)
                )
            ),
            "named by its title",
        ),
    ):
        with pytest.raises(ValueError, match=refusal):
            paper_front.check(broken)
    assert paper_front.revised(front) == release.OPTIMALITY_REVIEW_REVISED
    assert "{{FRONT_MATTER}}" not in paper_front.front_matter(front)
    with pytest.raises(ValueError, match="exactly once"):
        paper_front.fill("no slot here", front)
    with pytest.raises(ValueError, match="does not carry the paper's front once"):
        paper_front.published("no front here", front)


def test_each_paper_takes_its_series_strip_from_the_one_registry() -> None:
    """The strip is written from the site's list of papers, so every paper names the
    others the same way: its parts are the registry's, in reading order, and its part is
    the paper's own. A paper the site does not list has no strip to take."""
    for record in SERIES:
        series = paper_front.series(record.slug)
        assert series.name == paper_front.SERIES_NAME == "the n = 11 series"
        assert series.part == record.part
        assert [(part.number, part.slug, part.title) for part in series.parts] == [
            (other.part, other.slug, other.title) for other in SERIES
        ]
    for module in (render_n11_lower_bounds_explainer, paper):
        assert module.FRONT.series == paper_front.series(module.SLUG)
    with pytest.raises(ValueError, match="no paper of the site"):
        paper_front.series("n11-no-such-paper")
    assert [paper_front.numeral(n) for n in (1, 2, 3)] == ["I", "II", "III"]
    with pytest.raises(ValueError, match="no numeral"):
        paper_front.numeral(0)


def test_every_registered_renderer_writes_its_front_with_the_strip() -> None:
    """Each renderer the registry names titles its paper as the registry does and
    writes its front with the strip, Part II's among them."""
    for record in PAPERS:
        module = renderer(record.slug)
        assert record.title == module.TITLE, record.slug
        if record.part is None:
            assert module.FRONT.series is None, record.slug
            with pytest.raises(ValueError, match="standalone paper"):
                paper_front.series(record.slug)
        else:
            assert module.FRONT.series == paper_front.series(record.slug), record.slug


def test_standalone_absence_does_not_relax_the_series_or_caption_grammar(
    structures: dict[str, paper_structure.Structure],
) -> None:
    reference = structures[EXPLAINER]
    standalone = structures[METHODS]
    assert paper_structure.axes(standalone)["series: strip"] == "none"
    assert (
        paper_structure.axes(standalone)["figures: captions"]
        == "Figure N. lead, numbered from 1"
    )
    assert paper_structure.differences(paper_structure.compare(reference, standalone)) == []
    missing = replace(
        reference, credits=tuple(line for line in reference.credits if line.kind != "series")
    )
    assert "series: strip" in {
        row["axis"]
        for row in paper_structure.differences(paper_structure.compare(reference, missing))
    }
    broken = replace(standalone, captions=("Figure 2. A skipped first caption",))
    assert "figures: captions" in {
        row["axis"]
        for row in paper_structure.differences(paper_structure.compare(reference, broken))
    }
    # No headings or strips in either input is a valid empty optional comparison.
    empty = replace(standalone, h2=(), h3=())
    optional = {"sections: h2 case", "sections: h3 case", "series: strip", "figures: captions"}
    assert all(
        row["same"] for row in paper_structure.compare(empty, empty) if row["axis"] in optional
    )
