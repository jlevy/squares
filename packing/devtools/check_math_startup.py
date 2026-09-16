"""Measure natural math startup and neighboring text movement, without delaying fonts.

Each load starts a fresh browser and context. Browser caches are cold; the operating
system's file and font caches are uncontrolled. Paired runs alternate control and
candidate order and retain every observation, including invalid loads. Times are
relative to navigation start. An animation-frame observation is an opportunity to
paint, not a compositor presentation timestamp. Exposed math includes the active
document below the fold; the probe never scrolls to manufacture an earlier result.

The primary latency measurement is ``parameters_ready_ms``: all fourteen initial
Figure 6 math labels and readouts are readable in the same observed frame. Geometry
follows persistent adjacent text characters, including their positions relative to
the containing block. Text-range bottoms are baseline proxies, not font baselines.
Layout and latency remain descriptive: this tool does not invent a performance
acceptance threshold. Missing math, anchors, or instrumentation invalidates a run.

The explicit ``parameters`` mode measures only the fourteen parameter targets. It
omits all-page text discovery and geometry, retaining the same source and exposure
checks once each target can be visible, and stops frame sampling when all fourteen
are readable. This records an animation-frame paint opportunity, not a compositor
presentation or first-contentful-paint timestamp. Final settlement rediscovers and
validates every target; ``finish_validation_ms`` records that later work separately
from ``sampler_total_ms``. Its timings form a separate instrument regime; compare
control and candidate within that mode, never across modes.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import statistics
import subprocess
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Literal

from devtools.check_math_loading import MATH_LIBRARY_INIT, page_url
from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY, SETTLED_REFERENCE
from sqpack.probes import applied, probe

type BrowserName = Literal["chromium", "firefox", "webkit"]
type MeasurementMode = Literal["full", "parameters"]
type JsonRecord = dict[str, Any]

EXPECTED_PARAMETERS = 14

#: The probes this module hands the page, one file each under `probes/`.
PROBES = Path(__file__).resolve().parent / "probes"

#: The instrument, installed before parsing after `MATH_LIBRARY_INIT`, applied with the mode.
_STARTUP = probe(PROBES, "check_math_startup/startup")
_SETTLEMENT_DONE = probe(PROBES, "check_math_startup/settlement_done")
_FINISH = probe(PROBES, "check_math_startup/finish")
_FIXTURE_PENDING = applied(probe(PROBES, "check_math_startup/fixture_pending"))
_FIXTURE_PAGE = probe(PROBES, "check_math_startup/fixture_page")


def startup_findings(report: JsonRecord, *, width: int, height: int) -> list[str]:
    """Reject incomplete measurements; speed and movement need a separate criterion."""
    findings: list[str] = []
    mode = report.get("mode", "full")
    if mode not in ("full", "parameters"):
        findings.append(f"unknown startup measurement mode: {mode}")
    full = mode != "parameters"
    counters = report.get("counters", {})
    for name, minimum in {
        "frames": 1,
        "font_hooks": 2,
        "katex_hooks": 1,
        "runtime_hooks": 2,
        **({"anchor_samples": 1} if full else {}),
    }.items():
        if counters.get(name, 0) < minimum:
            findings.append(f"missing instrumentation: {name}")
    if counters.get("render_calls", 0) + counters.get("hydrate_calls", 0) == 0:
        findings.append("no observed math rendering or hydration activity")
    metrics = report.get("metrics", {})
    milestones = [
        "instrumentation_installed_ms",
        "parameters_ready_ms",
        "math_ready_marker_ms",
    ]
    if full:
        milestones.extend(("first_prose_math_ms", "first_caption_math_ms"))
    for name in milestones:
        value = metrics.get(name)
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            findings.append(f"missing startup milestone: {name}")
    targets = report.get("targets", [])
    if len(targets) != EXPECTED_PARAMETERS:
        findings.append(
            f"expected {EXPECTED_PARAMETERS} active parameter targets, found {len(targets)}"
        )
    findings.extend(
        f"missing, hidden, or incorrect parameter math: {target.get('id')}"
        for target in targets
        if not target.get("correct") or not target.get("exposed")
    )
    anchors = report.get("anchors", [])
    findings.extend(
        f"no readable neighboring text anchors: {category}"
        for category in (("prose", "caption", "parameter") if full else ())
        if not any(
            anchor.get("category") == category and anchor.get("samples", 0)
            for anchor in anchors
        )
    )
    snapshots = report.get("snapshots", [])
    if len(snapshots) < 2:
        findings.append("missing initial or final viewport state")
    for index, snapshot in enumerate(snapshots):
        if snapshot.get("width") != width or snapshot.get("height") != height:
            findings.append("viewport dimensions changed during startup")
        if snapshot.get("visibility") != "visible" or not snapshot.get("focused"):
            findings.append("page was not visible and focused during startup")
        initializing = (
            index < len(snapshots) - 1
            and not snapshot.get("math_ready")
            and not snapshot.get("active_certificates")
        )
        if not initializing and len(snapshot.get("active_certificates", [])) != 1:
            findings.append("expected exactly one active certificate")
    if snapshots:
        findings.extend(
            f"startup changed viewport state: {key}"
            for key in (
                "scroll_x",
                "scroll_y",
                "document_scroll_x",
                "document_scroll_y",
            )
            if any(snapshot.get(key) != snapshots[0].get(key) for snapshot in snapshots[1:])
        )
        certificates = [
            snapshot["active_certificates"]
            for snapshot in snapshots
            if snapshot.get("active_certificates")
        ]
        if certificates and any(value != certificates[0] for value in certificates[1:]):
            findings.append("startup changed viewport state: active_certificates")
    findings.extend(f"page error: {error}" for error in report.get("errors", []))
    return findings


def measure_startup(
    path: Path | str = PAGE,
    *,
    width: int = 1280,
    height: int = 720,
    browser_name: BrowserName = "chromium",
    mode: MeasurementMode = "full",
    timeout_ms: int = 60_000,
) -> JsonRecord:
    """Observe one untouched navigation in a fresh browser process and context."""
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError  # noqa: PLC0415
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        override = os.environ.get(BROWSER_OVERRIDE) if browser_name == "chromium" else None
        browser = getattr(driver, browser_name).launch(executable_path=override)
        try:
            page = browser.new_page(viewport={"width": width, "height": height})
            page.set_default_timeout(timeout_ms)
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.add_init_script(MATH_LIBRARY_INIT)
            page.add_init_script(applied(_STARTUP, {"mode": mode}))
            timeout: str | None = None
            try:
                page.goto(page_url(path), wait_until="domcontentloaded")
                page.wait_for_selector(READY)
                # Evaluate does not honor Playwright's default timeout. Start the
                # real settlement promise without awaiting it in that call, then
                # use the bounded wait API so broken pages still retain a report.
                page.evaluate(
                    probe(PROBES, "check_math_startup/start_settlement"),
                    {"settled": page.evaluate_handle(SETTLED_REFERENCE)},
                )
                page.wait_for_function(_SETTLEMENT_DONE)
            except PlaywrightTimeoutError as error:
                timeout = str(error).splitlines()[0]
            report: JsonRecord = page.evaluate(_FINISH)
            report["errors"].extend(errors)
            report["environment"] = {
                "browser": browser_name,
                "browser_version": browser.version,
                "browser_cache": "cold: fresh process and context per load",
                "os_cache": "uncontrolled: file and font caches may be warm",
                "headless": True,
                "viewport": {"width": width, "height": height},
                "recorded_at": datetime.now(UTC).isoformat(),
            }
            report["requested_source"] = str(path)
            report["findings"] = startup_findings(report, width=width, height=height)
            if timeout:
                report["findings"].append(f"startup did not settle: {timeout}")
            return report
        finally:
            browser.close()


def summarize(runs: Sequence[JsonRecord]) -> JsonRecord:
    """Keep missing observations absent from statistics, never turn them into zeros."""
    names = sorted({name for run in runs for name in run.get("metrics", {})})
    summary: JsonRecord = {}
    for name in names:
        values = [
            value
            for run in runs
            if isinstance(value := run.get("metrics", {}).get(name), (int, float))
            and math.isfinite(value)
        ]
        summary[name] = {
            "count": len(values),
            "missing": len(runs) - len(values),
            "median": statistics.median(values) if values else None,
            "min": min(values) if values else None,
            "max": max(values) if values else None,
        }
    return summary


def instrument_provenance(runs: Sequence[JsonRecord]) -> JsonRecord:
    """Record the executing tool's provenance directly from Git and the process."""
    repo = Path(__file__).resolve().parents[2]

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=repo, check=True, capture_output=True, text=True
        ).stdout.strip()

    return {
        "git_head": git("rev-parse", "HEAD"),
        "git_dirty": bool(git("status", "--porcelain")),
        "entry_point": "devtools.check_math_startup",
        "argv": sys.orig_argv,
        "platform": platform.platform(),
        "python": sys.version,
        "python_executable": sys.executable,
        "browser_versions": sorted(
            {
                f"{run['environment']['browser']} {run['environment']['browser_version']}"
                for run in runs
                if "environment" in run
            }
        ),
    }


