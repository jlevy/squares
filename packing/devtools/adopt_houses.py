# ruff: noqa: RUF001 -- this module writes case prose, whose typography uses curly apostrophes.
"""Move each case record to the house `devtools.select_houses` derives from the register.

The register held confirmed, reviewed upper bounds by others below their case records'
ceilings, each *pending adoption*, while house adoption waited for jlevy/squares#403; the
owner lifted that wait on 11 October 2026. For every count whose house moves, this writes:

- **the case record's front matter**: the reported and the verified upper bound move
  together to the house's exact side, the reported lane citing the source's report and
  the verified lane its confirming replay; the earlier house becomes a priority note,
  kept as history; every confirmed certificate at the count, selected or not, joins the
  case's evidence roster, which is what lets `check_certificate_citations` drop its
  deferrals; the source joins the resources; a conjectured optimum the house is below,
  wherever its print may round, is withdrawn, and any other stays (`conjecture_stands`);
  a blocker that only said the verified lane trailed the report goes;
- **the case record's body**: a dated paragraph under the title that states the move,
  and a section after the verification code that says whose certificate the house is,
  how it was confirmed here and which certificates it replaces;
- **the coverage register**: the count's selected override names the new source, the
  reports the earlier one superseded name the new one, and the earlier selected claim is
  itself recorded as superseded;
- **the deferrals**: every `certificate-citation-deferrals.yaml` entry whose evidence a
  case record now cites is removed, as that file requires;
- **the prior state**: before the first record is written, each moved record's complete
  earlier text is retained in the archive of the pass that moves it (`prior_state`), as
  the Ry-Xu and Gupta adoptions retain theirs, so the tests of a source this adoption
  displaced can still draft its case as that source held it, and the writer can be
  replayed from what each pass read. The earlier houses are not copied: each is rebuilt
  from its own retained packet.

The drawing, `witnesses/known-best/n-NNN.yaml`, is `devtools.upper_bound_houses`'s; this
refuses a count that module does not house. A new house is a new witness, so what follows
a write is the regularization guide's "When a Witness Changes", not the axis tool's
refresh alone: `build_known_best_atlas --update` for the witness, the axis tool's
`--update-atlas`, `default_drawings --update`, then the strong generators on each count it
reads `pending`, in the same pull request, with each re-housed count's drawing listed
before and after. The house rule defers no re-housed count's runs to
`default_drawings.PENDING_ALLOWED`: an adoption whose runs do not fit under the pass's
compute cap waits with them, staged in `select_houses.PENDING_ADOPTION`. The adoptions of
#553, #598 and #614 ran only the axis tool's refresh and left twenty counts without a
strong generator's decision, n = 176 drawn raw (think-sfas). So a write, and `--dry-run`,
print what the moves owe the regularized layer (`regularization_owed`): the counts, the
commands with run directories no earlier run has named, and what they cost;
`default_drawings --check-state` fails until each pending count is decided, and while the
allowlist defers the runs of a witness whose house has moved since
(`default_drawings.deferral_problems`, keyed on the witness, not on a pass's day).
`adopt_case` is the generator's half: `generate_frontier_case` redrafts an adopted case
through it (`source_supersession.adopt_selected_report`), which keeps the house and takes
the ordinary lower lanes from the draft.

It is idempotent: a count already at its house is left alone, so a second run writes
nothing, and ``--check`` reports any adopted count whose record differs from its house.

**The house rule** (packing/campaign/result-import.md, "The House Rule") leaves nothing
here to a person: the house is the smallest validated side, and a count whose adoption
waits does so only staged in `select_houses.PENDING_ADOPTION` with the bead that adopts
it, which `plan` leaves to that bead's pull request. Until the counts are adopted, their
records keep the houses the rule of 15 October chose, and say why, with no wait left to
the owner (review A2 of #660): an adopted record's certificate section names each
certificate the lifted hold kept out (`select_houses.LIFTED`) below its house, why it
waited, that the house rule lifted the hold, and the bead its staged adoption waits
under, and so does a dated paragraph under the title of a record no pass houses
(`held_note`), which also cites the held certificate's evidence; an algebraic certificate
below the house, which that rule left out (RP-3), is named in the section the same way,
its adoption staged for the writer. Every replay and check here reads the records as
written (`recorded_days`, `select_houses.select(recorded=...)`).

Usage, from ``packing/`` with the project interpreter::

    python -m devtools.adopt_houses             # write
    python -m devtools.adopt_houses --dry-run   # list what would move
    python -m devtools.adopt_houses --check     # hold every adopted case to its house
    python -m devtools.adopt_houses --refresh   # full replay, refusing later lower layers
    python -m devtools.adopt_houses --refresh-openings  # only the current dated paragraph
    python -m devtools.adopt_houses --refresh --n 155 229  # only those records

``--refresh`` brings every adopted record's evidence roster, dated paragraph and
certificate section to what its last pass's writer writes now, from the record that pass
read, and every held count's note to the lifted holds. It refuses a record whose lower
lanes have changed since that pass, before writing any record: reconciling those later
writers' evidence and prose needs an explicit merge rather than a historical replay.
A record changes this way when the register gains a confirmed certificate at its count.
For an opening-only wording correction, ``--refresh-openings`` leaves all other bytes
alone, including evidence and prose a later lower-bound writer has added. Both refreshes
also bring each adopted count's selected override reason in the coverage register to
what the writer writes now (`override_reason`), which ``--check`` holds. ``--n`` limits
either refresh to the records it names, so a writer change at a few counts is applied
without replaying a record whose later layer the full refresh refuses.

**A later pass.** A later import adopted the same way needs:

- its register entry at `V3`/`C3` with an accepted review covering it;
- its packet in `upper_bound_houses._sources`, each count it houses in
  `upper_bound_houses.ADOPTED`, and those counts under the pass's day in
  `upper_bound_houses.LATER_PASSES`, which dates every sentence, note, review date and
  coverage reason this writes for them;
- a coverage-register entry for its source key whose scope holds each count it houses.
  Where that entry declares a `claims_record`, the record must print the in-corpus claims,
  since `_value` holds the selected value to its print: a record that holds only claims
  beyond the corpus refuses the adoption. Such a source takes a second entry for its
  in-corpus counts with no claims record, as issue 506's does (`coverage_source`); Hunt
  3's moved its `claims_record` to `claims.json` for the same reason;
- its prose in `RESULTS` and each count's credit in `CREDITS` here.

`select_houses` then names the counts and this writes them. A count an earlier pass
adopted is adopted again in place: the earlier pass's paragraph, section and verified
statements are marked as history (`historical`), its house becomes a note dated from the
day it was adopted until this one, and its selected override becomes a superseded row.
The pass retains each record it moves, as it stood before, in an archive of its own day;
the earlier pass's archive is never rewritten, so the writer can be replayed from each
count's state before its last pass (`before_last_pass`) and the history readers still
find each count as it stood before its first (`read_history`).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any, cast

import yaml
from strif import atomic_output_file

from devtools import apply_closed_form as closed_form
from devtools import default_drawings, exact_sides, select_houses
from devtools import upper_bound_houses as houses
from sqpack.yamlio import safe_load

ROOT = select_houses.ROOT
REPO = select_houses.REPO
FRONTIER = select_houses.FRONTIER
COVERAGE = FRONTIER / "source-coverage.yaml"
BIBLIOGRAPHY = ROOT / "resources/bibliography.yaml"
DEFERRALS = ROOT / "devtools/certificate-citation-deferrals.yaml"
PRIOR_FORMAT = "house-adoption-prior-frontier-v1"
WIDTH = 96
FINAL_REVIEW = "docs/project/reviews/review-2026-10-11-final-upper-bounds.md"
FOOTER = "<!-- This document follows common-doc-guidelines.md."
PLACES = select_houses.DISPLAY_PLACES
#: Longest exact fraction the prose writes out; a longer one is given by its decimals.
FRACTION_CHARS = 72
#: The verifier table, which `render_case_verifiers` writes into the body, not this.
VERIFIER_TABLE = re.compile(
    r"<!-- BEGIN verification code.*?<!-- END verification code -->", re.DOTALL
)
#: Counts whose body a pass marked as history by hand, in prose no tool writes in a fixed
#: form (`historical`): the first pass, on 11 October 2026, the SQUISH update sections at
#: 155, 258, 263 and 302 and the grid prose at 308, and the pass of 19 October 2026 the
#: intake's staging paragraph, grid sentence and packing section at 183 (T-220). Only
#: their owned parts are the writer's.
HAND_MARKED = frozenset({155, 183, 258, 263, 302, 308})
#: The first pass whose writer also marks the closing sentence of a T-155 view's section as
#: history (`_regularized_certificate`); earlier passes' records read as they wrote them.
VIEW_SECTION_FROM = "2026-10-19"
#: The pass that retained and registered Couzo's #672 (T-227), from which the intake's and
#: T-199's sentences saying it was not retained are history (`_retained_672`).
RETAINED_672_FROM = "2026-10-22"
#: The first pass whose writer marks an earlier section's staged-adoption sentence as history
#: (`staged_history`): on 20 October 2026 issue 678's certificate (T-223) took 204 off T-193's
#: staged adoption, the first staged count a smaller packing overtook in a written section.
STAGED_HISTORY_FROM = "2026-10-20"


@dataclass(frozen=True)
class Prose:
    """What a case body says of one adopted result's certificates."""

    author: str
    reported: str
    producer_route: bool
    ai: str
    #: Where the source itself ran this repository's maintained routes, what to say instead.
    routes: str = ""
    #: What the source says of where the packing came from and what was measured of it
    #: here, where its review asked the record to say so (T-160's RD-1, RD-5 and RD-7).
    lineage: str = ""
    #: Each count's own lineage paragraph, where one result's counts have different starts
    #: and measurements (T-223: Polkovskyi's construction at 204, de Winter's #668 packing at
    #: 260; review A4 of #706); `lineage` stands for a count this does not name.
    lineage_at: Mapping[int, str] | None = None
    #: Whether `devtools.check_half_angle_area`, the third exact route, decided the
    #: certificate too. T-220's replay ran the two maintained routes only, so its record
    #: says no third route decided it rather than that one did. A string is the clause the
    #: record writes instead, where the review decided the certificate on an exact route of
    #: its own that no verifier entry names (T-224, A5 of the 21 October review).
    third_route: bool | str = True
    #: Which confirmation the verified bound's sentence names, as the register's relation
    #: reads it (`verifier_registry.LABELS`). T-223's two routes share the corner verifier
    #: its source reports running, so its replay shares the producer's components.
    confirmation: str = "independently re-implemented"
    #: How the certificate states each square. T-196's states a rational centre and the
    #: rotation's cosine and sine, which the adapter turns into a half-angle tangent.
    squares: str = "a rational centre and the tangent of its half-angle"


