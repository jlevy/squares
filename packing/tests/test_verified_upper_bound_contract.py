#!/usr/bin/env python3
"""`verified_upper_bound` is a ceiling, and every reader of it has to be told so.

The name invites reading the field as "the verified exact value of s(n)". It is not.
It is the strongest upper bound this repository can certify from its own evidence, and
for a third of n <= 100 it is WEAKER than the best known construction two fields above
it -- by as much as 0.46, with `exact_form` set to the trivial grid integer. An agent
read "all 100 verified upper bounds carry an exact_form" as "all 100 side lengths are
exact algebraic numbers" and told a user so. The claim is false and the naming is why.

Renaming the field would touch the record generators, renderers and the validation CLI,
which this change does not own. So the relationship is documented instead, in the three
places a reader can actually meet the field, and these tests hold all three in place:

1. the schema, for anyone reading the contract;
2. the body of every record where the ceiling trails the report, for anyone reading one
   case;
3. a declared list of consumers, so no new code or document can name the field without
   someone deciding what it means there.
"""

from __future__ import annotations

import math
import re
from decimal import Decimal, localcontext
from pathlib import Path

import yaml

from sqpack.assurance import bounds_agree_at_declared_precision

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# The consumers of this field now span the repository: it is named in SYNOPSIS.md and
# in active plans, which sit above packing/.
REPO = PROJECT_ROOT.parent
FRONTIER = PROJECT_ROOT / "frontier"
SCHEMA = FRONTIER / "square-packing-case.schema.yaml"
CEILING_HEADING = "## The verified upper bound is a ceiling"

# Every file in the project that names `verified_upper_bound`, and what it does with it.
# A new entry is a decision, not a formality: the field is a ceiling, so a consumer that
# wants the best known side length wants `reported_upper_bound` instead, and a consumer
# that wants a proved side length has to check `status` first.
DECLARED_CONSUMERS = {
    "packing/devtools/check_basic_bounds.py": (
        "checks the ceiling really is the certifiable grid bound"
    ),
    "packing/devtools/check_golden_basins.py": (
        "reads the ceiling as an upper limit on a basin side"
    ),
    "packing/devtools/controls.yaml": (
        "corrupts the field on purpose, to prove the checkers fire"
    ),
    "packing/devtools/migrate_frontier_v2.py": "builds the field from the v1 records",
    "packing/devtools/render_research_tables.py": (
        "renders it beside the report, never instead of it"
    ),
    "docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md": (
        "the plan that introduced the reported/verified split"
    ),
    "packing/frontier/README.md": "documents the field for a reader of the corpus",
    "packing/frontier/evidence.yaml": (
        "names the fields as the certificate the grid bound lives in"
    ),
    "packing/frontier/square-packing-case.schema.yaml": "defines it",
    "packing/src/sqpack/assurance.py": (
        "compares report against ceiling and demands a blocker for any gap"
    ),
    "packing/tests/test_frontier_assurance_contract.py": "exercises those comparisons",
    "packing/tests/test_verified_upper_bound_contract.py": "this file",
    "SYNOPSIS.md": "names the field when describing the reported/verified split",
    "packing/campaign/agendas/agenda-005-symbolic-promotion-and-identity.md": (
        "plans promotion work that reads the ceiling, never as the value"
    ),
    "docs/project/specs/active/plan-2026-08-28-interval-certification.md": (
        "specs certification that would tighten the ceiling toward the report"
    ),
    "packing/campaign/research-loop-logbook/run-002-2026-08-29-overnight-promotion-blocks.md": (
        "reports how far below the ceiling the run's certificate sits, and that the "
        "ceiling did not move"
    ),
    "packing/campaign/agent-sessions/session-039-block5-witness-plumbing.md": (
        "records the certificate as evidence and says the ceiling was not moved to it"
    ),
    "packing/campaign/agent-sessions/session-040-block6-chirality.md": (
        "names the ceiling only as a stop condition: the block builds the pose model and "
        "does not touch it"
    ),
    "packing/campaign/agent-sessions/session-041-block7-collinearity.md": (
        "names the ceiling only as a stop condition: the block repairs an assembly "
        "equation and does not touch it"
    ),
    "packing/campaign/ledger.md": (
        "generated: it renders the agenda notes below and inherits whatever they say, so "
        "it is an output of a consumer rather than one itself"
    ),
    "packing/campaign/agent-sessions/session-036-block1-interval-operator.md": (
        "records that block 1 did not touch the ceiling"
    ),
    "packing/campaign/agent-sessions/session-037-block2-interval-calibration.md": (
        "reports how far below the ceiling its certificate sits, and that it promotes nothing"
    ),
    "packing/cases/kingbird29/certify_interval.py": (
        "compares its bound against the ceiling and refuses to promote it"
    ),
    "packing/campaign/agendas/agenda-006-overnight-research-blocks.md": (
        "schedules that certification work, and says the ceiling does not move in the run"
    ),
    "packing/devtools/assess_frontier_rigidity.py": (
        "reads the ceiling only together with the floor, and only to confirm they pin the "
        "side at exactly k before making the perfect-square tiling argument; a one-sided "
        "read would not establish a tiling and is never made"
    ),
    "packing/tests/test_frontier_rigidity_assessment.py": (
        "exercises that two-sided pin, including the cases where it must refuse"
    ),
}

