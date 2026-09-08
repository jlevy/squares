"""Observe visible math during startup, including deliberately delayed font loads.

The probe samples animation frames, so hidden staging nodes do not count as a paint.
Its controlled run holds successful font-load completions, triggers the page's input
and resize handlers, then releases them. This catches callbacks that bypass startup
readiness and semantic MathML that flashes before KaTeX replaces it. The prepared
geometry checker separately holds real font requests to test delayed decoding.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal, TypedDict

from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY, SETTLED


class EarlyTarget(TypedDict):
    """A requested slider value, captured before any event can reset the controls."""

    id: str
    value: str


class Readout(TypedDict):
    """A rendered and accessible response to one frozen early-input target."""

    id: str
    expected_value: str
    actual_value: str | None
    expected_source: str
    source: str
    sans: bool
    state_matches: bool
    supported: bool


class LoadingReport(TypedDict):
    """Observed startup state and failures of the visual loading contract."""

    held_loads: int
    sliders: int
    early_targets: list[EarlyTarget]
    frames: int
    math_font_checks: int
    first_paint: dict[str, object] | None
    unready_math: list[str]
    early_math: str | None
    fallback: str | None
    readouts: list[str]
    no_javascript: dict[str, int]
    findings: list[str]


#: Keep font loading pending long enough for several paints and an initial ResizeObserver
#: delivery, while remaining well below the runtime's failure-recovery timeout.
OBSERVATION_MS = 200

#: checkVisibility ignores clipping. Intersect the element's box with ancestor overflow,
#: legacy clip rectangles, and inset clip paths before calling semantic fallback visible.
#: Unrecognised clip shapes are not evidence of readable fallback.
EXPOSED = r"""node => {
  if (!node.checkVisibility({ opacityProperty: true, visibilityProperty: true })) {
    return false;
  }
  const rect = node.getBoundingClientRect();
  let {left, right, top, bottom} = rect;
  const intersect = box => {
    left = Math.max(left, box.left); right = Math.min(right, box.right);
    top = Math.max(top, box.top); bottom = Math.min(bottom, box.bottom);
  };
  for (let parent = node; parent; parent = parent.parentElement) {
    const style = getComputedStyle(parent), box = parent.getBoundingClientRect();
    // The probe covers the document, including content a reader can scroll into view.
    // Project that content into its scroll viewport before checking outer clipping.
    if (/^(auto|scroll)$/.test(style.overflowX) && parent.scrollWidth > parent.clientWidth) {
      const width = right - left;
      left = box.left; right = Math.min(box.right, left + width);
    }
    if (/^(auto|scroll)$/.test(style.overflowY) && parent.scrollHeight > parent.clientHeight) {
      const height = bottom - top;
      top = box.top; bottom = Math.min(box.bottom, top + height);
    }
    if (/^(hidden|clip)$/.test(style.overflowX)) {
      left = Math.max(left, box.left); right = Math.min(right, box.right);
    }
    if (/^(hidden|clip)$/.test(style.overflowY)) {
      top = Math.max(top, box.top); bottom = Math.min(bottom, box.bottom);
    }
    const clip = (style.clip || 'auto').match(/^rect\(([^)]+)\)$/);
    if (clip) {
      const defaults = [0, box.width, box.height, 0];
      const edges = clip[1].trim().split(/[,\s]+/).map((value, i) =>
        value === 'auto' ? defaults[i] : parseFloat(value));
      if (edges.length !== 4 || !edges.every(Number.isFinite)) return false;
      intersect({left: box.left + edges[3], right: box.left + edges[1],
        top: box.top + edges[0], bottom: box.top + edges[2]});
    }
    const path = style.clipPath || 'none';
    if (path !== 'none') {
      const inset = path.match(/^inset\(([^)]+)\)$/);
      if (!inset) return false;
      const values = inset[1].split(/\s+round\s+/)[0].trim().split(/\s+/);
      if (values.length < 1 || values.length > 4) return false;
      const edges = [values[0], values[1] || values[0],
        values[2] || values[0], values[3] || values[1] || values[0]];
      const pixels = edges.map((value, i) => parseFloat(value) *
        (value.endsWith('%') ? (i % 2 ? box.width : box.height) / 100 : 1));
      if (!pixels.every(Number.isFinite)) return false;
      intersect({left: box.left + pixels[3], right: box.right - pixels[1],
        top: box.top + pixels[0], bottom: box.bottom - pixels[2]});
    }
    if (right - left <= 1 || bottom - top <= 1) return false;
  }
  return right - left > 1 && bottom - top > 1;
}"""

#: Describe actual glyph runs, including hidden staging. Query each CSS family
#: separately: WebKit can report a family list ready while a later face is pending.
#: Native load matching, rather than a second CSS matching engine, handles weights,
#: unicode ranges, and families excluded from the glyph run.
REQUIRED_FONTS = r"""(math, observe) => {
  const html = math.querySelector('.katex-html');
  if (!html) return [];
  const walker = document.createTreeWalker(html, NodeFilter.SHOW_TEXT);
  const groups = new Map();
  while (walker.nextNode()) {
    const node = walker.currentNode, text = node.textContent;
    if (!text.trim()) continue;
    const style = getComputedStyle(node.parentElement);
    for (const family of families(style.fontFamily)) {
      const spec = `${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${family}`;
      if (!groups.has(spec)) groups.set(spec, new Set());
      for (const character of text) groups.get(spec).add(character);
    }
  }
  return [...groups].map(([spec, characters]) => {
    const text = [...characters].join('');
    try { return {spec, text, ...observe(spec, text)}; }
    catch (error) {
      return {spec, text, ready: false, outcome: 'rejected', faces: [], error: String(error)};
    }
  });

  function families(list) {
    const parts = [];
    let start = 0, quote = '', escaped = false;
    for (let index = 0; index < list.length; index++) {
      const character = list[index];
      if (escaped) escaped = false;
      else if (character === '\\') escaped = true;
      else if (quote) { if (character === quote) quote = ''; }
      else if (character === '"' || character === "'") quote = character;
      else if (character === ',') {
        parts.push(list.slice(start, index).trim()); start = index + 1;
      }
    }
    parts.push(list.slice(start).trim());
    return parts.filter(Boolean);
  }
}"""

#: A readiness oracle separate from the renderer's cache. In WebKit, even a
#: single-family check() can return true while load() remains pending. Discovering
#: staged glyphs before rAF lets already-ready promises settle before first exposure;
#: a previously unseen visible closure must fail instead of passing vacuously.
FONT_LOAD_OBSERVER = r"""load => {
  const requests = new Map();
  return (spec, text) => {
    const key = JSON.stringify([spec, text]);
    if (!requests.has(key)) {
      const record = {outcome: 'pending', faces: []};
      requests.set(key, record);
      try {
        Promise.resolve(load(spec, text)).then(faces => {
          record.outcome = 'resolved';
          record.faces = [...faces];
        }, error => {
          record.outcome = 'rejected'; record.error = String(error);
        });
      } catch (error) {
        record.outcome = 'rejected'; record.error = String(error);
      }
    }
    const record = requests.get(key);
    const faces = record.faces.map(face => ({family: face.family, style: face.style,
      weight: face.weight, unicodeRange: face.unicodeRange, status: face.status}));
    return {outcome: record.outcome, faces, ...(record.error ? {error: record.error} : {}),
      ready: record.outcome === 'resolved' && faces.every(face => face.status === 'loaded')};
  };
}"""

FIRST_PAINT_SCRIPT = (
    r"""
