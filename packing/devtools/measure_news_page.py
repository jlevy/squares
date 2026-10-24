"""Measure the News page's bytes and load, and project it to a size it has not reached.

`news.html` keeps every story (the owner's "Keep all, raise the limit", 23 October 2026),
so it grows with every S3+ merge, and a raise of its byte budget is set only on this
tool's measurement: the plan of 23 October 2026
(`docs/project/specs/active/plan-2026-10-23-news-pr-feed.md`, The page budget) and
`think-3oxz`. Three modes, from `packing/`:

- `bytes [PAGE...]` needs no browser. For each page, a file or a deployed address, and
  for the page the site's own renderer writes when none is named, it reports the raw
  bytes; the gzip bytes at level 6, the level `preview_site.serve` sends; the brotli bytes
  at quality 11, for reference, since GitHub Pages answered a brotli-only request with the
  uncompressed page, and withheld on a projected page, whose repeated cards brotli's
  window reaches across; for an address, the raw bytes and the gzip transfer size the
  site sent; the stories', the feed rows' and the shell's shares and the 90th-percentile
  story by nearest rank; and the days of room left before the trip point and the budget
  at the story pace of the last 28 days, or of `--pace-days`, read from the page's own
  dated cards, with the earliest story in that window named, since a young page's
  window dilutes the pace. The budget is the one the registry gives `news.html`
  (`site_urls.page_budget`) and the trip point `TRIP_MARGIN` under it, the plan's
  proposed margin; `--budget` and `--trip` set others.
- `project BYTES --out DIR` writes a site directory, `news.html` beside the shared files
  it names (`render_overview.write_site`), whose page is today's with its own story cards
  repeated, in the page's order, under new ids and anchors, until it reaches BYTES. The
  page passes BYTES by less than one story. A BYTES at or below today's size writes
  today's page unchanged, so `project 0 --out DIR` builds the page as `main` renders it.
  `--without SCRIPT`, given a script's name such as `news-cards.js`, leaves that script's
  element out of the page: a control, which says what one script costs at load.
- `load DIR...` measures `news.html` in each directory in Chromium, every protocol
  unchanged from the tool it belongs to: `check_site_rendering DIR --page news.html
  --runs 3` (CLS, LCP, longest task and blocking time at 1280 and 390 px, light and dark,
  and the no-JS readability context); `measure_site_pages load` at both widths,
  unthrottled and over `slow-4g`; Chromium's main-thread counters at load
  (`Performance.getMetrics`, read as `measure_atlas_views move` reads them); and the
  `ParseHTML` total of one traced `check_site_rendering` navigation, a diagnostic with no
  gate credit. The report names the host, its load, the Chromium version and the runs.

A page's verdict is the budget's condition: every `check_site_rendering` limit,
unchanged, on the median of the runs, and the no-JS page readable. A run the checker
could not time, or that raised a page error or a failed request, fails it too, since its
limits were then not measured. Only the checker's count of formulas it cannot see with
scripts on, which the default filter's hidden S3 cards produce, is listed beside it.
Timings on a shared host are advisory, as `results.html`'s exception says of its own.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import os
import platform
import re
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.request
from collections.abc import Sequence
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, NamedTuple

import brotli

from devtools import check_site_rendering, site_urls

if TYPE_CHECKING:
    from playwright.sync_api import Browser

PACKING = Path(__file__).resolve().parents[1]
PAGE = "news.html"
#: The plan's proposed distance from the trip point up to the budget: about ten days of
#: stories at October 2026's pace. A proposal until the owner confirms it.
TRIP_MARGIN = 150_000
#: zlib's level, as `preview_site.serve` compresses a page.
GZIP_LEVEL = 6
#: Brotli's highest quality, a reference figure only.
BROTLI_QUALITY = 11
#: The window the story pace is read over by default, ending on the day of the reading:
#: the plan's last 28 days. `bytes --pace-days` reads another.
PACE_DAYS = 28
#: A story card as `render_changelog.news_card` writes it, `hidden` when it opens
#: filtered out.
_CARD = re.compile(r'<section (?:hidden )?class="site-news-day"')
_SECTION = re.compile(r"<section\b|</section>")
_DAY = re.compile(r'data-news-day="(\d{4}-\d{2}-\d{2})"')
#: A feed row, as the plan's Phase 2 draws one: `<li id="pr-706">` in an `<ol>`. None
#: before Phase 2.
_ROW = re.compile(r'<li id="pr-\d+"')
_LI = re.compile(r"<li\b|</li>")
_ID = re.compile(r'\sid="([^"]+)"')
#: The attributes whose values name an id in the page, and so move with it in a copy.
_REFERENCE = re.compile(
    r'\b(id|for|aria-controls|aria-labelledby|aria-describedby|aria-owns|headers)="([^"]*)"'
)
_LOCAL_HREF = re.compile(r'\bhref="#([^"]*)"')
_ENTRY = re.compile(r'\bdata-news-entry="([^"]*)"')
#: The suffix a copy's ids take, numbered by the round of copies it belongs to.
COPY_SUFFIX = "--projected-{round}"
#: An id a projection gave a copy, which marks the page as projected.
_PROJECTED = re.compile(r'\sid="[^"]*--projected-\d+"')
#: The two widths `check_site_rendering` and `preview_site` lay a page out at.
WIDTHS = (1280, 390)
#: Chromium's counters read at load, as `measure_atlas_views` names them.
COUNTERS = {
    "ScriptDuration": "script_ms",
    "LayoutDuration": "layout_ms",
    "RecalcStyleDuration": "style_ms",
    "TaskDuration": "task_ms",
}
COUNTS = {"LayoutCount": "layouts", "RecalcStyleCount": "style_recalcs"}
#: The `check_site_rendering` problems that are its four limits, judged on the median.
LIMIT_PREFIXES = ("cls ", "lcpMs ", "longestTaskMs ", "blockingMs ")
#: The one problem the checker reports with scripts on that does not decide the verdict:
#: formulas in the S3 cards the default filter hides. The no-JS check reads them all.
LISTED_BESIDE = ("visual mathematics missing",)


class Card(NamedTuple):
    """One story card: where it stands in the page, and its day."""

    start: int
    end: int
    day: date
    bytes: int


class Room(NamedTuple):
    """How far a page is from the trip point and the budget, at its own story pace over
    the `pace_days` days ending on the reading, whose earliest dated story is `earliest`."""

    stories: int
    pace_days: int
    pace_stories: int
    earliest: date | None
    bytes_per_day: float
    days_to_trip: float | None
    days_to_budget: float | None


def _closing(page: str, start: int, tags: re.Pattern[str], closer: str) -> int:
    """The end of the element opened at `start`, counting its own kind's nesting."""
    depth = 0
    for match in tags.finditer(page, start):
        depth += -1 if match.group() == closer else 1
        if depth == 0:
            return match.end()
    raise ValueError(f"an element opened at byte {start} is never closed")


