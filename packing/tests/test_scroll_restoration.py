"""Fail-closed verdict checks for the real HTTP reload probe."""

from __future__ import annotations

from copy import deepcopy

import pytest

from devtools.check_scroll_restoration import Position, ReloadReport, findings


@pytest.fixture
def restored() -> ReloadReport:
    before: Position = {
        "top": 3000.0,
        "document_top": 3000.0,
        "native": True,
        "restoration": "auto",
        "hash": "#381-100",
    }
    return {
        "browser": "chromium",
        "browser_version": "test",
        "javascript": True,
        "width": 1280,
        "before": before,
        "after": before.copy(),
        "navigation_type": "reload",
        "findings": [],
    }


def test_native_reload_preserves_fractional_reading_position(restored: ReloadReport) -> None:
    restored["after"]["top"] += 0.5
    assert findings(restored) == []


def test_a_page_that_never_scrolled_cannot_pass(restored: ReloadReport) -> None:
    restored["before"]["top"] = restored["after"]["top"] = 0
    assert any("meaningful reading position" in item for item in findings(restored))


def test_reload_reset_and_fragment_loss_are_both_reported(restored: ReloadReport) -> None:
    restored["after"]["top"] = 0
    restored["after"]["hash"] = ""
    assert len(findings(restored)) == 2


def test_non_reload_and_pane_controls_are_rejected(restored: ReloadReport) -> None:
    wrong_navigation = deepcopy(restored)
    wrong_navigation["navigation_type"] = "navigate"
    assert any("browser reload" in item for item in findings(wrong_navigation))
    restored["before"]["native"] = False
    assert any("document scroller" in item for item in findings(restored))