#: Each adopted result, as its register entry and its review describe it.
RESULTS: dict[str, Prose] = {
    "T-128": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#451](https://github.com/jlevy/squares/issues/451)",
        producer_route=True,
        ai="",
    ),
    "T-130": Prose(
        author="Francisco Couzo",
        reported=(
            "in a comment on "
            "[pull request #460](https://github.com/jlevy/squares/pull/460#issuecomment-6070798890)"
        ),
        producer_route=True,
        ai="",
    ),
    "T-134": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#476](https://github.com/jlevy/squares/issues/476)",
        producer_route=True,
        ai="The author says the search was written with Claude under his direction.",
    ),
    "T-136": Prose(
        author="Nate Chaoweeraprasit",
        reported="on [jlevy/squares#481](https://github.com/jlevy/squares/issues/481)",
        producer_route=False,
        ai=(
            "The source states that SQUISH’s solver, its verification and the issue were "
            "written with Claude Opus 5.5 under the author’s direction."
        ),
    ),
    "T-139": Prose(
        author="Evan Daniel",
        reported="in his repository’s `search/trio126` directory, on no issue",
        producer_route=False,
        ai="The source’s commit names Claude Opus 5.5 as co-author.",
    ),
    "T-140": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#488](https://github.com/jlevy/squares/issues/488)",
        producer_route=True,
        ai=(
            "The author says the search code and the request were written with Claude "
            "under his direction."
        ),
    ),
    "T-141": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#489](https://github.com/jlevy/squares/issues/489)",
        producer_route=False,
        ai=(
            "The author says the search code and the request were written with Claude "
            "under his direction."
        ),
    ),
    "T-146": Prose(
        author="Evan Daniel",
        reported="in his regularized record lists, on no issue",
        producer_route=False,
        ai=(
            "The source’s credits say the repository’s work was produced by Claude "
            "(Anthropic) under human direction."
        ),
    ),
    "T-147": Prose(
        author="PingYou Ltd",
        reported="on [jlevy/squares#503](https://github.com/jlevy/squares/issues/503)",
        producer_route=False,
        ai=(
            "The source’s first commit and the issue as first posted said that verification, "
            "comparison review and package preparation were assisted by OpenAI Codex; the "
            "pinned commit removed that sentence, giving no reason. Asked which account "
            "stands, the author wrote on jlevy/squares#503 on 12 October 2026: “Both "
            "solutions were AI assisted by ‘PY’, an unreleased agentic AI offering by "
            "PingYou Ltd.”"
        ),
        routes=(
            "The source ran both maintained routes itself before reporting; both predate it, "
            "and the third route is independently re-implemented."
        ),
    ),
    "T-148": Prose(
        author="PingYou Ltd",
        reported="on [jlevy/squares#504](https://github.com/jlevy/squares/issues/504)",
        producer_route=False,
        ai=(
            "The source makes no statement about AI assistance; the same author’s n207 "
            "release, eight minutes earlier, removed a disclosure of OpenAI Codex assistance "
            "at its pin. Asked which account stands for both releases, the author wrote on "
            "jlevy/squares#503 on 12 October 2026: “Both solutions were AI assisted by ‘PY’, "
            "an unreleased agentic AI offering by PingYou Ltd.”"
        ),
        routes=(
            "The source ran both maintained routes itself before reporting; both predate it, "
            "and the third route is independently re-implemented."
        ),
    ),
    "T-149": Prose(
        author="Daniil Ostashev",
        reported="on [jlevy/squares#501](https://github.com/jlevy/squares/issues/501)",
        producer_route=False,
        ai="The source states nothing about AI assistance.",
    ),
    "T-150": Prose(
        author="Robert Barnett",
        reported="on [jlevy/squares#505](https://github.com/jlevy/squares/issues/505)",
        producer_route=False,
        ai=(
            "The author discloses OpenAI Codex assistance with the solver, the certificate "
            "and checker code, source review and preparation."
        ),
    ),
    "T-151": Prose(
        author="Nate Chaoweeraprasit",
        reported="on [jlevy/squares#500](https://github.com/jlevy/squares/issues/500)",
        producer_route=False,
        ai=(
            "The source states that SQUISH’s solver, its verification and the issue were "
            "written with Claude Opus 5.5, and that the Mondrian composition method was "
            "formulated by the author and implemented with Claude Opus 5.5, under his "
            "direction."
        ),
    ),
    "T-152": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#506](https://github.com/jlevy/squares/issues/506)",
        producer_route=True,
        ai=(
            "The author says the search code and the request were written with Claude "
            "under his direction."
        ),
    ),
    "T-158": Prose(
        author="Daniil Ostashev",
        reported="on [jlevy/squares#528](https://github.com/jlevy/squares/issues/528)",
        producer_route=False,
        ai=(
            "The issue says the author set up an AI-assisted research loop and drove it with "
            "his own ideas, the rectangle library and the composition being his, and that AI "
            "agents wrote and ran the search, composition and verification code."
        ),
    ),
    "T-160": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#552](https://github.com/jlevy/squares/issues/552)",
        producer_route=False,
        ai=(
            "The issue says the search code, the run and the request were done with Claude "
            "(Claude Code), which Evan Daniel directed and reviewed."
        ),
        lineage=(
            "The author states that the packing came from a time-travel test of his "
            "size-chaining explorer, restarted from this register as it stood on 5 October, "
            "and that it descends from Francisco Couzo’s 5 October packing of 155 squares "
            "with one square removed; he asks that the start be credited to that packing, and "
            "it is. Measured here, the packing is another arrangement than T-136’s: no "
            "symmetry of the box pairs the two square for square. The measurements are "
            "consistent with the author’s account of the start and do not establish it: 43 "
            "squares of Couzo’s 155 reappear to the digit, but so do 45 of his 154, and the "
            "round-by-round trace is not published."
        ),
    ),
    "T-161": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#561](https://github.com/jlevy/squares/issues/561)",
        producer_route=True,
        ai=(
            "The author states that OpenAI Codex assisted the continuing search, the "
            "application work, the source audit, the verification orchestration and the "
            "request, that earlier search code and submissions were prepared with Claude "
            "Code, and that he directed the work."
        ),
    ),
    "T-162": Prose(
        author="Daniil Ostashev",
        reported="on [jlevy/squares#562](https://github.com/jlevy/squares/issues/562)",
        producer_route=False,
        ai=(
            "The issue says the author drives an AI-assisted research loop with his own "
            "ideas, the rectangle library and the composition being his, and that AI agents "
            "wrote and ran the search, composition and verification code."
        ),
        lineage=(
            "The issue says the 129 is cut from the n = 302 house of the time, Evan Daniel’s "
            "view of Nate Chaoweeraprasit’s SQUISH packing, and re-optimised, and that the "
            "204 and 303 are new arrangements. Measured here, the 129 pairs square for square "
            "with neither Ryan Xu’s packing nor T-146’s, though 46 of Xu’s squares lie in "
            "place under a quarter turn, and 49 of the 302’s reappear in it by pose; that "
            "supports the author’s account and establishes none of it."
        ),
    ),
    "T-165": Prose(
        author="Francisco Couzo",
        reported=(
            "in [his repository](https://github.com/franciscouzo/square-packing) on 12 "
            "October 2026, with no issue"
        ),
        producer_route=True,
        ai=(
            "The commit makes no statement about AI assistance; the author’s issues of 12 "
            "and 13 October say OpenAI Codex assisted the search and verification and that "
            "he directed the work."
        ),
    ),
    "T-168": Prose(
        author="PingYou Ltd",
        reported="on [jlevy/squares#566](https://github.com/jlevy/squares/issues/566)",
        producer_route=False,
        ai="The pinned source makes no statement about AI assistance.",
        routes=(
            "The source ran both maintained routes itself on its corners witnesses; those "
            "runs are its own, and the replay here is independently re-implemented."
        ),
    ),
    "T-169": Prose(
        author="PingYou Ltd",
        reported="on [jlevy/squares#567](https://github.com/jlevy/squares/issues/567)",
        producer_route=False,
        ai="The pinned source makes no statement about AI assistance.",
        routes=(
            "The source ran both maintained routes itself on its corners witnesses; those "
            "runs are its own, and the replay here is independently re-implemented."
        ),
    ),
    "T-170": Prose(
        author="PingYou Ltd",
        reported="on [jlevy/squares#568](https://github.com/jlevy/squares/issues/568)",
        producer_route=False,
        ai=(
            "The issue states that computation, checking and submission preparation were "
            "AI-assisted; the pinned source makes no statement about AI assistance."
        ),
        routes=(
            "The source ran both maintained routes itself on its corners witnesses; those "
            "runs are its own, and the replay here is independently re-implemented."
        ),
    ),
    "T-171": Prose(
        author="PingYou Ltd",
        reported="on [jlevy/squares#569](https://github.com/jlevy/squares/issues/569)",
        producer_route=False,
        ai=(
            "The issue states that computation, checking and submission preparation were "
            "AI-assisted; the pinned source makes no statement about AI assistance."
        ),
        routes=(
            "The source ran both maintained routes itself on its corners witnesses; those "
            "runs are its own, and the replay here is independently re-implemented."
        ),
    ),
    "T-173": Prose(
        author="Mykhailo Polkovskyi",
        reported="on [jlevy/squares#573](https://github.com/jlevy/squares/issues/573)",
        producer_route=True,
        ai=(
            "The issue says Gemini was used for the search implementation, the verification "
            "orchestration and the issue’s preparation, directed by the author."
        ),
    ),
    "T-174": Prose(
        author="PingYou Ltd",
        reported="in [pull request #574](https://github.com/jlevy/squares/pull/574)",
        producer_route=False,
        ai=(
            "The source makes no statement about AI assistance in this pull request; for "
            "its #503 and #504 certificates the author said on 12 October 2026 that they "
            "were AI assisted by ‘PY’, an unreleased agentic AI offering by PingYou Ltd."
        ),
        routes=(
            "The source ran both maintained routes itself on its corners witnesses; those "
            "runs are its own, and the replay here is independently re-implemented."
        ),
    ),
    "T-175": Prose(
        author="Daniil Ostashev",
        reported="on [jlevy/squares#575](https://github.com/jlevy/squares/issues/575)",
        producer_route=False,
        ai=(
            "The issue says the author drives an AI-assisted research loop with his own "
            "ideas, merging the tilted bands being his, and that AI agents wrote and ran the "
            "search and verification code."
        ),
    ),
    "T-181": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#583](https://github.com/jlevy/squares/issues/583)",
        producer_route=True,
        ai=(
            "The author says OpenAI Codex assisted the search implementation, the "
            "verification orchestration and the requests, that earlier search work used "
            "Claude Code, and that he directed the work."
        ),
    ),
    "T-182": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#586](https://github.com/jlevy/squares/issues/586)",
        producer_route=True,
        ai=(
            "The author says OpenAI Codex assisted the search implementation, the "
            "verification orchestration and the requests, that earlier search work used "
            "Claude Code, and that he directed the work."
        ),
    ),
    "T-183": Prose(
        author="Mykhailo Polkovskyi",
        reported="on [jlevy/squares#593](https://github.com/jlevy/squares/issues/593)",
        producer_route=True,
        ai=(
            "The source discloses Gemini assistance with solver scripting, precision checks "
            "and formatting."
        ),
    ),
    "T-186": Prose(
        author="Mykhailo Polkovskyi",
        reported=(
            "in [his repository](https://github.com/Mishapolk/square-packing-records) on 14 "
            "October 2026, with no issue"
        ),
        producer_route=False,
        ai=(
            "The commit makes no statement about AI assistance; the author’s issue 593 "
            "discloses Gemini assistance with solver scripting, precision checks and "
            "formatting."
        ),
    ),
    "T-187": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#606](https://github.com/jlevy/squares/issues/606)",
        producer_route=False,
        ai=(
            "The issue says the search, the checks and the request were done with Claude "
            "(Claude Code), directed and reviewed by Evan Daniel."
        ),
        lineage=(
            "The author started his chain search from Ryan Xu’s packing and names Robert "
            "Barnett’s refinement of it as the record it improves, calling the result a "
            "different local minimum. Measured here pose by pose, it pairs one to one with "
            "Xu’s packing and with Barnett’s under the identity, nine squares moving beyond a "
            "tenth: another arrangement of Xu’s design, a refinement of neither (T-187)."
        ),
    ),
    "T-188": Prose(
        author="Francisco Couzo",
        reported=(
            "in [his repository](https://github.com/franciscouzo/square-packing) on 14 "
            "October 2026, with no issue"
        ),
        producer_route=True,
        ai=(
            "The commit makes no statement about AI assistance; the author’s issues of 13 and "
            "14 October say OpenAI Codex assisted the search and verification "
            "orchestration, that earlier search work used Claude Code, and that he directed "
            "the work."
        ),
        lineage=(
            "The certificate’s metadata seeds the author’s search from Daniil Ostashev’s "
            "certificate, whose digest is that of issue 575’s, though it labels it issue 501. "
            "Measured here pose by pose, it continues Ostashev’s issue-575 arrangement as the "
            "author’s issue-583 and issue-586 certificates did, five squares moving beyond a "
            "tenth against each: another arrangement of that design (T-188)."
        ),
    ),
    "T-190": Prose(
        author="Francisco Couzo",
        reported=(
            "in [his repository](https://github.com/franciscouzo/square-packing) on 15 "
            "October 2026, with no issue"
        ),
        producer_route=True,
        ai=(
            "The commit makes no statement about AI assistance; the author’s issue 607, of "
            "the day before, says OpenAI Codex assisted the search and verification "
            "orchestration, that earlier search work used Claude Code, and that he directed "
            "the work."
        ),
    ),
    "T-195": Prose(
        author="PingYou Ltd",
        reported="in [pull request #622](https://github.com/jlevy/squares/pull/622)",
        producer_route=False,
        ai=(
            "The author says all of its submissions are PingYou Ltd’s, assisted by the PY "
            "agentic offering."
        ),
        routes=(
            "The source ran both maintained routes itself on its corners witness, so on them "
            "the replay reproduces its runs; the third route and the review’s clean-room "
            "checker, which share no code with any check it ran, are independently "
            "re-implemented."
        ),
    ),
    "T-197": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#669](https://github.com/jlevy/squares/issues/669)",
        producer_route=False,
        ai=(
            "The issue says the work was done with Claude (Claude Code), directed and "
            "approved by Evan Daniel."
        ),
        lineage=(
            "The author’s basin explorer started from Daniil Ostashev’s packing, the "
            "register’s witness for 155 when the search ran, and reached this one after a "
            "chain of 18 moves; the issue credits that packing as the start. Measured here "
            "square by square, no symmetry of the box pairs the two one to one, and the best "
            "assignment moves 29 squares beyond a tenth, sharing no tilt: a new arrangement "
            "found from Ostashev’s packing (T-197)."
        ),
    ),
    "T-199": Prose(
        author="Evan Daniel",
        reported=(
            "in [an update]"
            "(https://github.com/jlevy/squares/issues/674#issuecomment-6244298663) on "
            "[jlevy/squares#674](https://github.com/jlevy/squares/issues/674)"
        ),
        producer_route=False,
        ai=(
            "The issue says the work was done with Claude (Claude Code), directed and "
            "approved by Evan Daniel."
        ),
        lineage=(
            "The certificate is a dilation of the author’s binary64 packing by about "
            "1 + 10⁻¹² with rational half-angle tangents; measured here, it pairs one to one "
            "with his opening report (T-198), eight squares beyond a tenth. The issue credits "
            "Francisco Couzo’s #672 packing, itself after Joost de Winter’s #668, as the "
            "start; it carries de Winter’s four tilt bands but does not pair with his packing, "
            "and #672 is not yet retained, so that step is the source’s (T-199)."
        ),
    ),
    "T-218": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#659](https://github.com/jlevy/squares/issues/659)",
        producer_route=False,
        ai=(
            "The issue says the work was done with Claude (Claude Code), directed and "
            "approved by Evan Daniel."
        ),
        lineage=(
            "The author’s basin explorer descended to this packing from a rebuild of Nate "
            "Chaoweeraprasit’s SQUISH composition of #481, made from Kingbird’s s(152)_r2 "
            "corner piece and itsnaka’s s(88); the issue credits that composition for the "
            "construction. Measured here, the best assignment against the view of #481’s "
            "packing the case held moves ten squares beyond a tenth and keeps 226 within one: "
            "another arrangement of #481’s design (T-218)."
        ),
    ),
    "T-219": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#664](https://github.com/jlevy/squares/issues/664)",
        producer_route=False,
        ai=(
            "The issue says the work was done with Claude (Claude Code), directed and "
            "approved by Evan Daniel."
        ),
        lineage=(
            "The author’s basin explorer started from the register’s witness for 271 and "
            "found this packing with one tilt-swap move and a re-polish; the issue calls it a "
            "refinement of Francisco Couzo’s #561 packing of Nate Chaoweeraprasit’s SQUISH "
            "design and asks that both be credited. Measured here, it pairs one to one with "
            "#561’s packing, three squares beyond a tenth: Couzo’s arrangement continued, not "
            "a refinement in this record’s sense (T-219). The author’s comment of 20 October "
            "on the issue says he meant a different local minimum and asks to be named its "
            "finder, with #561’s packing and the SQUISH design it continues as its start, as "
            "at 146, 236 and 308; the case credits it so."
        ),
    ),
    "T-220": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#680](https://github.com/jlevy/squares/issues/680)",
        producer_route=False,
        ai=(
            "The source’s credits say its work was produced by Claude (Anthropic) under "
            "human direction, and the commit that publishes the certificate names Claude "
            "Opus 5.5 as co-author."
        ),
        lineage=(
            "The author asks that the start be credited to Francisco Couzo’s n = 182 "
            "packing, this register’s witness of the time, and it is: his basin explorer ran "
            "17 moves at n = 182 from that witness to a packing that was no record, a square "
            "was inserted into it, and a tilt-angle swap, two two-parent crossovers and "
            "refinement led to this certificate. The crossovers’ second parents, other "
            "packings of the same run, were not logged, so that lineage is the author’s "
            "account and is not measured here. The source’s 27 numerical candidate flat "
            "modes concern the 182-square force-bearing subsystem, excluding a free rattler, "
            "and prove no local optimality."
        ),
        third_route=False,
    ),
    "T-196": Prose(
        author="Joost de Winter",
        reported="on [jlevy/squares#668](https://github.com/jlevy/squares/issues/668)",
        producer_route=False,
        ai=(
            "The issue says the search, numerical optimization, rational certificates, "
            "checkers and figures were made with OpenAI Codex agents under Joost de Winter’s "
            "direction, and that Claude (Anthropic) replayed the checkers and prepared the "
            "repository for publication."
        ),
        lineage=(
            "The issue says the search started from this repository’s catalogue, whose "
            "credits for the former packings apply, and built asymmetric Young-corner fills "
            "around slipped tilted ribbons, then restored the supports and angles; the three "
            "counts are one construction family, and the 229-square packing descends from the "
            "260-square one. None of this lineage is measured here (T-196)."
        ),
        squares="a rational centre and the cosine and sine of its rotation",
    ),
    "T-221": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#689](https://github.com/jlevy/squares/issues/689)",
        producer_route=False,
        ai=(
            "The source’s credits say its work was done with Claude (Anthropic) under human "
            "direction, and the commit that publishes the certificate names Claude Opus 5.5 "
            "as co-author and says Evan Daniel approved it."
        ),
        lineage=(
            "The author’s chained explorer inserted one square into Nate Chaoweeraprasit’s n = "
            "307 packing of #481, the register’s witness for 307, and his basin explorer "
            "descended from there to this packing; the issue asks that the 307 packing be "
            "credited as the ultimate start, and says the packing neither refines nor descends "
            "from Kevin Fang’s #484 or Daniel’s #489. Measured by the 20 October review, "
            "square by square, the best assignment against #489’s packing under a quarter turn "
            "moves 15 squares beyond a tenth, at most 0.708, and keeps 293 within one, and 263 "
            "of the 307 squares of #481’s packing lie within a tenth of this one: another "
            "arrangement of the two-wedge design that #484, #489 and #481’s 307 share, found "
            "from #481’s 307 by the source’s account (T-221)."
        ),
    ),
    "T-222": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#694](https://github.com/jlevy/squares/issues/694)",
        producer_route=False,
        ai=(
            "The source’s credits say its work was done with Claude (Anthropic) under human "
            "direction, and the commit that publishes the certificate names Claude Opus 5.5 "
            "as co-author and says Evan Daniel approved it."
        ),
        lineage=(
            "The author’s chained explorer removed two squares from Daniil Ostashev’s n = 156 "
            "packing, the register’s witness for 156, and crossovers against close relatives "
            "of Francisco Couzo’s #586 packing and a later restart of his basin explorer "
            "reached this packing; the issue asks that #586’s arrangement, itself continued "
            "from Daniel’s #552, and Ostashev’s packing be credited as its starts, and calls "
            "it a different KKT point in #586’s family. Measured by the 20 October review, "
            "square by square, it pairs one to one with #586’s packing under a quarter turn, "
            "three squares beyond a tenth, at most 0.204: Couzo’s arrangement continued, not a "
            "refinement in this record’s sense (T-222), as Daniel’s packing at 271 (T-219) "
            "continues Couzo’s #561 arrangement. Ostashev’s packing lies within a tenth of it "
            "at only 94 of its 156 squares, so his credit as the start rests on the source’s "
            "account of the search, and Couzo’s on the measured arrangement."
        ),
    ),
    "T-223": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#678](https://github.com/jlevy/squares/issues/678)",
        producer_route=True,
        ai=(
            "The issue states nothing about AI assistance; the header of the source’s "
            "checker names Codex, and the author’s issues of 13 and 14 October 2026 disclose "
            "OpenAI Codex and Claude Code assistance."
        ),
        routes=(
            "One maintained route, `sqpack`’s predicates, is the corner verifier the source "
            "reports running, and the packet’s filtered replay reads the certificate once "
            "for both routes, through one parser, half-angle map and pair filter; the "
            "source’s own checker, run unchanged from its retained copy, accepted it too."
        ),
        lineage_at={
            204: (
                "The source’s manifest credits Mykhailo Polkovskyi’s construction as the seed "
                "at 204. Measured by review A of #706 under the box’s symmetries against "
                "T-186’s packing, the house best packing here before this adoption and the "
                "record’s packing of Polkovskyi’s refinement, 87 of the 204 squares lie within "
                "10⁻⁴ of a square of it with the same axes and 44 moved by more than 10⁻², 14 "
                "of them beyond a tenth: not a refinement of that packing in place "
                "([the review programs](../resources/web/couzo-issue678-2026-10-18/review/"
                "README.md), T-223)."
            ),
            260: (
                "The source’s manifest credits Joost de Winter’s #668 packing as the seed at "
                "260, through Evan Daniel’s exact-form certificate of it in "
                "[`evand/square-packing`](https://github.com/evand/square-packing), which the "
                "issue’s comment of 19 October names and the intake retained. Measured here "
                "under the box’s symmetries, 162 of the 260 squares lie within 10⁻⁴ of a "
                "square of that seed and 55 moved by more than 10⁻²: not a refinement of the "
                "seed in place (T-223)."
            ),
        },
        confirmation="re-implemented, sharing the producer’s components",
    ),
    "T-224": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#703](https://github.com/jlevy/squares/issues/703)",
        producer_route=False,
        ai=(
            "The source’s credits say its work was done with Claude (Anthropic) under human "
            "direction, and the commit that publishes the certificate names Claude Opus 5.5 "
            "as co-author and says Evan Daniel approved it."
        ),
        lineage=(
            "The author’s basin explorer started from Nate Chaoweeraprasit’s n = 270 packing "
            "of #500, the register’s packing for 270, which PingYou Ltd’s certificate (T-174) "
            "refines, and stored non-record descendants of it; a near-record sweep over them "
            "reached this packing. The issue asks that #500’s packing be credited as the "
            "ultimate start, and calls this a different local minimum from the register’s. "
            "Measured by the 21 October review, square by square, the best assignment "
            "against T-174’s packing, which is #500’s to $10^{-30}$, is the identity: it "
            "keeps 255 of the 270 squares within a tenth and moves 15 beyond it, at most "
            "0.224, and no tilt angle is shared. So it is another arrangement of the design "
            "that packing holds, not a refinement in this record’s sense, found from #500’s "
            "packing by the source’s account (T-224)."
        ),
        third_route=(
            "; the 21 October review’s own exact route, which no verifier entry names, "
            "decided it again by separating axes on every pair and exact intersection area "
            "on the near pairs, and its sharp controls at $10^{-30}$ found both maintained "
            "routes exact at the far wall and at the closest pair"
        ),
    ),
    "T-225": Prose(
        author="Evan Daniel",
        reported="in his regularized record lists, on no issue",
        producer_route=False,
        ai=(
            "The source’s credits say the repository’s work was produced by Claude "
            "(Anthropic) under human direction, and the commit that publishes the "
            "certificate names Claude Opus 5.5 as co-author and says Evan Daniel approved "
            "it."
        ),
        lineage_at={
            227: (
                "The source names Francisco Couzo’s #672 packing (T-227), the refinement of "
                "Joost de Winter’s #668 packing (T-196) that #672 reports, as the one it "
                "regularizes and calls "
                "the certificate not a new bound: Evan Daniel solved that packing to its "
                "exact side, $1.76 \\times 10^{-11}$ below #672’s certificate, and "
                "regularized it for display at that side. Measured by the import and again "
                "by the 21 October review, nearest centres pair the two one to one under a "
                "half turn; 194 of the 227 squares lie within $10^{-6}$ of T-227’s, 16 move "
                "beyond $10^{-3}$ and 3 beyond a tenth, at most 0.168, and one square turns "
                "by 2.54° (T-225). #672’s packing moves no square beyond a tenth from de "
                "Winter’s (T-227)."
            ),
            204: (
                "The source names Francisco Couzo’s #678 packing (T-223) as the one it "
                "regularizes and calls the certificate not a new bound: Evan Daniel solved "
                "that packing to its exact side, $1.39 \\times 10^{-9}$ below #678’s "
                "certificate, and regularized it for display at that side. Measured by the "
                "import and again by the 21 October review, nearest centres pair the two "
                "one to one under a half turn; 132 of the 204 squares lie within $10^{-6}$ "
                "of T-223’s, 58 move beyond $10^{-3}$ and 4 beyond a tenth, at most 0.442, "
                "and three squares T-223 tilts by up to 0.088° are axis-aligned here (T-225)."
            ),
            229: (
                "The source names Evan Daniel’s own #674 packing (T-199) as the one it "
                "regularizes, polished to its exact side, $1.91 \\times 10^{-11}$ below "
                "#674’s certificate, and calls the certificate not a new bound. Measured "
                "by the import and again by the 21 October review, under no symmetry of "
                "the box do nearest centres pair the two one to one; an optimal assignment "
                "keeps 95 of "
                "the 229 squares within $10^{-6}$ of T-199’s, moves 112 beyond $10^{-3}$ "
                "and 13 beyond a tenth, at most 0.650, and turns six near-axis squares to "
                "the axis (T-225). Francisco Couzo’s #672 packing (T-227), which #674 names "
                "as its start, pairs with T-199 under no symmetry either: an optimal "
                "assignment moves 79 squares beyond a tenth, at most 0.873, with turns up to "
                "38° (T-227)."
            ),
            260: (
                "The source names Francisco Couzo’s #678 packing (T-223) as the one it "
                "regularizes and calls the certificate not a new bound: Evan Daniel solved "
                "that packing to its exact side, $2.51 \\times 10^{-11}$ below #678’s "
                "certificate, and regularized it for display at that side. Measured by the "
                "import and again by the 21 October review, 207 of the 260 squares lie "
                "within $10^{-9}$ of T-223’s and none turns; under no symmetry of the box "
                "do nearest centres pair the two one to one, and an optimal assignment "
                "slides 41 squares beyond $10^{-3}$ and 20 beyond a tenth, at most 0.643 "
                "(T-225)."
            ),
        },
        third_route=(
            ", and the 21 October review’s clean-room checker decided it again on two "
            "routes of its own, in integers alone and in rationals with exact intersection "
            "area on the pairs whose boxes overlap; its sharp controls at $10^{-30}$ found "
            "both maintained routes exact at the far wall, the near wall and the least-gap "
            "pair"
        ),
    ),
    "T-229": Prose(
        author="Mykhailo Polkovskyi",
        reported="on [jlevy/squares#719](https://github.com/jlevy/squares/issues/719)",
        producer_route=True,
        ai=(
            "The issue says Gemini assisted with solver scripting, precision checks and "
            "formatting."
        ),
        routes=(
            "One maintained route, `sqpack`’s exact verifier, is this repository’s "
            "`sqpack/verify.py`, which the issue names as one of its two checkers, so the "
            "replay shares the producer’s components; as the issue writes its command, that "
            "file reads no certificate, so the issue’s statement is no evidence of a check. "
            "The review’s checker shares no code with either maintained route or the source."
        ),
        lineage_at={
            105: (
                "The issue names the house it improves and no parent packing. Measured by the "
                "import and again by the 22 October review under the box’s symmetries, the "
                "nearest centres pair it one to one under the identity with T-174’s packing, "
                "the house best packing here before this adoption: 63 of the 105 squares lie "
                "within $10^{-6}$ of T-174’s, 42 move beyond $10^{-3}$ and none beyond a "
                "tenth, at most 0.049, and squares turn by up to 2.41°. It is T-174’s packing "
                "re-solved to a smaller side, a refinement that is not padding (T-229)."
            ),
            204: (
                "The author’s comment of 23 October on the issue says his continuous SQP "
                "optimization started from Francisco Couzo’s #678 certificate (T-223), in "
                "Couzo’s own frame, and not from Evan Daniel’s regularized view of it "
                "(T-225). Measured by the import and again by the 22 October review, the "
                "nearest centres pair it one to one with #678’s packing under the identity, "
                "keeping that certificate’s frame and tilt pattern: 60 squares move beyond "
                "$10^{-3}$ of T-223’s and 7 beyond a tenth, at most 0.237. It pairs with "
                "T-225’s packing, the house best packing here before this adoption, only under "
                "a half turn. Every square turns by less than 1° but square 38, which T-223 "
                "and T-225 hold by four neighbours and which this packing releases and turns "
                "by 25.64°, so that nothing lies within $1.25 \\times 10^{-2}$ of it (T-229): "
                "a release the author says his relaxation made."
            ),
        },
        third_route=(
            ", and the 22 October review’s clean-room checker decided it again on two routes "
            "of its own, in integers alone and in rationals with exact clipping area on every "
            "pair, from the source’s certificate and from the packet’s derived fact; its sharp "
            "controls at $10^{-30}$ found both maintained routes exact at the far wall, the "
            "near wall and the least-gap pair"
        ),
    ),
    "T-230": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#728](https://github.com/jlevy/squares/issues/728)",
        producer_route=False,
        ai=(
            "The source’s credits say its work was done with Claude (Anthropic) under human "
            "direction, and the commit that publishes the certificate names Claude Opus 5.5 "
            "as co-author and says Evan Daniel approved the record claim."
        ),
        routes=(
            "No route here is the source’s code, but both read the certificate through an "
            "adapter whose author read the source’s two checkers and which carries two of "
            "their expressions transcribed, its line filter and its corner construction (RF-1 "
            "of the 22 October review), so the replay shares those components with the "
            "producer. The review’s checker shares no code with either maintained route or the "
            "source, and the independent re-implementation rests on it."
        ),
        lineage=(
            "The author’s basin explorer started from Daniil Ostashev’s n = 303 packing of "
            "#562, the packing this case’s house best packing certified before this adoption "
            "(T-186), and near-record sweeps, crossovers and a final band flip, which reflects "
            "one of the packing’s two tilted bands along its wall, reached this packing; the "
            "issue calls it a new packing, not a refinement of Ostashev’s. Measured by the 22 "
            "October review, square by square, no symmetry of the box pairs nearest centres "
            "one to one with T-186’s packing, and the best assignment, the identity, moves 64 "
            "squares beyond a tenth, at most 0.910, keeps 180 within $10^{-3}$ and reverses 24 "
            "tilts. So it is another arrangement of Ostashev’s two-band design with one band’s "
            "tilt reversed, not a refinement in this record’s sense, found from Ostashev’s "
            "packing by the source’s account (T-230). The source leaves local optimality "
            "unresolved: it finds the packing not first-order jammed and predicts a further "
            "descent of about $5 \\times 10^{-7}$."
        ),
        third_route=(
            ", and the 22 October review’s clean-room checker decided it again on two routes "
            "of its own, in integers alone and in rationals with the exact clipped area of "
            "every pair; its sharp controls at $10^{-30}$ found both maintained routes exact "
            "at a wall and at the least-gap pair"
        ),
    ),
    "T-231": Prose(
        author="Mykhailo Polkovskyi",
        reported=(
            "on [jlevy/squares#719](https://github.com/jlevy/squares/issues/719), the "
            "release’s second 204 file, which he claimed after T-229 was registered"
        ),
        producer_route=True,
        ai=(
            "The issue says Gemini assisted with solver scripting, precision checks and "
            "formatting."
        ),
        routes=(
            "One maintained route, `sqpack`’s exact verifier, is this repository’s "
            "`sqpack/verify.py`, which the author says he imported as a module in his batch "
            "harness, so the replay shares the producer’s components. The review’s checker "
            "shares no code with either maintained route or the source."
        ),
        lineage=(
            "The release published it in the same commit as T-229’s certificate, and the "
            "author’s comment of 23 October says his continuous SQP optimization at 204 "
            "started from Francisco Couzo’s #678 certificate (T-223), in Couzo’s own frame. "
            "Measured by the 23 October review, it is T-229’s packing at its solved side: "
            "nearest centres pair the two one to one under the identity, no square moving "
            "beyond $2.02 \\times 10^{-11}$, and T-229’s certificate is this one dilated by "
            "$1 + 10^{-12}$. Its side and the rows that Evan Daniel’s exact solver "
            "determines equal that solver’s output for T-229’s arrangement, row for row, a "
            "method the source does not name (T-231). The packing is not rigid: its 21 free "
            "squares keep clearances of $5.774 \\times 10^{-9}$ to $1.25 \\times 10^{-2}$."
        ),
        third_route=(
            ", and the 23 October review’s clean-room checker decided it again on two routes "
            "of its own, in integers alone and in rationals with exact clipping area and "
            "Euclidean distance on every pair; its sharp controls at $10^{-30}$ found both "
            "maintained routes exact at every wall and at three kinds of least-gap pair"
        ),
    ),
}