(() => {
  globalThis.__mathFirstPaint = null;
  const state = globalThis.__mathLoadingState = {
    frames: 0, mathFontChecks: 0, unreadyMath: [], earlyMath: null,
    fallback: null, stop: false
  };
  const exposed = __EXPOSED__;
  const requiredFonts = __REQUIRED_FONTS__;
  const observe = (__FONT_LOAD_OBSERVER__)((...args) =>
    globalThis.__mathLoadControl?.nativeLoad
      ? globalThis.__mathLoadControl.nativeLoad(...args) : document.fonts.load(...args));
  const discover = () => {
    if (state.stop) return;
    for (const math of document.querySelectorAll('.katex')) requiredFonts(math, observe);
  };
  const mutations = new MutationObserver(discover);
  mutations.observe(document, {subtree: true, childList: true, characterData: true,
    attributes: true, attributeFilter: ['class', 'style', 'hidden',
      'data-kpress-math-face', 'data-kpress-math-prepared', 'data-squares-math-ready']});
  discover();
  const observed = new WeakSet();
  const label = (node) => node.textContent.trim().replace(/\s+/g, ' ').slice(0, 100);
  const sample = () => {
    state.frames++;
    const maths = [...document.querySelectorAll('.katex')].filter(exposed);
    for (const math of maths) {
      if (observed.has(math)) continue;
      observed.add(math);
      const required = requiredFonts(math, observe);
      state.mathFontChecks += required.length;
      const late = required.filter(face => !face.ready);
      if (!required.length) state.unreadyMath.push(label(math) + ': no observed glyph closure');
      if (late.length) state.unreadyMath.push(label(math) + ': '
        + late.map(face => `${face.spec} [${face.text}] (${face.outcome || 'error'}; `
          + face.faces.map(match => `${match.family}: ${match.status}`).join(', ')
          + (face.error ? `; ${face.error}` : '') + ')').join(', '));
      if (!globalThis.__mathFirstPaint) {
        const faces = [...document.fonts].map(face => ({
          family: face.family, style: face.style, weight: face.weight,
          unicodeRange: face.unicodeRange, status: face.status
        }));
        globalThis.__mathFirstPaint = { at: performance.now(), faces, required };
      }
    }
    const control = globalThis.__mathLoadControl;
    if (maths.length && control && !control.released && !state.earlyMath) {
      state.earlyMath = label(maths[0]);
    }
    const fallback = [...document.querySelectorAll('.kpress-math-semantic')].find(exposed);
    if (fallback && !state.fallback) state.fallback = label(fallback);
    if (!state.stop) requestAnimationFrame(sample);
    else mutations.disconnect();
  };
  requestAnimationFrame(sample);
})();
""".replace("__EXPOSED__", EXPOSED)
    .replace("__REQUIRED_FONTS__", REQUIRED_FONTS)
    .replace("__FONT_LOAD_OBSERVER__", FONT_LOAD_OBSERVER)
)

#: Gate successful loads only when CSS actually matches a declared face. Empty
#: unicode-range/system-family results remain immediate. CSS and the independent
#: oracle can decode fonts normally; this tests the explicit readiness contract.
#: prepare_explainer_math.check_geometry separately holds real font requests.
HOLD_FONTS_SCRIPT = r"""
(() => {
  let release;
  const gate = new Promise(resolve => { release = resolve; });
  const control = globalThis.__mathLoadControl = {
    heldLoads: 0, released: false,
    release() { this.released = true; release(); }
  };
  const fontSet = Object.getPrototypeOf(document.fonts), loadSet = fontSet.load;
  control.nativeLoad = loadSet.bind(document.fonts);
  // Some pinned Chromium versions have no global FontFaceSet constructor.
  fontSet.load = function(...args) {
    const promise = loadSet.apply(this, args);
    if (control.released) return promise;
    return promise.then(faces => {
      if (!faces.length) return faces;
      control.heldLoads++;
      return gate.then(() => faces);
    });
  };
  const loadFace = FontFace.prototype.load;
  FontFace.prototype.load = function(...args) {
    if (control.released) return loadFace.apply(this, args);
    control.heldLoads++;
    return gate.then(() => loadFace.apply(this, args));
  };
})();
"""

EARLY_EVENTS = r"""() => {
  const sliders = [...document.querySelectorAll('input[type="range"]')];
  const targets = sliders.map((slider, index) => {
    const min = Number(slider.min || 0), max = Number(slider.max || 100);
    const step = Number(slider.step) || 1;
    const steps = Math.floor((max - min) / step);
    let value = min + step * ((index + 1) % (steps + 1));
    if (value === Number(slider.value)) value = value === max ? min : max;
    if (value === Number(slider.value)) throw new Error(`No distinct target for ${slider.id}`);
    return Object.freeze({id: slider.id, value: String(value)});
  });
  Object.freeze(targets);
  for (const [index, slider] of sliders.entries()) {
    const target = targets[index];
    slider.value = target.value === slider.max ? slider.min : slider.max;
    slider.dispatchEvent(new Event('input', { bubbles: true }));
    slider.value = target.value;
    slider.dispatchEvent(new Event('input', { bubbles: true }));
  }
  window.dispatchEvent(new Event('resize'));
  window.dispatchEvent(new Event('beforeprint'));
  window.dispatchEvent(new Event('afterprint'));
  // Playwright retains this snapshot outside the page, independently of boot resets.
  return targets;
}"""

READOUTS = r"""targets => targets.map(target => {
  const slider = document.getElementById(target.id);
  const angle = target.id.startsWith('phi-');
  const direction = target.id.startsWith('kslider-');
  const output = document.getElementById(angle ? 's-' + target.id
    : target.id.replace(/^kslider-/, 'kval-'));
  const annotation = output?.querySelector('annotation[encoding="application/x-tex"]');
  const math = angle ? (output ? [output] : []) : [...(output?.children || [])];
  return {
    id: target.id, expected_value: target.value, actual_value: slider?.value ?? null,
    expected_source: angle ? (Number(target.value) / 10).toFixed(3) + '^{\\circ}'
      : `k = ${target.value}`,
    source: annotation?.textContent || '',
    sans: math.length > 0 && math.every(node => node.dataset.kpressMathFace === 'sans'),
    state_matches: !direction || (slider?.getAttribute('aria-valuetext') || '')
      .startsWith(`Direction ${target.value} of `),
    supported: angle || direction
  };
})"""

NO_JAVASCRIPT = r"""() => {
  const exposed = __EXPOSED__;
  const visible = selector => [...document.querySelectorAll(selector)].filter(exposed).length;
  const wrappers = '.kpress-math,.tex,.tex-d,[data-kpress-math-prepared="true"]';
  const raw = node => node.matches('.tex,.tex-d') && !node.querySelector('.katex')
    && !!node.textContent.trim() && exposed(node);
  const prepared = node => [...node.querySelectorAll('.katex-html')]
    .some(html => html.textContent.trim() && exposed(html));
  const native = node => [...node.querySelectorAll('.kpress-math-semantic')].some(exposed);
  const targets = [...document.querySelectorAll(wrappers)].filter(node => {
    // Judge every intended formula in readable surrounding content. Filtering on
    // the formula's own box would silently discard clipped or empty fallbacks.
    return !node.parentElement.closest(wrappers) && exposed(node.parentElement);
  });
  return {
    raw_tex: targets.filter(raw).length,
    native_math: visible('.kpress-math-semantic'),
    prepared_math: visible('.katex-html'),
    math_wrappers: targets.length,
    unreadable_math: targets
      .filter(node => !raw(node) && !prepared(node) && !native(node)).length
  };
}""".replace("__EXPOSED__", EXPOSED)


def loading_findings(report: LoadingReport) -> list[str]:
    """Judge observations independently of the runtime's font-family allowlist."""
    findings: list[str] = []
    if report["held_loads"] == 0:
        findings.append("the delayed-load control intercepted no font loads")
    if report["frames"] == 0:
        findings.append("the loading probe observed no animation frames")
    if report["math_font_checks"] == 0:
        findings.append("the font probe checked no rendered glyphs")
    if report["sliders"] == 0:
        findings.append("the early-input control exercised no sliders")
    if report["early_math"] is not None:
        findings.append(f"math appeared before font readiness: {report['early_math']}")
    if report["fallback"] is not None:
        findings.append(f"native MathML was visible before enhancement: {report['fallback']}")
    paint = report["first_paint"]
    if paint is None:
        findings.append("no visible mathematics was observed after font release")
    else:
        faces = paint.get("faces", [])
        assert isinstance(faces, list)
        math_faces = [
            face
            for face in faces
            if str(face["family"]).strip("\"'").startswith(("KaTeX_", "KPress Math Text"))
        ]
        if not math_faces:
            findings.append("the font probe observed no math font declarations")
        required = paint.get("required", [])
        assert isinstance(required, list)
        if not required:
            findings.append("the first visible formula has no observed glyph closure")
        late = [f"{face['spec']} [{face['text']}]" for face in required if not face["ready"]]
        if late:
            findings.append(
                "math faces were not ready at first visible paint: " + ", ".join(late)
            )
    if report["unready_math"]:
        findings.append(
            "math appeared with unavailable required faces: "
            + "; ".join(report["unready_math"])
        )
    return findings


