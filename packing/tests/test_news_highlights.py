"""Homepage previews keep the canonical News articles and their public metadata."""

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


def test_selection_uses_eligible_s5_result_articles_in_frozen_date_and_id_order() -> None:
    def entry(identifier: str, day: str, score: int = 5) -> render_changelog.Document:
        return {
            "id": identifier,
            "date": day,
            "result_ids": ["T-154"],
            "significance": {"score": score, "rationale": "A result announcement."},
        }

    candidates = [
        entry("z-third", "2026-10-12"),
        entry("low-score", "2026-10-14", 4),
        entry("a-second", "2026-10-12"),
        entry("older", "2026-09-29"),
        entry("newest", "2026-10-13"),
        {**entry("unrelated", "2026-10-15"), "result_ids": []},
        {**entry("excluded", "2026-10-16"), "news_exclusion": "Retained history only."},
    ]
    expected = ["newest", "a-second", "z-third"]
    for ordered in (candidates, list(reversed(candidates))):
        assert [
            item["id"] for item in news_highlights.highlights({"entries": ordered})
        ] == expected
    assert not news_highlights.highlights({"entries": candidates[1:2] + candidates[5:]})
    assert news_highlights.highlights({"entries": candidates[3:4]}) == (candidates[3],)
    assert not news_highlights.highlights({"entries": []})


def _cards(rendered: str) -> dict[str, str]:
    return {
        identifier: card
        for card, identifier in re.findall(
            r'(<section class="site-news-day"[^>]*>.*?data-news-entry="([^"]+)".*?</section>)',
            rendered,
            re.DOTALL,
        )
    }


def test_homepage_and_archive_render_the_same_articles_and_cards(
    document: render_changelog.Document,
) -> None:
    before = copy.deepcopy(document)
    selected = news_highlights.highlights(document)
    rendered = news_highlights.render(document)
    archive = render_changelog.render_news(document)
    preview_cards = _cards(rendered)
    archive_cards = _cards(archive)
    assert list(preview_cards) == [entry["id"] for entry in selected]
    assert 0 < len(preview_cards) <= 3
    assert "data-news-filters" not in rendered
    assert "site-result-status" not in rendered
    assert "data-kind=" not in rendered
    for entry in selected:
        identifier = entry["id"]
        anchor = render_changelog.entry_anchor(identifier)
        preview = preview_cards[identifier]
        canonical = archive_cards[identifier]
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


def test_homepage_does_not_fill_missing_s5_result_slots_from_other_news(
    document: render_changelog.Document,
) -> None:
    data = copy.deepcopy(document)
    selected = news_highlights.highlights(data)
    for entry in render_changelog.news_entries(data):
        if entry.get("result_ids") and entry["significance"]["score"] == 5:
            entry["significance"]["score"] = 4
    assert not _cards(news_highlights.render(data))
    selected[0]["significance"]["score"] = 5
    assert list(_cards(news_highlights.render(data))) == [selected[0]["id"]]


def test_homepage_keeps_both_reported_proofs_and_their_complete_qualification_text(
    document: render_changelog.Document,
) -> None:
    cards = _cards(news_highlights.render(document))
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
    assert 'href="https://jlevy.github.io/squares/result/t-154.html"' in fitzharding
    assert 'href="https://jlevy.github.io/squares/result/t-153.html"' in overbeck


def test_homepage_ahmed_article_keeps_the_result_and_explainer_reachable(
    document: render_changelog.Document,
) -> None:
    card = _cards(news_highlights.render(document))["ahmed-eleven-square-optimality"]
    assert 'datetime="2026-09-30"' in card
    assert "V3/C3" in card
    assert "a second independent proof method" in card
    assert 'href="https://jlevy.github.io/squares/result/t-060.html"' in card
    assert 'href="https://jlevy.github.io/squares/papers/n11-optimality-review.html"' in card


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
    for rendered in (news_highlights.render(document), render_changelog.render_news(document)):
        cards = _cards(rendered)
        for identifier, people in expected.items():
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
