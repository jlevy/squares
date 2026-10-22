"""The home page's News box keeps the canonical News articles and their public metadata,
under the archive's own significance filter in its compact form."""

from __future__ import annotations

import copy
import html
import re

import pytest

from devtools import check_results, news_highlights, render_changelog, site_topics
from devtools.profile_links import public_names


@pytest.fixture(scope="module")
def document() -> render_changelog.Document:
    return render_changelog.load()


def _entry(identifier: str, day: str, score: int) -> render_changelog.Document:
    return {
        "id": identifier,
        "date": day,
        "result_ids": ["T-154"],
        "significance": {"score": score, "rationale": "A News article."},
    }


def test_the_box_opens_on_s5_alone_once_s5_fills_it_and_otherwise_on_s4_and_s5() -> None:
    """The opening levels follow the archive (`default_levels`, the owner, 22 October
    2026): S5 alone where News holds `LIMIT` S5 articles, of any age, and S4 and S5 while
    it holds fewer. An article outside News, below S3 or excluded, never counts."""
    limit = news_highlights.LIMIT
    fives = [_entry(f"five-{index}", f"2026-10-0{index + 1}", 5) for index in range(limit)]
    others = [
        _entry("four", "2026-10-20", 4),
        _entry("three", "2026-10-21", 3),
        _entry("two", "2026-10-22", 2),
        {**_entry("excluded", "2026-10-22", 5), "news_exclusion": "Retained history only."},
    ]
    full = {"entries": [*fives, *others]}
    assert news_highlights.default_levels(full) == (5,)
    assert [entry["id"] for entry in news_highlights.highlights(full)] == [
        f"five-{index}" for index in reversed(range(limit))
    ]
    short = {"entries": [*fives[1:], *others]}
    assert news_highlights.default_levels(short) == render_changelog.NEWS_LEVELS == (4, 5)
    assert [entry["id"] for entry in news_highlights.highlights(short)] == [
        "four",
        *(f"five-{index}" for index in reversed(range(1, limit))),
    ][:limit]
    assert news_highlights.default_levels({"entries": others}) == (4, 5)
    assert not news_highlights.highlights({"entries": []})


def test_the_box_carries_the_newest_of_each_level_in_frozen_date_and_id_order() -> None:
    """Any choice of levels finds its newest `LIMIT` among the carried articles: the
    newest `LIMIT` at each level, in News order, ties on a day broken by id."""
    entries = [
        _entry("z-third", "2026-10-12", 5),
        _entry("low-score", "2026-10-14", 4),
        _entry("a-second", "2026-10-12", 5),
        _entry("older", "2026-09-29", 5),
        _entry("newest", "2026-10-13", 5),
        _entry("oldest", "2026-09-28", 5),
        _entry("three", "2026-10-15", 3),
        {**_entry("excluded", "2026-10-16", 5), "news_exclusion": "Retained history only."},
    ]
    for ordered in (entries, list(reversed(entries))):
        document = {"entries": ordered}
        assert [entry["id"] for entry in news_highlights.carried(document)] == [
            "three",
            "low-score",
            "newest",
            "a-second",
            "z-third",
        ]
        assert [entry["id"] for entry in news_highlights.highlights(document)] == [
            "newest",
            "a-second",
            "z-third",
        ]


def test_the_box_follows_new_s5_articles_with_and_without_t194(
    document: render_changelog.Document,
) -> None:
    """On the record today, and with the S5 article for T-194 of 16 October that another
    lane adds: the box opens on S5 whenever News holds three S5 articles, and leads with
    the newest of them."""
    for added in (False, True):
        data = copy.deepcopy(document)
        if added and not any(
            "T-194" in entry.get("result_ids", []) for entry in data["entries"]
        ):
            model = next(
                entry
                for entry in render_changelog.news_entries(data)
                if render_changelog.entry_significance(entry)["score"] == 5
            )
            data["entries"].append(
                {**copy.deepcopy(model), "id": "t194-for-this-test", "date": "2026-10-16"}
            )
        fives = [
            entry
            for entry in render_changelog.news_entries(data)
            if render_changelog.entry_significance(entry)["score"] == 5
        ]
        levels = news_highlights.default_levels(data)
        assert levels == ((5,) if len(fives) >= news_highlights.LIMIT else (4, 5))
        shown = news_highlights.highlights(data)
        assert len(shown) == news_highlights.LIMIT
        if levels == (5,):
            assert list(shown) == fives[: news_highlights.LIMIT]
        if added:
            assert shown[0]["date"] >= "2026-10-16"


def _cards(rendered: str) -> dict[str, str]:
    return {
        identifier: card
        for card, identifier in re.findall(
            r'(<section (?:hidden )?class="site-news-day"[^>]*>.*?data-news-entry="([^"]+)"'
            r".*?</section>)",
            rendered,
            re.DOTALL,
        )
    }