def no_javascript_findings(fallback: dict[str, int]) -> list[str]:
    """Native MathML, raw TeX, and prepared KaTeX are alternative readable fallbacks."""
    findings: list[str] = []
    if fallback.get("math_wrappers", 0) == 0:
        findings.append("no JavaScript: no mathematical fallback targets")
    if fallback.get("unreadable_math", 0):
        findings.append(
            f"no JavaScript: {fallback['unreadable_math']} formulas have no readable fallback"
        )
    if not any(fallback.get(name, 0) for name in ("raw_tex", "native_math", "prepared_math")):
        findings.append("no JavaScript: no readable math fallback")
    return findings


def readout_findings(readouts: list[Readout]) -> list[str]:
    """Compare eventual output with the requested values, not mutable DOM inputs."""
    findings: list[str] = []
    if not readouts:
        findings.append("no readouts were checked after early input")
    for readout in readouts:
        label = readout["id"]
        if not readout["supported"]:
            findings.append(f"{label}: early-input control has no readout contract")
            continue
        if readout["actual_value"] != readout["expected_value"]:
            findings.append(
                f"{label}: slider value changed after early input: "
                f"{readout['actual_value']!r}, expected {readout['expected_value']!r}"
            )
        if readout["source"] != readout["expected_source"]:
            findings.append(
                f"{label}: stale readout after rapid input: "
                f"{readout['source']!r}, expected {readout['expected_source']!r}"
            )
        if not readout["state_matches"]:
            findings.append(f"{label}: accessible direction state lost the early input")
        if not readout["sans"]:
            findings.append(f"{label}: readout lost sans math")
    return findings


