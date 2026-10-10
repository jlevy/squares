"""Fixture subsets keep exactly the canonical case pages the full publisher serves."""

from __future__ import annotations

import pytest

from devtools import render_case_pages, site_math
from tests import site_renders


def test_selected_case_pages_are_byte_identical_to_the_complete_publication() -> None:
    complete = site_renders.case_records()
    assert len(complete) == 324
    selected = site_renders.case_records((291, 53, 53))
    assert list(selected) == ["cases/53.html", "cases/291.html"]
    assert selected is site_renders.case_records((53, 291))
    assert selected == {name: complete[name] for name in selected}


@pytest.mark.parametrize("only", [(), (0,), (1000,)])
def test_invalid_requested_case_counts_are_refused(only: tuple[int, ...]) -> None:
    with pytest.raises(ValueError, match=r"case subset must request|unknown case counts:"):
        render_case_pages.case_records(only=only)


@pytest.mark.parametrize("only", [None, (53, 291)])
def test_required_case_missing_after_math_preparation_is_refused(
    monkeypatch: pytest.MonkeyPatch, only: tuple[int, ...] | None
) -> None:
    monkeypatch.setattr(render_case_pages, "_rendered", lambda: "")
    monkeypatch.setattr(render_case_pages, "_records", lambda _: {53: "first", 291: "second"})
    monkeypatch.setattr(
        site_math,
        "prepare",
        lambda _: "<!-- static-case 291 -->second<!-- /static-case -->",
    )
    monkeypatch.setattr(render_case_pages.frontier, "frontier_cases", lambda: [{"n": 53}])
    monkeypatch.setattr(render_case_pages, "_description", lambda _: "")
    with pytest.raises(KeyError, match="53"):
        render_case_pages.case_records(only=only)
