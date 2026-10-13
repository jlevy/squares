"""Inventory bead/spec drift for a human-reviewed reconciliation; never mutate beads.

Read a ``tbd list --all --json`` snapshot, including closed children so an
undecomposed epic cannot be mistaken for a completed one. Emit disjoint review queues
with explicit coverage; a flag is a question to investigate, not a verdict.
``--split N`` regroups the queues so each spec travels with the beads it governs, and
``--prior`` carries an earlier round's dispositions onto the items it reviewed.
Children are direct children only, and the default spec lanes alternate by sorted path,
so a lane assignment is stable only against the frozen baseline it was cut from.
``--needs-evidence`` lists what earlier rounds left waiting on a named fact and is still
open, so that list has one place to be worked down from.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
FIRST_LANE = frozenset("0123456789abcdefgh")
OLD_ROOT = "explorations/packing/"
BEAD_ACTIONS = frozenset({"close", "update", "retain", "needs_evidence"})
SPEC_ACTIONS = frozenset(
    {
        "move_active",
        "move_archive",
        "move_done",
        "move_draft",
        "move_future",
        "move_paused",
        "needs_evidence",
        "retain",
        "update_status",
    }
)
EXPECTED_UPDATE_FIELDS = frozenset({"expected_delegate", "expected_status", "expected_version"})
TARGET_UPDATE_FIELDS = {
    "close": frozenset({"close_reason", "duplicate_of", "resolution", "status"}),
    "update": frozenset({"hold", "notes_append", "spec_path"}),
}
CLOSE_RESOLUTIONS = frozenset({"canceled", "completed", "duplicate"})
# A spec is read in full and decides the folder for every bead it governs, so it
# costs a reviewer several beads' worth of time when lanes are balanced.
SPEC_REVIEW_WEIGHT = 5
STATUS_SCAN_LINES = 40
# Words too common in bead titles to say two beads share a subject.
TITLE_STOPWORDS = frozenset(
    [
        "a",
        "an",
        "and",
        "as",
        "at",
        "by",
        "for",
        "from",
        "in",
        "into",
        "is",
        "it",
        "its",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    ]
)
DUPLICATE_THRESHOLD = 0.6
# A commit-shaped token with at least one hex letter; all-digit runs are comment and run ids,
# so a short hash that happens to be all digits is not read as a commit (cite full hashes).
COMMIT_TOKEN = re.compile(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b")
STATUS_LINE = re.compile(r"\bstatus\b\W{0,4}:\W{0,4}\s*(.+)", re.IGNORECASE)


def current_path(path: str, repo: Path) -> str:
    """Recognize the exact former root only when its replacement exists."""
    candidate = path.removeprefix(OLD_ROOT)
    return candidate if path.startswith(OLD_ROOT) and (repo / candidate).is_file() else path


def status_line(text: str) -> str:
    """Return the spec's own status claim, whole, from its head or frontmatter."""
    for line in text.splitlines()[:STATUS_SCAN_LINES]:
        if match := STATUS_LINE.search(line):
            return match.group(1).strip().rstrip("\\").strip()
    return ""


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
        direct_children = children.get(bead_id, [])
        item["children_total"] = len(direct_children)
        item["children_nonclosed"] = sum(b.get("status") != "closed" for b in direct_children)
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
        if direct_children and not item["children_nonclosed"]:
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
                "folder": path.parent.name,
                "status_line": status_line(text),
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


def split_lanes(report: dict[str, Any], count: int, repo: Path) -> dict[str, Any]:
    """Regroup an inventory into ``count`` lanes, keeping each spec with its beads.

    A bead goes with the document its ``spec_path`` names, so one reviewer decides a
    spec's folder together with the work it governs. Groups are placed largest first on
    the least-loaded lane, which is deterministic for a given snapshot.
    """
    if count < 1:
        raise ValueError("lane count must be positive")
    groups: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for lane in report["lanes"].values():
        for spec in lane["specs"]:
            groups.setdefault(spec["path"], {"beads": [], "specs": []})["specs"].append(spec)
        for bead in lane["beads"]:
            governing = current_path(str(bead.get("spec_path") or ""), repo)
            key = governing or f"bead:{bead['id']}"
            groups.setdefault(key, {"beads": [], "specs": []})["beads"].append(bead)

    def weight(group: dict[str, list[dict[str, Any]]]) -> int:
        return len(group["beads"]) + SPEC_REVIEW_WEIGHT * len(group["specs"])

    names = [str(index) for index in range(1, count + 1)]
    lanes: dict[str, dict[str, list[dict[str, Any]]]] = {
        name: {"beads": [], "specs": []} for name in names
    }
    load = dict.fromkeys(names, 0)
    for key in sorted(groups, key=lambda key: (-weight(groups[key]), key)):
        target = min(names, key=lambda name: (load[name], int(name)))
        lanes[target]["beads"].extend(groups[key]["beads"])
        lanes[target]["specs"].extend(groups[key]["specs"])
        load[target] += weight(groups[key])
    for lane in lanes.values():
        lane["beads"].sort(key=lambda bead: str(bead["id"]))
        lane["specs"].sort(key=lambda spec: str(spec["path"]))
    counts = dict(report["counts"])
    counts.pop("lane_a_beads", None)
    counts.pop("lane_b_beads", None)
    counts.update({f"lane_{name}_beads": len(lanes[name]["beads"]) for name in names})
    return {**report, "counts": counts, "lanes": lanes}