def page_url(path: Path | str) -> str:
    """Preserve a live HTTP URL or resolve a local page for browser navigation."""
    value = str(path)
    return value if value.startswith(("https://", "http://")) else Path(path).resolve().as_uri()


def check_loading(
    path: Path | str = PAGE,
    *,
    width: int = 1280,
    browser_name: Literal["chromium", "firefox", "webkit"] = "chromium",
    artifacts: Path | None = None,
) -> LoadingReport:
    """Load a page with delayed fonts and exercise events before releasing them."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        browser_type = getattr(driver, browser_name)
        override = os.environ.get(BROWSER_OVERRIDE) if browser_name == "chromium" else None
        browser = browser_type.launch(executable_path=override)
        try:
            page = browser.new_page(viewport={"width": width, "height": 720})
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.add_init_script(HOLD_FONTS_SCRIPT)
            page.add_init_script(FIRST_PAINT_SCRIPT)
            url = page_url(path)
            page.goto(url, wait_until="domcontentloaded")
            targets: list[EarlyTarget] = page.evaluate(EARLY_EVENTS)
            page.set_viewport_size({"width": max(1, width - 1), "height": 720})
            page.set_viewport_size({"width": width, "height": 720})
            page.wait_for_timeout(OBSERVATION_MS)
            if artifacts is not None:
                artifacts.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=artifacts / f"{browser_name}-{width}-fonts-held.png")
            page.evaluate("globalThis.__mathLoadControl.release()")
            page.wait_for_selector(READY, timeout=60_000)
            page.evaluate(SETTLED)
            report: LoadingReport = page.evaluate(
                """() => {
                  const state = globalThis.__mathLoadingState;
                  state.stop = true;
                  return {
                    held_loads: globalThis.__mathLoadControl.heldLoads,
                    sliders: 0,
                    early_targets: [],
                    frames: state.frames,
                    math_font_checks: state.mathFontChecks,
                    first_paint: globalThis.__mathFirstPaint,
                    unready_math: state.unreadyMath,
                    early_math: state.earlyMath,
                    fallback: state.fallback,
                    readouts: [],
                    no_javascript: {},
                    findings: []
                  };
                }"""
            )
            report["sliders"] = len(targets)
            report["early_targets"] = targets
            report["findings"] = loading_findings(report)
            readouts: list[Readout] = page.evaluate(READOUTS, targets)
            for readout in readouts:
                report["readouts"].append(f"{readout['id']}: {readout['source']}")
            report["findings"].extend(readout_findings(readouts))
            report["findings"].extend(f"page error: {error}" for error in errors)
            if artifacts is not None:
                page.screenshot(path=artifacts / f"{browser_name}-{width}-settled.png")
                caption = page.locator(".kpress-figcaption").first
                caption.screenshot(path=artifacts / f"{browser_name}-{width}-caption.png")
            fallback_page = browser.new_page(
                java_script_enabled=False, viewport={"width": width, "height": 720}
            )
            try:
                fallback_page.goto(url, wait_until="load")
                fallback = fallback_page.evaluate(NO_JAVASCRIPT)
                report["no_javascript"] = fallback
                report["findings"].extend(no_javascript_findings(fallback))
            finally:
                fallback_page.close()
            return report
        finally:
            browser.close()


#: These mutations retain the real page, fonts, event handlers, and no-JS rendering.
#: Running only dictionary-shaped observations would miss defects in the observer itself.
NEGATIVE_FIXTURES = {
    "early-paint": (
        r"""<script>
