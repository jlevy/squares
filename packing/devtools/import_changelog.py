"""Draft changelog candidates from merged main PRs; never publish unreviewed prose.

Use `--pr NUMBER` to acquire GitHub metadata, or `--metadata FILE` for a retained
GitHub JSON export. Both verify merge commits against the local main reference.
Fetch main before authoring if the local reference trails the requested deliveries.
"""

from __future__ import annotations

import argparse
import copy
import html
import json
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

from devtools import render_changelog
from sqpack.yamlio import load_yaml

Document = dict[str, Any]
FIELDS = "number,title,body,mergedAt,baseRefName,mergeCommit,state,url"


def _empty() -> Document:
    return {
        "softschema": {
            "contract": "packing.squares:SiteChangelog/v1",
            "schema": "site-changelog.schema.yaml",
            "status": "enforced",
        },
        "repository": "https://github.com/jlevy/squares",
        "entries": [],
        "deliveries": [],
        "coverage": {"pull_requests": [], "omissions": []},
        "frozen_entries": [],
    }


def _delivery(row: Document, *, require_main_delivery: bool = True) -> Document:
    if (
        row.get("state") != "MERGED"
        or not row.get("mergedAt")
        or not isinstance(row.get("baseRefName"), str)
        or not row["baseRefName"].strip()
        or (
            require_main_delivery
            and row["baseRefName"] != "main"
            and not row.get("delivery_to_main")
        )
    ):
        raise ValueError(
            f"PR #{row.get('number', '?')}: actual merged main metadata is required"
        )
    commit = row.get("mergeCommit")
    if not isinstance(commit, dict) or not re.fullmatch(
        r"[0-9a-f]{40}", str(commit.get("oid", ""))
    ):
        raise ValueError("merged PR requires a full mergeCommit oid")
    delivery = {
        "number": row["number"],
        "title": row["title"],
        "merged_at": row["mergedAt"],
        "base_ref": row["baseRefName"],
        "merge_commit": commit["oid"],
    }
    if "delivery_to_main" in row:
        delivery["delivery_to_main"] = copy.deepcopy(row["delivery_to_main"])
    return delivery