def test_homepage_and_archive_render_the_same_articles_and_cards(
    document: render_changelog.Document,
) -> None:
    before = copy.deepcopy(document)
    carried = news_highlights.carried(document)
    selected = news_highlights.highlights(document)
    rendered = news_highlights.render(document)
    archive = render_changelog.render_news(document)
    preview_cards = _cards(rendered)
    archive_cards = _cards(archive)
    assert list(preview_cards) == [entry["id"] for entry in carried]
    shown = [
        identifier
        for identifier, card in preview_cards.items()
        if card.startswith('<section class="site-news-day"')
    ]
    assert shown == [entry["id"] for entry in selected]
    assert 0 < len(shown) <= news_highlights.LIMIT
    assert f'data-news data-news-limit="{news_highlights.LIMIT}"' in rendered
    assert "site-result-status" not in rendered
    assert "data-kind=" not in rendered
    for entry in carried:
        identifier = entry["id"]
        anchor = render_changelog.entry_anchor(identifier)
        # Which cards start hidden is each list's own choice.
        preview = preview_cards[identifier].replace("<section hidden ", "<section ", 1)
        canonical = archive_cards[identifier].replace("<section hidden ", "<section ", 1)
        # Preview titles link to the full archive. Daily bookmarks occur only once.
        preview = re.sub(
            r'<h3><a href="news.html#[^"]+">(.*?)</a></h3>', r"<h3>\1</h3>", preview
        )
        preview = re.sub(r'<div id="changelog-date-[^"]+"></div>\n?', "", preview)
        canonical = re.sub(r'<div id="changelog-date-[^"]+"></div>\n?', "", canonical)
        assert preview == canonical
        assert f'id="{anchor}"' in preview
        assert f'data-news-day="{entry["date"]}"' in preview
        assert (
            f"<h3>{render_changelog.inline_html(entry['title'], allow_links=False)}</h3>"
            in preview
        )
        assert render_changelog.news_topics(entry.get("topics", [])) in preview
        assert preview.count('class="site-significance"') == 1
        assert f'aria-controls="{anchor}-body"' in preview
        assert f'href="news.html#{anchor}"' in rendered
    assert document == before


def test_homepage_draws_the_archives_significance_filter_compact_and_preselected(
    document: render_changelog.Document,
) -> None:
    """The box's filter is the archive's own significance widget, drawn by the one
    function both call, in its compact form: the same buttons, titles and legend, pressed
    at the box's opening levels, with no topics, reset or count, hidden until the script
    shows it."""
    rendered = news_highlights.render(document)
    archive = render_changelog.render_news(document)
    levels = news_highlights.default_levels(document)
    widget = render_changelog.news_significance_filter(levels)
    assert rendered.startswith(
        '<div class="site-news-filters site-news-filters-compact sans-text" '
        f"data-news-filters data-site-tooltip-outside hidden>{widget}"
        f"{render_changelog.NEWS_EMPTY}</div>"
    )
    assert render_changelog.news_significance_filter() in archive
    assert re.findall(r'data-news-score="(\d)"[^>]*aria-pressed="true"', widget) == [
        str(level) for level in levels
    ]
    for absent in ('aria-labelledby="news-topics-label"', "data-news-reset", "data-news-count"):
        assert absent not in rendered
        assert absent in archive
    # The archive itself still opens on S4 and S5 under its full filters.
    assert re.findall(
        r'data-news-score="(\d)"[^>]*aria-pressed="true"',
        archive.split('aria-labelledby="news-topics-label"', 1)[0],
    ) == ["4", "5"]


def test_news_keeps_both_reported_proofs_and_their_complete_qualification_text(
    document: render_changelog.Document,
) -> None:
    cards = _cards(render_changelog.render_news(document))
    fitzharding = cards["fitzharding-n17-reported-proof"]
    overbeck = cards["overbeck-n17-candidate-proof"]
    for card in (fitzharding, overbeck):
        assert 'data-news-topic="optimality">Optimality</span>' in card
        assert 'data-news-topic="verification">Verification</span>' in card
        assert 'data-news-topic="formalization"' not in card
        assert "V0/C1" in card
        assert 'datetime="2026-10-13"' in card
    assert "the full Lean build has not been replayed here" in fitzharding
    assert "The full capture computation" in overbeck
    assert "These samples do not confirm the whole" in overbeck
    assert 'href="https://squaremath.org/result/t-154.html"' in fitzharding
    assert 'href="https://squaremath.org/result/t-153.html"' in overbeck


def test_news_ahmed_article_keeps_the_result_and_explainer_reachable(
    document: render_changelog.Document,
) -> None:
    card = _cards(render_changelog.render_news(document))["ahmed-eleven-square-optimality"]
    assert 'datetime="2026-09-30"' in card
    assert "V3/C3" in card
    assert "a second independent proof method" in card
    assert 'href="https://squaremath.org/result/t-060.html"' in card
    assert 'href="https://squaremath.org/papers/n11-optimality-review.html"' in card


