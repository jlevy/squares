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

Thirteen checks:

  1. every round's verdict in the roll-up matches its artifact
  2. every hypothesis's status and round count match the ledger's derived values
  3. every round-count and effort-total restatement matches the ledger
  4. prose does not promote exp-012 past H-024's unresolved formal prerequisite
  5. the defect count and per-class counts match `defects.yaml`
  6. no round, hypothesis or open defect is silently missing from the synopsis
  7. the stated hypothesis-artifact count matches the registry directory
  8. every relative link and heading anchor resolves
  9. freshness labels name the current round count and do not embed a stale update note
 10. the readiness dashboard remains attached to its canonical status owners
 11. living reproducibility instructions do not name removed command paths
 12. the cold-start handoff agrees with the latest terminal session and its next entry
 13. the reported covering values it names match `CERTIFICATE-REACH.md`'s own table
 14. the `n = 11` fact table's two ends and their gap match the case's own front matter

Check 8 closes a real gap: `packing-ledger check` walks links under `campaign/`
only, so the root document's forty-odd references were unchecked.

Usage: uv run --frozen python -m devtools.check_synopsis
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, localcontext
from pathlib import Path

from devtools.check_rung_figures import round_to
from devtools.render_certificate_reach import reported_covering_values
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
# The repository root. The reader-facing documents live there, not under packing/.
REPO = ROOT.parent
SYNOPSIS = REPO / "SYNOPSIS.md"
README = REPO / "README.md"
HYPOTHESES = ROOT / "campaign/hypotheses"
AGENT_SESSIONS = ROOT / "campaign/agent-sessions"
AGENDAS = ROOT / "campaign/agendas"
ACTIVE_PLAN = REPO / "docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md"
DEFECTS = ROOT / "defects.yaml"
CASE_INTERVAL_ARTIFACT = ROOT / "frontier" / "n-011.md"
#: The three rows of the `n = 11` fact table under "The Problem", by their row labels.
#: `gap` is deliberately the term `conventions.md` fixes: the distance between the best
#: upper and lower bounds, whoever proved them.
CASE_INTERVAL_LABELS = {
    "upper": "Best known packing (upper bound)",
    "lower": "Best certified lower bound",
    "gap": "Bound gap",
}
#: Wide enough for the degree-8 upper bound's thirty-three digits with headroom, for the
#: same reason `check_rung_figures` carries one.
_DECIMAL_PRECISION = 60
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
    return safe_load(path.read_text().split("---\n")[1])


def slugs(text: str) -> set[str]:
    """GitHub-style heading anchors, plus any explicit `id="..."`."""
    out = {
        re.sub(r"[^a-z0-9\- ]", "", re.sub(r"<[^>]+>", "", h).lower()).strip().replace(" ", "-")
        for h in re.findall(r"^#{1,6}\s+(.*)$", text, re.MULTILINE)
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
        re.MULTILINE | re.DOTALL,
    )
    cost_match = re.search(
        r"^### Cost and provenance\s*$\n(?P<body>.*?)(?=^###\s)",
        text,
        re.MULTILINE | re.DOTALL,
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
    cost_counts = Counter(
        re.findall(r"^\| (exp-\d{3}) \|", cost_match.group("body"), re.MULTILINE)
    )

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
        for hid, status in re.findall(r"^\| (H-\d{3}) \| ([^|]+) \|", ledger, re.MULTILINE)
    }
    if not derived:
        return ["campaign/ledger.md: no registry table to check against"]
    derived_rounds = dict(
        re.findall(r"^\| (H-\d{3}) \|(?:[^|]*\|){4} (\d+) \|", ledger, re.MULTILINE)
    )

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
        r"^(\d+) rounds, ([\d.]+) agent-minutes, ([\d.]+) wall-minutes\.$", ledger, re.MULTILINE
    )
    if not line:
        return ["campaign/ledger.md: no effort total to check against"]
    rounds, agent, wall = line.groups()

    problems = check_round_effort_claims(text, rounds, agent, wall)
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
    if not re.search(rf"\b({rounds}|{spelled})\b rounds", text, re.IGNORECASE):
        problems.append(f"SYNOPSIS.md: does not say there are {rounds} rounds")
    if not re.search(
        rf"^### What the {rounds} rounds jointly establish\s*$",
        text,
        re.IGNORECASE | re.MULTILINE,
    ):
        problems.append(
            f"SYNOPSIS.md: synthesis heading does not name the current round count ({rounds})"
        )
    for value, label in ((agent, "agent-minutes"), (wall, "wall-minutes")):
        if f"{value} {label}" not in text:
            problems.append(f"SYNOPSIS.md: effort total '{value} {label}' not stated")
    return problems


