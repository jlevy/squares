"""Inventory bead/spec drift for a human-reviewed reconciliation; never mutate beads.

Read a ``tbd list --all --json`` snapshot, including closed children so an
undecomposed epic cannot be mistaken for a completed one. Emit two disjoint review
queues with explicit coverage; a flag is a question to investigate, not a verdict.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
FIRST_LANE = frozenset("0123456789abcdefgh")
OLD_ROOT = "explorations/packing/"
BEAD_ACTIONS = frozenset({"close", "update", "retain", "needs_evidence"})
SPEC_ACTIONS = frozenset(
    {
        "move_archive",
        "move_done",
        "move_draft",
        "move_paused",
        "needs_evidence",
        "retain",
        "update_status",
    }
)
EXPECTED_UPDATE_FIELDS = frozenset({"expected_delegate", "expected_status", "expected_version"})
TARGET_UPDATE_FIELDS = {
    "close": frozenset({"close_reason", "status"}),
    "update": frozenset({"hold", "spec_path"}),
}


def current_path(path: str, repo: Path) -> str:
    """Recognize the exact former root only when its replacement exists."""
    candidate = path.removeprefix(OLD_ROOT)
    return candidate if path.startswith(OLD_ROOT) and (repo / candidate).is_file() else path


def inventory(beads: list[dict[str, Any]], repo: Path) -> dict[str, Any]:
    """Keep every nonclosed bead and every plan, with evidence for review flags."""
    specs = sorted((repo / "docs/project/specs").rglob("*.md"))
    specs_by_name: dict[str, list[str]] = {}
    beads_by_id = {str(bead["id"]): bead for bead in beads}
    for path in specs:
        specs_by_name.setdefault(path.name, []).append(path.relative_to(repo).as_posix())
    children: dict[str, list[dict[str, Any]]] = {}
    for bead in beads:
        parent = bead.get("parentId")
        if parent:
            children.setdefault(str(parent), []).append(bead)
    queues: dict[str, list[dict[str, Any]]] = {"a": [], "b": []}
    for bead in beads:
        if bead.get("status") == "closed":
            continue
        item = dict(bead)
        bead_id = str(bead["id"])
        linked = str(bead.get("spec_path") or "")
        descendants = children.get(bead_id, [])
        item["children_total"] = len(descendants)
        item["children_nonclosed"] = sum(b.get("status") != "closed" for b in descendants)
        item["spec_exists"] = bool(linked and (repo / linked).is_file())
        item["spec_same_filename"] = specs_by_name.get(Path(linked).name, []) if linked else []
        flags: list[str] = []
        if linked and not item["spec_exists"]:
            flags.append("missing_spec_path")
        if bead.get("status") == "in_progress":
            if "delegate" not in bead:
                flags.append("ownership_not_in_snapshot_read_details")
            elif not bead["delegate"]:
                flags.append("missing_delegate")
        if descendants and not item["children_nonclosed"]:
            flags.append("all_children_closed_read_scope")
        item["review_flags"] = flags
        queues["a" if bead_id.rsplit("-", 1)[-1][0] in FIRST_LANE else "b"].append(item)
    plans: dict[str, list[dict[str, Any]]] = {"a": [], "b": []}
    for index, path in enumerate(specs):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(repo).as_posix()
        mentioned_beads = sorted(set(re.findall(r"\bthink-[a-z0-9]+\b", text)))
        linked_beads = [
            b for b in beads if current_path(str(b.get("spec_path") or ""), repo) == relative
        ]
        plans["a" if index % 2 == 0 else "b"].append(
            {
                "path": relative,
                "unchecked": len(re.findall(r"^\s*-\s*\[ \]", text, re.MULTILINE)),
                "linked_total": len(linked_beads),
                "linked_nonclosed": [
                    b["id"] for b in linked_beads if b.get("status") != "closed"
                ],
                "mentioned_beads": mentioned_beads,
                "mentioned_nonclosed": [
                    bead_id
                    for bead_id in mentioned_beads
                    if bead_id in beads_by_id and beads_by_id[bead_id].get("status") != "closed"
                ],
                "mentioned_missing": [
                    bead_id for bead_id in mentioned_beads if bead_id not in beads_by_id
                ],
            }
        )
    return {
        "counts": {
            "all_beads": len(beads),
            "statuses": dict(Counter(str(b.get("status")) for b in beads)),
            "specs": len(specs),
            "lane_a_beads": len(queues["a"]),
            "lane_b_beads": len(queues["b"]),
        },
        "lanes": {name: {"beads": queues[name], "specs": plans[name]} for name in ("a", "b")},
        "exact_path_repairs": [
            {"id": b["id"], "status": b["status"], "from": b["spec_path"], "to": resolved}
            for b in beads
            if (resolved := current_path(str(b.get("spec_path") or ""), repo))
            != str(b.get("spec_path") or "")
        ],
    }


def review_coverage(report: dict[str, Any], reviews: list[dict[str, Any]]) -> dict[str, Any]:
    """Require an explicit disposition for every assigned bead and spec exactly once."""
    problems: list[str] = []
    totals: dict[str, int] = {}
    for kind, key in (("beads", "id"), ("specs", "path")):
        expected = (
            {item[key] for lane in report["lanes"].values() for item in lane[kind]}
            if "lanes" in report
            else set(report[kind])
        )
        entries = [item for review in reviews for item in review.get(kind, [])]
        counts = Counter(str(item.get(key, "")) for item in entries)
        problems.extend(
            f"missing {kind}: {value}" for value in sorted(expected - counts.keys())
        )
        problems.extend(
            f"unexpected {kind}: {value}" for value in sorted(counts.keys() - expected)
        )
        problems.extend(
            f"duplicate {kind}: {value}" for value, count in counts.items() if count > 1
        )
        for item in entries:
            if not item.get("reason") or not item.get("action"):
                problems.append(f"incomplete disposition: {item.get(key)}")
            action = str(item.get("action", ""))
            allowed = BEAD_ACTIONS if kind == "beads" else SPEC_ACTIONS
            if action not in allowed:
                problems.append(f"unknown {kind[:-1]} action: {item.get(key)}")
            evidence = item.get("evidence")
            if not isinstance(evidence, list) or not any(
                isinstance(value, str) and value.strip() for value in evidence
            ):
                problems.append(f"disposition without evidence: {item.get(key)}")
            if kind == "beads" and action in {"close", "update"}:
                updates = item.get("updates")
                if not isinstance(updates, dict):
                    problems.append(f"mutation without updates: {item.get(key)}")
                    continue
                target_fields = TARGET_UPDATE_FIELDS[action]
                unknown_fields = set(updates) - EXPECTED_UPDATE_FIELDS - target_fields
                if unknown_fields:
                    problems.append(
                        f"unknown mutation fields: {item.get(key)}: "
                        f"{', '.join(sorted(unknown_fields))}"
                    )
                if type(updates.get("expected_version")) is not int:
                    problems.append(f"mutation without expected_version: {item.get(key)}")
                if (
                    not isinstance(updates.get("expected_status"), str)
                    or not updates["expected_status"].strip()
                ):
                    problems.append(f"mutation without expected_status: {item.get(key)}")
                if not set(updates) & target_fields:
                    problems.append(f"mutation without target: {item.get(key)}")
                if action == "close" and updates.get("status") != "closed":
                    problems.append(f"close without closed target: {item.get(key)}")
        totals[kind] = len(entries)
    return {"reviewed": totals, "problems": problems}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "snapshot", type=Path, help="tbd snapshot or retained coverage baseline"
    )
    parser.add_argument("--repo", type=Path, default=REPO)
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--lane", choices=("a", "b"))
    output.add_argument("--reviews", type=Path, nargs="+")
    output.add_argument(
        "--path-repairs", action="store_true", help="show exact former-root moves"
    )
    output.add_argument(
        "--baseline", action="store_true", help="emit only the frozen review scope"
    )
    args = parser.parse_args()
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    is_inventory = isinstance(snapshot, list)
    if not is_inventory and (args.lane or args.path_repairs or args.baseline):
        parser.error("--lane, --path-repairs, and --baseline require a full tbd list snapshot")
    result = inventory(snapshot, args.repo) if is_inventory else snapshot
    if args.path_repairs:
        repairs = result["exact_path_repairs"]
        print(json.dumps({"count": len(repairs), "repairs": repairs}, indent=2))
        return
    if args.baseline:
        print(
            json.dumps(
                {
                    "counts": result["counts"],
                    "beads": sorted(
                        b["id"] for lane in result["lanes"].values() for b in lane["beads"]
                    ),
                    "specs": sorted(
                        s["path"] for lane in result["lanes"].values() for s in lane["specs"]
                    ),
                },
                indent=2,
            )
        )
        return
    if args.reviews:
        coverage = review_coverage(
            result, [json.loads(path.read_text(encoding="utf-8")) for path in args.reviews]
        )
        print(json.dumps(coverage, indent=2))
        raise SystemExit(bool(coverage["problems"]))
    print(json.dumps(result["lanes"][args.lane] if args.lane else result, indent=2))


if __name__ == "__main__":
    main()
