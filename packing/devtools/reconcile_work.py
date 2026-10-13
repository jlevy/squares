"""Inventory bead/spec drift for a human-reviewed reconciliation; never mutate beads.

Read a ``tbd list --all --json`` snapshot, including closed children so an
undecomposed epic cannot be mistaken for a completed one. Emit disjoint review queues
with explicit coverage; a flag is a question to investigate, not a verdict.
Children are direct children only, and the default spec lanes alternate by sorted path,
so a lane assignment is stable only against the frozen baseline it was cut from.

Modes, each printing JSON:

- the default inventory, or one lane with ``--lane``; ``--split N`` regroups the queues
  so each spec travels with the beads it governs, and ``--prior`` carries an earlier
  round's dispositions onto the items it reviewed;
- ``--baseline`` freezes the review scope, and ``--reviews`` checks lane records against
  a snapshot or that baseline: every item disposed of exactly once, with evidence;
- ``--path-repairs`` lists exact former-root moves;
- ``--duplicates`` lists bead pairs whose titles share most of their words;
- ``--needs-evidence`` lists what earlier rounds left waiting on a named fact and is
  still open, so that list has one place to be worked down from;
- ``--branch-only-paths`` lists beads whose ``spec_path`` exists here but not at a ref;
- ``--check-commits`` checks that every commit a close cites is on ``--base``, and needs
  no snapshot;
- ``--verify`` checks a fresh snapshot, the beads' ``tbd show`` records and the tree
  against applied dispositions, and fails when it recognizes nothing.

Every mode but ``--check-commits`` needs a full ``tbd list --all --json`` snapshot, apart
from ``--reviews``, which also takes a retained baseline. Records are passed oldest
first wherever several are read.
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
#: Dispositions that change nothing, so a record of them has nothing to verify.
UNCHANGED_ACTIONS = frozenset({"needs_evidence", "retain"})
#: Round 1's applied receipt records what was done, in the past tense, with each target
#: beside the action; later records carry the lane action and its ``updates``.
APPLIED_ACTIONS = frozenset({"closed", "closed_duplicate", "notes_updated", "updated"})
#: The fields a ``tbd list --all --json`` snapshot carries; the rest need ``tbd show``.
SNAPSHOT_FIELDS = frozenset({"spec_path", "status"})
SHOW_BATCH = 100
#: A field a record says it set without recording the value, such as round 1's notes
#: and close reasons: counted as unchecked, never compared.
UNRECORDED = "<unrecorded>"
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

    A spec matches the path the earlier round reviewed, or the folder it moved the spec
    to; failing both, its filename, but only while one spec in the report carries that
    name, since the same name can stand in two folders. The prior disposition is
    context for the reviewer, not a verdict carried forward.
    """
    beads = {
        str(item["id"]): {"action": item.get("action"), "reason": item.get("reason")}
        for review in reviews
        for item in review.get("beads", [])
    }
    by_path: dict[str, dict[str, Any]] = {}
    by_name: dict[str, dict[str, Any]] = {}
    for review in reviews:
        for item in review.get("specs", []):
            path, action = str(item["path"]), str(item.get("action", ""))
            prior = {"action": item.get("action"), "reason": item.get("reason")}
            by_path[path] = by_name[Path(path).name] = prior
            if action.startswith("move_"):
                by_path[
                    f"docs/project/specs/{action.removeprefix('move_')}/{Path(path).name}"
                ] = prior
    names = Counter(
        Path(str(spec["path"])).name
        for lane in report["lanes"].values()
        for spec in lane["specs"]
    )
    for lane in report["lanes"].values():
        for bead in lane["beads"]:
            if (prior := beads.get(str(bead["id"]))) is not None:
                bead["prior"] = prior
        for spec in lane["specs"]:
            path = str(spec["path"])
            prior = by_path.get(path)
            if prior is None and names[Path(path).name] == 1:
                prior = by_name.get(Path(path).name)
            if prior is not None:
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
            if kind == "beads" and action in UNCHANGED_ACTIONS and item.get("updates"):
                problems.append(
                    f"updates on a disposition that changes nothing: {item.get(key)}"
                )
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
                if action == "close" and not str(updates.get("close_reason") or "").strip():
                    problems.append(f"close without close_reason: {item.get(key)}")
                if updates.get("duplicate_of") == item.get(key):
                    problems.append(f"duplicate of itself: {item.get(key)}")
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


