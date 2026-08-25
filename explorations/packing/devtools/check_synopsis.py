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

Eleven checks:

  1. every round's verdict in the roll-up matches its artifact
  2. every hypothesis's status and round count match the ledger's derived values
  3. the round count and effort totals match the ledger
  4. the defect count and per-class counts match `defects.yaml`
  5. no round, hypothesis or open defect is silently missing from the synopsis
  6. the stated hypothesis-artifact count matches the registry directory
  7. every relative link and heading anchor resolves
  8. freshness labels name the current round count and do not embed a stale update note
 9. the readiness dashboard remains attached to its canonical status owners
10. living reproducibility instructions do not name removed command paths
11. the cold-start handoff agrees with the latest session and active agenda

Check 7 closes a real gap: `packing-ledger check` walks links under `campaign/`
only, so the root document's forty-odd references were unchecked.

Usage: uv run --frozen python -m devtools.check_synopsis
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SYNOPSIS = ROOT / "SYNOPSIS.md"
README = ROOT / "README.md"
HYPOTHESES = ROOT / "campaign/hypotheses"
AGENT_SESSIONS = ROOT / "campaign/agent-sessions"
AGENDA = ROOT / "campaign/agendas/agenda-001-basin-confidence-ladder.md"
ACTIVE_PLAN = ROOT / "docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md"
DEVELOPMENT = ROOT / "development.md"
READINESS_BEGIN = "<!-- BEGIN CURRENT-RESEARCH-READINESS -->"
READINESS_END = "<!-- END CURRENT-RESEARCH-READINESS -->"
READINESS_SOURCES = (
    "campaign/ledger.md",
    "campaign/agendas/agenda-001-basin-confidence-ladder.md",
    "defects.md",
    "docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md",
    "#what-is-built",
    "#where-this-stands",
)


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
    """Every round appears exactly once in each table, with its recorded verdict."""
    problems = []
    rollup_match = re.search(
        r"^### Roll-up\s*$\n(?P<body>.*?)(?=^### Cost and provenance\s*$)",
        text,
        re.M | re.S,
    )
    cost_match = re.search(
        r"^### Cost and provenance\s*$\n(?P<body>.*?)(?=^###\s)",
        text,
        re.M | re.S,
    )
    if rollup_match is None:
        return ["SYNOPSIS.md: has no Roll-up section"]
    if cost_match is None:
        return ["SYNOPSIS.md: has no Cost and provenance section"]

    shown: dict[str, str] = {}
    rollup_ids: list[str] = []
    for rid, rest in re.findall(
        r"\| \[(exp-\d{3})\]\([^)]+\) \|(.+)\|\n", rollup_match.group("body")
    ):
        cells = [c.strip().replace("*", "") for c in rest.split("|")]
        if len(cells) >= 6:
            rollup_ids.append(rid)
            shown.setdefault(rid, cells[-1])
    rollup_counts = Counter(rollup_ids)
    cost_counts = Counter(re.findall(r"^\| (exp-\d{3}) \|", cost_match.group("body"), re.M))

    for path in sorted(ROOT.glob("campaign/series/*/experiments/exp-*.md")):
        experiment = front(path)["experiment"]
        rid = experiment["id"]
        recorded = experiment["verdict"]["decision"]
        rollup_count = rollup_counts[rid]
        cost_count = cost_counts[rid]
        if rollup_count != 1:
            problems.append(
                f"SYNOPSIS.md: {rid} appears {rollup_count} times in the roll-up table"
            )
        elif shown[rid] != recorded:
            problems.append(
                f"SYNOPSIS.md: {rid} shown as '{shown[rid]}', artifact says '{recorded}'"
            )
        if cost_count != 1:
            problems.append(f"SYNOPSIS.md: {rid} appears {cost_count} times in the cost table")
    return problems