# Prose, code and hand-written records. Generated artifacts are excluded because they
# are outputs of the consumers below rather than consumers themselves: the atlas alone
# is 44 MB of them, and nothing hand-written in this project comes close to the cap.
SEARCHED_SUFFIXES = (".py", ".md", ".yaml", ".yml", ".rs")
SKIPPED_PARTS = {
    ".venv",
    "__pycache__",
    "resources",
    "target",
    ".pytest_cache",
    "results",
    "node_modules",
}
GENERATED_BYTES = 512 * 1024


def cases() -> dict[int, dict]:
    loaded: dict[int, dict] = {}
    for path in sorted(FRONTIER.glob("n-*.md")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        loaded[int(payload["n"])] = payload
    return loaded


def trailing_ceilings() -> dict[int, tuple[Decimal, Decimal]]:
    """Cases whose certified ceiling does not agree with the reported best known."""
    trailing: dict[int, tuple[Decimal, Decimal]] = {}
    for n, case in cases().items():
        reported = case["reported_upper_bound"]
        verified = case["verified_upper_bound"]
        if not bounds_agree_at_declared_precision(reported, verified):
            trailing[n] = (Decimal(reported["value"]), Decimal(verified["value"]))
    return trailing


def test_a_third_of_the_corpus_certifies_a_weaker_bound_than_it_reports() -> None:
    trailing = trailing_ceilings()
    # Not a target to be held at 33; a measurement, and a loud one. Every one of these
    # is a case where reading `verified_upper_bound` as s(n) overstates the side length.
    assert len(trailing) == 33
    for n, (reported, verified) in trailing.items():
        assert verified > reported, n
    worst = max(verified - reported for reported, verified in trailing.values())
    assert worst > Decimal("0.46")

    # And in those cases `exact_form` is exact about the ceiling and says nothing about
    # s(n): for all but n = 29 it is literally the integer grid bound.
    grids = {
        n
        for n in trailing
        if cases()[n]["verified_upper_bound"]["exact_form"] == str(math.isqrt(n - 1) + 1)
    }
    assert sorted(set(trailing) - grids) == [29]

    # Every case carrying an exact_form on the ceiling, split by whether s(n) is known.
    exact_forms = sum(
        1 for case in cases().values() if case["verified_upper_bound"]["exact_form"]
    )
    proved = sum(1 for case in cases().values() if case["status"] == "proved")
    assert exact_forms == 100
    assert proved < exact_forms


def test_every_trailing_case_says_so_in_the_record_a_reader_opens() -> None:
    trailing = trailing_ceilings()
    for n, (reported, verified) in sorted(trailing.items()):
        body = _body(n)
        assert CEILING_HEADING in body, f"n={n} certifies a weaker ceiling and does not say so"
        section = body.split(CEILING_HEADING, 1)[1].split("\n## ", 1)[0]
        flat = " ".join(section.split())
        assert str(verified) in flat, n
        assert str(reported) in flat, n
        # Pin the precision. The gap is rendered into the record at Python's
        # default 28 digits, but decimal's context is process-global and
        # sqpack.field raises it to digits + 20 while refining an enclosure, so
        # a test running after one of those would otherwise compute a longer
        # rendering of the same number and call the record stale. The record is
        # not stale; the ambient precision moved. See the bead on that global
        # mutation.
        with localcontext() as context:
            context.prec = 28
            gap = str(verified - reported)
        assert gap in flat, n
        assert f"not the value of `s({n})`" in flat, n
        assert "`reported_upper_bound`" in flat, n

    # The section is a statement about this case, so it must not appear where the
    # ceiling does reach the report.
    for n in set(cases()) - set(trailing):
        assert CEILING_HEADING not in _body(n), n


def test_the_schema_states_what_the_field_is_and_is_not() -> None:
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    assert schema["properties"]["verified_upper_bound"] == {"$ref": "#/$defs/verifiedUpper"}
    definition = schema["$defs"]["verifiedUpper"]
    description = " ".join(definition["description"].split())
    assert "NOT the value of s(n)" in description
    assert "NOT a copy of reported_upper_bound" in description
    assert "status is proved" in description

    exact_form = " ".join(definition["properties"]["exact_form"]["description"].split())
    assert "never of s(n)" in exact_form
    assert "only when status is proved" in exact_form


def test_no_undeclared_consumer_reads_the_field() -> None:
    found: set[str] = set()
    for path in sorted(REPO.rglob("*")):
        if path.is_dir() or path.suffix not in SEARCHED_SUFFIXES:
            continue
        relative = path.relative_to(REPO)
        # Dot-directories hold vendored agent skills and tooling state, not our prose.
        if (
            SKIPPED_PARTS & set(relative.parts)
            or any(part.startswith(".") for part in relative.parts)
            or re.fullmatch(r"n-\d{3}\.md", path.name)
        ):
            continue
        if path.stat().st_size > GENERATED_BYTES:
            continue
        if "verified_upper_bound" in path.read_text(encoding="utf-8", errors="ignore"):
            found.add(relative.as_posix())
    undeclared = sorted(found - set(DECLARED_CONSUMERS))
    assert undeclared == [], (
        "these name verified_upper_bound without saying what they take it to mean; "
        "it is a ceiling, not s(n) -- add them to DECLARED_CONSUMERS with a reason"
    )
    stale = sorted(set(DECLARED_CONSUMERS) - found)
    assert stale == [], "declared consumers that no longer read the field"


def _body(n: int) -> str:
    return (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8").split("---\n", 2)[2]