def cards(page: str) -> list[Card]:
    """Every story card in the page, in its order."""
    found: list[Card] = []
    for match in _CARD.finditer(page):
        end = _closing(page, match.start(), _SECTION, "</section>")
        text = page[match.start() : end]
        day = _DAY.search(text)
        if day is None:
            raise ValueError(f"a News card at byte {match.start()} has no data-news-day")
        found.append(
            Card(match.start(), end, date.fromisoformat(day.group(1)), len(text.encode()))
        )
    return found


def row_bytes(page: str) -> int:
    """The feed rows' bytes: none before the plan's Phase 2 draws a feed."""
    return sum(
        len(page[match.start() : _closing(page, match.start(), _LI, "</li>")].encode())
        for match in _ROW.finditer(page)
    )


class Limits(NamedTuple):
    """The byte budget a page is held to, and the trip point under it."""

    budget: int
    trip: int


def registered_limits() -> Limits:
    """`news.html`'s budget as the registry gives it (`site_urls.page_budget`), which
    `check_published_site` holds the page to, and the trip point `TRIP_MARGIN` under it."""
    row = next(row for row in site_urls.load_registry() if row.path == PAGE)
    budget = site_urls.page_budget(row)
    return Limits(budget, budget - TRIP_MARGIN)


def room(page: str, *, as_of: date, limits: Limits, pace_days: int = PACE_DAYS) -> Room:
    """The page's days of room before the trip point and the budget at the pace of the
    stories it dates in the `pace_days` days ending on `as_of`, by default the plan's
    last 28 days. The window's bytes are spread over all its days, so a window that
    starts before the page's first stories reads a slower pace than the page has
    kept since; `earliest` names the first story inside it."""
    if pace_days < 1:
        raise ValueError(f"the pace is read over at least one day, not {pace_days}")
    found = cards(page)
    first = as_of - timedelta(days=pace_days - 1)
    recent = [card for card in found if first <= card.day <= as_of]
    per_day = sum(card.bytes for card in recent) / pace_days
    size = len(page.encode())

    def days(limit: int) -> float | None:
        if size >= limit:
            return 0.0
        return (limit - size) / per_day if per_day else None

    return Room(
        len(found),
        pace_days,
        len(recent),
        min((card.day for card in recent), default=None),
        per_day,
        days(limits.trip),
        days(limits.budget),
    )


