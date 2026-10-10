"""Permanent published URL registrations, producer validation and deterministic crawl files.

Builders declare outputs; the register retains addresses and semantic result identity.
Partial builds must name producers. Missing files never imply a partial build.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import re
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, replace
from datetime import date
from html import escape
from pathlib import Path, PurePosixPath
from typing import Any, cast
from urllib.parse import urlsplit
from xml.etree.ElementTree import Element, SubElement, tostring

import yaml
from strif import atomic_output_file

from sqpack.yamlio import load_yaml

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
REGISTRY = PACKING / "site-urls.yaml"
DOCUMENT = REPO / "docs/project/site-urls.md"
FIRST_SITE_DATE = "2026-09-29"
# The declared registration day for this URL migration, never the render clock.
REGISTRATION_DATE = "2026-10-08"
HARD_HTML_LIMIT = 2_000_000
# Measured exceptions retain the global two-megabyte ceiling.
PAGE_BUDGET_EXCEPTIONS: dict[str, tuple[int, str]] = {
    "index.html": (
        1_300_000,
        (
            "The native 324-case Atlas payload, six-row preview and shared reading "
            "and documentation cards measure 1,172,462 bytes. Three-run loopback load "
            "medians are 274 ms at 1280 px and 261 ms at 390 px; retained staged "
            "expansion checks cover the embedded preview. "
            "The page-specific ceiling remains below the global two-megabyte limit."
        ),
    ),
    "papers/n11-threshold-bound-review.html": (
        900_000,
        (
            "The 401-formula review measures 823,322 bytes after sharing font geometry. "
            "Its 842,245-byte edition passed three-run desktop/mobile, light/dark and "
            "no-JS checks with CLS ≤0.050 and LCP ≤836 ms. The ceiling leaves "
            "headroom above the measured edition."
        ),
    ),
    "cases/11.html": (
        500_000,
        "Complete n=11 proof/certificate record and prepared bounds measure 416,870 bytes.",
    ),
    "cases/17.html": (
        500_000,
        "Complete n=17 proof/certificate record and prepared bounds measure 443,761 bytes.",
    ),
    "cases/18.html": (
        350_000,
        "Complete n=18 certificate record; prepared HTML measures 326,548 bytes.",
    ),
    "result/t-007.html": (
        800_000,
        "Complete broad scope history and prepared exact bounds measure 711,115 bytes.",
    ),
    "result/t-085.html": (
        800_000,
        "Complete broad scope history and prepared exact bounds measure 694,374 bytes.",
    ),
    "result/t-083.html": (
        800_000,
        "Complete broad scope history and prepared exact bounds measure 688,505 bytes.",
    ),
    "result/t-058.html": (
        600_000,
        "Complete broad scope history and prepared exact bounds measure 509,332 bytes.",
    ),
    "result/t-046.html": (
        400_000,
        "Complete broad scope history and prepared exact bounds measure 355,078 bytes.",
    ),
    "atlas.html": (
        1_000_000,
        (
            "Combined 324-case Atlas measures 862,357 bytes: 688,112 for the complete "
            "Frontier Survey and 174,245 for graphics and the shared shell."
        ),
    ),
    "all-results.html": (
        800_000,
        "The complete registered-result table with prepared math measures 717,328 bytes.",
    ),
    "tutorial.html": (
        800_000,
        "The complete authored tutorial and prepared formulas measure 742,713 bytes.",
    ),
    "papers/n11-lower-bounds-explainer.html": (
        1_500_000,
        (
            "Four prepared font preferences and the authored paper content "
            "measure 1,417,498 bytes."
        ),
    ),
}
PAGE_BUDGETS = {
    "page": 600_000,
    "record": 300_000,
    "result": 300_000,
    "paper": 800_000,
    "workbench": 600_000,
}
FOOTER = (
    "<!-- This document follows common-doc-guidelines.md.\n"
    "See github.com/jlevy/practical-prose and review guidelines before editing.\n-->\n"
)
KINDS = frozenset(
    {"page", "record", "result", "paper-file", "forwarder", "copy", "asset-file", "site-file"}
)
STATUSES = frozenset({"live", "forwarded", "withdrawn"})
HASHED_ASSET_PATTERN = (
    r"assets/(?:css/[a-zA-Z0-9_-]+\.[0-9a-f]{16}\.css"
    r"|js/[a-zA-Z0-9_-]+\.[0-9a-f]{16}\.js"
    r"|fonts/[a-zA-Z0-9_-]+\.[0-9a-f]{16}\.woff2)"
)
WORKBENCH_ASSET_PATTERN = "workbench/" + HASHED_ASSET_PATTERN
WORKBENCH_DATA_PATTERN = r"workbench/data/corpus\.[0-9a-f]{16}\.json"
ALLOWED_PATTERNS = frozenset(
    {HASHED_ASSET_PATTERN, WORKBENCH_ASSET_PATTERN, WORKBENCH_DATA_PATTERN}
)
Checks = list[tuple[bool, str]]


@dataclass(frozen=True)
class SiteURL:
    """A physical output path, separate from the address readers and crawlers use."""

    path: str
    canonical: str
    kind: str
    generator: str
    producer: str
    first_published: str
    lastmod: str
    status: str = "live"
    target: str = ""
    tombstone: str = ""
    pattern: str = ""
    identity: dict[str, Any] | None = None
    amendments: tuple[dict[str, Any], ...] = ()


def canonical_path(path: str) -> str:
    return (
        path.removesuffix("index.html")
        if path == "index.html" or path.endswith("/index.html")
        else path
    )


def site_url() -> str:
    from devtools.render_overview import SITE_URL  # noqa: PLC0415

    return SITE_URL


def _valid_path(path: str, *, canonical: bool = False) -> bool:
    if not path and canonical:
        return True
    return (
        bool(path)
        and not path.startswith("/")
        and not any(character in path for character in "\\?#\x00")
        and all(part not in ("", ".", "..") for part in path.removesuffix("/").split("/"))
        and PurePosixPath(path).as_posix() == path.removesuffix("/")
    )


def _date(value: str) -> bool:
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def result_identity(record: Mapping[str, Any]) -> dict[str, Any]:
    """Bind an ID to claim scope and source publication, allowing wording corrections.

    Evidence and artifact IDs identify the work, not bytes of its evolving files.
    Confidence, headline, notes and review ratings are deliberately absent.
    """
    return {
        key: record.get(key)
        for key in (
            "kind",
            "scope",
            "established",
            "attribution",
            "builds_on",
            "evidence",
            "artifacts",
        )
    }


def hashed_asset_rows(day: str) -> list[SiteURL]:
    return [
        SiteURL(
            "assets/{css,js,fonts}/*.{hash}.{ext}",
            "",
            "asset-file",
            "devtools.site_assets:shared",
            "shared",
            day,
            day,
            pattern=HASHED_ASSET_PATTERN,
        )
    ]


def _result_dates(record: Mapping[str, Any]) -> tuple[str, str]:
    registered = str(record["registered"])
    return registered, max(
        [registered, *(str(change["date"]) for change in record.get("amendments", []))]
    )


def _new_row(
    path: str,
    kind: str,
    producer: str,
    generator: str,
    *,
    first: str = REGISTRATION_DATE,
    lastmod: str,
    target: str = "",
    identity: dict[str, Any] | None = None,
) -> SiteURL:
    return SiteURL(
        path,
        canonical_path(target or path),
        kind,
        generator,
        producer,
        first,
        lastmod,
        status="forwarded" if kind == "forwarder" else "live",
        target=target,
        identity=identity,
    )


def derive_registry(previous: Sequence[SiteURL] | None = None) -> list[SiteURL]:
    """Builder declarations and retained registrations, without rendering site pages."""
    from devtools import (  # noqa: PLC0415
        overview_data,
        paper_front,
        render_overview,
        site_documents,
    )
    from devtools.check_source_coverage import scope_contains  # noqa: PLC0415
    from devtools.render_n11_lower_bounds_explainer import COMPOSITE_ASSETS  # noqa: PLC0415
    from devtools.render_research_tables import load_cases  # noqa: PLC0415
    from sqpack.release import PUBLICATION_DATE  # noqa: PLC0415

    day = paper_front.iso_date(PUBLICATION_DATE)
    records = cast(
        dict[str, Any], load_yaml(overview_data.RESULTS.read_text(encoding="utf-8"))
    )["results"]
    rows = [
        _new_row(path, "page", "overview", "devtools.render_overview:render_all", lastmod=day)
        for path in render_overview.PAGES
    ]
    for record in records:
        first, revised = _result_dates(record)
        rows.append(
            _new_row(
                f"result/{record['id'].lower()}.html",
                "result",
                "overview",
                "devtools.render_overview:result_fragments",
                first=first,
                lastmod=revised,
                identity=result_identity(record),
            )
        )
    for case in load_cases():
        n = case["n"]
        dates = [str(case.get("source_reviewed", FIRST_SITE_DATE))]
        dates.extend(
            _result_dates(record)[1] for record in records if scope_contains(record["scope"], n)
        )
        rows.append(
            _new_row(
                f"cases/{n}.html",
                "record",
                "overview",
                "devtools.render_case_pages:case_records",
                first=REGISTRATION_DATE,
                lastmod=max(dates),
            )
        )
    for paper in render_overview.PAPERS:
        front = importlib.import_module(paper.module).FRONT
        first = paper_front.iso_date(front.dates[0].day)
        revised = paper_front.iso_date(paper_front.revised(front))
        for extension in (".html", ".md", ".pdf"):
            rows.append(  # noqa: PERF401 -- each output has its own registration
                _new_row(
                    render_overview.paper_path(paper.slug, extension),
                    "paper-file",
                    "paper:" + paper.slug,
                    paper.module + ":main",
                    first=first,
                    lastmod=revised,
                )
            )
    rows += [
        _new_row(
            old,
            "forwarder",
            "overview",
            "devtools.render_overview:forwarder_pages",
            lastmod=day,
            target=new,
        )
        for old, new in render_overview.MOVED_PAGES
    ]
    rows += [
        _new_row(
            old,
            "copy",
            "assembly",
            "devtools.preview_site:copy_moved_files",
            lastmod=day,
            target=new,
        )
        for old, new in render_overview.MOVED_FILES
    ]
    rows += [
        _new_row(
            path.name,
            "asset-file",
            "paper:" + render_overview.N11_LOWER_BOUNDS_EXPLAINER,
            "devtools.render_n11_lower_bounds_explainer:write",
            lastmod=day,
        )
        for path in COMPOSITE_ASSETS
    ]
    rows.append(
        _new_row(
            render_overview.SOCIAL_CARD,
            "asset-file",
            "overview",
            "devtools.social_card:write",
            lastmod=day,
        )
    )
    rows.append(
        _new_row(
            "workbench/index.html",
            "page",
            "workbench",
            "devtools.build_site:build",
            lastmod=day,
        )
    )
    rows += hashed_asset_rows(day)
    rows += [
        SiteURL(
            "workbench/assets/{css,js,fonts}/*.{hash}.{ext}",
            "",
            "asset-file",
            "devtools.build_site:build",
            "workbench",
            REGISTRATION_DATE,
            day,
            pattern=WORKBENCH_ASSET_PATTERN,
        ),
        SiteURL(
            "workbench/data/corpus.{hash}.json",
            "",
            "asset-file",
            "devtools.build_site:build",
            "workbench",
            REGISTRATION_DATE,
            day,
            pattern=WORKBENCH_DATA_PATTERN,
        ),
    ]
    for path in ("404.html", "sitemap.xml"):
        rows.append(
            _new_row(
                path,
                "site-file",
                "overview",
                "devtools.site_urls:write_crawl_files",
                lastmod=day,
            )
        )
    if paths := getattr(render_overview, "support_file_paths", None):
        rows += [
            _new_row(
                path,
                "asset-file",
                "overview",
                "devtools.render_overview:support_files",
                lastmod=day,
            )
            for path in paths()
        ]
    if chapters := getattr(site_documents, "chapter_names", None):
        rows += [
            _new_row(
                path, "page", "overview", "devtools.site_documents:chapter_pages", lastmod=day
            )
            for path in chapters()
        ]
    retained = {row.path: row for row in previous or ()}
    current: dict[str, SiteURL] = {}
    for declared in rows:
        row = declared
        if row.path in current:
            raise ValueError(f"duplicate builder URL: {row.path}")
        if old := retained.pop(row.path, None):
            row = replace(row, first_published=old.first_published, amendments=old.amendments)
            if row.amendments:
                row = replace(
                    row,
                    lastmod=max(
                        row.lastmod, *(str(change["date"]) for change in row.amendments)
                    ),
                )
        current[row.path] = replace(row, lastmod=max(row.lastmod, row.first_published))
    for old in retained.values():
        if old.status == "live":
            raise ValueError(
                f"removed live URL {old.path}: retain a forwarder or a withdrawn tombstone"
            )
        current[old.path] = old
    result = sorted(current.values(), key=lambda row: row.path)
    _require_valid(result)
    if previous is not None:
        failed = [message for passed, message in check_history(result, previous) if not passed]
        if failed:
            raise ValueError("\n".join(failed))
    return result


def _parse_row(record: dict[str, Any]) -> SiteURL:
    return SiteURL(**{**record, "amendments": tuple(record.get("amendments", []))})


def load_registry(path: Path = REGISTRY) -> list[SiteURL]:
    document = cast(dict[str, Any], load_yaml(path.read_text(encoding="utf-8")))
    if document.get("version") != 1:
        raise ValueError("site URL registry version must be 1")
    rows = [_parse_row(row) for row in document["urls"]]
    _require_valid(rows)
    return rows


def render_registry(rows: Sequence[SiteURL]) -> str:
    records = []
    for row in rows:
        record = asdict(row)
        records.append(
            {
                key: value
                for key, value in record.items()
                if key == "canonical" or value not in ("", None, ())
            }
        )
    return (
        "# Generated by devtools.site_urls; retain withdrawn URLs and dated amendments.\n"
        + yaml.safe_dump(
            {"version": 1, "urls": records}, allow_unicode=True, sort_keys=False, width=96
        )
    )


def render_document(rows: Sequence[SiteURL]) -> str:
    lines = [
        "# Published Site URLs",
        "",
        (
            "Generated from builder declarations and the "
            "[URL register](../../packing/site-urls.yaml)."
        ),
        (
            "See [The Published Site](../../development.md#the-published-site) "
            "for changes and validation."
        ),
        "",
        "Physical paths identify output files. Canonical paths identify reader addresses.",
        "Patterns admit declared namespaces, file types and sixteen-digit asset names.",
        "",
        (
            "| Physical path | Canonical path | Kind | Producer | First published | "
            "Last modified | Status / target |"
        ),
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        status = row.status + (" → " + row.target if row.target else "")
        cells = (
            row.path,
            row.canonical or ("—" if row.pattern else "/"),
            row.kind,
            row.producer,
            row.first_published,
            row.lastmod,
            status,
        )
        lines.append("| " + " | ".join(cell.replace("|", r"\|") for cell in cells) + " |")
    lines += ["", "## HTML Byte Budgets", "", "| Family | Bytes |", "| --- | ---: |"]
    lines += [f"| {family} | {limit:,} |" for family, limit in PAGE_BUDGETS.items()]
    lines += [f"| Every HTML file, hard limit | {HARD_HTML_LIMIT:,} |", ""]
    lines += [
        "### Measured exceptions",
        "",
        "| Physical path | Bytes | Reason |",
        "| --- | ---: | --- |",
    ]
    lines += [
        f"| {path} | {limit:,} | {reason} |"
        for path, (limit, reason) in sorted(PAGE_BUDGET_EXCEPTIONS.items())
    ]
    lines += ["", FOOTER.rstrip(), ""]
    return "\n".join(lines)


def _target_path(target: str) -> str:
    return (
        target.removesuffix("/") + "/index.html"
        if target.endswith("/")
        else target or "index.html"
    )


def validate_registry(rows: Sequence[SiteURL]) -> Checks:
    checks: Checks = [
        (
            0 < limit <= HARD_HTML_LIMIT and bool(reason.strip()),
            f"budget exception {path}: measured reason and ceiling within hard limit",
        )
        for path, (limit, reason) in PAGE_BUDGET_EXCEPTIONS.items()
    ]
    paths = {row.path: row for row in rows}
    checks.append((len(paths) == len(rows), "registry: unique physical paths"))
    for row in rows:
        valid = (
            row.kind in KINDS
            and row.status in STATUSES
            and bool(row.generator)
            and bool(row.producer)
        )
        valid = (
            valid
            and _date(row.first_published)
            and _date(row.lastmod)
            and row.first_published <= row.lastmod
        )
        if row.pattern:
            valid = (
                valid
                and row.kind == "asset-file"
                and row.pattern in ALLOWED_PATTERNS
                and row.status == "live"
            )
        else:
            valid = valid and _valid_path(row.path)
        valid = valid and (
            row.canonical.startswith("https://") or _valid_path(row.canonical, canonical=True)
        )
        checks.append(
            (
                valid,
                f"registry {row.path}: valid path, producer, dates and constrained pattern",
            )
        )
        if not row.pattern and not row.canonical.startswith("https://"):
            checks.append(
                (
                    _target_path(row.canonical) in paths,
                    f"{row.path}: canonical destination {row.canonical or '/'} registered",
                )
            )
        if row.status == "withdrawn":
            checks.append(
                (
                    bool(row.tombstone.strip()) and row.path.endswith(".html"),
                    f"withdrawn {row.path}: HTML tombstone explains the disposition",
                )
            )
        if row.status == "forwarded" or row.kind == "copy":
            checks.append((bool(row.target), f"{row.path}: forwarder/copy has a target"))
        if row.target:
            checks += _target_checks(row, paths)
        if row.kind == "result":
            checks.append(
                (row.identity is not None, f"result {row.path}: semantic identity retained")
            )
        for amendment in row.amendments:
            checks.append(
                (
                    _date(str(amendment.get("date", "")))
                    and bool(amendment.get("reason"))
                    and isinstance(amendment.get("previous"), dict),
                    f"{row.path}: dated amendment with reason and previous identity",
                )
            )
            if "historical_target" in amendment:
                target = amendment["historical_target"]
                title = amendment.get("historical_title")
                checks.append(
                    (
                        isinstance(target, str)
                        and _valid_path(target)
                        and isinstance(title, str)
                        and bool(title.strip()),
                        f"{row.path}: historical amendment has a local target and reader title",
                    )
                )
                if isinstance(target, str):
                    checks += _target_checks(replace(row, target=target), paths)
    return checks


def _target_checks(row: SiteURL, paths: Mapping[str, SiteURL]) -> Checks:
    checks: Checks = []
    seen = {row.path}
    target = row.target
    while target:
        if target.startswith("https://"):
            parsed = urlsplit(target)
            checks.append(
                (
                    bool(parsed.netloc) and not parsed.username and not parsed.password,
                    f"{row.path}: explicit external HTTPS target",
                )
            )
            break
        path = _target_path(target)
        if path in seen:
            checks.append((False, f"{row.path}: redirect cycle through {path}"))
            break
        seen.add(path)
        destination = paths.get(path)
        if destination is None or destination.pattern:
            checks.append((False, f"{row.path}: unknown target {target}"))
            break
        checks.append((True, f"{row.path}: target {target} registered"))
        target = destination.target
    return checks


def _require_valid(rows: Sequence[SiteURL]) -> None:
    failed = [line for passed, line in validate_registry(rows) if not passed]
    if failed:
        raise ValueError("\n".join(failed))


def check_history(current: Sequence[SiteURL], baseline: Sequence[SiteURL]) -> Checks:
    checks = validate_registry(current)
    paths = {row.path: row for row in current}
    for old in baseline:
        row = paths.get(old.path)
        checks.append(
            (
                row is not None,
                f"history {old.path}: {'retained' if row else 'removed registration'}",
            )
        )
        if row is None:
            continue
        checks.append(
            (
                row.first_published == old.first_published,
                f"history {old.path}: first publication retained",
            )
        )
        if old.identity is not None:
            prefix_retained = row.amendments[: len(old.amendments)] == old.amendments
            unchanged = row.identity == old.identity and prefix_retained
            amendment = row.amendments[len(old.amendments) :]
            amended = (
                prefix_retained
                and len(amendment) == 1
                and amendment[0].get("previous") == old.identity
            )
            checks.append(
                (prefix_retained, f"history {old.path}: complete amendment prefix retained")
            )
            checks.append(
                (
                    unchanged or amended,
                    f"history {old.path}: semantic identity unchanged or explicitly amended",
                )
            )
    return checks


def page_budget(row: SiteURL) -> int:
    if exception := PAGE_BUDGET_EXCEPTIONS.get(row.path):
        return exception[0]
    family = (
        "paper"
        if row.kind == "paper-file"
        else "workbench"
        if row.producer == "workbench"
        else row.kind
    )
    return PAGE_BUDGETS.get(family, PAGE_BUDGETS["page"])


def check_site(
    directory: Path,
    rows: Sequence[SiteURL] | None = None,
    *,
    partial: bool = False,
    producers: Sequence[str] = (),
) -> Checks:
    """Closed-world physical outputs and budgets, scoped only by explicit producers."""
    rows = list(rows) if rows is not None else load_registry()
    if partial and not producers:
        raise ValueError("a partial build must name at least one producer")
    known = {row.producer for row in rows} - {"shared"}
    if set(producers) - known or (producers and not partial):
        raise ValueError(f"unknown or unscoped producer selection: {producers}")
    checks = validate_registry(rows)
    selected = set(producers)
    paths = {row.path: row for row in rows if not row.pattern}
    patterns = [row for row in rows if row.pattern]
    observed: set[str] = set()
    for file in sorted(directory.rglob("*")):
        name = file.relative_to(directory).as_posix()
        if file.is_symlink():
            checks.append((False, f"site {name}: symlink is outside the publication contract"))
            continue
        if not file.is_file():
            continue
        observed.add(name)
        row = paths.get(name) or next(
            (item for item in patterns if re.fullmatch(item.pattern, name)), None
        )
        checks.append(
            (row is not None, f"site {name}: {'registered' if row else 'unregistered file'}")
        )
        if name.endswith(".html"):
            size = file.stat().st_size
            checks.append(
                (
                    size <= HARD_HTML_LIMIT,
                    f"HTML {name}: {size} bytes, hard limit {HARD_HTML_LIMIT}",
                )
            )
            if row:
                budget = page_budget(row)
                checks.append((size <= budget, f"HTML {name}: {size} bytes, budget {budget}"))
    for row in paths.values():
        if not partial or row.producer in selected:
            checks.append(
                (
                    row.path in observed,
                    (
                        f"site {row.path}: required {row.producer} output "
                        f"{'present' if row.path in observed else 'missing'}"
                    ),
                )
            )
    for row in patterns:
        if not partial or row.producer in selected:
            present = any(re.fullmatch(row.pattern, name) for name in observed)
            checks.append(
                (
                    present,
                    (
                        f"site {row.path}: required {row.producer} namespace "
                        f"{'present' if present else 'missing'}"
                    ),
                )
            )
    return checks


def render_sitemap(rows: Sequence[SiteURL]) -> str:
    root = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for row in sorted(rows, key=lambda item: item.canonical):
        if (
            row.status != "live"
            or row.kind not in ("page", "record", "result", "paper-file")
            or (row.kind == "paper-file" and not row.path.endswith(".html"))
        ):
            continue
        item = SubElement(root, "url")
        SubElement(item, "loc").text = site_url() + row.canonical
        SubElement(item, "lastmod").text = row.lastmod
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root, encoding="unicode") + "\n"
    )


def alias_target(path: str, rows: Sequence[SiteURL]) -> str | None:
    """Only named result/case aliases, resolving to a retained registration."""
    paths = {row.path for row in rows if row.kind in ("record", "result") and not row.pattern}
    if match := re.fullmatch(r"cases/(?:n-)?0*(\d+)\.html", path):
        target = f"cases/{int(match[1])}.html"
    elif match := re.fullmatch(r"result/[Tt]-(\d{3})\.html", path):
        target = f"result/t-{match[1]}.html"
    else:
        return None
    return target if target in paths else None


def render_not_found(rows: Sequence[SiteURL]) -> tuple[str, dict[str, bytes]]:
    from devtools import render_overview, site_assets  # noqa: PLC0415

    shared = site_assets.shared()
    bundle = shared.assets
    script = bundle.script_file(PACKING / "devtools/overview/not-found.js")
    root = urlsplit(site_url()).path
    config = json.dumps(
        {
            "cases": sorted(
                int(row.path.split("/")[1].removesuffix(".html"))
                for row in rows
                if row.kind == "record"
            ),
            "results": sorted(row.path for row in rows if row.kind == "result"),
            "rows": sorted(
                Path(row.path).stem
                for row in rows
                if row.kind == "result" and row.status == "live"
            ),
            "allResults": "all-results.html"
            if any(row.path == "all-results.html" and row.status == "live" for row in rows)
            else None,
        },
        separators=(",", ":"),
    ).replace("<", r"\u003c")
    page = (
        "<!doctype html>\n"
        f'<html lang="en" data-site-root="{escape(root)}"><head>'
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>Page Not Found · {escape(render_overview.PROJECT_NAME)}</title>"
        '<meta name="robots" content="noindex, max-image-preview:large">'
        f'<link rel="stylesheet" href="{root}assets/{shared.kpress_css.output_path}">'
        f'<link rel="icon" type="image/svg+xml" href="{root}favicon.svg">'
        f'<link rel="icon" type="image/png" sizes="48x48" href="{root}favicon-48.png">'
        f'<link rel="apple-touch-icon" href="{root}apple-touch-icon.png">'
        "</head><body><main>"
        "<h1>Page Not Found</h1><p>This address does not identify a published page.</p>"
        f'<p><a href="{root}">The Squares Project</a></p></main>'
        f'<script type="application/json" id="site-url-aliases">{config}</script>'
        f'<script src="{root}assets/{script.output_path}"></script></body></html>\n'
    )
    files = bundle.referenced([page.replace(root + "assets/", "assets/")])
    return page, files


def render_tombstone(row: SiteURL) -> str:
    target = row.target if row.target.startswith("https://") else site_url() + row.target
    replacement = (
        f'<p>Replacement: <a href="{escape(target)}">{escape(row.target)}</a>.</p>'
        if row.target
        else ""
    )
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>Withdrawn Address · The Squares Project</title>"
        '<meta name="robots" content="noindex, max-image-preview:large">'
        f'<link rel="canonical" href="{escape(site_url() + row.canonical)}">'
        "</head><body><main><h1>Withdrawn Address</h1>"
        f"<p>{escape(row.tombstone)}</p>{replacement}"
        f'<p><a href="{escape(site_url())}">The Squares Project</a></p>'
        "</main></body></html>\n"
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as output:
        output.write_text(text, encoding="utf-8")


def crawl_files(
    rows: Sequence[SiteURL] | None = None,
) -> tuple[dict[str, str], dict[str, bytes]]:
    """The overview producer's crawl pages, retained withdrawals and shared assets."""
    rows = list(rows) if rows is not None else load_registry()
    _require_valid(rows)
    page, assets = render_not_found(rows)
    files = {"sitemap.xml": render_sitemap(rows), "404.html": page}
    files.update((row.path, render_tombstone(row)) for row in rows if row.status == "withdrawn")
    return files, assets


