#!/usr/bin/env python3
"""Audit the Kingbird catalogue: live SVG adapters, and the retained rigidity register.

Two audits live here because they answer the same question about the same source.

`audit_catalogue` fetches every active prospective SVG and reports adapter health
without retaining geometry. It needs the network.

`audit_rigidity` is offline. It re-derives, from the retained Markdown archive, what
the catalogue says about each packing's rigidity, and compares that against
`reported_upper_bound.catalogue_rigid` in all 100 frontier records. It exists because
n = 11's annotation was silently dropped and no check noticed: the field was only ever
migrated forward, never re-read from the source it transcribes.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from collections.abc import Callable, Mapping
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
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
CATALOGUE = ROOT / "resources/web/kingbird-squares-in-squares.html"
CATALOGUE_MARKDOWN = ROOT / "resources/web/kingbird-squares-in-squares.md"
FRONTIER = ROOT / "frontier"
USER_AGENT = "sqpack-source-audit/1 (+https://github.com/jlevy/thinking-scratchpad)"

# The catalogue's own vocabulary. It annotates rigidity for a handful of packings and
# is silent for the rest; it never asserts that a packing is non-rigid, which is why
# `not-stated` and not `false` is the third value.
NOT_STATED = "not-stated"
RIGIDITY_STATES = ("rigid", "semi-rigid", NOT_STATED)

_ENTRY_HEADING = re.compile(r"^(\d+(?:\s*,\s*\d+)*)\s*$")
# The picture filename may carry a variant suffix (`square-26b.svg`), and its number is
# the largest n of the block, not necessarily the heading's first -- so it identifies a
# block but is never used to name one.
_ENTRY_PICTURE = re.compile(r"^\[]\(square-\d+[a-z]?\.svg\)\s*$")
# The catalogue prints the side either as a high-precision decimal inside \Nn{...} or,
# for the integer grid packings, as a bare integer.
_PRINTED_DECIMAL = re.compile(r"\\Nn\{([0-9]+(?:\.[0-9]+)?)\}")
_PRINTED_INTEGER = re.compile(r"^\$s\s*=\s*([0-9]+)\$\s*$")
_RIGIDITY_ANNOTATION = re.compile(
    r"^\[(Rigid|Semi-rigid)\.?]\(squares_in_squares__rigid\.html\)"
)


class CatalogueFormatError(ValueError):
    """The retained catalogue no longer has the shape this audit reads."""


@dataclass(frozen=True)
class CatalogueEntry:
    """One pictured catalogue block, keyed by the side value printed above it.

    `printed_side` is the identity that matters. The catalogue's blocks move whenever
    a record is improved, so the audit matches a rigidity annotation to a frontier case
    through the decimal the catalogue prints, never through the block's position.
    """

    listed_n: tuple[int, ...]
    printed_side: str
    side_line: int
    rigidity: str
    rigidity_line: int | None


def catalogue_entries(text: str) -> tuple[CatalogueEntry, ...]:
    """Parse the retained catalogue into its pictured blocks, in file order."""
    lines = text.splitlines()
    starts: list[tuple[int, tuple[int, ...]]] = []
    for index, line in enumerate(lines):
        heading = _ENTRY_HEADING.match(line.rstrip())
        following = next(
            (candidate for candidate in lines[index + 1 : index + 3] if candidate.strip()), ""
        )
        if heading and _ENTRY_PICTURE.match(following.strip()):
            listed = tuple(int(part) for part in re.split(r"\s*,\s*", heading.group(1)))
            starts.append((index, listed))
    if not starts:
        raise CatalogueFormatError(
            "no pictured catalogue blocks found; the archive format changed"
        )

    entries: list[CatalogueEntry] = []
    bounds = [start for start, _ in starts] + [len(lines)]
    for position, (start, listed_n) in enumerate(starts):
        block = lines[start : bounds[position + 1]]
        printed_side: str | None = None
        side_line: int | None = None
        rigidity = NOT_STATED
        rigidity_line: int | None = None
        for offset, line in enumerate(block):
            if printed_side is None:
                printed = _PRINTED_DECIMAL.search(line) or _PRINTED_INTEGER.match(line.strip())
                if printed:
                    printed_side = printed.group(1)
                    side_line = start + offset + 1
            annotation = _RIGIDITY_ANNOTATION.match(line.strip())
            if annotation and rigidity == NOT_STATED:
                rigidity = annotation.group(1).lower()
                rigidity_line = start + offset + 1
        if printed_side is None or side_line is None:
            raise CatalogueFormatError(
                f"catalogue block for n={list(listed_n)} at line {start + 1} "
                f"prints no side value"
            )
        entries.append(
            CatalogueEntry(
                listed_n=listed_n,
                printed_side=printed_side,
                side_line=side_line,
                rigidity=rigidity,
                rigidity_line=rigidity_line,
            )
        )
    return tuple(entries)


def catalogue_rigidity(text: str) -> dict[int, CatalogueEntry]:
    """Return the catalogue block covering each listed n."""
    by_n: dict[int, CatalogueEntry] = {}
    for entry in catalogue_entries(text):
        for n in entry.listed_n:
            previous = by_n.setdefault(n, entry)
            if previous is not entry:
                raise CatalogueFormatError(f"n={n} is listed by two catalogue blocks")
    return by_n


def load_frontier_cases(frontier: Path = FRONTIER) -> dict[int, Mapping[str, object]]:
    """Return the frontier case payloads by n."""
    cases: dict[int, Mapping[str, object]] = {}
    for path in sorted(frontier.glob("n-*.md")):
        payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        cases[int(payload["n"])] = payload
    return cases


def audit_rigidity(
    *,
    catalogue_text: str | None = None,
    cases: Mapping[int, Mapping[str, object]] | None = None,
) -> list[str]:
    """Return every disagreement between the retained catalogue and the records.

    The catalogue annotates rigidity for four packings at n <= 100 and says nothing for
    the rest. Silence is transcribed as `not-stated`; it is not a claim that a packing
    can move, and a record must not turn it into one.
    """
    text = (
        catalogue_text
        if catalogue_text is not None
        else CATALOGUE_MARKDOWN.read_text(encoding="utf-8")
    )
    records = cases if cases is not None else load_frontier_cases()
    by_n = catalogue_rigidity(text)
    errors: list[str] = []

    annotated = {
        entry.printed_side: entry
        for entry in catalogue_rigidity(text).values()
        if entry.rigidity != NOT_STATED
    }
    if not annotated:
        # A parser that silently matches nothing would agree with every record, which
        # is exactly the failure mode this audit exists to prevent.
        errors.append(
            "catalogue: no rigidity annotation parsed at all; the archive format changed "
            "and this audit can no longer see what the source says"
        )

    for n in sorted(records):
        case = records[n]
        upper = case.get("reported_upper_bound")
        if not isinstance(upper, Mapping):
            errors.append(f"n={n}: reported_upper_bound is missing or malformed")
            continue
        recorded = upper.get("catalogue_rigid")
        entry = by_n.get(n)
        expected = entry.rigidity if entry else NOT_STATED
        if recorded not in RIGIDITY_STATES:
            errors.append(
                f"n={n}: catalogue_rigid is {recorded!r}, not one of {list(RIGIDITY_STATES)}"
            )
            continue
        if recorded != expected:
            where = (
                f"catalogue line {entry.rigidity_line or entry.side_line}"
                if entry
                else "no catalogue block lists this n"
            )
            errors.append(
                f"n={n}: catalogue_rigid is {recorded!r} but the catalogue says "
                f"{expected!r} ({where})"
            )
            continue
        if entry is None or expected == NOT_STATED:
            continue
        # The annotation belongs to the side value printed above it. If the record no
        # longer carries that side, the packing it describes is not the annotated one
        # and the transcription is stale.
        if upper.get("value") != entry.printed_side:
            errors.append(
                f"n={n}: catalogue_rigid is {recorded!r} from the block printing "
                f"{entry.printed_side!r} at line {entry.side_line}, but the record's "
                f"reported upper bound is {upper.get('value')!r}; re-read the source "
                f"before keeping the annotation"
            )
    return errors


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
            except Exception as error:  # noqa: BLE001 - a fetch failure of any kind is a recorded miss
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
    parser.add_argument(
        "--rigidity",
        action="store_true",
        help="check the retained rigidity register against frontier/ without the network",
    )
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    if args.rigidity:
        errors = audit_rigidity()
        for error in errors:
            print(f"  {error}")
        if errors:
            return 1
        annotated = sorted(
            n
            for n, entry in catalogue_rigidity(
                CATALOGUE_MARKDOWN.read_text(encoding="utf-8")
            ).items()
            if entry.rigidity != NOT_STATED and n <= 100
        )
        print(
            f"  catalogue rigidity register agrees with all 100 records; annotated: {annotated}"
        )
        return 0
    audit = audit_catalogue(jobs=args.jobs)
    summary = audit["summary"]
    if args.json:
        print(json.dumps(audit, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(json.dumps(summary, sort_keys=True))
    return int(summary["adapter_failed"] != 0)  # type: ignore[index]


if __name__ == "__main__":
    raise SystemExit(main())