def room_line(page: str, *, as_of: date, limits: Limits, pace_days: int = PACE_DAYS) -> str:
    """One line: the page's bytes, the trip point, the budget and the days of room."""
    found = room(page, as_of=as_of, limits=limits, pace_days=pace_days)
    if found.days_to_trip is None or found.days_to_budget is None:
        pace = f"no story dated in the {pace_days} days to {as_of}, so no pace to project"
    else:
        pace = (
            f"about {found.days_to_trip:.0f} days of room before the trip point and "
            f"{found.days_to_budget:.0f} before the budget at the last {pace_days} days' "
            f"pace ({found.pace_stories} stories, the earliest dated {found.earliest}, "
            f"{found.bytes_per_day:,.0f} bytes a day)"
        )
    return (
        f"{len(page.encode()):,} bytes over {found.stories} stories; trip point "
        f"{limits.trip:,}, budget {limits.budget:,}; {pace}"
    )


def rendered_page() -> str:
    """`news.html` as the site build writes it: `render_overview.news_page`, with the
    GitHub links `render_overview.write_site` decorates (`decorate_github_links`)."""
    from devtools import render_overview  # noqa: PLC0415
    from devtools.site_github_links import decorate_github_links  # noqa: PLC0415

    return decorate_github_links(render_overview.news_page().html)


def nearest_rank(sizes: Sequence[int], share: float) -> int:
    """The `share` percentile of `sizes` by nearest rank: the smallest size at or above
    that share of them, `sorted(sizes)[ceil(share * n) - 1]`."""
    if not sizes:
        raise ValueError("no size to rank")
    return sorted(sizes)[max(math.ceil(share * len(sizes)), 1) - 1]


def projected(page: str) -> bool:
    """Whether `page` carries a projection's copies."""
    return _PROJECTED.search(page) is not None


def gzip_bytes(data: bytes) -> int:
    return len(gzip.compress(data, compresslevel=GZIP_LEVEL, mtime=0))


def brotli_bytes(data: bytes) -> int:
    return len(brotli.compress(data, quality=BROTLI_QUALITY))


def fetch(address: str) -> tuple[bytes, int, str]:
    """A deployed page as its site sends it to a reader accepting gzip: the raw bytes,
    the bytes sent, and the content encoding."""
    if not address.startswith("https://"):
        raise ValueError(f"a deployed page is an https address: {address}")
    request = urllib.request.Request(address, headers={"Accept-Encoding": "gzip"})
    with urllib.request.urlopen(request, timeout=30) as response:
        sent = response.read()
        encoding = response.headers.get("Content-Encoding", "identity")
    raw = gzip.decompress(sent) if encoding == "gzip" else sent
    return raw, len(sent), encoding


