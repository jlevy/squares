"""Part II, the review of T-037, renders complete and offline, cites pinned sources, links
its sibling papers per edition, and agrees with the register on every result number."""

from __future__ import annotations

import json
import re
from fractions import Fraction
from pathlib import Path
from urllib.parse import urljoin

import pytest
from markdown_it import MarkdownIt

from devtools import (
    check_published_site,
    n11_threshold_figures,
    paper_front,
    paper_links,
    paper_structure,
    render_overview,
)
from devtools import render_n11_threshold_bound_review as paper
from devtools.render_n11_lower_bounds_explainer import assert_self_contained
from sqpack import release
from sqpack.fractional.parent_core import load_kleddamag_parent_core
from sqpack.yamlio import load_yaml

ARTICLE = paper.ARTICLE
REVISION = "a" * 40
SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-test" viewBox="0 0 2 2">'
    '<title>Exact diagram</title><rect width="2" height="2"/></svg>'
)
FIGURES: dict[str, str] = dict.fromkeys(paper.FIGURE_KEYS, SVG)
#: Mathematics written as text, which a caption never is: the relations, Greek letters,
#: superscript two and the minus sign the sans face does not carry.
UNICODE_MATH = "[\u2264\u2265\u00b2\u2212\u03b3\u0393]"
#: The reviewed certificate's bytes, which the loader refuses to read otherwise.
CERTIFICATE_SHA256 = "57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458"
CERTIFICATE = paper.ARCHIVE / "global-certificate.json"
REGISTER = paper.PACKING / "frontier" / "results.yaml"
#: The archived source as the article links it, relative to the templates directory.
ARCHIVE_LINK = "../../resources/web/external-square-certificates-2026-09-22/kleddamag-11"
SOURCE = """{{FRONT_MATTER}}

An exact formula is $x^2$.[^proof] See the
[review](../../../docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md),
the [record][register] and
[Part I]({{PAPER:n11-lower-bounds-explainer#the-result-and-proof-roadmap}}).

<figure>
{{CHARGE_SVG}}
<figcaption><strong>Figure 1.</strong> See the
<a href="PROOF_LINK">the budget argument</a>.</figcaption>
</figure>

[^proof]: The claim has a retained proof.

[register]: ../../frontier/results.yaml
"""

SOURCE = SOURCE.replace("PROOF_LINK", f"{ARCHIVE_LINK}/PROOF.md#L31-L39")
SOURCE += "\n" + "\n".join(
    "{{" + key + "}}" for key in paper.FIGURE_KEYS if "{{" + key + "}}" not in SOURCE
)


def _decimal(value: Fraction, places: int) -> str:
    """`value` written with exactly `places` decimals, which every retained value here
    has: the weights have denominator 10^9."""
    scaled = value * 10**places
    assert scaled.denominator == 1, value
    whole, part = divmod(scaled.numerator, 10**places)
    return f"{whole}.{part:0{places}d}"


def certificate_facts() -> dict[str, str]:
    """The `CERT_*` facts as the figures module must supply them, computed here from the
    retained certificate through the project's loader, so the article's numbers are
    cross-checked against the data and not only against each other."""
    certificate = load_kleddamag_parent_core(CERTIFICATE, expected_sha256=CERTIFICATE_SHA256)
    gamma = certificate.minimum_charge
    budget = certificate.budget
    raw = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    features = sum(len(orbit["sets"]) for orbit in raw["charge_orbits"] if orbit["weight"])
    charge_orbits = sum(1 for orbit in raw["charge_orbits"] if orbit["weight"])
    sites = {(atom.x, atom.y) for atom in certificate.atoms}
    sites |= {point for atom in certificate.threshold_atoms for point in atom.points}
    return {
        "CERT_GAMMA": _decimal(gamma, 9),
        "CERT_M": _decimal(budget, 9),
        "CERT_ELEVEN_GAMMA": _decimal(11 * gamma, 9),
        "CERT_SURPLUS_UNITS": f"{(11 * gamma - budget) * 10**9:,}",
        "CERT_ROWS": f"{len(certificate.rows):,}",
        "CERT_SITES": f"{len(sites):,}",
        "CERT_POINT_SITES": f"{len(certificate.atoms):,}",
        "CERT_ORBITS": f"{len(raw['point_orbits']):,}",
        "CERT_CHARGE_ORBITS": f"{charge_orbits:,}",
        "CERT_FEATURES": f"{features:,}",
        "CERT_A": str(certificate.parent_side),
        "CERT_L0": str(certificate.outer_side),
        "CERT_BOUND": str(certificate.outer_side / certificate.parent_side),
    }


