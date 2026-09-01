#!/usr/bin/env python3
"""Check README.md against the directory it describes.

`SYNOPSIS.md` is reconciled against the artifacts by `check_synopsis.py`; README was
not, and it drifted twice in one day for exactly that reason -- it restated defect
counts owned by `defects.yaml` and went stale behind them both times. The counts are
gone now, moved to the generated view that owns them. What is left is the part a
checker can hold: the layout tree, the report index, the links, and the work model.

Five checks:

1. **Every link resolves**, including anchors into other documents. README and SYNOPSIS
   cross-reference each other heavily and a dead link between them is invisible until
   someone clicks it. Shared with `check_synopsis.py`, which owns the implementation.
2. **The layout tree matches the directory.** Every top-level entry appears in the tree
   and every path the tree names exists. This is a hand-maintained view of generated
   truth, which is the shape of D-010, D-017, D-022 and D-028, and it was already wrong
   about seven files.
3. **The report index is complete.** The prose says "six research reports" and the table
   lists six; both must match what is in `docs/project/research/`.
4. **The defect summary is derived.** README may state whether the gate has caught a
   soundness defect, but may not repeat a numeric aggregate owned by `defects.yaml`.
5. **The work model agrees.** README and SYNOPSIS must expose the same seven numbered
   workflow entry points, the agent-session schema must be able to record them, and the
   synopsis must define the work units those workflows produce.

Usage: uv run --frozen python -m devtools.check_readme
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from devtools.check_synopsis import check_links
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
# The repository root. The reader-facing documents live there, not under packing/.
REPO = ROOT.parent
README = REPO / "README.md"
SYNOPSIS = REPO / "SYNOPSIS.md"
RESEARCH = REPO / "docs/project/research"
DEFECTS = ROOT / "defects.yaml"
SESSION_SCHEMA = ROOT / "campaign/schemas/agent-session.schema.yaml"

WORK_UNITS = (
    "Packing exploration",
    "Campaign",
    "Series",
    "Agent session",
    "Workflow phase",
    "Focus",
    "Slice",
    "Hypothesis",
    "Experiment",
    "Round",
    "Run",
    "Result",
    "Ledger",
)

# Tooling that is not part of what the directory *is*: caches, lockfiles, build config.
# LICENSE is legal boilerplate rather than orientation content: the layout tree
# may draw it once the README grows its license summary, but its absence from a
# reader's map of the directory is not a documentation defect.
NOT_CONTENT = {"uv.lock", "pyproject.toml", "__pycache__", ".venv", "LICENSE"}
CACHE_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".venv"}
IGNORED_FILES = {".DS_Store"}

_SPELLED = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
}


#: W1 through W8. Bumping this is the deliberate half of adding a workflow; the other
#: half is the two orientation tables in README.md and SYNOPSIS.md, which this check
#: compares against the schema rather than against each other.
EXPECTED_NUMBERED_WORKFLOWS = 8


def layout_tree(text: str) -> str | None:
    """The fenced block that draws the directory, if README still has one."""
    # Anchored on the drawing, not on a path prefix. The tree used to be found by the
    # directory name it opened with, which broke the moment that directory moved; a
    # branch marker is what actually makes a fenced block a tree, and it survives
    # renames.
    #
    # Fences are paired opener-to-closer, with or without a language tag. The old
    # pattern required a bare ``` as the opener, so every ```shell block ahead of the
    # tree shifted the pairing by one and the tree was "found" mid-prose or not at all;
    # which blocks sit ahead of the tree is a presentation choice that must not decide
    # whether this check runs.
    for block in re.findall(r"^```[^\n]*\n(.*?)^```", text, re.S | re.M):
        if "\u251c\u2500\u2500 " in block:
            return block
    return None


def meaningful_top_level_entries(root: Path) -> set[str]:
    """Entries with durable content, excluding cache-only migration remnants."""
    entries: set[str] = set()
    for entry in root.iterdir():
        if entry.name.startswith(".") or entry.name in NOT_CONTENT:
            continue
        if entry.is_file():
            if entry.name not in IGNORED_FILES:
                entries.add(entry.name)
            continue
        if any(
            path.is_file()
            and path.name not in IGNORED_FILES
            and not CACHE_PARTS.intersection(path.relative_to(entry).parts)
            for path in entry.rglob("*")
        ):
            entries.add(entry.name)
    return entries


def _exists_somewhere(name: str) -> bool:
    """Whether a nested tree entry exists anywhere the project keeps content.

    The tree draws nested entries by bare name, so `atlas` under `packing/` has no
    repo-relative path of its own. Search for it, but only through project content:
    walking .git and node_modules to answer a documentation question is pure cost.
    """
    skip = {"node_modules", "__pycache__", ".venv"}
    if any((base / name).exists() for base in (REPO, REPO / "packing")):
        return True
    return any(
        not any(part in skip or part.startswith(".") for part in path.relative_to(REPO).parts)
        for path in REPO.rglob(name)
    )


def check_layout(text: str) -> list[str]:
    """Every top-level entry is drawn, and every drawn path exists."""
    tree = layout_tree(text)
    if tree is None:
        return ["README.md: the layout tree is gone; this check has nothing to hold"]

    # Only a branch marker declares an entry. Continuation lines carry the description
    # of the entry above and start with a bare `|` column, which is why matching "first
    # word on the line" reported a prose word as a missing file.
    top = re.findall(r"^[├└]── ([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*/?)", tree, re.M)
    nested = re.findall(r"^│\s+[├└]── ([A-Za-z0-9_.-]+/?)", tree, re.M)
    # A top-level entry is the first path segment: `docs/project/` lives under `docs`.
    drawn_top = {name.strip("/").split("/")[0] for name in top}
    drawn_any = drawn_top | {name.strip("/") for name in top + nested}

    on_disk = meaningful_top_level_entries(REPO)

    problems = [
        f"README.md: {missing} exists but the layout tree does not show it"
        for missing in sorted(on_disk - drawn_top - {README.name})
    ]
    problems += [
        f"README.md: the layout tree shows {drawn}, which does not exist"
        for drawn in sorted(drawn_any)
        if not (REPO / drawn).exists() and not _exists_somewhere(drawn.split("/")[-1])
    ]
    return problems


def check_reports(text: str) -> list[str]:
    """The prose count, the table, and the directory agree."""
    actual = sorted(p.name for p in RESEARCH.glob("research-*.md"))
    rows = re.findall(r"^\| \[([^\]]+)\]\(([^)]+)\)", text, re.M)
    linked = {Path(target).name for _, target in rows if "docs/project/research/" in target}

    problems = [
        f"README.md: {gone} is not in the reports table"
        for gone in sorted(set(actual) - linked)
    ]
    problems += [
        f"README.md: the reports table lists {extra}, which does not exist"
        for extra in sorted(linked - set(actual))
    ]

    n = len(actual)
    word = _SPELLED.get(n, str(n))
    if not re.search(rf"\b({n}|{word})\s+research reports\b", text, re.I):
        problems.append(
            f"README.md: does not say there are {word} research reports (there are)"
        )
    return problems


def check_defect_summary(text: str) -> list[str]:
    """Keep the README's qualitative gate claim reconciled without copying counts."""
    data = safe_load(DEFECTS.read_text(encoding="utf-8"))
    normalized = re.sub(r"\s+", " ", text)
    gate_soundness = sum(
        1
        for defect in data["defects"]
        if defect["detected_by"] == "gate" and defect["class"] == "soundness"
    )
    zero_claim = "No soundness defect in the log was caught by it."
    problems: list[str] = []
    if gate_soundness == 0 and zero_claim not in normalized:
        problems.append(
            "README.md: must state the derived fact that the gate caught no soundness defect"
        )
    if gate_soundness != 0 and zero_claim in normalized:
        problems.append(
            "README.md: says the gate caught no soundness defect, but defects.yaml disagrees"
        )

    number = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
    if re.search(rf"\bgate\b[^.]*\bcaught\s+{number}\s+defects?\b", normalized, re.I):
        problems.append(
            "README.md: repeats a numeric gate-defect aggregate owned by defects.yaml"
        )
    return problems