def recorded_targets(item: dict[str, Any]) -> tuple[dict[str, Any], int | None] | None:
    """The fields one bead disposition set, and the version it was applied against.

    ``None`` for a disposition that changes nothing. Round 1's past-tense actions carry
    their targets beside the action, and record neither a close's reason nor the text
    ``notes_updated`` wrote, so those targets are ``UNRECORDED``. A close always targets
    ``closed``, whether or not its record says so. Raises ``ValueError`` for an action
    outside both vocabularies, and for a receipt item that records no target.
    """
    action = item.get("action")
    if action in UNCHANGED_ACTIONS:
        return None
    if action in {"close", "update"}:
        updates = dict(item.get("updates") or {})
        version = updates.pop("expected_version", None)
        for guard in EXPECTED_UPDATE_FIELDS:
            updates.pop(guard, None)
        if action == "close":
            updates.setdefault("status", "closed")
            updates.setdefault("resolution", "completed")
        return updates, version
    if action not in APPLIED_ACTIONS:
        raise ValueError(f"unknown bead action: {item.get('id')}: {action}")
    version = item.get("previous_version")
    closed = {"status": "closed", "close_reason": UNRECORDED}
    if action == "closed":
        return {**closed, "resolution": "completed"}, version
    if action == "closed_duplicate":
        duplicate = {"resolution": "duplicate", "duplicate_of": item.get("duplicate_of")}
        return {**closed, **duplicate}, version
    if action == "notes_updated":
        return {"notes": UNRECORDED}, version
    if "hold" in item:
        return {"hold": item["hold"]}, version
    raise ValueError(f"receipt item with no recorded target: {item.get('id')}: {action}")


def show_records(ids: list[str], repo: Path) -> dict[str, dict[str, Any]]:
    """The full ``tbd show --json`` record of each bead, by public ID, read in batches."""
    shown: dict[str, dict[str, Any]] = {}
    for start in range(0, len(ids), SHOW_BATCH):
        listed = subprocess.run(
            [
                "tbd",
                "show",
                "--json",
                "--no-parent",
                "--ignore-missing",
                *ids[start : start + SHOW_BATCH],
            ],
            cwd=repo,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        records = json.loads(listed) if listed.strip() else []
        for record in records if isinstance(records, list) else [records]:
            shown[str(record.get("displayId") or record.get("id"))] = record
    return shown


def applied_expectations(
    reviews: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, int], list[list[str]], set[str], list[str]]:
    """What a sequence of records, oldest first, leaves each bead and spec holding.

    For each bead field the latest record wins; a close clears an earlier hold, as tbd
    requires before closing; appended notes accumulate under ``notes_append``; and the
    version guard keeps the highest version a mutation was applied against. Each moved
    spec is followed as one chain of places, so a spec moved twice ends at its last.
    The places whose plans a record gave a ``new_status`` are returned too.
    """
    expected: dict[str, dict[str, Any]] = {}
    versions: dict[str, int] = {}
    chains: list[list[str]] = []
    at: dict[str, int] = {}
    statuses: set[str] = set()
    problems: list[str] = []

    def target(bead_id: str, fields: dict[str, Any], version: Any) -> None:
        current = expected.setdefault(bead_id, {})
        if fields.get("status") == "closed":
            current.pop("hold", None)
        if (appended := fields.pop("notes_append", None)) is not None:
            current.setdefault("notes_append", []).append(str(appended))
        current.update(fields)
        if type(version) is int:
            versions[bead_id] = max(versions.get(bead_id, version), version)

    for review in reviews:
        for spec in review.get("specs", []):
            path, action = str(spec.get("path", "")), str(spec.get("action", ""))
            if "new_status" in spec:
                folder = action.removeprefix("move_") if action.startswith("move_") else ""
                place = f"docs/project/specs/{folder}/{Path(path).name}" if folder else path
                statuses.add(place)
            if action in UNCHANGED_ACTIONS or action == "update_status":
                continue
            if action not in SPEC_ACTIONS:
                problems.append(f"unknown spec action: {path}: {action}")
                continue
            new = f"docs/project/specs/{action.removeprefix('move_')}/{Path(path).name}"
            index = at.pop(path, None)
            if index is None:
                index = len(chains)
                chains.append([path])
            chains[index].append(new)
            at[new] = index
        for item in review.get("beads", []):
            try:
                recorded = recorded_targets(item)
            except ValueError as error:
                problems.append(str(error))
                continue
            if recorded is not None:
                target(str(item.get("id")), *recorded)
        receipt = review.get("receipt") or {}
        for repair in [*review.get("path_repairs", []), *receipt.get("path_repoints", [])]:
            target(
                str(repair["id"]), {"spec_path": repair["to"]}, repair.get("previous_version")
            )
    return expected, versions, chains, statuses, problems