def fake_facts() -> dict[str, str]:
    """Every fact the article names: the certificate's own computed here, the figures'
    stood in for by a marker, since the figure module is not a dependency of this test."""
    facts = {key: f"FACT-{key}" for key in paper.CAPTION_FACT_KEYS}
    facts.update(certificate_facts())
    return facts


@pytest.fixture(scope="module")
def rendered() -> tuple[str, str]:
    return paper.render(SOURCE, figures=FIGURES, revision=REVISION, article=ARTICLE)


@pytest.fixture(scope="module")
def actual() -> tuple[str, str]:
    """The real article, rendered with placeholder figures and the certificate's facts."""
    return paper.render(
        ARTICLE.read_text(encoding="utf-8"),
        figures=FIGURES,
        facts=fake_facts(),
        revision=REVISION,
    )


def test_rendered_page_is_offline_and_contains_proof_figures(rendered: tuple[str, str]) -> None:
    html, markdown = rendered
    assert_self_contained(html)
    assert html.count("<title>Exact diagram</title>") == len(paper.FIGURE_KEYS)
    assert '<span class="kpress-math kpress-math-inline"' in html
    assert 'class="kpress-footnotes"' in html
    assert "{{" not in markdown
    for name in ("MD", "PDF", "GITHUB"):
        assert f">{name}</a>" in html
    assert '<div class="doc-links screen-only">' in html
    assert 'href="https://github.com/jlevy/squares"' in html


def test_the_papers_head_is_the_sites_set_at_the_papers_own_address(
    rendered: tuple[str, str],
) -> None:
    html, _ = rendered
    url = render_overview.canonical_url(paper.SITE_PATH)
    assert (
        paper.SLUG == render_overview.N11_THRESHOLD_BOUND_REVIEW == "n11-threshold-bound-review"
    )
    assert paper.SITE_PATH == "papers/n11-threshold-bound-review.html"
    assert check_published_site.head_problems(html, url, allow_inline_favicon=True) == []
    head = check_published_site.read_head(html)
    assert head.titles == (paper.TITLE,)
    assert head.meta("og:title") == [paper.TITLE]
    assert head.meta("og:type") == ["article"]
    assert head.meta("description") == [paper.DESCRIPTION]
    assert "<" not in paper.TITLE
    meta = paper.page_meta()
    assert meta.modified == paper_front.iso_date(release.THRESHOLD_REVIEW_REVISED)
    assert head.meta("article:modified_time") == [meta.modified]
    assert meta.published == paper_front.iso_date(
        release.THRESHOLD_REVIEW_HISTORY[-1].first_published
    )
    assert paper_front.revised(paper.FRONT) == release.THRESHOLD_REVIEW_REVISED


