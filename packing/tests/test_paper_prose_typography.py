"""Generated paper histories use Flowmark where the Markdown hook cannot reach them."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from yaml import safe_load

from devtools import (
    render_n11_lower_bounds_explainer,
    render_n11_optimality_review,
    render_n11_threshold_bound_review,
    render_packing_methods,
)
from sqpack.release import PublicationHistoryEntry

REPO = Path(__file__).resolve().parents[2]
HISTORY = (
    PublicationHistoryEntry(
        version="v1.2.3",
        first_published="October 10, 2026",
        result_scope=(
            "Compare Couzo's \"basin hopping\" with Xu's exact certificates... "
            "Keep `Xu's \"raw\"`, $x'$, and $s(11) > 31/8$ at 2.4142135623730951; "
            "[source](https://example.invalid/Couzo's) stays linked. "
            '<span title="Xu\'s raw">Attribute</span>.'
        ),
    ),
    PublicationHistoryEntry(
        version="v1.2.2",
        first_published="October 9, 2026",
        result_scope='Record Daniel\'s "contact solver" result.',
    ),
)
EXPECTED = (
    "- **v1.2.3 — October 10, 2026.** "
    "Compare Couzo\u2019s \u201cbasin hopping\u201d with Xu\u2019s exact certificates \u2026 "
    "Keep `Xu's \"raw\"`, $x'$, and $s(11) > 31/8$ at 2.4142135623730951; "
    "[source](https://example.invalid/Couzo's) stays linked. "
    '<span title="Xu\'s raw">Attribute</span>. '
    "- **v1.2.2 — October 9, 2026.** "
    "Record Daniel\u2019s \u201ccontact solver\u201d result."
)


def test_every_paper_formats_generated_history_and_preserves_protected_syntax(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for renderer, attribute in (
        (render_n11_lower_bounds_explainer, "EXPLAINER_HISTORY"),
        (render_n11_optimality_review, "OPTIMALITY_REVIEW_HISTORY"),
        (render_n11_threshold_bound_review, "THRESHOLD_REVIEW_HISTORY"),
        (render_packing_methods, "PACKING_METHODS_HISTORY"),
    ):
        monkeypatch.setattr(renderer, attribute, HISTORY)
        history = renderer.version_history_markdown()
        assert " ".join(history.split()) == EXPECTED
        for protected in (
            '`Xu\'s "raw"`',
            "$x'$",
            "$s(11) > 31/8$",
            "2.4142135623730951",
            "[source](https://example.invalid/Couzo's)",
            '<span title="Xu\'s raw">Attribute</span>',
        ):
            assert protected in history
        assert renderer.version_history_markdown() == history


def test_standard_markdown_hook_runs_pinned_auto_formatting_and_stages_fixes() -> None:
    hook = safe_load((REPO / "lefthook.yml").read_text(encoding="utf-8"))["pre-commit"]
    markdown = hook["commands"]["format-markdown"]
    assert hook["parallel"] is False
    assert markdown["glob"] == "*.{md,markdown,mdc,py}"
    assert markdown["run"] == "make format paper-style-check"
    assert markdown["stage_fixed"] is True
    makefile = (REPO / "Makefile").read_text(encoding="utf-8")
    assert "FLOWMARK := uvx --from flowmark-rs==0.4.0 flowmark\n" in makefile
    assert re.search(r"(?m)^format:\n\t\$\(FLOWMARK\) --auto \.\n", makefile)
