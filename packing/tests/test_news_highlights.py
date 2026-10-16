"""Homepage News selects existing S5 results without changing project history."""

from __future__ import annotations

import copy
import re
from dataclasses import replace

import pytest

from devtools import (
    check_results,
    news_highlights,
    overview_data,
    overview_sections,
    render_changelog,
    site_math,
    site_topics,
)
from devtools.register_prose import paragraphs
from tests import site_renders


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


def _candidate(
    original: overview_data.Result, result_id: str, day: str, score: int = 5
) -> overview_data.Result:
    record = copy.deepcopy(original.record)
    record["id"] = result_id
    if record.get("attribution"):
        record["attribution"]["published"] = day
    else:
        record["established"] = day
    record["significance"]["score"] = score
    return replace(original, record=record)


def test_selection_uses_only_s5_and_the_existing_date_and_id_order(
    overview: overview_data.Overview,
) -> None:
    original = next(result for result in overview.results if result.id == "T-154")
    candidates = [
        _candidate(original, "T-001", "2026-10-12"),
        _candidate(original, "T-999", "2026-10-13", 4),
        _candidate(original, "T-003", "2026-10-12"),
        _candidate(original, "T-004", "2026-09-29"),
        _candidate(original, "T-002", "2026-10-12"),
    ]
    example = replace(overview, results=candidates)
    assert [result.id for result in news_highlights.highlights(example)] == [
        "T-003",
        "T-002",
        "T-001",
    ]
    assert [
        result.id
        for result in news_highlights.highlights(
            replace(example, results=list(reversed(candidates)))
        )
    ] == ["T-003", "T-002", "T-001"]
    assert not news_highlights.highlights(replace(example, results=[candidates[1]]))


def test_current_news_has_three_results_including_the_older_s5_result(
    overview: overview_data.Overview,
) -> None:
    selected = news_highlights.highlights(overview)
    assert [result.id for result in selected] == ["T-154", "T-153", "T-060"]
    assert [result.dated for result in selected] == [
        ("published", "2026-10-12"),
        ("published", "2026-10-12"),
        ("published", "2026-09-29"),
    ]
    rendered = news_highlights.render(overview)
    assert re.findall(r'data-news-entry="([^"]+)"', rendered) == ["T-154", "T-153", "T-060"]
    assert rendered.count('class="site-news-day"') == 3
    assert rendered.count('data-news-topic="optimality"') == 2
    assert rendered.count('data-news-topic="formalization"') == 1
    assert 'data-kind="formalization"' not in rendered
    assert 'data-news-day="2026-10-12"' in rendered
    assert 'data-news-day="2026-09-29"' in rendered
    assert rendered.count('data-news-day="2026-10-12"') == 2
    assert re.findall(r'class="site-news-day" id="([^"]+)"', rendered) == [
        "news-result-t-154",
        "news-result-t-153",
        "news-result-t-060",
    ]
    assert re.findall(r'class="site-news-body" id="([^"]+)"', rendered) == [
        "news-result-t-154-body",
        "news-result-t-153-body",
        "news-result-t-060-body",
    ]
    assert 'id="t-154"' not in rendered


def test_news_keeps_claim_excerpts_credit_rungs_and_canonical_result_links(
    overview: overview_data.Overview,
) -> None:
    rendered = news_highlights.render(overview)
    for result in news_highlights.highlights(overview):
        match = re.search(
            rf'<article class="site-news-item" data-news-entry="{result.id}">(.*?)</article>',
            rendered,
            re.DOTALL,
        )
        assert match is not None
        article = match.group(1)
        title = render_changelog.inline_html(result.summary, allow_links=False)
        assert f"<h3>{title}</h3>" in article
        assert overview_sections.credit_cell(result.credit) in article
        assert f'<time datetime="{overview_sections.first_day(result.dated[1])}">' in article
        assert overview_sections.ladder_chips(result) in article
        assert overview_sections.status_marks(result) in article
        assert article.count(f'data-news-topic="{result.record["kind"]}"') == 1
        assert "data-kind=" not in article
        qualifier = "Reported result: this project has not verified the complete claim."
        claim = paragraphs(result.record["claim"])[0]
        for full, surname in (
            ("Oscar Fitzharding", "Fitzharding"),
            ("John Bidwell", "Bidwell"),
            ("Marc Leonard Overbeck", "Overbeck"),
        ):
            claim = claim.replace(full, surname)
            assert full not in article
        excerpt = render_changelog.inline_html(claim)
        if result.record["verification"] == "V0":
            assert article.index(qualifier) < article.index(excerpt)
        else:
            assert qualifier not in article
        assert f"<p>{excerpt}</p>" in article
        assert f'href="result/{result.id.lower()}.html"' in article
        assert f"Full result {result.id}" in article
    assert "Nothing here has repeated that build." not in rendered
    assert "The complete capture recomputation and ten trees have not been run." not in rendered