def test_the_front_is_the_shared_components_in_the_owners_form(
    rendered: tuple[str, str],
) -> None:
    """The article carries one slot for its front; the page and the Markdown edition take
    it from `paper_front`: the original proof first, by Marc Leonard Overbeck's name in
    bold and the repository's address as a plain link; this review's own credits a line's
    space below; the draft's version linking the version history; then the dates from
    `sqpack.release`'s `THRESHOLD_*` names. The hero sets the title's formula as the
    page's own math span, as Part I does, and the head keeps the title plain."""
    article = ARTICLE.read_text(encoding="utf-8")
    assert article.count("{{FRONT_MATTER}}") == 1
    assert '<div class="credits' not in article
    assert "doc-links" not in article
    assert "doc-links" not in paper.SHELL.read_text(encoding="utf-8")
    assert ".credits" not in paper.STYLE.read_text(encoding="utf-8")
    html, markdown = rendered
    root = paper_structure.parse(html)
    assert len(root.find_all(cls="credits")) == 1
    structure = paper_structure.read(paper.SLUG, html, markdown)
    assert [line.kind for line in structure.credits[:6]] == [
        "source",
        "address",
        "oversight",
        "agents",
        "version",
        "dates",
    ]
    source, address, oversight, agents, version, dates, *series = structure.credits
    author_profile = render_overview.canonical_url("profiles/marc-leonard-overbeck.html")
    assert {href for _label, href in source.links} == {author_profile}
    assert source.bold
    assert {href for _label, href in address.links} == {
        "https://github.com/Kleddamag/11-squares-certified-bound"
    }
    assert not address.bold
    assert {href for _label, href in oversight.links} == {
        person.url for person in paper.FRONT.oversight
    }
    assert oversight.bold
    assert set(agents.bold) == set(paper.FRONT.agents)
    assert release.THRESHOLD_REVIEW_EDITION in version.text
    assert {href for _label, href in version.links} == {"#version-history"}
    assert not version.bold
    for dated in paper.FRONT.dates:
        assert f"{dated.label} {dated.day}" in dates.text
    assert len(series) == 3
    assert "Part II of 3" in series[0].text
    assert [href for line in series[1:] for _label, href in line.links] == [
        "n11-lower-bounds-explainer.html",
        "n11-optimality-review.html",
    ]
    elements = list(root.walk())
    formats = root.find(cls="doc-links")
    hero = root.find(cls="hero")
    assert formats is not None
    assert hero is not None
    assert elements.index(formats) < elements.index(hero)
    markdown_front = paper_structure.parse(
        MarkdownIt().render("\n".join(structure.markdown_head))
    )
    assert markdown_front.find("h1") is not None
    items = markdown_front.find_all("li")
    assert len(items) == len(structure.credits)
    page_url = render_overview.canonical_url(paper.SITE_PATH)
    for item, credit in zip(items, structure.credits, strict=True):
        assert [urljoin(page_url, link.attrs["href"]) for link in item.find_all("a")] == [
            urljoin(page_url, href) for _label, href in credit.links
        ]
        assert bool(item.find_all("strong")) == bool(credit.bold)
    assert release.THRESHOLD_REVIEW_EDITION in items[4].text()
    for dated in paper.FRONT.dates:
        assert f"{dated.label} {dated.day}" in items[5].text()
    heading = root.find("h1")
    assert heading is not None
    assert heading.find(cls="kpress-math") is not None
    assert not heading.find_all(cls="tex")
    assert "doc-links" not in markdown
    assert paper.PACKING / "src" / "sqpack" / "release.py" in paper.RENDER_INPUTS


def test_the_page_carries_the_sites_bar_and_the_shared_layers(
    rendered: tuple[str, str],
) -> None:
    html, _ = rendered
    root = paper_structure.parse(html)
    navs = root.find_all("nav", "site-nav")
    assert len(navs) == 1
    assert navs[0].attrs.get("aria-label")
    current = [
        link for link in navs[0].find_all("button") if link.attrs.get("aria-current") == "true"
    ]
    assert [(link.attrs.get("data-page"), link.attrs.get("href")) for link in current] == [
        ("learn", None)
    ]
    assert current[0].text() == "Learn"
    trail = root.find("nav", "site-breadcrumbs")
    assert trail is not None
    assert [(link.text(), link.attrs.get("href")) for link in trail.find_all("a")] == [
        ("Papers", "../papers.html")
    ]
    assert trail.find_all("span")[0].text() == "Learn"
    assert trail.find_all("span")[0].attrs.get("href") is None
    assert [
        (node.tag, node.text())
        for node in trail.walk()
        if node.attrs.get("aria-current") == "page"
    ] == [("span", paper.TITLE)]
    assert html.count(render_overview.NAVIGATION_SCRIPT.read_text(encoding="utf-8")) == 1
    layer = paper.render_n11_lower_bounds_explainer.publication_layer()
    head = html.split("</head>", 1)[0]
    for name, value in layer.items():
        assert head.count(value) == 1, name
    footer = f'<p class="col colophon centred">{render_overview.colophon_lines(edition="")}</p>'
    assert html.count(footer) == 1
    assert release.PUBLICATION_EDITION not in html
    for needed in (
        render_overview.PAPER_TYPE_CSS,
        render_overview.SITE_NAV,
        render_overview.SITE_NAV_CSS,
        render_overview.NAVIGATION_SCRIPT,
        paper.PACKING / "devtools/site_navigation.py",
        render_overview.THEME_SCRIPT,
        render_overview.EMBED_SCRIPT,
        render_overview.MATH_SCRIPT,
        paper.PACKING / "devtools" / "paper_front.py",
        paper.PACKING / "devtools" / "paper_links.py",
        paper.TERMS,
    ):
        assert needed.is_file(), needed
        assert needed in paper.RENDER_INPUTS, needed.name