def check_round_effort_claims(
    text: str, rounds: str, agent_minutes: str, wall_minutes: str
) -> list[str]:
    """Require every narrative campaign-total claim to match the generated footer."""
    claims = re.findall(
        r"There are (\d+) (?:terminal )?rounds registered in `series-\d+`\.\s+"
        r"They record ([\d.]+) agent-minutes\s+and ([\d.]+) wall-minutes\.",
        text,
    )
    expected = (rounds, agent_minutes, wall_minutes)
    if claims and all(claim == expected for claim in claims):
        return []
    return [
        (
            "SYNOPSIS.md: registered-round aggregate is not "
            f"{rounds} rounds, {agent_minutes} agent-minutes, and "
            f"{wall_minutes} wall-minutes at every occurrence"
        )
    ]


def check_experiment_scope_claims(text: str) -> list[str]:
    """Reject the known promotion of exp-012 past H-024's formal prerequisite."""
    for paragraph in re.split(r"\n\s*\n", text):
        if "Exp-012" not in paragraph or "H-024" not in paragraph:
            continue
        if re.search(r"\b(?:refutes?|rejected|confirms?|confirmed)\s+H-024\b", paragraph):
            return [
                (
                    "SYNOPSIS.md: exp-012 must leave H-024 unresolved; its formal "
                    "witness prerequisite is unmet"
                )
            ]
    return []


def check_freshness_label(text: str) -> list[str]:
    """The dateline may state a date, but not duplicate volatile campaign state."""
    dateline = re.search(r"^\*\*Date:\*\*.*$", text, re.MULTILINE)
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


def select_handoff_cell(items: list[dict], next_action: str) -> dict:
    """Select the one agenda item explicitly named by a terminal session action."""
    matches = [
        item
        for item in items
        if isinstance(item.get("id"), str)
        and re.search(rf"\b{re.escape(item['id'])}\b", next_action)
    ]
    if len(matches) != 1:
        raise ValueError(
            f"terminal next_action must name exactly one agenda cell; found {len(matches)}"
        )
    return matches[0]


def session_handoff_key(session: dict, session_number: int) -> tuple[str, str, int]:
    """Order sessions by their terminal clock, then their start and stable number."""
    started_at = str(session.get("started_at") or "")
    terminal_at = str(session.get("deadline_at") or started_at)
    return terminal_at, started_at, session_number


def select_latest_terminal_session(
    records: Iterable[tuple[Path, dict]],
) -> tuple[Path, dict] | None:
    """Select the terminal session whose terminal clock is latest."""
    terminal = [
        (path, session)
        for path, session in records
        if session.get("status") in {"completed", "stopped"}
    ]
    if not terminal:
        return None
    return max(
        terminal,
        key=lambda record: session_handoff_key(record[1], int(record[0].name.split("-", 2)[1])),
    )


def select_handoff_target(items: list[dict], next_action: str) -> tuple[dict | None, str]:
    """Resolve one agenda cell or one standalone bead from a terminal next action."""
    matching_cells = [
        item
        for item in items
        if isinstance(item.get("id"), str)
        and re.search(rf"\b{re.escape(item['id'])}\b", next_action)
    ]
    if len(matching_cells) > 1:
        count = len(matching_cells)
        raise ValueError(
            f"terminal next_action must name at most one agenda cell; found {count}"
        )

    beads = sorted(set(re.findall(r"\bthink-[a-z0-9]+\b", next_action)))
    if matching_cells:
        cell = matching_cells[0]
        agenda_bead = cell["bead"]
        if agenda_bead not in beads:
            raise ValueError(f"next_action and {cell['id']} disagree on bead {agenda_bead}")
        return cell, agenda_bead
    if len(beads) != 1:
        raise ValueError(
            "terminal next_action without an agenda cell must name exactly one bead; "
            f"found {len(beads)}"
        )
    return None, beads[0]


