"""Check static readability and browser load budgets in a built producer tree.

Chromium, fresh context, 1280/390px, light/dark, default local gzip server, no network
throttling. The observer is installed before navigation. Load and fonts settle, then
three viewport samples cover scrolling. No user input is generated; input-induced
shifts are excluded by the native observer. CLI output includes the protocol and every
measurement. The separate no-JS context requires primary prose, headings and visual math.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal
from urllib.parse import unquote, urlsplit

from sqpack.probes import applied, probe

if TYPE_CHECKING:
    from playwright.sync_api import Browser, BrowserContext, Page

PROBES = Path(__file__).parent / "probes"
INSTRUMENT = applied(probe(PROBES, "check_site_rendering/instrument"))
REPORT = probe(PROBES, "check_site_rendering/report")
_FONTS = probe(PROBES, "check_site_rendering/fonts_ready")
_SCROLL = probe(PROBES, "check_site_rendering/scroll")
CLS_LIMIT = 0.1
LCP_LIMIT_MS = 4000
LONGEST_TASK_LIMIT_MS = 300
BLOCKING_LIMIT_MS = 600
SETTLE_MS = 250
NATIVE_TRACE_CATEGORIES = (
    "devtools.timeline,disabled-by-default-devtools.timeline,blink.user_timing,loading"
)
DEFAULT_PAGES = (
    "index.html",
    "all-results.html",
    "frontier.html",
    "cases/11.html",
    "result/t-037.html",
)


def install_observer(context: BrowserContext) -> None:
    """Install the production observer before a test or measured navigation."""
    context.add_init_script(INSTRUMENT)


def read_report(page: Page) -> dict[str, Any]:
    """Read the production report; fixtures exercise the same visibility/timing probe."""
    return page.evaluate(REPORT)


def wait_for_fonts(page: Page) -> None:
    """Settle the current document's face loads before measurement."""
    page.evaluate(_FONTS)