def test_homepage_and_archive_link_preferred_names_directly_to_reviewed_profiles(
    document: render_changelog.Document,
) -> None:
    expected = {
        "fitzharding-n17-reported-proof": (
            ("Oscar Fitzharding", "oscar-fitzharding"),
            ("John Bidwell", "john-bidwell"),
            ("Marc Leonard Overbeck", "marc-leonard-overbeck"),
            ("Hiroaki Hosono", "hiroaki-hosono"),
        ),
        "overbeck-n17-candidate-proof": (
            ("Marc Leonard Overbeck", "marc-leonard-overbeck"),
            ("John Bidwell", "john-bidwell"),
        ),
        "ahmed-eleven-square-optimality": (
            ("Manasseh Ahmed", "manasseh-ahmed"),
            ("Walter Trump", "walter-trump"),
            ("Joshua Levy", "joshua-levy"),
            ("Marc Leonard Overbeck", "marc-leonard-overbeck"),
        ),
    }
    home = news_highlights.render(document)
    archive = render_changelog.render_news(document)
    # The box carries the newest articles of each level, so these three leave it in time;
    # the archive keeps them all.
    assert set(expected) & set(_cards(home))
    limited = f' data-news-limit="{news_highlights.LIMIT}"'
    for rendered, attributes in ((home, limited), (archive, "")):
        # The names stay plain links, since their container says so once and the profile
        # popover leaves every profile link inside it alone.
        assert (
            f'<div class="site-news" data-news{attributes} data-contributor-plain>' in rendered
        )
        cards = _cards(rendered)
        for identifier, people in expected.items():
            if identifier not in cards and rendered is home:
                continue
            card = cards[identifier]
            for _preferred_name, profile_id in people:
                label = public_names()[profile_id].label
                assert f'<a href="profiles/{profile_id}.html">{html.escape(label)}</a>' in card
            assert "data-person" not in card


@pytest.mark.parametrize("suffix", ["", "?plain=1&view=full#accounts"])
def test_inline_news_converts_repository_profile_links_once(suffix: str) -> None:
    target = f"packing/contributors/people/hiroaki-hosono.md{suffix}"
    rendered = render_changelog.inline_html(f"Reviewed by [Hiroaki Hosono]({target}).")
    canonical = html.escape(f"profiles/hiroaki-hosono.html{suffix}", quote=True)
    assert rendered == f'Reviewed by <a href="{canonical}">Hiroaki Hosono</a>.'
    math = render_changelog.inline_html(rf"$\href{{{target}}}{{H}}$")
    assert "<math" in math
    assert f'href="{canonical}"' in math


def test_inline_news_keeps_authored_preferred_names_and_styling() -> None:
    target = "packing/contributors/people/hiroaki-hosono.md"
    for label, styled in (
        ("**Hiroaki Hosono**", "<strong>Hiroaki Hosono</strong>"),
        (
            "*Reviewed by **Hiroaki Hosono***",
            "<em>Reviewed by <strong>Hiroaki Hosono</strong></em>",
        ),
    ):
        rendered = render_changelog.inline_html(
            f"Hiroaki Hosono; [{label}]({target}); "
            "[**Hiroaki Hosono**](https://example.org/proof); Hiroaki Hosono."
        )
        assert rendered == (
            f'Hiroaki Hosono; <a href="profiles/hiroaki-hosono.html">{styled}</a>; '
            '<a href="https://example.org/proof"><strong>Hiroaki Hosono</strong></a>; '
            "Hiroaki Hosono."
        )


@pytest.mark.parametrize(
    ("target", "message"),
    [
        ("packing/contributors/people/missing-person-not-a-profile.md", "missing repository"),
        ("packing/contributors/people/%252e%252e/README.md", "repository-relative"),
        ("packing/contributors/people/hiroaki-hosono.md?x=%3Cscript%3E", "unsafe"),
    ],
)
def test_inline_news_rejects_missing_and_unsafe_profile_targets(
    target: str, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        render_changelog.inline_html(f"[Person]({target})")


def test_news_schema_uses_the_shared_topic_vocabulary() -> None:
    import yaml  # noqa: PLC0415

    schema = yaml.safe_load(render_changelog.SCHEMA.read_text())
    entry = schema["$defs"]["entry"]
    assert set(entry["properties"]["topics"]["items"]["enum"]) == set(
        render_changelog.NEWS_TOPICS
    )
    assert set(render_changelog.NEWS_TOPICS) == set(site_topics.TOPICS) - {
        "correction",
        "audit",
    }
    assert set(check_results.KINDS) <= set(site_topics.TOPICS)
    assert site_topics.topic_label("lower-bound") == "Lower bound"
    assert site_topics.topic_label("upper-bound") == "Upper bound"
    with pytest.raises(ValueError, match="unknown topic"):
        site_topics.topic_label("unregistered")
    with pytest.raises(ValueError, match="unknown topic"):
        site_topics.topic_label("documentation")
    filters = render_changelog.news_filters()
    for topic in ("documentation", "correction", "audit"):
        assert f'data-news-topic="{topic}"' not in filters
        with pytest.raises(ValueError, match="unknown News topic"):
            render_changelog.news_topics([topic])