XU = "Ryan Xu"
SQUISH = "Nate Chaoweeraprasit (itsnaka)"
COUZO = "Francisco Couzo"
DANIEL = "Evan Daniel"
DE_WINTER = "Joost de Winter"
PINGYOU = "PingYou Ltd"
OSTASHEV = "Daniil Ostashev"
BARNETT = "Robert Barnett"
#: Mykhailo Polkovskyi, by the handle his earlier credits use (T-173, T-183).
POLKOVSKYI = "Mishapolk"


@dataclass(frozen=True)
class Credit:
    """Who found the packing a count's house holds, who improved it, and how to say so."""

    found_by: tuple[str, ...]
    improved_by: tuple[str, ...]
    phrase: str
    #: The year the packing was found, where its house's certificate is of a later year:
    #: a tighter certificate of an earlier finder's packing leaves the packing with its
    #: finder and its year (review A's A7 of #661). Unset, the house's own year.
    found_year: int | None = None
    #: Whether the house is the replaced reported lane's own packing, measured pose for
    #: pose with no square turned (the result's `regularizations`), so the lane keeps
    #: what the record knew of that packing, `PACKING_FACTS` (review C6 of #661).
    same_packing: bool = False


#: What a reported lane says of its packing rather than of its certificate, carried to a
#: house that is the same packing (`Credit.same_packing`), and otherwise not known.
PACKING_FACTS = ("analytically_optimized", "construction_method", "tilt_angles_deg")


def _couzo(start: str) -> Credit:
    finder = XU if start == "Xu" else SQUISH
    whose = "Ryan Xu’s" if start == "Xu" else "Nate Chaoweeraprasit’s SQUISH"
    return Credit((finder,), (COUZO,), f"Francisco Couzo’s refinement of {whose} packing")


def _regularized(
    finder: str, whose: str, *, via: str | None = None, how: str | None = None
) -> Credit:
    """Evan Daniel's regularization of `finder`'s packing, as `via` refined it, or as `how`
    says where the source says less (review A4 of #718). The clause carries no comma of its
    own, so each sentence that quotes the credit punctuates it (review A5)."""
    improved = (via, DANIEL) if via else (DANIEL,)
    refined = how if how is not None else (f" as {via} refined it" if via else "")
    return Credit(
        (finder,),
        improved,
        f"Evan Daniel’s display regularization of {whose} packing{refined}",
    )