def write_crawl_files(directory: Path, rows: Sequence[SiteURL] | None = None) -> None:
    from devtools.site_assets import write_assets  # noqa: PLC0415

    files, assets = crawl_files(rows)
    for name, text in files.items():
        _write(directory / name, text)
    write_assets(directory, assets)


def _git_read(ref: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=REPO, text=True, capture_output=True, check=False
    )
    if result.returncode:
        raise ValueError(f"cannot read historical {ref}:{path}: {result.stderr.strip()}")
    return result.stdout


def historical_registry(ref: str = "origin/main") -> list[SiteURL]:
    """Use the checked-in baseline; bootstrap old main from actual builder declarations."""
    exists = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:packing/site-urls.yaml"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if exists.returncode == 0:
        document = cast(dict[str, Any], load_yaml(_git_read(ref, "packing/site-urls.yaml")))
        return [_parse_row(row) for row in document["urls"]]
    return _seed_history(ref)


def _constants(source: str) -> dict[str, ast.expr]:
    constants: dict[str, ast.expr] = {}
    for statement in ast.parse(source).body:
        if (
            isinstance(statement, ast.AnnAssign)
            and isinstance(statement.target, ast.Name)
            and statement.value
        ):
            constants[statement.target.id] = statement.value
        elif isinstance(statement, ast.Assign):
            for target in statement.targets:
                if isinstance(target, ast.Name):
                    constants[target.id] = statement.value
    return constants


