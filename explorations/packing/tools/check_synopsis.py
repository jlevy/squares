#!/usr/bin/env python3
"""Keep `SYNOPSIS.md` honest against the artifacts it summarises.

The synopsis is the directory's root document and a *living* one: it is revised
every time a round lands, and it restates numbers that live authoritatively
somewhere else. That is exactly the shape of document this repository has already
been bitten by -- a hand-maintained view drifting from its source is D-010, D-017
and D-022, three times in one week.

It cannot be generated: most of it is judgement, and the judgement is the point.
So it is *reconciled* instead, the way `campaign/ideas.md` is -- the numbers and
statuses it asserts must match the artifacts, and every artifact must appear.

Six checks:

  1. every round's verdict in the roll-up matches its artifact
  2. every hypothesis's status matches the ledger's derived status
  3. the round count and effort totals match the ledger
  4. the defect count and per-class counts match `defects.yaml`
  5. no round, hypothesis or open defect is silently missing from the synopsis
  6. every relative link and heading anchor resolves

Check 6 closes a real gap: `campaign/ledger.py` walks links under `campaign/`
only, so the root document's forty-odd references were unchecked.

Usage:  python3 tools/check_synopsis.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SYNOPSIS = ROOT / "SYNOPSIS.md"


def front(path: Path) -> dict:
    """The YAML frontmatter of a soft-schema artifact."""
    return yaml.safe_load(path.read_text().split("---\n")[1])


def slugs(text: str) -> set[str]:
    """GitHub-style heading anchors, plus any explicit `id="..."`."""
    out = {
        re.sub(r"[^a-z0-9\- ]", "", re.sub(r"<[^>]+>", "", h).lower()).strip().replace(" ", "-")
        for h in re.findall(r"^#{1,6}\s+(.*)$", text, re.M)
    }
    return out | set(re.findall(r'id="([^"]+)"', text))


def check_links(text: str, doc: Path = SYNOPSIS) -> list[str]:
    """Relative links resolve, and fragments name a real heading.

    Takes the document so `check_readme.py` can reuse it: the two high-level documents
    cross-reference each other constantly, and a dead link in either is the same defect.
    """
    label = doc.name
    problems = []
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        path, _, frag = target.partition("#")
        if not path:  # in-document anchor
            if frag not in slugs(text):
                problems.append(f"{label}: no such section '#{frag}'")
            continue
        resolved = (doc.parent / path).resolve()
        if not resolved.exists():
            problems.append(f"{label}: dead link -> {target}")
        elif frag and resolved.suffix == ".md" and frag not in slugs(resolved.read_text()):
            problems.append(f"{label}: dead anchor -> {target}")
    return problems


def check_rounds(text: str) -> list[str]:
    """Every round appears, and the verdict shown is the verdict recorded."""
    problems = []
    shown: dict[str, str] = {}
    for rid, rest in re.findall(r"\| \[(exp-\d{3})\]\([^)]+\) \|(.+)\|\n", text):
        cells = [c.strip().replace("*", "") for c in rest.split("|")]
        if len(cells) >= 6:  # the roll-up table, not the cost table
            shown.setdefault(rid, cells[-1])

    for path in sorted(ROOT.glob("campaign/series/*/experiments/exp-*.md")):
        experiment = front(path)["experiment"]
        rid = experiment["id"]
        recorded = experiment["verdict"]["decision"]
        if rid not in shown:
            problems.append(f"SYNOPSIS.md: {rid} is not in the roll-up table")
        elif shown[rid] != recorded:
            problems.append(
                f"SYNOPSIS.md: {rid} shown as '{shown[rid]}', artifact says '{recorded}'"
            )
    return problems


def check_hypotheses(text: str) -> list[str]:
    """Every hypothesis appears, with the status the ledger derives for it.

    Read from the generated `ledger.md` rather than re-derived from the artifacts.
    Status is a derived quantity with real precedence rules (a rejected cell outranks
    an accepted one, because a swept claim is universally quantified), and a second
    implementation of that logic here would be one more thing to keep in step.
    The ledger's own freshness is already checked by `campaign/ledger.py --check`.
    """
    ledger = (ROOT / "campaign" / "ledger.md").read_text()
    derived = dict(re.findall(r"^\| (H-\d{3}) \| (\S+) \|", ledger, re.M))
    if not derived:
        return ["campaign/ledger.md: no registry table to check against"]

    shown = dict(
        re.findall(
            r"\[(H-\d{3})\]\([^)]+\) \| \*{0,2}([a-z ]+?)\*{0,2}(?: as stated)? \|", text
        )
    )

    problems = []
    for hid, status in sorted(derived.items()):
        if hid not in shown:
            problems.append(f"SYNOPSIS.md: {hid} is not in the registry table")
        elif shown[hid].strip() != status:
            problems.append(
                f"SYNOPSIS.md: {hid} shown as '{shown[hid].strip()}', ledger says '{status}'"
            )
    return problems


def check_totals(text: str) -> list[str]:
    """The round count and effort totals match the ledger's generated footer."""
    ledger = (ROOT / "campaign" / "ledger.md").read_text()
    line = re.search(
        r"^(\d+) rounds, ([\d.]+) agent-minutes, ([\d.]+) wall-minutes\.$", ledger, re.M
    )
    if not line:
        return ["campaign/ledger.md: no effort total to check against"]
    rounds, agent, wall = line.groups()

    problems = []
    words = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
    ]
    spelled = words[int(rounds)] if int(rounds) < len(words) else rounds
    if not re.search(rf"\b({rounds}|{spelled})\b rounds", text, re.I):
        problems.append(f"SYNOPSIS.md: does not say there are {rounds} rounds")
    for value, label in ((agent, "agent-minutes"), (wall, "wall-minutes")):
        if f"{value} {label}" not in text:
            problems.append(f"SYNOPSIS.md: effort total '{value} {label}' not stated")
    return problems