#: The credit of each adopted count, from the register's credit lines and the adoption
#: tables of the reviews that recommended each house; a regularization leaves the packing
#: with its finder (`T-146`'s `regularizations`).
CREDITS: dict[int, Credit] = {
    # PingYou Ltd's tighter certificate of the packing the Kingbird catalogue credits to
    # Thomas Schadt, improved by David Ellsworth (T-195's regularization of T-009); padding
    # only, as the source says. The packing is of 2025, as n-029.md's reported lane and the
    # release asset's credits say; the certificate is of 2026.
    29: Credit(
        ("Thomas Schadt",),
        ("David Ellsworth", PINGYOU),
        "PingYou Ltd’s tighter certificate of Thomas Schadt’s packing, as David Ellsworth "
        "improved it",
        found_year=2025,
        same_packing=True,
    ),
    # T-174's regularization of T-118's packing, 22 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    68: Credit(
        (COUZO,),
        ("Seth Rehwaldt", PINGYOU),
        "PingYou Ltd’s refinement of Seth Rehwaldt’s refinement of Francisco Couzo’s packing",
    ),
    70: _regularized(XU, "Ryan Xu’s"),
    # T-174's regularization of T-130's packing, 45 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    84: Credit(
        (XU,),
        (COUZO, PINGYOU),
        "PingYou Ltd’s refinement of Francisco Couzo’s refinement of Ryan Xu’s packing",
    ),
    # T-174's regularization of T-130's packing, 64 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    86: Credit(
        (XU,),
        (COUZO, PINGYOU),
        "PingYou Ltd’s refinement of Francisco Couzo’s refinement of Ryan Xu’s packing",
    ),
    102: _regularized(XU, "Ryan Xu’s"),
    # T-174's regularization of T-146's view, measured one to one, no square moved beyond
    # 1e-12 (the 14 October review of PR 574).
    103: Credit(
        (XU,),
        (POLKOVSKYI, DANIEL, PINGYOU),
        "PingYou Ltd’s tighter certificate of Evan Daniel’s display regularization of Ryan "
        "Xu’s packing as Mykhailo Polkovskyi refined it",
    ),
    # Mykhailo Polkovskyi's re-solve (T-229, adopted on 23 October 2026) of T-174's packing,
    # T-174's regularization of T-130's packing as T-170 padded it: one to one with T-174's,
    # 42 squares moved beyond 1e-3 and none beyond a tenth (the import's measurement and the
    # 22 October review's), so the packing stays with Xu and Polkovskyi joins the refiners.
    105: Credit(
        (XU,),
        (COUZO, PINGYOU, POLKOVSKYI),
        "Mykhailo Polkovskyi’s re-solve of PingYou Ltd’s tighter certificate of Francisco "
        "Couzo’s refinement of Ryan Xu’s packing",
    ),
    # T-174's regularization of T-128's packing, 13 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    108: Credit(
        (XU,),
        (COUZO, PINGYOU),
        "PingYou Ltd’s refinement of Francisco Couzo’s refinement of Ryan Xu’s packing",
    ),
    # T-174's regularization of T-098's packing, 5 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    110: Credit(
        (COUZO,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s refinement of Evan Daniel’s exact optimum of Francisco Couzo’s packing",
    ),
    123: _regularized(XU, "Ryan Xu’s"),
    126: Credit(
        (XU,),
        (DANIEL,),
        "Evan Daniel’s reconstruction and exact certificate of Ryan Xu’s arrangement",
    ),
    # T-174's regularization of T-128's packing, 53 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    127: Credit(
        (XU,),
        (COUZO, PINGYOU),
        "PingYou Ltd’s refinement of Francisco Couzo’s refinement of Ryan Xu’s packing",
    ),
    # Mykhailo Polkovskyi's KKT refinement of PR 574's re-solve of issue 562's packing
    # (T-186's regularization of T-174), no square moved beyond 1e-3.
    129: Credit(
        (OSTASHEV,),
        (PINGYOU, POLKOVSKYI),
        "Mykhailo Polkovskyi’s refinement of Daniil Ostashev’s n = 129 packing, as PingYou "
        "Ltd refined it",
    ),
    # T-174's regularization of T-127's packing, 15 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    130: Credit(
        (SQUISH,),
        ("Siddharth Gupta", PINGYOU),
        "PingYou Ltd’s refinement of Siddharth Gupta’s refinement of Nate Chaoweeraprasit’s "
        "SQUISH packing",
    ),
    # T-174's regularization of T-136's packing, measured one to one, no square moved
    # beyond 1e-12 (the 14 October review of PR 574).
    131: Credit(
        (SQUISH,),
        (PINGYOU,),
        "PingYou Ltd’s tighter certificate of Nate Chaoweeraprasit’s SQUISH packing",
    ),
    # T-174's regularization of T-141's packing, 18 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    132: Credit(
        (DANIEL,),
        (PINGYOU,),
        "PingYou Ltd’s refinement of Evan Daniel’s record-hunt packing",
    ),
    # Evan Daniel's chain search from Ryan Xu's packing: nine squares beyond a tenth
    # against Xu's and Barnett's (RT-5 of the 16 October review; T-187 records no
    # regularization). Issue 673 corrects the source's credit: the start was named as
    # "based on", and the finder of the packing posted is Daniel (19 October 2026).
    146: Credit(
        (DANIEL,),
        (),
        "Evan Daniel’s packing from a chain search started from Ryan Xu’s n = 146 packing",
    ),
    # PingYou Ltd's design rearranged by Mykhailo Polkovskyi, as the 14 October review
    # measured it (RQ-5); whether it is a new arrangement is the owner's decision 1 on
    # pull request 602 (T-173).
    153: Credit(
        (PINGYOU,),
        ("Mishapolk",),
        "Mykhailo Polkovskyi’s arrangement of PingYou Ltd’s n = 153 design, after Ryan "
        "Xu’s n = 70 packing and Evan Daniel’s exact certificate of it",
    ),
    # Evan Daniel's continuation of issue 586's arrangement, three squares beyond a tenth
    # (the 20 October review), which Couzo continued from Daniel's issue-552 packing; issue
    # 694 credits #586's arrangement and Ostashev's n = 156 packing as its starts, and only
    # the first is near it by pose, so Ostashev is named as the source's account of the
    # search. T-186's re-solve of T-182, the earlier house, is not its start.
    154: Credit(
        (DANIEL,),
        (COUZO,),
        "Evan Daniel’s continuation of Francisco Couzo’s further arrangement of Daniel’s "
        "n = 154 packing in a search the source started from Daniil Ostashev’s n = 156 "
        "packing",
    ),
    # T-174's regularization of T-149's packing, 3 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    # Evan Daniel's basin explorer from Ostashev's packing to a different local minimum;
    # the issue credits Ostashev's packing as the start, which the author's issue 673
    # reads as "based on", not as the finder of the packing posted.
    155: Credit(
        (DANIEL,),
        (),
        "Evan Daniel’s packing from a search started from Daniil Ostashev’s packing",
    ),
    # PR 574's padding of issue 561's continuation of Ostashev's packing, padded again
    # (T-186's regularization of T-174; RT-4).
    156: Credit(
        (OSTASHEV,),
        (COUZO, PINGYOU, POLKOVSKYI),
        "Mykhailo Polkovskyi’s tighter certificate of Francisco Couzo’s continuation of "
        "Daniil Ostashev’s n = 156 packing, after PingYou Ltd’s",
    ),
    # T-174's regularization of T-098's packing, 69 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    172: Credit(
        (COUZO,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s refinement of Evan Daniel’s exact optimum of Francisco Couzo’s packing",
    ),
    # PR 574's padding of issue 528's composition, padded again (T-186's regularization of
    # T-174).
    175: Credit(
        (OSTASHEV,),
        (PINGYOU, POLKOVSKYI),
        "Mykhailo Polkovskyi’s tighter certificate, after PingYou Ltd’s, of Daniil "
        "Ostashev’s composition of two of his 38-square rectangles with David Ellsworth’s "
        "n = 171 template, in place of its pieces of Thomas Schadt’s n = 50 packing",
    ),
    # Ostashev's issue-575 packing re-solved, through PR 574's (T-186's regularization of
    # T-174; RP-4 of the PR 574 review).
    176: Credit(
        (OSTASHEV,),
        (PINGYOU, POLKOVSKYI),
        "Mykhailo Polkovskyi’s exact re-solve of Daniil Ostashev’s issue-575 n = 176 "
        "packing, after PingYou Ltd’s",
    ),
    # T-174's regularization of T-127's packing, 42 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    179: Credit(
        (SQUISH,),
        ("Siddharth Gupta", PINGYOU),
        "PingYou Ltd’s refinement of Siddharth Gupta’s refinement of Nate Chaoweeraprasit’s "
        "SQUISH packing",
    ),
    # T-174's regularization of T-128's packing, 25 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    180: Credit(
        (SQUISH,),
        ("Siddharth Gupta", COUZO, PINGYOU),
        "PingYou Ltd’s refinement of Francisco Couzo’s refinement of Nate Chaoweeraprasit’s "
        "SQUISH packing, after Siddharth Gupta’s",
    ),
    # T-174's regularization of T-151's packing re-solved, measured one to one, no square
    # moved beyond 1.5e-4 (the 14 October review of PR 574).
    181: Credit(
        (SQUISH,),
        (PINGYOU,),
        "PingYou Ltd’s exact re-solve of Nate Chaoweeraprasit’s SQUISH packing composed "
        "from two of SQUISH’s own n = 154 packings",
    ),
    # T-174's regularization of T-098's packing, 27 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    182: Credit(
        (COUZO,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s refinement of Evan Daniel’s exact optimum of Francisco Couzo’s packing",
    ),
    # Evan Daniel's packing from his basin explorer, which started from Francisco Couzo's
    # n = 182 packing as this register's witness held it; the crossover mates were not
    # logged (issue 680, T-220). The register's seed is acknowledged in the bibliography's
    # credit only, as no packing of the project's is in the lineage.
    183: Credit(
        (DANIEL,),
        (),
        "Evan Daniel’s basin-explorer packing after Francisco Couzo’s n = 182 packing",
    ),
    # Mykhailo Polkovskyi's re-solve (T-229, adopted on 23 October 2026) of Francisco
    # Couzo's packing, which Couzo first reported in issue 670 and refined in 675 and 678
    # (T-226, T-228, T-223): one to one with #678's under the identity and with T-225's under
    # a half turn, one square released and turned by 25.64 degrees (the import's measurement
    # and the 22 October review's, its RF-3 and RF-4). The author's comment of 23 October on
    # issue 719 says the solve started from Couzo's #678 certificate, not from Evan Daniel's
    # view (T-225), so T-229's item names T-223 and Daniel is no antecedent here (think-xyhn).
    # The packing stays with Couzo, whose source's manifest credits Polkovskyi's own
    # construction as its seed (A11 of #716). The pass of 24 October 2026 adopted the
    # release's other 204 file (T-231), T-229's packing at its solved side, which T-231's
    # item names, so the credit is the same; Evan Daniel's exact solver, measured as its
    # method by the 23 October review, is a method credit and no antecedent of the packing.
    204: Credit(
        (COUZO,),
        (POLKOVSKYI,),
        "Mykhailo Polkovskyi’s re-solve of Francisco Couzo’s packing from a search Couzo’s "
        "source seeded with Polkovskyi’s own n = 204 construction",
    ),
    # T-174's regularization of T-098's packing, measured one to one, no square moved
    # beyond 1e-12 (the 14 October review of PR 574).
    206: Credit(
        (COUZO,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s tighter certificate of Evan Daniel’s exact optimum of Francisco "
        "Couzo’s packing",
    ),
    # By pose an exact re-solve of PingYou Ltd's packing (RQ-5 of the 14 October review).
    207: Credit(
        (PINGYOU,),
        ("Mishapolk",),
        "Mykhailo Polkovskyi’s exact re-solve of PingYou Ltd’s assembly of two placed "
        "patches of Ryan Xu’s n = 70 packing, from Evan Daniel’s exact certificate of it",
    ),
    # T-174's regularization of T-127's packing, 20 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    208: Credit(
        (SQUISH,),
        ("Siddharth Gupta", PINGYOU),
        "PingYou Ltd’s refinement of Siddharth Gupta’s refinement of Nate Chaoweeraprasit’s "
        "SQUISH packing",
    ),
    # T-174's regularization of T-140's packing, 23 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    209: Credit(
        (SQUISH,),
        (COUZO, PINGYOU),
        "PingYou Ltd’s refinement of Francisco Couzo’s refinement of Nate Chaoweeraprasit’s "
        "SQUISH packing",
    ),
    # T-174's regularization of T-098's packing, 33 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    210: Credit(
        (COUZO,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s refinement of Evan Daniel’s exact optimum of Francisco Couzo’s packing",
    ),
    # Couzo's further arrangement of Ostashev's issue-575 design, five squares beyond a
    # tenth against T-182 and T-175 (RT-1 of the 16 October review; T-188 records no
    # regularization).
    211: Credit(
        (OSTASHEV,),
        (COUZO,),
        "Francisco Couzo’s further arrangement of Daniil Ostashev’s n = 211 design",
    ),
    # Evan Daniel's display regularization (T-225, adopted on 22 October 2026) of Francisco
    # Couzo's issue-672 packing (T-227), solved to its exact side 1.76e-11 below #672's
    # certificate: T-225's item names T-227, whose own item names de Winter's T-196, which
    # #672 refines (no square beyond a tenth). So the packing stays with de Winter, Couzo is
    # credited with the refinement and Daniel with the regularization, as at 258. The house
    # it replaced was de Winter's packing of issue 668 (T-196), from a search the issue says
    # started from this repository's catalogue.
    # #672 reports the refinement; the source's manifest credits it to Couzo, retaining de
    # Winter's seed credit, and the CT105 web submission it names as provenance names no
    # submitter (RF-3 of the 22 October review of T-226 to T-228); the #672 reply asks who
    # made it (review A4 of #718).
    227: _regularized(
        DE_WINTER,
        "Joost de Winter’s",
        via=COUZO,
        how=" as refined in Francisco Couzo’s #672 report",
    ),
    # T-174's regularization of T-128's packing, 46 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    228: Credit(
        (COUZO,),
        (PINGYOU,),
        "PingYou Ltd’s refinement of Francisco Couzo’s refinement of his own packing",
    ),
    # Evan Daniel's display regularization (T-225, adopted on 22 October 2026) of his own
    # issue-674 packing (T-199), polished to its exact side 1.91e-11 below #674's
    # certificate: T-225's item names T-199, whose finder he is. #674's packing is his
    # dilation of a nearby configuration of his opening packing (T-198); the issue credits
    # Couzo's issue-672 packing, after de Winter's issue 668, as the start, which the
    # author's issue 673 reads as "based on".
    229: Credit(
        (DANIEL,),
        (),
        "Evan Daniel’s display regularization of his own packing from a search started from "
        "Francisco Couzo’s refinement of Joost de Winter’s packing",
    ),
    # PR 574's re-solve of issue 528's composition, re-solved again (T-186's
    # regularization of T-174).
    232: Credit(
        (OSTASHEV,),
        (PINGYOU, POLKOVSKYI),
        "Mykhailo Polkovskyi’s refinement, after PingYou Ltd’s, of Daniil Ostashev’s "
        "composition of his 38-square rectangle with a 76-square piece of Erich Friedman’s "
        "n = 85 packing",
    ),
    # Evan Daniel's basin explorer from a rebuild of issue 481's composition to a different
    # local minimum; the issue credits the composition for the construction, which the
    # author's issue 673 reads as "based on", not as the finder of the packing posted.
    236: Credit(
        (DANIEL,),
        (),
        "Evan Daniel’s packing from a rebuild of Nate Chaoweeraprasit’s SQUISH composition",
    ),
    # Couzo's refinement of issue 593's arrangement of his issue-561 design (T-190's
    # regularization of T-183).
    237: Credit(
        (SQUISH,),
        (COUZO, POLKOVSKYI),
        "Francisco Couzo’s refinement of Mykhailo Polkovskyi’s arrangement of Couzo’s "
        "design, after Nate Chaoweeraprasit’s SQUISH packing",
    ),
    # T-174's regularization of T-151's packing, measured one to one, no square moved
    # beyond 1e-12 (the 14 October review of PR 574).
    238: Credit(
        (SQUISH,),
        (PINGYOU,),
        "PingYou Ltd’s tighter certificate of Nate Chaoweeraprasit’s SQUISH packing "
        "composed from SQUISH’s own n = 305 and n = 154 packings",
    ),
    # T-174's regularization of T-151's packing re-solved, measured one to one, no square
    # moved beyond 1.5e-4 (the 14 October review of PR 574).
    239: Credit(
        (SQUISH,),
        (PINGYOU,),
        "PingYou Ltd’s exact re-solve of Nate Chaoweeraprasit’s SQUISH packing composed "
        "from SQUISH’s n = 209 packing as Siddharth Gupta refined it and its own n = 240 "
        "packing",
    ),
    # T-174's regularization of T-098's packing, 28 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    240: Credit(
        (COUZO,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s refinement of Evan Daniel’s exact optimum of Francisco Couzo’s packing",
    ),
    241: Credit(
        (OSTASHEV,),
        (COUZO,),
        "Francisco Couzo’s continuation of Daniil Ostashev’s n = 241 packing",
    ),
    258: _regularized(SQUISH, "Nate Chaoweeraprasit’s SQUISH", via="Mishapolk"),
    259: Credit((SQUISH,), (), "Nate Chaoweeraprasit’s SQUISH packing"),
    # Evan Daniel's display regularization (T-225, adopted on 22 October 2026) of issue
    # 678's packing (T-223), solved to its exact side 2.51e-11 below #678's certificate:
    # T-225's item names T-223, and the packing stays with Couzo. T-223 was adopted here on
    # 21 October 2026 from Joost de Winter's T-196: its source seeded its search with Evan
    # Daniel's exact-form certificate of de Winter's issue-668 packing (T-196), and the 20
    # October review measured 162 of its squares within 1e-4 of that seed's, 55 beyond
    # 1e-2, so de Winter is named in the sentence as the construction's author, as at 229,
    # and not in the structured fields.
    260: Credit(
        (COUZO,),
        (DANIEL,),
        "Evan Daniel’s display regularization of Francisco Couzo’s packing from a search "
        "seeded with Evan Daniel’s exact certificate of Joost de Winter’s n = 260 packing",
    ),
    # T-174's regularization of T-169's re-solve, measured one to one, no square moved
    # beyond 1e-12 (the 14 October review of PR 574).
    261: Credit(
        (XU,),
        (BARNETT, PINGYOU),
        "PingYou Ltd’s exact re-solve of Robert Barnett’s refinement of Ryan Xu’s packing",
    ),
    # T-174's regularization of T-146's view, measured one to one, no square moved beyond
    # 1e-12 (the 14 October review of PR 574).
    263: Credit(
        (SQUISH,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s tighter certificate of Evan Daniel’s display regularization of Nate "
        "Chaoweeraprasit’s SQUISH packing",
    ),
    # PR 574's padding of issue 528's composition, padded again (T-186's regularization of
    # T-174).
    264: Credit(
        (OSTASHEV,),
        (PINGYOU, POLKOVSKYI),
        "Mykhailo Polkovskyi’s tighter certificate, after PingYou Ltd’s, of Daniil "
        "Ostashev’s composition of his 38-square rectangle with a 93-square piece of Evan "
        "Daniel’s exact optimum of Joost de Winter’s n = 126 packing",
    ),
    267: _couzo("Xu"),
    # T-174's regularization of T-098's packing, 117 squares moved beyond 1e-3, one to
    # one; that it is that packing is the source's statement (the 14 October review of PR
    # 574).
    268: Credit(
        (COUZO,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s refinement of Evan Daniel’s exact optimum of Francisco Couzo’s packing",
    ),
    # T-174's regularization of T-146's view, measured one to one, no square moved beyond
    # 1e-12 (the 14 October review of PR 574).
    269: Credit(
        (SQUISH,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s tighter certificate of Evan Daniel’s display regularization of Nate "
        "Chaoweeraprasit’s SQUISH packing",
    ),
    # Issue 703's packing, another arrangement of the design of issue 500's packing, which
    # T-174 refines to 1e-30: 15 squares beyond a tenth under the identity (the 21 October
    # review), found from issue 500's packing, which the issue credits as the ultimate
    # start. As at 308, Daniel is the finder and the start's author is named in the
    # sentence, not in the structured fields.
    270: Credit(
        (DANIEL,),
        (),
        "Evan Daniel’s arrangement, in a search started from Nate Chaoweeraprasit’s SQUISH "
        "packing, of that packing’s design, composed from SQUISH’s issue 481 n = 209 "
        "packing, whole, and the Kingbird catalogue’s former n = 19 packing",
    ),
    # Evan Daniel's tilt-swap from the register's witness (T-186's tightening of issue 561's
    # packing): issue 561's arrangement continued, three squares beyond a tenth (RV-2 of the
    # 19 October review), which issue 664 first called a refinement of Couzo's packing of
    # SQUISH's. The author's comment of 20 October (issuecomment-6302892909) says he meant a
    # different local minimum and asks to be the finder, with both credited as the start,
    # the issue 673 reading, as at 146, 236 and 308.
    271: Credit(
        (DANIEL,),
        (),
        "Evan Daniel’s packing from a search started from Francisco Couzo’s arrangement "
        "of Nate Chaoweeraprasit’s SQUISH packing",
    ),
    # T-174's regularization of T-151's packing, as T-171 re-solved it, measured one to
    # one, no square moved beyond 1.5e-4 (the 14 October review of PR 574).
    272: Credit(
        (SQUISH,),
        (PINGYOU,),
        "PingYou Ltd’s exact re-solve of Nate Chaoweeraprasit’s SQUISH packing",
    ),
    # T-174's regularization of T-098's packing, 49 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    273: Credit(
        (COUZO,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s refinement of Evan Daniel’s exact optimum of Francisco Couzo’s packing",
    ),
    292: _regularized(SQUISH, "Nate Chaoweeraprasit’s SQUISH"),
    295: _regularized(XU, "Ryan Xu’s"),
    # T-174's regularization of T-098's packing, 119 squares moved beyond 1e-3, one to
    # one; that it is that packing is the source's statement (the 14 October review of PR
    # 574).
    297: Credit(
        (COUZO,),
        (DANIEL, PINGYOU),
        "PingYou Ltd’s refinement of Evan Daniel’s exact optimum of Francisco Couzo’s packing",
    ),
    # Issue 583's continuation of PingYou Ltd's arrangement, padded (T-186's
    # regularization of T-181; RT-4).
    302: Credit(
        (PINGYOU,),
        (COUZO, POLKOVSKYI),
        "Mykhailo Polkovskyi’s tighter certificate of Francisco Couzo’s continuation of "
        "PingYou Ltd’s n = 302 arrangement",
    ),
    # Issue 728's packing (T-230, adopted on 23 October 2026), another arrangement of Daniil
    # Ostashev's two-band design (64 squares beyond a tenth of T-186's packing and 24 tilts
    # reversed, the 22 October review), found from Ostashev's packing, which the issue names
    # as the start. As at 155, Daniel is the finder and the start's author is named in the
    # sentence, not in the structured fields.
    303: Credit(
        (DANIEL,),
        (),
        "Evan Daniel’s arrangement of Daniil Ostashev’s two-band design in a search started "
        "from Ostashev’s n = 303 packing",
    ),
    # Issue 575's packing padded (T-186's regularization of T-175).
    304: Credit(
        (OSTASHEV,),
        (POLKOVSKYI,),
        "Mykhailo Polkovskyi’s tighter certificate of Daniil Ostashev’s n = 304 packing",
    ),
    # T-174's regularization of T-152's packing, measured one to one, no square moved
    # beyond 1e-12 (the 14 October review of PR 574).
    305: Credit(
        (SQUISH,),
        (COUZO, PINGYOU),
        "PingYou Ltd’s tighter certificate of Francisco Couzo’s refinement of Nate "
        "Chaoweeraprasit’s SQUISH Mondrian packing",
    ),
    # T-174's regularization of T-128's packing, 34 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    306: Credit(
        (COUZO,),
        (PINGYOU,),
        "PingYou Ltd’s refinement of Francisco Couzo’s refinement of his own packing",
    ),
    # T-174's regularization of T-136's packing re-solved, measured one to one, no square
    # moved beyond 1.5e-4 (the 14 October review of PR 574).
    307: Credit(
        (SQUISH,),
        (PINGYOU,),
        "PingYou Ltd’s exact re-solve of Nate Chaoweeraprasit’s SQUISH packing",
    ),
    # T-174's regularization of T-141's packing, 25 squares moved beyond 1e-3, one to one;
    # that it is that packing is the source's statement (the 14 October review of PR 574).
    # Issue 689's packing, another arrangement of the two-wedge design (15 squares beyond a
    # tenth of #489's, the 20 October review), found from issue 481's n = 307 packing, which
    # the issue credits as the ultimate start. Fang is named in the sentence as the design's
    # author, as the earlier house's credit named him, and not in the structured fields,
    # which is the owner's open decision under think-a95t (RW-1 of that review).
    308: Credit(
        (DANIEL,),
        (),
        "Evan Daniel’s arrangement of Kevin Fang’s two-wedge design in a search started from "
        "Nate Chaoweeraprasit’s n = 307 packing",
    ),
}


class AdoptionError(ValueError):
    """The record cannot be moved as asked: a count, a source or a reader is missing."""


# ------------------------------------------------------------------------- reading


def _split(text: str) -> tuple[str, str, str]:
    """The record's opening fence, its front matter and the rest from the closing fence."""
    if not text.startswith("---\n"):
        raise AdoptionError("case record has no front matter")
    end = text.index("\n---\n", 4)
    return "---\n", text[4 : end + 1], text[end + 1 :]


def _packing(front: str) -> dict[str, Any]:
    return dict(safe_load(front)["packing"])


def _block_span(front: str, key: str) -> tuple[int, int]:
    """Where `packing.<key>` sits in the front matter, from its line to the next key's."""
    match = re.search(rf"^  {key}:", front, re.MULTILINE)
    if match is None:
        raise AdoptionError(f"front matter has no packing.{key}")
    following = re.search(r"^(  [a-z_]+:|[a-z_]+:)", front[match.end() :], re.MULTILINE)
    return match.start(), match.end() + following.start() if following else len(front)


def _dump(key: str, value: Any) -> str:
    text = yaml.safe_dump(
        {"packing": {key: value}}, sort_keys=False, allow_unicode=True, width=WIDTH
    )
    return text.split("\n", 1)[1]


def _replace(front: str, key: str, value: Any) -> str:
    start, end = _block_span(front, key)
    return front[:start] + _dump(key, value) + front[end:]


def _append(front: str, key: str, items: Sequence[Any]) -> str:
    """Append list items to `packing.<key>`, leaving the existing items' text alone."""
    if not items:
        return front
    start, end = _block_span(front, key)
    block = front[start:end]
    if block.rstrip().endswith("[]"):
        return front[:start] + _dump(key, list(items)) + front[end:]
    added = _dump(key, list(items)).split("\n", 1)[1]
    if not block.endswith("\n"):
        raise AdoptionError(f"packing.{key} does not end a line")
    return front[:end] + added + front[end:]


@cache
def _register() -> tuple[Mapping[str, Any], ...]:
    return tuple(select_houses.load_results())


def display(side: exact_sides.Side) -> str:
    """A side as prose shows it: exact where it ends within sixteen places, else rounded up;
    an algebraic side never ends, and is rounded up."""
    if isinstance(side, exact_sides.Algebraic):
        return select_houses.ceiling(side)
    for places in range(PLACES + 1):
        if (side * 10**places).denominator == 1:
            return select_houses.ceiling(side, places) if places else str(side.numerator)
    return select_houses.ceiling(side)


def _bibliography() -> Mapping[str, Mapping[str, Any]]:
    return _keyed(BIBLIOGRAPHY.read_text(encoding="utf-8"), "key")


def _covering(key: str, n: int) -> Mapping[str, Any]:
    """`coverage_source` in the register on disk, parsed and looked up once for each text."""
    return _covered(COVERAGE.read_text(encoding="utf-8"), key, n)


@cache
def _covered(text: str, key: str, n: int) -> Mapping[str, Any]:
    return coverage_source(_listed(text), key, n)


def coverage_source(
    sources: Sequence[Mapping[str, Any]], key: str, n: int
) -> Mapping[str, Any]:
    """The coverage register's entry for the source key `key` whose scope holds `n`.

    A source key can have more than one entry. Francisco Couzo's release of 11 October
    has two: its beyond-horizon rows read a claims record that holds only the claims
    beyond the corpus, and `check_source_coverage` holds a selected override of a source
    with a claims record to that record's print, so its in-corpus counts are an entry of
    their own. A key with one entry is that entry, as the register is keyed elsewhere.
    """
    found = [source for source in sources if str(source["source_key"]) == key]
    if len(found) > 1:
        found = [
            source for source in found if n in select_houses.scope_values(dict(source["scope"]))
        ]
    if len(found) != 1:
        raise AdoptionError(f"n={n}: {len(found)} coverage entries of {key} hold this count")
    return found[0]


@cache
def _listed(text: str) -> tuple[Mapping[str, Any], ...]:
    """A register's `sources` in order, parsed once for each text the file has held."""
    return tuple(safe_load(text)["sources"])


@cache
def _keyed(text: str, key: str) -> Mapping[str, Mapping[str, Any]]:
    """A register's `sources` by `key`, parsed once for each text the file has held."""
    return {str(source[key]): source for source in _listed(text)}


# ------------------------------------------------------------------------- the move


@dataclass(frozen=True)
class Move:
    """One count's adoption: the selection, the house and the record as it stood before."""

    selection: select_houses.Selection
    house: select_houses.Candidate
    packing: Mapping[str, Any]
    #: The case record's complete text before the move, which `rewrite` rewrites.
    text: str

    @property
    def n(self) -> int:
        return self.selection.n

    @property
    def side(self) -> Fraction:
        """The house's exact side, which this writer states: a fraction (`rational`)."""
        return rational(self.house.side)


def rational(side: exact_sides.Side) -> Fraction:
    """A side this writer states. It writes rational houses only, and `plan` refuses an
    algebraic one; a certificate the prose quotes beside a house is rational wherever the
    rule of 15 October wrote it, which left every algebraic certificate out."""
    if isinstance(side, exact_sides.Algebraic):
        raise AdoptionError(
            f"the writer states rational sides, not {exact_sides.literal(side)}"
        )
    return side


@cache
def _claims(path: Path) -> Mapping[int, str]:
    """A source's claims reparsed from its retained record, once a run: the records are
    retained evidence, which an adoption reads and never writes."""
    from devtools.check_source_coverage import load_claims  # noqa: PLC0415

    return load_claims(path)


#: The most places a house's side is printed at to stay below the house it replaces: 40
#: until 17 October 2026, when T-174's 68 came in 4.58e-61 below Seth Rehwaldt's exact
#: 59-place print (T-118), which 40 places tie.
MAX_PLACES = 72


def shown(side: Fraction, above: object = None) -> str:
    """A house's side rounded up at sixteen places, or at the fewest more that print it
    strictly below `above`, the reported value of the house it replaces, where sixteen
    would tie the two: PingYou Ltd's n = 105 re-solve (T-170) is 1.08e-19 below Francisco
    Couzo's certificate (T-130), and both round up to 10.7893037837481589."""
    printed = select_houses.ceiling(side)
    if above is None:
        return printed
    bar = Fraction(Decimal(str(above)))
    places = PLACES
    while side < bar and Fraction(Decimal(printed)) >= bar and places < MAX_PLACES:
        places += 1
        printed = select_houses.ceiling(side, places)
    return printed


def printed_at(value: object, side: Fraction) -> bool:
    """Whether `value` prints `side`: the side itself, or rounded up at its own places, at
    sixteen or more (`shown`)."""
    text = str(value)
    if Fraction(Decimal(text)) == side:
        return True
    places = len(text.partition(".")[2])
    return places >= PLACES and text == select_houses.ceiling(side, places)


def _above(move: Move) -> object:
    """The reported value of the house the move replaces, where the record states one."""
    return (move.packing.get("reported_upper_bound") or {}).get("value")


def _value(candidate: select_houses.Candidate, above: object = None) -> str:
    """The reported value: the source's print where its coverage claims record holds one.

    `check_source_coverage` holds a selected source that declares a claims record to the
    side that record prints; every other house is reported at its exact side as `shown`
    prints it against `above`, the house it replaces, as the verified lane writes it.
    """
    source = _covering(candidate.source_key, candidate.n)
    if source.get("claims_record"):
        printed = _claims(ROOT / str(source["claims_record"])).get(candidate.n)
        if printed is None or Fraction(Decimal(printed)) != candidate.side:
            raise AdoptionError(
                f"n={candidate.n}: {source['id']}'s claims record does not print the exact side"
            )
        return printed
    return shown(rational(candidate.side), above)


def words(iso: str) -> str:
    """An ISO date as prose writes it: ``2026-10-12`` is ``12 October 2026``."""
    day = date.fromisoformat(iso)
    return f"{day.day} {day:%B %Y}"


def day_words(n: int) -> str:
    """The day the count's house was adopted, as prose writes it: ``12 October 2026``."""
    return words(houses.adopted_on(n))


def _sci(value: Fraction) -> str:
    return f"{float(value):.2e}"


def _join(names: Sequence[str]) -> str:
    names = list(names)
    if len(names) <= 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def _results_holding(evidence: Sequence[str], n: int) -> list[str]:
    """The register entries whose evidence the case's bound cites, at `n`."""
    wanted = set(evidence)
    found = []
    for entry in _register():
        scope = select_houses.scope_values(dict(entry["scope"]))
        if n in scope and wanted & set(entry.get("evidence") or ()):
            found.append(str(entry["id"]))
    return found


#: Credited handles prose writes as the person's name, as the register's prose does.
PROSE_NAMES = {"ry-xu": "Ryan Xu"}
#: The credited name for a handle a record written before 14 October 2026 carries in a
#: name field, so a note built from an earlier house names the person (epistemics.md,
#: People and projects, never tools).
RECORD_NAMES = {"ry-xu": XU}
#: The ry-xu section's heading and lead as records written before 14 October 2026 carry
#: them (`register_ryxu_reports.FORMER_SECTION`), and as the record names its finder now.
FORMER_PROSE = (
    (re.compile(r"\n## The ry-xu construction\n"), "\n## The Xu construction\n"),
    (re.compile(r"\nry-xu reports \((T-\d{3})\)"), r"\nRyan Xu reports (\1)"),
)


#: A name field's item that gives the handle, in front matter an earlier record wrote.
FORMER_NAME_FIELD = re.compile(r"(\n(\s*)(?:claimed_by|found_by|improved_by):\n\2- )ry-xu\n")


#: The prover a record written before the attribution migration of 13 to 20 October 2026
#: names by handle in a lower bound, with the credited name that replaced it
#: (attribution.md), and the same handle's possessive in that lower bound's note.
FORMER_PROVERS = {"wand125": "Hosono", "squarepacker (Ryu Sungjoon)": "Ryu Sungjoon"}
FORMER_NOTE_NAMES = ((re.compile(r"(?<![\w/@\[-])wand125's"), "Hosono's"),)


def _named_lower(layer: object) -> object:
    """A lower-bound layer with its prover and note credited as the record credits them
    now, so a replayed earlier layer that differs only by the migrated name is the same
    layer (`refreshed`)."""
    if not isinstance(layer, Mapping):
        return layer
    named = dict(cast("Mapping[str, Any]", layer))
    provers = named.get("proved_by")
    if isinstance(provers, list):
        named["proved_by"] = [FORMER_PROVERS.get(str(name), name) for name in provers]
    note = named.get("note")
    if isinstance(note, str):
        for pattern, replacement in FORMER_NOTE_NAMES:
            note = pattern.sub(replacement, note)
        named["note"] = note
    return named


def _named_fields(front: str) -> str:
    """Front matter whose name fields credit the finder by name where an earlier record
    gave the handle; every other item's text is left alone."""
    return FORMER_NAME_FIELD.sub(rf"\1{XU}\n", front)


def _named_prose(text: str) -> str:
    """`text` with the ry-xu section crediting its finder by name, not by handle."""
    for pattern, replacement in FORMER_PROSE:
        text = pattern.sub(replacement, text)
    return text


def _person(name: object) -> str:
    """A credited name as prose writes it, without the handle in parentheses."""
    text = re.sub(r"\s*\([^)]*\)$", "", str(name))
    return PROSE_NAMES.get(text, text)


def _earlier(packing: Mapping[str, Any]) -> list[str]:
    """The register entries the case's earlier verified ceiling rests on."""
    evidence = list(packing["verified_upper_bound"].get("evidence") or ())
    return _results_holding(evidence, packing["n"])


def _holder(packing: Mapping[str, Any]) -> str:
    """The earlier house, said the way the record credits it."""
    upper = packing["reported_upper_bound"]
    finders = [_person(name) for name in upper.get("found_by") or ()]
    improvers = [_person(name) for name in upper.get("improved_by") or ()]
    evidence = list(packing["verified_upper_bound"].get("evidence") or ())
    if "E-basic-grid-upper" in evidence:
        return "the trivial grid"
    text = _join(finders) + "’s packing" if finders else "the catalogue’s packing"
    if improvers:
        text += f", improved by {_join(improvers)}"
    results = _earlier(packing)
    if results:
        text += f" ({', '.join(results)})"
    return text


def plan(
    selections: Mapping[int, select_houses.Selection] | None = None,
    texts: Mapping[int, str] | None = None,
) -> list[Move]:
    """Every count whose derived house is below its case and is one this adoption houses.

    Each move carries its case record's text, read from the frontier unless `texts` holds
    the count, as a replay of the retained prior state passes it. A count staged in
    `select_houses.PENDING_ADOPTION` for the house the selection names is no move here
    until its bead's pull request takes it off the list. A house whose regularization item
    is owed a correction (`select_houses.CORRECTIONS_OWED`) is refused until the item is
    corrected, so its uncorrected credit is never written (review B1 of #658).
    """
    selections = select_houses.select() if selections is None else selections
    moves = []
    for n, selection in sorted(selections.items()):
        if selection.house is None:
            continue
        house = selection.house
        staged = select_houses.PENDING_ADOPTION.get(n)
        if staged is not None and staged.house == house.result:
            # Owed to the staged bead's pull request, which takes the count off the list
            # and then adopts it here.
            continue
        if (owed := select_houses.owed_correction(n, house)) is not None:
            # The credit this writes is the item's `of`, which a review measured to be
            # wrong here: the adoption waits for the correction (review B1 of #658).
            raise AdoptionError(
                f"n={n}: {house.result}'s regularization item names {owed.named} as the "
                f"packing it solves, which {owed.measured_in} measured to be {owed.measured}; "
                f"correct the item first ({owed.bead}, select_houses.CORRECTIONS_OWED)"
            )
        if house.algebraic:
            raise AdoptionError(
                f"n={n}: the house is {house.result}'s algebraic side, and this writes a "
                "rational exact form and witness only; stage the count with the bead that "
                "adds the algebraic writer (select_houses.PENDING_ADOPTION)"
            )
        if houses.ADOPTED.get(n) != house.result:
            raise AdoptionError(
                f"n={n}: the house is {house.result}, which upper_bound_houses does not draw "
                "here; add its packet and the count to upper_bound_houses first"
            )
        if house.result not in RESULTS or n not in CREDITS:
            raise AdoptionError(f"n={n}: no prose or credit for {house.result}")
        if texts is not None and n in texts:
            text = texts[n]
        else:
            text = select_houses.case_path(n).read_text(encoding="utf-8")
        moves.append(Move(selection, house, _packing(_split(text)[1]), text))
    return moves


def _source_url(key: str, n: int) -> str:
    return str(_covering(key, n)["url"])


def reported_bound(move: Move) -> dict[str, Any]:
    house, credit = move.house, CREDITS[move.n]
    bibliography = _bibliography()[house.source_key]
    origin = houses.source_for(move.n).origin(move.n)
    replaced = move.packing["reported_upper_bound"]
    known: dict[str, Any] = {
        "analytically_optimized": None,
        "construction_method": "unknown",
        "tilt_angles_deg": None,
    }
    if credit.same_packing:
        known = {field: replaced.get(field, known[field]) for field in PACKING_FACTS}
    return {
        "value": _value(house, _above(move)),
        "exact_form": houses.legacy.literal(move.side),
        "evidence": list(house.report_evidence),
        "algebraic_degree": 1,
        "minimal_polynomial": None,
        "analytically_optimized": known["analytically_optimized"],
        "catalogue_rigid": "not-stated",
        "construction_method": known["construction_method"],
        "tilt_angles_deg": known["tilt_angles_deg"],
        "found_by": list(credit.found_by),
        "found_year": (
            credit.found_year
            if credit.found_year is not None
            else date.fromisoformat(house.published).year
        ),
        "improved_by": list(credit.improved_by),
        "catalogue_pictured": False,
        "source_key": house.source_key,
        "source_date": str(bibliography["dated"]),
        "retrieved_date": origin.retrieved,
        "witnesses": [f"W-known-best-n{move.n:03d}"],
    }


def verified_bound(move: Move) -> dict[str, Any]:
    return {
        "value": shown(move.side, _above(move)),
        "exact_form": houses.legacy.literal(move.side),
        "evidence": list(move.house.confirming_evidence),
    }


#: A history note this adoption wrote, and the day its house stopped being the ceiling.
HELD_UNTIL = re.compile(r"^Earlier house .*, the case’s ceiling (?:from .* )?until (.+?);")


def held_since(packing: Mapping[str, Any]) -> str | None:
    """The day the record's house became its ceiling, where an earlier note dates it.

    When an earlier pass adopted the house, its note on the house before says until when
    that one held, which is the day this one began; a house no pass of this adoption
    wrote has no such note, and its start is not stated.
    """
    days = [
        match.group(1)
        for note in packing.get("priority_notes") or ()
        if (match := HELD_UNTIL.match(" ".join(str(note.get("claim") or "").split())))
    ]
    return days[-1] if days else None


def history_note(move: Move) -> dict[str, Any]:
    upper = move.packing["reported_upper_bound"]
    claimed = [*(upper.get("found_by") or ()), *(upper.get("improved_by") or ())]
    since = held_since(move.packing)
    held = f"from {since} until" if since else "until"
    earlier = f"{upper['value']} from {upper['source_key']}"
    if _lanes_differ(move.packing):
        results = ", ".join(_earlier(move.packing)) or "its verified evidence"
        earlier = (
            f"{_ceiling(move.packing)} from {results} (reported as {upper['value']} from "
            f"{upper['source_key']})"
        )
    return {
        "claim": (
            f"Earlier house {earlier}, the case’s ceiling {held} {day_words(move.n)}; its "
            "certificate and replay remain retained."
        ),
        "claimed_by": [RECORD_NAMES.get(str(name), str(name)) for name in claimed],
        "published": upper.get("source_date"),
        "year": upper.get("found_year"),
    }


def _roster(move: Move) -> list[str]:
    """Every confirmed certificate's evidence at the count, selected or not."""
    wanted: list[str] = []
    for candidate in move.selection.candidates:
        wanted.extend(candidate.report_evidence)
        wanted.extend(candidate.confirming_evidence)
    return list(dict.fromkeys(wanted))


def _resource(move: Move) -> dict[str, Any]:
    return {
        "key": move.house.source_key,
        "role": "upper-bound-report",
        "local": f"web/{houses.source_for(move.n).packet.name}",
        "url": _source_url(move.house.source_key, move.n),
        "retrieved": True,
    }


def front_matter(move: Move, front: str) -> str:
    packing = move.packing
    withdrawn = not conjecture_stands(packing, move.house.side)
    front = _named_fields(front)
    reviewed = f"  source_reviewed: '{houses.adopted_on(move.n)}'"
    front = re.sub(r"^  source_reviewed: .*$", reviewed, front, count=1, flags=re.MULTILINE)
    front = _replace(front, "reported_upper_bound", reported_bound(move))
    front = _replace(front, "verified_upper_bound", verified_bound(move))
    if withdrawn:
        front = re.sub(
            r"^  conjectured_optimum: .*$",
            "  conjectured_optimum: null",
            front,
            count=1,
            flags=re.MULTILINE,
        )
    front = _append(front, "priority_notes", [history_note(move)])
    present = set(packing.get("evidence") or ())
    front = _append(front, "evidence", [item for item in _roster(move) if item not in present])
    keys = {str(item["key"]) for item in packing.get("resources") or ()}
    if move.house.source_key not in keys:
        front = _append(front, "resources", [_resource(move)])
    blockers = packing.get("blockers") or []
    kept = [item for item in blockers if not _trailing_blocker(item)]
    if kept != blockers:
        front = _replace(front, "blockers", kept)
    return front


def conjecture_stands(packing: Mapping[str, Any], side: exact_sides.Side) -> bool:
    """Whether a record's conjectured optimum stands beside a house at `side`.

    A conjecture the house is below is refuted and withdrawn. A conjecture is the
    catalogue's printed side, whose rounding the record does not state: however it was
    rounded, the number it stands for lies strictly within one unit of its last place of
    the print, so the house is below it wherever it is at or below the print less that
    unit (review B6 of #660). An integer conjecture is exact, and a house below it refutes
    it. Any other conjecture stands: a house at it, or above, or within its print's
    rounding, is no evidence against it, and the adoption goes ahead either way
    (result-import.md, "The House Rule").
    """
    conjecture = conjectured(packing)
    if conjecture is None:
        return True
    text = str(packing.get("conjectured_optimum"))
    places = 0 if text == "integer" else len(text.strip().partition(".")[2])
    if not places:
        return not side < conjecture
    return not side <= conjecture - Fraction(1, 10**places)


def conjectured(packing: Mapping[str, Any]) -> Fraction | None:
    """The side a record conjectures optimal, if it conjectures one.

    The generator writes `integer` for a grid case, whose conjecture is that the optimum
    is the integer side the case reports (`generate_frontier_case`).
    """
    conjecture = packing.get("conjectured_optimum")
    if conjecture is None:
        return None
    if conjecture == "integer":
        conjecture = packing["reported_upper_bound"]["value"]
    return Fraction(Decimal(str(conjecture)))


def _trailing_blocker(blocker: Mapping[str, Any]) -> bool:
    """A blocker that only said the verified lane trailed the report, which now agree."""
    detail = str(blocker.get("detail") or "")
    return blocker.get("kind") == "mathematics" and detail.startswith(
        "verified_upper_bound is "
    )


# ------------------------------------------------------------------------- the body


def _math_fraction(value: Fraction) -> str | None:
    text = houses.legacy.literal(value)
    return f"${text}$" if len(text) <= FRACTION_CHARS else None


def _review(result: str) -> tuple[str, str]:
    """The stage 4 review that recommended the result, and its date in words."""
    entry = next(e for e in _register() if e["id"] == result)
    review = next(
        r for r in entry["reviews"] if r["path"] != FINAL_REVIEW and r["verdict"] == "accepted"
    )
    return str(review["path"]), words(str(review["date"]))


def _finally_reviewed(result: str) -> bool:
    """Whether the final review of 11 October covered the result as well as its own."""
    entry = next(e for e in _register() if e["id"] == result)
    return any(r["path"] == FINAL_REVIEW for r in entry["reviews"])


def _lanes_differ(packing: Mapping[str, Any]) -> bool:
    """Whether the replaced record's reported and verified upper bounds are two numbers.

    Where they are, the ceiling a house is measured from is the verified one, and the
    reported one is said apart (review C3 of #661): at 29 the catalogue's print
    5.93383346267692 beside T-155's exact side."""
    reported = packing["reported_upper_bound"]["value"]
    verified = packing["verified_upper_bound"]["value"]
    return Decimal(str(reported)) != Decimal(str(verified))


def _ceiling(packing: Mapping[str, Any]) -> str:
    """The earlier ceiling to quote: the exact verified side when its displays differ.

    Otherwise retain the shared display. The exact certificate margin is stated
    separately, since neither outward display need equal its certificate's side.
    """
    if _lanes_differ(packing):
        return str(packing["verified_upper_bound"]["exact_form"])
    return str(packing["reported_upper_bound"]["value"])


def _reported_apart(move: Move) -> str:
    """What the replaced reported bound says of the new side, where it is a number apart
    from the verified ceiling: a print orders a side only beyond one unit of its last
    place, so inside that unit it orders nothing (`check_source_coverage.print_order`)."""
    if not _lanes_differ(move.packing):
        return ""
    upper = move.packing["reported_upper_bound"]
    printed = Decimal(str(upper["value"]))
    bound, side = Fraction(printed), Fraction(move.side)
    unit = Fraction(Decimal(1).scaleb(int(printed.as_tuple().exponent)))
    if side < bound:
        relation = f"lies `{_sci(bound - side)}` above the new side"
    elif side < bound + unit and printed != printed.to_integral_value():
        relation = (
            f"is a print `{_sci(side - bound)}` below the new side, within one unit of its "
            "last place, so it does not order them"
        )
    else:
        relation = f"lies `{_sci(side - bound)}` below the new side"
    return (
        f"; the reported upper bound it replaces, ${upper['value']}$ from "
        f"{upper['source_key']}, {relation}"
    )


def opening(move: Move) -> str:
    n, house, credit = move.n, move.house, CREDITS[move.n]
    earlier = (
        "The earlier exact ceiling, "
        if _lanes_differ(move.packing)
        else "The earlier ceiling, displayed outward as "
    )
    return (
        f"**House adoption, {day_words(n)}.** {credit.phrase[0].upper()}{credit.phrase[1:]} "
        f"({house.result}) is now this case’s house: its exact certificate proves "
        f"$s({n}) \\le {shown(move.side, _above(move))}$, the reported and the verified "
        "upper bound, rounded outward from its exact side. The exact certificate side "
        "improves the previous verified exact side "
        f"by about `{_sci(move.selection.margin)}`. {earlier}"
        f"${_ceiling(move.packing)}$ from {_holder(move.packing)}, applied until this "
        "adoption and stays retained "
        f"as history{_reported_apart(move)} ([the certificate](#{_anchor(move)}))."
    )


def _title(move: Move) -> str:
    return f"{RESULTS[move.house.result].author}’s certificate ({move.house.result})"


def _anchor(move: Move) -> str:
    text = _title(move).lower().replace("’", "")
    return re.sub(r"[^a-z0-9 -]", "", text).replace(" ", "-")


def section(move: Move) -> str:
    n, house, credit = move.n, move.house, CREDITS[move.n]
    prose = RESULTS[house.result]
    packet = houses.source_for(n).packet.name
    review, reviewed = _review(house.result)
    fraction = _math_fraction(move.side)
    ceiling = shown(move.side, _above(move))
    side = (
        f"at exact side {fraction}, displayed upward as ${ceiling}$"
        if fraction
        else f"at an exact rational side, displayed upward as ${ceiling}$"
    )
    routes = prose.routes or (
        "One maintained route is the verifier the source ran; the independent rational "
        "corner checker and the third route are independently re-implemented."
        if prose.producer_route
        else "No route here is the source’s code, so the replay is independently "
        "re-implemented."
    )
    reviews = f"[review of {reviewed}](../../{review})"
    third = (
        prose.third_route
        if isinstance(prose.third_route, str)
        else ", and a third exact route, half-extent containment and exact intersection area, "
        "decided it again"
        if prose.third_route
        else "; no third exact route has decided it"
    )
    if _finally_reviewed(house.result):
        reviews = f"{reviews} and the [final review of 11 October 2026](../../{FINAL_REVIEW})"
    # A credit that ends in a report ("as refined in Francisco Couzo's #672 report") takes
    # another verb, so the sentence does not read "report, reported" (review B6 of #718).
    verb = "published" if credit.phrase.endswith(" report") else "reported"
    paragraphs = [
        f"## {_title(move)}",
        (
            f"{credit.phrase[0].upper()}{credit.phrase[1:]}, {verb} {prose.reported}, "
            f"{side} ({house.result}). The certificate gives a rational side and, for each "
            f"of the {n} unit squares, {prose.squares}; "
            f"the [retained packet](../resources/web/{packet}/README.md) holds it with the "
            "complete native jobs that decided it."
        ),
        (
            "Both maintained exact routes decided it here, `sqpack`’s exact separating-axis "
            "verifier and the independent rational corner checker, with its duplicate-square "
            f"and outside-container controls{third}. {routes} The {reviews} "
            "accepted the replay for finite feasibility. "
            f"That proves $s({n}) \\le {ceiling}$, the verified upper bound: confirmed, "
            f"{prose.confirmation}. It says nothing about "
            "optimality, rigidity or a local minimum."
        ),
    ]
    if house.regularizes and house.result not in DISPLAY_REGULARIZERS:
        paragraphs.append(_regularization(move, prose.author))
    elif house.regularizes:
        paragraphs.append(
            "The certificate regularizes for display the packing "
            f"{house.regularizes} records, at the side the source reports as that packing’s "
            "exact optimum, so the packing stays with its finder and Evan Daniel is "
            "credited with the regularization and the certificate. That the two are one "
            f"packing is the source’s claim, measured here and not decided ({house.result}’s "
            "regularizations)."
        )
    if prose.ai:
        paragraphs.append(prose.ai)
    lineage = (prose.lineage_at or {}).get(move.n, prose.lineage)
    if lineage:
        paragraphs.append(lineage)
    earlier = set(_earlier(move.packing))
    held = set(move.selection.held)
    others = [
        c
        for c in move.selection.candidates
        if c is not house and c.result not in earlier and c not in held
    ]
    history = (
        f"The house it replaces, ${_ceiling(move.packing)}$ from {_holder(move.packing)}, "
        "stays retained with its own replay as history."
    )
    if others:
        listed = _join([f"{c.result} at ${display(c.side)}$" for c in others])
        history += (
            f" The other certificates confirmed here at this count, {listed}, stay verified "
            "and are not selected."
        )
    waiting = [
        *held_sentences(move.selection.held, move.side, below="this house", keeps="this house"),
        *algebraic_sentences(move.selection, move.side),
        *staged_sentences(
            move.n,
            move.side,
            named={c.result for c in move.selection.held}
            | {
                result
                for result, key in move.selection.algebraic
                if select_houses.algebraic_below(key, move.n, move.side)
            },
            below="this house",
            keeps="this house",
        ),
    ]
    if waiting:
        history += " " + " ".join(waiting)
    paragraphs.append(history)
    return "\n\n".join(paragraphs) + "\n"


def _reason(result: str) -> str:
    """Why a held result waited, as case prose writes it, in the past since the house rule."""
    return select_houses.LIFTED[result].reason.replace("'", "’")


def _staged(n: int, result: str) -> str:
    """Where a record says the count's adoption of `result` waits: its staged bead."""
    staged = select_houses.PENDING_ADOPTION.get(n)
    if staged is None or staged.house != result:
        return ""
    return f", staged under {staged.bead},"


def _writer_clause(staged: select_houses.Pending) -> str:
    """What a staged adoption that waits for the writer adds: when it can move the case."""
    if staged.why == select_houses.NO_WRITER:
        return ", once the writer takes an algebraic side"
    return ""


def _keeps_until(n: int, result: str, keeps: str) -> str:
    """The sentence that says what the case keeps until an adoption moves it.

    Where the count is staged for `result`, or for nothing, that is `result`'s adoption.
    Where a packing validated since is smaller still and staged in its place, as T-193's
    exact sides are below T-174's at twelve counts (#658), it is that packing's adoption,
    under its own bead and, where it waits for the writer, once the writer takes it; the
    held result is named as the side it passes, and `staged_sentences` describes the
    staged house (review B3 of #658)."""
    staged = select_houses.PENDING_ADOPTION.get(n)
    if staged is not None and staged.house != result:
        return (
            f"The case keeps {keeps} until {staged.house}’s adoption, staged under "
            f"{staged.bead}, moves it to {staged.house}’s side, below {result}’s"
            f"{_writer_clause(staged)}."
        )
    return (
        f"The case keeps {keeps} until {result}’s adoption{_staged(n, result)} moves it to "
        f"{result}’s side."
    )


def held_sentences(
    held: Sequence[select_houses.Candidate], side: exact_sides.Side, *, below: str, keeps: str
) -> list[str]:
    """What a record says of each held certificate below `side`: smaller, confirmed and
    reviewed, when it was held and why, and that the house rule lifted the hold, so the
    case moves to it when its staged adoption lands. No wait is the owner's (reviews A2
    and C7 of #660)."""
    sentences = []
    for candidate in held:
        review, reviewed = _review(candidate.result)
        sentences.append(
            f"{candidate.result} at ${display(candidate.side)}$, "
            f"`{_sci(exact_sides.lower_gap(side, candidate.side))}` below {below}, is "
            "confirmed here and accepted by "
            f"the [review of {reviewed}](../../{review}). {lifted_sentence(candidate.result)} "
            + _keeps_until(candidate.n, candidate.result, keeps)
        )
    return sentences


def lifted_sentence(result: str) -> str:
    """The sentence a record gives a lifted hold: from when to when, and why it held."""
    hold = select_houses.LIFTED[result]
    return (
        f"From {words(hold.since)} until the owner’s house rule of {words(hold.until)} "
        f"lifted the hold, {_reason(result)}."
    )


def _spaced(words_: str) -> str:
    """A phrase as a pattern that matches it wrapped at any space."""
    return r"\s+".join(re.escape(word) for word in words_.split())


def held_history(text: str) -> str:
    """A section's held sentences once a later pass moves the house, as history.

    The section says why a lifted hold's certificate below its house waited and that the
    case would keep that house until the certificate's adoption. A later pass has moved
    the house, to that certificate or below it, so the section keeps when the hold held
    and why, and the clause that the case keeps the house goes: #657's adoption moved ten
    such counts below T-174 on 16 October 2026. The sentence is matched as each writer
    wrote it: the rule of 15 October's, which left the wait to the owner, and the house
    rule's, before and since its dates came first (review C7 of #660).
    """
    for result, hold in select_houses.LIFTED.items():
        whose = _spaced(hold.whose.replace("'", "’"))
        name = re.escape(result)
        since, until = _spaced(words(hold.since)), _spaced(words(hold.until))
        lifted = rf"until\s+the\s+owner’s\s+house\s+rule\s+of\s+{until}\s+lifted\s+the\s+hold"
        # Either the held result's own adoption moves the case, or a smaller packing staged
        # in its place does, below the held result's side (`_keeps_until`).
        keeps = (
            rf"case\s+keeps\s+(?:this|its)\s+house\s+until\s+(?:{name}’s\s+adoption"
            rf"(?:,\s+staged\s+under\s+think-[a-z0-9]+,)?\s+moves\s+it\s+to\s+{name}’s\s+side\."
            rf"|T-\d+’s\s+adoption,\s+staged\s+under\s+think-[a-z0-9]+,\s+moves\s+it\s+to\s+"
            rf"T-\d+’s\s+side,\s+below\s+{name}’s"
            rf"(?:,\s+once\s+the\s+writer\s+takes\s+an\s+algebraic\s+side)?\.)"
        )
        history = f". {lifted_sentence(result)}"
        # The rule of 15 October's: "..., but PR #574's houses are held for the owner:
        # <why>; the case keeps this house until the owner decides, and moves to T-174's
        # side if the owner adopts them."
        text = re.sub(
            rf",\s+but\s+{whose}\s+houses\s+are\s+held\s+for\s+the\s+owner:\s+(?:(?!\n\n).)*?;"
            rf"\s+the\s+case\s+keeps\s+(?:this|its)\s+house\s+until\s+the\s+owner\s+decides,"
            rf"\s+and\s+moves\s+to\s+{name}’s\s+side\s+if\s+the\s+owner\s+adopts\s+them\.",
            lambda _match, history=history: history,
            text,
            flags=re.DOTALL,
        )
        # The house rule's first: ". PR #574's houses were held for the owner, since <why>,
        # from <since> until the owner's house rule of <until> lifted the hold: the case
        # keeps this house until T-174's adoption[, staged under <bead>,] moves it ..."
        text = re.sub(
            rf"\.\s+{whose}\s+houses\s+were\s+held\s+for\s+the\s+owner,\s+since\s+"
            rf"(?:(?!\n\n).)*?,\s+from\s+{since}\s+{lifted}:\s+the\s+{keeps}",
            lambda _match, history=history: history,
            text,
            flags=re.DOTALL,
        )
        # The house rule's since: "From <since> until ... lifted the hold, PR #574's houses
        # were held for the owner, since <why>. The case keeps this house until ..."
        text = re.sub(
            rf"(From\s+{since}\s+{lifted},\s+{whose}\s+houses\s+were\s+held\s+for\s+the\s+"
            rf"owner,\s+since\s+(?:(?!\n\n).)*?\.)\s+The\s+{keeps}",
            r"\1",
            text,
            flags=re.DOTALL,
        )
    return text


def algebraic_sentences(selection: select_houses.Selection, side: Fraction) -> list[str]:
    """What a record says of an algebraic certificate below its house: decided on one exact
    route, which the rule of 15 October left out for the owner (RP-3 of PR 574's review),
    and which the house rule adopts, staged until the writer takes an algebraic side
    (review A2 of #660)."""
    sentences = []
    for result, key in selection.algebraic:
        if not select_houses.algebraic_below(key, selection.n, side):
            continue
        _value, degree = select_houses.algebraic_side(key, selection.n)
        margin = select_houses.algebraic_margin(key, selection.n, side)
        review, reviewed = _review(result)
        opening = (
            f"{result}’s algebraic certificate at this count, a root of a degree-{degree} "
            f"integer polynomial `{_sci(margin)}` below this house, is decided here on one "
            "exact route. The rule of 15 October left it out for the owner (RP-3 of the "
            f"[review of {reviewed}](../../{review})), and the owner’s house rule of "
            f"{words(select_houses.RULE_SET_ON)} "
        )
        staged = select_houses.PENDING_ADOPTION.get(selection.n)
        if staged is not None and staged.house != result:
            # A smaller packing is staged in its place (review B3 of #658).
            sentences.append(
                f"{opening}ended that wait. {_keeps_until(selection.n, result, 'this house')}"
            )
            continue
        sentences.append(
            f"{opening}adopts it: the case keeps this house until "
            f"its adoption{_staged(selection.n, result)} moves it to {result}’s side, once "
            "the writer takes an algebraic side."
        )
    return sentences


def _staged_house(n: int) -> tuple[select_houses.Pending, select_houses.Candidate] | None:
    """The adoption staged at `n` and its house's candidate there, if any."""
    staged = select_houses.PENDING_ADOPTION.get(n)
    if staged is None:
        return None
    entries = [e for e in select_houses.load_results() if e["id"] == staged.house]
    found = select_houses.candidates(entries, select_houses.load_evidence()).get(n)
    return (staged, found[0]) if found else None


def staged_sentences(
    n: int, side: exact_sides.Side, *, named: set[str], below: str, keeps: str
) -> list[str]:
    """What a record says of a smaller house staged at its count that its other sentences
    do not describe: one validated after the pass that wrote the record, as T-193's exact
    algebraic sides are below T-186's houses at 175, 204, 232 and 302 and below T-174's
    held sides at twelve counts (#658).

    `named` are the results the record's held and algebraic sentences describe. Where the
    staged house is among them, nothing is added. Where they describe others, their
    closing clause already says the case moves to the staged house (`_keeps_until`), so
    this adds what the staged house is: its kind, its margin below `below` and the review
    that accepted it (review B3 of #658). Where there are none, it says that and that the
    case keeps `keeps` until the staged adoption moves it."""
    found = _staged_house(n)
    if found is None:
        return []
    staged, candidate = found
    if staged.house in named or not candidate.side < side:
        return []
    review, reviewed = _review(staged.house)
    kind = (
        f"exact algebraic side at this count, a root of a degree-{candidate.side.degree} "
        "integer polynomial"
        if isinstance(candidate.side, exact_sides.Algebraic)
        else "exact side at this count"
    )
    margin = _sci(exact_sides.lower_gap(side, candidate.side))
    described = (
        f"{staged.house}’s {kind} `{margin}` below {below}, is confirmed here and "
        f"accepted by the [review of {reviewed}](../../{review})."
    )
    if named:
        return [described]
    return [
        (
            f"{described[:-1]}. The owner’s house rule "
            f"of {words(select_houses.RULE_SET_ON)} adopts it: the case keeps {keeps} "
            f"until its adoption, staged under {staged.bead}, moves it to {staged.house}’s "
            f"side{_writer_clause(staged)}."
        )
    ]


#: The results whose regularizations are for display, at the side the source reports as
#: the packing's exact optimum, with the regularizer credited (T-146 and T-225, Evan
#: Daniel's regularized lists of 10 and 20 October). Every other result's regularizations
#: are certificates of the packing its entry names, by the identity's basis
#: (`_regularization`).
DISPLAY_REGULARIZERS = frozenset({"T-146", "T-225"})


def _regularization(move: Move, author: str) -> str:
    """What a house that tightens a registered packing says of it, by its identity's basis.

    T-146's regularizations, for display at the source's exact optimum, keep their own
    sentence; any other is a certificate of the packing its entry names (`of`).
    """
    house = move.house
    entry = next(e for e in _register() if e["id"] == house.result)
    item = next(i for i in entry["regularizations"] if i["n"] == move.n)
    basis = str((item.get("identity") or {}).get("basis") or "source-claim")
    how = (
        "measured here pose by pose as that packing"
        if basis == "measured"
        else "that packing by the source’s statement, not decided here"
    )
    return (
        f"The certificate is {author}’s tightening of the packing {house.regularizes} "
        f"records, {how} ({house.result}’s regularizations), so the packing keeps its "
        f"finder’s credit and {author} is credited with the certificate."
    )


#: The heading `apply_exact_ceilings` gives the section on a ceiling that trails the print.
CEILING_HEADING = "## The verified upper bound is a ceiling"
EARLIER_CEILING = "## The earlier verified ceiling"


def _earlier_ceiling(move: Move, text: str) -> str:
    """`T-101`'s exact-ceiling prose, in the past tense from this adoption on.

    `apply_exact_ceilings` wrote it where a certified side, rounded up at the catalogue's
    places, trailed the catalogue's print; the house replaces both lanes, so the ceiling,
    the blocker that recorded the gap and the certificate's bound are history.
    """
    n, until = move.n, day_words(move.n)
    bound = rf"\$s\({n}\)\s+\\le\s+[0-9.]+\$"
    text = re.sub(
        rf"\bit\s+proves\s+({bound}),\s+the\s+verified\s+upper\s+bound\s+\((T-\d+)\)\.",
        rf"it proved \1, the verified upper bound until {until} (\2).",
        text,
    )
    text = re.sub(
        rf"\bThat\s+proves\s+({bound}),\s+the\s+verified\s+upper\s+bound:\s+the\s+certificate’s",
        rf"That proved \1, the verified upper bound until {until}: the certificate’s",
        text,
    )
    start = text.find(f"\n{CEILING_HEADING}\n")
    if start < 0:
        return text
    end = text.find("\n## ", start + 1)
    end = len(text) if end < 0 else end
    section = text[start:end].replace(CEILING_HEADING, EARLIER_CEILING, 1)
    section = re.sub(
        r"`verified_upper_bound`\s+for\s+this\s+case\s+is\s+(\$[0-9.]+\$),",
        rf"Until {until} the verified upper bound here was \1,",
        section,
    )
    # T-101's ceiling section opens the sentence with "It is"; T-155's, where it took the
    # ceiling to T-101's exact side, with "As printed it is" (`register_regularized_bounds`).
    section = re.sub(
        r"(It|As\s+printed\s+it)\s+is\s+\*\*larger\*\*\s+than\s+the\s+best\s+known\s+"
        r"(\$[0-9.]+\$)\s+two\s+fields\s+above\s+it,",
        r"\1 was **larger** than the catalogue’s printed side \2, then the best known,",
        section,
    )
    section = re.sub(
        rf"It\s+is\s+not\s+the\s+value\s+of\s+\$s\({n}\)\$",
        f"It was not the value of $s({n})$",
        section,
    )
    section = re.sub(
        r"The\s+`mathematics`\s+blocker\s+in\s+the\s+frontmatter\s+records\s+the\s+difference\."
        r"\s+Read\s+`reported_upper_bound`\s+for\s+the\s+best\s+known\s+side\s+length\.",
        f"A `mathematics` blocker in the frontmatter recorded the difference until "
        f"{_title(move)} replaced both lanes.",
        section,
    )
    return text[:start] + section + text[end:]


def _regularized_certificate(move: Move, text: str) -> str:
    """The prose `register_regularized_bounds` wrote, in the past tense from this adoption on.

    Where a regularized view's exact side was registered (T-155) at exactly the side of Evan
    Daniel's certificate of the same packing (T-101), that layer made the side the verified
    upper bound in a dated paragraph and a section of fixed form; the house replaces both
    lanes below it, so the view's bound is history and stays true as stated.
    """
    n, until = move.n, day_words(move.n)
    bound = rf"\$s\({n}\)\s+\\le\s+[0-9.]+\$"
    text = re.sub(
        r"\bThe\s+verified\s+upper\s+bound\s+is\s+now\s+that\s+side\s+exactly,\s+resting\s+on"
        r"\s+both\s+certificates\s+\(([^)]*)\),\s+and\s+the\s+record\s+still\s+prints\s+it\s+as",
        rf"The verified upper bound was that side exactly until {until}, resting on both "
        r"certificates (\1), and the record printed it as",
        text,
    )
    text = re.sub(
        rf"\bThat\s+proves\s+({bound})\.(\s+Evan\s+Daniel’s\s+certificate\s+of\s+this\s+packing"
        r"\s+already\s+proves\s+the\s+same\s+bound)",
        rf"That proves \1, the verified upper bound until {until}.\2",
        text,
    )
    text = re.sub(
        r"\bThat\s+side\s+is\s+the\s+exact\s+form\s+of\s+the\s+case’s\s+`verified_upper_bound`,"
        r"\s+which\s+cites\s+both\s+certificates\s+\(([^)]*)\)\s+and\s+prints\s+it\s+as",
        rf"That side was the exact form of the case’s `verified_upper_bound` until {until}, "
        r"which cited both certificates (\1) and printed it as",
        text,
    )
    if houses.adopted_on(n) < VIEW_SECTION_FROM:
        return text
    # Where the view's dated paragraph and section state the bound it proved as the
    # verified lane, both are history too, from the pass of 19 October 2026 on: n = 229
    # was the first count whose house moved off a T-155 view by more than the section's
    # printed places. The paragraph is the form `register_regularized_bounds` writes for a
    # side not at T-101's (review A1 of #692).
    text = re.sub(
        rf"\b(it\s+proves\s+{bound}),\s+the\s+verified\s+upper\s+bound\s+\((T-\d+)\)"
        r"(\s+rounded\s+up\s+at\s+\d+\s+places)?,\s+which\s+the\s+record\s+still\s+prints\s+as"
        r"\s+(\$[0-9.]+\$)\.",
        rf"\1, the verified upper bound until {until} (\2)\3, which the record printed as \4.",
        text,
    )
    return re.sub(
        rf"\bThat\s+proves\s+({bound}),\s+the\s+verified\s+upper\s+bound\s+\((T-\d+)\),\s+the"
        r"\s+exact\s+form\s+of\s+the\s+case’s\s+`verified_upper_bound`,\s+which\s+prints\s+it\s+as"
        r"\s+(\$[0-9.]+\$),\s+the\s+decimal\s+it\s+printed\s+before",
        rf"That proves \1, the verified upper bound until {until} (\2), then the exact form "
        r"of the case’s `verified_upper_bound`, which printed it as \3, the decimal it printed "
        r"before",
        text,
    )


#: The dated paragraph the intake of 18 October 2026 wrote under a case's title for a
#: report it registered at V0/C0 below the house (b783bcc0a), through the paragraphs that
#: follow it up to the next dated one or heading.
PENDING_REPORT = re.compile(
    r"\*\*Reported\s+certificate\s+pending\s+adoption,\s+(\d{4}-\d{2}-\d{2})\.\*\*"
    r"(?:(?!\n\n(?:\*\*|#)).)*",
    re.DOTALL,
)


def pending_history(text: str, until: str) -> str:
    """A registration's "pending adoption" paragraph, once a pass moves the house, as history.

    The paragraph said the registration left both upper lanes, the house witness and its
    drawing unchanged until review and adoption, and that the rigidity and arrangement
    notes below described that house; from the intake of 20 October 2026 it says the same
    of the house best packing, in a sentence of its own (#701 at n = 260), and that the
    side is registered at V0/C0; where no rigidity or arrangement note follows, that
    sentence ends at the drawing (#701's A6 at n = 204), and #704's names the house best
    packing in parentheses (T-196 at 260). An adoption at the count moves all of them,
    whichever certificate it adopts, so the paragraph says what held until then, and a
    sentence after it that calls a report pending adoption says until when (review A1 of
    #692: n = 155 and 229 adopted the very reports their paragraphs named, on 19 October
    2026).
    """

    def past(match: re.Match[str]) -> str:
        block = re.sub(
            r"^\*\*Reported\s+certificate\s+pending\s+adoption,\s+",
            "**Reported certificate, ",
            match.group(),
        )
        block = re.sub(
            r"\breports\s+a\s+(\d+)-square\s+certificate\b",
            r"reported a \1-square certificate",
            block,
        )
        # The rung the side held before its review, said as history: once the review
        # raises the result, a bare "was registered at V0/C0" asserts a rung no result at
        # the count holds (`rung_prose`), as at 204 once T-223 was V3/C3.
        block = re.sub(
            r"\bThe\s+exact\s+rational\s+side\s+is\s+registered\s+at\s+V0/C0\b",
            "Before its review, the exact rational side was registered at V0/C0",
            block,
        )
        # The house best packing may be named in parentheses, as #704's intake named T-196's
        # at 260 (review A1 of #706); the past form keeps the name.
        block = re.sub(
            r"\bUntil\s+separate\s+Stage\s+4\s+review\s+and\s+adoption,\s+both\s+case\s+upper"
            r"\s+lanes,\s+the\s+house\s+best\s+packing(\s+\([^)]*\))?\s+and\s+its\s+drawing\s+stay"
            r"\s+as\s+they\s+were(,\s+and\s+the\s+rigidity\s+and\s+arrangement\s+notes\s+below"
            r"\s+describe\s+that\s+packing)?\.",
            lambda match: (
                f"Until the adoption of {until}, both case upper lanes, the house best packing"
                + (f" {' '.join(match.group(1).split())}" if match.group(1) else "")
                + " and its drawing stayed as they were"
                + (
                    ", and the rigidity and arrangement notes below described that packing"
                    if match.group(2)
                    else ""
                )
                + "."
            ),
            block,
        )
        block = re.sub(
            r"\bThis\s+V0/C0\s+registration\s+leaves\s+both\s+case\s+upper\s+lanes,\s+the\s+house"
            r"\s+witness\s+and\s+its\s+drawing\s+unchanged\s+until\s+separate\s+Stage\s+4\s+review"
            r"\s+and\s+adoption\.\s+Rigidity\s+and\s+arrangement\s+notes\s+below\s+describe\s+that"
            r"\s+retained\s+house\.",
            f"Its V0/C0 registration left both case upper lanes, the house witness and its "
            f"drawing unchanged until the house adoption of {until}, and until then the "
            "rigidity and arrangement notes below described that retained house.",
            block,
        )
        return re.sub(r"\bpending\s+adoption\.", f"pending adoption until {until}.", block)

    return PENDING_REPORT.sub(past, text)


def _n29_history(text: str) -> str:
    """The numerical solve and Schadt's rational ceiling as historical evidence."""
    earlier = (
        "**This does not move any bound.** A high-precision root is not a certificate: "
        "no outward-rounded interval and no exact algebraic form is produced, so "
        "`verified_upper_bound` remains the Schadt rational and the `5.23e-5` gap to "
        "the reported record stands."
    )
    historical = (
        "**This solve did not move a bound.** A high-precision root is not a certificate: "
        "no outward-rounded interval and no exact algebraic form is produced, so at "
        "the time of the 28 August measurement, `verified_upper_bound` remained the "
        "Schadt rational and the `5.23e-5` gap to the reported record stood. "
        "The later interval and exact regularized certificates above superseded that ceiling."
    )
    text = re.sub(_spaced(earlier), historical, text)
    return re.sub(
        _spaced("This proves the formal upper bound shown above."),
        "This proved the earlier Schadt rational ceiling.",
        text,
    )


_STAGED_SENTENCE = re.compile(
    r"\b([Tt])he\s+owner’s\s+house\s+rule\s+of\s+(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})\s+adopts\s+it:"
    r"\s+the\s+case\s+keeps\s+this\s+house\s+until\s+its\s+adoption,\s+staged\s+under"
    r"\s+(think-[a-z0-9]+),\s+moves\s+it\s+to\s+(T-\d+)’s\s+side"
    r"(,\s+once\s+the\s+writer\s+takes\s+an\s+algebraic\s+side)?\."
)


def staged_history(text: str, until: str, house: str) -> str:
    """An earlier section's staged-adoption sentence (`staged_sentences`), once a pass moves
    the count: it said the case kept its house until the staged adoption moved it, which
    held until this pass, whether the pass adopts the staged house or a smaller one."""

    def past(match: re.Match[str]) -> str:
        initial, rule, bead, staged, writer = match.groups()
        opening = f"{initial}he owner’s house rule of {rule} adopted it"
        if staged == house:
            return (
                f"{opening}: the case kept this house until its adoption, staged under {bead}, "
                f"moved it to {staged}’s side on {until}."
            )
        waiting = " for the writer to take an algebraic side" if writer else ""
        return (
            f"{opening}, staged under {bead}{waiting}; on {until} the case moved instead to "
            f"{house}, a smaller validated packing below {staged}’s side."
        )

    return _STAGED_SENTENCE.sub(past, text)


def _retained_672(text: str) -> str:
    """The intake's and T-199's statements that Couzo's #672 was neither retained nor
    verified here, in the past tense: the pass of 22 October 2026 retained it and
    registered it as T-227, and measured it against T-199 (review A2 of #718)."""
    text = re.sub(
        r"Couzo’s\s+intervening\s+claim\s+remains\s+Stage\s+1\s+under\s+`think-2vjc`,\s+with"
        r"\s+no\s+packet\s+or\s+verification\s+adopted\s+here\.",
        "Couzo’s intervening claim remained Stage 1 under `think-2vjc`, with no packet or "
        "verification here, until 22 October 2026, when it was retained and registered as "
        "T-227.",
        text,
    )
    return re.sub(
        r"and\s+#672\s+is\s+not\s+yet\s+retained,\s+so\s+that\s+step\s+is\s+the\s+source’s"
        r"\s+\(T-199\)\.",
        "and #672 was not retained until 22 October 2026, so that step is the source’s "
        "(T-199); measured since (T-227), #672’s packing pairs with T-199’s under no "
        "symmetry.",
        text,
    )


def historical(move: Move, text: str) -> str:
    """The body's own statements of the earlier house, marked as history.

    `check_case_prose` holds every `s(n) <= x` a body writes to the front matter unless
    its sentence says it is historical. Seven kinds of prose refer to earlier bounds and
    are marked as history:

    - the opening "Open." sentence the generator writes, of the best known packing;
    - the exact-optimum sections that `T-098` wrote, in two fixed sentences;
    - the exact-ceiling prose that `T-101` wrote where a certified side rounded up trails
      the catalogue's print (`apply_exact_ceilings`): its dated paragraph, its ceiling
      section, now "The earlier verified ceiling", and its certificate section;
    - the regularized certificate's prose that `T-155` wrote (`register_regularized_bounds`):
      its dated paragraph and its section, at T-101's side and, from the pass of 19
      October 2026 on, off it;
    - a house an earlier pass of this adoption adopted, in its dated paragraph and its
      section;
    - the dated paragraph an intake wrote for a report it registered pending adoption,
      which said the house stayed until review and adoption (`pending_history`);
    - the n = 29 numerical solve and Schadt-certificate statements, which describe a
      ceiling the later interval and exact certificates superseded.

    Prose in no fixed form, which no tool here wrote, is not rewritten; `check_case_prose`
    refuses a record that still states it as the bound. The first pass marked such prose
    by hand at five counts, the SQUISH update sections at 155, 258, 263 and 302 and the
    grid prose at 308, and the pass of 19 October 2026 the intake's prose at 183
    (`HAND_MARKED`); every other word of an adopted body, the verifier table apart, is
    what this writes from the record its last pass read.
    """
    n, until = move.n, day_words(move.n)
    text = _named_prose(text)
    text = re.sub(
        r"^Open\. The best known published packing,",
        "Open. Previously, the best known published packing,",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^Open\.\s+The\s+best\s+known\s+packing\s+gives\b",
        "Open. Previously, the best known packing gave",
        text,
        flags=re.MULTILINE,
    )
    text = _earlier_ceiling(move, text)
    text = _regularized_certificate(move, text)
    if n == 29:
        text = _n29_history(text)
    text = held_history(text)
    text = pending_history(text, until)
    if houses.adopted_on(n) >= RETAINED_672_FROM:
        text = _retained_672(text)
    if houses.adopted_on(n) >= STAGED_HISTORY_FROM:
        text = staged_history(text, until, move.house.result)
    # The records are wrapped, so a sentence may break at any space; whitespace is
    # matched as such and the reflow is the formatter's.
    text = re.sub(
        r"(\*\*House adoption, [^*]+\.\*\*(?:(?!\n\n).)*?)\bis\s+now\s+this\s+case’s\s+house:",
        rf"\1was this case’s house until {until}:",
        text,
        flags=re.DOTALL,
    )
    # The 11 October pass quoted a credit that ended in its own comma, so its history at
    # 103 read "refined it, (T-146) was" and "refined it,, reported" (review B4 of #718).
    text = re.sub(r"\brefined\s+it,\s+\((T-\d+)\)\s+was\b", r"refined it (\1), was", text)
    text = re.sub(r"\brefined\s+it,,(\s)", r"refined it,\1", text)
    text = re.sub(
        rf"(That\s+proves\s+\$s\({n}\)\s+\\le\s+[0-9.]+\$,\s+the\s+verified\s+upper\s+bound):"
        r"\s+confirmed,",
        rf"\1 until {until}: confirmed,",
        text,
    )
    return re.sub(
        rf"(That\s+proves\s+\$s\({n}\)\s+\\le\s+[0-9.]+\\ldots\$,\s+the\s+verified\s+upper\s+bound);"
        r"\s+it\s+says",
        rf"\1 until {until}; it says",
        text,
    )


def body(move: Move, rest: str) -> str:
    """The body with the dated paragraph under its title and the section before the footer."""
    rest = historical(move, rest)
    lines = rest.split("\n")
    title = next(i for i, line in enumerate(lines) if line.startswith("# "))
    lines[title + 1 : title + 1] = ["", opening(move)]
    text = "\n".join(lines)
    footer = text.find(FOOTER)
    insert = section(move) + "\n"
    if footer < 0:
        return text.rstrip("\n") + "\n\n" + insert
    return text[:footer] + insert + text[footer:]


def adopted(move: Move) -> bool:
    upper = move.packing["reported_upper_bound"]
    return (
        upper.get("source_key") == move.house.source_key
        and Fraction(str(move.packing["verified_upper_bound"].get("exact_form")))
        == move.house.side
    )


def rewrite(move: Move) -> str:
    """The case record at its house: `move.text` with its front matter and body moved."""
    opening_fence, front, rest = _split(move.text)
    closing, text = rest[:4], rest[4:]
    if closing != "---\n":
        raise AdoptionError(f"n={move.n}: front matter has no closing fence")
    return opening_fence + front_matter(move, front) + closing + body(move, text)


# ------------------------------------------------------------------------- coverage


def _section_span(text: str, key: str) -> tuple[int, int]:
    start = re.search(rf"^{key}:\n", text, re.MULTILINE)
    if start is None:
        raise AdoptionError(f"coverage register has no {key}")
    following = re.search(r"^[a-z_]+:", text[start.end() :], re.MULTILINE)
    return start.start(), start.end() + following.start() if following else len(text)


#: The clause of a displaced house's row that names the certificate below it.
DISPLACED_BY = re.compile(r"and T-\d+'s exact side is smaller\.$")
#: A superseded row's words for the house above which its report lies, as `_unaccounted`
#: writes them or a pass wrote them by hand: a later house is smaller still, so the report
#: lies above it too, and the row names it (n = 305's issue-489 row, 17 October 2026).
ABOVE_HOUSE = re.compile(
    r"\babove the house adopted (here )?on \d{4}-\d{2}-\d{2}(?: \(T-\d+\))?"
)
#: The day a selected override's reason says its house was adopted.
ADOPTED_ON_DAY = re.compile(r"\badopted on (\d{4}-\d{2}-\d{2}) \(T-\d+\)")


def override_reason(n: int, result: str) -> str:
    """The selected override's reason at a count adopted for `result`.

    It says the smallest validated side, since the register may hold a smaller one not yet
    validated: T-223 at V0/C0, below the house best packings at 204 and 260 (review B1 of
    #704). Until that review it said "the smallest exact side the register holds"."""
    return (
        f"The smallest validated exact side the register holds at this count, confirmed at "
        f"V3/C3 by a replay here and an accepted review, adopted on {houses.adopted_on(n)} "
        f"({result})."
    )


def reworded(text: str, counts: Collection[int] | None = None) -> tuple[str, list[int]]:
    """The coverage register with each adopted count's selected override giving the reason
    `override_reason` writes now, and the counts whose reason that changes.

    `counts`, where given, limits it to those counts. An override at another source than
    the count's house is left as it is, for `check` to report."""
    data = safe_load(text)
    sources = {str(source["id"]): source for source in data["sources"]}
    changed = []
    for entry in data["selected_overrides"]:
        n = int(entry["n"])
        result = houses.ADOPTED.get(n)
        if result is None or (counts is not None and n not in counts):
            continue
        if sources[str(entry["source_id"])]["source_key"] != houses.source_for(n).key:
            continue
        reason = override_reason(n, result)
        if entry.get("reason") != reason:
            entry["reason"] = reason
            changed.append(n)
    if not changed:
        return text, []
    start, end = _section_span(text, "selected_overrides")
    dumped = yaml.safe_dump(
        {"selected_overrides": data["selected_overrides"]},
        sort_keys=False,
        allow_unicode=True,
        width=WIDTH,
    )
    return text[:start] + dumped + text[end:], changed


def coverage(moves: Sequence[Move], text: str) -> str:
    """The coverage register with each moved count's selection and supersessions."""
    data = safe_load(text)
    overrides = {int(entry["n"]): entry for entry in data["selected_overrides"]}
    superseded = list(data["superseded_reports"])
    for move in moves:
        n, house = move.n, move.house
        new = str(coverage_source(data["sources"], house.source_key, n)["id"])
        old = overrides.get(n)
        if old is not None and old["source_id"] == new:
            continue
        reason = override_reason(n, house.result)
        # Every report the earlier house beat, a catalogue baseline's included, is beaten
        # by the new one, which is smaller still. A row that an earlier adoption wrote for
        # the house it displaced names the house that is smaller; that is now this one.
        for report in superseded:
            if report["n"] == n:
                report["superseded_by"] = new
                if "reason" in report:
                    report["reason"] = DISPLACED_BY.sub(
                        f"and {house.result}'s exact side is smaller.", str(report["reason"])
                    )
                    report["reason"] = ABOVE_HOUSE.sub(
                        lambda match, n=n, result=house.result: (
                            f"above the house adopted {match.group(1) or ''}on "
                            f"{houses.adopted_on(n)} ({result})"
                        ),
                        str(report["reason"]),
                    )
        # The displaced house is recorded whether or not its source has a claims record:
        # its selected value is the source's print where it has one and the ceiling of
        # its exact side where it has none (`_value`). One an earlier pass adopted is
        # dated from that pass's day.
        if old is not None:
            since = ADOPTED_ON_DAY.search(str(old.get("reason") or ""))
            held = f"from {since.group(1)} until" if since else "until"
            superseded.append(
                {
                    "n": n,
                    "source_id": old["source_id"],
                    "value": old["value"],
                    "reason": (
                        f"The house {held} {houses.adopted_on(n)}; its certificate stays "
                        "retained and "
                        f"verified, and {house.result}'s exact side is smaller."
                    ),
                    "superseded_by": new,
                }
            )
        overrides[n] = {
            "n": n,
            "source_id": new,
            "value": _value(house, _above(move)),
            "evidence": house.report_evidence[0],
            "reason": reason,
        }
    superseded.extend(_unaccounted(data, overrides, superseded, moves))
    data["selected_overrides"] = [overrides[n] for n in sorted(overrides)]
    data["superseded_reports"] = superseded
    for key in ("selected_overrides", "superseded_reports"):
        start, end = _section_span(text, key)
        dumped = yaml.safe_dump(
            {key: data[key]}, sort_keys=False, allow_unicode=True, width=WIDTH
        )
        text = text[:start] + dumped + text[end:]
    return text


def _unaccounted(
    data: Mapping[str, Any],
    overrides: Mapping[int, Mapping[str, Any]],
    superseded: Sequence[Mapping[str, Any]],
    moves: Sequence[Move],
) -> list[dict[str, Any]]:
    """Each reparsed claim at a moved count that the new house holds, as superseded.

    `check_source_coverage` accounts for every claim a claims record prints, as a
    selected override, a superseded report or a beyond-horizon row. A claim at a moved
    count that was none of these, such as a certificate the issue did not name, is
    superseded by the count's new house when the house is not above it. Where the claim's
    source has an exact reader the two exact sides are compared, so a certificate equal
    to the house is said to be equal, whatever its print; otherwise the house is held to
    the print, and the row says so.
    """
    held = {move.n: move.house for move in moves}
    accounted = {(str(e["source_id"]), int(e["n"])) for e in superseded}
    accounted |= {(str(o["source_id"]), n) for n, o in overrides.items()}
    added = []
    for source in data["sources"]:
        if not source.get("claims_record"):
            continue
        for n, printed in sorted(_claims(ROOT / str(source["claims_record"])).items()):
            selected = overrides.get(n)
            if n not in held or (str(source["id"]), n) in accounted or selected is None:
                continue
            house, day = held[n], houses.adopted_on(n)
            exact = _exact_side(str(source.get("source_key") or ""), n)
            if exact is None and house.side < Fraction(Decimal(printed)):
                standing = f"the side it prints is above the house adopted here on {day}"
            elif exact is not None and house.side < exact:
                standing = (
                    f"its exact side is above the house adopted here on {day} ({house.result})"
                )
            elif exact is not None and house.side == exact:
                standing = (
                    f"its exact side equals the house adopted here on {day}, which "
                    f"{house.result}'s registered certificate holds"
                )
            else:
                continue
            added.append(
                {
                    "n": n,
                    "source_id": source["id"],
                    "value": printed,
                    "reason": (
                        "A certificate of the same release that no register entry cites; "
                        f"{standing}."
                    ),
                    "superseded_by": selected["source_id"],
                }
            )
    return added


def _exact_side(key: str, n: int) -> Fraction | None:
    """A claim's exact side where its source has a reader that rebuilds it at `n`."""
    if key not in select_houses.reports.HOUSES:
        return None
    try:
        return select_houses.reports.house_side(key, n)
    except select_houses.reports.ReportError:
        return None


# ------------------------------------------------------------------------- deferrals


def deferrals(text: str, cited: set[str]) -> str:
    """The deferral list without every entry whose evidence a case record now cites."""
    data = safe_load(text)
    kept = [entry for entry in data["deferrals"] if entry["evidence"] not in cited]
    if len(kept) == len(data["deferrals"]):
        return text
    head = text[: text.index("deferrals:")]
    if not kept:
        return head + "deferrals: []\n"
    rendered = yaml.safe_dump(
        {"deferrals": kept}, sort_keys=False, allow_unicode=True, width=WIDTH
    )
    lines = rendered.splitlines(keepends=True)
    return (
        head + lines[0] + "".join(f"  {line}" if line.strip() else line for line in lines[1:])
    )


def _cited(rewritten: Mapping[int, str] | None = None) -> set[str]:
    """The evidence every case record cites, reading `rewritten`'s texts where it has them."""
    rewritten = rewritten or {}
    found: set[str] = set()
    for path in sorted(FRONTIER.glob("n-[0-9][0-9][0-9].md")):
        n = int(path.stem.removeprefix("n-"))
        text = rewritten.get(n) or path.read_text(encoding="utf-8")
        found |= _evidence(_packing(_split(text)[1]))
    return found


def _evidence(node: object) -> set[str]:
    found: set[str] = set()
    if isinstance(node, Mapping):
        for key, value in node.items():
            if key == "evidence" and isinstance(value, list):
                found.update(str(item) for item in value)
            else:
                found |= _evidence(value)
    elif isinstance(node, list):
        for item in node:
            found |= _evidence(item)
    return found


# ------------------------------------------------------------------------- driving


# ------------------------------------------------------------------------- history


def passes() -> tuple[str, ...]:
    """The adoption's passes, earliest first: the day it began and each later pass's."""
    return (houses.ADOPTED_ON, *sorted(houses.LATER_PASSES))


def prior_state(day: str) -> Path:
    """The archive of the pass of `day`: each record it moved, as it stood before."""
    return ROOT / f"devtools/house-adoption-prior-state-{day}.json.xz"


def read_pass(day: str) -> dict[int, str]:
    """Each record the pass of `day` moved, as that pass read it before writing, by count.

    A count two passes moved is in both archives: the earlier holds the record before
    the adoption first moved it, and the later the record as the earlier pass left it.
    """
    path = prior_state(day)
    houses.reports.ensure_private(path)
    record = houses.kernel.read_xz(path)
    if (
        type(record) is not dict
        or set(record) != {"format", "adopted_on", "cases"}
        or record["format"] != PRIOR_FORMAT
        or record["adopted_on"] != day
        or type(record["cases"]) is not list
    ):
        raise AdoptionError(f"{path.name}: not the prior state of the pass of {day}")
    rows = {}
    for row in record["cases"]:
        if type(row) is not dict or set(row) != {"n", "frontier"} or row["n"] in rows:
            raise AdoptionError(f"{path.name}: malformed or repeated row")
        rows[int(row["n"])] = str(row["frontier"])
    return rows


def read_history() -> dict[int, str]:
    """Each moved record as it stood before this adoption first moved it, by count.

    What a source this adoption displaced held: the earliest pass's text of each count.
    """
    rows: dict[int, str] = {}
    for day in passes():
        if prior_state(day).exists():
            for n, text in read_pass(day).items():
                rows.setdefault(n, text)
    return rows


def before_last_pass() -> dict[int, str]:
    """Each adopted record as it stood before the pass that last moved it, by count.

    What that pass's writer read, so a replay of it from here gives the committed record:
    a count moved twice is read from the later pass's archive, as the earlier left it.
    """
    archives = {day: read_pass(day) for day in passes() if prior_state(day).exists()}
    rows = {}
    for n in houses.ADOPTED:
        day = houses.adopted_on(n)
        if n not in archives.get(day, {}):
            raise AdoptionError(f"n={n}: the pass of {day} retained no prior state of it")
        rows[n] = archives[day][n]
    return rows


def retain_history(day: str, texts: Mapping[int, str]) -> None:
    """Retain each record's earlier text in its pass's archive before the pass writes it.

    A count already in that archive keeps the text it was retained with: a pass's prior
    state is the record before that pass first moved it, never an intermediate one, and
    a later pass retains in its own archive and never rewrites an earlier one.
    """
    path = prior_state(day)
    rows = read_pass(day) if path.exists() else {}
    added = {n: text for n, text in texts.items() if n not in rows}
    if not added:
        return
    rows.update(added)
    houses.kernel.save_xz(
        path,
        {
            "format": PRIOR_FORMAT,
            "adopted_on": day,
            "cases": [{"n": n, "frontier": rows[n]} for n in sorted(rows)],
        },
    )


# ------------------------------------------------------------------------- redrafting

LOWER_LANES = ("reported_lower_bound", "verified_lower_bound", "reported_status", "status")
LOWER_SECTION = r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)"


