#!/usr/bin/env python3
"""Audit every active prospective Kingbird SVG without retaining source geometry."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

from sqpack.known_best import (
    KINGBIRD_BASE_URL,
    SourceGeometryError,
    catalogue_source_map,
    parse_kingbird_svg,
)

ROOT = Path(__file__).resolve().parent.parent
CATALOGUE = ROOT / "resources/web/kingbird-squares-in-squares.html"
USER_AGENT = "sqpack-source-audit/1 (+https://github.com/jlevy/thinking-scratchpad)"


@dataclass(frozen=True)
class SourceGroup:
    source_path: str
    source_n: int
    listed_n: tuple[int, ...]


def source_groups() -> tuple[SourceGroup, ...]:
    """Return the distinct active Kingbird SVG groups in deterministic order."""
    catalogue = catalogue_source_map(CATALOGUE, first_n=101, last_n=324)
    by_path: dict[str, SourceGroup] = {}
    for source_path, source_n, listed_n in catalogue.values():
        group = SourceGroup(source_path, source_n, listed_n)
        previous = by_path.setdefault(source_path, group)
        if previous != group:
            raise ValueError(f"conflicting catalogue identity for {source_path}")
    return tuple(sorted(by_path.values(), key=lambda group: group.source_n))


def _fetch(source_path: str) -> bytes:
    request = Request(f"{KINGBIRD_BASE_URL}/{source_path}", headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read()


def _local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def source_quirks(text: str) -> list[dict[str, object]]:
    """Describe only malformed-reference recovery facts, never packing coordinates."""
    root = ET.fromstring(text)
    identifiers = [value for element in root.iter() if (value := element.get("id"))]
    counts = Counter(identifiers)
    definitions = set(identifiers)
    quirks: list[dict[str, object]] = []
    duplicate_ids = sorted(identifier for identifier, count in counts.items() if count > 1)
    if duplicate_ids:
        quirks.append(
            {
                "kind": "duplicate-id-first-in-tree-order",
                "identifiers": duplicate_ids,
            }
        )
    bare_local = []
    for element in root.iter():
        if _local_name(element) != "use":
            continue
        href = element.get("href") or next(
            (value for key, value in element.attrib.items() if key.endswith("}href")), ""
        )
        if href and not href.startswith("#") and href in definitions:
            bare_local.append(href)
    if bare_local:
        quirks.append(
            {
                "kind": "bare-local-use-ignored-after-count-reconciliation",
                "identifiers": sorted(bare_local),
            }
        )
    return quirks


def audit_catalogue(
    *,
    fetch: Callable[[str], bytes] = _fetch,
    checked_at: str | None = None,
    jobs: int = 12,
) -> dict[str, object]:
    """Fetch concurrently, parse sequentially, and return a geometry-free receipt."""
    groups = source_groups()
    payloads: dict[str, bytes] = {}
    fetch_failures: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=jobs) as executor:
        future_to_group = {executor.submit(fetch, group.source_path): group for group in groups}
        for future in as_completed(future_to_group):
            group = future_to_group[future]
            try:
                payloads[group.source_path] = future.result()
            except Exception as error:
                fetch_failures[group.source_path] = f"{type(error).__name__}: {error}"

    sources: list[dict[str, object]] = []
    passed = 0
    for group in groups:
        payload = payloads.get(group.source_path)
        record: dict[str, object] = {
            "listed_n": list(group.listed_n),
            "source_n": group.source_n,
            "source_path": group.source_path,
        }
        if payload is None:
            record.update(
                {
                    "adapter_status": "fetch-failed",
                    "reason": fetch_failures[group.source_path],
                }
            )
        else:
            record["bytes"] = len(payload)
            try:
                text = payload.decode("utf-8")
                geometry = parse_kingbird_svg(text, expected_n=group.source_n)
                record.update(
                    {
                        "adapter_status": "passed",
                        "extracted_squares": len(geometry.poses),
                        "source_quirks": source_quirks(text),
                    }
                )
                passed += 1
            except (UnicodeDecodeError, ET.ParseError, SourceGeometryError) as error:
                kind = (
                    error.kind
                    if isinstance(error, SourceGeometryError)
                    else type(error).__name__
                )
                record.update({"adapter_status": "parse-failed", "reason": f"{kind}: {error}"})
        sources.append(record)

    timestamp = checked_at or datetime.now(UTC).astimezone().isoformat(timespec="seconds")
    return {
        "claim_status": "source-access-and-adapter-only-no-geometry-retained",
        "checked_at": timestamp,
        "policy": {
            "annotations": "prohibited",
            "coordinate_output": "prohibited",
            "source_retention": "prohibited-pending-license-review",
        },
        "summary": {
            "adapter_failed": len(groups) - passed,
            "adapter_passed": passed,
            "source_groups": len(groups),
            "svg_responses": len(payloads),
        },
        "sources": sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=12)
    parser.add_argument("--json", action="store_true", help="print the metadata-only receipt")
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    audit = audit_catalogue(jobs=args.jobs)
    summary = audit["summary"]
    if args.json:
        print(json.dumps(audit, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(json.dumps(summary, sort_keys=True))
    return int(summary["adapter_failed"] != 0)  # type: ignore[index]


if __name__ == "__main__":
    raise SystemExit(main())
