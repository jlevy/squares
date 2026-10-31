"""The launch history reaches both reader surfaces and the publication scope."""

from __future__ import annotations

import copy
import html
import re
from fnmatch import fnmatchcase

import pytest

from devtools import (
    check_published_site,
    news_highlights,
    pages_scope,
    render_changelog,
    render_overview,
    site_documents,
    site_math,
)
from devtools.pages_scope import REPO
from devtools.profile_links import public_names
from tests import site_renders

#: The News archive's own card container, where a story and its links live.
NEWS_CARDS = '<div class="site-news" data-news data-contributor-plain>'


@pytest.fixture(scope="module")
def views() -> tuple[dict, str, str, str, str, str]:
    document = render_changelog.load()
    return (
        document,
        site_renders.html("news.html"),
        render_changelog.render(document),
        site_renders.html(render_changelog.CHANGELOG_PAGE),
        site_renders.html("about.html"),
        site_renders.html("index.html"),
    )


def test_the_changelog_keeps_every_entry_and_news_keeps_the_public_launches(
    views: tuple[dict, str, str, str, str, str],
) -> None:
    """Since 26 October 2026 the whole retained history is the Changelog page's and News
    shows the S3 and above stories, and the two surfaces divide the work rather than share
    it: News tells the story with every link it declares, while the Changelog gives one
    brief line an entry, its GitHub threads, and a link to the story where there is one.
    A change News never shows has no other reader surface, so its line carries everything
    it declares."""
    document, news, github, changelog, _about, _home = views
    cards = news[news.index(NEWS_CARDS) :]
    for entry in document["entries"]:
        anchor = render_changelog.entry_anchor(entry["id"])
        assert f'id="{anchor}"' in changelog
        assert f'id="{anchor}"' in github
        excluded = "news_exclusion" in entry or entry["significance"]["score"] < 3
        if excluded:
            target = render_changelog.archived_news_targets(document)[anchor]
            assert f'href="{target}" data-news-target' in news
            assert f'data-news-entry="{entry["id"]}"' not in news
        else:
            # The line is the summary and the story is the detail, written once.
            assert f'href="{render_changelog.NEWS_PAGE}#{anchor}"' in changelog
        for number in entry["pull_requests"]:
            target = f"{document['repository']}/pull/{number}"
            if not excluded:
                assert target in cards
            assert target in github
            assert target in changelog
        for artifact in entry.get("artifacts", []):
            if not excluded:
                assert artifact["target"] in cards
            assert artifact["target"] in github
            if excluded:
                assert artifact["target"] in changelog


def test_news_links_named_contributors_directly_to_their_profiles(
    views: tuple[dict, str, str, str, str, str],
) -> None:
    document, news, github, _changelog, _about, _home = views
    history = news
    eligible = {entry["id"] for entry in render_changelog.news_entries(document)}
    published_profiles = []
    for entry in document["entries"]:
        prose = entry["summary"] + "\n" + entry.get("details", "")
        for name, identifier in re.findall(
            r"\[([^\]]+)\]\(packing/contributors/people/([a-z0-9-]+)\.md\)", prose
        ):
            assert f"[{name}](packing/contributors/people/{identifier}.md)" in github
            if entry["id"] in eligible:
                published_profiles.append((name, identifier))
    assert published_profiles
    for _name, identifier in published_profiles:
        label = public_names()[identifier].label
        assert f'<a href="profiles/{identifier}.html">{html.escape(label)}</a>' in history
    assert "wand125\N{RIGHT SINGLE QUOTATION MARK}s" not in history
    # The names stay plain links: the News container declares its profile links plain
    # once, and every one of them lies inside it.
    plain = history.index(NEWS_CARDS)
    assert all(
        history.index(f'<a href="profiles/{identifier}.html">') > plain
        for _name, identifier in published_profiles
    )


def test_a_yaml_only_history_change_selects_and_deploys_news() -> None:
    workflow = pages_scope.load_workflow()
    changed = "packing/site-changelog.yaml"
    decisions = pages_scope.decide([changed], pages_scope.declared_inputs())
    assert any(item.half == "overview" and item.in_scope for item in decisions)
    push = workflow["on"]["push"]
    assert any(fnmatchcase(changed, pattern) for pattern in push["paths"])
    assert REPO / changed in render_overview.RENDER_INPUTS


def test_repository_changelog_links_land_on_the_changelog_page() -> None:
    """A Markdown link to the file lands on the page that shows what it holds."""
    assert site_documents.RECORD_PAGES["CHANGELOG.md"] == render_changelog.CHANGELOG_PAGE