def byte_report(
    page: str,
    *,
    name: str,
    as_of: date,
    limits: Limits,
    pace_days: int = PACE_DAYS,
    sent: tuple[int, str] | None = None,
) -> dict[str, Any]:
    """The `bytes` mode's report on one page. On a projected page the brotli size is
    withheld: quality 11's window reaches across the repeated cards, so it measures the
    repetition, not the stories. Gzip's 32 KB window does not, so its size stands."""
    data = page.encode()
    found = cards(page)
    sizes = sorted(card.bytes for card in found)
    stories = sum(sizes)
    rows = row_bytes(page)
    shell = len(data) - stories - rows
    space = room(page, as_of=as_of, limits=limits, pace_days=pace_days)
    copies = projected(page)
    report: dict[str, Any] = {
        "page": name,
        "raw_bytes": len(data),
        "gzip_bytes": gzip_bytes(data),
        "gzip_level": GZIP_LEVEL,
        "brotli_bytes": None if copies else brotli_bytes(data),
        "brotli_quality": BROTLI_QUALITY,
        "stories": len(found),
        "story_bytes": stories,
        "row_bytes": rows,
        "shell_bytes": shell,
        "story_share": round(stories / len(data), 4),
        "row_share": round(rows / len(data), 4),
        "shell_share": round(shell / len(data), 4),
        "story_mean_bytes": round(stories / len(found)) if found else None,
        "story_p90_bytes": nearest_rank(sizes, 0.9) if sizes else None,
        "story_p90_rule": "nearest rank",
        "as_of": as_of.isoformat(),
        "pace_days": space.pace_days,
        "pace_stories": space.pace_stories,
        "pace_earliest_story": None if space.earliest is None else space.earliest.isoformat(),
        "pace_bytes_per_day": round(space.bytes_per_day),
        "trip_bytes": limits.trip,
        "budget_bytes": limits.budget,
        "days_to_trip": None if space.days_to_trip is None else round(space.days_to_trip, 1),
        "days_to_budget": (
            None if space.days_to_budget is None else round(space.days_to_budget, 1)
        ),
    }
    if copies:
        report["brotli_withheld"] = (
            "a projected page: brotli's window reaches across its repeated cards"
        )
    if sent is not None:
        report["sent_bytes"], report["sent_encoding"] = sent
    return report


def _renamed(card: str, suffix: str) -> str:
    """A card's copy, every id it defines and every reference to one of them renamed."""
    names = {name: name + suffix for name in _ID.findall(card)}

    def attribute(match: re.Match[str]) -> str:
        values = " ".join(names.get(value, value) for value in match.group(2).split(" "))
        return f'{match.group(1)}="{values}"'

    copy = _REFERENCE.sub(attribute, card)
    copy = _LOCAL_HREF.sub(lambda match: f'href="#{names.get(match[1], match[1])}"', copy)
    return _ENTRY.sub(lambda match: f'data-news-entry="{match[1]}{suffix}"', copy)


class Projection(NamedTuple):
    page: str
    stories_added: int
    rounds: int


def project_page(page: str, target: int) -> Projection:
    """`page` grown to `target` bytes from its own cards alone: each card repeated in
    the page's order, round after round, under new ids and anchors, ahead of the first
    card, where a newer story stands. The page passes `target` by less than the last
    card added; at or above `target` already, it is returned unchanged."""
    found = cards(page)
    if not found:
        raise ValueError("the page has no News card to repeat")
    size = len(page.encode())
    copies: list[str] = []
    rounds = 0
    while size < target:
        rounds += 1
        suffix = COPY_SUFFIX.format(round=rounds)
        for card in found:
            copy = _renamed(page[card.start : card.end], suffix) + "\n"
            copies.append(copy)
            size += len(copy.encode())
            if size >= target:
                break
    first = found[0].start
    return Projection(page[:first] + "".join(copies) + page[first:], len(copies), rounds)


