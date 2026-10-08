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
import os
import re
import stat
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import pytest
import yaml

from devtools import apply_exact_ceilings
from devtools import squish_followup_packets as squish_update
from devtools import squish_second_update_packets as squish_second
from devtools import squish_upper_bound_packets as squish
from devtools.check_case_prose import Reading
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.known_best import KNOWN_BEST_CORPUS

#: Cases whose verified ceiling trails the reported side, per corpus (think-93on).
#: Lowered on 2026-09-29 by 46: Francisco Couzo's 49 packings (T-056) replaced 49 trailing
#: reports with certified ones, three of which, n = 206, 259 and 305, still trail by 2 or
#: 3 units of the printed fifteenth decimal; de Winter's n = 211 (T-057) moved a report
#: and its ceiling together off the grid. Raised on 2026-10-05 by one: Couzo's packing of 3
#: October at n = 306 (T-092) certifies only 2 units of the fifteenth decimal above its side.
#: Unchanged by n = 69, 83 and 87 leaving the grid for exact certificates of the catalogue's
#: packings (T-088, T-089), which still trail their printed sides by 2 to 89 units of the
#: fourteenth decimal. Lowered on 2026-10-05 by five: Evan Daniel's exact optima of 48
#: known-best packings (T-098) put both lanes on one exact side at n = 206, 259, 305 and
#: 306, and certified de Winter's n = 126, whose ceiling had been the grid. Lowered on
#: 2026-10-06 by 22, to the 55 counts whose catalogue side is a closed form and n = 29:
#: Evan Daniel's exact certificates of the catalogue's packings (T-101) took 74 ceilings
#: off the grid and lowered n = 69, 83 and 87's, each to the printed side plus one unit of
#: its fourteenth decimal, which agrees with a decimal report and trails a closed form.
TRAILING_BY_CORPUS: dict[str, int] = {"n=1..100": 4, "n=1..200": 28, "n=1..324": 56}

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
# Trees whose files may name the field without reading it, declared once rather than one
# file at a time. A tree qualifies only when its files are generated, when the field can
# appear in them as incidental identity rather than as a value anything consumes, and when
# a new file arrives on every run so a per-file list would be pure churn.
DECLARED_CONSUMER_TREES = {
    "packing/campaign/agent-sessions/": (
        "session records narrate work, and work touches this field, so every session that "
        "did any names it -- seven were declared one by one before this became a tree. "
        "They make no claim about any bound: a record saying a session moved a "
        "verified_upper_bound is reporting what happened, and the claim itself lives in "
        "the case record that moved. This is D-394's argument at a third level, and the "
        "list it was growing had started to grow for reasons unrelated to its purpose"
    ),
    "packing/campaign/resource-usage/": (
        "derived per-session measurement records. They never read the field: it reaches "
        "them as the name of a tool that ran, such as the test file that guards this very "
        "contract, and a rollup makes no claim about any bound"
    ),
}