def with_lane(text: str, key: str, value: Any) -> str:
    """The record with `packing.<key>` replaced and every other line as it was."""
    fence, front, rest = _split(text)
    return fence + _replace(front, key, value) + rest


def holds(n: int, text: str) -> bool:
    """Whether the record names this adoption's source as the house at its count."""
    if n not in houses.ADOPTED:
        return False
    upper = _packing(_split(text)[1])["reported_upper_bound"]
    return upper.get("source_key") == houses.source_for(n).key


# ------------------------------------------------------------------------- held notes


#: The opening words of the dated paragraph a held count's record carries under its title
#: where no pass houses the count (`held_note`).
HELD_OPENING = "**Held for the owner, "


def held_at(n: int, case: select_houses.Case) -> tuple[select_houses.Candidate, ...]:
    """The rational certificates of lifted holds (`select_houses.LIFTED`) below the case at
    `n`: what the record's held note says, as the rule of 15 October wrote it."""
    entries = [e for e in select_houses.load_results() if str(e["id"]) in select_houses.LIFTED]
    found = select_houses.candidates(entries, select_houses.load_evidence()).get(n, [])
    return tuple(
        sorted(
            (c for c in found if not c.algebraic and c.side < case.verified),
            key=select_houses.precedence,
        )
    )