def load_agenda_items(paths: Iterable[Path]) -> list[dict]:
    """Load agenda cells across every supplied mutable queue."""
    return [item for path in sorted(paths) for item in front(path)["agenda"].get("items", [])]


def select_latest_closeout(paths: Iterable[Path]) -> tuple[Path, dict] | None:
    """Select the newest terminal agenda carrying a W10 closeout."""
    records = []
    for path in paths:
        agenda = front(path)["agenda"]
        if agenda.get("status") in {"completed", "superseded"} and agenda.get("closeout"):
            records.append((path, agenda["closeout"]))
    if not records:
        return None
    return max(records, key=lambda record: int(record[0].stem.split("-", 2)[1]))


def check_current_handoff(text: str) -> list[str]:
    """The cold-start path names the latest terminal session and next entry."""
    section = re.search(
        r"^### Current Handoff\s*$\n(?P<body>.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL
    )
    if section is None:
        return ["SYNOPSIS.md: has no Current Handoff section"]

    # Chronology, not numbering or start order: a coordinator can start before a lane
    # and terminalize after it. The record's terminal clock is the truth the handoff
    # follows. Session number is only the final deterministic tie-breaker.
    records = [
        (path, front(path)["session"])
        for path in AGENT_SESSIONS.glob("session-[0-9][0-9][0-9]-*.md")
    ]
    latest_record = select_latest_terminal_session(records)
    if latest_record is None:
        return ["campaign/agent-sessions: has no terminal numbered session artifact"]

    latest_path, latest = latest_record
    next_action = latest.get("next_action", "")

    agenda_items = load_agenda_items(AGENDAS.glob("agenda-*.md"))
    try:
        cell, expected_bead = select_handoff_target(agenda_items, next_action)
    except ValueError as error:
        return [f"{latest_path.name}: {error}"]

    problems: list[str] = []
    body = section.group("body")
    closeout_record = select_latest_closeout(AGENDAS.glob("agenda-*.md"))
    if closeout_record is not None:
        closeout_path, closeout = closeout_record
        selected = closeout["replanning"]["selected"]
        if selected["bead"] != expected_bead:
            problems.append(
                f"{closeout_path.name}: selected bead {selected['bead']} disagrees with "
                f"latest terminal session bead {expected_bead}"
            )

    selected_markers = re.findall(
        r"^\*\*Selected next entry:\*\* `(?P<bead>think-[a-z0-9]+)`",
        body,
        re.MULTILINE,
    )
    if selected_markers != [expected_bead]:
        problems.append(
            "SYNOPSIS.md: Current Handoff must contain exactly one canonical "
            f"Selected next entry marker for {expected_bead}; found {selected_markers}"
        )
    session_target = f"campaign/agent-sessions/{latest_path.name}"
    if session_target not in body:
        problems.append(f"SYNOPSIS.md: Current Handoff does not point to latest {latest['id']}")
    if expected_bead not in body:
        label = f"{cell['id']} bead" if cell is not None else "standalone bead"
        problems.append(f"SYNOPSIS.md: Current Handoff does not name {label} {expected_bead}")

    experiment_ids: list[str] = []
    evidence_owner: str | None = None
    if cell is not None:
        cell_id = cell["id"]
        evidence_owner = cell_id
        if cell_id not in body:
            problems.append(f"SYNOPSIS.md: Current Handoff does not name {cell_id}")
        experiment_ids = sorted(
            {
                match
                for artifact in cell.get("artifacts", [])
                for match in re.findall(r"exp-[0-9]{3}", artifact)
            }
        )
    body_lower = body.lower()
    if evidence_owner is not None:
        problems.extend(
            f"SYNOPSIS.md: Current Handoff omits {evidence_owner} evidence {experiment_id}"
            for experiment_id in experiment_ids
            if experiment_id not in body_lower
        )

    if "SYNOPSIS.md#current-handoff" not in README.read_text(encoding="utf-8"):
        problems.append("README.md: does not route cold starts to SYNOPSIS current handoff")

    plan = ACTIVE_PLAN.read_text(encoding="utf-8")
    plan_handoff = re.search(
        r"^For the next supervised exact-research goal,.*?(?=^##\s|\Z)",
        plan,
        re.MULTILINE | re.DOTALL,
    )
    if plan_handoff is None:
        problems.append("active launch plan: has no current handoff paragraph")
    else:
        plan_text = plan_handoff.group(0)
        if expected_bead not in plan_text or (cell is not None and cell["id"] not in plan_text):
            expected = (
                f"{cell['id']} and {expected_bead}"
                if cell is not None
                else f"standalone bead {expected_bead}"
            )
            problems.append(f"active launch plan: current handoff does not name {expected}")
        plan_beads = set(re.findall(r"\bthink-[a-z0-9]+\b", plan_text))
        if plan_beads != {expected_bead}:
            problems.append(
                "active launch plan: current handoff bead set is "
                f"{sorted(plan_beads)}, expected {[expected_bead]}"
            )
        defect_records = safe_load(DEFECTS.read_text(encoding="utf-8"))["defects"]
        fixed_defects = {
            defect["id"] for defect in defect_records if defect["status"] == "fixed"
        }
        stale_defects = sorted(set(re.findall(r"\bD-[0-9]{3}\b", plan_text)) & fixed_defects)
        if stale_defects:
            problems.append(
                f"active launch plan: current handoff names fixed defects {stale_defects}"
            )
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