def without_scripts(page: str, names: Sequence[str]) -> str:
    """`page` with the element of each named script left out, a script named by its
    file, `news-cards.js`, as the site writes it content-hashed under `assets/js/`."""
    for name in names:
        stem = name.removesuffix(".js")
        element = re.compile(
            rf'<script\b[^>]*\bsrc="(?:[^"]*/)?{re.escape(stem)}(?:\.[0-9a-f]+)?\.js"'
            r"[^>]*></script>\n?"
        )
        page, count = element.subn("", page)
        if count != 1:
            raise ValueError(f"the page has {count} elements for the script {name}, not 1")
    return page


def write_projection(page: str, out: Path) -> None:
    """A site directory holding `page` as `news.html`, with the shared files it names."""
    from devtools import render_overview  # noqa: PLC0415

    if out.exists() and any(out.iterdir()):
        raise ValueError(f"{out} is not empty; `project` writes a directory of its own")
    render_overview.write_site(out, [render_overview.Page(PAGE, page)])


def _counters(client: Any) -> dict[str, float]:
    metrics = client.send("Performance.getMetrics")["metrics"]
    found = {metric["name"]: metric["value"] for metric in metrics}
    report = {label: round(found[name] * 1000, 1) for name, label in COUNTERS.items()}
    report.update({label: round(found[name]) for name, label in COUNTS.items()})
    return report


def load_counters(browser: Browser, url: str, *, width: int) -> dict[str, float]:
    """Chromium's main-thread counters over one load, in a fresh context: script, layout,
    style and task time in milliseconds of the thread's own clock, and the layouts and
    style recalculations it made, read once the fonts have settled."""
    context = browser.new_context(viewport={"width": width, "height": 900})
    try:
        page = context.new_page()
        client = context.new_cdp_session(page)
        client.send("Performance.enable", {"timeDomain": "threadTicks"})
        response = page.goto(url, wait_until="load", timeout=30_000)
        if response is None or not response.ok:
            raise ValueError(f"navigation failed: {url}")
        check_site_rendering.wait_for_fonts(page)
        page.wait_for_timeout(check_site_rendering.SETTLE_MS)
        return _counters(client)
    finally:
        context.close()


def _median_counters(samples: Sequence[dict[str, float]]) -> dict[str, float]:
    return {key: statistics.median(sample[key] for sample in samples) for key in samples[0]}


def parse_html_ms(browser: Browser, url: str) -> dict[str, Any]:
    """The `ParseHTML` phase of one traced navigation at 1280 px, light, a diagnostic
    with the tracing's own overhead and no gate credit."""
    with tempfile.TemporaryDirectory() as scratch:
        trace = Path(scratch) / "trace.json"
        check_site_rendering.measure(browser, url, width=1280, scheme="light", trace=trace)
        summary = json.loads(trace.read_text(encoding="utf-8"))["summary"]
    phase = summary["phases"].get("ParseHTML", {})
    return {
        "parse_html_ms": round(phase.get("inclusive_ms", 0.0), 1),
        "parse_html_slices": phase.get("count", 0),
        "longest_parse_html_ms": round(phase.get("max_ms", 0.0), 1),
        "credit": summary["interpretation"],
    }


def rendering(directory: Path, runs: int) -> dict[str, Any]:
    """`check_site_rendering DIR --page news.html --runs RUNS`, as its CLI runs it."""
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "devtools.check_site_rendering",
            str(directory),
            "--page",
            PAGE,
            "--runs",
            str(runs),
        ],
        cwd=PACKING,
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"check_site_rendering printed no report (exit {completed.returncode}): "
            f"{completed.stderr.strip()[-2000:]}"
        ) from error
    report["exit"] = completed.returncode
    return report