def test_publication_audit_refuses_a_missing_launch_link(
    views: tuple[dict, str, str, str, str, str],
) -> None:
    document, news, _github, changelog, _about, _home = views
    assert all(passed for passed, _line in check_published_site.news_checks(news))
    assert all(passed for passed, _line in check_published_site.changelog_checks(changelog))
    told = {entry["id"] for entry in render_changelog.news_entries(document)}
    # Each page is held to the artifacts it is the reader's surface for: News to every
    # story's, the Changelog to those of a change News never shows.
    shown = next(
        artifact["target"]
        for entry in document["entries"]
        if entry["id"] in told
        for artifact in entry.get("artifacts", [])
    )
    retained = next(
        artifact["target"]
        for entry in document["entries"]
        if entry["id"] not in told
        for artifact in entry.get("artifacts", [])
    )
    for page, check, target in (
        (news, check_published_site.news_checks, shown),
        (changelog, check_published_site.changelog_checks, retained),
    ):
        damaged = page.replace(target, "https://example.com/missing")
        assert damaged != page
        assert not all(passed for passed, _line in check(damaged))


def test_the_changelog_audit_holds_every_declared_link_of_a_below_floor_entry(
    views: tuple[dict, str, str, str, str, str],
) -> None:
    """An entry News never shows still has to arrive whole on the Changelog page: its
    publication evidence and its supporting references as well as its issues, pull
    requests and artifacts. The audit read only the last three until 26 October 2026, so
    a lost evidence or reference link left its anchors intact and passed."""
    document, _news, _github, changelog, _about, _home = views
    public = {entry["id"] for entry in render_changelog.news_entries(document)}
    below = [entry for entry in document["entries"] if entry["id"] not in public]
    assert below
    issues = {
        entry["id"]: {
            render_changelog.serialized_target(
                f"{document['repository']}/issues/{number}", destination="site"
            )
            for number in entry.get("issues", [])
        }
        for entry in below
    }
    checked = 0
    for entry in below:
        targets = [
            *([entry["publication"]["evidence"]] if entry.get("publication") else []),
            *(item["target"] for item in entry.get("references", [])),
        ]
        for target in targets:
            served = render_changelog.serialized_target(target, destination="site")
            # A reference naming a listed issue is that issue's own link, written once.
            if served in issues[entry["id"]] or served not in changelog:
                continue
            damaged = changelog.replace(served, "https://example.com/missing")
            assert damaged != changelog
            assert not all(
                passed for passed, _line in check_published_site.changelog_checks(damaged)
            ), (entry["id"], target)
            checked += 1
    assert checked