def check_unprotected_fix_claims(text: str, expected: int) -> list[str]:
    """Require every unprotected-fix claim to state the derived count."""
    stated = re.findall(r"([\w-]+) fixes left no", text, re.IGNORECASE)
    accepted = {str(expected), spell(expected).lower()}
    if stated and all(claim.lower() in accepted for claim in stated):
        return []
    return [
        (
            f"SYNOPSIS.md: does not state the unprotected-fix count ({expected}) "
            'in the form "<n> fixes left no regression check behind" at every occurrence'
        )
    ]


#: "at side `4.68`" / "at sides `3.82`, `3.95` and `4.80`" -- the shape the synopsis uses
#: to attach a covering-value report to the side it was reported at. Backticked decimals
#: only, which is what keeps this off the other "at side" phrases in the document: the
#: exact ones are written as fractions or surds (`19/5`, `1 + 5√2/4`) and the unbackticked
#: ones are not quotations of a reported value at all.
_AT_SIDES = re.compile(r"\bat sides?\s+((?:`\d+\.\d+`(?:,\s+|\s+and\s+)?)+)")

#: "`11.9706` at `3.95`" and its neighbours; a backticked decimal inside an `_AT_SIDES`
#: run.
_QUOTED_DECIMAL = re.compile(r"`(\d+\.\d+)`")


def reported_covering_sides() -> tuple[list[str], list[str]]:
    """Every side `CERTIFICATE-REACH.md` reports a covering value at, and the recomputable ones.

    Both lists are read from `frontier/covering-values.yaml` through the renderer, so a
    side with several site sets (`3.82` has two, `4.68` three) is one side here, as the
    prose counts it. "Recomputable" is derived, not listed: a side is recomputable when
    some row's reported value *is* its frozen artifact's own feasible mass, to the places
    the report writes. Exactly one side is, today, and calling that one a measured
    optimum is the error this check exists to refuse -- a feasible mass is an upper bound
    on the covering value at that side, and the search's objective is a different number
    the record cannot replay.
    """
    sides: list[str] = []
    recomputable: list[str] = []
    for row in reported_covering_values():
        if row["side"] not in sides:
            sides.append(row["side"])
        mass = row["mass"]
        if mass is None:
            continue
        reported = row["reported"]
        digits = len(reported.split(".", 1)[1]) if "." in reported else 0
        if round_to(mass, digits) == Decimal(reported) and row["side"] not in recomputable:
            recomputable.append(row["side"])
    return sides, recomputable