def _paragraphs(body: str) -> tuple[str, list[str]]:
    title, _, rest = body.partition("\n\n")
    return title, rest.split("\n\n")


def held_note(n: int, text: str) -> str:
    """The record with its held note, where a held result is below a case no pass houses.

    The note is a dated paragraph under the title, after the paragraphs that lead it
    (`apply_closed_form.LEADS` and the closed form's own), which says what
    `held_sentences` says in a certificate section, and the held certificates' evidence
    joins the case's roster. A note whose words are already these is kept as it is
    wrapped; a note no held result supports is dropped. An adopted record is returned as
    it is: its certificate section says it (`section`).
    """
    if n in houses.ADOPTED:
        return text
    fence, front, rest = _split(text)
    held = held_at(n, select_houses.parse_case(n, text))
    closing, body = rest[:4], rest[4:]
    title, parts = _paragraphs(body)
    mine = [i for i, part in enumerate(parts) if part.startswith(HELD_OPENING)]
    if len(mine) > 1:
        raise AdoptionError(f"n={n} holds {len(mine)} held notes")
    kept = [part for i, part in enumerate(parts) if i not in mine]
    if held:
        since = min(select_houses.LIFTED[c.result].since for c in held)
        until = max(select_houses.LIFTED[c.result].until for c in held)
        verified = select_houses.parse_case(n, text).verified
        sentences = [
            *held_sentences(
                held, verified, below="this case’s verified ceiling", keeps="its house"
            ),
            *staged_sentences(
                n,
                verified,
                named={c.result for c in held},
                below="this case’s verified ceiling",
                keeps="its house",
            ),
        ]
        written = f"{HELD_OPENING}{words(since)}; lifted {words(until)}.** " + " ".join(
            sentences
        )
        if mine and " ".join(parts[mine[0]].split()) == written:
            written = parts[mine[0]]
        else:
            written = closed_form.formatted(written)
        place = 0
        while place < len(kept) and kept[place].startswith(
            (*closed_form.LEADS, *closed_form.OPENINGS)
        ):
            place += 1
        kept.insert(place, written)
        roster = [e for c in held for e in (*c.report_evidence, *c.confirming_evidence)]
        cited = set(_packing(front).get("evidence") or ())
        front = _append(front, "evidence", [e for e in dict.fromkeys(roster) if e not in cited])
    return fence + front + closing + title + "\n\n" + "\n\n".join(kept)


