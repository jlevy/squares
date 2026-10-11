"""Report shared scrollbar styles in page and case-popover contexts, in both themes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

from devtools.preview_site import launch_chromium
from sqpack.probes import probe

PROBES = Path(__file__).resolve().parent / "probes"


def main() -> None:
    """Inspect a running homepage without rebuilding its assets."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Homepage URL, such as http://127.0.0.1:8766/")
    args = parser.parse_args()
    results = []
    with sync_playwright() as driver:
        browser = launch_chromium(driver)
        try:
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto(args.url)
            for theme in ("light", "dark"):
                page.locator(".site-theme-button").click()
                page.locator(f'[data-theme-choice="{theme}"]').click()
                page.locator(".site-hero-packings a").click()
                page.locator(".site-case-pop article.site-case").wait_for()
                styles = page.evaluate(
                    probe(PROBES, "measure_site_scrollbars/styles"),
                    ["html", ".kpress-page-main", ".site-case-pop", ".site-case-interval"],
                )
                results.append({"theme": theme, "styles": styles})
                page.keyboard.press("Escape")
        finally:
            browser.close()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