def check_covering_value_reports(text: str) -> list[str]:
    """The synopsis's account of the reported covering values matches the generated table.

    The synopsis said "only four restricted optima have ever been measured" and named
    four, while `CERTIFICATE-REACH.md` listed seven reports -- and called them reports,
    because no covering-search run log or solver checkpoint was retained for any of them.
    Three sides were simply missing from the sentence, and the four that were there were
    described as measurements this repository holds. Two claims, both reconcilable against
    the renderer, so both are:

    1. the count, stated in the anchored form the table itself uses, and
    2. every side the synopsis attaches a covering value to is one the table lists, with
       some sentence naming all of them.

    A third, conditional: where the synopsis claims a value is recomputable here, the
    sides it names must be the ones that are. It is conditional rather than required
    because the honest statement of "one of seven" is a judgement the document is free to
    make in its own words; what it is not free to do is name the wrong side.

    Under-matching a rewording is the safe failure here, as it is in `check_case_prose`: a
    covering value written in some shape `_AT_SIDES` does not recognise goes unchecked,
    where a looser pattern would start reporting the document's other uses of "at side".
    """
    sides, recomputable = reported_covering_sides()
    problems = []

    count_pattern = (
        rf"\b(?:{len(sides)}|{re.escape(spell(len(sides)))}) values have been reported\b"
    )
    if not re.search(count_pattern, text, re.IGNORECASE):
        problems.append(
            f"SYNOPSIS.md: does not state the reported-covering-value count ({len(sides)}) "
            'in the form "<n> values have been reported"'
        )

    named = [set(_QUOTED_DECIMAL.findall(run.group(1))) for run in _AT_SIDES.finditer(text)]
    for quoted in named:
        stray = sorted(quoted - set(sides))
        if stray:
            problems.append(
                f"SYNOPSIS.md: names covering-value side(s) {', '.join(stray)}, which "
                "CERTIFICATE-REACH.md does not report a value at"
            )
    if not any(quoted == set(sides) for quoted in named):
        problems.append(
            f"SYNOPSIS.md: no sentence names all {len(sides)} reported covering-value "
            f"sides ({', '.join(sides)})"
        )

    for sentence in re.split(r"(?<=[a-z0-9)`])\.\s+(?=[A-Z])", text):
        if "recomputable" not in sentence:
            continue
        claimed = {
            side
            for run in _AT_SIDES.finditer(sentence)
            for side in _QUOTED_DECIMAL.findall(run.group(1))
        }
        if claimed and claimed != set(recomputable):
            problems.append(
                f"SYNOPSIS.md: claims a covering value is recomputable at "
                f"{', '.join(sorted(claimed))}; the table's recomputable side(s) are "
                f"{', '.join(recomputable)}"
            )
    return problems


def fact_row(text: str, label: str) -> str | None:
    """The value cell of the fact-table row named `label`, or `None` if there is none."""
    match = re.search(rf"^\| {re.escape(label)} \| (.*?) \|", text, re.MULTILINE)
    return None if match is None else match.group(1)