def verdict(report: dict[str, Any]) -> dict[str, Any]:
    """Whether a `check_site_rendering` report meets the budget's condition: its four
    limits on the medians, unchanged, and the no-JS page readable. A run the checker
    could not time, or one with a page error or a failed request, fails it as well,
    since the limits were then not all measured. Only `LISTED_BESIDE` is listed beside
    the verdict without deciding it."""
    limits: list[str] = []
    static: list[str] = []
    runs: list[str] = []
    other: list[str] = []
    for failure in report["failures"]:
        problem = failure.split(": ", 1)[-1]
        if " no-JS " in failure:
            static.append(failure)
        elif problem.startswith(LIMIT_PREFIXES):
            limits.append(failure)
        elif problem in LISTED_BESIDE:
            other.append(failure)
        else:
            runs.append(failure)
    worst = {
        key: max(row[key] for row in report["pages"])
        for key in ("cls", "lcpMs", "longestTaskMs", "blockingMs")
    }
    return {
        "passes": not limits and not static and not runs,
        "limit_failures": limits,
        "no_js_failures": static,
        "run_failures": sorted(set(runs)),
        "other_findings": sorted(set(other)),
        "worst_medians": worst,
        "timing_exceedances": report.get("timing_exceedances", []),
    }


def _shifts(sample: dict[str, Any]) -> list[dict[str, Any]]:
    """A run's layout shifts, each with its time, its score and the nodes that moved,
    and the run's font events, which the shifts are read against."""
    return [
        {
            "ms": round(shift["startTime"]),
            "value": round(shift["value"], 4),
            "sources": [source["node"] for source in shift["sources"]],
        }
        for shift in sample.get("layoutShifts", [])
    ] + [
        {"ms": round(event["startTime"]), "font": event["type"]}
        for event in sample.get("fontEvents", [])
    ]


def host() -> dict[str, Any]:
    """The machine a reading was taken on, which a shared host's timings depend on."""
    return {
        "node": platform.node(),
        "platform": platform.platform(),
        "cpus": os.cpu_count(),
        "load_average": [round(value, 2) for value in os.getloadavg()],
    }