def test_publication_audit_accepts_the_renderers_encoded_artifact_destinations(
    views: tuple[dict, str, str, str, str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    document = copy.deepcopy(views[0])
    told = {entry["id"] for entry in render_changelog.news_entries(document)}
    # One artifact on each surface: a story's, which News writes, and one belonging to a
    # change News never shows, which only the Changelog line carries.
    for shown in (True, False):
        artifact = next(
            artifact
            for entry in document["entries"]
            if (entry["id"] in told) is shown
            for artifact in entry.get("artifacts", [])
        )
        artifact["target"] += "#proof(1)"
    render_changelog.validate(document)
    monkeypatch.setattr(render_changelog, "load", lambda: document)
    news = render_overview.news_page().html
    changelog = render_overview.changelog_page().html
    assert "#proof%281%29" in news
    assert "#proof%281%29" in changelog
    assert all(passed for passed, _line in check_published_site.news_checks(news))
    assert all(passed for passed, _line in check_published_site.changelog_checks(changelog))


def test_news_has_one_card_per_entry_and_home_shows_the_newest_at_its_opening_levels(
    views: tuple[dict, str, str, str, str, str],
) -> None:
    document, news, _github, _changelog, about, home = views
    ordered = render_changelog.news_entries(document)
    assert {entry["significance"]["score"] for entry in ordered} <= {3, 4, 5}
    assert re.findall(r'<button[^>]*data-news-score="(\d)"', news) == ["3", "4", "5"]
    assert re.findall(r'data-news-entry="([^"]+)"', news) == [e["id"] for e in ordered]
    assert re.findall(r'data-news-day="([^"]+)"', news) == [e["date"] for e in ordered]
    for day in {entry["date"] for entry in ordered}:
        assert news.count(f'id="changelog-date-{day}"') == 1
    selected = news_highlights.highlights(document)
    levels = news_highlights.default_levels(document)
    assert len(selected) == news_highlights.LIMIT
    assert all(entry["significance"]["score"] in levels for entry in selected)
    assert (
        selected
        == tuple(entry for entry in ordered if entry["significance"]["score"] in levels)[
            : news_highlights.LIMIT
        ]
    )
    carried = [entry["id"] for entry in news_highlights.carried(document)]
    assert re.findall(r'data-news-entry="([^"]+)"', home) == carried
    shown = re.findall(r'<section class="site-news-day" id="changelog-entry-([^"]+)"', home)
    assert shown == [entry["id"] for entry in selected]
    # Today News holds four S5 articles, so the box opens on S5 and leads with T-245's
    # (25 October).
    assert levels == (5,)
    assert [entry["result_ids"] for entry in selected] == [["T-245"], ["T-194"], ["T-154"]]
    for entry in selected:
        anchor = render_changelog.entry_anchor(entry["id"])
        assert f'href="news.html#{anchor}"' in home
    assert '<a class="site-action" href="news.html" data-news-carry>All News' in home
    assert 'id="news" class="site-title">News' in news
    assert re.search(
        r'<a(?=[^>]*data-page="news")(?=[^>]*aria-current="page")(?=[^>]*href="news.html")[^>]*>',
        news,
    )
    assert 'href="news.html"' in about
    assert "data-news-entry=" not in about
    assert 'class="site-news-day"' not in about
    for anchor, target in render_changelog.archived_news_targets(document).items():
        assert f'id="{anchor}" href="{target}" data-news-target' in about
    for entry in ordered:
        anchor = render_changelog.entry_anchor(entry["id"])
        assert f'id="{anchor}" href="news.html#{anchor}" data-news-target' in about
        card = news.split(f'id="{anchor}"', 1)[1].split("</section>", 1)[0]
        assert re.findall(r'data-news-topic="([^"]+)"', card) == entry.get("topics", [])


@pytest.mark.parametrize(
    ("formula", "structure"),
    [
        (r"s(11) \ge 381/100", "mrow"),
        (r"s(n) \ge \sqrt{n}", "msqrt"),
        (r"s(11) \ge \frac{381}{100}", "mfrac"),
        (r"s(n)^2 \ge n", "msup"),
    ],
)
def test_news_cards_keep_the_actual_article_and_structured_math_once(
    formula: str, structure: str
) -> None:
    document = copy.deepcopy(render_changelog.load())
    first = render_changelog.news_entries(document)[0]
    first["summary"] = f"Verified **bound & label** ${formula}$. Use `<tag>`."
    first["details"] = "Actual article detail with a [proof](https://example.com/proof)."
    rendered = render_changelog.render_news(document, limit=1)
    assert rendered.count("Actual article detail") == 1
    assert rendered.count("data-news-entry=") == 1
    assert "<strong>bound &amp; label</strong>" in rendered
    assert "<code>&lt;tag&gt;</code>" in rendered
    assert f"<{structure}>" in rendered
    assert "<summary" not in rendered
    assert "site-news-preview" not in rendered
    assert 'href="https://example.com/proof"' in rendered
    formulas = site_math.formula_sources(rendered)
    assert [item.source for item in formulas].count(formula) == 1
    assert next(item for item in formulas if item.source == formula).profile == "prose"
    assert all(item.profile == "sans" for item in formulas if item.source != formula)


def test_publication_audit_refuses_lost_archives_or_reintroduced_maintenance(
    views: tuple[dict, str, str, str, str, str],
) -> None:
    document, news, _github, _changelog, _about, _home = views
    excluded = [entry for entry in document["entries"] if "news_exclusion" in entry]
    # News carries the mathematical and newsworthy items; a site, documentation or
    # tooling change is a Changelog line instead (the owner, 26 October 2026). Nothing
    # touching the records, their regularization or the mathematics is on this roster.
    assert sorted(entry["id"] for entry in excluded) == [
        # This change applies its own rule to itself: moving the log to the Changelog is
        # a site-only change, so it is a line there rather than a News story.
        "changelog-day-log-and-news-division",
        "contributor-profiles-and-contribution-summaries",
        "every-selected-validation-check-runs",
        "paper-typography-and-title-case",
        "project-changelog-and-independent-editions",
        "significance-levels-for-news-and-pull-requests",
        "unified-site-navigation",
    ]
    # Two more were excluded on 26 October 2026 and put back the same day, because the
    # test above is the one that has to hold: `basic-and-advanced-tutorials` is a
    # substantial public explanation of the problem and the research methods by its own
    # rationale, and `readable-atlas-and-print-exports` launched the redesigned posters,
    # which are published artifacts with their own editions. Neither is site-only.
    assert all(entry["news_exclusion"].strip() for entry in excluded)
    maintenance = next(
        entry for entry in excluded if entry["id"] == "paper-typography-and-title-case"
    )
    assert maintenance["pull_requests"] == [492]
    assert "documentation" in maintenance["categories"]
    assert all("documentation" not in entry.get("topics", []) for entry in document["entries"])
    assert all(passed for passed, _line in check_published_site.news_checks(news))
    archived = render_changelog.archived_news_targets(document)
    target = next(iter(archived.values()))
    damaged = news.replace(target, "https://example.com/missing-archive")
    assert not all(passed for passed, _line in check_published_site.news_checks(damaged))
    damaged = news + f'<article data-news-entry="{maintenance["id"]}"></article>'
    assert not all(passed for passed, _line in check_published_site.news_checks(damaged))
