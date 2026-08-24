#!/usr/bin/env python3
"""Check README.md against the directory it describes.

`SYNOPSIS.md` is reconciled against the artifacts by `check_synopsis.py`; README was
not, and it drifted twice in one day for exactly that reason -- it restated defect
counts owned by `defects.yaml` and went stale behind them both times. The counts are
gone now, moved to the generated view that owns them. What is left is the part a
checker can hold: the layout tree, the report index, and the links.

Four checks:

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

Usage:  python3 tools/check_readme.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_synopsis import check_links  # needs the sys.path line above

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
RESEARCH = ROOT / "docs/project/research"
DEFECTS = ROOT / "defects.yaml"

# Tooling that is not part of what the directory *is*: caches, lockfiles, build config.
NOT_CONTENT = {"uv.lock", "pyproject.toml", "__pycache__", ".venv"}

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


def layout_tree(text: str) -> str | None:
    """The fenced block that draws the directory, if README still has one."""
    for block in re.findall(r"```\n(.*?)```", text, re.S):
        if block.lstrip().startswith("explorations/packing/"):
            return block
    return None


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

    on_disk = {
        e.name
        for e in ROOT.iterdir()
        if not e.name.startswith(".") and e.name not in NOT_CONTENT
    }

    problems = [
        f"README.md: {missing} exists but the layout tree does not show it"
        for missing in sorted(on_disk - drawn_top - {README.name})
    ]
    problems += [
        f"README.md: the layout tree shows {drawn}, which does not exist"
        for drawn in sorted(drawn_any)
        if not (ROOT / drawn).exists() and not list(ROOT.rglob(drawn.split("/")[-1]))
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
    data = yaml.safe_load(DEFECTS.read_text(encoding="utf-8"))
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


def main() -> int:
    text = README.read_text(encoding="utf-8")
    problems = (
        check_links(text, README)
        + check_layout(text)
        + check_reports(text)
        + check_defect_summary(text)
    )
    if problems:
        print("README.md has drifted from the directory:", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1
    print("  README.md agrees with the directory, reports, defect source and its own links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