def measure_directory(directory: Path, *, runs: int) -> dict[str, Any]:
    """Every `load` reading of `news.html` in one built site directory."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    from devtools import measure_site_pages  # noqa: PLC0415
    from devtools.preview_site import launch_chromium, serve  # noqa: PLC0415

    page = (directory / PAGE).read_text(encoding="utf-8")
    started = time.monotonic()
    report: dict[str, Any] = {
        "directory": str(directory),
        "raw_bytes": len(page.encode()),
        "gzip_bytes": gzip_bytes(page.encode()),
        "stories": len(cards(page)),
        "host_before": host(),
    }
    checked = rendering(directory, runs)
    report["check_site_rendering"] = {
        "protocol": checked["protocol"],
        "scenarios": [
            {
                key: row[key]
                for key in ("width", "scheme", "cls", "lcpMs", "longestTaskMs", "blockingMs")
            }
            | {
                "sample_cls": [sample["cls"] for sample in row["samples"]],
                "no_js_heading": row["static"].get("heading"),
                "no_js_content_chars": row["static"].get("contentChars"),
                "no_js_unreadable_math": row["static"].get("unreadableMath"),
                "shown_math": row["samples"][0].get("shownMath"),
                "unreadable_math": row["samples"][0].get("unreadableMath"),
                "worst_run_shifts": _shifts(max(row["samples"], key=lambda run: run["cls"])),
            }
            for row in checked["pages"]
        ],
        "failures": checked["failures"],
        "exit": checked["exit"],
    }
    report["verdict"] = verdict(checked)
    server = serve(directory, 0, as_pages=True)
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        report["loads"] = [
            row
            for network in (None, "slow-4g")
            for row in measure_site_pages.measure_load(
                base, [PAGE], widths=WIDTHS, runs=runs, network=network
            )
        ]
        with sync_playwright() as driver:
            browser = launch_chromium(driver)
            try:
                report["chromium"] = browser.version
                report["counters"] = [
                    {"width": width}
                    | _median_counters(
                        [
                            load_counters(browser, f"{base}/{PAGE}", width=width)
                            for _ in range(runs)
                        ]
                    )
                    for width in WIDTHS
                ]
                report["parse_html"] = parse_html_ms(browser, f"{base}/{PAGE}")
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    # Rendering: 4 scenarios x (runs + 1 no-JS); loads: 2 widths x runs x 2 networks;
    # counters: 2 widths x runs; one traced navigation.
    report["navigations"] = 4 * (runs + 1) + 4 * runs + 2 * runs + 1
    report["wall_seconds"] = round(time.monotonic() - started, 1)
    report["host_after"] = host()
    return report


def markdown(reports: Sequence[dict[str, Any]]) -> str:
    """The `load` report as the tables a pull request carries."""
    lines = [
        (
            "| Page | Raw | Gzip | Stories | Worst median CLS | LCP ms | Longest task ms "
            "| Blocking ms | No-JS readable | Passes |"
        ),
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for report in reports:
        worst = report["verdict"]["worst_medians"]
        lines.append(
            f"| {report['directory']} | {report['raw_bytes']:,} | {report['gzip_bytes']:,} "
            f"| {report['stories']} | {worst['cls']:.3f} | {worst['lcpMs']:.0f} "
            f"| {worst['longestTaskMs']:.0f} | {worst['blockingMs']:.0f} "
            f"| {'yes' if not report['verdict']['no_js_failures'] else 'no'} "
            f"| {'yes' if report['verdict']['passes'] else 'no'} |"
        )
    lines += [
        "",
        "| Page | Width | Scheme | CLS | LCP ms | Longest task ms | Blocking ms | CLS runs |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for report in reports:
        for row in report["check_site_rendering"]["scenarios"]:
            runs = ", ".join(f"{value:.3f}" for value in row["sample_cls"])
            lines.append(
                f"| {report['directory']} | {row['width']} | {row['scheme']} "
                f"| {row['cls']:.3f} | {row['lcpMs']:.0f} | {row['longestTaskMs']:.0f} "
                f"| {row['blockingMs']:.0f} | {runs} |"
            )
    lines += [
        "",
        "| Page | Width | Network | DCL ms | Load ms | FCP ms | Transfer bytes |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for report in reports:
        for row in report["loads"]:
            lines.append(
                f"| {report['directory']} | {row['width']} | {row['network'] or 'local'} "
                f"| {row['dcl_ms']:.0f} | {row['load_ms']:.0f} | {row['fcp_ms']:.0f} "
                f"| {row['transfer_bytes']:,.0f} |"
            )
    lines += [
        "",
        (
            "| Page | Width | Script ms | Layout ms | Style ms | Task ms | Layouts "
            "| Style recalcs | ParseHTML ms (traced, 1280) |"
        ),
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for report in reports:
        for row in report["counters"]:
            lines.append(
                f"| {report['directory']} | {row['width']} | {row['script_ms']:.0f} "
                f"| {row['layout_ms']:.0f} | {row['style_ms']:.0f} | {row['task_ms']:.0f} "
                f"| {row['layouts']:.0f} | {row['style_recalcs']:.0f} "
                f"| {report['parse_html']['parse_html_ms']:.0f} |"
            )
    return "\n".join(lines)


def _today() -> date:
    return datetime.now(UTC).date()


def _bytes_mode(args: argparse.Namespace) -> None:
    as_of = args.as_of or _today()
    pace_days = args.pace_days
    registered = registered_limits()
    budget = args.budget or registered.budget
    limits = Limits(budget, args.trip or budget - TRIP_MARGIN)
    pages: list[tuple[str, str, tuple[int, str] | None]] = []
    for name in args.page or ["rendered"]:
        if name == "rendered":
            pages.append((name, rendered_page(), None))
        elif name.startswith(("http://", "https://")):
            raw, sent, encoding = fetch(name)
            pages.append((name, raw.decode(), (sent, encoding)))
        else:
            pages.append((name, Path(name).read_text(encoding="utf-8"), None))
    if args.markdown:
        for name, text, _sent in pages:
            line = room_line(text, as_of=as_of, limits=limits, pace_days=pace_days)
            print(f"{name}: {line}")
        return
    reports = [
        byte_report(text, name=name, as_of=as_of, limits=limits, pace_days=pace_days, sent=sent)
        for name, text, sent in pages
    ]
    json.dump(reports, sys.stdout, indent=2)
    print()


def _project_mode(args: argparse.Namespace) -> None:
    today = rendered_page()
    projection = project_page(today, args.target)
    written = without_scripts(projection.page, args.without)
    write_projection(written, args.out)
    report = {
        "out": str(args.out / PAGE),
        "target_bytes": args.target,
        "today_bytes": len(today.encode()),
        "today_stories": len(cards(today)),
        "raw_bytes": len(written.encode()),
        "stories": len(cards(written)),
        "stories_added": projection.stories_added,
        "rounds": projection.rounds,
        "without": args.without,
    }
    print(json.dumps(report, indent=2))


def _load_mode(args: argparse.Namespace) -> int:
    reports = [measure_directory(path, runs=args.runs) for path in args.directory]
    if args.markdown:
        print(markdown(reports))
    else:
        json.dump(reports, sys.stdout, indent=2)
        print()
    return 0 if all(report["verdict"]["passes"] for report in reports) else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    modes = parser.add_subparsers(dest="mode", required=True)
    sizes = modes.add_parser("bytes", help="bytes, compression, shares and room; no browser")
    sizes.add_argument(
        "page",
        nargs="*",
        help="a built news.html, a deployed https address, or `rendered`, the page the "
        "site's renderer writes now, which is the default",
    )
    sizes.add_argument(
        "--as-of",
        type=date.fromisoformat,
        default=None,
        help="the day the story pace is read to, today (UTC) by default",
    )
    sizes.add_argument(
        "--budget", type=int, help="the budget, the registry's for news.html by default"
    )
    sizes.add_argument(
        "--trip", type=int, help=f"the trip point, {TRIP_MARGIN:,} under the budget by default"
    )
    sizes.add_argument(
        "--pace-days",
        type=int,
        default=PACE_DAYS,
        metavar="N",
        help=f"read the story pace over the N days to --as-of, {PACE_DAYS} by default",
    )
    sizes.add_argument(
        "--markdown", action="store_true", help="print each page's room line, not JSON"
    )
    grow = modes.add_parser("project", help="write today's page grown to BYTES")
    grow.add_argument("target", type=int, metavar="BYTES")
    grow.add_argument("--out", type=Path, required=True, metavar="DIR")
    grow.add_argument(
        "--without",
        action="append",
        default=[],
        metavar="SCRIPT",
        help="leave this script, such as news-cards.js, out of the page, as a control",
    )
    loads = modes.add_parser("load", help="measure news.html in each built directory")
    loads.add_argument("directory", type=Path, nargs="+", metavar="DIR")
    loads.add_argument("--runs", type=int, default=3)
    loads.add_argument("--markdown", action="store_true", help="print tables, not JSON")
    args = parser.parse_args(argv)
    if args.mode == "load" and args.runs < 1:
        parser.error("--runs must be positive")
    if args.mode == "bytes" and args.pace_days < 1:
        parser.error("--pace-days must be positive")
    try:
        if args.mode == "bytes":
            _bytes_mode(args)
        elif args.mode == "project":
            _project_mode(args)
        else:
            return _load_mode(args)
    except (OSError, ValueError) as error:
        print(f"measure_news_page: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
