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
from sqpack.probes import applied, probe

#: The probes this module hands the page, one file each under `probes/`.
PROBES = Path(__file__).resolve().parent / "probes"

#: The explainer's shared math helpers (`probes/math/library.js`): `activeVariant`,
#: `exposed`, `requiredFonts`, `fontLoadObserver` and `mutatedMath`. A probe that needs them
#: takes `page.evaluate_handle(MATH_LIBRARY)` in its argument, as `math`.
MATH_LIBRARY = probe(PROBES, "math/library")

#: The same helpers installed as `__squaresMathProbes`, for an init script registered after
#: this one: an init script takes no argument, so it cannot be handed a handle.
MATH_LIBRARY_INIT = applied(MATH_LIBRARY, {"install": True})


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


#: Installed before parsing, after `MATH_LIBRARY_INIT`: samples animation frames, so hidden
#: staging nodes do not count as a paint (`probes/check_math_loading/first_paint.js`).
FIRST_PAINT_SCRIPT = applied(probe(PROBES, "check_math_loading/first_paint"))

#: Installed before parsing: holds successful font loads until released
#: (`probes/check_math_loading/hold_fonts.js`).
HOLD_FONTS_SCRIPT = applied(probe(PROBES, "check_math_loading/hold_fonts"))

EARLY_EVENTS = probe(PROBES, "check_math_loading/early_events")
READOUTS = probe(PROBES, "check_math_loading/readouts")
NO_JAVASCRIPT = probe(PROBES, "check_math_loading/no_javascript")
_REPORT = probe(PROBES, "check_math_loading/report")
_RELEASE = probe(PROBES, "check_math_loading/release")


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
            page.add_init_script(MATH_LIBRARY_INIT)
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
            page.evaluate(_RELEASE)
            page.wait_for_selector(READY, timeout=60_000)
            page.evaluate(SETTLED)
            report: LoadingReport = page.evaluate(_REPORT)
            report["sliders"] = len(targets)
            report["early_targets"] = targets
            report["findings"] = loading_findings(report)
            readouts: list[Readout] = page.evaluate(
                READOUTS, {"targets": targets, "math": page.evaluate_handle(MATH_LIBRARY)}
            )
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
                fallback = fallback_page.evaluate(
                    NO_JAVASCRIPT, {"math": fallback_page.evaluate_handle(MATH_LIBRARY)}
                )
                report["no_javascript"] = fallback
                report["findings"].extend(no_javascript_findings(fallback))
            finally:
                fallback_page.close()
            return report
        finally:
            browser.close()


def _head_script(name: str) -> str:
    """A fault probe, applied, as the script tag a negative fixture adds to the head."""
    return f"<script>{applied(probe(PROBES, name))}</script>"


#: These mutations retain the real page, fonts, event handlers, and no-JS rendering.
#: Running only dictionary-shaped observations would miss defects in the observer itself.
NEGATIVE_FIXTURES = {
    "early-paint": (
        _head_script("check_math_loading/fault_early_paint"),
        (
            "math appeared before font readiness:",
            "native MathML was visible before enhancement:",
            "math faces were not ready at first visible paint:",
        ),
    ),
    "dropped-early-input": (
        _head_script("check_math_loading/fault_dropped_early_input"),
        ("stale readout after rapid input:", "slider value changed after early input:"),
    ),
    "unready-later-family": (
        _head_script("check_math_loading/fault_unready_later_family"),
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
