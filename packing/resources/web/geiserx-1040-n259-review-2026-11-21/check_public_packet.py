from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path
from urllib.parse import unquote, urlsplit


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def anchors(document: str) -> set[str]:
    result = set()
    for heading in re.findall(r"^#{1,6}\s+(.+)$", document, re.MULTILINE):
        plain = re.sub(r"[^\w\s-]", "", heading.lower())
        result.add(re.sub(r"\s+", "-", plain))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check public packet integrity and links without executing geometry."
    )
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--out", type=Path)
    arguments = parser.parse_args()
    packet = Path(__file__).resolve().parent
    repo = arguments.repo_root.resolve() if arguments.repo_root else packet.parents[3]
    retention = json.loads((packet / "retention.json").read_text())
    scope = json.loads((packet / "scope.json").read_text())
    final = json.loads((packet / "results.json").read_text())
    initial = json.loads((packet / "frozen/results.json").read_text())
    freeze = json.loads((packet / "frozen/findings-freeze.json").read_text())
    checks: dict[str, bool] = {}
    for artifact in retention["copied_unchanged"]:
        path = packet / artifact["path"]
        checks[f"preserved:{artifact['path']}"] = (
            path.is_file()
            and path.stat().st_size == artifact["bytes"]
            and digest(path) == artifact["sha256"]
        )
    private = {row["archive_member"]: row for row in retention["retained_externally"]}
    external_freeze_members = []
    for name, expected in freeze["artifact_sha256"].items():
        stored_name = f"{name}.txt" if name.endswith(".py") else name
        path = packet / "frozen" / stored_name
        if path.is_file():
            checks[f"freeze:{name}"] = digest(path) == expected
        else:
            member = f"frozen/{name}"
            checks[f"freeze_external:{name}"] = (
                member in private and private[member]["sha256"] == expected
            )
            external_freeze_members.append(name)
    checks["freeze_has_only_declared_external_launcher"] = external_freeze_members == ["run.sh"]
    checks["source_identities_agree"] = (
        initial["source_identity"]
        == final["source_identity"]
        == {
            Path(name).name: value for name, value in scope["source"]["archive_members"].items()
        }
    )
    checksum_lines = {
        name: value
        for value, name in (
            line.split() for line in (packet / "source-sha256.txt").read_text().splitlines()
        )
    }
    checks["source_checksum_recipe_matches_receipts"] = checksum_lines == {
        name: value["sha256"] for name, value in final["source_identity"].items()
    }
    checks["initial_and_final_geometry_agree"] = all(
        {key: value for key, value in initial[method].items() if key != "elapsed_seconds"}
        == {key: value for key, value in final[method].items() if key != "elapsed_seconds"}
        for method in ("center_check", "corner_check")
    )
    checks["initial_and_final_controls_agree"] = initial["controls"] == final["controls"]
    checks["recorded_controls_all_passed"] = all(row["passed"] for row in final["controls"])
    checks["scope_and_receipts_state_same_side"] = (
        scope["side_exact"] == initial["side_exact"] == final["side_exact"]
    )
    checks["receipt_decimal_is_exact"] = Fraction(
        final["side_decimal_approximation"]
    ) == Fraction(final["side_exact"])
    review = repo / scope["review_document"]
    checks["review_prints_exact_receipt_decimal"] = (
        final["side_decimal_approximation"] in review.read_text()
    )
    local_links = []
    external_links = []
    for document in (packet / "README.md", review):
        text = document.read_text()
        for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme:
                external_links.append(target)
                continue
            destination = (
                (document.parent / unquote(parsed.path)).resolve() if parsed.path else document
            )
            exists = destination.is_relative_to(repo) and destination.is_file()
            anchor_exists = not parsed.fragment or (
                exists and unquote(parsed.fragment) in anchors(destination.read_text())
            )
            local_links.append(
                {
                    "from": str(document.relative_to(repo)),
                    "target": target,
                    "resolves": exists and anchor_exists,
                }
            )
    checks["all_local_links_resolve"] = all(link["resolves"] for link in local_links)
    checks["source_links_match_recorded_urls"] = set(external_links) <= {
        scope["source"]["issue_url"],
        scope["source"]["attachment_url"],
    }
    host_path = re.compile(r"/(?:Users|Volumes)/")
    checks["no_host_paths_in_public_text"] = (
        all(
            host_path.search(path.read_text()) is None
            for path in packet.rglob("*")
            if path.is_file() and path.suffix in {".md", ".py", ".json", ".txt"}
        )
        and host_path.search(review.read_text()) is None
    )
    report = {
        "scope": "Packet integrity and local-link checks.",
        "passed": all(checks.values()),
        "checks": checks,
        "copied_unchanged_count": len(retention["copied_unchanged"]),
        "local_links_checked": len(local_links),
        "local_links": local_links,
        "external_urls_from_permitted_source": sorted(set(external_links)),
        "external_urls_network_checked_by_this_program": False,
        "freeze_members_retained_externally": external_freeze_members,
    }
    rendered = json.dumps(report, indent=2) + "\n"
    if arguments.out:
        arguments.out.write_text(rendered)
    sys.stdout.write(rendered)
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