def check_case_interval(
    text: str,
    front: dict,
    labels: dict[str, str] = CASE_INTERVAL_LABELS,
) -> list[str]:
    """The fact table's two ends and their gap match the case artifact's front matter.

    `D-450`, which is `D-442` one day later. T-018 moved the verified lower bound of
    `n = 11` to `381/100`, `frontier/n-011.md`'s front matter moved with it, and the
    fact table under "The Problem" -- the first table a reader meets in this document --
    kept the displaced `2 + 4/sqrt(5)` and the gap computed from it. `check_case_prose`
    holds a case *body* to its own front matter and `check_rung_figures` holds the
    results register to its certificates; the two reader-facing documents were held to
    nothing, so the class moved to them.

    Three things are required, and each is the shape of the drift that happened:

    * the upper row's digits are the front matter's own, allowing the trailing ellipsis
      the row writes but not a different value;
    * the lower row states both the exact form the record carries and its decimal, so a
      row cannot go stale in one and stay current in the other;
    * the gap is the difference of the two, at whatever precision the row is written to.

    Pure in its inputs -- `text` and the already-loaded front matter -- so that the
    negative control can drive it directly rather than doctoring the repository.
    """

    found = {key: fact_row(text, label) for key, label in labels.items()}
    if missing := [labels[key] for key, row in found.items() if row is None]:
        return [f"SYNOPSIS.md: fact table has no '{label}' row" for label in sorted(missing)]

    rows = {key: row for key, row in found.items() if row is not None}
    figures = {key: re.findall(r"`([^`]*)`", row) for key, row in rows.items()}
    if empty := [labels[key] for key, found in figures.items() if not found]:
        return [f"SYNOPSIS.md: '{label}' row states no figure" for label in sorted(empty)]

    upper = str(front["verified_upper_bound"]["value"])
    lower = str(front["verified_lower_bound"]["value"])
    exact = str(front["verified_lower_bound"]["exact_form"])

    problems = []
    written_upper = figures["upper"][0].rstrip("\u2026. ")
    if not written_upper or not upper.startswith(written_upper):
        problems.append(
            f"SYNOPSIS.md: '{labels['upper']}' states '{figures['upper'][0]}', "
            f"not the case's verified {upper}"
        )

    lower_cell = figures["lower"][0]
    absent = [
        wanted
        for wanted in (exact, lower)
        if not re.search(rf"(?<![\w./]){re.escape(wanted)}(?![\w./])", lower_cell)
    ]
    if absent:
        problems.append(
            f"SYNOPSIS.md: '{labels['lower']}' states '{lower_cell}', which does not "
            f"carry the case's verified {' and '.join(absent)}"
        )

    stated_gap = figures["gap"][0]
    try:
        stated = Decimal(stated_gap)
    except InvalidOperation:
        stated = Decimal("nan")
    # A non-integer exponent is what a NaN or an infinity carries -- the cell `Decimal`
    # refused above, and the "nan" or "Infinity" it would have accepted. No gap is one.
    exponent = stated.as_tuple().exponent
    if not isinstance(exponent, int):
        problems.append(f"SYNOPSIS.md: '{labels['gap']}' states no decimal ({stated_gap})")
        return problems
    places = -exponent
    with localcontext() as context:
        context.prec = _DECIMAL_PRECISION
        expected = (Decimal(upper) - Decimal(lower)).quantize(
            Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP
        )
    if stated != expected:
        problems.append(
            f"SYNOPSIS.md: '{labels['gap']}' states {stated}, "
            f"not the {expected} the two rows leave between them"
        )
    return problems


def check_defects(text: str) -> list[str]:
    """The defect count and per-class counts match the dataset."""
    data = safe_load((ROOT / "defects.yaml").read_text())
    defects = data["defects"]

    problems = []
    total = len(defects)
    # Anchored to the sentence that states it, not searched for loose in the document.
    # A bare `\b(399)\b` over the whole text passes on any other occurrence of the number,
    # and the synopsis states it twice -- "The log contains N defects" and "the automated
    # gate has caught M defects in N". So the first could read 400 against a dataset of 399
    # and this check still found the 399 in the second and said nothing. That is what
    # happened on 2026-08-30, to a one-line sed; see `D-400`.
    log_pattern = rf"the\s+log\s+contains\s+(?:{total}|{re.escape(spell(total))})\s+defects"
    if not re.search(log_pattern, text, re.IGNORECASE):
        problems.append(
            f"SYNOPSIS.md: does not state the defect count ({total}) in the form "
            '"The log contains <n> defects"'
        )

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
    if not re.search(soundness_pattern, text, re.IGNORECASE):
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
    if not re.search(gate_pattern, text, re.IGNORECASE):
        problems.append(
            f"SYNOPSIS.md: gate-detector aggregate is not {caught_by_gate} of {total}"
        )

    # The unprotected-fix count. This is the log's most actionable claim -- the list
    # that predicts what comes back -- and it is the one that drifted: the synopsis said
    # "Six" while the generated view said seven, which is D-028 recurring in the document
    # D-028 was about. The same rule as the flattering-direction claim applies: derive it,
    # do not assert it. Every occurrence must state the derived count, not just one:
    # D-326 hid a stale duplicate behind a correct first statement for a full merge.
    unprotected = sum(
        1 for d in defects if d["regression"] == "none" and d["status"] != "outstanding"
    )
    problems.extend(check_unprotected_fix_claims(text, unprotected))

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
        + check_experiment_scope_claims(text)
        + check_freshness_label(text)
        + check_readiness_dashboard(text)
        + check_migrated_commands(text)
        + check_current_handoff(text)
        + check_covering_value_reports(text)
        + check_defects(text)
        + check_case_interval(text, front(CASE_INTERVAL_ARTIFACT)["packing"])
    )
    if problems:
        print("SYNOPSIS.md has drifted from the artifacts:", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1
    print("  SYNOPSIS.md agrees with the artifacts, the ledger and the defect log")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