document.addEventListener('DOMContentLoaded', () => {
  // A failed face stays unavailable even if decoding finishes before the next
  // sampled frame. This makes the missing-font negative control deterministic.
  document.fonts.add(new FontFace('Math Unready Control', 'url(data:font/woff2;base64,AA==)'));
  const fault = document.createElement('div');
  fault.innerHTML = '<span class="katex" style="visibility:visible!important">' +
    `<span class="katex-html" style='font-family:"Math Unready Control"'>x = 1</span></span>` +
    '<math class="kpress-math-semantic" style="visibility:visible!important">' +
    '<mi>y</mi><mo>=</mo><mn>2</mn></math>';
  document.body.prepend(fault);
});
</script>""",
        (
            "math appeared before font readiness:",
            "native MathML was visible before enhancement:",
            "math faces were not ready at first visible paint:",
        ),
    ),
    "dropped-early-input": (
        r"""<script>
document.addEventListener('input', event => {
  if (!globalThis.__mathLoadControl.released) event.stopImmediatePropagation();
}, true);
</script>""",
        ("stale readout after rapid input:", "slider value changed after early input:"),
    ),
    "unready-later-family": (
        r"""<script>
document.addEventListener('DOMContentLoaded', () => {
  // The first family excludes ≥. A whole-family-list check can overlook the
  // later required face in WebKit; the oracle must observe its actual load.
  document.fonts.add(new FontFace('Math Range First', 'url(data:font/woff2;base64,AA==)',
    {unicodeRange:'U+0041'}));
  document.fonts.add(new FontFace('Math Range Late', 'url(data:font/woff2;base64,AA==)',
    {unicodeRange:'U+2265'}));
  const fault = document.createElement('div');
  fault.innerHTML = '<span class="katex" style="visibility:visible!important">' +
    `<span class="katex-html" style='font-family:"Math Range First","Math Range Late",serif'>` +
    '≥</span></span>';
  document.body.prepend(fault);
});
</script>""",
        ("math appeared with unavailable required faces:", "Math Range Late"),
    ),
    "clipped-no-javascript": (
        """<noscript><style>
