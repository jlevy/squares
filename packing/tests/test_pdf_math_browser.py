"""Real PDF math controls, run by Pages with SQPACK_PDF_MATH_BROWSER=1.

These tests consume the prepared publication page and pinned Chromium. Python-only
jobs skip them; the dedicated Pages invocation requires both inputs and fails if
either is absent. Faults change one rendered FontFace, leaving the actual KPress
runtime, host fallback, export waits, and final DOM guard in use.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Literal

import pytest
from playwright.sync_api import Browser, Error, Page, sync_playwright

from devtools import render_explainer_pdf as pdf
from devtools.render_explainer_pdf import _MATH_RENDERED  # pyright: ignore[reportPrivateUsage]

pytestmark = pytest.mark.skipif(
    os.environ.get("SQPACK_PDF_MATH_BROWSER") != "1",
    reason="the dedicated Pages PDF math browser controls set SQPACK_PDF_MATH_BROWSER=1",
)


#: The error is a real invalid FontFace response. The timeout holds the matching
#: FontFaceSet request beyond KPress's own deadline, rather than replacing its render
#: promise with a synthetic rejection. Only one printed formula is affected.
FONT_FAULT = r"""(() => {
  const wrapper = %s;
  const mode = %s;
  const family = 'PDF Math Fault Control';
  let selected;
  document.fonts.add(new FontFace(family, 'url(data:font/woff2;base64,AA==)'));
  if (mode === 'timeout') {
    const fontSet = Object.getPrototypeOf(document.fonts), load = fontSet.load;
    fontSet.load = function(spec, text) {
      if (spec.includes(family)) return new Promise(() => {});
      return load.call(this, spec, text);
    };
  }
  Object.defineProperty(globalThis, 'kpressMathText', {
    configurable: true,
    set(api) {
      for (const key of ['render', 'hydrate']) {
        const original = api[key];
        api[key] = function(source, node, ...args) {
          const owner = node.closest(wrapper === 'tex' ? '.tex' : '.kpress-math');
          const wanted = wrapper === 'native'
            || (owner?.closest('figcaption') && source.includes('\\'));
          if (owner?.getClientRects().length && wanted && !selected) {
            selected = owner;
            selected.dataset.pdfMathFault = wrapper;
            globalThis.pdfMathFaultSource = source;
            const style = document.createElement('style');
            style.textContent = '[data-pdf-math-fault] .katex-html * '
              + '{ font-family: "PDF Math Fault Control" !important; }';
            document.head.appendChild(style);
          }
          return original.call(this, source, node, ...args);
        };
      }
      delete globalThis.kpressMathText;
      globalThis.kpressMathText = api;
    }
  });
})();"""


FAULT_STATE = r"""() => {
  const target = document.querySelector('[data-pdf-math-fault]');
  const semantic = target?.querySelector('.kpress-math-semantic math');
  const render = target?.querySelector('.kpress-math-render');
  const visible = node => !!node
    && node.checkVisibility({opacityProperty: true, visibilityProperty: true})
    && !!node.getClientRects().length;
  return {
    target_found: !!target,
    source: globalThis.pdfMathFaultSource,
    math_ready: document.documentElement.classList.contains('math-ready'),
    host_ready: (render || target)?.dataset.squaresMathReady,
    visible: visible(target),
    semantic_visible: visible(semantic),
    raw_box_visible: visible(render),
    visible_text: target?.innerText,
    raw_text: target?.textContent,
    katex_count: target?.querySelectorAll('.katex').length,
    waits: (globalThis.kpressMathFaceWait || [])
      .filter(entry => entry.request.includes('PDF Math Fault Control'))
      .map(entry => entry.outcome)
  };
}"""


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
            page.add_init_script(script=FONT_FAULT % (json.dumps(wrapper), json.dumps(mode)))
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
            page.evaluate(_MATH_RENDERED)
            page.evaluate("""() => {
              const printed = selector => [...document.querySelectorAll(selector)]
                .find(node => node.getClientRects().length
                  && node.querySelector('.katex-html'));
              const fixture = document.createElement('div');
              fixture.id = 'pdf-math-guard-control';
              document.querySelector('.cert-page').appendChild(fixture);
              globalThis.pdfMathGuardNodes = {
                tex: printed('.tex').cloneNode(true),
                native: printed('.kpress-math').cloneNode(true)
              };
              globalThis.resetPdfMathGuardNode = kind => {
                fixture.replaceChildren(globalThis.pdfMathGuardNodes[kind].cloneNode(true));
                return fixture.firstElementChild;
              };
            }""")

            # A dormant prepared profile may retain raw source. Its visible sibling
            # supplies the printed formula; clipped semantic copies elsewhere on the
            # real page remain beside their successfully rendered KaTeX too.
            assert page.evaluate(r"""() => {
              const host = resetPdfMathGuardNode('tex');
              const alternative = document.createElement('span');
              alternative.className = 'squares-math-variant';
              alternative.dataset.squaresMathContexts = 'system-sans';
              alternative.textContent = '\\frac{1}{2}';
              host.appendChild(alternative);
              return alternative.getClientRects().length === 0;
            }""")
            page.evaluate(_MATH_RENDERED)

            faults = [
                """() => {
                  const host = resetPdfMathGuardNode('tex');
                  host.dataset.squaresMathQueued = 'true';
                  return host.getClientRects().length > 0;
                }""",
                """() => {
                  const host = resetPdfMathGuardNode('tex');
                  const error = document.createElement('span');
                  error.className = 'katex-error';
                  error.textContent = 'unparsed formula';
                  host.appendChild(error);
                  return error.checkVisibility();
                }""",
                """() => {
                  const host = resetPdfMathGuardNode('native');
                  delete host.dataset.kpressMathRendered;
                  const semantic = host.querySelector('.kpress-math-semantic');
                  semantic.style.cssText = 'clip:rect(0px,0px,0px,0px); '
                    + 'clip-path:inset(50%); width:1px; height:1px; '
                    + 'overflow:hidden; position:absolute';
                  return !!semantic.querySelector('math');
                }""",
                """() => {
                  const host = resetPdfMathGuardNode('native');
                  delete host.dataset.kpressMathRendered;
                  const math = host.querySelector('.kpress-math-semantic math');
                  math.innerHTML = '<merror><mtext>unparsed formula</mtext></merror>';
                  return math.checkVisibility();
                }""",
                r"""() => {
                  const host = resetPdfMathGuardNode('tex');
                  host.className = '';
                  host.dataset.squaresMathReady = 'true';
                  host.textContent = '\\frac{1}{2}';
                  return host.checkVisibility();
                }""",
            ]
            for fault in faults:
                assert page.evaluate(fault), "the intended fault must be present in the DOM"
                with pytest.raises(Error, match="unrendered math"):
                    page.evaluate(_MATH_RENDERED)
        finally:
            browser.close()