@pytest.mark.parametrize(
    "dropped",
    ["<script>{{NATIVE_MATH_METRICS}}</script>\n", "<script>{{SITE_MATH}}</script>\n"],
)
def test_a_shell_that_drops_half_of_a_shared_layer_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, dropped: str
) -> None:
    shell = paper.SHELL.read_text(encoding="utf-8")
    assert shell.count(dropped) == 1
    broken = tmp_path / paper.SHELL.name
    broken.write_text(shell.replace(dropped, ""), encoding="utf-8")
    monkeypatch.setattr(paper, "SHELL", broken)
    with pytest.raises(ValueError, match="values with no placeholder"):
        paper.render(SOURCE, figures=FIGURES, revision=REVISION, article=ARTICLE)


def test_a_caption_fact_the_article_does_not_use_is_refused() -> None:
    with pytest.raises(ValueError, match="caption facts unused"):
        paper.render(
            SOURCE, figures=FIGURES, revision=REVISION, article=ARTICLE, facts={"A": "1"}
        )
    used = SOURCE.replace("budget argument</a>.", "budget argument</a>, {{CERT_ROWS}} rows.")
    html, markdown = paper.render(
        used, figures=FIGURES, revision=REVISION, article=ARTICLE, facts={"CERT_ROWS": "32"}
    )
    assert "budget argument</a>, 32 rows." in html
    assert "32 rows." in markdown
    with pytest.raises(ValueError, match="unresolved placeholders"):
        paper.render(used, figures=FIGURES, revision=REVISION, article=ARTICLE)


def test_a_fact_named_as_a_figure_is_refused() -> None:
    with pytest.raises(ValueError, match="named as figures"):
        paper.expanded_markdown(
            SOURCE,
            figures=FIGURES,
            article=ARTICLE,
            revision=REVISION,
            facts={"CHARGE_SVG": "x"},
        )


@pytest.mark.parametrize(
    ("source", "figures"),
    [
        (SOURCE.replace("{{MINIMA_SVG}}", ""), FIGURES),
        (SOURCE + "\n{{MINIMA_SVG}}\n", FIGURES),
        (SOURCE, {**FIGURES, "EXTRA_SVG": SVG}),
        (SOURCE, {**FIGURES, "MINIMA_SVG": "<svg><script>bad</script></svg>"}),
    ],
)
def test_incomplete_or_active_figure_input_refuses(
    source: str, figures: dict[str, str]
) -> None:
    with pytest.raises(ValueError, match=r"figure|article|SVG"):
        paper.expanded_markdown(source, figures=figures, article=ARTICLE, revision=REVISION)


def test_the_figure_contract_is_the_plans() -> None:
    """The twelve slots are plan figures II.1 to II.12 in reading order, and every fact
    is named for its figure or for the certificate, so the figures lane can read the
    article's side of the contract from one tuple."""
    assert paper.FIGURE_KEYS == (
        "CHANGES_SVG",
        "LADDER_SVG",
        "ROADMAP_SVG",
        "CHARGE_SVG",
        "BUDGET_SVG",
        "FAMILIES_SVG",
        "CORE_SVG",
        "CATALOGUE_SVG",
        "ENVELOPE_SVG",
        "SIGNED_SVG",
        "FIELD_SVG",
        "MINIMA_SVG",
    )
    assert len(set(paper.CAPTION_FACT_KEYS)) == len(paper.CAPTION_FACT_KEYS)
    prefixes = {key.removesuffix("_SVG") for key in paper.FIGURE_KEYS} | {"CERT"}
    for key in paper.CAPTION_FACT_KEYS:
        assert re.fullmatch(r"[A-Z0-9]+(?:_[A-Z0-9]+)+", key), key
        assert key.split("_", 1)[0] in prefixes, key
    for key in (
        "CERT_GAMMA",
        "CERT_M",
        "CERT_ELEVEN_GAMMA",
        "CERT_SURPLUS_UNITS",
        "CERT_ROWS",
        "CERT_SITES",
        "CERT_POINT_SITES",
        "CERT_ORBITS",
        "CERT_CHARGE_ORBITS",
        "CERT_FEATURES",
        "CERT_A",
        "CERT_L0",
        "CERT_BOUND",
    ):
        assert key in paper.CAPTION_FACT_KEYS, key