def annotate_prior(report: dict[str, Any], reviews: list[dict[str, Any]]) -> dict[str, Any]:
    """Attach an earlier round's disposition to each item it covered.

    Specs match by filename, since an earlier round may have moved them between
    lifecycle folders. The prior disposition is context for the reviewer, not a verdict
    carried forward.
    """
    beads = {
        str(item["id"]): {"action": item.get("action"), "reason": item.get("reason")}
        for review in reviews
        for item in review.get("beads", [])
    }
    specs = {
        Path(str(item["path"])).name: {
            "action": item.get("action"),
            "reason": item.get("reason"),
        }
        for review in reviews
        for item in review.get("specs", [])
    }
    for lane in report["lanes"].values():
        for bead in lane["beads"]:
            if (prior := beads.get(str(bead["id"]))) is not None:
                bead["prior"] = prior
        for spec in lane["specs"]:
            if (prior := specs.get(Path(str(spec["path"])).name)) is not None:
                spec["prior"] = prior
    return report


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
                resolution = updates.get("resolution", "completed")
                if action == "close" and resolution not in CLOSE_RESOLUTIONS:
                    problems.append(f"unknown close resolution: {item.get(key)}")
                if action == "close" and (resolution == "duplicate") != bool(
                    updates.get("duplicate_of")
                ):
                    problems.append(
                        f"duplicate close needs exactly one target: {item.get(key)}"
                    )
        totals[kind] = len(entries)
    return {"reviewed": totals, "problems": problems}


