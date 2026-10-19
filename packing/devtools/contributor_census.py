"""Reconcile structured credit fields and inspection receipts without guessing identities.

Run from packing with `python -m devtools.contributor_census`. `--draft PATH` writes
unresolved source spans for review; it never promotes an alias candidate to a person.
`--stale` lists every reviewed span whose live source text no longer matches, which the
manifest loader reports one at a time; run it after merging new credit records.
`--reconcile` rewrites the manifest after such a merge: it preserves unchanged reviewed
fields, replaces stale fields and adds new structured fields. Every new person span stays
unresolved for source-specific review; the report lists candidate profiles without
assigning an identity.
PDF coverage requires explicit inspection receipts. Missing extraction is pending work.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from contextlib import ExitStack
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file, atomic_write_text

from sqpack.contributor_occurrences import (
    CONTRACT,
    MANIFEST,
    SCHEMA_PATH,
    CreditOccurrence,
    CreditOrigin,
    OccurrenceError,
    OccurrenceRegistry,
    load_occurrences,
    source_text,
)
from sqpack.contributors import PEOPLE_DIR, load_contributors
from sqpack.project import require_project_root
from sqpack.yamlio import load_yaml

# These are extraction boundaries, not a statement that the remaining archive was read.
STRUCTURED_SCOPE = (
    "bibliography authors/credit; result prerequisites; case finders/improvers/provers"
)
PENDING_FAMILIES = (
    "PDF bylines, acknowledgments, references and figure credits",
    "evidence performers and acknowledgments",
    "witness provenance and discoverers",
    "web packet text and catalogue construction history",
    "asymptotic, strategy, rigidity, methods and simulation literature",
    "paper renderer authors and oversight; private correspondence public-identity review",
    "correction labels and project-card/footer attribution",
)


def _spans(
    text: str, origin: CreditOrigin, role: str, *, grouped: bool = False
) -> list[CreditOccurrence]:
    rows = []
    delimiters = (
        list(re.finditer(r",|;| after | and ", text))
        if grouped
        else list(re.finditer(r" and ", text))
    )
    boundaries = [(0, ""), *((match.end(), match.group()) for match in delimiters)]
    ends = [*(match.start() for match in delimiters), len(text)]
    current_role = role
    for (left, delimiter), right in zip(boundaries, ends, strict=True):
        start, end = left, right
        if delimiter == " after ":
            current_role = "prerequisite"
        elif delimiter == ";":
            current_role = role
        while start < end and text[start].isspace():
            start += 1
        while end > start and text[end - 1].isspace():
            end -= 1
        label = text[start:end]
        if not label:
            continue
        collective = re.search(r"\s+et al\.$", label)
        if collective:
            person_end = start + collective.start()
            rows.append(
                CreditOccurrence(
                    origin,
                    text,
                    start,
                    person_end,
                    text[start:person_end],
                    current_role,
                    "unresolved",
                    note="Identity review pending.",
                )
            )
            start += collective.start() + len(collective.group()) - len("et al.")
            rows.append(
                CreditOccurrence(
                    origin,
                    text,
                    start,
                    end,
                    "et al.",
                    "collective-abbreviation",
                    "non-person",
                    note="Collective abbreviation; omitted authors require source inspection.",
                )
            )
        else:
            rows.append(
                CreditOccurrence(
                    origin,
                    text,
                    start,
                    end,
                    label,
                    current_role,
                    "unresolved",
                    note="Identity review pending.",
                )
            )
    return rows


def structured_occurrences(repo: Path) -> tuple[CreditOccurrence, ...]:
    """Extract stable field addresses; grouped labels remain unresolved review proposals."""
    rows = []
    bibliography = load_yaml((repo / "packing/resources/bibliography.yaml").read_text())
    for source in bibliography["sources"]:
        key = source["key"]
        for index, name in enumerate(source["authors"]):
            rows.extend(
                _spans(
                    name,
                    CreditOrigin(
                        "packing/resources/bibliography.yaml", key, f"/authors/{index}"
                    ),
                    "source-author",
                )
            )
        if source.get("credit"):
            rows.extend(
                _spans(
                    source["credit"],
                    CreditOrigin("packing/resources/bibliography.yaml", key, "/credit"),
                    "credited-contributor",
                    grouped=True,
                )
            )
    register = load_yaml((repo / "packing/frontier/results.yaml").read_text())
    for result in register["results"]:
        for index, name in enumerate((result.get("builds_on") or {}).get("credit") or []):
            rows.extend(
                _spans(
                    name,
                    CreditOrigin(
                        "packing/frontier/results.yaml",
                        result["id"],
                        f"/builds_on/credit/{index}",
                    ),
                    "prerequisite",
                )
            )
    for path in sorted((repo / "packing/frontier").glob("n-*.md")):
        case = load_yaml(path.read_text().split("---\n", 2)[1])["packing"]
        for bound, field, role in (
            ("reported_upper_bound", "found_by", "construction-finder"),
            ("reported_upper_bound", "improved_by", "construction-improver"),
            ("reported_lower_bound", "proved_by", "lower-bound-prover"),
        ):
            for index, name in enumerate(case[bound].get(field) or []):
                rows.extend(
                    _spans(
                        name,
                        CreditOrigin(
                            path.relative_to(repo).as_posix(),
                            str(case["n"]),
                            f"/{bound}/{field}/{index}",
                        ),
                        role,
                    )
                )
    return tuple(rows)


def tracked_pdfs(repo: Path) -> tuple[str, ...]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "packing/resources"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(sorted(path for path in result.stdout.split("\0") if path.endswith(".pdf")))


def census(repo: Path, registry: OccurrenceRegistry | None = None) -> dict[str, Any]:
    """Distinguish reviewed spans, new source fields, candidate spellings and unread PDFs."""
    registry = registry if registry is not None else load_occurrences(repo=repo)
    profiles = load_contributors(repo / "packing" / PEOPLE_DIR, repo=repo)
    candidates = structured_occurrences(repo)
    extracted: dict[CreditOrigin, list[CreditOccurrence]] = {}
    for item in candidates:
        extracted.setdefault(item.origin, []).append(item)
    counts: Counter[str] = Counter()
    pending = []
    for origin, items in extracted.items():
        reviewed = registry.by_origin.get(origin)
        for item in reviewed if reviewed is not None else items:
            disposition = item.disposition if reviewed is not None else "unreviewed"
            counts[disposition] += 1
            if disposition in {"unreviewed", "unresolved"}:
                pending.append(
                    {
                        "origin": asdict(origin),
                        "label": item.label,
                        "disposition": disposition,
                        "candidate_ids": [
                            profile.id for profile in profiles.candidates(item.label)
                        ],
                    }
                )
    pdfs = tracked_pdfs(repo)
    receipts = {
        receipt.path: receipt
        for receipt in registry.inspections
        if receipt.scope == "PDF full credit census"
    }
    pdf_status = Counter(
        receipts[path].status if path in receipts else "pending" for path in pdfs
    )
    return {
        "structured_scope": STRUCTURED_SCOPE,
        "profile_count": len(profiles.by_id),
        "structured_occurrence_count": sum(counts.values()),
        "dispositions": dict(sorted(counts.items())),
        "pdfs": {"tracked": len(pdfs), **dict(sorted(pdf_status.items()))},
        "pending_families": list(PENDING_FAMILIES),
        "pending_occurrences": pending,
        "pending_pdf_paths": [
            path for path in pdfs if path not in receipts or receipts[path].status == "pending"
        ],
    }


def stale_occurrences(repo: Path, path: Path | None = None) -> list[dict[str, Any]]:
    """Every reviewed span whose addressed source text changed or no longer exists.

    The manifest loader refuses the first such span; this reads the manifest without
    validating it, so one run shows the whole review a source change needs."""
    path = path if path is not None else repo / "packing" / MANIFEST
    documents: dict[str, Any] = {}
    stale = []
    for row in load_yaml(path.read_text(encoding="utf-8"))["occurrences"]:
        origin = CreditOrigin(**row["origin"])
        try:
            live: str | None = source_text(origin, repo=repo, documents=documents)
        except OccurrenceError:
            live = None
        if live != row["expected_text"]:
            stale.append(
                {
                    "origin": asdict(origin),
                    "label": row["label"],
                    "disposition": row["disposition"],
                    "contributor_id": row.get("contributor_id"),
                    "expected_text": row["expected_text"],
                    "live_text": live,
                }
            )
    return stale


def reconcile(repo: Path, path: Path | None = None) -> dict[str, Any]:
    """Rewrite the manifest against the live structured credit fields.

    Reviewed spans whose source text is unchanged are kept as they are. A stale span is
    dropped, with the rest of its field's spans, and the field's live spans take their
    place; spans of fields the manifest never held are added after the last span from
    the same file. A reviewed field's manual span boundaries remain authoritative.
    Every new person span stays unresolved, with profile candidates in the report.
    Validate the complete proposed manifest before atomically replacing the prior file."""
    path = path if path is not None else repo / "packing" / MANIFEST
    document = load_yaml(path.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = document["occurrences"]
    stale_origins = {CreditOrigin(**item["origin"]) for item in stale_occurrences(repo, path)}
    kept = [row for row in rows if CreditOrigin(**row["origin"]) not in stale_origins]
    profiles = load_contributors(repo / "packing" / PEOPLE_DIR, repo=repo)
    reviewed_origins = {CreditOrigin(**row["origin"]) for row in kept}
    fresh: dict[CreditOrigin, list[dict[str, Any]]] = {}
    report: dict[str, Any] = {"dropped": [], "unresolved": [], "non-person": []}
    for item in structured_occurrences(repo):
        if item.origin in reviewed_origins:
            continue
        row = asdict(item)
        row.pop("contributor_id")
        row["evidence"] = []
        if item.disposition != "non-person":
            row["disposition"] = "unresolved"
        row = _ordered(row)
        report[row["disposition"]].append(
            {
                **row,
                "candidate_ids": sorted(
                    profile.id for profile in profiles.candidates(item.label)
                )
                if row["disposition"] == "unresolved"
                else [],
            }
        )
        fresh.setdefault(item.origin, []).append(row)
    report["dropped"] = [
        _ordered(row) for row in rows if CreditOrigin(**row["origin"]) in stale_origins
    ]
    result: list[dict[str, Any]] = []
    placed: set[CreditOrigin] = set()
    for row in rows:
        origin = CreditOrigin(**row["origin"])
        if origin in stale_origins:
            if origin not in placed:
                result.extend(fresh.get(origin, []))
                placed.add(origin)
            continue
        result.append(row)
    for origin, new_rows in fresh.items():
        if origin in placed:
            continue
        last = max(
            (index for index, row in enumerate(result) if row["origin"]["path"] == origin.path),
            default=len(result) - 1,
        )
        result[last + 1 : last + 1] = new_rows
        placed.add(origin)
    document["occurrences"] = result
    with ExitStack() as cleanup, atomic_output_file(path) as temporary:
        cleanup.callback(temporary.unlink, missing_ok=True)
        temporary.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )
        load_occurrences(temporary, repo=repo, profiles=profiles)
    return report


def _ordered(row: dict[str, Any]) -> dict[str, Any]:
    """A manifest row in the manifest's own key order, without empty optional fields."""
    order = (
        "origin",
        "expected_text",
        "start",
        "end",
        "label",
        "role",
        "disposition",
        "evidence",
        "contributor_id",
        "note",
    )
    return {key: row[key] for key in order if key in row and row[key] not in (None, "")}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print the full actionable census.")
    parser.add_argument(
        "--draft", type=Path, help="Write unresolved proposals for manual identity review."
    )
    parser.add_argument(
        "--stale",
        action="store_true",
        help="List every reviewed span whose source text changed; exit 1 if any did.",
    )
    parser.add_argument(
        "--reconcile",
        action="store_true",
        help="Rewrite the manifest against the live credit fields and list what changed.",
    )
    args = parser.parse_args(argv)
    repo = require_project_root().parent
    if args.reconcile:
        print(json.dumps(reconcile(repo), ensure_ascii=False, indent=2))
        return 0
    if args.stale:
        stale = stale_occurrences(repo)
        print(json.dumps(stale, ensure_ascii=False, indent=2))
        return 1 if stale else 0
    if args.draft:
        rows = []
        for item in structured_occurrences(repo):
            row = asdict(item)
            row.pop("contributor_id")
            rows.append(row)
        draft = {
            "softschema": {"contract": CONTRACT, "schema": SCHEMA_PATH, "status": "enforced"},
            "occurrences": rows,
            "inspections": [
                {
                    "path": path,
                    "status": "pending",
                    "scope": "PDF full credit census",
                    "locators": [],
                }
                for path in tracked_pdfs(repo)
            ],
        }
        atomic_write_text(
            args.draft, yaml.safe_dump(draft, sort_keys=False, allow_unicode=True)
        )
        print(f"Wrote {len(rows)} unresolved proposals; no identities assigned: {args.draft}")
        return 0
    report = census(repo)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        summary = {
            key: value
            for key, value in report.items()
            if key not in {"pending_occurrences", "pending_pdf_paths"}
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