def carries_held_note(text: str) -> bool:
    """Whether a record carries a held note, which a redraft of it must carry too."""
    return any(part.startswith(HELD_OPENING) for part in _paragraphs(_split(text)[2][4:])[1])


def held_counts() -> list[int]:
    """The counts no pass houses where a lifted hold's result is below the case, or a note
    stands."""
    entries = [e for e in select_houses.load_results() if str(e["id"]) in select_houses.LIFTED]
    reached = {n for entry in entries for n in select_houses.scope_values(dict(entry["scope"]))}
    noted = {
        int(path.stem.removeprefix("n-"))
        for path in FRONTIER.glob("n-[0-9][0-9][0-9].md")
        if HELD_OPENING in path.read_text(encoding="utf-8")
    }
    return sorted(
        n
        for n in reached | noted
        if n not in houses.ADOPTED and select_houses.case_path(n).exists()
    )


# ------------------------------------------------------------------------- refreshing


def recorded_days() -> dict[int, str]:
    """The day each record this adoption owns was last written: its last pass's, or, for a
    record no pass houses that carries a held note, the day of the hold it names. The
    replays and checks here select as each record was written
    (`select_houses.select(recorded=...)`)."""
    days = {n: houses.adopted_on(n) for n in houses.ADOPTED}
    first = min((hold.since for hold in select_houses.LIFTED.values()), default=None)
    if first is not None:
        days.update({n: first for n in held_counts() if n not in days})
    return days


def replay_plan() -> list[Move]:
    """Each adopted count's last pass planned again from the record as that pass read it."""
    latest = before_last_pass()
    days = recorded_days()
    current = select_houses.select(recorded=days)
    cases = {
        n: select_houses.parse_case(n, latest[n]) if n in latest else selection.case
        for n, selection in current.items()
    }
    return plan(select_houses.select(cases=cases, recorded=days), texts=latest)