def branch_only_paths(
    beads: list[dict[str, Any]], repo: Path, ref: str = "origin/main"
) -> dict[str, Any]:
    """Beads whose ``spec_path`` exists in this tree but not at ``ref``.

    A repair applied ahead of the move it follows lands on the shared tracker at once,
    while the file reaches ``ref`` only when the change merges; until then these beads
    dangle there, and a declined move leaves them dangling for good.
    """
    present: dict[str, bool] = {}

    def on_ref(path: str) -> bool:
        if path not in present:
            present[path] = (
                subprocess.run(
                    ["git", "-C", str(repo), "cat-file", "-e", f"{ref}:{path}"],
                    capture_output=True,
                    check=False,
                ).returncode
                == 0
            )
        return present[path]

    listed = subprocess.run(
        ["git", "-C", str(repo), "config", "-f", ".gitmodules", "--get-regexp", "path"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    submodules = tuple(f"{line.split()[1]}/" for line in listed.splitlines() if line.strip())
    found = sorted(
        (str(bead["id"]), str(bead.get("status")), str(bead["spec_path"]))
        for bead in beads
        if bead.get("spec_path")
        and not str(bead["spec_path"]).startswith(submodules)
        and (repo / str(bead["spec_path"])).is_file()
        and not on_ref(str(bead["spec_path"]))
    )
    by_path: dict[str, int] = {}
    for _, _, path in found:
        by_path[path] = by_path.get(path, 0) + 1
    return {
        "ref": ref,
        "beads": len(found),
        "nonclosed": sum(status != "closed" for _, status, _ in found),
        "by_path": dict(sorted(by_path.items(), key=lambda item: (-item[1], item[0]))),
        "items": [{"id": i, "status": st, "spec_path": sp} for i, st, sp in found],
    }


def open_needs_evidence(
    beads: list[dict[str, Any]], reviews: list[dict[str, Any]], repo: Path
) -> dict[str, Any]:
    """Every item a review left at ``needs_evidence`` that is still open, with its question.

    A later review of the same item supersedes an earlier one, so pass the rounds oldest
    first; an item a later round decided drops out. Beads are open while not closed, and
    specs while the reviewed file is still in place.
    """
    status = {str(bead["id"]): bead.get("status") for bead in beads}
    latest: dict[tuple[str, str], dict[str, Any]] = {}
    for review in reviews:
        for kind, key in (("beads", "id"), ("specs", "path")):
            for item in review.get(kind, []):
                latest[(kind, str(item[key]))] = item
    waiting = [
        {"kind": kind[:-1], "id": ident, "reason": item.get("reason", "")}
        for (kind, ident), item in sorted(latest.items())
        if item.get("action") == "needs_evidence"
        and (
            status.get(ident) not in (None, "closed")
            if kind == "beads"
            else (repo / ident).is_file()
        )
    ]
    return {"open": len(waiting), "items": waiting}


def verify_applied(
    beads: list[dict[str, Any]], reviews: list[dict[str, Any]], repo: Path
) -> dict[str, Any]:
    """Check a fresh snapshot and tree against the dispositions that were applied.

    Every close is closed, every ``spec_path`` update holds, every moved spec stands in
    its new folder and not its old one, and no bead still names a moved spec's old
    path. Holds and notes are not in a list snapshot, so they are counted, not checked.
    """
    by_id = {str(bead["id"]): bead for bead in beads}
    moved: dict[str, str] = {}
    problems: list[str] = []
    checked = unverifiable = 0
    for review in reviews:
        for spec in review.get("specs", []):
            action = str(spec.get("action", ""))
            if not action.startswith("move_"):
                continue
            old = str(spec["path"])
            new = f"docs/project/specs/{action.removeprefix('move_')}/{Path(old).name}"
            moved[old] = new
            checked += 1
            if not (repo / new).is_file():
                problems.append(f"moved spec missing from {new}")
            if (repo / old).exists():
                problems.append(f"moved spec still at {old}")
    for review in reviews:
        for item in review.get("beads", []):
            action = item.get("action")
            if action not in {"close", "update"}:
                continue
            bead = by_id.get(str(item["id"]))
            updates = item.get("updates", {})
            if bead is None:
                problems.append(f"bead not in snapshot: {item['id']}")
                continue
            if action == "close":
                checked += 1
                if bead.get("status") != "closed":
                    problems.append(f"not closed: {item['id']} is {bead.get('status')}")
            if "spec_path" in updates:
                checked += 1
                want = moved.get(updates["spec_path"], updates["spec_path"])
                if bead.get("spec_path") != want:
                    problems.append(
                        f"spec_path not applied: {item['id']} has {bead.get('spec_path')}"
                    )
            unverifiable += sum(field in updates for field in ("hold", "notes_append"))
    stale = sorted(str(b["id"]) for b in beads if str(b.get("spec_path") or "") in moved)
    problems.extend(f"bead still names a moved spec's old path: {bead}" for bead in stale)
    return {"checked": checked, "not_in_snapshot": unverifiable, "problems": problems}


def title_tokens(title: str) -> frozenset[str]:
    return frozenset(
        word
        for word in re.findall(r"[a-z0-9]+", title.lower())
        if len(word) > 1 and word not in TITLE_STOPWORDS
    )


def duplicate_candidates(
    beads: list[dict[str, Any]], threshold: float = DUPLICATE_THRESHOLD
) -> list[dict[str, Any]]:
    """Pairs of beads whose titles share most of their words, at least one not closed.

    A closed partner matters as much as an open one: an open bead that repeats finished
    work is a duplicate of it. The score is the Jaccard index of the title words; a pair
    is a question for a reviewer, never a verdict.
    """
    tokens = {str(b["id"]): title_tokens(str(b.get("title", ""))) for b in beads}
    by_id = {str(b["id"]): b for b in beads}
    index: dict[str, set[str]] = {}
    for bead_id, words in tokens.items():
        for word in words:
            index.setdefault(word, set()).add(bead_id)
    pairs: dict[tuple[str, str], float] = {}
    for bead_id, words in tokens.items():
        if by_id[bead_id].get("status") == "closed" or not words:
            continue
        for other in set().union(*(index[word] for word in words)) - {bead_id}:
            key = (min(bead_id, other), max(bead_id, other))
            if key in pairs or not tokens[other]:
                continue
            score = len(words & tokens[other]) / len(words | tokens[other])
            if score >= threshold:
                pairs[key] = score
    return [
        {
            "ids": list(key),
            "score": round(score, 3),
            "statuses": [by_id[key[0]].get("status"), by_id[key[1]].get("status")],
            "same_parent": by_id[key[0]].get("parentId") == by_id[key[1]].get("parentId"),
            "titles": [by_id[key[0]].get("title"), by_id[key[1]].get("title")],
        }
        for key, score in sorted(pairs.items(), key=lambda item: (-item[1], item[0]))
    ]


def cited_commits(
    reviews: list[dict[str, Any]], repo: Path, base: str = "origin/main"
) -> dict[str, Any]:
    """Every commit a close cites must be on ``base``; a close resting on a commit that
    is not is a question to answer before applying it.

    Tokens that do not name a commit at all (digests, abbreviated ids of other things)
    are listed as unresolved, which is information rather than a fault.
    """

    def git(*arguments: str) -> int:
        return subprocess.run(
            ["git", "-C", str(repo), *arguments], capture_output=True, check=False
        ).returncode

    off_base: list[str] = []
    unresolved: list[str] = []
    closes = citing = 0
    for review in reviews:
        for item in review.get("beads", []):
            if item.get("action") != "close":
                continue
            closes += 1
            text = " ".join(
                [
                    str(item.get("reason", "")),
                    *map(str, item.get("evidence", [])),
                    str(item.get("updates", {}).get("close_reason", "")),
                ]
            )
            tokens = sorted(set(COMMIT_TOKEN.findall(text)))
            citing += bool(tokens)
            for token in tokens:
                if git("rev-parse", "--verify", "--quiet", f"{token}^{{commit}}"):
                    unresolved.append(f"{item['id']}: {token}")
                elif git("merge-base", "--is-ancestor", token, base):
                    off_base.append(f"{item['id']}: {token} is not on {base}")
    return {
        "closes": closes,
        "citing_commits": citing,
        "off_base": off_base,
        "unresolved": unresolved,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "snapshot", type=Path, help="tbd snapshot or retained coverage baseline"
    )
    parser.add_argument("--repo", type=Path, default=REPO)
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--lane", help="print one lane: a or b, or 1..N with --split")
    output.add_argument("--reviews", type=Path, nargs="+")
    output.add_argument(
        "--path-repairs", action="store_true", help="show exact former-root moves"
    )
    output.add_argument(
        "--baseline", action="store_true", help="emit only the frozen review scope"
    )
    output.add_argument(
        "--branch-only-paths",
        nargs="?",
        const="origin/main",
        metavar="REF",
        help="list beads whose spec_path exists here but not at REF (origin/main)",
    )
    output.add_argument(
        "--needs-evidence",
        type=Path,
        nargs="+",
        metavar="REVIEW",
        help="list items reviews left at needs_evidence that are still open (oldest first)",
    )
    output.add_argument(
        "--duplicates",
        type=float,
        nargs="?",
        const=DUPLICATE_THRESHOLD,
        metavar="THRESHOLD",
        help="list bead pairs whose titles share most of their words",
    )
    output.add_argument(
        "--check-commits",
        type=Path,
        nargs="+",
        metavar="REVIEW",
        help="check that every commit a close cites is on origin/main",
    )
    output.add_argument(
        "--verify",
        type=Path,
        nargs="+",
        metavar="REVIEW",
        help="check a fresh snapshot and tree against applied dispositions",
    )
    parser.add_argument(
        "--split", type=int, metavar="N", help="regroup into N lanes by governing spec"
    )
    parser.add_argument(
        "--prior", type=Path, nargs="+", help="annotate items with earlier dispositions"
    )
    args = parser.parse_args()
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    is_inventory = isinstance(snapshot, list)
    if not is_inventory and (
        args.lane
        or args.path_repairs
        or args.baseline
        or args.split
        or args.prior
        or args.verify
        or args.duplicates is not None
        or args.needs_evidence
        or args.branch_only_paths
    ):
        parser.error(
            "--lane, --path-repairs, --baseline, --split, --prior, --verify, "
            "--duplicates, --needs-evidence, and --branch-only-paths "
            "require a full tbd list snapshot"
        )
    if args.branch_only_paths:
        print(
            json.dumps(branch_only_paths(snapshot, args.repo, args.branch_only_paths), indent=2)
        )
        return
    if args.needs_evidence:
        pending = open_needs_evidence(
            snapshot,
            [json.loads(path.read_text(encoding="utf-8")) for path in args.needs_evidence],
            args.repo,
        )
        print(json.dumps(pending, indent=2))
        return
    if args.duplicates is not None:
        found = duplicate_candidates(snapshot, args.duplicates)
        print(json.dumps({"threshold": args.duplicates, "pairs": found}, indent=2))
        return
    if args.verify:
        verified = verify_applied(
            snapshot,
            [json.loads(path.read_text(encoding="utf-8")) for path in args.verify],
            args.repo,
        )
        print(json.dumps(verified, indent=2))
        raise SystemExit(bool(verified["problems"]))
    if args.split is not None and args.split < 1:
        parser.error("--split needs a positive lane count")
    if args.check_commits:
        cited = cited_commits(
            [json.loads(path.read_text(encoding="utf-8")) for path in args.check_commits],
            args.repo,
        )
        print(json.dumps(cited, indent=2))
        raise SystemExit(bool(cited["off_base"]))
    result = inventory(snapshot, args.repo) if is_inventory else snapshot
    if args.split:
        result = split_lanes(result, args.split, args.repo)
    if args.prior:
        result = annotate_prior(
            result, [json.loads(path.read_text(encoding="utf-8")) for path in args.prior]
        )
    if args.lane and args.lane not in result["lanes"]:
        parser.error(f"no lane {args.lane!r}; lanes are {', '.join(result['lanes'])}")
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
