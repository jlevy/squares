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
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from sqpack.probes import applied, probe

if TYPE_CHECKING:
    from playwright.sync_api import Browser

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
DEFAULT_PAGES = (
    "index.html",
    "all-results.html",
    "frontier.html",
    "cases/11.html",
    "result/t-037.html",
)


def measure(
    browser: Browser,
    url: str,
    *,
    width: int,
    scheme: Literal["light", "dark"],
    javascript: bool = True,
) -> dict[str, Any]:
    """Measure one navigation without reusing a cache or a browser context."""
    context = browser.new_context(
        viewport={"width": width, "height": 900},
        color_scheme=scheme,
        java_script_enabled=javascript,
    )
    try:
        if javascript:
            context.add_init_script(INSTRUMENT)
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
        response = page.goto(url, wait_until="load", timeout=30_000)
        if response is None or not response.ok:
            raise ValueError(f"navigation failed: {url}")
        page.evaluate(_FONTS)
        page.wait_for_timeout(SETTLE_MS)
        reports = [page.evaluate(REPORT)]
        for fraction in (0.5, 1.0):
            page.evaluate(_SCROLL, fraction)
            page.wait_for_timeout(SETTLE_MS)
            reports.append(page.evaluate(REPORT))
        report = dict(reports[-1])
        report["unreadableMath"] = max(row["unreadableMath"] for row in reports)
        report["errors"] = errors
        return report
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


def main(argv: Sequence[str] | None = None) -> int:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    from devtools.preview_site import launch_chromium, serve  # noqa: PLC0415

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--page", action="append")
    parser.add_argument("--runs", type=int, default=1)
    args = parser.parse_args(argv)
    if args.runs < 1:
        parser.error("--runs must be positive")
    names = args.page or [name for name in DEFAULT_PAGES if (args.directory / name).is_file()]
    if not names or any(not (args.directory / name).is_file() for name in names):
        parser.error("every selected page must exist, and the selection must be nonempty")
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
                                measure(browser, f"{base}/{name}", width=width, scheme=scheme)
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