def verify_applied(
    beads: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
    repo: Path,
    shown: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Check a fresh snapshot and tree against the dispositions that were applied.

    Pass the records oldest first: the latest record wins for each bead field, so a
    repair a later round superseded is not a problem, and a spec moved twice is checked
    at its last place, with no bead left naming any place it left. Round 1's receipt
    (past-tense actions and ``path_repairs``) is read as well as the lane shape, and so
    are the ``path_repoints`` later receipts record for beads that named a moved plan.

    A list snapshot shows only ``status`` and ``spec_path``. With ``shown``, the beads'
    ``tbd show --json`` records, the resolution, ``duplicate_of``, ``close_reason``,
    hold, appended notes and the version guard are checked too. Whatever stays
    unchecked is counted by field, including each plan's recorded ``new_status``, which
    a status line wrapped and retyped by the formatter cannot be matched against; an
    unknown action is a problem, and so is a set of records in which nothing could be
    verified.
    """
    expected, versions, chains, statuses, problems = applied_expectations(reviews)
    by_id = {str(bead["id"]): bead for bead in beads}
    public = {
        str(bead["internalId"]): str(bead["id"]) for bead in beads if "internalId" in bead
    }
    for bead_id, record in (shown or {}).items():
        if record.get("id"):
            public.setdefault(str(record["id"]), bead_id)
    unchecked: Counter[str] = Counter()
    checked = 0
    final: dict[str, str] = {}
    for chain in chains:
        last = chain[-1]
        checked += 1
        if not (repo / last).is_file():
            problems.append(f"moved spec missing from {last}")
        for place in dict.fromkeys(chain[:-1]):
            if place != last:
                final[place] = last
                if (repo / place).exists():
                    problems.append(f"moved spec still at {place}")
    if statuses:
        unchecked["new_status"] = len({final.get(place, place) for place in statuses})
    for bead_id, fields in expected.items():
        if shown is not None:
            if bead_id not in shown:
                problems.append(f"bead not shown by tbd: {bead_id}")
                continue
            bead = shown[bead_id]
        elif bead_id in by_id:
            bead = by_id[bead_id]
        else:
            problems.append(f"bead not in snapshot: {bead_id}")
            continue
        for name in sorted(fields):
            want = fields[name]
            if want == UNRECORDED or (shown is None and name not in SNAPSHOT_FIELDS):
                unchecked[name] += 1
                continue
            checked += 1
            if name == "notes_append":
                notes = str(bead.get("notes") or "")
                if not all(text.strip() in notes for text in want):
                    problems.append(f"notes lack the appended text: {bead_id}")
                continue
            have = bead.get(name)
            if name == "spec_path":
                want = final.get(str(want), want)
            elif name == "resolution":
                have = have or "completed"
            elif name == "duplicate_of" and have is not None:
                have = public.get(str(have), have)
            elif name == "close_reason":
                have, want = str(have or "").strip(), str(want or "").strip()
            if have == want:
                continue
            if name == "status":
                problems.append(f"not closed: {bead_id} is {have}")
            else:
                shown_value = repr(have) if name == "close_reason" else have
                problems.append(f"{name} not applied: {bead_id} has {shown_value}")
        if bead_id in versions:
            if shown is None:
                unchecked["version"] += 1
            else:
                checked += 1
                if int(bead.get("version", 0)) <= versions[bead_id]:
                    problems.append(
                        f"version not advanced: {bead_id} is at {bead.get('version')}, "
                        f"recorded as applied at {versions[bead_id]}"
                    )
    stale = sorted(str(b["id"]) for b in beads if str(b.get("spec_path") or "") in final)
    problems.extend(f"bead still names a moved spec's old path: {bead}" for bead in stale)
    if not checked:
        problems.append("nothing verified: no recognized close, update, move or path repair")
    return {
        "checked": checked,
        "unchecked": sum(unchecked.values()),
        "unchecked_fields": dict(sorted(unchecked.items())),
        "source": "tbd show" if shown is not None else "snapshot",
        "problems": problems,
    }


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

    ``base`` must resolve, so fetch it first. Tokens that name no commit here are listed
    as unresolved: digests, other repositories' commits, and commits of this repository
    that were never fetched, which is why ``--strict`` can fail on them.
    """

    def git(*arguments: str) -> int:
        return subprocess.run(
            ["git", "-C", str(repo), *arguments], capture_output=True, check=False
        ).returncode

    problems: list[str] = []
    if git("rev-parse", "--verify", "--quiet", f"{base}^{{commit}}"):
        problems.append(f"base does not resolve to a commit: {base}")
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
                elif not problems and git("merge-base", "--is-ancestor", token, base):
                    off_base.append(f"{item['id']}: {token} is not on {base}")
    return {
        "base": base,
        "closes": closes,
        "citing_commits": citing,
        "off_base": off_base,
        "unresolved": unresolved,
        "note": (
            "unresolved tokens name no commit here: digests, other repositories' commits, "
            "or this repository's commits not fetched here"
        ),
        "problems": problems,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "snapshot",
        type=Path,
        nargs="?",
        help="tbd snapshot or retained coverage baseline; --check-commits needs none",
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
        help="check that every commit a close cites is on --base",
    )
    output.add_argument(
        "--verify",
        type=Path,
        nargs="+",
        metavar="REVIEW",
        help="check a fresh snapshot, tbd show and the tree against applied dispositions",
    )
    parser.add_argument(
        "--base", default="origin/main", help="--check-commits: the ref closes must be on"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="--check-commits: also fail on tokens that name no commit here",
    )
    parser.add_argument(
        "--snapshot-only",
        action="store_true",
        help="--verify: read only the snapshot, and count what it cannot show",
    )
    parser.add_argument(
        "--split", type=int, metavar="N", help="regroup into N lanes by governing spec"
    )
    parser.add_argument(
        "--prior", type=Path, nargs="+", help="annotate items with earlier dispositions"
    )
    args = parser.parse_args()
    if args.check_commits:
        cited = cited_commits(
            [json.loads(path.read_text(encoding="utf-8")) for path in args.check_commits],
            args.repo,
            args.base,
        )
        print(json.dumps(cited, indent=2))
        failed = cited["off_base"] or cited["problems"] or (args.strict and cited["unresolved"])
        raise SystemExit(bool(failed))
    if args.snapshot is None:
        parser.error("a snapshot is required except with --check-commits")
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
        reviews = [json.loads(path.read_text(encoding="utf-8")) for path in args.verify]
        shown = (
            None
            if args.snapshot_only
            else show_records(sorted(applied_expectations(reviews)[0]), args.repo)
        )
        verified = verify_applied(snapshot, reviews, args.repo, shown)
        print(json.dumps(verified, indent=2))
        raise SystemExit(bool(verified["problems"]))
    if args.split is not None and args.split < 1:
        parser.error("--split needs a positive lane count")
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