# fmt: off
_ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen",
]
_TENS = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty",
    "ninety",
]
# fmt: on


def spell(n: int) -> str:
    """Spell a count the way prose does, so the check accepts either form.

    The synopsis writes "Twenty-six defects", not "26". This was a four-entry lookup
    table covering 21-24, which would have stopped matching at 25 without failing --
    the check would just have demanded the digits. Prose here never exceeds two digits.
    """
    if n < 0 or n > 99:
        return str(n)
    if n < 20:
        return _ONES[n]
    tens, ones = divmod(n, 10)
    return _TENS[tens] if ones == 0 else f"{_TENS[tens]}-{_ONES[ones]}"


def check_defects(text: str) -> list[str]:
    """The defect count and per-class counts match the dataset."""
    data = yaml.safe_load((ROOT / "defects.yaml").read_text())
    defects = data["defects"]

    problems = []
    total = len(defects)
    if not re.search(rf"\b({total}|{spell(total)})\b", text, re.I):
        problems.append(f"SYNOPSIS.md: does not state the defect count ({total})")

    counts: dict[str, int] = {}
    for defect in defects:
        counts[defect["class"]] = counts.get(defect["class"], 0) + 1
    for name, count in sorted(counts.items()):
        if not re.search(rf"\| {name} \| {count} \|", text):
            problems.append(
                f"SYNOPSIS.md: class table says wrong count for {name} (is {count})"
            )

    # The unprotected-fix count. This is the log's most actionable claim -- the list
    # that predicts what comes back -- and it is the one that drifted: the synopsis said
    # "Six" while the generated view said seven, which is D-028 recurring in the document
    # D-028 was about. The same rule as the flattering-direction claim applies: derive it,
    # do not assert it.
    unprotected = sum(
        1 for d in defects if d["regression"] == "none" and d["status"] != "outstanding"
    )
    if not re.search(rf"\b({unprotected}|{spell(unprotected)}) fixes left no", text, re.I):
        problems.append(
            f"SYNOPSIS.md: does not state the unprotected-fix count ({unprotected}) "
            'in the form "<n> fixes left no regression check behind"'
        )

    problems.extend(
        f"SYNOPSIS.md: open defect {d['id']} is not mentioned"
        for d in defects
        if d["status"] in ("outstanding", "contained") and d["id"] not in text
    )
    return problems


def main() -> int:
    text = SYNOPSIS.read_text()
    problems = (
        check_links(text)
        + check_rounds(text)
        + check_hypotheses(text)
        + check_totals(text)
        + check_defects(text)
    )
    if problems:
        print("SYNOPSIS.md has drifted from the artifacts:", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1
    print("  SYNOPSIS.md agrees with the artifacts, the ledger and the defect log")
    return 0


if __name__ == "__main__":
    sys.exit(main())