def run_measurements(
    sources: Mapping[str, Path | str],
    *,
    runs: int = 3,
    width: int = 1280,
    height: int = 720,
    browser_name: BrowserName = "chromium",
    mode: MeasurementMode = "full",
) -> JsonRecord:
    """Measure matched pairs sequentially, reversing their order on alternate pairs."""
    observations: list[JsonRecord] = []
    for pair in range(runs):
        order = list(sources.items())
        if pair % 2:
            order.reverse()
        for label, path in order:
            report = measure_startup(
                path, width=width, height=height, browser_name=browser_name, mode=mode
            )
            observations.append({"pair": pair + 1, "label": label, **report})
    return {
        "schema_version": 1,
        "measurement": "natural-math-startup",
        "mode": mode,
        "instrument": instrument_provenance(observations),
        "performance_verdict": "not evaluated; acceptance criterion belongs to the experiment",
        "runs": observations,
        "summary": {
            label: summarize([run for run in observations if run["label"] == label])
            for label in sources
        },
        "findings": [
            f"{run['label']} pair {run['pair']}: {finding}"
            for run in observations
            for finding in run["findings"]
        ],
    }


def browser_fixture(mode: str) -> str:
    """A real layout with the same public API and Figure 6 output contract.

    Only the fixtures introduce delays or changed widths. Normal measurements never
    alter page behavior. These small controls isolate the observer from publication
    changes and do not need external fonts, images, or a generated site artifact.
    """
    return (
        r"""<!doctype html>
<html><head><meta charset="utf-8"><title>Math startup observer control</title>
<style>
body {font:16px serif; margin:20px}
.kpress-prose {width:600px; max-width:90vw}
.katex-mathml {position:absolute; width:1px; height:1px; overflow:hidden; clip-path:inset(50%)}
html[data-kpress-math-pending] .tex {visibility:hidden}
dt, dd {height:24px; margin:0} dt {float:left; width:240px} dd {width:480px}
.shift .tex {display:inline-block; width:20px}
.squares-math-variant {display:none}
.squares-math-variant[data-squares-math-contexts~="custom-serif"] {display:inline}
</style>
<script>"""
        + _FIXTURE_PENDING
        + r"""</script>
</head><body>
<main class="kpress-prose" data-kpress-viewport>
<p id="prose" class="shift">Before <span class="tex">x</span> after the formula.</p>
<div class="cert-figure" data-cert="test">
<figure data-figure="6"><div class="panel">
<div class="ctl"><span class="caps">Angle <span class="tex">\varphi</span></span>
<input id="phi-test" type="range" min="0" max="450" value="196"></div>
<div class="ctl"><span class="caps">Net <span class="tex">K</span></span></div>
<dl class="kv">
<dt><span class="tex">\varphi</span></dt><dd id="s-phi-test"></dd>
<dt>nearest <span class="tex">\theta</span></dt><dd id="s-theta-test"></dd>
<dt>mismatch <span class="tex">d</span></dt><dd id="s-d-test"></dd>
<dt>largest <span class="tex">D</span></dt><dd id="s-D-test"></dd>
<dt><span class="tex">B</span> admitted</dt><dd id="s-B-test"></dd>
<dt><span class="tex">B(\cos d + \sin d)</span></dt><dd id="s-prod-test"></dd>
</dl></div>
<figcaption class="kpress-figcaption">Caption before
<span class="tex">x</span> after math.</figcaption>
</figure></div></main>
<script>
"""
        + applied(_FIXTURE_PAGE, {"mode": mode})
        + "</script></body></html>"
    )


