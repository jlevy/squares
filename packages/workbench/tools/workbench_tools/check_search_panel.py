"""Smoke-test bounded experimental Search runs in the built workbench."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, expect, sync_playwright

from workbench_tools.probes import probe

# The status line once a run stops, whichever way it stops.
SETTLED = re.compile(r"finished|cancelled|could not run")
# The source revision `build_site` stamps into the page.
REVISION = re.compile(r"[0-9a-f]{40}")


def fill_plan(
    page: Page, *, n: int, seeds: str, steps: int, repair: bool, proposal: str = "grid"
) -> None:
    """Fill the Search form."""
    page.locator("#search-n").fill(str(n))
    page.locator("#search-seeds").fill(seeds)
    page.locator("#search-steps").fill(str(steps))
    page.locator("#search-proposal").select_option(proposal)
    page.locator("#search-repair").set_checked(repair)


def run_plan(
    page: Page, *, n: int, seeds: str, steps: int, repair: bool, proposal: str = "grid"
) -> str:
    """Fill the Search form, start a run, and return the status line once it settles.

    Start's click handler sets the "running" status before the click returns, so the settled
    text this waits for is the new run's, not the previous one's. Runs long enough to cancel
    wait for Cancel to enable instead, which only a running search does.
    """
    fill_plan(page, n=n, seeds=seeds, steps=steps, repair=repair, proposal=proposal)
    page.locator("#search-start").click()
    status = page.locator("#search-status")
    expect(status).to_have_text(SETTLED)
    return status.inner_text()


def start_long_run(page: Page) -> None:
    """Start a plan that runs for seconds and return once it is running."""
    fill_plan(page, n=32, seeds="0,1,2,3,4,5,6,7", steps=5000, repair=False)
    page.locator("#search-start").click()
    expect(page.locator("#search-cancel")).to_be_enabled()
    expect(page.locator("#search-status")).to_contain_text("running")


def export_ledger(page: Page) -> dict[str, Any]:
    """Download the panel's ledger and parse it."""
    exported = page.locator("#search-export")
    expect(exported).to_be_enabled()
    with page.expect_download() as captured:
        exported.click()
    ledger_path = captured.value.path()
    if ledger_path is None:
        raise ValueError("Search ledger export did not download")
    return json.loads(Path(str(ledger_path)).read_text(encoding="utf-8"))


def check_bounded_run(page: Page) -> None:
    """One slot of one step records its outcome and exports it."""
    status = run_plan(page, n=1, seeds="0", steps=1, repair=False)
    if "finished" not in status:
        raise ValueError(f"Search did not finish its bounded slot: {status}")
    progress = page.locator("#search-progress").inner_text()
    if "1/1 slots" not in progress or "1 completed" not in progress:
        raise ValueError(f"Search did not record its bounded slot: {progress}")
    if "1 of 1 completed valid" not in progress:
        raise ValueError(f"Search did not summarise validity: {progress}")
    ledger = export_ledger(page)
    if len(ledger.get("outcomes", [])) != 1:
        raise ValueError("Search ledger omitted its completed slot")
    source = ledger["plan"]["source"]
    stamped = page.locator('meta[name="squares-workbench-dirty"]').get_attribute("content")
    if REVISION.fullmatch(source["commit"]) is None or source["dirty"] != (stamped == "true"):
        raise ValueError(f"Search plan does not record the page's source: {source}")


def check_keys_stay_in_search(page: Page) -> None:
    """While Search shows, the page's global shortcuts leave its fields and buttons alone.

    The catalogue's key handler used to act behind Search: Space or an arrow blurred the
    field being typed in and ran the hidden Animate transport, Space on a focused button was
    swallowed, and a bare `c` entered capture mode (#160 R6).
    """
    seeds = page.locator("#search-seeds")
    seeds.fill("")
    seeds.focus()
    page.keyboard.type("0, 5")
    page.keyboard.press("ArrowLeft")
    page.keyboard.press("ArrowRight")
    owner = page.evaluate(probe("animate/input-owner"))
    if owner["seeds"] != "0, 5" or owner["focused"] != "search-seeds":
        raise ValueError(f"typing in Search's seeds field was taken by page shortcuts: {owner}")
    if owner["transport"] != "Play":
        raise ValueError(f"a key in Search ran the hidden Animate transport: {owner}")
    page.locator("#search-n").fill("1")
    page.locator("#search-steps").fill("1")
    seeds.fill("0")
    page.locator("#search-repair").set_checked(False)
    page.locator("#search-start").focus()
    page.keyboard.press("c")
    if page.evaluate(probe("animate/input-owner"))["capture"]:
        raise ValueError("a bare `c` on a focused Search button entered capture mode")
    page.keyboard.press(" ")
    status = page.locator("#search-status")
    expect(status).to_have_text(SETTLED)
    if "finished" not in status.inner_text():
        raise ValueError(
            f"Space on a focused Start did not run the search: {status.inner_text()}"
        )


def check_multi_seed_run(page: Page) -> dict[str, Any]:
    """Three random-start seeds each record an outcome, rank by side and export together."""
    status = run_plan(page, n=3, seeds="0,1,2", steps=30, repair=False, proposal="random")
    if "finished" not in status:
        raise ValueError(f"Search did not finish its three seeds: {status}")
    progress = page.locator("#search-progress").inner_text()
    if "3/3 slots; 3 completed" not in progress or "of 3 completed valid" not in progress:
        raise ValueError(f"Search did not record and summarise three seeds: {progress}")
    rows = page.locator("#search-results tr")
    expect(rows).to_have_count(3)
    cells = [rows.nth(index).locator("td").all_inner_texts() for index in range(3)]
    if sorted(row[0] for row in cells) != ["0", "1", "2"]:
        raise ValueError(f"Search table does not show each seed once: {cells}")
    ranks = [
        float(row[3]) if row[2] == "valid" and row[3] != "—" else float("inf") for row in cells
    ]
    if ranks != sorted(ranks):
        raise ValueError(f"Search table is not ranked by side: {cells}")
    ledger = export_ledger(page)
    outcomes = ledger["outcomes"]
    if [outcome["slot"]["seed"] for outcome in outcomes] != [0, 1, 2] or any(
        outcome["status"] != "completed" or outcome["slot"]["n"] != 3 for outcome in outcomes
    ):
        raise ValueError("Search ledger does not hold the three completed n = 3 seeds")
    return ledger