def workflow_rows(text: str) -> list[tuple[str, str]]:
    """Numbered workflow rows in a Markdown table."""
    return re.findall(r"^\| (W\d+) \| `([^`]+)` \|", text, re.M)


def check_work_model(text: str) -> list[str]:
    """Keep the human workflow entry points and machine contract in lockstep."""
    synopsis = SYNOPSIS.read_text(encoding="utf-8")
    schema = safe_load(SESSION_SCHEMA.read_text(encoding="utf-8"))
    properties = schema.get("properties", {})
    schema_workflows = (schema.get("$defs") or {}).get("workflow", {}).get("enum", [])
    phase_workflow = (
        properties.get("workflow_phases", {})
        .get("items", {})
        .get("properties", {})
        .get("workflow", {})
    )

    problems: list[str] = []
    if not isinstance(schema_workflows, list) or not all(
        isinstance(workflow, str) and workflow for workflow in schema_workflows
    ):
        problems.append(
            "agent-session.schema.yaml: canonical workflow enum is missing or malformed"
        )
        schema_workflows = []

    # The schema owns names and ordering. Its final enum value is the unnumbered
    # fallback; everything before it receives the compact W1, W2, ... labels used by
    # the two human orientation tables.
    numbered_workflows = schema_workflows[:-1]
    fallback = schema_workflows[-1] if schema_workflows else ""
    expected_rows = [
        (f"W{index}", workflow) for index, workflow in enumerate(numbered_workflows, start=1)
    ]
    # The count is asserted rather than derived on purpose: an enum that silently grows or
    # shrinks would still produce a self-consistent pair of tables, and the point of this
    # check is that a workflow cannot be added without a human editing both orientation
    # tables and this number.
    if len(numbered_workflows) != EXPECTED_NUMBERED_WORKFLOWS or not fallback:
        problems.append(
            f"agent-session.schema.yaml: workflow enum must contain "
            f"{EXPECTED_NUMBERED_WORKFLOWS} numbered workflows followed by one fallback"
        )
    for label, rows in (
        ("README.md", workflow_rows(text)),
        ("SYNOPSIS.md", workflow_rows(synopsis)),
    ):
        if rows != expected_rows:
            problems.append(
                f"{label}: workflow table is {rows or 'missing'}, expected {expected_rows}"
            )
        if fallback and fallback not in (text if label == "README.md" else synopsis):
            problems.append(f"{label}: does not name the {fallback} fallback")
    if phase_workflow.get("$ref") != "#/$defs/workflow":
        problems.append(
            "agent-session.schema.yaml: phase workflow does not reference the canonical enum"
        )
    if "entry_workflow" in properties or "entry_workflow" in schema.get("required", []):
        problems.append(
            "agent-session.schema.yaml: redundant entry_workflow must be derived "
            "from the first phase"
        )

    terminology = re.search(
        r"^### Work Units and Records\s*$\n(?P<body>.*?)(?=^###\s)",
        synopsis,
        re.M | re.S,
    )
    if terminology is None:
        problems.append("SYNOPSIS.md: has no Work Units and Records section")
    else:
        body = terminology.group("body")
        problems.extend(
            f"SYNOPSIS.md: does not define {term}"
            for term in WORK_UNITS
            if not re.search(rf"\*\*{re.escape(term)}(?:\.|\s|\()", body)
        )
    return problems


def main() -> int:
    text = README.read_text(encoding="utf-8")
    problems = (
        check_links(text, README)
        + check_layout(text)
        + check_reports(text)
        + check_defect_summary(text)
        + check_work_model(text)
    )
    if problems:
        print("README.md has drifted from the directory:", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1
    print(
        "  README.md agrees with the directory, reports, defect source, work model "
        "and its own links"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