def check_hypotheses(text: str) -> list[str]:
    """Every hypothesis appears, with the status the ledger derives for it.

    Read from the generated `ledger.md` rather than re-derived from the artifacts.
    Status is a derived quantity with real precedence rules (a rejected cell outranks
    an accepted one, because a swept claim is universally quantified), and a second
    implementation of that logic here would be one more thing to keep in step.
    The ledger's own freshness is already checked by `packing-ledger check`.
    """
    ledger = (ROOT / "campaign" / "ledger.md").read_text()
    derived = {
        hid: status.strip()
        for hid, status in re.findall(r"^\| (H-\d{3}) \| ([^|]+) \|", ledger, re.M)
    }
    if not derived:
        return ["campaign/ledger.md: no registry table to check against"]
    derived_rounds = dict(re.findall(r"^\| (H-\d{3}) \|(?:[^|]*\|){4} (\d+) \|", ledger, re.M))

    shown = dict(
        re.findall(
            r"\[(H-\d{3})\]\([^)]+\) \| \*{0,2}([a-z ]+?)\*{0,2}(?: as stated)? \|", text
        )
    )
    shown_rounds = dict(re.findall(r"\[(H-\d{3})\]\([^)]+\) \|(?:[^|]*\|){2} (\d+) \|", text))

    problems = []
    for hid, status in sorted(derived.items()):
        if hid not in shown:
            problems.append(f"SYNOPSIS.md: {hid} is not in the registry table")
        elif shown[hid].strip() != status:
            problems.append(
                f"SYNOPSIS.md: {hid} shown as '{shown[hid].strip()}', ledger says '{status}'"
            )
        # The registry table repeats the ledger's per-hypothesis totals verbatim, so a
        # round landed without touching this table is drift, not a counting convention
        # (H-023 silently lagged exp-039 this way).
        elif hid in shown_rounds and shown_rounds[hid] != derived_rounds.get(hid):
            problems.append(
                f"SYNOPSIS.md: {hid} shows {shown_rounds[hid]} rounds, "
                f"ledger counts {derived_rounds.get(hid)}"
            )

    counts = Counter(derived.values())
    expected_summary = (
        "The generated ledger currently derives "
        f"{counted(counts['confirmed'], 'confirmed hypothesis', 'confirmed hypotheses')}, "
        f"{counted(counts['refuted'], 'refuted hypothesis', 'refuted hypotheses')}, "
        f"{counted(counts['open'], 'open hypothesis', 'open hypotheses')}, "
        f"{counted(counts['open question'], 'open question', 'open questions')}, and "
        f"{counted(counts['blocked'], 'blocked hypothesis', 'blocked hypotheses')}."
    )
    if expected_summary.lower() not in re.sub(r"\s+", " ", text).lower():
        problems.append(
            "SYNOPSIS.md: hypothesis-status aggregate does not match campaign/ledger.md; "
            f"expected '{expected_summary}'"
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
    if not re.search(
        rf"^### What the {rounds} rounds jointly establish\s*$", text, re.I | re.M
    ):
        problems.append(
            f"SYNOPSIS.md: synthesis heading does not name the current round count ({rounds})"
        )
    for value, label in ((agent, "agent-minutes"), (wall, "wall-minutes")):
        if f"{value} {label}" not in text:
            problems.append(f"SYNOPSIS.md: effort total '{value} {label}' not stated")
    return problems


def check_freshness_label(text: str) -> list[str]:
    """The dateline may state a date, but not duplicate volatile campaign state."""
    dateline = re.search(r"^\*\*Date:\*\*.*$", text, re.M)
    if dateline is None:
        return ["SYNOPSIS.md: has no Date dateline"]
    if not re.fullmatch(r"\*\*Date:\*\* \d{4}-\d{2}-\d{2}", dateline.group(0)):
        return [
            (
                "SYNOPSIS.md: Date dateline repeats campaign progress or is not an ISO "
                "date; the ledger owns progress"
            )
        ]
    return []


def check_readiness_dashboard(text: str) -> list[str]:
    """The top-level readiness view exists once and links to canonical status owners."""
    begin_count = text.count(READINESS_BEGIN)
    end_count = text.count(READINESS_END)
    if begin_count != 1 or end_count != 1:
        message = (
            "SYNOPSIS.md: readiness dashboard needs exactly one ordered marker pair "
            f"(found {begin_count} begin, {end_count} end)"
        )
        return [message]

    begin = text.index(READINESS_BEGIN)
    end = text.index(READINESS_END)
    if begin >= end:
        return ["SYNOPSIS.md: readiness dashboard markers are reversed"]

    block = text[begin:end]
    return [
        f"SYNOPSIS.md: readiness dashboard is detached from canonical source '{source}'"
        for source in READINESS_SOURCES
        if source not in block
    ]


def check_migrated_commands(text: str) -> list[str]:
    """Living instructions must use the maintained module and command surfaces."""
    obsolete = {
        r"negative_control\.py": "cases.trump11.verifier_limits",
        r"verify_trump11\.py": "cases.trump11.verify_exact",
        r"(?<!independent_)lp_cell\.py": "cases.trump11.independent_lp_cell",
        r"test\.sh": "packing-validate",
        r"tools/render_tables\.py": "devtools.render_research_tables",
    }
    return [
        f"SYNOPSIS.md: removed command path matches {pattern!r}; use {replacement}"
        for pattern, replacement in obsolete.items()
        if re.search(pattern, text)
    ]


def check_current_handoff(text: str) -> list[str]:
    """The cold-start path names the latest session, agenda bead, and evidence head."""
    section = re.search(
        r"^### Current Handoff\s*$\n(?P<body>.*?)(?=^##\s|\Z)", text, re.M | re.S
    )
    if section is None:
        return ["SYNOPSIS.md: has no Current Handoff section"]

    session_paths = sorted(
        AGENT_SESSIONS.glob("session-[0-9][0-9][0-9]-*.md"),
        key=lambda path: int(path.name.split("-", 2)[1]),
    )
    if not session_paths:
        return ["campaign/agent-sessions: has no numbered session artifact"]

    latest_path = session_paths[-1]
    latest = front(latest_path)["session"]
    next_action = latest.get("next_action", "")
    next_beads = re.findall(r"\bthink-[a-z0-9]+\b", next_action)
    if not next_beads:
        return [f"{latest_path.name}: terminal next_action names no bead"]

    agenda = front(AGENDA)["agenda"]
    cell = next((item for item in agenda["items"] if item["id"] == "BC-010"), None)
    if cell is None:
        return ["agenda-001: has no BC-010 handoff cell"]
    agenda_bead = cell["bead"]

    problems: list[str] = []
    if agenda_bead not in next_beads:
        problems.append(
            f"{latest_path.name}: next_action and BC-010 disagree on bead {agenda_bead}"
        )

    body = section.group("body")
    session_target = f"campaign/agent-sessions/{latest_path.name}"
    if session_target not in body:
        problems.append(f"SYNOPSIS.md: Current Handoff does not point to latest {latest['id']}")
    if agenda_bead not in body:
        problems.append(f"SYNOPSIS.md: Current Handoff does not name BC-010 bead {agenda_bead}")

    experiment_ids = sorted(
        {
            match
            for artifact in cell.get("artifacts", [])
            for match in re.findall(r"exp-[0-9]{3}", artifact)
        }
    )
    body_lower = body.lower()
    problems.extend(
        f"SYNOPSIS.md: Current Handoff omits BC-010 evidence {experiment_id}"
        for experiment_id in experiment_ids
        if experiment_id not in body_lower
    )

    if "SYNOPSIS.md#current-handoff" not in README.read_text(encoding="utf-8"):
        problems.append("README.md: does not route cold starts to SYNOPSIS current handoff")

    plan = ACTIVE_PLAN.read_text(encoding="utf-8")
    plan_handoff = re.search(
        r"^For the next supervised exact-research goal,.*?(?=^##\s|\Z)",
        plan,
        re.M | re.S,
    )
    if plan_handoff is None or agenda_bead not in plan_handoff.group(0):
        problems.append(f"active launch plan: current handoff does not name {agenda_bead}")
    elif "D-203" in plan_handoff.group(0) or "think-nm35" in plan_handoff.group(0):
        problems.append("active launch plan: current handoff retains a completed blocker")

    development = DEVELOPMENT.read_text(encoding="utf-8")
    if "temporarily asserts D-203" in development:
        problems.append("development.md: still instructs CI to expect fixed D-203")
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


def counted(n: int, singular: str, plural: str) -> str:
    """Write a synopsis count with the noun form that belongs to it."""
    return f"{spell(n)} {singular if n == 1 else plural}"


def check_hypothesis_count(text: str) -> list[str]:
    """The registry introduction states the number of hypothesis artifacts."""
    total = len(list(HYPOTHESES.glob("H-*.md")))
    section = re.search(
        r"^## The Hypothesis Registry\s*$\n(?P<body>.*?)(?=^##\s|\Z)", text, re.M | re.S
    )
    if section is None:
        return ["SYNOPSIS.md: has no Hypothesis Registry section"]
    expected = (
        rf"\b(?:{total}|{re.escape(spell(total))}) "
        r"claims or open questions are codified as artifacts\b"
    )
    if not re.search(expected, section.group("body"), re.I):
        return [f"SYNOPSIS.md: does not state the hypothesis artifact count ({total})"]
    return []


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

    soundness = [defect for defect in defects if defect["class"] == "soundness"]
    flattering = sum(defect.get("direction") == "flattering" for defect in soundness)
    soundness_pattern = (
        rf"\b(?:{flattering}|{re.escape(spell(flattering))})\s+of\s+the\s+"
        rf"(?:{len(soundness)}|{re.escape(spell(len(soundness)))})\s+soundness\s+"
        r"defects\s+pointed\s+in\s+the\s+\*flattering\*\s+direction"
    )
    if not re.search(soundness_pattern, text, re.I):
        problems.append(
            "SYNOPSIS.md: soundness-direction aggregate is not "
            f"{flattering} of {len(soundness)}"
        )

    caught_by_gate = sum(defect["detected_by"] == "gate" for defect in defects)
    gate_pattern = (
        rf"the\s+automated\s+gate\s+has\s+caught\s+"
        rf"(?:{caught_by_gate}|{re.escape(spell(caught_by_gate))})\s+defects\s+in\s+"
        rf"(?:{total}|{re.escape(spell(total))})"
    )
    if not re.search(gate_pattern, text, re.I):
        problems.append(
            f"SYNOPSIS.md: gate-detector aggregate is not {caught_by_gate} of {total}"
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
        + check_hypothesis_count(text)
        + check_totals(text)
        + check_freshness_label(text)
        + check_readiness_dashboard(text)
        + check_migrated_commands(text)
        + check_current_handoff(text)
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
