#!/usr/bin/env python3
"""The published workbench under its own Content-Security-Policy.

    uv run --frozen --all-extras --group dev python -m workbench_tools.check_page_policy [PAGE]

`build_site` publishes the page with a `default-src 'none'` policy, so the browser refuses
anything the page was not built to need. The policy grants no `'unsafe-eval'` for test
tooling, so a `wait_for_function` predicate written as an expression string, which
Playwright compiles inside the page, would be refused; the checkers' predicates are probe
functions, and none opens the page with `bypass_csp`. The other checkers exercise features,
though, and something has to hold the policy itself to what the page needs. This loads the
page as the public does:

1. It installs the `policy/record-violations` init probe, which keeps every
   `securitypolicyviolation` the document reports from before the page's own scripts run,
   and listens for console and page errors.
2. It requires the page to initialise (`policy/started`: the Pack and Search APIs exist,
   Pack drew its squares, the `data:` fonts loaded), then switches through Animate, Search
   and Pack and starts a Pack run.
3. It requires no recorded violation, no console error and no page error.

**The recorder is proved live on every run.** The same page, with its policy changed to
refuse the page's own fonts, must report `font-src` violations. A recorder that stopped
recording would otherwise read exactly like a page that needs nothing it is denied.

With no argument the page is `packing/site/workbench/index.html`, which
`squares-workbench-build` writes; `check_frontend` passes the page it built.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from playwright.sync_api import ConsoleMessage, sync_playwright

from sqpack.probes import applied
from workbench_tools.build_site import OUT, POLICY_META
from workbench_tools.probes import probe

DEFAULT_PAGE = OUT / "index.html"

#: The negative control: the published policy with the page's fonts refused.
FONTS_REFUSED = POLICY_META.replace("font-src data:", "font-src 'none'")

#: How long the page runs in each view before its violations are read, in milliseconds.
SETTLE_MS = 300


@dataclass
class PolicyRun:
    """What one load of the page reported."""

    started: dict[str, Any]
    violations: list[dict[str, str]] | None
    errors: list[str] = field(default_factory=list)


def with_policy(page_text: str, meta: str) -> str:
    """The page with its published policy replaced by `meta`; refuses a page without one."""
    if page_text.count(POLICY_META) != 1:
        raise ValueError("the page does not carry the published Content-Security-Policy once")
    return page_text.replace(POLICY_META, meta)


def load(page_path: Path, *, exercise: bool) -> PolicyRun:
    """Load the page with no policy bypass, and return what its policy refused."""
    errors: list[str] = []

    def console(message: ConsoleMessage) -> None:
        if message.type == "error":
            errors.append(f"console.error: {message.text}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        try:
            context = browser.new_context(viewport={"width": 1440, "height": 1000})
            context.add_init_script(applied(probe("policy/record-violations")))
            page = context.new_page()
            page.on("console", console)
            page.on("pageerror", lambda error: errors.append(f"pageerror: {error}"))
            page.goto(page_path.resolve().as_uri(), wait_until="load")
            started = page.evaluate(probe("policy/started"))
            if exercise:
                for mode in ("#mode-animate", "#mode-search", "#mode-pack"):
                    page.locator(mode).click()
                    page.wait_for_timeout(SETTLE_MS)
                page.locator("#pack-run").click()
                page.wait_for_timeout(SETTLE_MS)
            violations = page.evaluate(probe("policy/violations"))
        finally:
            browser.close()
    return PolicyRun(started=started, violations=violations, errors=errors)


def faults(published: PolicyRun, refused: PolicyRun) -> list[str]:
    """Everything wrong with the published run, and with the recorder's control run."""
    found: list[str] = []
    started = published.started
    if not (started.get("pack") and started.get("search")):
        found.append(f"the page did not start its APIs under its policy: {started}")
    if not started.get("squares"):
        found.append(f"the Pack stage drew no squares under its policy: {started}")
    if started.get("fonts") != "loaded":
        found.append(f"the page's fonts did not load under its policy: {started}")
    if published.violations is None:
        found.append("the violation recorder did not run in the published page")
    elif published.violations:
        found.append(
            "the published policy refused what the page needs: "
            + json.dumps(published.violations, sort_keys=True)
        )
    found.extend(published.errors)
    directives = {entry.get("directive") for entry in refused.violations or []}
    if "font-src" not in directives:
        found.append(
            "the recorder is not live: a policy refusing the page's fonts reported "
            f"{refused.violations!r}"
        )
    return found


def check(page_path: Path) -> str:
    """Load the page as published, and once under a policy that must be refused."""
    page_text = page_path.read_text(encoding="utf-8")
    with_policy(page_text, POLICY_META)
    published = load(page_path, exercise=True)
    with tempfile.TemporaryDirectory(prefix="squares-page-policy-") as scratch:
        control = Path(scratch) / "fonts-refused.html"
        control.write_text(with_policy(page_text, FONTS_REFUSED), encoding="utf-8")
        refused = load(control, exercise=False)
    found = faults(published, refused)
    if found:
        raise ValueError("page policy check failed:\n  " + "\n  ".join(found))
    count = len(refused.violations or [])
    return (
        "published policy: page starts, switches views and runs Pack with no violation; "
        f"recorder live ({count} font-src refusals under a control policy)"
    )


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    page_path = Path(arguments[0]) if arguments else DEFAULT_PAGE
    if not page_path.is_file():
        print(f"no built page at {page_path}; run `squares-workbench-build` first")
        return 1
    print(f"OK: {check(page_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