def test_link_revision_is_the_commit_the_paper_is_built_from(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    assert re.fullmatch(r"[0-9a-f]{40}", paper.link_revision())
    monkeypatch.setattr(paper, "REPO", tmp_path)
    with pytest.raises(SystemExit, match="give --revision"):
        paper.link_revision()


def test_local_citation_is_pinned(rendered: tuple[str, str]) -> None:
    html, markdown = rendered
    blob = "https://github.com/jlevy/squares/blob/" + REVISION
    review = blob + "/docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md"
    assert review in html
    assert review in markdown
    register_url = blob + "/packing/frontier/results.yaml"
    assert f"[register]: {register_url}" in markdown
    assert f'href="{register_url}"' in html
    proof = (
        blob
        + "/packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11/"
        + "PROOF.md#L31-L39"
    )
    assert f'<a href="{proof}"' in html
    assert ">the budget argument</a>" in html


def test_relative_link_must_resolve_to_a_repo_file() -> None:
    unsafe = SOURCE.replace(
        "../../../docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md",
        "../../../../etc/passwd",
    )
    with pytest.raises(ValueError, match="escapes repository"):
        paper.expanded_markdown(unsafe, figures=FIGURES, article=ARTICLE, revision=REVISION)
    missing = SOURCE.replace("../../frontier/results.yaml", "../../frontier/not-a-file.yaml")
    with pytest.raises(ValueError, match="does not exist"):
        paper.expanded_markdown(missing, figures=FIGURES, article=ARTICLE, revision=REVISION)


def test_the_archived_sources_resolve_and_are_declared() -> None:
    """Every archived Overbeck file the article links exists in the retained copy, is
    declared as a citation source, and so is one of the page's inputs."""
    article = ARTICLE.read_text(encoding="utf-8")
    archive = "../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/"
    linked = {
        (ARTICLE.parent / archive / rest.split("#")[0]).resolve()
        for rest in re.findall(re.escape(archive) + r"([^\s)\"#]+)", article)
    }
    assert linked, "the article cites no archived file"
    for target in linked:
        assert target.is_file(), target
        assert target in paper.ARCHIVED_CITATION_SOURCES, target.name
    for source in paper.ARCHIVED_CITATION_SOURCES:
        assert source.is_file(), source
        assert source in paper.RENDER_INPUTS, source.name
    for declared in paper.RENDER_INPUTS:
        assert declared.exists() or declared == paper.FIGURES_MODULE, declared


def test_cross_paper_links_are_filled_per_edition(rendered: tuple[str, str]) -> None:
    """A link to a sibling paper is page-relative on the page and absolute in the
    Markdown edition, and is never pinned to a repository blob."""
    html, markdown = rendered
    anchor = "the-result-and-proof-roadmap"
    page_target = f"n11-lower-bounds-explainer.html#{anchor}"
    assert f'href="{page_target}"' in html
    site_target = (
        render_overview.SITE_URL
        + render_overview.paper_path(render_overview.N11_LOWER_BOUNDS_EXPLAINER)
        + f"#{anchor}"
    )
    assert f"[Part I]({site_target})" in markdown
    assert f"]({page_target}" not in markdown
    assert "{{PAPER:" not in html + markdown
    assert "/blob/" + REVISION + "/n11-lower-bounds-explainer" not in html + markdown
    with pytest.raises(ValueError, match="names no paper"):
        paper.expanded_markdown(
            SOURCE.replace("n11-lower-bounds-explainer", "n11-nothing"),
            figures=FIGURES,
            article=ARTICLE,
            revision=REVISION,
        )


def test_the_actual_article_links_only_known_papers_at_stable_anchors() -> None:
    """The article links Papers I and III by their slugs, each with an anchor, and never
    links a data-dependent heading of Part I, which is no link target."""
    targets = paper_links.paper_link_targets(ARTICLE.read_text(encoding="utf-8"))
    assert targets
    assert {slug for slug, _ in targets} == {
        render_overview.N11_LOWER_BOUNDS_EXPLAINER,
        render_overview.N11_OPTIMALITY_REVIEW,
    }
    for slug, anchor in targets:
        assert slug in paper_links.PAPER_SLUGS
        if anchor is not None:
            assert re.fullmatch(r"[a-z0-9][a-z0-9-]*", anchor), (slug, anchor)
            assert "{{" not in anchor, anchor
            assert "continuum" not in anchor, anchor


def test_no_screen_only_prose(actual: tuple[str, str]) -> None:
    """A paper has no apparatus, so no sentence of it tells its reader to hover, tap or
    drag; the renderer refuses one, and the article has none."""
    _, markdown = actual
    body = markdown.split("\n\n", 2)[2]
    assert paper.ONLY_ON_SCREEN.search(body) is None
    with pytest.raises(ValueError, match="addresses a reader"):
        paper.expanded_markdown(
            SOURCE + "\nNow drag the square.\n",
            figures=FIGURES,
            article=ARTICLE,
            revision=REVISION,
        )


def test_the_actual_article_renders_every_slot_once_with_pinned_sources(
    actual: tuple[str, str],
) -> None:
    html, markdown = actual
    heading = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    assert heading is not None
    assert "kpress-math" in heading.group(1)
    assert "\\gt" not in heading.group(1)
    assert len(re.findall(r"<figure\b", html)) == len(paper.FIGURE_KEYS) == 12
    captions = re.findall(r"<figcaption[^>]*>(.*?)</figcaption>", html, re.DOTALL)
    assert len(captions) == 12
    assert all("$" not in caption for caption in captions)
    leads = [re.match(r"<strong>Figure (\d+)\.</strong>", caption) for caption in captions]
    assert [int(lead.group(1)) for lead in leads if lead] == list(range(1, 13))
    written = re.findall(r"<figcaption>(.*?)</figcaption>", markdown, re.DOTALL)
    assert sum(caption.count("$") for caption in written) >= 20
    assert not re.search(UNICODE_MATH, "".join(written))
    assert html.count("<title>Exact diagram</title>") == 12
    assert "{{" not in markdown
    assert "FACT-CERT" not in markdown
    assert "../../resources/" not in markdown
    assert (
        f"/blob/{REVISION}/packing/resources/web/external-square-certificates-2026-09-22/"
        in markdown
    )
    assert markdown.count(f"/blob/{REVISION}/") >= 60
    assert "katex-error" not in html.split("<article", 1)[1].split("</article>", 1)[0]
    assert "<pre><code><svg" not in html
    # Every heading the registry and the forward links name is on the page.
    ids = set(re.findall(r'<h2[^>]*\bid="([^"]+)"', html))
    registry = load_yaml(paper.TERMS.read_text(encoding="utf-8"))
    assert registry["paper"] == paper.SLUG
    for entry in registry["terms"]:
        assert entry["anchor"] in ids, entry["term"]
    for anchor in re.findall(r"\]\(#([a-z0-9-]+)\)", ARTICLE.read_text(encoding="utf-8")):
        assert anchor in ids, anchor
    assert "version-history" in ids


def test_every_bold_run_of_the_prose_is_a_registered_definition() -> None:
    """The define-before-use gate (`devtools.paper_terms`) holds every bold run of the
    body to be some term's definition on the rendered page; here the registry is held
    to the article's source: each bold run is part of a registered definition, each
    prerequisite is registered, each forward allowance has one of the three reasons,
    and the series tags name the concepts the plan gives this paper."""
    article = ARTICLE.read_text(encoding="utf-8")
    body = article.split("## Appendix A", 1)[0]
    body = re.sub(r"<figcaption>.*?</figcaption>", "", body, flags=re.DOTALL)
    registry = load_yaml(paper.TERMS.read_text(encoding="utf-8"))
    assert registry["paper"] == paper.SLUG
    definitions = [" ".join(entry["defined_by"].split()) for entry in registry["terms"]]
    for run in re.findall(r"\*\*([^*]+)\*\*", body):
        words = " ".join(run.split())
        if words.endswith((".", ":")):
            continue  # a run-in head, such as a lemma's name
        assert any(words in definition for definition in definitions), run
    names = {entry["term"] for entry in registry["terms"]}
    assert len(names) == len(registry["terms"])
    for entry in registry["terms"]:
        for required in entry.get("requires", []):
            assert required in names, (entry["term"], required)
        for forward in entry.get("forward", []):
            assert forward["reason"] in {"roadmap", "heading", "link-to-definition"}
    tagged = {
        entry["term"]: entry["series"] for entry in registry["terms"] if "series" in entry
    }
    assert tagged["charge"] == "charge"
    assert tagged["budget"] == "k-of-m-budget"
    assert tagged["Strict-core lemma"] == "strict-core"
    assert tagged["k-of-m charge"] == "threshold-atom"
    assert {"A", "\u03c1", "C"} <= names


def test_register_consistency_with_t037(published: tuple[str, str]) -> None:
    """The bound, Γ, M, 11Γ, the surplus and the row count in the article agree with the
    certificate, read through the project's loader, and with T-037's claim in the
    register; none is retyped from memory."""
    facts = certificate_facts()
    assert facts["CERT_BOUND"] == "31/8"
    assert facts["CERT_GAMMA"] == "0.999962528"
    assert facts["CERT_M"] == "10.999479944"
    assert facts["CERT_ELEVEN_GAMMA"] == "10.999587808"
    assert facts["CERT_SURPLUS_UNITS"] == "107,864"
    assert facts["CERT_ROWS"] == "12,028"
    assert (facts["CERT_A"], facts["CERT_L0"]) == ("764/775", "191/50")
    assert (facts["CERT_SITES"], facts["CERT_POINT_SITES"]) == ("5,284", "496")
    assert (facts["CERT_ORBITS"], facts["CERT_CHARGE_ORBITS"]) == ("679", "284")
    assert facts["CERT_FEATURES"] == "2,220"
    register = load_yaml(REGISTER.read_text(encoding="utf-8"))
    record = next(entry for entry in register["results"] if entry["id"] == "T-037")
    claim = record["claim"]
    for stated in (
        "s(11) > 31/8",
        "999962528",
        "10999479944",
        "107864",
        "12,028",
        "764/775",
        "191/50",
        "0.0020836",
    ):
        assert stated in claim, stated
    assert (record["verification"], record["confirmation"]) == ("V3", "C3")
    assert record["significance"]["score"] == 5
    assert "T-061" in record["next_rung"]
    assert "T-060" in record["next_rung"]
    html, markdown = published
    for number in (
        "31/8",
        facts["CERT_GAMMA"],
        facts["CERT_M"],
        facts["CERT_ELEVEN_GAMMA"],
        facts["CERT_SURPLUS_UNITS"],
        facts["CERT_ROWS"],
        "764/775",
        "191/50",
        "0.0020836",
        "S5/V3/C3",
    ):
        assert number in markdown, number
    article = ARTICLE.read_text(encoding="utf-8")
    # The literal values the prose carries are the certificate's, where it repeats them.
    for literal in ("12,028", "31/8", "764/775", "191/50"):
        assert literal in article, literal
    assert "katex-error" not in html.split("<article", 1)[1].split("</article>", 1)[0]


def test_the_table_wrap_is_capped_at_the_column(published: tuple[str, str]) -> None:
    css = paper.STYLE.read_text(encoding="utf-8")
    cap = "max-width: min(100%, calc(var(--kpress-measure) + 2 * var(--kpress-column-inset)));"
    assert f".cert-page.n11-paper > .kpress-table-wrap {{\n  {cap}\n}}" in css
    assert "--n11-threshold-diagram-ground: oklch(100% 0 0);" in css
    assert "prefers-color-scheme" not in css
    html, _ = published
    # The family census, the obligation table, Appendix B and the glossary.
    assert len(re.findall(r'<div class="kpress-table-wrap"><table\b', html)) == 4


def test_the_paper_is_written_under_papers_by_its_slug(
    tmp_path: Path, rendered: tuple[str, str]
) -> None:
    html, markdown = rendered
    outputs = paper.output_files(tmp_path, html, markdown)
    assert {path.relative_to(tmp_path).as_posix(): text for path, text in outputs.items()} == {
        "papers/n11-threshold-bound-review.html": html,
        "papers/n11-threshold-bound-review.md": markdown,
    }
    assert 'href="n11-threshold-bound-review.md"' in html
    assert 'href="n11-threshold-bound-review.pdf"' in html


def test_the_figure_modules_facts_are_exactly_the_articles() -> None:
    """The figures lane's `caption_facts()` and the article's `CAPTION_FACT_KEYS` are one
    list, so the renderer's unused-fact refusal passes on the real render path, and the
    figure module's data inputs are among the page's declared inputs."""
    facts = paper.render_all_facts()
    assert set(facts) == set(paper.CAPTION_FACT_KEYS)
    for key, value in certificate_facts().items():
        assert facts[key] == value, key
    for path in n11_threshold_figures.FIGURE_INPUTS:
        assert (paper.REPO / path).resolve() in {p.resolve() for p in paper.RENDER_INPUTS}, path
    for module in ("n11_threshold_figures.py", "paper_figures.py"):
        assert paper.PACKING / "devtools" / module in paper.RENDER_INPUTS, module
    assert (
        paper.PACKING / "src" / "sqpack" / "fractional" / "parent_core.py"
        in paper.RENDER_INPUTS
    )


@pytest.fixture(scope="module")
def published() -> tuple[str, str]:
    """The article rendered with the real figures and facts, as the site build does."""
    return paper.render(
        ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        facts=paper.render_all_facts(),
        revision=REVISION,
    )


def test_the_actual_article_renders_with_the_real_figures(published: tuple[str, str]) -> None:
    html, markdown = published
    assert len(re.findall(r"<figure\b", html)) == 12
    assert html.count('<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram ') >= 12
    assert "{{" not in markdown
    assert "katex-error" not in html.split("<article", 1)[1].split("</article>", 1)[0]
    facts = paper.render_all_facts()
    said = " ".join(markdown.split())
    for phrase in (
        f"weight {facts['CHARGE_WEIGHT']} on the five sites {facts['CHARGE_SITES']}",
        f"Γ={facts['CERT_GAMMA']}".replace("Γ", "\\Gamma"),
        f"a surplus of {facts['CERT_SURPLUS_UNITS']} units",
        f"drawn {facts['CORE_EXAGGERATION']} times its true size",
        f"row {facts['CATALOGUE_TIGHT_ROW']}, at {facts['CATALOGUE_TIGHT_ANGLES']}",
        f"which is {facts['SIGNED_ABS_SUMS']} for the three families",
    ):
        assert phrase in said, phrase
    # The family census is the figure module's table, not a retyped one.
    assert facts["FAMILIES_TABLE"] in markdown
    assert markdown.count("| 2-of-5 |") == 2  # the census and Appendix B


def test_every_diagram_drawn_in_fixed_ink_keeps_a_light_ground_on_the_dark_theme() -> None:
    """Every figure of this paper is drawn by the series' roles in fixed ink, so each needs
    the light ground on the dark theme; the stylesheet's list is exactly those diagrams,
    keyed on KPress's resolved theme (Part III's rule and test)."""
    fixed, themed = set(), set()
    for svg in paper.render_all_figures().values():
        found = re.match(r'<svg\b[^>]*\bclass="n11-diagram (n11-[a-z-]+)"', svg)
        assert found is not None
        ink = re.findall(r'\b(?:fill|stroke)="(#[0-9a-fA-F]{3,6})"', svg)
        (fixed if ink else themed).add(found.group(1))
    assert fixed
    assert not themed
    css = paper.STYLE.read_text(encoding="utf-8")
    rule = re.search(
        r':root\[data-kpress-resolved-theme="dark"\]\s+\.n11-threshold-paper\s+:is\(([^)]*)\)\s*'
        r"\{\s*background: var\(--n11-threshold-diagram-ground\);\s*\}",
        css,
    )
    assert rule is not None
    listed = {name.strip().removeprefix(".") for name in rule.group(1).split(",")}
    assert listed == fixed