def verify_main_delivery(delivery: Document, main_ref: str = "origin/main") -> Document | None:
    """Authoring boundary: the retained merge commit must actually reach local main."""
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", delivery["merge_commit"], main_ref],
        cwd=render_changelog.REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(
            f"PR #{delivery['number']}: merge commit is not delivered to {main_ref}; "
            "fetch main before importing"
        )
    if delivery["base_ref"] == "main":
        return None
    # GitHub keeps a formal stack layer's original base ref after the complete stack
    # lands. Retain that API fact and separately prove the recorded merge on main.
    first_parent = subprocess.run(
        ["git", "rev-list", "--first-parent", main_ref],
        cwd=render_changelog.REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    if delivery["merge_commit"] not in first_parent:
        raise ValueError(
            f"PR #{delivery['number']}: stacked merge is not a "
            f"first-parent delivery to {main_ref}"
        )
    return {
        "commit": delivery["merge_commit"],
        "evidence": "https://github.com/jlevy/squares/commit/" + delivery["merge_commit"],
    }


def draft(rows: Sequence[Document], baseline: Document | None = None) -> Document:
    """Preserve published announcements and add explicit editorial placeholders.

    This pure function validates supplied merge metadata. The CLI additionally checks
    ancestry before calling it; callers acquiring metadata themselves own that check.
    Publication dates, public artifacts, stacks and editions are editorial decisions.
    """
    document = copy.deepcopy(baseline) if baseline is not None else _empty()
    render_changelog.validate(document)
    frozen = {entry["id"]: copy.deepcopy(entry) for entry in document.get("frozen_entries", [])}
    for entry in document["entries"]:
        frozen[entry["id"]] = {
            key: copy.deepcopy(entry[key]) for key in ("id", "date", "pull_requests")
        }
    document["frozen_entries"] = list(frozen.values())
    retained = {delivery["number"]: delivery for delivery in document["deliveries"]}
    numbers: set[int] = set()
    known_results = {
        record["id"]
        for record in load_yaml(
            (render_changelog.ROOT / "frontier/results.yaml").read_text(encoding="utf-8")
        )["results"]
    }
    for row in sorted(rows, key=lambda item: item["number"]):
        delivery = _delivery(row)
        number = delivery["number"]
        if number in numbers:
            raise ValueError(f"duplicate imported PR #{number}")
        numbers.add(number)
        if number in retained:
            old = retained[number]
            if any(
                old.get(key) != delivery.get(key)
                for key in ("merged_at", "base_ref", "merge_commit", "delivery_to_main")
            ):
                raise ValueError(f"PR #{number}: imported metadata changes a retained delivery")
            continue
        document["deliveries"].append(delivery)
        document["coverage"]["pull_requests"].append(number)
        entry = {
            "id": f"pr-{number}",
            "date": delivery["merged_at"][:10],
            "title": delivery["title"],
            "pull_requests": [number],
            "summary": "Draft for editorial review: " + html.escape(delivery["title"]) + ".",
        }
        if "significance" not in row:
            raise ValueError(
                f"PR #{number}: an editorial significance score and rationale are required; "
                "supply significance metadata or --significance and --significance-rationale"
            )
        entry["significance"] = copy.deepcopy(row["significance"])
        cited = sorted(set(re.findall(r"\bT-\d{3,}\b", row.get("body") or "")) & known_results)
        if cited:
            entry["result_ids"] = cited
            entry["references"] = [
                {
                    "label": "Referenced result records",
                    "target": "packing/frontier/results.yaml",
                }
            ]
        document["entries"].append(entry)
    render_changelog.validate(document)
    if baseline is not None:
        render_changelog.validate_frozen(document, baseline)
    return document


def coverage_audit(document: Document) -> str:
    """The maintenance disposition table, kept outside the reader-facing section."""
    entries = {
        number: entry["id"]
        for entry in document["entries"]
        for number in entry["pull_requests"]
    }
    omissions = {
        item["pull_request"]: item["reason"] for item in document["coverage"]["omissions"]
    }
    lines = [
        "# Changelog coverage audit",
        "",
        "Candidate wording requires editorial review before publication.",
        "",
        "| PR | Disposition |",
        "| --- | --- |",
    ]
    for number in sorted(document["coverage"]["pull_requests"], reverse=True):
        disposition = entries.get(number) or "Omitted: " + omissions[number]
        disposition = html.escape(disposition).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| [#{number}]({document['repository']}/pull/{number}) | {disposition} |")
    return "\n".join([*lines, "", render_changelog.FOOTER, ""])


def _write_candidate(options: argparse.Namespace) -> None:
    if options.output.resolve() == options.baseline.resolve():
        raise ValueError("candidate output must differ from the published baseline")
    baseline = render_changelog.load(options.baseline) if options.baseline.exists() else None
    if options.metadata:
        rows = json.loads(options.metadata.read_text(encoding="utf-8"))
        if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
            raise ValueError("metadata must be an array of gh pr view records")
    else:
        rows = []
        for number in options.pr:
            result = subprocess.run(
                [
                    "gh",
                    "pr",
                    "view",
                    str(number),
                    "--repo",
                    "jlevy/squares",
                    "--json",
                    FIELDS,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            rows.append(json.loads(result.stdout))
    for row in rows:
        receipt = verify_main_delivery(
            _delivery(row, require_main_delivery=False), options.main_ref
        )
        if receipt is not None:
            row["delivery_to_main"] = receipt
    if (options.significance is None) != (options.significance_rationale is None):
        raise ValueError(
            "--significance and --significance-rationale must be supplied together"
        )
    if options.significance is not None:
        for row in rows:
            row["significance"] = {
                "score": options.significance,
                "rationale": options.significance_rationale,
            }
    document = draft(rows, baseline)
    rendered = yaml.safe_dump(document, allow_unicode=True, sort_keys=False, width=96)
    audit = coverage_audit(document)
    audit_path = options.audit or options.output.with_suffix(".coverage.md")
    protected = {options.baseline.resolve()}
    if options.metadata:
        protected.add(options.metadata.resolve())
    if options.output.resolve() in protected:
        raise ValueError("candidate output must not replace retained metadata or the baseline")
    if audit_path.resolve() in {options.output.resolve(), *protected}:
        raise ValueError("coverage audit must have a separate output path")
    with atomic_output_file(options.output) as output:
        output.write_text(rendered, encoding="utf-8")
    with atomic_output_file(audit_path) as output:
        output.write_text(audit, encoding="utf-8")
    print(
        f"wrote candidate {options.output} and audit {audit_path}; "
        "review wording before publication"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Write reviewable candidate YAML and a coverage audit, never a public view."""
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument(
        "--pr", type=int, action="append", help="Merged main PR number; may be repeated"
    )
    inputs.add_argument("--metadata", type=Path, help="Retained gh pr view JSON array")
    parser.add_argument("--baseline", type=Path, default=render_changelog.SRC)
    parser.add_argument("--main-ref", default="origin/main")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--significance", type=int, choices=range(1, 6))
    parser.add_argument(
        "--significance-rationale", help="Plain editorial reason for the candidate's importance"
    )
    options = parser.parse_args(argv)
    try:
        _write_candidate(options)
    except (
        OSError,
        TypeError,
        ValueError,
        KeyError,
        yaml.YAMLError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"changelog import: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