# The syntax reader returns once per supported AST node.
def _static(  # noqa: PLR0911
    node: ast.expr, constants: Mapping[str, ast.expr], names: Mapping[str, Any] | None = None
) -> Any:
    """Read declarations without importing or executing historical Python."""
    names = names or {}
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in names:
            return names[node.id]
        return _static(constants[node.id], constants, names)
    if isinstance(node, ast.JoinedStr):
        return "".join(
            str(
                _static(
                    part.value if isinstance(part, ast.FormattedValue) else part,
                    constants,
                    names,
                )
            )
            for part in node.values
        )
    if isinstance(node, ast.BinOp):
        left, right = (
            _static(node.left, constants, names),
            _static(node.right, constants, names),
        )
        return left / right if isinstance(node.op, ast.Div) else left + right
    if isinstance(node, (ast.Tuple, ast.List)):
        values: list[Any] = []
        for item in node.elts:
            if isinstance(item, ast.Starred):
                values.extend(_static(item.value, constants, names))
            else:
                values.append(_static(item, constants, names))
        return values
    if isinstance(node, ast.GeneratorExp) and len(node.generators) == 1:
        generator = node.generators[0]
        if isinstance(generator.target, ast.Name) and not generator.ifs:
            return [
                _static(node.elt, constants, {**names, generator.target.id: value})
                for value in _static(generator.iter, constants, names)
            ]
    if isinstance(node, ast.Attribute):
        if (
            isinstance(node.value, ast.Name)
            and node.value.id == "repo_links"
            and node.attr == "DEFECTS"
        ):
            return "defects.md"
        value = _static(node.value, constants, names)
        if node.attr == "name" and isinstance(value, Path):
            return value.name
    if isinstance(node, ast.Call):
        args = [_static(arg, constants, names) for arg in node.args]
        if isinstance(node.func, ast.Name):
            if node.func.id == "paper_path":
                return f"papers/{args[0]}{args[1] if len(args) > 1 else '.html'}"
            if node.func.id == "repo_url":
                return "https://github.com/jlevy/squares/blob/main/" + str(args[0])
        if isinstance(node.func, ast.Attribute) and node.func.attr in (
            "with_suffix",
            "with_name",
        ):
            value = _static(node.func.value, constants, names)
            if isinstance(value, Path):
                return (
                    value.with_suffix(args[0])
                    if node.func.attr == "with_suffix"
                    else value.with_name(args[0])
                )
    raise ValueError(f"unsupported historical declaration: {ast.dump(node)}")