def check_rejected_import(page: Page, ledger: dict[str, Any]) -> None:
    """Malformed and forged ledgers are refused; the untouched one resumes.

    The form still declares the plan `ledger` was run from, so a refusal is about the ledger.
    Each expected status differs from the one before it, so no wait can match stale text.
    """
    if page.locator("#search-workspace details[open]").count() == 0:
        page.locator("#search-workspace details summary").click()
    status = page.locator("#search-status")
    page.locator("#search-import").fill('{"contract": ')
    page.locator("#search-resume").click()
    expect(status).to_contain_text("Ledger rejected")
    forged = json.loads(json.dumps(ledger))
    forged["outcomes"][0]["result"]["raw"]["snapshot"]["poses"][0]["x"] += 100
    page.locator("#search-import").fill(json.dumps(forged))
    page.locator("#search-resume").click()
    expect(status).to_have_text(re.compile(r"^Ledger rejected: .*disagrees"))
    page.locator("#search-import").fill(json.dumps(ledger))
    page.locator("#search-resume").click()
    expect(status).to_contain_text("finished")


def check_cancel(page: Page) -> None:
    """Cancel stops the running slot, and the ledger exports it as cancelled."""
    start_long_run(page)
    page.locator("#search-cancel").click()
    expect(page.locator("#search-status")).to_contain_text("cancelled")
    expect(page.locator("#search-start")).to_be_enabled()
    ledger = export_ledger(page)
    statuses = [outcome["status"] for outcome in ledger["outcomes"]]
    if statuses != ["cancelled"] + ["not-started"] * 7:
        raise ValueError(f"Search ledger does not record the cancelled slot: {statuses}")
    if ledger["outcomes"][0]["slot"]["n"] != 32:
        raise ValueError("Search exported a ledger from an earlier plan")


def check_leaving_cancels(page: Page) -> None:
    """Switching to Pack cancels a running search rather than leaving it working unseen."""
    start_long_run(page)
    page.locator("#mode-pack").click()
    expect(page.locator("#pack-workspace")).to_be_visible()
    page.locator("#mode-search").click()
    expect(page.locator("#search-status")).to_contain_text("cancelled")
    expect(page.locator("#search-start")).to_be_enabled()
    progress = page.locator("#search-progress").inner_text()
    if " 0 pending" in progress:
        raise ValueError(f"Search finished every slot instead of cancelling: {progress}")


def check_repair_run(page: Page) -> None:
    """Ticking Attempt Resolve runs Resolve and ranks the repaired state."""
    status = run_plan(page, n=5, seeds="0", steps=100, repair=True)
    if "could not run" in status or "finished" not in status:
        raise ValueError(f"Search with Resolve did not finish: {status}")
    ledger = export_ledger(page)
    configuration = ledger["plan"]["configurations"][0]["configuration"]
    if configuration["objective"]["state"] != "repaired":
        raise ValueError(f"Search with Resolve ranks {configuration['objective']['state']}")
    for outcome in ledger["outcomes"]:
        if outcome["status"] != "completed":
            raise ValueError(f"Search with Resolve left a slot {outcome['status']}")
        result = outcome["result"]
        if result["selectedState"] != "repaired" or result["repair"]["termination"] == (
            "not-requested"
        ):
            raise ValueError(f"Search with Resolve did not repair: {result['repair']}")
    steps = sum(outcome["result"]["work"]["physicsSteps"] for outcome in ledger["outcomes"])
    iterations = sum(
        outcome["result"]["work"]["repairIterations"] for outcome in ledger["outcomes"]
    )
    work = f"{steps} physics steps, {iterations} repair iterations"
    progress = page.locator("#search-progress").inner_text()
    if iterations < 1 or "1 of 1 completed valid" not in progress or work not in progress:
        raise ValueError(f"Search with Resolve summary lacks validity or {work}: {progress}")


def check(page_path: Path) -> str:
    """Run tiny plans and verify exportable outcomes, Resolve, and Pack return."""
    errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True, executable_path=os.environ.get("SQUARES_BROWSER_EXECUTABLE")
        )
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on(
            "console",
            lambda event: errors.append(event.text) if event.type == "error" else None,
        )
        page.goto(page_path.resolve().as_uri())
        page.locator("#mode-search").click()
        if not page.locator("#search-workspace").is_visible():
            raise ValueError("Search tab did not expose its panel")
        check_keys_stay_in_search(page)
        check_bounded_run(page)
        check_rejected_import(page, check_multi_seed_run(page))
        check_repair_run(page)
        check_cancel(page)
        check_leaving_cancels(page)
        page.locator("#mode-pack").click()
        if not page.locator("#pack-workspace").is_visible():
            raise ValueError("Pack did not return after Search")
        if errors:
            raise ValueError("Search page errors: " + "; ".join(errors))
        browser.close()
    return (
        "bounded, three-seed and Resolve Search runs, summaries, source, rejected imports, "
        "keys kept from the page's shortcuts, Cancel, cancel on leaving, and Pack return"
    )