.kpress-math-semantic, .katex-html, .tex, .tex-d {
  position:absolute!important; width:1px!important; height:1px!important;
  overflow:hidden!important; clip-path:inset(50%)!important;
}
</style></noscript>""",
        ("formulas have no readable fallback", "no JavaScript: no readable math fallback"),
    ),
}


class ControlReport(TypedDict):
    """Whether a real-browser fault was detected by the ordinary loading guard."""

    name: str
    findings: list[str]
    missing_findings: list[str]


class SelfTestReport(TypedDict):
    """Positive baseline and negative controls for the browser observer."""

    baseline_findings: list[str]
    controls: list[ControlReport]
    findings: list[str]


def self_test(
    path: Path = PAGE,
    *,
    width: int = 1280,
    browser_name: Literal["chromium", "firefox", "webkit"] = "chromium",
) -> SelfTestReport:
    """Prove in a browser that retained faults make the loading guard fail."""
    html = path.read_text(encoding="utf-8")
    if "</head>" not in html:
        raise ValueError("self-test requires the generated HTML page with a closing head tag")
    baseline = check_loading(path, width=width, browser_name=browser_name)
    report: SelfTestReport = {
        "baseline_findings": baseline["findings"],
        "controls": [],
        "findings": [f"positive baseline: {finding}" for finding in baseline["findings"]],
    }
    with TemporaryDirectory(prefix="squares-math-loading-") as temporary:
        for name, (mutation, expected) in NEGATIVE_FIXTURES.items():
            fixture = Path(temporary) / f"{name}.html"
            fixture.write_text(
                html.replace("</head>", mutation + "</head>", 1), encoding="utf-8"
            )
            observed = check_loading(fixture, width=width, browser_name=browser_name)
            missing = [
                phrase
                for phrase in expected
                if not any(phrase in finding for finding in observed["findings"])
            ]
            report["controls"].append(
                {"name": name, "findings": observed["findings"], "missing_findings": missing}
            )
            report["findings"].extend(
                f"{name}: failed to detect {phrase}" for phrase in missing
            )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "page", nargs="?", default=str(PAGE), help="Local HTML or live page URL"
    )
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument(
        "--browser", choices=("chromium", "firefox", "webkit"), default="chromium"
    )
    parser.add_argument(
        "--artifacts", type=Path, help="Save startup and caption screenshots here"
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Check real-browser fault fixtures against a local page",
    )
    args = parser.parse_args(argv)
    if args.width <= 0:
        parser.error("--width must be positive")
    report: LoadingReport | SelfTestReport
    if args.self_test:
        if str(args.page).startswith(("https://", "http://")):
            parser.error("--self-test requires a local generated HTML page")
        report = self_test(Path(args.page), width=args.width, browser_name=args.browser)
    else:
        report = check_loading(
            args.page, width=args.width, browser_name=args.browser, artifacts=args.artifacts
        )
    print(json.dumps(report, indent=2))
    return int(bool(report["findings"]))


if __name__ == "__main__":
    raise SystemExit(main())