def test_news_reads_no_launch_history_and_mutates_no_result_record(
    overview: overview_data.Overview, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = copy.deepcopy(overview)

    def no_history() -> render_changelog.Document:
        raise AssertionError("result News must not read or backfill launch history")

    monkeypatch.setattr(render_changelog, "load", no_history)
    assert news_highlights.render(overview)
    assert overview == before


@pytest.mark.parametrize("kind", check_results.KINDS)
def test_result_kind_and_evidence_survive_news_topic_selection(
    overview: overview_data.Overview, kind: str
) -> None:
    candidate = _candidate(overview.results[0], "T-999", "2026-10-14")
    candidate.record["kind"] = kind
    rendered = news_highlights.render(replace(overview, results=[candidate]))
    topics = re.findall(r'data-news-topic="([^"]+)"', rendered)
    assert topics == ([kind] if kind not in {"correction", "audit"} else [])
    label = site_topics.topic_label(kind)
    if topics:
        assert f'data-news-topic="{kind}">{label}</span>' in rendered
    assert overview_sections.kind_chip(candidate) == site_topics.topic_chip(
        kind, attribute="data-kind"
    )
    assert label[0].isupper()
    assert label[1:] == label[1:].lower()
    assert overview_sections.ladder_chips(candidate) in rendered
    assert overview_sections.status_marks(candidate) in rendered
    assert "data-kind=" not in rendered
    assert rendered.count('class="site-significance"') == 1
    assert 'data-level="5"' in rendered
    assert overview_sections.credit_cell(candidate.credit) in rendered
    excerpt = render_changelog.inline_html(paragraphs(candidate.record["claim"])[0])
    assert f"<p>{excerpt}</p>" in rendered


def test_a_real_rigidity_result_can_enter_the_s5_news_without_changing_its_claim(
    overview: overview_data.Overview,
) -> None:
    original = next(result for result in overview.results if result.id == "T-012")
    candidate = _candidate(original, original.id, "2026-10-14")
    assert candidate.record["kind"] == "rigidity"
    example = replace(overview, results=[candidate, *overview.results])
    assert news_highlights.highlights(example)[0] is candidate
    rendered = news_highlights.render(example)
    article = rendered.split('data-news-entry="T-012">', 1)[1].split("</article>", 1)[0]
    assert 'data-news-topic="rigidity">Rigidity</span>' in article
    assert overview_sections.ladder_chips(candidate) in article
    assert overview_sections.status_marks(candidate) in article
    assert article.count('data-news-topic="rigidity"') == 1
    assert "data-kind=" not in article
    assert overview_sections.credit_cell(original.credit) in article
    excerpt = render_changelog.inline_html(paragraphs(original.record["claim"])[0])
    assert f"<p>{excerpt}</p>" in article
    with pytest.raises(ValueError, match="unknown News topic"):
        render_changelog.news_topics(["not-a-topic"])


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


def test_news_name_display_preserves_ambiguity_aliases_and_canonical_identifiers(
    overview: overview_data.Overview,
) -> None:
    names = {
        "Oscar Fitzharding": "Fitzharding",
        "John Bidwell": "Bidwell",
        "Ryan Xu": "Xu",
        "Ryan Xu (ry-xu)": "Xu",
        "Nate Chaoweeraprasit": "Chaoweeraprasit",
        "Nate Chaoweeraprasit (itsnaka)": "Chaoweeraprasit",
        "Alice Smith": "Smith",
        "Bob Smith": "Smith",
        "PingYou Ltd": "PingYou Ltd",
    }
    text = (
        "Oscar Fitzharding and John Bidwell; Ryan Xu (ry-xu); "
        "Nate Chaoweeraprasit (itsnaka); Alice Smith and Bob Smith; "
        "PingYou Ltd, Guzhou0806; Oscar Fitzhardington; "
        "https://example.org/Oscar%20Fitzharding; $s(17) = 4.67553$."
    )
    assert news_highlights.surname_text(text, names) == (
        "Fitzharding and Bidwell; Xu (ry-xu); "
        "Chaoweeraprasit (itsnaka); Alice Smith and Bob Smith; "
        "PingYou Ltd, Guzhou0806; Oscar Fitzhardington; "
        "https://example.org/Oscar%20Fitzharding; $s(17) = 4.67553$."
    )

    candidate = _candidate(overview.results[0], "T-999", "2026-10-14")
    candidate.record["headline"] = "John Bidwell and `John Bidwell`"
    linked_name = '[John Bidwell](<https://example.org/John Bidwell> "John Bidwell")'
    candidate.record["claim"] = (
        "John Bidwell; " + linked_name + r"; `John Bidwell`; $\text{John Bidwell}$."
    )
    candidate.credit = "Bidwell after Levy"
    before = copy.deepcopy(candidate)
    rendered = news_highlights.render(replace(overview, results=[candidate]))
    assert "<h3>Bidwell and <code>John Bidwell</code></h3>" in rendered
    assert (
        '<a href="https://example.org/John%20Bidwell" title="John Bidwell">Bidwell</a>'
        in rendered
    )
    assert rendered.count("<code>John Bidwell</code>") == 2
    assert overview_sections.credit_cell(candidate.credit) in rendered
    assert [formula.source for formula in site_math.formula_sources(rendered)] == [
        r"\text{John Bidwell}"
    ]
    assert candidate == before
