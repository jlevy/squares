"""Real PDF math controls, run by Pages with SQPACK_PDF_MATH_BROWSER=1.

These tests consume the prepared publication page and pinned Chromium. Python-only
jobs skip them; the dedicated Pages invocation requires both inputs and fails if
either is absent. Faults change one rendered FontFace, leaving the actual KPress
runtime, host fallback, export waits, and final DOM guard in use.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import pytest
from playwright.sync_api import Browser, Error, Page, sync_playwright

from devtools import render_explainer_pdf as pdf
from devtools.check_math_loading import MATH_LIBRARY
from devtools.render_explainer_pdf import _MATH_RENDERED  # pyright: ignore[reportPrivateUsage]
from sqpack.probes import applied, probe

pytestmark = pytest.mark.skipif(
    os.environ.get("SQPACK_PDF_MATH_BROWSER") != "1",
    reason="the dedicated Pages PDF math browser controls set SQPACK_PDF_MATH_BROWSER=1",
)


#: The probes this module hands the page, one file each under `probes/pdf_math_browser/`.
PROBES = Path(__file__).resolve().parent / "probes"

#: Breaks the math font of exactly one printed formula, as an init script taking the
#: wrapper and the failure mode (`font_fault.js`).
FONT_FAULT = probe(PROBES, "pdf_math_browser/font_fault")

#: The faulted formula as the exporter left it.
FAULT_STATE = probe(PROBES, "pdf_math_browser/fault_state")


@dataclass
class Observation:
    """State immediately before production closes its page, including refusals."""

    state: dict[str, Any] = field(default_factory=dict)
    draws: int = 0


def observe_export(
    monkeypatch: pytest.MonkeyPatch,
    *,
    wrapper: Literal["tex", "native"] | None = None,
    mode: Literal["error", "timeout"] | None = None,
) -> Observation:
    """Inject only the font fault and observe the exporter's unmodified control flow."""
    assert pdf.PAGE.is_file(), "Pages must provide its prepared site/index.html"
    observed = Observation()
    opened: list[Page] = []
    new_page = Browser.new_page
    close = Browser.close
    draw = Page.pdf

    def observed_new_page(browser: Browser, **kwargs: Any) -> Page:
        page = new_page(browser, **kwargs)
        if wrapper is not None:
            page.add_init_script(script=applied(FONT_FAULT, {"wrapper": wrapper, "mode": mode}))
        opened.append(page)
        return page

    def observed_draw(page: Page, **kwargs: Any) -> bytes:
        observed.draws += 1
        return draw(page, **kwargs)

    def observed_close(browser: Browser, **kwargs: Any) -> None:
        try:
            if opened:
                observed.state = opened[-1].evaluate(FAULT_STATE)
        finally:
            close(browser, **kwargs)

    monkeypatch.setattr(Browser, "new_page", observed_new_page)
    monkeypatch.setattr(Page, "pdf", observed_draw)
    monkeypatch.setattr(Browser, "close", observed_close)
    return observed


def test_production_pdf_accepts_typeset_math(monkeypatch: pytest.MonkeyPatch) -> None:
    observed = observe_export(monkeypatch)
    document = pdf.render_pdf_bytes()
    assert document.startswith(b"%PDF-")
    assert observed.draws == 1
    assert observed.state["math_ready"] is True
    assert pdf.font_findings(document) == []


@pytest.mark.parametrize("mode", ["error", "timeout"])
def test_production_pdf_refuses_raw_tex_after_font_failure(
    monkeypatch: pytest.MonkeyPatch, mode: Literal["error", "timeout"]
) -> None:
    observed = observe_export(monkeypatch, wrapper="tex", mode=mode)
    with pytest.raises(Error, match="unrendered math"):
        pdf.render_pdf_bytes()
    assert observed.draws == 0, "refuse source text before drawing publishable PDF bytes"
    state = observed.state
    assert state["target_found"] is True
    assert state["math_ready"] is True
    assert state["host_ready"] == "true", "finished fallback is not typeset math"
    assert state["visible"] is True
    assert "\\" in state["source"]
    assert state["visible_text"] == state["source"]
    assert state["katex_count"] == 0
    assert state["waits"]
    assert set(state["waits"]) == {"error" if mode == "error" else "pending"}


@pytest.mark.parametrize("mode", ["error", "timeout"])
def test_production_pdf_preserves_readable_native_mathml_fallback(
    monkeypatch: pytest.MonkeyPatch, mode: Literal["error", "timeout"]
) -> None:
    observed = observe_export(monkeypatch, wrapper="native", mode=mode)
    document = pdf.render_pdf_bytes()
    assert document.startswith(b"%PDF-")
    assert observed.draws == 1
    state = observed.state
    assert state["target_found"] is True
    assert state["math_ready"] is True
    assert state["host_ready"] == "true"
    assert state["semantic_visible"] is True
    assert state["raw_box_visible"] is False
    assert state["visible_text"].strip()
    assert "\\" not in state["visible_text"]
    assert state["katex_count"] == 0
    assert state["waits"]
    assert set(state["waits"]) == {"error" if mode == "error" else "pending"}
    # Native MathML is readable here. The independent PDF font policy can still
    # refuse a host's fallback face; this control does not broaden that allowlist.


def test_final_math_guard_distinguishes_hidden_alternatives_and_render_errors() -> None:
    """Exercise the final predicate with real prepared nodes and the page's CSS."""
    assert pdf.PAGE.is_file(), "Pages must provide its prepared site/index.html"
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(pdf.BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            page.emulate_media(media="print", reduced_motion="reduce")
            page.goto(pdf.PAGE.as_uri(), wait_until="load")
            page.wait_for_selector(pdf.READY, timeout=60_000)
            page.evaluate(pdf.SETTLED)
            math = {"math": page.evaluate_handle(MATH_LIBRARY)}
            page.evaluate(_MATH_RENDERED, math)
            page.evaluate(probe(PROBES, "pdf_math_browser/guard_fixture"))

            # A dormant prepared profile may retain raw source. Its visible sibling
            # supplies the printed formula; clipped semantic copies elsewhere on the
            # real page remain beside their successfully rendered KaTeX too.
            assert page.evaluate(probe(PROBES, "pdf_math_browser/hidden_alternative"))
            page.evaluate(_MATH_RENDERED, math)

            faults = [
                probe(PROBES, "pdf_math_browser/fault_queued"),
                probe(PROBES, "pdf_math_browser/fault_katex_error"),
                probe(PROBES, "pdf_math_browser/fault_clipped_native"),
                probe(PROBES, "pdf_math_browser/fault_merror"),
                probe(PROBES, "pdf_math_browser/fault_raw_tex"),
            ]
            for fault in faults:
                assert page.evaluate(fault), "the intended fault must be present in the DOM"
                with pytest.raises(Error, match="unrendered math"):
                    page.evaluate(_MATH_RENDERED, math)
        finally:
            browser.close()