DECLARED_CONSUMERS = {
    "packing/devtools/squish_second_update_confirmation.py": (
        "publishes the admitted complete exact replay as a feasible upper ceiling, "
        "retaining earlier ceilings and refusing optimality claims"
    ),
    "packing/tests/test_squish_second_update_confirmation.py": (
        "checks complete replay custody and preservation of earlier upper ceilings; "
        "the confirmed feasible construction does not establish s(n)"
    ),
    "packing/devtools/squish_second_update_packets.py": (
        "preserves the previous independently certified ceiling while adopting a stronger "
        "second-update source report; the historical ceiling is never promoted to the "
        "new geometry or read as s(n)"
    ),
    "packing/tests/test_squish_upper_bound_packets.py": (
        "checks that source-packet admission preserves the independently certified "
        "ceiling and cannot grant verification or optimality to a reported packing"
    ),
    "packing/devtools/source_supersession.py": (
        "rebuilds an explicitly selected source report from exact facts while retaining "
        "the historical independently certified ceiling until the reviewed SQUISH lane "
        "is present; the two fields remain upper bounds, never exact optima"
    ),
    "packing/devtools/render_n11_lower_bounds_explainer.py": (
        "admits the solved n11 caption only when the case is proved, its exact lower "
        "identity matches the ceiling and T-060 confirmation is present; the ceiling "
        "alone and matching decimal displays do not establish s(11)"
    ),
    "packing/tests/test_n11_lower_bounds_explainer.py": (
        "tests the proved-case exact lower/ceiling identity and refuses missing T-060 "
        "confirmation or a changed root; rounded equality alone is not optimality"
    ),
    "packing/tests/test_certificate_reach.py": (
        "checks the solved n11 record has proved status and matching exact lower/ceiling "
        "identities; the diagnostic float cap is not used to prove optimality"
    ),
    "packing/devtools/apply_upper_bound_packets.py": (
        "writes the ceiling a parallel packing's exact certificate proves, the printed side "
        "or the certified side rounded up at its precision, and the ceiling section, conflict "
        "and blocker wherever that trails the report; it reads the field as a ceiling and "
        "never as s(n)"
    ),
    "packing/devtools/apply_exact_optima.py": (
        "writes the ceiling Evan Daniel's exact certificates prove at 48 counts (T-098), "
        "the certificate's side itself, and drops the blocker and conflict that recorded the "
        "earlier ceiling trailing its report; it reads the field as a ceiling and never as s(n)"
    ),
    "packing/devtools/apply_exact_ceilings.py": (
        "writes the ceiling Evan Daniel's exact certificates prove at 77 counts (T-101), the "
        "certified side rounded up at the printed precision, drops the upper-gap blocker and "
        "ceiling section where that agrees with the report, and keeps a rewritten blocker "
        "and section where the report is a closed form it does not reach; it reads the field "
        "as a ceiling and never as s(n)"
    ),
    "packing/devtools/catalogue_upper_bounds.py": (
        "writes the ceiling the exact certificates of the catalogue's n = 69, 83 and 87 "
        "packings prove, the certified side rounded up, and the blocker saying it trails the "
        "printed side; it reads the field as a ceiling and never as s(n)"
    ),
    "packing/devtools/render_stack_results.py": (
        "counts the case records whose verified_upper_bound value differs between two "
        "revisions, for a pull request's description; it compares the stored strings and "
        "reads no value as s(n) or as anything but the ceiling the record holds"
    ),
    "packing/tests/test_render_stack_results.py": (
        "builds two case records whose ceiling is the same and checks the rendered count of "
        "changed ceilings is zero; it asserts nothing about s(n)"
    ),
    "packing/tests/test_catalogue_upper_bounds.py": (
        "checks that n = 69, 83 and 87 carry the ceiling their exact certificates' receipts "
        "derive and that it still trails the printed side; it asserts nothing about s(n)"
    ),
    "packing/tests/test_upper_bound_packets.py": (
        "checks that each certified case's ceiling cites its replay and agrees with the "
        "report exactly where the receipt says it does; it asserts nothing about s(n)"
    ),
    "packing/devtools/check_results.py": (
        "reads only the evidence ids a case's bound fields cite, to derive whether a "
        "registered result still holds a case bound; it takes no value from the field and "
        "never reads the ceiling as s(n)"
    ),
    "packing/devtools/render_case_verifiers.py": (
        "reads only the evidence ids the field cites, to name the programs behind a case "
        "record's verified upper bound in its Verification Code table; it takes no value "
        "from the field and never reads the ceiling as s(n)"
    ),
    "packing/devtools/render_case_pages.py": (
        "shows the field in each case record's own panel, labelled the verified upper bound, "
        "and as the upper end of the verified interval the record's heading states; it "
        "reads the field as a ceiling on s(n) and never as s(n)"
    ),
    "packing/devtools/result_overview.py": (
        "shows the field in a result overview's grid of its case record's four bounds, in "
        "the Upper cell of the Verified row, linked to its line in the case file, beside "
        "the gap the frontier page computes; the solved note is the record's own status, "
        "and it reads the field as a ceiling on s(n) and never as s(n)"
    ),
    "packing/devtools/render_recent_results.py": (
        "reads only the evidence ids a case's bound fields cite, to derive which register "
        "entries hold a case bound for the standing column; it takes no value from the "
        "field and never reads the ceiling as s(n)"
    ),
    "docs/project/reviews/review-2026-09-29-issue-227-upper-bound-packings.md": (
        "a dated review explaining why n = 206, 259 and 305 carry a verified ceiling above "
        "the printed side; it reads the field as the certified ceiling and says it is "
        "neither s(n) nor a different packing"
    ),
    "docs/project/reviews/review-2026-10-05-couzo-6042c56.md": (
        "the T-092 review, explaining why n = 306 carries a verified ceiling two units of "
        "the fifteenth decimal above the printed side, as the 29 September review did for "
        "n = 206, 259 and 305; it reads the field as the certified ceiling, not as s(n)"
    ),
    "docs/project/reviews/review-2026-10-05-kingbird-intake-n69-n83-n87.md": (
        "a dated review saying what n = 69, 83 and 87's verified upper lanes may state: the "
        "exact certificates' sides rounded up, above the printed sides, and never s(n) or "
        "the catalogue's roots"
    ),
    "docs/project/reviews/review-2026-10-06-evand-exact-optima.md": (
        "the T-098 review, finding that n = 126 conjectured a side above the ceiling its "
        "exact certificate verifies; it reads the field as a ceiling on s(n), not as s(n)"
    ),
    "docs/project/reviews/review-2026-10-06-evand-exact-optima-fix-check.md": (
        "the check of that review's fixes, quoting its proposed bracket of a conjecture "
        "between the verified floor and ceiling; a ceiling, not s(n)"
    ),
    "packing/tests/test_evand_exact_certificates.py": (
        "holds a synthetic case's ceiling against conjectures inside and past half a unit "
        "of their last place, and each T-101 ceiling to the certified side rounded up and "
        "to the report it agrees with or trails; it reads the field as a ceiling, not as s(n)"
    ),
    "packing/tests/test_evand_square_packing.py": (
        "pins n = 32's ceiling to the trivial grid's 6, which with the verified lower bound "
        "6 is what makes that case proved; it reads the field as a ceiling, not as s(n)"
    ),
    "packing/cases/w3_lower_bound_directions/frontier_transfer_audit.py": (
        "reads the verified ceiling to measure a bounded transfer-diagnostic gap; it "
        "does not identify that ceiling with s(n) or claim optimality"
    ),
    "packing/atlas/known-best/video/spikes/v1-slideshow/NOTES.md": (
        "a retained prototype's notes, listing the record fields the slideshow panel "
        "deliberately does not draw; it names this field to say the figure omits it "
        "because it is a ceiling rather than s(n), which is the contract's own reading"
    ),
    "packing/devtools/build_bound_citations.py": (
        "compares the ceiling with reported_upper_bound through "
        "bounds_agree_at_declared_precision to mark a shown upper bound verified or reported, "
        "and omits a line only where the ceiling's own evidence is common-knowledge; it never "
        "reads the field as s(n)"
    ),
    "packing/tests/test_bound_citations.py": (
        "builds synthetic cases carrying the field and restates the same agreement rule; it "
        "asserts nothing about s(n)"
    ),
    "docs/project/specs/active/plan-2026-09-22-upper-bound-certification-blocks.md": (
        "plans the blocks that certify reported upper bounds; it names the field to explain "
        "the certification rule and the queue, reading it as a ceiling, never as s(n)"
    ),
    "packing/devtools/audit_ds7_lower_bounds.py": (
        "preserves the certified ceiling unchanged while auditing source-reported lower "
        "bounds; it neither promotes that ceiling to s(n) nor derives a new upper bound"
    ),
    "packing/tests/test_audit_ds7_lower_bounds.py": (
        "checks that reported-lower-bound updates leave the certified ceiling unchanged; "
        "equality of stored fields makes no claim that the ceiling is optimal"
    ),
    (
        "packing/campaign/series/series-000-smoke-and-calibration/experiments/"
        "exp-126-h099-complete-graph-candidate.md"
    ): (
        "requires an independent graph-proof status for a conditional depth ceiling, "
        "not the frontier packing-side field or an exact value of s(n)"
    ),
    "packing/devtools/check_geometric_graph_certificate.py": (
        "consumes a graph-proof status only after reconstructing the conservative "
        "interior-overlap graph; the resulting depth ceiling is not a packing side"
    ),
    "packing/tests/test_check_geometric_graph_certificate.py": (
        "uses synthetic graph-proof statuses to test exact family-depth replay, "
        "not the frontier upper-bound field or an exact value of s(n)"
    ),
    "packing/devtools/check_weighted_clique_certificate.py": (
        "uses the same spelling as a graph-proof status, not the frontier field: it "
        "certifies an upper bound on every weighted graph clique, never a packing side"
    ),
    "packing/tests/test_check_weighted_clique_certificate.py": (
        "tests the graph-only upper-bound status on unrelated synthetic graphs; it "
        "neither reads the frontier ceiling nor claims an exact packing side"
    ),
    "packing/devtools/check_basic_bounds.py": (
        "checks the ceiling really is the certifiable grid bound"
    ),
    "packing/tests/test_certificate_citations.py": (
        "names the field in a fixture proving evidence refs are found in every block that "
        "carries one; it asserts nothing about the bound's value"
    ),
    "packing/devtools/render_evidence_inventory.py": (
        "names the field only as one of the case blocks that can carry evidence ids, so "
        "that citations can be counted; it reads no bound and makes no claim about what "
        "any of them is worth"
    ),
    "packing/devtools/price_gobel_family.py": (
        "says in prose that the four family sizes now certify the exact side rather than "
        "the grid ceiling, to keep its own coverage record from reading as a gap; it "
        "computes nothing from the field"
    ),
    "packing/devtools/check_golden_basins.py": (
        "reads the ceiling as an upper limit on a basin side"
    ),
    "packing/devtools/check_synopsis.py": (
        "reads the n = 11 case's ceiling from its front matter only to hold the synopsis's "
        "fact table to it: the table's upper row must be the record's own digits and the gap "
        "row their difference (D-452). It takes the field to mean exactly what the front "
        "matter means and asserts nothing about s(n)"
    ),
    "packing/tests/test_synopsis_handoff.py": (
        "names the field in a fixture standing in for the n = 11 front matter, so that the "
        "fact-table check can be driven on doctored tables; it asserts nothing about the "
        "bound's value"
    ),
    "packing/devtools/check_case_prose.py": (
        "reads the field as the ceiling the case's own front matter declares, only to "
        "hold that case's prose to it: a body that quotes an upper bound must quote the "
        "one its record carries (D-442). It takes the field to mean exactly what the "
        "front matter means and asserts nothing about s(n)"
    ),
    "packing/tests/test_case_prose.py": (
        "names the field in fixtures that give check_case_prose a front matter and a "
        "body to compare; the values are synthetic and prove the detector fires, not "
        "anything about a bound"
    ),
    "packing/campaign/explorations/X-009-where-a-new-packing-is-reachable.md": (
        "sequences the research blocks by how far each could move the ceiling; it treats "
        "the field as the certified ceiling throughout and states that every move of it "
        "is a reviewed change, never s(n)"
    ),
    "packing/devtools/controls.yaml": (
        "corrupts the field on purpose, to prove the checkers fire"
    ),
    "packing/devtools/migrate_frontier_v2.py": "builds the field from the v1 records",
    "packing/devtools/generate_frontier_case.py": (
        "builds the field for a drafted case as the trivial grid ceiling ceil(sqrt(n)) "
        "under E-basic-grid-upper, and writes the case's own ceiling disclaimer and its "
        "mathematics blocker whenever that ceiling trails the reported best known side. "
        "It never copies reported_upper_bound into it and never treats either as s(n)"
    ),
    "packing/tests/test_generate_frontier_case.py": (
        "compares the generated field against the one a hand-written record carries, and "
        "asserts it is the grid ceiling; it makes no claim about any bound's worth"
    ),
    "docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md": (
        "the plan that extends the register to n = 324; it states the bound rule for the "
        "field in the new range -- the grid ceiling under E-basic-grid-upper -- and never "
        "as a side length"
    ),
    "packing/devtools/render_research_tables.py": (
        "renders it beside the report, never instead of it"
    ),
    "docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md": (
        "the plan that introduced the reported/verified split"
    ),
    "packing/defects.yaml": (
        "D-367 cites the consumer contract as the nearest existing guard against the "
        "claim-boundary conflation it records, one level up from it"
    ),
    "packing/frontier/README.md": "documents the field for a reader of the corpus",
    "packing/frontier/evidence.yaml": (
        "names the fields as the certificate the grid bound lives in"
    ),
    "packing/frontier/square-packing-case.schema.yaml": "defines it",
    "packing/src/sqpack/assurance.py": (
        "compares report against ceiling and demands a blocker for any gap, and refuses a "
        "decimal conjectured optimum above the ceiling, which a conjecture of s(n) may not "
        "exceed"
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
    "packing/campaign/ledger.md": (
        "generated: it renders the agenda notes below and inherits whatever they say, so "
        "it is an output of a consumer rather than one itself"
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
    "packing/devtools/render_frontier_page.py": (
        "shows each case's verified ceiling in its own column beside the verified lower "
        "bound, links its evidence, and takes their difference as the open gap; a zero gap "
        "is what the record already calls proved, and the page reads it no further"
    ),
    "packing/tests/test_frontier_page.py": (
        "builds the frontier page's cells from the real records and asserts their text; "
        "it reads the ceiling only as the page does"
    ),
    "packing/tests/test_overview.py": (
        "holds the homepage introduction's upper-bound example for n = 29 at or above the "
        "verified ceiling as well as the reported bound, so the example is itself a proved "
        "ceiling; it reads the field as a ceiling, never as s(n)"
    ),
    "docs/project/specs/active/plan-2026-09-29-github-pages-overview.md": (
        "the plan for the overview and frontier pages, naming the field as the verified "
        "ceiling those pages show beside the lower bound"
    ),
}

# Prose, code and hand-written records. Generated artifacts are excluded because they
# are outputs of the consumers below rather than consumers themselves: the atlas alone
# is 44 MB of them, and nothing hand-written in this project comes close to the cap.
SEARCHED_SUFFIXES = (".py", ".md", ".yaml", ".yml", ".rs")
SKIPPED_PARTS = {
    # A worktree's gitignored scratch, never part of the record: a consumer found there does
    # not exist in any checkout but the one it was written in.
    "attic",
    ".venv",
    "__pycache__",
    "resources",
    "target",
    ".pytest_cache",
    "results",
    "node_modules",
}
OWN_NAME = "test_verified_upper_bound_contract"
"""This file's own stem, which is not a mention of the field and must not read as one.

Citing the guard is not using the thing it guards. `defects.md` renders each defect's
`recorded_in` as a link and `D-392` is recorded here; a session record lists this file as
evidence. Both then "name" `verified_upper_bound` without any claim about a ceiling
anywhere in them, and declaring each one would grow the consumer list by a line every time
someone referred to this test -- churn with no signal, which is the same argument
`DECLARED_CONSUMER_TREES` already makes for generated trees.

Stripping the stem keeps the sweep pointed at what it is for. A document that discusses the
field still matches, because it cannot discuss it without writing the name outside a
filename.
"""

GENERATED_BYTES = 512 * 1024


def cases() -> dict[int, dict]:
    loaded: dict[int, dict] = {}
    for path in sorted(FRONTIER.glob("n-*.md")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        loaded[int(payload["n"])] = payload
    return loaded


def trailing_ceilings(loaded_cases: dict[int, dict]) -> dict[int, tuple[Decimal, Decimal]]:
    """Cases whose certified ceiling does not agree with the reported best known."""
    trailing: dict[int, tuple[Decimal, Decimal]] = {}
    for n, case in loaded_cases.items():
        reported = case["reported_upper_bound"]
        verified = case["verified_upper_bound"]
        if not bounds_agree_at_declared_precision(reported, verified):
            trailing[n] = (Decimal(reported["value"]), Decimal(verified["value"]))
    return trailing


def test_a_third_of_the_corpus_certifies_a_weaker_bound_than_it_reports() -> None:
    loaded_cases = cases()
    trailing = trailing_ceilings(loaded_cases)
    # Not a target to be held at any number; a measurement, and a loud one. Every one of
    # these is a case where reading `verified_upper_bound` as s(n) overstates the side
    # length. It was 33 until D-398 promoted n = 40, 65 and 89 off the integer grid ceiling
    # onto Goebel's exact family construction, whose certificates had been in the gate for
    # two sessions while the records still declared a mathematical blocker. Moving it down
    # is the point of the measurement, not a break in it: BC-089 took twelve cases off
    # the grid on 2026-08-31 -- n = 82 (the worst trailing gap, 0.464), the strip
    # family's 27, 38, 52, 67 and 84, the off-centre family's 26 and 85, and the lifted
    # witnesses 19 and 66 in Q(sqrt 2) and 18 and 86 in Q(sqrt 7) -- leaving n = 50's
    # 3/7 as the widest.
    # 16 at n = 1..100 after n=17's certified endpoint. New cases above 100 trail
    # on the grid ceiling wherever the catalogue reports a non-integer side.
    # The frozen catalogue certificates identify the old trailing closed forms.
    # A newly reported source can precede its replay, then disappear from this set
    # when its own exact ceiling is adopted. Neither event rewrites that old audit.
    frozen_trailing = {
        n
        for n, row in apply_exact_ceilings.committed().items()
        if not row["agrees_with_report"]
    } | {29}
    for corpus, expected in TRAILING_BY_CORPUS.items():
        limit = int(corpus.split("..", 1)[1])
        assert sum(n <= limit for n in frozen_trailing) == expected
    historical = {
        n
        for n, row in apply_exact_ceilings.committed().items()
        if not row["agrees_with_report"]
        and loaded_cases[n]["reported_upper_bound"]["source_key"] == "[Kingbird]"
    }
    pending = {
        n
        for n in squish.NUMBERS
        if loaded_cases[n]["reported_upper_bound"]["source_key"] == squish.source_key(n)
        and not any(
            e.startswith("E-squish-")
            for e in loaded_cases[n]["verified_upper_bound"]["evidence"]
        )
    }
    # Earlier SQUISH replay evidence certifies the earlier geometry, not this update.
    pending |= {
        n
        for n in squish_update.NUMBERS
        if loaded_cases[n]["reported_upper_bound"]["source_key"] == squish_update.SOURCE_KEY
        and not any(
            e.startswith("E-squish-update-")
            for e in loaded_cases[n]["verified_upper_bound"]["evidence"]
        )
    }
    pending |= {
        n
        for n in squish_second.NUMBERS
        if loaded_cases[n]["reported_upper_bound"]["source_key"] == squish_second.SOURCE_KEY
        and not any(
            e.startswith("E-squish-second-update-")
            for e in loaded_cases[n]["verified_upper_bound"]["evidence"]
        )
    }
    interval = (
        {29}
        if loaded_cases[29]["reported_upper_bound"]["source_key"] == "[Kingbird]"
        else set()
    )
    assert set(trailing) == historical | interval | pending
    for n, (reported, verified) in trailing.items():
        assert verified > reported, n
    # Up to 0.464 until 2026-10-06, when T-101's certificates took the last trailing
    # ceilings off the integer grid; what trails now does so by one unit of the printed
    # fourteenth decimal at most.
    worst = max(
        verified - reported for n, (reported, verified) in trailing.items() if n not in pending
    )
    assert worst <= Decimal("1E-14")

    # And in those cases `exact_form` is exact about the ceiling and says nothing about
    # s(n). None is the integer grid bound any more. n = 29 carries an interval
    # certificate's endpoint; every other trailing case reports a closed form, which the
    # rounded-up side of a rational certificate of its packing does not reach (T-101).
    grids = {
        n
        for n in trailing
        if loaded_cases[n]["verified_upper_bound"]["exact_form"] == str(math.isqrt(n - 1) + 1)
    }
    assert not grids
    closed = {n for n in trailing if loaded_cases[n]["reported_upper_bound"]["exact_form"]}
    assert sorted(set(trailing) - closed - pending) == sorted(interval)

    # Every case carrying an exact_form on the ceiling, split by whether s(n) is known.
    exact_forms = sum(
        1 for case in loaded_cases.values() if case["verified_upper_bound"]["exact_form"]
    )
    proved = sum(1 for case in loaded_cases.values() if case["status"] == "proved")
    assert exact_forms == KNOWN_BEST_CORPUS.count
    assert proved < exact_forms


def test_n17_endpoint_ceiling_keeps_report_and_optimality_distinct() -> None:
    case = cases()[17]
    upper = case["verified_upper_bound"]
    reported = case["reported_upper_bound"]
    assert upper == {
        "value": "4.6755300936045509516342148538535054",
        "exact_form": "23377650468022754758171074269267527/5000000000000000000000000000000000",
        "evidence": ["E-n017-certified-endpoint"],
    }
    assert Decimal(upper["value"]) < Decimal("4.675530093604551")
    assert Fraction(upper["exact_form"]) == Fraction(upper["value"])
    assert bounds_agree_at_declared_precision(reported, upper)
    assert reported["algebraic_degree"] == 18
    assert case["status"] == "open"
    assert case["verified_lower_bound"]["exact_form"] == "18641771/4000000"
    assert "E-n017-kleddamag-rational-upper" in case["evidence"]
    assert all(
        "E-kingbird-upper-register" not in blocker.get("evidence", [])
        for blocker in case["blockers"]
    )
    body = _body(17)
    assert CEILING_HEADING not in body
    assert "degree-18 polynomial" in body
    assert "global minimum" in body


def test_every_trailing_case_says_so_in_the_record_a_reader_opens() -> None:
    loaded_cases = cases()
    trailing = trailing_ceilings(loaded_cases)
    for n, (reported, verified) in sorted(trailing.items()):
        body = _body(n)
        assert CEILING_HEADING in body, f"n={n} certifies a weaker ceiling and does not say so"
        section = body.split(CEILING_HEADING, 1)[1].split("\n## ", 1)[0]
        # Its figures are math; read back, each is the code span it was written as.
        flat = " ".join(Reading.of(section).text.split())
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
        # n = 29's hand-written section prints Decimal's `9.18...E-15`; the Couzo ceilings
        # print the receipts' lowercase `2e-15`. Either spelling is the same number.
        assert gap in flat or gap.replace("E", "e") in flat, n
        assert f"not the value of `s({n})`" in flat, n
        assert "`reported_upper_bound`" in flat, n

    # The section is a statement about this case, so it must not appear where the
    # ceiling does reach the report.
    for n in set(loaded_cases) - set(trailing):
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


def _consumer_paths(root: Path) -> list[Path]:
    """Prune excluded trees, then return deterministic, included regular-file paths.

    Directory links are never followed. Included file links retain their lexical
    consumer names, but must resolve inside the checkout; broken or external links
    and included traversal/stat errors fail the check rather than hiding a consumer.
    """
    resolved_root = root.resolve(strict=True)
    paths: list[Path] = []

    def raise_walk_error(error: OSError) -> None:
        raise error

    for directory, subdirectories, filenames in os.walk(
        root, topdown=True, onerror=raise_walk_error, followlinks=False
    ):
        parent = Path(directory)
        # Dot-directories hold vendored agent skills and tooling state, not our prose.
        # Mutate this list before os.walk descends: filtering the resulting files is late.
        subdirectories[:] = [
            name
            for name in sorted(subdirectories)
            if name not in SKIPPED_PARTS
            and not name.startswith(".")
            and not stat.S_ISLNK((parent / name).lstat().st_mode)
        ]
        for name in sorted(filenames):
            path = parent / name
            if (
                path.suffix not in SEARCHED_SUFFIXES
                or name in SKIPPED_PARTS
                or name.startswith(".")
                or re.fullmatch(r"n-\d{3}\.md", name)
            ):
                continue
            metadata = path.lstat()
            if stat.S_ISLNK(metadata.st_mode):
                if not path.resolve(strict=True).is_relative_to(resolved_root):
                    raise ValueError(
                        f"included consumer symlink points outside checkout: {path}"
                    )
                metadata = path.stat()
            if not stat.S_ISREG(metadata.st_mode):
                continue
            relative = path.relative_to(root).as_posix()
            # Declared consumers are scanned however large they grow. `packing/defects.yaml`
            # crossed this generated-blob heuristic in D-392 and silently stopped being read.
            if metadata.st_size > GENERATED_BYTES and relative not in DECLARED_CONSUMERS:
                continue
            paths.append(path)
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def test_no_undeclared_consumer_reads_the_field() -> None:
    found: set[str] = set()
    for path in _consumer_paths(REPO):
        relative = path.relative_to(REPO)
        body = path.read_text(encoding="utf-8", errors="ignore").replace(OWN_NAME, "")
        if "verified_upper_bound" in body:
            found.add(relative.as_posix())
    undeclared = sorted(
        path
        for path in found - set(DECLARED_CONSUMERS)
        if not path.startswith(tuple(DECLARED_CONSUMER_TREES))
    )
    assert undeclared == [], (
        "these name verified_upper_bound without saying what they take it to mean; "
        "it is a ceiling, not s(n) -- add them to DECLARED_CONSUMERS with a reason"
    )
    stale = sorted(set(DECLARED_CONSUMERS) - found)
    assert stale == [], "declared consumers that no longer read the field"


def test_consumer_walk_prunes_before_descent_and_keeps_large_declared_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    excluded = [tmp_path / name for name in SKIPPED_PARTS | {".git", ".claude", ".hidden"}]
    for directory in excluded:
        directory.mkdir()
        (directory / "unread.md").write_text("verified_upper_bound", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    nested_excluded = nested / "node_modules"
    nested_excluded.mkdir()
    (nested_excluded / "unread.md").write_text("verified_upper_bound", encoding="utf-8")
    excluded.append(nested_excluded)
    (nested / "a.py").write_text("verified_upper_bound", encoding="utf-8")
    (tmp_path / "z.md").write_text("verified_upper_bound", encoding="utf-8")
    for name in ("large.md", "generated.md"):
        (tmp_path / name).write_text("x" * (GENERATED_BYTES + 1), encoding="utf-8")
    (tmp_path / "n-123.md").write_text("excluded frontier case", encoding="utf-8")
    (tmp_path / ".hidden.md").write_text("excluded hidden file", encoding="utf-8")
    monkeypatch.setitem(DECLARED_CONSUMERS, "large.md", "large declared control")
    original_scandir = os.scandir

    def guarded_scandir(path: str | os.PathLike[str]):
        assert not any(Path(path).is_relative_to(directory) for directory in excluded)
        return original_scandir(path)

    monkeypatch.setattr(os, "scandir", guarded_scandir)
    assert [path.relative_to(tmp_path).as_posix() for path in _consumer_paths(tmp_path)] == [
        "large.md",
        "nested/a.py",
        "z.md",
    ]


def test_consumer_walk_has_explicit_symlink_and_error_boundaries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    nested = root / "nested"
    nested.mkdir()
    source = nested / "source.py"
    source.write_text("verified_upper_bound", encoding="utf-8")
    (root / "alias.py").symlink_to(source)
    (root / "directory-alias").symlink_to(nested, target_is_directory=True)
    assert [path.relative_to(root).as_posix() for path in _consumer_paths(root)] == [
        "alias.py",
        "nested/source.py",
    ]
    external = tmp_path / "outside.py"
    external.write_text("verified_upper_bound", encoding="utf-8")
    (root / "outside.py").symlink_to(external)
    with pytest.raises(ValueError, match="outside"):
        _consumer_paths(root)
    (root / "outside.py").unlink()
    broken = root / "broken.py"
    broken.symlink_to(root / "missing.py")
    with pytest.raises(FileNotFoundError):
        _consumer_paths(root)
    broken.unlink()
    original_scandir = os.scandir

    def unreadable(path: str | os.PathLike[str]):
        if Path(path) == nested:
            raise PermissionError("included directory cannot be read")
        return original_scandir(path)

    monkeypatch.setattr(os, "scandir", unreadable)
    with pytest.raises(PermissionError, match="included directory"):
        _consumer_paths(root)


def _body(n: int) -> str:
    return (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8").split("---\n", 2)[2]