def self_test(
    *, browser_name: BrowserName = "chromium", mode: MeasurementMode = "full"
) -> JsonRecord:
    """Run real positive and negative pages; a fast pytest run does not need a browser."""
    observations: JsonRecord = {}
    findings: list[str] = []
    with TemporaryDirectory(prefix="math-startup-controls-") as directory:
        controls = (
            "control",
            "no-warmup",
            "delayed",
            "variants",
            "wrong-active-variant",
            "missing-math",
            "missing-counters",
            "late-target",
            *(("width-change", "missing-anchors") if mode == "full" else ()),
        )
        for control in controls:
            path = Path(directory) / f"{control}.html"
            path.write_text(browser_fixture(control))
            observations[control] = measure_startup(
                path, browser_name=browser_name, mode=mode, timeout_ms=5_000
            )
    for control in (
        "control",
        "no-warmup",
        "delayed",
        "variants",
        *(("width-change",) if mode == "full" else ()),
    ):
        findings.extend(
            f"{control}: {message}" for message in observations[control]["findings"]
        )
    if observations["no-warmup"]["counters"]["ready_calls"] != 0:
        findings.append("the no-warmup control unexpectedly called the warmup API")
    for control, run in observations.items():
        duration = run["metrics"].get("finish_validation_ms")
        if (
            not isinstance(duration, (int, float))
            or not math.isfinite(duration)
            or duration < 0
        ):
            findings.append(f"{control}: missing final-validation cost")
    baseline = observations["control"]["metrics"]
    delayed = observations["delayed"]["metrics"]
    if delayed.get("parameters_ready_ms", 0) - baseline.get("parameters_ready_ms", 0) < 150:
        findings.append("the delayed control did not record the known 300 ms delay")
    if mode == "full":
        changed = observations["width-change"]
        if baseline.get("anchor_max_displacement_px", math.inf) > 0.1:
            findings.append("the stable control reported neighboring text movement")
        if changed["metrics"].get("anchor_max_local_displacement_px", 0) < 100:
            findings.append("the width-change control did not detect adjacent text movement")
        if not changed.get("pre_reveal_frame_observed"):
            findings.append("the width-change control missed the readable pre-reveal frame")
    elif any(run["counters"]["anchor_samples"] for run in observations.values()):
        findings.append("parameter mode unexpectedly sampled all-page text anchors")
    for control, required in {
        "missing-math": "incorrect parameter math",
        "wrong-active-variant": "incorrect parameter math",
        "missing-counters": "missing instrumentation: font_hooks",
        "late-target": "expected 14 active parameter targets, found 15",
        **({"missing-anchors": "neighboring text anchors: prose"} if mode == "full" else {}),
    }.items():
        if not any(required in message for message in observations[control]["findings"]):
            findings.append(f"{control}: the negative control was not rejected")
    return {
        "schema_version": 1,
        "mode": mode,
        "instrument": instrument_provenance(list(observations.values())),
        "self_test": observations,
        "findings": findings,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", nargs="?", help="Local HTML or HTTP(S) URL")
    parser.add_argument("--control", help="Frozen control HTML or URL")
    parser.add_argument("--candidate", help="Candidate HTML or URL")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument(
        "--browser", choices=("chromium", "firefox", "webkit"), default="chromium"
    )
    parser.add_argument("--mode", choices=("full", "parameters"), default="full")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--self-test", action="store_true", help="Exercise retained browser controls"
    )
    args = parser.parse_args(argv)
    if args.runs < 1 or args.width < 1 or args.height < 1:
        parser.error("runs and viewport dimensions must be positive")
    if bool(args.control) != bool(args.candidate) or (args.page and args.control):
        parser.error("use a page, or both --control and --candidate")
    report = (
        self_test(browser_name=args.browser, mode=args.mode)
        if args.self_test
        else run_measurements(
            {"control": args.control, "candidate": args.candidate}
            if args.control
            else {"page": args.page or PAGE},
            runs=args.runs,
            width=args.width,
            height=args.height,
            browser_name=args.browser,
            mode=args.mode,
        )
    )
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
        print(f"Wrote {args.output}")
    else:
        print(encoded, end="")
    for finding in report["findings"]:
        print(f"FAIL: {finding}")
    return int(bool(report["findings"]))


if __name__ == "__main__":
    raise SystemExit(main())
