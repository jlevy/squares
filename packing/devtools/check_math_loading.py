"""Observe visible math during startup, including deliberately delayed font loads.

The probe samples animation frames, so hidden staging nodes do not count as a paint.
Its controlled run holds explicit font loads, triggers the page's input and resize
handlers, then releases them. This catches callbacks that bypass startup readiness
and semantic MathML that flashes before KaTeX replaces it.
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
    first_paint: dict[str, object] | None
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

FIRST_PAINT_SCRIPT = r"""
(() => {
  globalThis.__mathFirstPaint = null;
  const state = globalThis.__mathLoadingState = {
    frames: 0, earlyMath: null, fallback: null, stop: false
  };
  const exposed = __EXPOSED__;
  const label = (node) => node.textContent.trim().replace(/\s+/g, ' ').slice(0, 100);
  const sample = () => {
    state.frames++;
    const math = [...document.querySelectorAll('.katex')].find(exposed);
    if (math && !globalThis.__mathFirstPaint) {
      const faces = [...document.fonts].map(face => ({
        family: face.family, style: face.style, weight: face.weight,
        unicodeRange: face.unicodeRange, status: face.status
      }));
      globalThis.__mathFirstPaint = { at: performance.now(), faces };
    }
    const control = globalThis.__mathLoadControl;
    if (math && control && !control.released && !state.earlyMath) {
      state.earlyMath = label(math);
    }
    const fallback = [...document.querySelectorAll('.kpress-math-semantic')].find(exposed);
    if (fallback && !state.fallback) state.fallback = label(fallback);
    if (!state.stop) requestAnimationFrame(sample);
  };
  requestAnimationFrame(sample);
})();
""".replace("__EXPOSED__", EXPOSED)

#: Delay the real load call as well as its promise. CSS may independently request fonts;
#: the invariant tested here is that rendering awaits its explicit readiness work.
HOLD_FONTS_SCRIPT = r"""
(() => {
  let release;
  const gate = new Promise(resolve => { release = resolve; });
  const control = globalThis.__mathLoadControl = {
    heldLoads: 0, released: false,
    release() { this.released = true; release(); }
  };
  // Some pinned Chromium versions have no global FontFaceSet constructor.
  for (const owner of [FontFace.prototype, Object.getPrototypeOf(document.fonts)]) {
    const load = owner.load;
    owner.load = function(...args) {
      control.heldLoads++;
      return gate.then(() => load.apply(this, args));
    };
  }
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
  return {
    raw_tex: visible('.tex, .tex-d'),
    native_math: visible('.kpress-math-semantic')
  };
}""".replace("__EXPOSED__", EXPOSED)


def loading_findings(report: LoadingReport) -> list[str]:
    """Judge observations independently of the runtime's font-family allowlist."""
    findings: list[str] = []
    if report["held_loads"] == 0:
        findings.append("the delayed-load control intercepted no font loads")
    if report["frames"] == 0:
        findings.append("the loading probe observed no animation frames")
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
        late = [
            f"{face['family']} {face['style']} {face['weight']} ({face['status']})"
            for face in math_faces
            if face["status"] != "loaded"
        ]
        if late:
            findings.append(
                "math faces were not ready at first visible paint: " + ", ".join(late)
            )
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
            url = (
                str(path)
                if str(path).startswith(("https://", "http://"))
                else Path(path).resolve().as_uri()
            )
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
                    first_paint: globalThis.__mathFirstPaint,
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
                for kind, count in fallback.items():
                    if count == 0:
                        report["findings"].append(f"no JavaScript: no visible {kind} fallback")
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
  const fault = document.createElement('div');
  fault.innerHTML = '<span class="katex" style="visibility:visible!important">x = 1</span>' +
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
    "clipped-no-javascript": (
        """<noscript><style>
.kpress-math-semantic {
  position:absolute!important; width:1px!important; height:1px!important;
  overflow:hidden!important; clip-path:inset(50%)!important;
}
</style></noscript>""",
        ("no JavaScript: no visible native_math fallback",),
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