def _historical_results(ref: str) -> list[dict[str, Any]]:
    """Latest semantic binding of every result ID ever recorded on the baseline branch."""
    revisions = subprocess.run(
        ["git", "log", "--format=%H", ref, "--", "packing/frontier/results.yaml"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    request = "".join(revision + ":packing/frontier/results.yaml\n" for revision in revisions)
    response = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input=request.encode(),
        capture_output=True,
        check=True,
    ).stdout
    records: dict[str, dict[str, Any]] = {}
    first_published: dict[str, str] = {}
    cursor = 0
    for _revision in revisions:
        end = response.index(b"\n", cursor)
        header = response[cursor:end].split()
        if len(header) != 3 or header[1] != b"blob":
            raise ValueError("historical result register is missing from its recorded revision")
        size = int(header[2])
        text = response[end + 1 : end + 1 + size].decode()
        cursor = end + 2 + size
        document = cast(dict[str, Any], load_yaml(text))
        for result in document["results"]:
            record = dict(result)
            record.setdefault(
                "registered", record.get("established", document["last_reviewed"])
            )
            identifier = str(record["id"])
            # A scientific establishment date is not an earlier URL registration.
            if "registered" in result:
                registered = str(result["registered"])
                first_published[identifier] = min(
                    first_published.get(identifier, registered), registered
                )
            records.setdefault(identifier, record)
    return [
        {
            **record,
            "_url_first_published": first_published.get(identifier, str(record["registered"])),
        }
        for identifier, record in records.items()
    ]


def _historical_paper_dates(ref: str, module: str) -> tuple[str, str]:
    """Read the edition history and revision date without executing historical code.

    A review's original-proof date belongs to its source, not to the review's URL.
    Older review fronts omitted First published; their own version history retains it.
    """
    from devtools.paper_front import iso_date  # noqa: PLC0415

    release = _constants(_git_read(ref, "packing/src/sqpack/release.py"))
    paper = _constants(_git_read(ref, "packing/" + module.replace(".", "/") + ".py"))
    front = next(
        node
        for node in ast.walk(paper["FRONT"])
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "PaperFront"
    )
    version = next(keyword.value for keyword in front.keywords if keyword.arg == "version")
    pending = [version]
    visited: set[str] = set()
    histories: list[ast.Tuple] = []
    while pending:
        for node in ast.walk(pending.pop()):
            if not isinstance(node, ast.Name) or node.id not in release or node.id in visited:
                continue
            visited.add(node.id)
            value = release[node.id]
            if (
                isinstance(value, ast.Tuple)
                and value.elts
                and all(
                    isinstance(entry, ast.Call)
                    and isinstance(entry.func, ast.Name)
                    and entry.func.id == "PublicationHistoryEntry"
                    for entry in value.elts
                )
            ):
                histories.append(value)
            else:
                pending.append(value)
    if len(histories) != 1:
        raise ValueError(f"historical {module} has no unique edition history")
    first = min(
        iso_date(str(_static(keyword.value, release)))
        for entry in histories[0].elts
        if isinstance(entry, ast.Call)
        for keyword in entry.keywords
        if keyword.arg == "first_published"
    )
    revision = next(
        node.args[1]
        for node in ast.walk(front)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "Dated"
        and len(node.args) == 2
        and isinstance(node.args[0], ast.Attribute)
        and node.args[0].attr == "REVISED"
    )
    return first, max(first, iso_date(str(_static(revision, {**release, **paper}))))


def _seed_history(ref: str) -> list[SiteURL]:
    constants = _constants(_git_read(ref, "packing/devtools/render_overview.py"))
    day = FIRST_SITE_DATE
    page_node = constants["PAGES"]
    if not isinstance(page_node, ast.Dict):
        raise TypeError("historical builder has no explicit PAGES dictionary")
    pages = [_static(key, constants) for key in page_node.keys if key is not None]
    pages += _static(constants["DOCUMENT_PAGES"], constants)
    rows = [
        _new_row(path, "page", "overview", "devtools.render_overview:render_all", lastmod=day)
        for path in pages
    ]
    for old, target in _static(constants["MOVED_PAGES"], constants):
        rows.append(
            _new_row(
                old,
                "forwarder",
                "overview",
                "devtools.render_overview:forwarder_pages",
                lastmod=day,
                target=target,
            )
        )
    for old, target in _static(constants["MOVED_FILES"], constants):
        rows.append(
            _new_row(
                old,
                "copy",
                "assembly",
                "devtools.preview_site:copy_moved_files",
                lastmod=day,
                target=target,
            )
        )
    papers = constants["PAPERS"]
    if not isinstance(papers, ast.Tuple):
        raise TypeError("historical PAPERS is not a declared tuple")
    for paper in papers.elts:
        if not isinstance(paper, ast.Call):
            raise TypeError("historical paper is not a PaperRecord")
        slug = next(_static(kw.value, constants) for kw in paper.keywords if kw.arg == "slug")
        module = next(
            _static(kw.value, constants) for kw in paper.keywords if kw.arg == "module"
        )
        first, revised = _historical_paper_dates(ref, module)
        for extension in (".html", ".md", ".pdf"):
            rows.append(  # noqa: PERF401 -- each output has its own registration
                _new_row(
                    f"papers/{slug}{extension}",
                    "paper-file",
                    "paper:" + slug,
                    "historical:paper",
                    first=first,
                    lastmod=revised,
                )
            )
    records = _historical_results(ref)
    for record in records:
        first, lastmod = _result_dates(record)
        first = str(record.get("_url_first_published", first))
        rows.append(
            _new_row(
                f"result/{record['id'].lower()}.html",
                "result",
                "overview",
                "devtools.render_overview:result_fragments",
                first=first,
                lastmod=lastmod,
                identity=result_identity(record),
            )
        )
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref, "packing/frontier"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    for path in listing.splitlines():
        if match := re.fullmatch(r"packing/frontier/n-(\d+)\.md", path):
            rows.append(  # noqa: PERF401 -- filter and parse each historical declaration
                _new_row(
                    f"cases/{int(match[1])}.html",
                    "record",
                    "overview",
                    "devtools.render_case_pages:case_records",
                    first="2026-10-03",
                    lastmod=day,
                )
            )
    asset_constants = _constants(
        _git_read(ref, "packing/devtools/render_n11_lower_bounds_explainer.py")
    )
    assets = _static(
        asset_constants["COMPOSITE_ASSETS"],
        asset_constants,
        {"REPO": Path("/repo"), "PACKING": Path("/repo/packing")},
    )
    rows += [
        _new_row(
            path.name,
            "asset-file",
            "paper:n11-lower-bounds-explainer",
            "historical:composite-assets",
            lastmod=day,
        )
        for path in assets
    ]
    rows += [
        _new_row(
            _static(constants["SOCIAL_CARD"], constants),
            "asset-file",
            "overview",
            "devtools.social_card:write",
            lastmod=day,
        ),
        _new_row(
            "workbench/index.html",
            "page",
            "workbench",
            "devtools.build_site:build",
            lastmod=day,
        ),
        *hashed_asset_rows(day),
    ]
    return sorted(
        (
            replace(row, first_published=FIRST_SITE_DATE)
            if row.first_published == REGISTRATION_DATE
            and row.kind not in ("result", "paper-file")
            else row
            for row in rows
        ),
        key=lambda row: row.path,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail on registry/document drift")
    mode.add_argument(
        "--write", action="store_false", dest="check", help="write registry/document"
    )
    parser.add_argument("--history-ref", default="origin/main", help="retained URL baseline")
    args = parser.parse_args(argv)
    try:
        previous = (
            load_registry() if REGISTRY.is_file() else historical_registry(args.history_ref)
        )
        rows = derive_registry(previous)
        checks = check_history(rows, historical_registry(args.history_ref))
        for path, text in (
            (REGISTRY, render_registry(rows)),
            (DOCUMENT, render_document(rows)),
        ):
            if args.check:
                checks.append(
                    (
                        path.is_file() and path.read_text(encoding="utf-8") == text,
                        f"{path.relative_to(REPO)}: generated register current",
                    )
                )
            elif all(passed for passed, _message in checks):
                _write(path, text)
    except (ValueError, TypeError, KeyError, OSError) as error:
        print(f"FAIL URL registry: {error}")
        return 1
    failed = [line for passed, line in checks if not passed]
    for line in failed:
        print("FAIL " + line)
    print(f"URL registry: {len(rows)} rows, {len(failed)} failures")
    return bool(failed)


if __name__ == "__main__":
    sys.exit(main())
