"""Check native document-scroll restoration through a real HTTP reload.

Use location.reload(), the browser's document navigation API. Playwright's WebKit
Page.reload protocol command resets even an unmodified document control, so it cannot
establish the browser behavior being checked here. No production scroll state or
restoration code is injected. --self-test retains a disabled-restoration control.
"""

from __future__ import annotations

import argparse
import json
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal, TypedDict

from devtools.render_explainer_pdf import PAGE


class Position(TypedDict):
    """The actual scrolling element and its position at one observation."""

    top: float
    document_top: float
    native: bool
    restoration: str
    hash: str


class ReloadReport(TypedDict):
    """Before/after observations, including the navigation type and engine."""

    browser: str
    browser_version: str
    javascript: bool
    width: int
    before: Position
    after: Position
    navigation_type: str
    findings: list[str]


POSITION = """() => {
  const viewport = document.querySelector('[data-kpress-viewport]')
    || document.scrollingElement;
  return {top: viewport.scrollTop, document_top: scrollY,
    native: viewport === document.scrollingElement,
    restoration: history.scrollRestoration, hash: location.hash};
}"""
SETTLE = """async () => {
  await globalThis.squaresMath?.settled?.();
  await document.fonts.ready;
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
}"""


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        _ = format, args


@contextmanager
def served_page(path: Path) -> Iterator[str]:
    """Serve the original directory so relative publication assets still resolve."""
    handler = partial(_QuietHandler, directory=str(path.resolve().parent))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        from urllib.parse import quote  # noqa: PLC0415

        yield f"http://127.0.0.1:{server.server_port}/{quote(path.name)}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def findings(report: ReloadReport) -> list[str]:
    """A top-of-page reload cannot pass by never scrolling in the first place."""
    before, after = report["before"], report["after"]
    found: list[str] = []
    if not before["native"] or not after["native"]:
        found.append("The article does not use the browser's document scroller")
    if before["top"] < 600:
        found.append("The page did not reach a meaningful reading position before reload")
    if abs(after["top"] - before["top"]) > 1:
        found.append(f"Reload moved the reading position: {before['top']} -> {after['top']} px")
    if after["hash"] != before["hash"]:
        found.append("Reload changed the selected document fragment")
    if report["navigation_type"] != "reload":
        found.append("The observation did not perform a browser reload")
    return found


def check_reload(
    path: Path,
    *,
    browser_name: Literal["chromium", "firefox", "webkit"] = "chromium",
    width: int = 1280,
    javascript: bool = True,
    fragment: str = "",
) -> ReloadReport:
    """Load, scroll, then reload the same history entry without replacing its state."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with served_page(path) as url, sync_playwright() as driver:
        browser = getattr(driver, browser_name).launch()
        try:
            page = browser.new_page(
                viewport={"width": width, "height": 720}, java_script_enabled=javascript
            )
            page.goto(url + ("#" + fragment if fragment else ""), wait_until="load")
            if javascript:
                page.evaluate(SETTLE)
            page.evaluate("""() => {
              const viewport = document.querySelector('[data-kpress-viewport]')
                || document.scrollingElement;
              viewport.scrollTo({top: Math.min(3000,
                (viewport.scrollHeight - viewport.clientHeight) * .6), behavior: 'instant'});
            }""")
            if javascript:
                page.evaluate(SETTLE)
            before: Position = page.evaluate(POSITION)
            with page.expect_navigation(wait_until="load"):
                page.evaluate("location.reload()")
            if javascript:
                page.evaluate(SETTLE)
            after: Position = page.evaluate(POSITION)
            report: ReloadReport = {
                "browser": browser_name,
                "browser_version": browser.version,
                "javascript": javascript,
                "width": width,
                "before": before,
                "after": after,
                "navigation_type": page.evaluate(
                    "performance.getEntriesByType('navigation')[0].type"
                ),
                "findings": [],
            }
            report["findings"] = findings(report)
            return report
        finally:
            browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", type=Path, nargs="?", default=PAGE)
    parser.add_argument(
        "--browser", choices=("chromium", "firefox", "webkit"), default="chromium"
    )
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--fragment", default="")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    runs = [
        check_reload(
            args.page,
            browser_name=args.browser,
            width=args.width,
            javascript=js,
            fragment=args.fragment,
        )
        for js in (True, False)
    ]
    result: dict[str, object] = {"input": str(args.page.resolve()), "runs": runs}
    failed = any(run["findings"] for run in runs)
    if args.self_test:
        with TemporaryDirectory(prefix="squares-scroll-controls-") as temporary:
            root = Path(temporary)
            positive = root / "native.html"
            control = (
                "<!doctype html><html><body>"
                "<main style='height:10000px'>Prose</main></body></html>"
            )
            positive.write_text(control)
            negative = root / "disabled.html"
            negative.write_text(
                control.replace(
                    "<body>", "<body><script>history.scrollRestoration='manual'</script>"
                )
            )
            good = check_reload(positive, browser_name=args.browser, width=args.width)
            bad = check_reload(negative, browser_name=args.browser, width=args.width)
            rejected = any("Reload moved" in finding for finding in bad["findings"])
            result["controls"] = {"native": good, "disabled": bad, "rejected": rejected}
            failed = failed or bool(good["findings"]) or not rejected
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
