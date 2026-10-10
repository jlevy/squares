"""Declared paper editions govern links without changing shared front matter."""

import pytest

from devtools import paper_front, render_overview


def test_front_formats_follow_the_declared_pdf_capability() -> None:
    front = paper_front.PaperFront(
        slug="report",
        title="Report",
        oversight=(paper_front.Person("Editor", "https://example.test"),),
        agents=("Agent",),
        version="Draft v1",
        dates=(paper_front.Dated(paper_front.REVISED, "October 9, 2026"),),
    )
    assert [chip[0] for chip in paper_front.chips(front)] == ["MD", "PDF", "GITHUB"]
    web = front._replace(has_pdf=False)
    assert paper_front.check(web) == web
    assert [chip[0] for chip in paper_front.chips(web)] == ["MD", "GITHUB"]
    assert ".pdf" not in paper_front.front_matter(web)
    assert paper_front.hero(front) == paper_front.hero(web)
    assert [record.slug for record in render_overview.PAPERS if not record.has_pdf] == [
        render_overview.EXACT_SIDE_VALUES
    ]


def test_pdf_capability_requires_an_explicit_boolean() -> None:
    front = paper_front.PaperFront(
        slug="report",
        title="Report",
        oversight=(paper_front.Person("Editor", "https://example.test"),),
        agents=("Agent",),
        version="Draft v1",
        dates=(paper_front.Dated(paper_front.REVISED, "October 9, 2026"),),
    )
    with pytest.raises(ValueError, match="boolean"):
        paper_front.check(front._replace(has_pdf="no"))