def replayed_text(move: Move) -> str:
    """What the move's pass writes now, with the closed form, which ran after the earliest
    passes and before the later ones, laid over it as the last layer, as it is laid over
    the records."""
    return closed_form.replay(move.n, rewrite(move))


def _span(text: str, start: str, end: str) -> tuple[int, int]:
    found = text.rindex(start)
    return found, text.index(end, found)


def refreshed_opening(move: Move, committed: str) -> str:
    """Replace only this pass's dated opening; preserve every other writer's bytes."""
    start, end = _span(committed, f"\n**House adoption, {day_words(move.n)}.**", "\n\n")
    paragraph = "\n" + opening(move)
    if _flat(committed[start:end]) == _flat(paragraph):
        return committed
    return committed[:start] + paragraph + committed[end:]


def refreshed(move: Move, committed: str) -> str:
    """The committed record with what its last pass's writer writes now in the parts the
    writer alone owns: the evidence roster, priority notes, the dated paragraph and the
    certificate section, and, outside `HAND_MARKED`, the rest of the body, marked as history.
    The rest, the verifier table and the front matter other tools refresh, stays as it
    is."""
    written = replayed_text(move)
    fence, front, rest = _split(committed)
    packing = _packing(_split(written)[1])
    current = _packing(front)
    if any(
        _named_lower(current.get(key)) != _named_lower(packing.get(key))
        for key in ("reported_lower_bound", "verified_lower_bound")
    ):
        raise AdoptionError(
            f"n={move.n}: full refresh refuses a later lower-bound layer; "
            "use --refresh-openings for an opening-only correction, or reconcile "
            "the later writer's evidence and prose explicitly"
        )
    for key in ("evidence", "priority_notes"):
        if _packing(front).get(key) != packing.get(key):
            front = _replace(front, key, packing[key])
    if move.n not in HAND_MARKED:
        rest = _with_history(rest, _split(written)[2])
    text = fence + front + rest
    for start, end in (
        (f"\n**House adoption, {day_words(move.n)}.**", "\n\n"),
        (f"\n## {_title(move)}\n", FOOTER),
    ):
        a, b = _span(text, start, end)
        c, d = _span(written, start, end)
        if _flat(text[a:b]) != _flat(written[c:d]):
            text = text[:a] + written[c:d] + text[b:]
    return text


def _flat(text: str) -> str:
    return " ".join(text.split())


def history_words(body: str) -> str:
    """A body as the writer is answerable for it: flowmark's wrapping and escapes undone
    and the verifier table left out."""
    return _flat(VERIFIER_TABLE.sub("", body).replace("\\+", "+"))


def _with_history(committed: str, written: str) -> str:
    """The written body where its words differ from the committed one's, with the
    committed verifier table in place of the written one."""
    if history_words(committed) == history_words(written):
        return committed
    table = VERIFIER_TABLE.search(committed)
    if table is None:
        return written
    return VERIFIER_TABLE.sub(lambda _match: table.group(), written, count=1)


def refresh(
    *, write: bool, openings_only: bool = False, counts: Collection[int] | None = None
) -> list[int]:
    """Every record whose writer-owned text, or held note, differs from what the writer
    writes now, by count; written where `write`. Whitespace is the formatter's.

    `counts`, where given, limits the refresh to those records: a writer change at a few
    counts is applied without replaying a count whose later lower layer the full refresh
    refuses, as n = 108's fine-net lower bound is (review A1 of #692). Both refreshes also
    bring each adopted count's selected override reason in the coverage register to
    `override_reason`, which no later writer edits (review B1 of #704)."""
    changed = []
    updates: list[tuple[Path, str]] = []
    for move in replay_plan():
        if counts is not None and move.n not in counts:
            continue
        path = select_houses.case_path(move.n)
        committed = path.read_text(encoding="utf-8")
        text = (
            refreshed_opening(move, committed) if openings_only else refreshed(move, committed)
        )
        if _flat(text) != _flat(committed):
            changed.append(move.n)
            updates.append((path, text))
    if not openings_only:
        for n in held_counts():
            if counts is not None and n not in counts:
                continue
            path = select_houses.case_path(n)
            committed = path.read_text(encoding="utf-8")
            text = held_note(n, committed)
            if _flat(text) != _flat(committed):
                changed.append(n)
                updates.append((path, text))
    covered, reasons = reworded(COVERAGE.read_text(encoding="utf-8"), counts)
    if reasons:
        changed.extend(reasons)
        updates.append((COVERAGE, covered))
    # Plan every record before the first write: a refused later layer must leave the
    # whole batch intact, including earlier records with legitimate pending changes.
    if write:
        for path, text in updates:
            _write(path, text)
    return sorted(set(changed))


def adopt_case(n: int, existing: str, generated: str) -> str:
    """The generator's redraft of an adopted case: the house stays, lower lanes are drafted.

    `generate_frontier_case` drafts a case from the catalogue and the sources it reads and
    hands the draft here with the record. An adopted case keeps its upper lanes, its prose
    and its history from the record, each upper lane held to the exact side its certificate
    rebuilds; the ordinary lower lanes, the status and the lower-bound section are the
    draft's. A record no longer at this adoption's source is the draft's entirely.
    """
    if not holds(n, existing):
        return generated
    opening_fence, front, rest = _split(existing)
    packing = _packing(front)
    source = houses.source_for(n)
    side = houses.side(n)
    for lane in ("reported_upper_bound", "verified_upper_bound"):
        if Fraction(str(packing[lane].get("exact_form"))) != side:
            raise AdoptionError(f"n={n}: the {lane} is not {source.result}'s exact side")
    _, draft_front, draft_rest = _split(generated)
    draft = _packing(draft_front)
    for key in LOWER_LANES:
        if key in draft and draft[key] != packing.get(key):
            front = _replace(front, key, draft[key])
    drafted = re.search(LOWER_SECTION, draft_rest, re.DOTALL)
    if drafted is not None:
        rest = re.sub(
            LOWER_SECTION, lambda _match: drafted.group(), rest, count=1, flags=re.DOTALL
        )
    return opening_fence + front + rest


def _write(path: Path, text: str) -> bool:
    if path.read_text(encoding="utf-8") == text:
        return False
    with atomic_output_file(path) as temporary:
        temporary.write_text(text, encoding="utf-8")
    return True


def write(moves: Sequence[Move]) -> list[int]:
    """Write every move, so that a run stopped part-way is finished by running it again.

    Every text is computed before any file is written, so a move the tool refuses writes
    nothing. The case records are written last, since `plan` reads them: a rerun after an
    interruption plans exactly the records not yet written, and the prior state, coverage
    register and deferrals written before them are already what that rerun computes.
    """
    pending = [move for move in moves if not adopted(move)]
    rewritten = {move.n: rewrite(move) for move in pending}
    register = COVERAGE.read_text(encoding="utf-8")
    covered = coverage(pending, register) if pending else register
    deferred = deferrals(DEFERRALS.read_text(encoding="utf-8"), _cited(rewritten))
    for day in sorted({houses.adopted_on(move.n) for move in pending}):
        retain_history(
            day, {move.n: move.text for move in pending if houses.adopted_on(move.n) == day}
        )
    _write(COVERAGE, covered)
    _write(DEFERRALS, deferred)
    for move in pending:
        _write(select_houses.case_path(move.n), rewritten[move.n])
    return [move.n for move in pending]


def check() -> list[str]:
    """Every count `upper_bound_houses` draws is at its house in the case and coverage."""
    problems = []
    coverage_data = safe_load(COVERAGE.read_text(encoding="utf-8"))
    sources = {str(s["id"]): s for s in coverage_data["sources"]}
    overrides = {int(e["n"]): e for e in coverage_data["selected_overrides"]}
    for n, result in sorted(houses.ADOPTED.items()):
        packing = _packing(_split(select_houses.case_path(n).read_text(encoding="utf-8"))[1])
        side = houses.side(n)
        source = houses.source_for(n)
        upper, verified = packing["reported_upper_bound"], packing["verified_upper_bound"]
        if upper.get("source_key") != source.key:
            problems.append(f"n={n}: reported source is not {result}'s {source.key}")
        for lane, bound in (("reported", upper), ("verified", verified)):
            if Fraction(str(bound.get("exact_form"))) != side:
                problems.append(f"n={n}: the {lane} exact form is not {result}'s exact side")
            if not printed_at(bound["value"], side):
                problems.append(f"n={n}: the {lane} value is not the side, exact or rounded up")
        override = overrides.get(n)
        if override is None or sources[override["source_id"]]["source_key"] != source.key:
            problems.append(f"n={n}: the coverage register does not select {source.key}")
        elif override.get("reason") != override_reason(n, result):
            problems.append(
                f"n={n}: the selected override's reason is not what the writer writes "
                "(`--refresh-openings` rewrites it)"
            )
    for n in held_counts():
        text = select_houses.case_path(n).read_text(encoding="utf-8")
        if _flat(held_note(n, text)) != _flat(text):
            problems.append(f"n={n}: the held note is not what the held results say")
    return problems


#: Where the steps that follow a new house are written (think-g3q7).
WITNESS_CHANGES = 'docs/project/guides/regularization-process.md, "When a Witness Changes"'
#: Where the intake runbook schedules those steps and their compute.
INTAKE_STEP = 'packing/campaign/result-import.md, "Adopt a House, Then Regularize It"'
#: Both strong generators and the selection on one re-housed count, in CPU-minutes, as the
#: regularization audit of 15 October 2026 read the layer's run receipts (think-sfas):
#: Evan Daniel's driver 140 to 220 CPU-seconds a count, grid-slack 37 to 110 at each of
#: its three thresholds, and the selection seconds to about four minutes for each of the
#: count's four candidate views (review A7 of #641). No receipt yet measures the selection
#: on a new witness, so the upper end is the guide's largest view taken four times.
REGULARIZE_CPU_MINUTES = (5, 25)
#: The workers the printed commands give the driver and the selection, as the guide's
#: examples do: what a shared host can spare, which the reader sets (review B3 of #641).
WORKERS = 2
#: The base branch's record as the file `default_drawings --compare` reads, in a shell
#: (review C4 of #641), for a pull request on main; a stacked one names its own base, as
#: the runbook and the guide say (review D2).
BASE_RECORD = f"`<(git show origin/main:{default_drawings.RECORD_PATH})`"
STACKED_BASE = "with a stacked pull request's base branch for main"
#: What the runbook, the guide and this printout say of every count an adoption re-houses,
#: in one wording (reviews C4, D1 and E1 of #641): the owner's rule is to adopt the
#: smallest packing and then regularize it, so the count's runs are owed in the adoption's
#: pull request (`default_drawings.RUNS_OWED`), and an adoption whose runs do not fit under
#: the pass's compute cap waits with them, staged in `select_houses.PENDING_ADOPTION`.
NEVER_DEFERRED = "never deferred to default_drawings.PENDING_ALLOWED"
#: What follows a write, as `python -m devtools.` commands from `packing/` with `{n}` the
#: re-housed counts: the new witness, the axis tool's view of it, and each count's state.
REFRESH_COMMANDS = (
    "build_known_best_atlas --update",
    "regularize_axis_components --update-atlas --n {n}",
    "default_drawings --update",
)
#: The strong runs' directories under `$RUNS`, each with the prefix the layer gives its
#: run id: a run is recorded as its directory's name after `grid-slack-`
#: (`regularize_grid_slack.admitted_views`) or `evand-regularize-`
#: (`regularize_evand.evand_candidates`), and admitting a run whose id the index already
#: holds replaces that run's block, its cost and decisions, under the views that name it
#: (review B2 of #641). So each name starts with a label no run in the index has, and
#: that names the re-housed counts, so that two adoptions in flight on one day print
#: different names (`run_label`, review C3 of #641).
RUN_DIRECTORIES = {
    "grid05": ("grid-slack", "{label}-grid-0.5"),
    "grid1": ("grid-slack", "{label}-grid-1"),
    "grid5": ("grid-slack", "{label}-grid-5"),
    "evand": ("evand-regularize", "{label}-evand"),
}
#: Then the strong generators on each pending count, grid-slack at its three thresholds
#: and Evan Daniel's driver, and the selection, which prints the `layer` commands.
STRONG_COMMANDS = (
    "regularize_grid_slack --n {n} --run-dir $RUNS/{grid05}",
    "regularize_grid_slack --n {n} --run-dir $RUNS/{grid1} --near-axis-degrees 1",
    "regularize_grid_slack --n {n} --run-dir $RUNS/{grid5} --near-axis-degrees 5",
    "regularize_evand run --run-dir $RUNS/{evand} --n {n} --workers $WORKERS",
    (
        "regularize_select --evand-run $RUNS/{evand} --grid-run $RUNS/{grid05} "
        "$RUNS/{grid1} $RUNS/{grid5} --workers $WORKERS "
        "--output $RUNS/{label}-selection.json --markdown $RUNS/{label}-selection.md"
    ),
)


def run_ids(label: str) -> dict[str, str]:
    """The run id each strong run under `label` gives the layer, by its directory's key."""
    return {
        key: f"{prefix}-{directory.format(label=label)}"
        for key, (prefix, directory) in RUN_DIRECTORIES.items()
    }


def run_label(day: str, counts: Sequence[int], index: Path = default_drawings.INDEX) -> str:
    """A label for an adoption's strong runs that gives no run an id the layer's index
    already has (review B2 of #641), and that names the re-housed counts by the lowest and
    the highest: `adopt-<day>-n176`, `adopt-<day>-n105-304`, or the same with `-b`, `-c`
    and on where an earlier run took it. The index holds only the runs merged into the
    branch, so two adoptions opened on one day would otherwise print the same ids and the
    second to admit would replace the first's block; two adoptions that re-house the same
    count already conflict on its case record (review C3 of #641)."""
    if not counts:
        raise ValueError("an adoption's run label names the counts it re-houses")
    low, high = min(counts), max(counts)
    named = f"adopt-{day}-n{low}" if low == high else f"adopt-{day}-n{low}-{high}"
    document = json.loads(index.read_text(encoding="utf-8"))
    taken = {str(run.get("id")) for run in document.get("runs") or []}
    for suffix in ("", *(f"-{letter}" for letter in "bcdefghijklmnopqrstuvwxyz")):
        label = f"{named}{suffix}"
        if not taken & set(run_ids(label).values()):
            return label
    raise SystemExit(f"every {named} run label is taken in {index}")


def _plural(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def _cost(certain: int, every: int) -> str:
    """The strong runs' cost, from the counts certain to be pending to all re-housed."""
    low, high = REGULARIZE_CPU_MINUTES
    each = f"{low} to {high} CPU-minutes a count for both strong generators and the selection"
    if certain == every:
        return f"{each}, {low * every} to {high * every} for these"
    if not certain:
        return f"{each}, up to {low * every} to {high * every} for all {every}"
    return (
        f"{each}, {low * certain} to {high * certain} for the {certain} certain to be "
        f"pending, up to {low * every} to {high * every} for all {every}"
    )


def regularization_owed(
    counts: Sequence[int],
    *,
    index: Path = default_drawings.INDEX,
    allowed: Mapping[int, str] | None = None,
    settled: Mapping[int, object] | None = None,
    day: str | None = None,
) -> list[str]:
    """What re-housing `counts` owes the regularized layer, as the lines `main` prints.

    A new house is a new witness: the layer's view of the count lapses with it, and the
    count reads `pending` in `default-drawings.json` until the strong generators decide the
    new witness, unless the new house drawing has no uneven and no near-axis square, no
    strong view of the count has lapsed, and `PENDING_ALLOWED` does not hold it for its
    bead's runs (`default_drawings.count_state`). Read from the committed index before the
    atlas is refreshed, this names the counts certain to be pending, one count a line, and
    a `SETTLED` decision the new witness voids, then gives the commands, with run
    directories named for `day` (the adoption's, by default) and the counts, that no run
    in the index has (`run_label`), what they cost, and what the adoption's pull request
    owes: the drawings before and after, and every re-housed count's runs, none deferred.
    It measures and runs nothing: the runs take minutes a count, and the pass prices them
    as one validation item under its compute cap (`INTAKE_STEP`).
    """
    if not counts:
        return []
    allowed = default_drawings.PENDING_ALLOWED if allowed is None else allowed
    settled = default_drawings.SETTLED if settled is None else settled
    if day is None:
        days = [houses.adopted_on(n) for n in counts if n in houses.ADOPTED]
        day = max(days, default=datetime.now(UTC).date().isoformat())
    label = run_label(day, counts, index)
    entries = default_drawings.index_entries(index)
    spaced = " ".join(map(str, counts))
    certain: list[str] = []
    unless: list[str] = []
    for n in counts:
        entry = entries.get(n, {})
        lapse = entry.get(default_drawings.LAPSED)
        why: list[str] = []
        if entry.get("generator") in default_drawings.STRONG_GENERATORS:
            why.append(f"its {entry['generator']} view lapses")
        elif lapse:
            why.append(f"a {lapse['generator']} view lapsed earlier")
        if n in allowed:
            bead = default_drawings.BEAD.match(allowed[n])
            holder = bead[0] if bead else repr(allowed[n])
            why.append(
                f"PENDING_ALLOWED holds it for {holder}'s runs, whatever the new house "
                "reads: they run here, on the new witness, and the entry comes off"
            )
        if why:
            certain.append(f"    {n}: {'; '.join(why)}")
        else:
            unless.append(str(n))
    lines = [
        (
            f"regularization owed: {_plural(len(counts), 're-housed count')}, {spaced} "
            f"({WITNESS_CHANGES})"
        )
    ]
    if certain:
        lines.append("  pending until the strong generators decide the new witness:")
        lines.extend(certain)
    if unless:
        lines.append(
            "  pending unless the new house drawing has no uneven and no near-axis square: "
            + " ".join(unless)
        )
    lines.extend(
        f"  n={n}: SETTLED was decided on the earlier witness; decide the new one and settle "
        "it again, or take it off"
        for n in counts
        if n in settled
    )
    lines.append(
        f"  cost: {_cost(len(certain), len(counts))}; one validation item under the pass's "
        f"compute cap ({INTAKE_STEP})"
    )
    lines.append(
        "  from packing/, in one shell, each python command after `uv run --frozen "
        "--all-extras --group dev`; RUNS is outside the checkout, WORKERS what the host can "
        "spare:"
    )
    lines.append(f"    RUNS=/tmp/regularize WORKERS={WORKERS}")
    lines.extend(f"    python -m devtools.{line.format(n=spaced)}" for line in REFRESH_COMMANDS)
    lines.append(
        "  then on each count `default_drawings --check-state` names pending (these, less any "
        "it reads regular), in run directories no run in the index has named:"
    )
    directories = {
        key: directory.format(label=label)
        for key, (_prefix, directory) in RUN_DIRECTORIES.items()
    }
    lines.extend(
        f"    python -m devtools.{line.format(n=spaced, label=label, **directories)}"
        for line in STRONG_COMMANDS
    )
    lines.append(
        "  and the `layer` commands it prints, then the guide's step 5 (render and record)."
    )
    lines.append(
        "  List each re-housed count's drawing before and after in this pull request "
        f"(`default_drawings --compare` with the base branch's record, {BASE_RECORD}, "
        f"{STACKED_BASE}); where {default_drawings.STRONG_VIEW_LOST}, it names those goals "
        f"and marks each such count still pending: {default_drawings.RUNS_OWED}."
    )
    lines.append(
        f"  A re-housed count is {NEVER_DEFERRED}: where the runs do not fit under the "
        "pass's compute cap, stage the counts they do not cover in "
        "select_houses.PENDING_ADOPTION with the open bead that adopts them, and adopt the "
        "rest. `python -m devtools.default_drawings --check-state` fails until the runs "
        "decide every re-housed count, and while the list defers the runs of a witness "
        "whose house has moved since."
    )
    return lines


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="list the moves, write nothing")
    mode.add_argument("--check", action="store_true", help="hold adopted cases to their houses")
    mode.add_argument(
        "--refresh", action="store_true", help="write what each record's writer writes now"
    )
    mode.add_argument(
        "--refresh-openings",
        action="store_true",
        help=(
            "refresh only current adoption paragraphs and override reasons, retaining all "
            "other writers' bytes"
        ),
    )
    parser.add_argument(
        "--n",
        type=int,
        nargs="+",
        metavar="N",
        help="with --refresh or --refresh-openings, refresh only these records",
    )
    arguments = parser.parse_args(argv)
    if arguments.n and not (arguments.refresh or arguments.refresh_openings):
        parser.error("--n needs --refresh or --refresh-openings")
    if arguments.refresh or arguments.refresh_openings:
        try:
            changed = refresh(
                write=True,
                openings_only=arguments.refresh_openings,
                counts=frozenset(arguments.n) if arguments.n else None,
            )
        except AdoptionError as error:
            print(f"FAIL {error}")
            return 1
        print(f"refreshed {len(changed)} records: {', '.join(map(str, changed)) or 'none'}")
        return 0
    if arguments.check:
        problems = check()
        for problem in problems:
            print(f"FAIL {problem}")
        if problems:
            return 1
        print(f"OK: {len(houses.ADOPTED)} adopted cases are at their houses")
        return 0
    moves = plan()
    if arguments.dry_run:
        for move in moves:
            print(f"n={move.n}: {move.house.result} {select_houses.ceiling(move.house.side)}")
        for line in regularization_owed([move.n for move in moves if not adopted(move)]):
            print(line)
        return 0
    written = write(moves)
    print(f"adopted {len(written)} houses: {', '.join(map(str, written)) or 'none'}")
    for line in regularization_owed(written):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