def native_trace_summary(events: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Inclusive native phases and measured selector work; nested totals overlap."""
    phases: dict[str, dict[str, float | int]] = {}
    selectors: dict[str, dict[str, int]] = {}
    for event in events:
        if event.get("ph") == "X" and "dur" in event:
            duration = event["dur"] / 1000
            phase = phases.setdefault(
                event["name"], {"count": 0, "inclusive_ms": 0.0, "max_ms": 0.0}
            )
            phase["count"] += 1
            phase["inclusive_ms"] += duration
            phase["max_ms"] = max(phase["max_ms"], duration)
        timings = event.get("args", {}).get("selector_stats", {}).get("selector_timings", [])
        for timing in timings:
            selector_row = selectors.setdefault(
                timing["selector"], {"elapsed_us": 0, "match_attempts": 0, "match_count": 0}
            )
            selector_row["elapsed_us"] += timing["elapsed (us)"]
            selector_row["match_attempts"] += timing["match_attempts"]
            selector_row["match_count"] += timing["match_count"]
    return {
        "event_count": len(events),
        "interpretation": "inclusive phases overlap; tracing overhead; no gate timing credit",
        "phases": dict(
            sorted(phases.items(), key=lambda item: item[1]["max_ms"], reverse=True)
        ),
        "selectors": [
            {"selector": selector, **data}
            for selector, data in sorted(
                selectors.items(), key=lambda item: item[1]["elapsed_us"], reverse=True
            )[:20]
        ],
    }


def record_native_trace(page: Page, destination: Path) -> Callable[[], None]:
    """Capture initial native style/layout/paint work separately from gate credit.

    The optional diagnostic adds tracing overhead. Raw CDP events remain intact, and
    an existing receipt is never overwritten."""
    if destination.exists():
        raise FileExistsError(f"native trace already exists: {destination}")
    session = page.context.new_cdp_session(page)
    events: list[dict[str, Any]] = []
    completion: dict[str, Any] | None = None

    def collected(parameters: dict[str, Any]) -> None:
        events.extend(parameters["value"])

    def finished(parameters: dict[str, Any]) -> None:
        nonlocal completion
        completion = dict(parameters)

    session.on("Tracing.dataCollected", collected)
    session.on("Tracing.tracingComplete", finished)
    session.send(
        "Tracing.start",
        {
            "categories": NATIVE_TRACE_CATEGORIES,
            "options": "recordUntilFull",
            "transferMode": "ReportEvents",
        },
    )

    def stop() -> None:
        try:
            session.send("Tracing.end")
            deadline = time.monotonic() + 10
            while completion is None:
                if time.monotonic() >= deadline:
                    raise TimeoutError("native tracing did not finish within 10 seconds")
                page.wait_for_timeout(10)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("x", encoding="utf-8") as output:
                json.dump(
                    {
                        "traceEvents": events,
                        "summary": native_trace_summary(events),
                        "diagnostic": {
                            "overhead": "native tracing enabled; no gate timing credit",
                            "categories": NATIVE_TRACE_CATEGORIES,
                            "url": page.url,
                            "browser": session.send("Browser.getVersion"),
                            "tracingComplete": completion,
                        },
                    },
                    output,
                )
        finally:
            session.detach()

    return stop


def measure(
    browser: Browser,
    url: str,
    *,
    width: int,
    scheme: Literal["light", "dark"],
    javascript: bool = True,
    trace: Path | None = None,
) -> dict[str, Any]:
    """Measure one navigation without reusing a cache or a browser context."""
    context = browser.new_context(
        viewport={"width": width, "height": 900},
        color_scheme=scheme,
        java_script_enabled=javascript,
    )
    stop_trace: Callable[[], None] | None = None
    try:
        if javascript:
            install_observer(context)
        page = context.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on(
            "response",
            lambda response: (
                errors.append(f"HTTP {response.status}: {response.url}")
                if response.status >= 400
                else None
            ),
        )
        stop_trace = record_native_trace(page, trace) if trace is not None else None
        response = page.goto(url, wait_until="load", timeout=30_000)
        if response is None or not response.ok:
            raise ValueError(f"navigation failed: {url}")
        wait_for_fonts(page)
        page.wait_for_timeout(SETTLE_MS)
        if stop_trace is not None:
            finish_trace, stop_trace = stop_trace, None
            finish_trace()
        reports = [read_report(page)]
        for fraction in (0.5, 1.0):
            page.evaluate(_SCROLL, fraction)
            page.wait_for_timeout(SETTLE_MS)
            reports.append(read_report(page))
        report = dict(reports[-1])
        report["unreadableMath"] = max(row["unreadableMath"] for row in reports)
        report["errors"] = errors
        if trace is not None:
            report["diagnosticTrace"] = str(trace)
            report["timingCredit"] = "diagnostic only; tracing overhead included"
        return report
    finally:
        try:
            if stop_trace is not None:
                stop_trace()
        finally:
            context.close()


def problems(report: dict[str, Any], *, javascript: bool = True) -> list[str]:
    found: list[str] = []
    if not report.get("heading") or report.get("contentChars", 0) < 40:
        found.append("primary heading/prose missing")
    if report.get("unreadableMath", 0):
        found.append("visual mathematics missing")
    if report.get("unreservedImages", 0):
        found.append("image dimensions are not reserved")
    if report.get("errors"):
        found.extend(report["errors"])
    if javascript:
        if not report.get("supported") or report.get("lcpMs", 0) <= 0:
            found.append("required native load timing is unavailable")
        for key, limit in (
            ("cls", CLS_LIMIT),
            ("lcpMs", LCP_LIMIT_MS),
            ("longestTaskMs", LONGEST_TASK_LIMIT_MS),
            ("blockingMs", BLOCKING_LIMIT_MS),
        ):
            if report.get(key, float("inf")) > limit:
                found.append(f"{key} {report[key]:.3f} exceeds {limit}")
    return found


def scenario_path(name: str) -> Path:
    """A scenario may carry the same query/fragment that a direct reader URL uses."""
    parsed = urlsplit(name)
    path = Path(unquote(parsed.path))
    if parsed.scheme or parsed.netloc or path.is_absolute() or ".." in path.parts:
        raise ValueError("a scenario must name a local published page")
    return path


def main(argv: Sequence[str] | None = None) -> int:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    from devtools.preview_site import launch_chromium, serve  # noqa: PLC0415

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--page", action="append")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument(
        "--trace",
        type=Path,
        help="save one initial native CDP trace; includes diagnostic overhead",
    )
    parser.add_argument(
        "--trace-scenario",
        choices=("1280-light", "1280-dark", "390-light", "390-dark"),
        default="1280-light",
        help="which existing viewport/theme pair to trace; the full gate still runs",
    )
    args = parser.parse_args(argv)
    if args.runs < 1:
        parser.error("--runs must be positive")
    names = args.page or [name for name in DEFAULT_PAGES if (args.directory / name).is_file()]
    try:
        paths = [scenario_path(name) for name in names]
    except ValueError as error:
        parser.error(str(error))
    if not names or any(not (args.directory / path).is_file() for path in paths):
        parser.error("every selected page must exist, and the selection must be nonempty")
    if args.trace is not None and (len(names) != 1 or args.runs != 1):
        parser.error("--trace requires exactly one page and one run")
    if args.trace is not None and args.trace.exists():
        parser.error("--trace refuses to overwrite an existing receipt")
    failures: list[str] = []
    results: list[dict[str, Any]] = []
    server = serve(args.directory, 0, as_pages=True)
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as playwright:
            browser = launch_chromium(playwright)
            try:
                for name in names:
                    for width in (1280, 390):
                        for scheme in ("light", "dark"):
                            samples = [
                                measure(
                                    browser,
                                    f"{base}/{name}",
                                    width=width,
                                    scheme=scheme,
                                    trace=args.trace
                                    if args.trace_scenario == f"{width}-{scheme}"
                                    else None,
                                )
                                for _ in range(args.runs)
                            ]
                            report = dict(samples[0])
                            for key in ("cls", "lcpMs", "longestTaskMs", "blockingMs"):
                                report[key] = statistics.median(
                                    sample[key] for sample in samples
                                )
                            for sample in samples:
                                failures.extend(
                                    f"{name} {width}px {scheme}: {problem}"
                                    for problem in problems(sample)
                                    if not problem.startswith(
                                        ("cls ", "lcpMs ", "longestTaskMs ", "blockingMs ")
                                    )
                                )
                            failures.extend(
                                f"{name} {width}px {scheme}: {problem}"
                                for problem in problems(report)
                                if problem.startswith(
                                    ("cls ", "lcpMs ", "longestTaskMs ", "blockingMs ")
                                )
                            )
                            static = measure(
                                browser,
                                f"{base}/{name}",
                                width=width,
                                scheme=scheme,
                                javascript=False,
                            )
                            failures.extend(
                                f"{name} no-JS {width}px {scheme}: {problem}"
                                for problem in problems(static, javascript=False)
                            )
                            results.append(
                                {
                                    "page": name,
                                    "width": width,
                                    "scheme": scheme,
                                    **report,
                                    "static": static,
                                }
                            )
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print(
        json.dumps(
            {
                "protocol": {
                    "cache": "fresh context",
                    "network": "local gzip, unthrottled",
                    "observer": "pre-navigation",
                    "runs": args.runs,
                    "settle_ms": SETTLE_MS,
                    "scroll": [0, 0.5, 1],
                    "budgets": {
                        "cls": CLS_LIMIT,
                        "lcp_ms": LCP_LIMIT_MS,
                        "longest_task_ms": LONGEST_TASK_LIMIT_MS,
                        "blocking_ms": BLOCKING_LIMIT_MS,
                    },
                },
                "pages": results,
                "failures": failures,
            },
            indent=2,
        )
    )
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
