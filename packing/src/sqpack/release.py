"""Independent public editions for the site, the infographic pair and each paper.

Site editions are retired as of 22 October 2026 (the owner; think-wdqo): "We don't have
any real value in committing a synthetic version for the site." The site deploys
continuously from `main`. `PUBLICATION_HISTORY` is kept as history, the record of the
site editions that were published, and is frozen together with `PUBLICATION_REVISION`,
the commit the claim documents link to: `devtools.check_release_impact` refuses an edit
to either, and `devtools.cut_release --component site` refuses to cut. The papers and
the art, the infographic posters and the films, keep their versions. Until the footer
names the deployed commit, the site's pages print the frozen edition with the data pin.

`PUBLICATION_EDITION` stamps the site's footer and workbench. The infographic family
has its own `INFOGRAPHIC_HISTORY` and `INFOGRAPHIC_VERSION`; its two SVGs, PDFs and PNG
exports carry one shared semantic core plus their derivation revision. Every paper
retains its own history, draft status and dates, with no site edition or data suffix.
The Python package version in `pyproject.toml` is separate from these public editions.

1. `DATA_REVISION` pins the last commit changing `DATA_PATHS`. Rendering never reads
   Git, so shallow deploys stamp the same edition as a complete checkout. Where Git
   can answer, `test_release` holds the pin to `data_revision()`. A data commit is
   followed by a one-line `release_pin --update` commit; re-pinning rebuilds nothing.
2. Drawn assets record the data commit and date they show. They keep those facts when
   the pin advances. The atlas posters formerly printed the pin, causing thirty
   re-pins to rewrite 13.6 MB of assets each without changing a card. Derivation
   receipts bind each PDF and PNG to its SVG independently of its edition.
3. An untouched poster may trail current data (`COMPOSITES_MAY_TRAIL`). Claims on a
   poster naming the current data must agree with the current record. Both posters
   must carry the current infographic version; a site cut moves neither.
4. A reader-visible infographic revision requires the family's patch or minor
   successor and rebuilds both complete export families. Changing a drawing under
   its existing semantic version is refused before any output is written. A
   byte-identical rebuild creates no edition.
5. Public component cuts retain their delivered impact and reason in `RELEASE_IMPACTS`.
   Patch covers corrections and ordinary refreshes; minor covers substantial new
   scope or capability and resets patch to zero. One component gets one bump for its
   complete batch, with minor winning if both apply. Internal work creates no edition.
6. Re-pins and drawn artifacts are excluded from the data paths, preventing a stamp
   from chasing the hash of its own redraw. Existing published history entries keep
   their numbers and publication dates; no impact decision is invented for old cuts.
"""

from __future__ import annotations

import ast
import re
import subprocess
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Literal, NamedTuple


class PublicationHistoryEntry(NamedTuple):
    """One public edition, when it was first published, and what it changed: an edition
    of the site and its data in `PUBLICATION_HISTORY`, or of one paper in that paper's
    own history."""

    version: str
    first_published: str
    result_scope: str


#: FROZEN since 22 October 2026, when site editions were retired (the owner; think-wdqo).
#: It is kept as the record of the site editions that were published: no entry is added,
#: removed or redated, and `devtools.check_release_impact` refuses an edit to it.
#:
#: Every edition this publication, the site and its data, has had, newest first, and NONE
#: is ever removed. It is the site's record: its pages and workbench are stamped from
#: it, the claim documents were regenerated at each entry, and `development.md` (Cutting
#: an edition) is where a reader finds it. It is not a paper's history: a paper lists its
#: own editions (`EXPLAINER_HISTORY`, below), which are the ones in which that paper
#: changed. Until 2026-10-02 the explainer listed this whole record and called it its
#: version history, so a site-only edition read as an edition of the paper.
#:
#: It used to be "the two editions retained in the explainer's short public history", and
#: under that rule adding v0.4.1 on 2026-09-22 dropped v0.3.0 -- the first edition, and the
#: proof of s(11) >= 381/100 the whole publication began with. A history that keeps the
#: last two is a changelog of the last two; a reader who wants to know when the result was
#: first put in front of anyone needs the first one most. `test_release` holds the list to
#: its oldest entry being that edition.
#:
#: Dates are when each edition's content was **first published** -- first live on the
#: public page -- read from the repository's GitHub Pages deployments, in UTC. They used to
#: be when each version *label* first appeared in Git, which is a different date whenever
#: an edition went live before it was named or was named before it went live, and both
#: happened (the owner, 2026-09-22: "accurately record the date of when that was first
#: published"). The deployment and commit behind each date, so it can be re-read:
#:
#:   v0.7.11 2026-10-16T01:25:34Z  bbc12b617  the merge of PR 631, the top of stack 632 (PR
#:                                            627 cut it); dated October 15 when cut, it went
#:                                            live the next day in UTC (think-tk0u)
#:   v0.5.0  2026-10-02T01:07:03Z  8aaa411dc  the merge of PR 291, label and content together
#:   v0.4.2  2026-09-28T06:11:35Z  c19e6c0e2  the merge of PR 239, label and content together
#:   v0.4.1  2026-09-22T23:12:36Z  d5b1c2e1b  the merge of PR 218, label and content together
#:   v0.4.0  2026-09-13T22:12:47Z  f2e24e07b  T-025's 191/50 and the v0.4.0 label first live;
#:                                            the label was cut on a branch on September 10
#:   v0.3.0  2026-09-05T08:06:30Z  f060b1d78  the first Pages deployment of all, headlining
#:                                            s(11) >= 381/100; "v0.3.0" was only put on it
#:                                            on September 8 (`ce3b1ab56`)
#:
#: Reproduce with `gh api "repos/jlevy/squares/deployments?environment=github-pages"` and,
#: for each deployment's commit, what the page it built stated.
PUBLICATION_HISTORY = (
    PublicationHistoryEntry(
        version="v0.9.2",
        first_published="October 22, 2026",
        result_scope=(
            "Record Mykhailo Polkovskyi's #719 re-solves of the house packings at 105 and "
            "204 as T-229, pending review and adoption, and his 111 rows beyond the "
            "corpus at or below 1024 as current beyond-horizon rows, superseding the rows "
            "that stood at those counts; record the replies after #720."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.9.1",
        first_published="October 22, 2026",
        result_scope=(
            "Publish canonical website addresses at squaremath.org while retaining GitHub "
            "repository citations."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.9.0",
        first_published="October 22, 2026",
        result_scope=(
            "Add person profiles and reviewed credit links, with direct profile "
            "navigation and shared article popovers for complete case and result records."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.20",
        first_published="October 22, 2026",
        result_scope=(
            "Record the beyond-horizon rows of four older reports, Joost de Winter's #666 "
            "at or below 1024 and Francisco Couzo's #670, #672 and #675, as 205 dated "
            "rows of which 8 of #670's become current, and record the replies after #718 "
            "and #643's acknowledgement."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.19",
        first_published="October 22, 2026",
        result_scope=(
            "Raise Evan Daniel's regularized views (T-225) to V3/C3 after their stage 4 "
            "review, adopt them as the house best packings at 204, 227, 229 and 260, and "
            "register Francisco Couzo's #670, #672 and #675 rows (T-226 to T-228)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.18",
        first_published="October 22, 2026",
        result_scope=(
            "Record Francisco Couzo's 109 new upper bounds at or below 1024 from issue "
            "715 as current beyond-horizon rows, superseding the rows that stood at those "
            "counts, and record the #715 acknowledgement and the #678 follow-up."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.17",
        first_published="October 22, 2026",
        result_scope=(
            "Register Evan Daniel's solved and regularized views at 204, 227, 229 and 260 "
            "(T-225, V0/C0); record the #668 and #702 replies, #678's stage 7 reply and "
            "#668's follow-up; enter #715 at triage; correct the overview's Couzo and de "
            "Winter cards; and announce T-196's and T-223's adoptions in the News."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.16",
        first_published="October 21, 2026",
        result_scope=(
            "Raise Francisco Couzo's n204 and n260 certificates (T-223) to V3/C3 on their "
            "stage 4 review and adopt them as the house best packings at 204 and at 260, "
            "where T-223 replaces T-196, with the strong generators' drawings."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.15",
        first_published="October 21, 2026",
        result_scope=(
            "Raise Joost de Winter's T-196 (#668) at 227, 229 and 260 to V3/C3 on the "
            "integrated exact replay and its stage 4 review, and adopt it as the house "
            "best packing at 227 and 260 with Evan Daniel's regularized views."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.14",
        first_published="October 21, 2026",
        result_scope=(
            "Record Evan Daniel's s(343) certificate of issue 702 as the current "
            "beyond-horizon row at 343, superseding issue 678's row there."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.13",
        first_published="October 21, 2026",
        result_scope="Name the 20 October review in the lineages at 154 and 308.",
    ),
    PublicationHistoryEntry(
        version="v0.8.12",
        first_published="October 21, 2026",
        result_scope=(
            "Record Darius Muglich's 100 reported upper bounds at 328 to 998 (#686) as "
            "beyond-horizon rows, superseding the rows they beat, with the issue's card."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.11",
        first_published="October 21, 2026",
        result_scope=(
            "Correct T-224's significance wording, give the 270 credit sentence the "
            "design's composition, and name the 21 October review as where T-224 was "
            "measured."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.10",
        first_published="October 21, 2026",
        result_scope=(
            "Raise Evan Daniel's n270 certificate (T-224) to V3/C3 on its stage 4 review "
            "and adopt it as the house best packing at 270, with its regularized drawing."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.9",
        first_published="October 21, 2026",
        result_scope=(
            "Credit Evan Daniel as finder at 271 as issue 664 asks, cite his answer on "
            "the regularized views' by field, and correct T-221's tilt count and the "
            "house best packing wording at 154 and 308."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.8",
        first_published="October 21, 2026",
        result_scope=(
            "Register Francisco Couzo's reported n204 and n260 certificates (T-223) at "
            "V0/C0, pending review and adoption, and his 83 beyond-horizon rows."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.7",
        first_published="October 20, 2026",
        result_scope=(
            "The synopsis defines the house best packing, and the conventions write house "
            "only as a modifier."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.6",
        first_published="October 20, 2026",
        result_scope=(
            "Register, confirm and adopt Evan Daniel's n308 and n154 certificates (T-221, "
            "T-222): raised to V3/C3 by the 20 October review, adopted as the house best "
            "packings at 308 and 154, and regularized."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.5",
        first_published="October 20, 2026",
        result_scope=(
            "Announce Evan Daniel's sub-grid n183 packing (T-220) in News and list the 20 "
            "October report-order ledger in the synopsis."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.4",
        first_published="October 20, 2026",
        result_scope=(
            "Register Evan Daniel's sub-grid n183 certificate (T-220), adopt it as the "
            "n183 house and draw its regularized view."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.3",
        first_published="October 20, 2026",
        result_scope=(
            "Register Evan Daniel's n236 and n271 packings (T-218, T-219), raise T-197 to "
            "T-199 to V3/C3, adopt his certificates as the houses at 155, 229, 236 and "
            "271, and correct the credit at 146 and 308."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.2",
        first_published="October 20, 2026",
        result_scope=(
            "The development guide describes how test sessions keep their temporary "
            "directories bounded."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.1",
        first_published="October 20, 2026",
        result_scope=(
            "Confirm the n68, n84 and n85 fine-net lower bounds T-205 to T-207 at V3/C3 "
            "from retained complete captures, whole-net controls and mapped reviews."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.8.0",
        first_published="October 20, 2026",
        result_scope=(
            "Open the results page on what was added in the last seven days, day by day, "
            "above the weekly rollup, with an Added filter on the table."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.35",
        first_published="October 19, 2026",
        result_scope=(
            "Simplify the News filters and chooser states, explain News significance "
            "scores in tooltips, and align News cards with the site's styling."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.34",
        first_published="October 19, 2026",
        result_scope=(
            "Map the s(19) Lean proof review onto T-194 (C1), raise T-193 to V3/C3 at its "
            "sixteen counts and stage those houses for the algebraic writer."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.33",
        first_published="October 19, 2026",
        result_scope=(
            "Count a retained formal source build toward verification rather than "
            "confirmation, moving Fitzharding's Lean proof of s(17) (T-154) from V0 to V3 "
            "while it stays at C1."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.32",
        first_published="October 19, 2026",
        result_scope=(
            "Keep Atlas grids at the available width under reduced motion during viewport "
            "changes."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.31",
        first_published="October 19, 2026",
        result_scope=(
            "Adopt T-174 at 37 rational counts with exact house custody, maintained "
            "history and regularized default drawings."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.30",
        first_published="October 19, 2026",
        result_scope=(
            "Document the cached libproc current-RSS contract and installed-SDK native "
            "assurance on macOS."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.29",
        first_published="October 19, 2026",
        result_scope=(
            "Register eighteen fine-net lower bounds, adopt the reviewed n108 bound and "
            "retain its exact audit provenance and safe packet publication."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.28",
        first_published="October 19, 2026",
        result_scope=(
            "Document the canonical Rust multiplication default and reproducible "
            "benchmark controls, and refresh the session accounting in the synopsis."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.27",
        first_published="October 18, 2026",
        result_scope=(
            "Register six upper-bound claim rows pending adoption at 155, 227, 229 and "
            "260, retain their chronological source credit, and link the October 18 intake and "
            "open-work reviews."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.26",
        first_published="October 17, 2026",
        result_scope=(
            "Adopt PingYou Ltd's tighter certificate of Thomas Schadt and David "
            "Ellsworth's 29-square packing as the house at 29, and settle its drawing as "
            "decided with no better view."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.25",
        first_published="October 17, 2026",
        result_scope=(
            "Say on the case and result pages that the house rule ended the hold on "
            "T-174's houses and RP-3's wait, naming each staged adoption's bead."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.24",
        first_published="October 17, 2026",
        result_scope=(
            "Serve the atlas posters' v0.6.2 edition, drawn at the 17 October data, and "
            "name it on the readme page."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.23",
        first_published="October 16, 2026",
        result_scope=(
            "Confirm T-185 to T-190 at V3/C3, move the houses at fifteen counts to T-186, "
            "T-187, T-188 and T-190, draw the regularized views of eleven of them, and "
            "record 176, 237, 303 and 304 as decided with no better view."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.22",
        first_published="October 16, 2026",
        result_scope="Draw the regularized views of 175, 232 and 264 by default.",
    ),
    PublicationHistoryEntry(
        version="v0.7.21",
        first_published="October 16, 2026",
        result_scope=(
            "Draw the regularized views of 153, 154, 207, 211, 237, 241 and 302 by "
            "default, and record 304 as decided with no better view."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.20",
        first_published="October 16, 2026",
        result_scope=(
            "Draw the regularized views of 105, 129, 146, 156, 176 and 271 by default, "
            "and record 204, 272 and 303 as decided with no better view."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.19",
        first_published="October 16, 2026",
        result_scope=(
            "Raise Benjamin Greff's s(76) = 9 and s(95) = 10 to V3/C1 on the intake's "
            "recorded reproductions."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.18",
        first_published="October 16, 2026",
        result_scope=(
            "List the October 16 review of Benjamin Greff's mixed covers for s(76) = 9 "
            "and s(95) = 10 in the synopsis document map."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.17",
        first_published="October 16, 2026",
        result_scope=(
            "List the October 16 review of the upper-bound imports T-185 to T-190 in the "
            "synopsis document map."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.16",
        first_published="October 16, 2026",
        result_scope=(
            "List the October 16 review of Oscar Fitzharding's Lean proof that s(19) = 3 "
            "+ 4√2/3 in the synopsis document map."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.15",
        first_published="October 16, 2026",
        result_scope=(
            "Register two results by others in report order, none adopting a house: exact "
            "algebraic sides of the best packings at sixteen counts and a reported Lean "
            "proof that s(19) = 3 + (4/3)√2."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.14",
        first_published="October 16, 2026",
        result_scope=(
            "Say on each case page whose house is drawn that it is drawn as published, and why."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.13",
        first_published="October 16, 2026",
        result_scope=(
            "Use the same canonical articles and topic chips on the homepage and News, "
            "backfill Ahmed's eleven-square optimum, and make navigation consistently "
            "sans."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.12",
        first_published="October 16, 2026",
        result_scope=(
            "Unify News topics, counts and surname style, and announce the newly "
            "registered bound reports as separate articles."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.11",
        first_published="October 16, 2026",
        result_scope=(
            "Register five results in report order, T-188 to T-192, none adopting a "
            "house: smaller reported packings of 211 and 237 squares, a reported s(95) = "
            "10, a reported lower bound for 28 squares and 267 beyond-horizon rows."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.10",
        first_published="October 15, 2026",
        result_scope=(
            "Correct News math and prose, add tutorial credits and update About and "
            "shared site headings."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.9",
        first_published="October 15, 2026",
        result_scope=(
            "Document complete selected CI coverage, scoped News validation and "
            "the distinction between timing reports and execution deadlines."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.8",
        first_published="October 15, 2026",
        result_scope=(
            "Backfill a week of News, connect PR significance labels to intake, and "
            "clarify proof credit, surname headlines and shared significance meters."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.7",
        first_published="October 15, 2026",
        result_scope=(
            "Complete tutorial launch coverage, clarify the studied counting-certificate "
            "limits and refresh the atlas and explainer downloads."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.6",
        first_published="October 15, 2026",
        result_scope=(
            "Keep routine push and component release validation focused on quick checks "
            "while preserving explicit deep checkpoints."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.5",
        first_published="October 15, 2026",
        result_scope=(
            "Unify News and Explanations headings with original publication dates, refine "
            "significance meters and filters, keep document maintenance out of News, "
            "announce the newly adopted packings, and use bundled fonts for literal "
            "mathematical code symbols."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.4",
        first_published="October 15, 2026",
        result_scope=(
            "Raise the 14 October upper-bound entries to V3/C3 on their stage 4 reviews "
            "and adopt eighteen houses, at 105, 129, 146, 153, 154, 156, 176, 204, 207, "
            "211, 237, 241, 261, 271, 272, 302, 303 and 304, with PR #574's held for the "
            "owner."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.3",
        first_published="October 15, 2026",
        result_scope=(
            "Register three results in report order, T-185 to T-187, none adopting a "
            "house, and bring the requests record and Ryan Xu's credits up to date."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.2",
        first_published="October 14, 2026",
        result_scope=(
            "Credit Ryan Xu by name across the record, record the 14 October replays and "
            "decided comparisons, and add the 13 and 14 October News entries."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.1",
        first_published="October 14, 2026",
        result_scope=(
            "Register 24 results from the 14 October intake, none adopting a house: "
            "smaller exact packings and certificates at 69 counts, lower bounds at 37, "
            "39, 44 and 145 to 149, Hiroaki Hosono's closed form, which raises 154 "
            "reported lower bounds, Kevin Fang's n^2 - n + 1 theorem and s(76) = 9."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.7.0",
        first_published="October 14, 2026",
        result_scope=(
            "Add News with significance and topic filters, unify Explanations and split "
            "the tutorial, and let the Atlas use the full available page width."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.6.3",
        first_published="October 14, 2026",
        result_scope=(
            "Add the 14 October intake ledger to the project changelog and state on the "
            "epistemics page that credits name people by name."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.6.2",
        first_published="October 14, 2026",
        result_scope=(
            "List the October 14 reviews and intake ledger in the synopsis document map, "
            "refresh its session rollups, and re-anchor result-page bibliography links to "
            "their entries."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.6.1",
        first_published="October 14, 2026",
        result_scope=(
            "Register four results: a raised lower bound for 40 squares and new exact "
            "packings of 102, 154, 175, 232 and 264 squares, four of which the case "
            "records adopt."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.6.0",
        first_published="October 14, 2026",
        result_scope=(
            "Add the project changelog and an About index of launched results, papers and "
            "downloads."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.5.0",
        first_published="October 2, 2026",
        result_scope=(
            "The website edition: the project gets its own site, with a rated table of "
            "results and a frontier survey to $n = 324$, and a second paper reviews the "
            "proof that $s(11) = 3.8770835…$ (T-060)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.2",
        first_published="September 28, 2026",
        result_scope=(
            "The recent-results edition: the atlas takes in $s(32) = 6$ and raises the "
            "lower bound for 22 more cases, among them $s(11) ≥ 3.875$ and "
            "$s(17) \\gt 4.66001$, from outside certificates the register verifies, and "
            "its star now marks every recent result, credited case by case."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.1",
        first_published="September 22, 2026",
        result_scope=(
            "The shared-version edition: the page and the atlas carry one version, "
            "named for the last commit that changed the data, and the atlas adds "
            "T-030's $s(18) ≥ 4679/1000$."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.0",
        first_published="September 13, 2026",
        result_scope=(
            "The T-025/T-026 proof edition: T-025 proves "
            "$s(11) ≥ 191/50 = 3.82$, and T-026 proves "
            "$s(11) ≥ 3.8264474…$."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.3.0",
        first_published="September 5, 2026",
        result_scope=(
            "The first edition: T-018's point certificate proves $s(11) ≥ 381/100 = 3.81$."
        ),
    ),
)

#: The edition the site's pages and workbench state: the last site edition, frozen since
#: site editions were retired (think-wdqo).
PUBLICATION_VERSION = PUBLICATION_HISTORY[0].version

#: Where the edition stands, said ahead of the version. Empty once it is final; the
#: join below then drops it and the stray space with it, so going final is one edit.
PUBLICATION_STATUS = ""

#: The already printed infographic edition becomes this family's independent baseline.
#: Its first-live date is the v0.5.0 Pages deployment recorded above (8aaa411dc,
#: 2026-10-02T01:07:03Z), not an export filename or the date of a later redraw.
#: Both retained 1-100 and 1-324 graphics, their PDFs and PNGs share this history.
INFOGRAPHIC_HISTORY = (
    PublicationHistoryEntry(
        version="v0.7.0",
        first_published="October 23, 2026",
        result_scope=(
            "Draw every atlas tile in its canonical pose by flip regularization "
            "(regularization policy, section 13): the heaviest quadrant lower right, "
            "keeping the published pose of 252 counts and turning 72."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.6.4",
        first_published="October 20, 2026",
        result_scope=(
            "Redraw both atlas posters with Evan Daniel's n183 packing (T-220), which "
            "takes 183 off the 14 x 14 grid, and the houses of 19 October at 155, 229, "
            "236 and 271."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.6.3",
        first_published="October 17, 2026",
        result_scope=(
            "Badge 29's exact side and draw PR #622's certificate, the house at 29 since "
            "17 October 2026."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.6.2",
        first_published="October 17, 2026",
        result_scope=(
            "Redraw both atlas posters and every export at the 17 October data, with the "
            "fifteen houses adopted from T-185 to T-190 and the regularized drawings of "
            "16 and 17 October, including 176's."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.6.1",
        first_published="October 15, 2026",
        result_scope=(
            "Refresh both atlas posters to the admitted October 15 packing data, bounds "
            "and credits, with descriptions matching gray case numbers and numeric-only "
            "recency accents."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.6.0",
        first_published="October 14, 2026",
        result_scope=(
            "Show regularized defaults on both atlas posters with compact attribution and "
            "original-source comparison."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.5.0",
        first_published="October 2, 2026",
        result_scope="The retained infographic pair's already published v0.5.0 edition.",
    ),
)
INFOGRAPHIC_VERSION = INFOGRAPHIC_HISTORY[0].version


#: What the shared version's hash names (the owner, 2026-09-22): the last commit that
#: changed the evidence and data every artifact is drawn from. Repository-relative, as
#: every declared path here is.
DATA_PATHS: tuple[str, ...] = ("packing/frontier", "packing/atlas/known-best")

#: What inside `DATA_PATHS` is not evidence and data, and so never moves the version, as
#: git pathspecs. The atlas composites and their raster and PDF exports carry the stamp
#: and are drawn from the data rather than being it; counting them would make the commit
#: that re-stamps them a data commit (rule 4 above). The video spikes are the players'
#: code, and the videos themselves are release assets, never committed.
#:
#: The registers' own READMEs join them on 2026-09-22, on the same grounds: they document
#: how a record is written, and nothing is drawn from them. `e560571f2` edited
#: `frontier/README.md` alone -- the prose on registration evidence, no packing record and
#: no bound -- and under the old list that moved the version every artifact prints, which
#: would have restamped the atlas and dated a cut whose every frame was identical. A
#: version that changes when the instructions change is not naming the evidence.
#:
#: The figure playbook joins them on 2026-09-28 for the same reason: it says how the atlas
#: is drawn and how to check it, and nothing is drawn from it. `6f6bc89ec` edited only its
#: legend counts and moved the version every artifact prints; the atlas's new citations
#: line then needed a one-word playbook edit that would have done it again.
DATA_EXCLUDED: tuple[str, ...] = (
    "packing/atlas/known-best/known-best-1-*",
    "packing/atlas/known-best/square-packings-*-????????.pdf",
    "packing/atlas/known-best/video",
    "packing/frontier/README.md",
    "packing/atlas/known-best/README.md",
    "packing/atlas/known-best/figure-playbook.md",
)

#: How many characters of that commit the version carries (the owner, 2026-09-22).
DATA_REVISION_LENGTH = 6

#: Whether an atlas poster may show data older than the pin between version bumps (rule
#: 3; the owner, 2026-10-01: the large assets are regenerated "whenever we do an official
#: site version number bump", and on demand). `True`: a card that differs from the
#: current record is listed and fails nothing, once the pin has moved past the poster's
#: own data revision. `False`: it fails, and the poster is redrawn whenever a card
#: changes -- as 26 commits did in September 2026, at 13.6 MB of blobs each.
COMPOSITES_MAY_TRAIL = True

#: The last data commit, pinned in full: what `data_revision` returned when it was last
#: re-pinned. Full rather than six characters so the drift check compares a commit, not
#: a prefix.
DATA_REVISION = "8e74e3a4ed8a1275813deb02ae55317be511e7d6"

#: The version, written the one way it is ever written: `v0.4.1-f5e113`. Semver core,
#: then the data revision, in the shape a build identifier takes everywhere else.
#:
#: This is the value to reach for. It exists because the artifacts that stamp an edition
#: used to compose their own strings from the parts, in two files and two languages, and
#: the page named a different commit from the atlas. Hand-assembled spellings of one fact
#: are how they come to disagree.
PUBLICATION_STAMP = f"{PUBLICATION_VERSION}-{DATA_REVISION[:DATA_REVISION_LENGTH]}"


def edition_at(revision: str) -> str:
    """The edition as an artifact drawn from the data commit `revision` writes it.

    `PUBLICATION_EDITION` is this at the pin. A drawn release asset keeps the one it
    was drawn with (rule 4), so its stamp is this at its own data revision.
    """
    stamp = f"{PUBLICATION_VERSION}-{revision[:DATA_REVISION_LENGTH]}"
    return " ".join(part for part in (PUBLICATION_STATUS, stamp) if part)


#: How the version is written wherever it is stamped: the stamp, with the status ahead
#: of it while there is one. The site's footer and the workbench take this string whole,
#: so neither can disagree about whether the reader is holding a draft, nor about how
#: the version is spelled. A paper's footer leaves it out (`render_overview.colophon_lines`).
PUBLICATION_EDITION = edition_at(DATA_REVISION)


def infographic_edition_at(revision: str, version: str | None = None) -> str:
    """A poster's own edition and derivation revision, independent of the site."""
    core = INFOGRAPHIC_VERSION if version is None else version
    parsed_version(core)
    return f"{core}-{revision[:DATA_REVISION_LENGTH]}"


INFOGRAPHIC_EDITION = f"{INFOGRAPHIC_VERSION}-{DATA_REVISION[:DATA_REVISION_LENGTH]}"

#: When the current edition was first published, written the way a reader reads it.
PUBLICATION_DATE = PUBLICATION_HISTORY[0].first_published

#: When the publication itself was first published: its oldest edition's date. The site
#: began as the explainer, so this is also that paper's first day (`EXPLAINER_FIRST_PUBLISHED`,
#: which is what the paper's front prints).
FIRST_PUBLISHED = PUBLICATION_HISTORY[-1].first_published

# ---------------------------------------------------------------------------
# The papers' own versions.
#
# Each paper is versioned on its own (the owner, 2026-10-01), and its version line and
# version history reflect versions of the paper, not of the site or anything else. A
# published number under which the paper changed stays exactly as published, number and
# date, and is never renumbered; an edition under which the paper did not change is not
# a version of the paper and is not in its history. `devtools.paper_front` writes the
# front of both papers from these, and `tests/test_release.py` holds the rules.
# ---------------------------------------------------------------------------

#: The first paper's own editions, newest first. Through v0.5.0 the paper carried the
#: site's number, so the entries up to v0.4.2 are the editions of the publication in
#: which the paper itself changed, with the site's own number and date for each; v0.4.3
#: is the paper's first number of its own. What changed in the paper under each, read
#: from the article's history between the deployments listed above `PUBLICATION_HISTORY`
#: on 2026-10-02:
#:
#:   v0.4.4  the paper becomes Part I of the n = 11 series: the frontier update names
#:           T-037 and links Parts II and III, and Further Reading lists the series
#:   v0.4.3  the frontier update of September 30 records T-060's proof that s(11) is
#:           Trump's side, the T-026 rating moves from V4/C5 to V3/C3 under the ladder
#:           of 2026-09-30, Figure 3 marks the settled endpoint, and a footnote records
#:           the n = 12 and n = 17 bounds others have since raised (249d42c37,
#:           d205561f0, 7862dc3e8, a6f630dd7); a patch revision of the paper (the owner,
#:           2026-10-01), published under the v0.4.2 label until it was numbered
#:   v0.4.2  the frontier update of September 22 records Overbeck's verified
#:           s(11) >= 3.875, built on T-026's certificate, and the paper presents T-026's
#:           bound as historical; Figure 2's star marks every recent result
#:   v0.4.0  the article rewritten around T-025 and T-026, the 381/100 proof kept as the
#:           worked example
#:   v0.3.0  the first edition
#:
#: Not versions of the paper: v0.4.1, under which the article did not change at all (the
#: shared version stamp and the atlas's T-030), and v0.5.0, the website edition, which
#: changed nothing in either paper. A new version of the paper goes on the front with its
#: own number and the day it is first published; `EXPLAINER_REVISED` moves with the
#: article either way.
#:
#: v0.4.3 is dated by the deployment that first served the article in its present
#: substance, the last substantive change being the V3/C3 regrade (d205561f0):
#:
#:   v0.4.3  2026-10-01T08:01:58Z  f9a3409f0  the first deployment holding d205561f0;
#:                                            the T-060 update was live from d44ec0408,
#:                                            2026-09-30T17:44:28Z, and the cosmetic
#:                                            changes after it (the slug, the credits
#:                                            form, 9b459da65 and 97e4069d5) went live
#:                                            on October 1 and 2, so the substantive
#:                                            day is the one recorded
#: The leading entry is proposed for the next publication; confirm its date at first deployment.
EXPLAINER_HISTORY = (
    PublicationHistoryEntry(
        version="v0.4.31",
        first_published="October 26, 2026",
        result_scope=(
            "Update the registered result count after the registration of Evan Daniel's "
            "packing at 299 (T-247) and three reported Lean formalizations (T-248 to "
            "T-250)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.30",
        first_published="October 25, 2026",
        result_scope=(
            "Update the registered result count after the registrations of T-245 and T-246."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.29",
        first_published="October 25, 2026",
        result_scope=(
            "Update the registered result count after the registration of Hyukdong Kim's "
            "exact sides at 172 and 263 (T-244)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.28",
        first_published="October 25, 2026",
        result_scope=(
            "Update the registered result count after the registration of Evan Daniel's "
            "#806 certificate at 182 (T-243)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.27",
        first_published="October 24, 2026",
        result_scope=(
            "Update the registered result count after the registration of Francisco "
            "Couzo's certificate at 304 (T-241) and Evan Daniel's exact descents at 268 "
            "and 304 (T-242)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.26",
        first_published="October 24, 2026",
        result_scope=(
            "Update the registered result count after the registration of Francisco "
            "Couzo's #763 certificates at 268 and 303 (T-240)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.25",
        first_published="October 24, 2026",
        result_scope=(
            "Update the registered result count after the registration of Amund "
            "Kristiansen's #755 certificate at 303 (T-239)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.24",
        first_published="October 24, 2026",
        result_scope=(
            "Update the registered result count after the registrations of the Lean "
            "formalization reports of Hosono at 21 (T-234) and 59 (T-235) and of Daniel "
            "for Fang's theorems (T-236), of the classical values at 2 to 5 (T-237) and "
            "of chelokot's and Daniel's Lean routes to them (T-238)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.23",
        first_published="October 24, 2026",
        result_scope=(
            "Update the registered result count after the registrations of Hosono's "
            "fine-net lower bounds at 31 (T-232) and at 19, 20, 26 and 27 (T-233)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.22",
        first_published="October 24, 2026",
        result_scope=(
            "Update the registered result count after the registration of Mykhailo "
            "Polkovskyi's lower 204 side (T-231)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.21",
        first_published="October 23, 2026",
        result_scope=(
            "Set a shared 35em reading measure for paper prose in HTML and PDF layouts."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.20",
        first_published="October 23, 2026",
        result_scope=(
            "Update the registered result count after the registration of Evan Daniel's "
            "#728 certificate at 303 (T-230)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.19",
        first_published="October 22, 2026",
        result_scope="Use full public names in explanatory narrative profile links.",
    ),
    PublicationHistoryEntry(
        version="v0.4.18",
        first_published="October 22, 2026",
        result_scope=(
            "Update the registered result count after the registration of Mykhailo "
            "Polkovskyi's #719 re-solves at 105 and 204 (T-229)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.17",
        first_published="October 22, 2026",
        result_scope=(
            "Publish canonical website addresses at squaremath.org while retaining GitHub "
            "repository citations."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.16",
        first_published="October 22, 2026",
        result_scope=(
            "Link reviewed oversight credits and article names to person profiles with "
            "consistent surname labels."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.15",
        first_published="October 22, 2026",
        result_scope=(
            "Update the registered result count after the registration of Francisco "
            "Couzo's #670, #672 and #675 rows (T-226 to T-228)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.14",
        first_published="October 22, 2026",
        result_scope=(
            "Update the registered result count after the registration of Evan Daniel's "
            "regularized views at 204, 227, 229 and 260 (T-225)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.13",
        first_published="October 21, 2026",
        result_scope=(
            "Update the registered result count after the n270 registration (T-224)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.12",
        first_published="October 21, 2026",
        result_scope=(
            "Update the registered result count after the n204 and n260 registration (T-223)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.11",
        first_published="October 20, 2026",
        result_scope=(
            "Update the registered result count after the n308 and n154 registrations "
            "(T-221, T-222)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.10",
        first_published="October 20, 2026",
        result_scope=(
            "Update the registered result count after the n183 registration and adoption "
            "(T-220)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.9",
        first_published="October 20, 2026",
        result_scope=(
            "Update the registered result count after Evan Daniel's n236 and n271 "
            "packings (T-218, T-219)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.8",
        first_published="October 19, 2026",
        result_scope=(
            "Update the registered result count and current bound citations after the "
            "fine-net imports and reviewed n108 adoption."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.7",
        first_published="October 15, 2026",
        result_scope=(
            "Refresh the embedded atlas to the admitted October 15 packings, bounds "
            "and credits, and correct its description of numeric-only recency accents."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.6",
        first_published="October 14, 2026",
        result_scope=(
            "Explain the two reported 17-square optimality proofs and their V0/C1 "
            "verification limits."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.5",
        first_published="October 10, 2026",
        result_scope=(
            "Use Chicago title case for bibliography titles and typographic "
            "punctuation in the shared version-history rendering."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.4",
        first_published="October 5, 2026",
        result_scope=(
            "The series revision: the paper is Part I of three; its frontier update and "
            "Further Reading link Part II, on Overbeck's T-037, and Part III, on T-060."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.3",
        first_published="October 1, 2026",
        result_scope=(
            "The settled-case revision: the frontier update records T-060's proof that "
            "$s(11)$ is Trump's side, Figure 3 marks the endpoint, T-026 is rated V3/C3, "
            "and the raised $n = 12$ and $17$ bounds are noted."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.2",
        first_published="September 28, 2026",
        result_scope=(
            "The recent-results edition: a frontier update records Overbeck's verified "
            "$s(11) ≥ 3.875$, built on the T-026 certificate, so the paper presents "
            "T-026's bound as historical, and the star on the atlas in Figure 2 marks "
            "every recent result."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.0",
        first_published="September 13, 2026",
        result_scope=(
            "The T-025/T-026 proof edition: T-025 proves "
            "$s(11) ≥ 191/50 = 3.82$, and T-026 proves "
            "$s(11) ≥ 3.8264474…$."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.3.0",
        first_published="September 5, 2026",
        result_scope=(
            "The first edition: T-018's point certificate proves $s(11) ≥ 381/100 = 3.81$."
        ),
    ),
)

#: The first paper's version, plain, which its version line prints and links to its
#: history: its newest edition's number, with no status ahead of it and no data hash.
EXPLAINER_VERSION = EXPLAINER_HISTORY[0].version

#: When the first paper was first published: its oldest edition's day, which its front
#: puts beside the day it was last revised, so a reader sees both how old the result is
#: and how recently it was revised.
EXPLAINER_FIRST_PUBLISHED = EXPLAINER_HISTORY[-1].first_published

#: When the explainer's own text last changed: the date its "Last revised" line prints.
#: It is the author date of the last commit that changed the article
#: (`devtools.artifact_dates` names the file and holds this to git), and it used to be
#: `PUBLICATION_DATE`, the day the edition was first published, which stood still while
#: the article changed under it: merging is the whole publish, so the text a reader sees
#: moves between editions. Change it in the commit that changes the article.
EXPLAINER_REVISED = "October 22, 2026"

#: The optimality review's own editions, newest first, each with the day it was first
#: published and what changed in the paper: the review's history, as `EXPLAINER_HISTORY`
#: is the explainer's, linked from its front (`PaperFront.history`). v0.1.0 is dated by
#: the commit that published it (620ffff54); the day it first went live is not recorded
#: (think-2cqu).
# The leading entry is proposed for the next publication; confirm its date at first deployment.
OPTIMALITY_REVIEW_HISTORY = (
    PublicationHistoryEntry(
        version="v0.1.11",
        first_published="October 22, 2026",
        result_scope=(
            "Set a shared 35em reading measure for paper prose in HTML and PDF layouts."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.10",
        first_published="October 22, 2026",
        result_scope="Use full public names in explanatory narrative profile links.",
    ),
    PublicationHistoryEntry(
        version="v0.1.9",
        first_published="October 22, 2026",
        result_scope=(
            "Publish canonical website addresses at squaremath.org while retaining GitHub "
            "repository citations."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.8",
        first_published="October 21, 2026",
        result_scope=(
            "Correct Manasseh Ahmed's name and credit Hiroaki Hosono's checker and "
            "formalization reports by name; link reviewed article names to person profiles."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.7",
        first_published="October 7, 2026",
        result_scope=(
            "The exposition review corrects the shorter symmetry proof's intermediate "
            "counts and states both propagation rules, distinguishes cases from masks "
            "and contact from a zero projection gap, limits the contact deformation "
            "to its root neighborhood, puts figure symbols after their definitions, "
            "and clarifies shared geometric code and the reported Lean formalization."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.6",
        first_published="October 6, 2026",
        result_scope=(
            "The uniqueness corollary is registered as T-112 and no longer called "
            "unreviewed, with its prior art: Trump's rigidity claim is local, and "
            "Stromquist's three optimal packings of ten squares show uniqueness is not "
            "automatic; and Ahmed's report of a complete Lean 4 "
            "formalization of October 6 is cited, with its native-compiler trust base "
            "and the project's statement audit."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.5",
        first_published="October 5, 2026",
        result_scope=(
            "The series revision: the paper is Part III of three, its lineage names Part "
            "II's three changes from T-026 and draws the series bound ladder as Figure 3, "
            "Charge Budgets contrasts capacity one with "
            "$\\lfloor m/k\\rfloor$, a test holds every term to a definition before its "
            "first use, and the notation follows the series: $L_0$, $\\Gamma_i$, "
            "$\\operatorname{rot}$, $\\mathbf{D}_4$ and $(191/50)/U$."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.4",
        first_published="October 4, 2026",
        result_scope=(
            "wand125's comment of October 4 is answered: the in-progress Lean 4 "
            "formalizations are named, with their status as wand125 reports it; the root "
            "node completes thirteen further updates, not fourteen; Figure 8 and the text "
            "agree that the symmetry lemma rests on the exhaustive search; and the "
            "1,931-case premise of cases 2175 and 2176 is stated as a premise of their "
            "accepted certificates, beside wand125's report of a Lean proof of all 76 "
            "prior-family cases that does not use it."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.3",
        first_published="October 3, 2026",
        result_scope=(
            "The closing section explains what a receipt is, the three depths at which "
            "a reader can verify the retained evidence, and the four checked components "
            "the reviews of October 3 added beside the accepted ones; the receipts "
            "register is linked."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.2",
        first_published="October 3, 2026",
        result_scope=(
            "The second reviewed revision: GPT-6 Pro's unified adversarial review of "
            "October 3 is applied. The invariant is stated row by row with ownership "
            "quantified over valid packings, the field citation names the original's "
            "§12 and a worked mask-0 certificate, the separation features are written "
            "as a disjunction of conjunctions, the isolation lemma carries the weighted "
            "residual, the five-site charge gains its ten-hull form, the root is "
            "certified unique on its interval, the uniqueness corollary is stated "
            "conditionally, and the frames, roles, radii and cover sites are tabulated."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.1",
        first_published="October 3, 2026",
        result_scope=(
            "The reviewed revision: the adversarial review of October 3 is applied, every "
            "term is defined before its first use, the transfer rule states the half-turn, "
            "the final deduction names the symmetry image, and the paper explains the tilt "
            "$u=\\tan(a/2)$, the polynomial as one contact and the four survivors as the "
            "construction under the eight symmetries."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.0",
        first_published="September 30, 2026",
        result_scope="The first edition: the explainer of T-060's proof, with its figures.",
    ),
)

#: Where the review stands, and its version line: a draft, written on the two papers'
#: one credits form (`devtools.paper_front`; the owner, 2026-10-01: "Draft v0.1.0", not
#: bold). It is the review's version and not the site's, which was the first of #289's
#: questions on think-cv22 and is settled: the site's edition goes on no paper. Joined as
#: `edition_at` joins the publication's status and stamp, so going final is one edit
#: here too.
OPTIMALITY_REVIEW_STATUS = "Draft"
OPTIMALITY_REVIEW_VERSION = OPTIMALITY_REVIEW_HISTORY[0].version
OPTIMALITY_REVIEW_EDITION = " ".join(
    part for part in (OPTIMALITY_REVIEW_STATUS, OPTIMALITY_REVIEW_VERSION) if part
)

#: When the optimality review's own text last changed: the date its "Last revised" line
#: prints, by the rule `EXPLAINER_REVISED` follows -- the author date of the last commit
#: that changed its article, `n11-optimality-review-article.md`, held to git by
#: `devtools.artifact_dates`. Change it in the commit that changes the article.
OPTIMALITY_REVIEW_REVISED = "October 13, 2026"

#: The day the proof the review explains was published by its source, which the review's
#: "Original proof" date prints. A fact about someone else's work, so it is typed, and
#: held by `devtools.artifact_dates` to the day the register records for T-060.
OPTIMALITY_PROOF_PUBLISHED = "September 29, 2026"

#: Every edition of Part II, the review of Overbeck's certified lower bound
#: `s(11) > 31/8` (T-037), newest first, as `OPTIMALITY_REVIEW_HISTORY` is Part III's.
# The leading entry is proposed for the next publication; confirm its date at first deployment.
THRESHOLD_REVIEW_HISTORY = (
    PublicationHistoryEntry(
        version="v0.1.4",
        first_published="October 22, 2026",
        result_scope=(
            "Set a shared 35em reading measure for paper prose in HTML and PDF layouts."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.3",
        first_published="October 22, 2026",
        result_scope="Use full public names in explanatory narrative profile links.",
    ),
    PublicationHistoryEntry(
        version="v0.1.2",
        first_published="October 22, 2026",
        result_scope=(
            "Publish canonical website addresses at squaremath.org while retaining GitHub "
            "repository citations."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.1",
        first_published="October 21, 2026",
        result_scope=(
            "Credit Hiroaki Hosono's checker and retained tools by name; "
            "link reviewed names in the article to person profiles."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.0",
        first_published="October 5, 2026",
        result_scope=(
            "The first edition: Part II of the series, the review of T-037's proof, with "
            "its figures."
        ),
    ),
)

#: Part II's status and version line, on the papers' one credits form, as
#: `OPTIMALITY_REVIEW_EDITION` is Part III's.
THRESHOLD_REVIEW_STATUS = "Draft"
THRESHOLD_REVIEW_VERSION = THRESHOLD_REVIEW_HISTORY[0].version
THRESHOLD_REVIEW_EDITION = " ".join(
    part for part in (THRESHOLD_REVIEW_STATUS, THRESHOLD_REVIEW_VERSION) if part
)

#: When Part II's text last changed, by the rule `OPTIMALITY_REVIEW_REVISED` follows: the
#: author date of the last commit that changed `n11-threshold-bound-review-article.md`,
#: held to git by `devtools.artifact_dates`.
THRESHOLD_REVIEW_REVISED = "October 13, 2026"

#: The day Overbeck published the proof Part II reviews (v1.0.2 of
#: 11-squares-certified-bound), which its "Original proof" date prints.
THRESHOLD_PROOF_PUBLISHED = "September 22, 2026"

#: The standalone tutorial on finding and verifying record packings. Its version and
#: dates belong to the paper, independently of the site and n = 11 series.
#: The leading entry is proposed for the next publication; confirm its date at first deployment.
PACKING_METHODS_HISTORY = (
    PublicationHistoryEntry(
        version="v0.2.7",
        first_published="October 22, 2026",
        result_scope=(
            "Set a shared 35em reading measure for paper prose in HTML and PDF layouts."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.2.6",
        first_published="October 22, 2026",
        result_scope="Use full public names in explanatory narrative profile links.",
    ),
    PublicationHistoryEntry(
        version="v0.2.5",
        first_published="October 22, 2026",
        result_scope=(
            "Publish canonical website addresses at squaremath.org while retaining GitHub "
            "repository citations."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.2.4",
        first_published="October 21, 2026",
        result_scope=(
            "Link reviewed oversight credits and article names to person profiles with "
            "consistent surname labels."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.2.3",
        first_published="October 17, 2026",
        result_scope=(
            "Figure 3 draws PingYou Ltd's exact rational certificate of the 29-square "
            "packing, the case's house since 17 October 2026."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.2.2",
        first_published="October 14, 2026",
        result_scope=(
            "Credit the 12 October adoptions at 154, 175, 232 and 264 in the account of "
            "the adopted houses."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.2.1",
        first_published="October 10, 2026",
        result_scope=(
            "Use typographic punctuation in version histories and consistent Chicago "
            "title case for paper titles and links."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.2.0",
        first_published="October 10, 2026",
        result_scope=(
            "Add the confirmed October 8 intake: 32 selected upper-bound improvements, "
            "Couzo's disclosed refinement workflow, Xu's radical certificate, and "
            "refiner calibration and branch-selection examples, with five attributed "
            "packing illustrations. Include Daniel's replayed October 9 record-hunt "
            "certificates, pending independent review and standing-bound adoption. "
            "Distinguish local rigidity, source assertions, and translation screens "
            "from optimality evidence."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.0",
        first_published="October 8, 2026",
        result_scope=(
            "First publication: a systematic tutorial on modelling, searching, refining, "
            "reconstructing and verifying record square packings, with sourced method "
            "and seed lineage tables."
        ),
    ),
)
PACKING_METHODS_VERSION = PACKING_METHODS_HISTORY[0].version
PACKING_METHODS_EDITION = PACKING_METHODS_VERSION
PACKING_METHODS_FIRST_PUBLISHED = PACKING_METHODS_HISTORY[-1].first_published
PACKING_METHODS_REVISED = "October 17, 2026"


# Public component identifiers are shared with changelog release references and cuts.
COMPONENT_HISTORY_NAMES = {
    "site": "PUBLICATION_HISTORY",
    "infographics": "INFOGRAPHIC_HISTORY",
    "paper:n11-lower-bounds-explainer": "EXPLAINER_HISTORY",
    "paper:n11-optimality-review": "OPTIMALITY_REVIEW_HISTORY",
    "paper:n11-threshold-bound-review": "THRESHOLD_REVIEW_HISTORY",
    "paper:square-packing-methods-survey": "PACKING_METHODS_HISTORY",
}

# Editions already retained when independent component-impact policy began. Historical
# releases keep their published numbers; impact decisions are required for successors.
RELEASE_POLICY_BASELINES = {
    "site": "v0.5.0",
    "infographics": "v0.5.0",
    "paper:n11-lower-bounds-explainer": "v0.4.5",
    "paper:n11-optimality-review": "v0.1.7",
    "paper:n11-threshold-bound-review": "v0.1.0",
    "paper:square-packing-methods-survey": "v0.2.1",
}

ReleaseImpact = Literal["patch", "minor"]


class ReleaseImpactDecision(NamedTuple):
    """One component's complete delivered change, its chosen bump, and its reason.

    Patch covers corrections, ordinary refreshes and small fixes within existing scope.
    Minor covers substantial capabilities, coverage, redesigns, exposition or methods.
    A batch with both takes minor; internal work and bookkeeping create no edition.
    """

    component: str
    previous_version: str
    version: str
    impact: ReleaseImpact
    reason: str


# New component cuts append decisions here, newest first, alongside their own histories.
# No impact is invented retrospectively for the published baseline editions.
RELEASE_IMPACTS: tuple[ReleaseImpactDecision, ...] = (
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.30",
        version="v0.4.31",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Evan Daniel's "
            "packing at 299 (T-247) and three reported Lean formalizations (T-248 to "
            "T-250)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.29",
        version="v0.4.30",
        impact="patch",
        reason=(
            "Update the registered result count after the registrations of Jatloe's "
            "reported Lean proof that s(12) = 4 (T-245) and Evan Daniel's reported "
            "minimal polynomial of the s(29) record side (T-246)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.28",
        version="v0.4.29",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Hyukdong Kim's "
            "exact sides at 172 and 263 (T-244)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.27",
        version="v0.4.28",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Evan Daniel's "
            "#806 certificate at 182 (T-243), adopted as the house best packing there."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.26",
        version="v0.4.27",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Francisco "
            "Couzo's certificate at 304 (T-241) and Evan Daniel's exact descents at 268 "
            "and 304 (T-242)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.25",
        version="v0.4.26",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Francisco "
            "Couzo's #763 certificates at 268 and 303 (T-240)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.24",
        version="v0.4.25",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Amund "
            "Kristiansen's #755 certificate at 303 (T-239)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.23",
        version="v0.4.24",
        impact="patch",
        reason=(
            "Update the registered result count after the registrations of the Lean "
            "formalization reports of Hosono at 21 (T-234) and 59 (T-235) and of Daniel "
            "for Fang's theorems (T-236), of the classical values at 2 to 5 (T-237) and "
            "of chelokot's and Daniel's Lean routes to them (T-238)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.22",
        version="v0.4.23",
        impact="patch",
        reason=(
            "Update the registered result count after the registrations of Hosono's "
            "fine-net lower bounds at 31 (T-232) and at 19, 20, 26 and 27 (T-233)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.21",
        version="v0.4.22",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Mykhailo "
            "Polkovskyi's lower 204 side (T-231)."
        ),
    ),
    ReleaseImpactDecision(
        component="infographics",
        previous_version="v0.6.4",
        version="v0.7.0",
        impact="minor",
        reason=(
            "Draw every atlas tile in its canonical pose by flip regularization "
            "(regularization policy, section 13): the heaviest quadrant lower right, "
            "keeping the published pose of 252 counts and turning 72."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:square-packing-methods-survey",
        previous_version="v0.2.6",
        version="v0.2.7",
        impact="patch",
        reason=("Set a shared 35em reading measure for paper prose in HTML and PDF layouts."),
    ),
    ReleaseImpactDecision(
        component="paper:n11-threshold-bound-review",
        previous_version="v0.1.3",
        version="v0.1.4",
        impact="patch",
        reason=("Set a shared 35em reading measure for paper prose in HTML and PDF layouts."),
    ),
    ReleaseImpactDecision(
        component="paper:n11-optimality-review",
        previous_version="v0.1.10",
        version="v0.1.11",
        impact="patch",
        reason=("Set a shared 35em reading measure for paper prose in HTML and PDF layouts."),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.20",
        version="v0.4.21",
        impact="patch",
        reason=("Set a shared 35em reading measure for paper prose in HTML and PDF layouts."),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.19",
        version="v0.4.20",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Evan Daniel's "
            "#728 certificate at 303 (T-230)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.18",
        version="v0.4.19",
        impact="patch",
        reason="Use full public names in explanatory narrative profile links.",
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.9.1",
        version="v0.9.2",
        impact="patch",
        reason=(
            "Record Mykhailo Polkovskyi's #719 re-solves of the house packings at 105 and "
            "204 as T-229, pending review and adoption, and his 111 rows beyond the "
            "corpus at or below 1024 as current beyond-horizon rows, superseding the rows "
            "that stood at those counts; record the replies after #720."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.17",
        version="v0.4.18",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Mykhailo "
            "Polkovskyi's #719 re-solves at 105 and 204 (T-229)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:square-packing-methods-survey",
        previous_version="v0.2.5",
        version="v0.2.6",
        impact="patch",
        reason="Use full public names in explanatory narrative profile links.",
    ),
    ReleaseImpactDecision(
        component="paper:n11-threshold-bound-review",
        previous_version="v0.1.2",
        version="v0.1.3",
        impact="patch",
        reason="Use full public names in explanatory narrative profile links.",
    ),
    ReleaseImpactDecision(
        component="paper:n11-optimality-review",
        previous_version="v0.1.9",
        version="v0.1.10",
        impact="patch",
        reason="Use full public names in explanatory narrative profile links.",
    ),
    ReleaseImpactDecision(
        component="paper:square-packing-methods-survey",
        previous_version="v0.2.4",
        version="v0.2.5",
        impact="patch",
        reason=(
            "Publish canonical website addresses at squaremath.org while retaining GitHub "
            "repository citations."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-threshold-bound-review",
        previous_version="v0.1.1",
        version="v0.1.2",
        impact="patch",
        reason=(
            "Publish canonical website addresses at squaremath.org while retaining GitHub "
            "repository citations."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-optimality-review",
        previous_version="v0.1.8",
        version="v0.1.9",
        impact="patch",
        reason=(
            "Publish canonical website addresses at squaremath.org while retaining GitHub "
            "repository citations."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.16",
        version="v0.4.17",
        impact="patch",
        reason=(
            "Publish canonical website addresses at squaremath.org while retaining GitHub "
            "repository citations."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.9.0",
        version="v0.9.1",
        impact="patch",
        reason=(
            "Publish canonical website addresses at squaremath.org while retaining GitHub "
            "repository citations."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.15",
        version="v0.4.16",
        impact="patch",
        reason=(
            "Link the oversight credit to Joshua Levy's profile and use the reviewed "
            "surname label in the HTML and Markdown fronts, also used for PDF output; "
            "link reviewed article names to profiles."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:square-packing-methods-survey",
        previous_version="v0.2.3",
        version="v0.2.4",
        impact="patch",
        reason=(
            "Link the oversight credit to Joshua Levy's profile and use the reviewed "
            "surname label in the HTML and Markdown fronts, also used for PDF output; "
            "link reviewed article names to profiles."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.20",
        version="v0.9.0",
        impact="minor",
        reason=(
            "Add person profiles and reviewed credit links, with direct profile "
            "navigation and shared article popovers for complete case and result records."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.19",
        version="v0.8.20",
        impact="patch",
        reason=(
            "Record the beyond-horizon rows of four older reports, Joost de Winter's #666 "
            "at or below 1024 and Francisco Couzo's #670, #672 and #675, as 205 dated "
            "rows of which 8 of #670's become current, and record the replies after #718 "
            "and #643's acknowledgement."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.18",
        version="v0.8.19",
        impact="patch",
        reason=(
            "Raise Evan Daniel's regularized views (T-225) to V3/C3 after their stage 4 "
            "review, adopt them as the house best packings at 204, 227, 229 and 260, and "
            "register Francisco Couzo's #670, #672 and #675 rows (T-226 to T-228)."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.17",
        version="v0.8.18",
        impact="patch",
        reason=(
            "Record Francisco Couzo's 109 new upper bounds at or below 1024 from issue "
            "715 as current beyond-horizon rows, superseding the rows that stood at those "
            "counts, and record the #715 acknowledgement and the #678 follow-up."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.14",
        version="v0.4.15",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Francisco "
            "Couzo's #670, #672 and #675 rows (T-226 to T-228)."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.16",
        version="v0.8.17",
        impact="patch",
        reason=(
            "Register Evan Daniel's solved and regularized views at 204, 227, 229 and 260 "
            "(T-225, V0/C0); record the #668 and #702 replies, #678's stage 7 reply and "
            "#668's follow-up; enter #715 at triage; correct the overview's Couzo and de "
            "Winter cards; and announce T-196's and T-223's adoptions in the News."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.13",
        version="v0.4.14",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Evan Daniel's "
            "regularized views at 204, 227, 229 and 260 (T-225)."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.15",
        version="v0.8.16",
        impact="patch",
        reason=(
            "Raise Francisco Couzo's n204 and n260 certificates (T-223) to V3/C3 on their "
            "stage 4 review and adopt them as the house best packings at 204 and at 260, "
            "where T-223 replaces T-196, with the strong generators' drawings."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.14",
        version="v0.8.15",
        impact="patch",
        reason=(
            "Raise Joost de Winter's T-196 (#668) at 227, 229 and 260 to V3/C3 on the "
            "integrated exact replay and its stage 4 review, and adopt it as the house "
            "best packing at 227 and 260 with Evan Daniel's regularized views."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.13",
        version="v0.8.14",
        impact="patch",
        reason=(
            "Record Evan Daniel's s(343) certificate of issue 702 as the current "
            "beyond-horizon row at 343, superseding issue 678's row there."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.12",
        version="v0.8.13",
        impact="patch",
        reason="Name the 20 October review in the lineages at 154 and 308.",
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.11",
        version="v0.8.12",
        impact="patch",
        reason=(
            "Record Darius Muglich's 100 reported upper bounds at 328 to 998 (#686) as "
            "beyond-horizon rows, superseding the rows they beat, with the issue's card."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.10",
        version="v0.8.11",
        impact="patch",
        reason=(
            "Correct T-224's significance wording, give the 270 credit sentence the "
            "design's composition, and name the 21 October review as where T-224 was "
            "measured."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.9",
        version="v0.8.10",
        impact="patch",
        reason=(
            "Raise Evan Daniel's n270 certificate (T-224) to V3/C3 on its stage 4 review "
            "and adopt it as the house best packing at 270, with its regularized drawing."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.12",
        version="v0.4.13",
        impact="patch",
        reason=("Update the registered result count after the n270 registration (T-224)."),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.8",
        version="v0.8.9",
        impact="patch",
        reason=(
            "Credit Evan Daniel as finder at 271 as issue 664 asks, cite his answer on "
            "the regularized views' by field, and correct T-221's tilt count and the "
            "house best packing wording at 154 and 308."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.7",
        version="v0.8.8",
        impact="patch",
        reason=(
            "Register Francisco Couzo's reported n204 and n260 certificates (T-223) at "
            "V0/C0, pending review and adoption, and his 83 beyond-horizon rows."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.11",
        version="v0.4.12",
        impact="patch",
        reason=(
            "Update the registered result count after the n204 and n260 registration (T-223)."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.6",
        version="v0.8.7",
        impact="patch",
        reason=(
            "The synopsis defines the house best packing, and the conventions write house "
            "only as a modifier."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.5",
        version="v0.8.6",
        impact="patch",
        reason=(
            "Register, confirm and adopt Evan Daniel's n308 and n154 certificates (T-221, "
            "T-222): raised to V3/C3 by the 20 October review, adopted as the house best "
            "packings at 308 and 154, and regularized."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.4",
        version="v0.8.5",
        impact="patch",
        reason=(
            "Announce Evan Daniel's sub-grid n183 packing (T-220) in News and list the 20 "
            "October report-order ledger in the synopsis."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.10",
        version="v0.4.11",
        impact="patch",
        reason=(
            "Update the registered result count after the n308 and n154 registrations "
            "(T-221, T-222)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.9",
        version="v0.4.10",
        impact="patch",
        reason=(
            "Update the registered result count after the n183 registration and adoption "
            "(T-220)."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.3",
        version="v0.8.4",
        impact="patch",
        reason=(
            "Register Evan Daniel's sub-grid n183 certificate (T-220), adopt it as the "
            "n183 house and draw its regularized view."
        ),
    ),
    ReleaseImpactDecision(
        component="infographics",
        previous_version="v0.6.3",
        version="v0.6.4",
        impact="patch",
        reason=(
            "Redraw both atlas posters with Evan Daniel's n183 packing (T-220), which "
            "takes 183 off the 14 x 14 grid, and the houses of 19 October at 155, 229, "
            "236 and 271."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.2",
        version="v0.8.3",
        impact="patch",
        reason=(
            "Register Evan Daniel's n236 and n271 packings (T-218, T-219), raise T-197 to "
            "T-199 to V3/C3, adopt his certificates as the houses at 155, 229, 236 and "
            "271, and correct the credit at 146 and 308."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.8",
        version="v0.4.9",
        impact="patch",
        reason=(
            "Update the registered result count after Evan Daniel's n236 and n271 "
            "packings (T-218, T-219)."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.1",
        version="v0.8.2",
        impact="patch",
        reason=(
            "The development guide describes how test sessions keep their temporary "
            "directories bounded."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.8.0",
        version="v0.8.1",
        impact="patch",
        reason=(
            "Confirm the n68, n84 and n85 fine-net lower bounds T-205 to T-207 at V3/C3 "
            "from retained complete captures, whole-net controls and mapped reviews."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.35",
        version="v0.8.0",
        impact="minor",
        reason=(
            "Open the results page on what was added in the last seven days, day by day, "
            "above the weekly rollup, with an Added filter on the table."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.34",
        version="v0.7.35",
        impact="patch",
        reason=(
            "Simplify the News filters and chooser states, explain News significance "
            "scores in tooltips, and align News cards with the site's styling."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.33",
        version="v0.7.34",
        impact="patch",
        reason=(
            "Map the s(19) Lean proof review onto T-194 (C1), raise T-193 to V3/C3 at its "
            "sixteen counts and stage those houses for the algebraic writer."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.32",
        version="v0.7.33",
        impact="patch",
        reason=(
            "Count a retained formal source build toward verification rather than "
            "confirmation, moving Fitzharding's Lean proof of s(17) (T-154) from V0 to V3 "
            "while it stays at C1."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.31",
        version="v0.7.32",
        impact="patch",
        reason=(
            "Keep Atlas grids at the available width under reduced motion during viewport "
            "changes."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.30",
        version="v0.7.31",
        impact="patch",
        reason=(
            "Adopt T-174 at 37 rational counts with exact house custody, maintained "
            "history and regularized default drawings."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.29",
        version="v0.7.30",
        impact="patch",
        reason=(
            "Document the cached libproc current-RSS contract and installed-SDK native "
            "assurance on macOS."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.28",
        version="v0.7.29",
        impact="patch",
        reason=(
            "Register eighteen fine-net lower bounds, adopt the reviewed n108 bound and "
            "retain its exact audit provenance and safe packet publication."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.7",
        version="v0.4.8",
        impact="patch",
        reason=(
            "Update the registered result count and current bound citations after the "
            "fine-net imports and reviewed n108 adoption."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-optimality-review",
        previous_version="v0.1.7",
        version="v0.1.8",
        impact="patch",
        reason=(
            "Correct Manasseh Ahmed's name and credit Hiroaki Hosono's checker and "
            "formalization reports by name; link reviewed article names to person profiles."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-threshold-bound-review",
        previous_version="v0.1.0",
        version="v0.1.1",
        impact="patch",
        reason=(
            "Credit Hiroaki Hosono's checker and retained tools by name; "
            "link reviewed names in the article to person profiles."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.27",
        version="v0.7.28",
        impact="patch",
        reason=(
            "Document the canonical Rust multiplication default and reproducible "
            "benchmark controls, and refresh the session accounting in the synopsis."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.26",
        version="v0.7.27",
        impact="patch",
        reason=(
            "Register six upper-bound claim rows pending adoption at 155, 227, 229 and "
            "260, retain their chronological source credit, and link the October 18 intake and "
            "open-work reviews."
        ),
    ),
    ReleaseImpactDecision(
        component="infographics",
        previous_version="v0.6.2",
        version="v0.6.3",
        impact="patch",
        reason=(
            "Badge 29's exact side and draw PR #622's certificate, the house at 29 since "
            "17 October 2026."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.25",
        version="v0.7.26",
        impact="patch",
        reason=(
            "Adopt PingYou Ltd's tighter certificate of Thomas Schadt and David "
            "Ellsworth's 29-square packing as the house at 29, and settle its drawing as "
            "decided with no better view."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:square-packing-methods-survey",
        previous_version="v0.2.2",
        version="v0.2.3",
        impact="patch",
        reason=(
            "Figure 3 draws PingYou Ltd's exact rational certificate of the 29-square "
            "packing, the case's house since 17 October 2026."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.24",
        version="v0.7.25",
        impact="patch",
        reason=(
            "Say on the case and result pages that the house rule ended the hold on "
            "T-174's houses and RP-3's wait, naming each staged adoption's bead."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.23",
        version="v0.7.24",
        impact="patch",
        reason=(
            "Serve the atlas posters' v0.6.2 edition, drawn at the 17 October data, and "
            "name it on the readme page."
        ),
    ),
    ReleaseImpactDecision(
        component="infographics",
        previous_version="v0.6.1",
        version="v0.6.2",
        impact="patch",
        reason=(
            "Redraw both atlas posters and every export at the 17 October data, with the "
            "fifteen houses adopted from T-185 to T-190 and the regularized drawings of "
            "16 and 17 October, including 176's."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.22",
        version="v0.7.23",
        impact="patch",
        reason=(
            "Confirm T-185 to T-190 at V3/C3, move the houses at fifteen counts to T-186, "
            "T-187, T-188 and T-190, draw the regularized views of eleven of them, and "
            "record 176, 237, 303 and 304 as decided with no better view."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.21",
        version="v0.7.22",
        impact="patch",
        reason="Draw the regularized views of 175, 232 and 264 by default.",
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.20",
        version="v0.7.21",
        impact="patch",
        reason=(
            "Draw the regularized views of 153, 154, 207, 211, 237, 241 and 302 by "
            "default, and record 304 as decided with no better view."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.19",
        version="v0.7.20",
        impact="patch",
        reason=(
            "Draw the regularized views of 105, 129, 146, 156, 176 and 271 by default, "
            "and record 204, 272 and 303 as decided with no better view."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.18",
        version="v0.7.19",
        impact="patch",
        reason=(
            "Raise Benjamin Greff's s(76) = 9 and s(95) = 10 to V3/C1 on the intake's "
            "recorded reproductions."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.17",
        version="v0.7.18",
        impact="patch",
        reason=(
            "List the October 16 review of Benjamin Greff's mixed covers for s(76) = 9 "
            "and s(95) = 10 in the synopsis document map."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.16",
        version="v0.7.17",
        impact="patch",
        reason=(
            "List the October 16 review of the upper-bound imports T-185 to T-190 in the "
            "synopsis document map."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.15",
        version="v0.7.16",
        impact="patch",
        reason=(
            "List the October 16 review of Oscar Fitzharding's Lean proof that s(19) = 3 "
            "+ 4√2/3 in the synopsis document map."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.14",
        version="v0.7.15",
        impact="patch",
        reason=(
            "Register two results by others in report order, none adopting a house: exact "
            "algebraic sides of the best packings at sixteen counts and a reported Lean "
            "proof that s(19) = 3 + (4/3)√2."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.13",
        version="v0.7.14",
        impact="patch",
        reason=(
            "Say on each case page whose house is drawn that it is drawn as published, and why."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.12",
        version="v0.7.13",
        impact="patch",
        reason=(
            "Use the same canonical articles and topic chips on the homepage and News, "
            "backfill Ahmed's eleven-square optimum, and make navigation consistently "
            "sans."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.11",
        version="v0.7.12",
        impact="patch",
        reason=(
            "Unify News topics, counts and surname style, and announce the newly "
            "registered bound reports as separate articles."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.10",
        version="v0.7.11",
        impact="patch",
        reason=(
            "Register five results in report order, T-188 to T-192, none adopting a "
            "house: smaller reported packings of 211 and 237 squares, a reported s(95) = "
            "10, a reported lower bound for 28 squares and 267 beyond-horizon rows."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.9",
        version="v0.7.10",
        impact="patch",
        reason=(
            "Correct News math and prose, add tutorial credits and update About and "
            "shared site headings."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.8",
        version="v0.7.9",
        impact="patch",
        reason=(
            "Document complete selected CI coverage, scoped News validation and "
            "the distinction between timing reports and execution deadlines."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.7",
        version="v0.7.8",
        impact="patch",
        reason=(
            "Backfill notable News from the past week, show S3 to S5 only, add the "
            "Project topic and labeled-PR intake, and clarify proof copy and meters."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.6",
        version="v0.7.7",
        impact="patch",
        reason=(
            "Complete tutorial launch coverage, clarify the studied counting-certificate "
            "limits and refresh the atlas and explainer downloads."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.6",
        version="v0.4.7",
        impact="patch",
        reason=(
            "Refresh the embedded atlas to the admitted October 15 packings, bounds "
            "and credits, and correct its description of numeric-only recency accents."
        ),
    ),
    ReleaseImpactDecision(
        component="infographics",
        previous_version="v0.6.0",
        version="v0.6.1",
        impact="patch",
        reason=(
            "Refresh both atlas posters to the admitted October 15 packing data, bounds "
            "and credits, with descriptions matching gray case numbers and numeric-only "
            "recency accents."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.5",
        version="v0.7.6",
        impact="patch",
        reason=(
            "Keep routine push and component release validation focused on quick checks "
            "while preserving explicit deep checkpoints."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.4",
        version="v0.7.5",
        impact="patch",
        reason=(
            "Unify News and Explanations headings with original publication dates, refine "
            "significance meters and filters, keep document maintenance out of News, "
            "announce the newly adopted packings, and use bundled fonts for literal "
            "mathematical code symbols."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.3",
        version="v0.7.4",
        impact="patch",
        reason=(
            "Raise the 14 October upper-bound entries to V3/C3 on their stage 4 reviews "
            "and adopt eighteen houses, at 105, 129, 146, 153, 154, 156, 176, 204, 207, "
            "211, 237, 241, 261, 271, 272, 302, 303 and 304, with PR #574's held for the "
            "owner."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.2",
        version="v0.7.3",
        impact="patch",
        reason=(
            "Register three results in report order, T-185 to T-187, none adopting a "
            "house, and bring the requests record and Ryan Xu's credits up to date."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.1",
        version="v0.7.2",
        impact="patch",
        reason=(
            "Credit Ryan Xu by name across the record, record the 14 October replays and "
            "decided comparisons, and add the 13 and 14 October News entries."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.7.0",
        version="v0.7.1",
        impact="patch",
        reason=(
            "Register 24 results from the 14 October intake, none adopting a house: "
            "smaller exact packings and certificates at 69 counts, lower bounds at 37, "
            "39, 44 and 145 to 149, Hiroaki Hosono's closed form, which raises 154 "
            "reported lower bounds, Kevin Fang's n^2 - n + 1 theorem and s(76) = 9."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.6.3",
        version="v0.7.0",
        impact="minor",
        reason=(
            "Add News with significance and topic filters, unify Explanations and split "
            "the tutorial, and let the Atlas use the full available page width."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.6.2",
        version="v0.6.3",
        impact="patch",
        reason=(
            "Add the 14 October intake ledger to the project changelog and state on the "
            "epistemics page that credits name people by name."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.6.1",
        version="v0.6.2",
        impact="patch",
        reason=(
            "List the October 14 reviews and intake ledger in the synopsis document map, "
            "refresh its session rollups, and re-anchor result-page bibliography links to "
            "their entries."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:square-packing-methods-survey",
        previous_version="v0.2.1",
        version="v0.2.2",
        impact="patch",
        reason=(
            "Credit the 12 October adoptions at 154, 175, 232 and 264 in the account of "
            "the adopted houses."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.6.0",
        version="v0.6.1",
        impact="patch",
        reason=(
            "Register four results: a raised lower bound for 40 squares and new exact "
            "packings of 102, 154, 175, 232 and 264 squares, four of which the case "
            "records adopt."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.5",
        version="v0.4.6",
        impact="patch",
        reason=(
            "Explain the two reported 17-square optimality proofs and their V0/C1 "
            "verification limits."
        ),
    ),
    ReleaseImpactDecision(
        component="infographics",
        previous_version="v0.5.0",
        version="v0.6.0",
        impact="minor",
        reason=(
            "Show regularized defaults on both atlas posters with compact attribution and "
            "original-source comparison."
        ),
    ),
    ReleaseImpactDecision(
        component="site",
        previous_version="v0.5.0",
        version="v0.6.0",
        impact="minor",
        reason=(
            "Add the project changelog and an About index of launched results, papers and "
            "downloads."
        ),
    ),
)


class ReleaseNoPublicChange(NamedTuple):
    """A reviewed, path-scoped finding that named component outputs did not change."""

    components: tuple[str, ...]
    paths: tuple[str, ...]
    outputs: tuple[str, ...]
    reason: str


RELEASE_NO_PUBLIC_CHANGES: tuple[ReleaseNoPublicChange, ...] = (
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/upper_bound_reports.py",
            "packing/devtools/upper_bound_sharp_controls.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The sharp-controls subcommand of upper_bound_reports and the module it runs, "
            "upper_bound_sharp_controls (think-jv2s, OR-1), against main 2ec489d1e (#789): "
            "rendered at link revision 2ec489d1 into empty site directories, twice from "
            "this tree at 7cf4ed59 and twice with main's upper_bound_reports.py swapped in "
            "and the new module set aside (69 files each), "
            "render_n11_lower_bounds_explainer, with its pinned Chromium math pass, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write every file byte-identical across all four. "
            "Measured again after merging main 3480b5fd3 (#792, whose upper_bound_reports.py "
            "gains the twin reader): rendered at link revision 3480b5fd into empty site "
            "directories, twice from this tree at 85c6cd7f and twice with that main's "
            "upper_bound_reports.py swapped in and the new module set aside (69 files "
            "each), every file byte-identical across all four. Measured once more after "
            "review A of #796 (the wall enlargement's expected margin, the row helper's name) "
            "and the merge of main dd0061553 (#793): rendered at link revision dd006155, "
            "twice from this tree at 4147f3f9 and twice with that main's "
            "upper_bound_reports.py swapped in and the new module set aside (69 files "
            "each), every file byte-identical across all four. No PDF was printed; each "
            "prints from that HTML. Retain v0.4.27, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/algebraic_witness_reports.py",
            "packing/devtools/build_known_best_atlas.py",
            "packing/devtools/check_standing.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/exact_sides.py",
            "packing/devtools/regularize_evand.py",
            "packing/devtools/regularized_drawings.py",
            "packing/devtools/render_case_pages.py",
            "packing/devtools/render_recent_results.py",
            "packing/devtools/render_research_tables.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/frontier/README.md",
            "packing/frontier/n-070.md",
            "packing/frontier/n-102.md",
            "packing/frontier/n-123.md",
            "packing/frontier/n-153.md",
            "packing/frontier/n-207.md",
            "packing/frontier/n-295.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
            "packing/frontier/square-packing-case.schema.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The house writer's algebraic side and the adoption of the nine algebraic "
            "houses of 23 October 2026 (think-ot5c: T-174 at 70, 153 and 207, T-193 at "
            "102, 123, 258, 259, 295 and 302), their regularization runs, settlements and "
            "re-renders, against main cc91ee1b8 (#746), after merging it: rendered at link "
            "revision 52d23673 into empty site directories, twice from this tree at "
            "52d23673 and twice from main's (69 files each), "
            "render_n11_lower_bounds_explainer, with its pinned Chromium math pass, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write every file byte-identical across all four. "
            "Measured before at 63c12e35 against main 769e441e1 (#748), at fb0889e2 "
            "against 7335d0098 (#752), and at e0c2bf25 and 1a2a7d47 against c1115c095 "
            "(#749), with the same outcome. Measured again after review A of #756 "
            "(the merge of main 0bbb0a2c4, #753 and #754; check_standing's exact order at "
            "an algebraic house; the regularization-owed state; T-193's exact solve in the "
            "case records and case pages; the strict readers; 295's closed form): rendered "
            "at link revision 618cd1f4 into empty site directories, twice from this tree "
            "at 618cd1f4 and twice from main 0bbb0a2c4's (69 files each), every file "
            "byte-identical across all four. No PDF was printed; each prints from that "
            "HTML. Retain v0.4.22, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Issue #732's f1ceee4 release (think-e3im): its 138 beyond-horizon rows at 328 to "
            "989 and their supersessions, the 8 October source's note on the 335 decision "
            "(think-rx26), the #732 request entry and #715's entry at 335: rendered into "
            "empty site directories, twice from this tree and twice from it with main's "
            "result-requests.yaml and source-coverage.yaml swapped in (43 files each), "
            "render_packing_methods writes every file byte-identical across all four, "
            "against main c35b21a14 (#765) at link revision c35b21a1 and again, after "
            "#715's entry changed, against main 14b14f2d1 (#768) at link revision "
            "14b14f2d. Measured once more after review A's fixes (#715's n335 text, the "
            "8 October note and #732's notes) and the merge of main 5f8f005a3 (#766), at "
            "link revision 6d4cc24c, twice from this tree and once with main 5f8f005a3's "
            "two files swapped in: all 43 files byte-identical across the three. No PDF "
            "was printed; it prints from that HTML. Retain v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The #545 grade-C review's request entry (think-7scz), against main c1115c095 "
            "(#749): rendered at link revision c1115c09 into empty site directories, twice "
            "from this tree and twice from it with main's result-requests.yaml swapped in "
            "(43 files each), render_packing_methods writes every file byte-identical "
            "across all four, as it did against main 598d23289 (#742) before the merge. "
            "After review A of #751 reworded the entry and added the source-coverage entry "
            "evand-exact-and-local-reports-2026-10-12, the same four renders, with main's "
            "result-requests.yaml and source-coverage.yaml both swapped in, are again "
            "byte-identical. Measured once more after merging main 7335d0098 (#752), at "
            "link revision 7335d009 with that main's two files swapped in: the same "
            "outcome. No PDF was printed; it prints from that HTML. Retain v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/contributors/people/amund-kristiansen.md",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/site_resources.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "T-239's registration (#755, Amund Kristiansen's s(303), registered as T-238 "
            "and renumbered on 24 October 2026), its stage 4 review (V3/C3, S2), its "
            "adoption at 303 in the pass of 24 October 2026 with its regularization, its "
            "contributor profile, its house reader, the #755 request entry and its gist's "
            "card in Other Square Packing Projects (OTHER_PROJECTS, and source_repository "
            "dropping a gist's revision), against main 0bbb0a2c4 (#753, #760, #754): "
            "rendered at link revision b6ae779b into empty site directories, twice from "
            "this tree and twice from the same tree with main's register, requests record, "
            "coverage record, upper_bound_reports.py, adopt_houses.py, default_drawings.py, "
            "upper_bound_houses.py, overview_sections.py and site_resources.py swapped in "
            "and the new profile set aside (69 files each), render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write every file "
            "byte-identical across all four. Measured before at ea8c6f10 against main "
            "64b316b6c (51 files each), and at 956839d7 against main 7335d0098, at 1c333cfe "
            "against 05e95db36, at 0f7eb786 against 769e441e1 and at 5617791b against "
            "7cd0a94bf (69 files each) without the card, with the same outcome. The "
            "explainer then counted the register (231 to 232 results), its Markdown and "
            "HTML differing from main's inputs' render only there and, in the HTML, in its "
            "version history's link to the new profile, and took v0.4.23. Measured once "
            "more after review A's wording fixes (1f208dfb1: adopt_houses.py and the "
            "register's notes) and the merge of main 2c58b6373 (#745, #750), at link "
            "revision f54ecc25 into empty site directories, twice from this tree and twice "
            "with main's nine candidate inputs swapped in and the new profile set aside "
            "(51 files each): the three papers' files are byte-identical across all four. "
            "The explainer, counting 238 to 239 results, takes v0.4.25 over main's "
            "v0.4.24. No PDF was printed; each prints from that HTML. Retain v0.1.11, "
            "v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/README.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "T-232's registration and adoption at 31 (V3/C3 after the 23 October replay "
            "and review) and T-233's at 19, 20, 26 and 27 (V0/C1), with #446's request "
            "entry, the coverage entries and the Smallest Open Gaps table, where n = 31 "
            "enters second, against main 7335d0098 (#752): rendered at link revision "
            "1d0fba96 into empty site directories, twice from this tree at 3c7f9d11e and "
            "twice from the same tree with main's requests record, frontier README, "
            "register, coverage record, bound citations and composite figure record "
            "swapped in (69 files each), render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write every file "
            "byte-identical across all four. Measured before at 2d32050e4 against main "
            "c1115c095, without the README, with the same outcome, and once more after "
            "merging main 769e441e1 (#751, #748), at link revision b33d7f7d with that "
            "main's six inputs swapped in: the same outcome. Only the explainer's register "
            "count differs (230 to 232). Measured once more after "
            "review A's record fixes (7e12d05ce, 541fea60a), against main 64b316b6c: at link "
            "revision 541fea60 into empty site directories, from this tree and with the 16 "
            "record files those commits change swapped back, all four papers' 69 files are "
            "byte-identical. And after merging main 5f5294d82 (#753: T-231 and the "
            "explainer's v0.4.22), at link revision 5f5294d8 into empty site directories, "
            "from main's tree and from this tree at ea4a21c61 (69 files each): the three "
            "papers' files are byte-identical, and only the explainer's HTML and Markdown "
            "differ, in its register count (231 to 233), so the explainer takes v0.4.23. "
            "Measured once more after merging main 0bbb0a2c4 (#754), at link revision "
            "0bbb0a2c from main's tree and from this tree at 9bbd14ca0: the three papers' "
            "files are again byte-identical, and the explainer differs only in that count "
            "and its v0.4.23 history line. No PDF was printed; each prints from that HTML. "
            "Retain v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/check_source_coverage.py",
            "packing/devtools/intake_ledger.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/README.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The owner's answers of 23 October as rules of the report-order walks "
            "(think-temp, think-8m4k, think-8krd): restatements below the 12-place print "
            "and Göbel's construction as an earlier report beyond 324, the "
            "above-classical-construction disposition with nine rows at 369, 375 and 376 "
            "marked, the T-188 sentence on #613, the requests entries and the frontier "
            "README's rule text, against main c1115c095 (#749): rendered at link revision "
            "d3a09393 into empty site directories from this tree and from the same tree "
            "with main's five candidate inputs swapped in (69 files each), "
            "render_n11_lower_bounds_explainer, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write every "
            "file byte-identical. Measured again at f590f81f4, after the D6 answer's "
            "records and notes, and after review A of #754, A2 included, against main "
            "7cd0a94bf (#747), with main's seven candidate inputs swapped in, "
            "intake_ledger.py and upper_bound_reports.py among them, with the same "
            "outcome; and at bb1cd1338, after review B of #754, against main 64b316b6c "
            "(#762), with the same seven swapped in, with the same outcome. No PDF was "
            "printed; each prints from that HTML. Retain v0.4.21, v0.1.11, v0.1.4 and "
            "v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/check_half_angle_area.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The 23 October closing pass (#747) after its reviews A and B, against main "
            "cc91ee1b8 (#746): the request entries' questions to the authors, holds for the "
            "owner and source-checker notes, T-197 to T-199 citing the source checkers' "
            "replay, T-138's measured lineage, and the identity route's readers of five "
            "earlier entries. Rendered at link revision 26339a13 into empty site "
            "directories from this tree and from the same tree with main's version of "
            "every file this branch modifies swapped in, release.py and tests aside (69 "
            "files each), render_n11_lower_bounds_explainer, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write every file "
            "byte-identical. No PDF was printed; "
            "each prints from that HTML. Retain v0.4.21, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/build_known_best_atlas.py",
            "packing/devtools/flip_regularization.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/render_case_pages.py",
            "packing/devtools/render_frontier_page.py",
            "packing/devtools/render_regularized_atlas.py",
            "packing/devtools/validate_schemas.py",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Flip regularization (think-l2i6, regularization policy section 13), which "
            "draws each count's default picture in its canonical pose on the posters and "
            "the site from its own record and check, against main 7cd0a94bf (#747): "
            "rendered at link revision 7cd0a94b into empty site directories, once from "
            "main and once from this branch after merging it (69 files each), "
            "render_n11_lower_bounds_explainer, with its pinned Chromium math pass, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write all eight papers/ files byte-identical, also "
            "after review round 2 at 140e9ece1. The seven others that differ are the "
            "atlas posters and their exports, which the explainer's build copies to the "
            "site root and the papers link by address: infographics v0.7.0's own outputs. "
            "Measured before at 6b5b479dd against main 7335d0098, with the same outcome. "
            "No PDF was printed; each prints from that HTML. Retain v0.4.21, v0.1.11, "
            "v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/site_resources.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "T-231's registration (#719's lower 204 file, V3/C3 after the 23 October "
            "review), its adoption at 204 in the 24 October pass, T-229's lineage at 204 "
            "and the request entries for #715, #719, #732 and #734, against main c1115c095 "
            "(#749): rendered at link revision 868925d6 into empty site directories, twice "
            "from this tree (at 5b0fcb2a and with v0.4.22 at 8386d394) and twice from "
            "main's (69 files each), render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write every file "
            "byte-identical across all four. The n204 source's card in site_resources "
            "and the 204 page's budget in site_urls (#753's CI), and review A's record "
            "fixes, change none of the 69 files: rendered again at 6f317a6b, ba0cb64e and "
            "ea8e97a1, every file equals the 8386d394 render. Re-measured against main "
            "7335d0098 (#752) after merging it, at c1d1cb7a: the three papers are "
            "byte-identical to main's, and the explainer differs only in its count and "
            "v0.4.22. Again against main 64b316b6c (#747, #748, #761, #762) after merging "
            "it, at 695a0743 with the stage 7 records of 23 October: the same outcome. "
            "The explainer counts the register and takes v0.4.22. No PDF was "
            "printed; each prints from that HTML. Retain v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The 23 October soundness review of wand125's sqverify_continuous (think-xzob, "
            "#533), after review A of #752: its accepted adversarial review item on T-192 "
            "only, T-192 from C0 to C1, next steps and notes on T-145, T-157 and T-192, "
            "#533's ask, and a coverage source for the new key, against main c1115c095 "
            "(#749): rendered at link revision 6c4747f7 into empty site directories, twice "
            "from this tree at 6c4747f7 and twice from the same tree with main's register, "
            "requests record and coverage record swapped in (69 files each), "
            "render_n11_lower_bounds_explainer, with its pinned Chromium math pass, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write every file byte-identical across all four. "
            "Measured before at 8625f55e against the same main, for the register alone, "
            "with the same outcome. The register stays at 230 results. No PDF was printed; "
            "each prints from that HTML. Retain v0.4.21, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The Lean formalization imports of 23 October (#750): T-234 to T-236, their "
            "notes on T-055, T-066 and T-163, and four coverage entries, against main "
            "c1115c095 (#749): rendered at link revision c1115c09 into empty site "
            "directories, twice from this tree at 85512881 and twice from the same tree "
            "with main's register and coverage register swapped in (69 files each), "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write every file byte-identical across all four. The "
            "explainer counts the register (233 entries here, 230 on main) and differs "
            "only there; it takes its successor, v0.4.22, after merging main 77aba4c02. "
            "Measured again at 2b064e103 and c1025d6f1, after T-237, T-238, chelokot's "
            "coverage entry and the [Friedman DS7] bibliography entry, against main "
            "0bbb0a2c4 (#754): at link revision 0bbb0a2c, twice from this tree and twice "
            "with main's version of each of the 16 files the branch modifies swapped in, "
            "release.py and tests aside (69 files each), the three write every file "
            "byte-identical, and the explainer differs only in counting 236 results "
            "against main's 231, so it takes v0.4.23 over main's v0.4.22. Measured "
            "again at 6b739f337, after review A's wording and credit fixes to T-234 to "
            "T-238 and their keys: from that tree, and with d8d5c6774's register, "
            "bibliography and credit manifest swapped in, all four papers write their 69 "
            "files byte-identical, so the explainer keeps v0.4.23. Measured a fourth time "
            "after merging main af9c9e850 (#745: T-232, T-233 and the explainer's v0.4.23 "
            "for 233 results), at link revision af9c9e85, from this tree at e48b9127d and "
            "with main's version of each of the 17 files the branch modifies swapped in, "
            "release.py and tests aside (69 files each): the three write every file "
            "byte-identical, and the explainer differs only in counting 238 results "
            "against main's 233, so it takes v0.4.24 over main's v0.4.23. No PDF was "
            "printed; each prints from that HTML. Retain v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/frontier/results.yaml",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The 23 October significance review of T-154, T-155 and T-156 (think-7j5d), "
            "which keeps their scores at S5, S1 and S1 and rewrites only their "
            "significance rationale, scored date and by, against main 598d23289 (#742): "
            "rendered at link revision 26339a13 into empty site directories from this "
            "tree and from the same tree with main's register swapped in (69 files "
            "each), render_n11_lower_bounds_explainer, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write every "
            "file byte-identical. Measured before against main 44df28b07 (#743), with "
            "the register edit stashed, with the same outcome. No PDF was printed; each "
            "prints from that HTML. Retain v0.4.21, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/check_results.py",
            "packing/devtools/check_source_coverage.py",
            "packing/devtools/site_resources.py",
            "packing/devtools/source_supersession.py",
            "packing/devtools/state_ai_assistance.py",
            "packing/frontier/README.md",
            "packing/frontier/n-011.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The record-integrity gates of the 1 October import review (think-nr59, "
            "think-du1e, think-g6d5, think-506q, think-j5so, think-mt6e), their record "
            "repairs (T-115's significance.by, T-086's review mapping, seven coverage "
            "sources with cards for the four that had none, n-011's AI-assistance "
            "sentence) and review A's fixes, against main c1115c095 (#749): rendered at "
            "link revision 868925d6 into empty site directories, twice from this tree at "
            "064648b9 and twice with main's versions of the 23 changed paths (69 files "
            "each), render_n11_lower_bounds_explainer, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write every file "
            "byte-identical across all four; measured before against main 44df28b07 and "
            "598d23289 with the same outcome. The explainer reads n-011's front matter, not "
            "the sentence added to its body, the papers print no project card, and the "
            "register stays at 230 results. source_supersession.py, changed after those "
            "renders, only caches its parse of the coverage register by the file's text, "
            "a source review with its 378 dependent tests passing; the papers select it as "
            "a broad builder input. No PDF was printed; each prints from that HTML. "
            "Retain v0.4.21, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "TUTORIAL.md",
            "packing/devtools/overview_sections.py",
            "packing/devtools/render_contributors.py",
            "packing/devtools/render_overview.py",
            "packing/devtools/site_assets.py",
            "packing/devtools/site_documents.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/templates/paper-publication.css",
            "packing/devtools/templates/paper-type.css",
            "packing/devtools/templates/site-nav.css",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "PR743 tutorial and site follow-ups against main 31584003e: source review "
            "finds no paper manuscript or mathematical figure changes. Tutorial changes "
            "preserve the cited anchors; reader rendering and removed daily/weekly views "
            "do not generate paper bodies. The new generated-image asset helper is used "
            "only by tutorials; its two registered URL patterns do not affect paper output. "
            "Existing image_file output is unchanged. Shared CSS replaces "
            "24rem and "
            "0.85rem/1rem literals with equal-valued tokens. New caption presentation is "
            "scoped to site reader documents, preserving paper caption alignment. "
            "Independent Chromium review of the four retained paper HTML outputs found "
            "no caption paragraph descendants; the broader "
            "alignment rule discovered in that review was corrected. Navigation changes "
            "are site chrome; validation changes affect CI ownership only. CSS bytes "
            "change, but these inputs do not revise paper content or typesetting. "
            "This is a source and DOM review, not a claim of PDF byte equality."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "T-230's registration (#728, V3/C3 after the 22 October review), its adoption at "
            "303 in the 23 October pass and the request entries for #522, #526 and #728, "
            "against main fcf2f96a5 (#730), after review A's record fixes: rendered at link "
            "revision 868925d6 into empty site directories, twice from this tree at 5cb3191c "
            "with this record and twice from main's, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write every file "
            "byte-identical across all four. The explainer counts the register and took "
            "v0.4.20. No PDF was printed; each prints from that HTML. Retain v0.1.10, "
            "v0.1.3 and v0.2.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Issue #732's 77 beyond-horizon rows at 325 to 1024 and their supersessions, and "
            "the request entries for #732, the four stage 7 replies after #730, #728's final "
            "reply, #526's correction and the final replies closing #582, #584, #624 and "
            "#675, against main 44df28b07 (#743): rendered at link revision 868925d6 into "
            "empty site directories, twice from this tree at 24fe305e and twice from main's "
            "(43 files each), render_packing_methods writes every file byte-identical across "
            "all four. Measured before against main fcf2f96a5, 6c70d843f and 31584003e with "
            "the same outcome. No PDF was printed; it prints from that HTML. Retain #737's "
            "v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The 23 October sweep's request entries (#719's answers, #732, #734) and the "
            "stage 7 follow-ups after #725, against main 690e21857 (#738): rendered at link "
            "revision 40a71b16 into empty site directories, twice from this tree at "
            "d40979ad with this record and twice from main's (42 files each), "
            "render_packing_methods writes every file byte-identical across all four. No "
            "PDF was printed; it prints from that HTML. Retain v0.2.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/render_overview.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Speculation rules on the site's own pages (think-gr4c): render_overview gains "
            "SPECULATION_RULES and speculation_rules_tag, which kpress_page and "
            "static_content_page add after head_tags; head_tags itself, which writes the "
            "papers' heads, is unchanged. Rendered at link revision e929137a into empty "
            "directories, once from this tree and twice from main e929137a8 (#725): the "
            "four renderers write 68 files each, none carrying the rules, byte-identical "
            "except one span's style attribute in the explainer's HTML, whose place varies "
            "between renders (the record below). No PDF was printed; each prints from that "
            "HTML. Retain v0.4.19, v0.1.10, v0.1.3 and v0.2.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/news_highlights.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/probes/check_site_rendering/report.js",
            "packing/devtools/render_changelog.py",
            "packing/devtools/render_overview.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "#736, the home page's News box filter and Recently Added (think-aqv8, "
            "think-rqen), against main cddc5843f (#733): rendered at link revision "
            "6610be93 into empty site directories, twice from this tree at 031619415 and "
            "twice from main's (68 files each). render_n11_lower_bounds_explainer, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write every file byte-identical across the two trees; "
            "the explainer's HTML differs between two renders of main's own tree in one "
            "span's attributes, and this tree's second render equals main's second in all "
            "68 files. Re-measured once from each tree after merging main bfc04b659 "
            "(#735), after main e929137a8 (#725) at its link revision 40a71b16, and after "
            "review A's fixes and main 0b2c8293c (#406) at f73d8d4a8: the same, the "
            "explainer's one span aside. Re-measured after review A's second round and "
            "main 6c70d843f (#731), both trees at link revision 01e2ca3e: all 68 files "
            "byte-identical. After main 31584003e (#737) at link revision 947d2863, "
            "after main 44df28b07 (#743) at d449eacc, after main da117ad0b (#742 to #764), "
            "when the branch was taken over (think-xae5), at e1f1adc4, and last after main "
            "14b14f2d1 (#765, #767, #768) at 95ac0de5: rendered from the merge and from the "
            "merge with these five paths at main's, all 69 files byte-identical each time. "
            "Last after main e5c1c64e3 (#745 to #771) and review B's fixes (B1, B2, B5 in "
            "news_highlights.py, overview_sections.py and render_overview.py), at link "
            "revision c0ce843f: rendered from the tree and from the tree with these five "
            "paths at main's, all 69 files byte-identical. No PDF was printed; each prints "
            "from that HTML. Retain main's v0.4.25, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Couzo's watched history at 325 to 1024 (#730: 319 beyond-horizon rows, the "
            "T-188, T-189 and T-191 notes, #715's and #624's request texts, review A's "
            "date-free wording) against main e929137a8 (#725): rendered at link revision "
            "6610be93 into empty site directories from this tree at 400a2dae and from "
            "main's (68 files each). render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write their "
            "HTML and Markdown byte-identical, and the explainer its Markdown; the "
            "explainer's HTML differs only in the order of attributes on a math span, "
            "which a second render of one tree reorders too, and is identical once they "
            "are normalized. Measured before against main 59b1ec594 and bfc04b659 with "
            "the same outcome. No PDF was printed; each prints from that HTML. Retain "
            "#733's v0.4.19, v0.1.10, v0.1.3 and v0.2.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/n-105.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Stage 4 of T-226 to T-229 (V3/C3 after the 22 October reviews, T-229 adopted "
            "at 105 and 204 and regularized, the replies after #722) against main "
            "bfc04b659 (#733, #735): rendered at link revision 40a71b16 into empty site "
            "directories, twice from this tree at 720648d3 and twice from main's (68 files "
            "each), render_n11_lower_bounds_explainer, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write every "
            "file byte-identical across all four, except one span's style attribute in "
            "the explainer's HTML, whose place varies between two renders of one tree. "
            "The register stays at 229 results. No PDF was printed; each prints from that "
            "HTML. Retain #733's v0.4.19, v0.1.10, v0.1.3 and v0.2.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/site_urls.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The #719 import (T-229 at 105 and 204, 111 beyond-horizon rows, the replies "
            "after #720, results.html's ceiling) against main 78dc902c1 (#727): rendered "
            "at link revision 6610be93 into empty site directories, twice from this tree "
            "at a9b8d809 and twice from main's (68 files each), "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write their HTML and Markdown byte-identical across "
            "all four; only the explainer's register count differs (228 to 229), and it "
            "took v0.4.18. No PDF was printed; each prints from that HTML. Retain v0.1.9, "
            "v0.1.2 and v0.2.5."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The v0.8.20 cut for PR-B moved the claim documents' link revision, d39f458c "
            "to cadf73fd, in 22 lines. Rendered into empty site directories from this "
            "tree after the cut and from main 7359fa8b's: the explainer and the other "
            "three papers write 68 byte-identical files. Retain v0.4.15."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/n-103.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "PR-B of the 22 October backlog (205 beyond-horizon rows of #666, #670, #672 "
            "and #675, review B of #718, the replies after #718 and #643's) against main "
            "7359fa8b: rendered at link revision b8045210 into empty site directories from "
            "this tree at cfeb44cc, again at 9efff725 after the hosted findings' fixes to "
            "adopt_houses.py and overview_sections.py, and from main's, "
            "render_n11_optimality_review, "
            "render_n11_threshold_bound_review, render_packing_methods and "
            "render_n11_lower_bounds_explainer write 68 files, byte-identical among the "
            "three. After review A's repoint of 77 start rows in source-coverage.yaml, "
            "rendered again at link revision 728dc883 from this tree at cecd6e26 and from "
            "main's: the same 68 files, byte-identical between the two. No PDF was "
            "printed; each prints from that HTML. Retain v0.4.15, v0.1.7, v0.1.0 and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The v0.8.18 cut for #715 moved the claim documents' link revision, 18a1fb61 "
            "to 9da60d47, in 22 lines. Rendered into empty site directories from this "
            "tree and with main d7923b8d's copies of the five: 54 byte-identical files. "
            "Retain v0.4.14."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "For the #715 import (Francisco Couzo's 109 new beyond-horizon rows at or "
            "below 1024, and the #715 and #678 replies) against main d7923b8d: the survey "
            "cites neither the #715 request nor the couzo-issue715-2026-10-21 source. "
            "Rendered at link revision 56dc2454 into empty site directories, from this tree "
            "and with main's copies of the two inputs: render_packing_methods writes 42 "
            "byte-identical files. No PDF printed; it prints from that HTML. Retain v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/result_credit.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "T-225's stage 4 review and rise to V3/C3, its adoption at 204, 227, 229 and "
            "260, and the registration of Francisco Couzo's #670, #672 and #675 rows "
            "(T-226 to T-228), against main d7923b8d. Rendered at link revision ab006e47 "
            "into empty site directories, twice from this tree at ba8b3cc9 and twice from "
            "main's: render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write their HTML and Markdown byte-identical across all "
            "four renders; only the explainer, which counts the register, differs, and it "
            "takes v0.4.15. Rendered the same way again at link revision da2671cf, from "
            "this tree at 369db682, after the rigidity blocks and t-180's page budget: the "
            "same three byte-identical. Re-taken against main de1651e1 (#717, #715's rows), "
            "after merging it: rendered at link revision 653597be, twice from this tree at "
            "089cf042 and twice from main's, the same three byte-identical and the explainer "
            "differing only in its edition and register count; the survey again at "
            "68b17200, after the four reply records of 22 October, its 42 files "
            "byte-identical to main's; and all four again at link revision 00e3de37, from "
            "this tree at f6457df8 after review A's fixes, the same three byte-identical and "
            "the explainer differing only in its edition and register count. No PDF was "
            "printed; each prints from that HTML. Retain v0.1.7, v0.1.0 and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/overview_sections.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The registration of Evan Daniel's regularized views (T-225), the #668 and "
            "#702 replies, the texts after #704 and #706 and T-196's and T-223's News, "
            "against main bb0c24e9, after merging it. Rendered at link revision 818f10bd "
            "into empty site directories, twice from this tree and twice with main's copies "
            "of these five inputs: render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write their HTML "
            "and Markdown byte-identical across all four renders; only the explainer, which "
            "counts the register, differs, and it takes v0.4.14. Rendered the same way again "
            "at 1300bc76, after the #678, #668 and #715 records and the overview's Couzo "
            "card, and at 3b8bd62e and fb58349a, after review A of #716, T-225's 22 October "
            "stamp and the reading of Couzo's answers on #678: the same three byte-identical. "
            "No PDF was printed; each prints from that HTML. Retain v0.1.7, v0.1.0 and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The v0.8.14 cut for #702 moved the claim documents' link revision, 902c92d9 "
            "to 642464f8, in 22 lines. Rendered into empty site directories from this "
            "tree and with main 51ac9d7e's copies of the five: 54 byte-identical files. "
            "Retain v0.4.13."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "For the #702 import (Evan Daniel's s(343) beyond-horizon row, superseding "
            "#678's row at 343) against main 51ac9d7e: the survey cites neither the #702 "
            "request nor the n343 source. Rendered at link revision 869bcac0 into an empty "
            "site directory, from this tree and with main's copies of the two inputs: "
            "render_packing_methods writes 42 byte-identical files. No PDF printed; it "
            "prints from that HTML. Retain v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/campaign/result-requests.yaml",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/couzo_678_replay.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Issue 678's stage 4 and house best packing adoption (T-223 at V3/C3, the "
            "house at 204 since 20 October and at 260 since 21 October 2026, from T-196) "
            "against main 970e89de, after merging it, and this branch's site v0.8.16 cut, "
            "which regenerates the five claim documents with only their source-link "
            "revision changed, 5e16f345 to 96a0d9ff. Rendered at link revision 02eef374, the "
            "merge, twice from its tree and twice with main's copies of the twelve other "
            "inputs, and again at 7bb219c7, the cut, twice from its tree and twice with "
            "main's bytes of all seventeen: render_n11_optimality_review, "
            "render_n11_threshold_bound_review, render_packing_methods and "
            "render_n11_lower_bounds_explainer write 68 files, byte-identical across each "
            "four. No PDF was printed; each prints from that HTML. Retain v0.4.13, v0.1.7, "
            "v0.1.0 and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/adopt_houses.py",
            "packing/frontier/n-154.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered at 1bcbe222 and with main 2e6d528d's copies of these paths: 68 "
            "byte-identical files, no PDF."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/overview_sections.py",
            "packing/devtools/run_negative_controls.py",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Issue 686's import against main 9dda9224. The v0.8.12 cut changed only the "
            "claim documents' link revision, fbb3d573 to 45f1918d, and the explainer links "
            "them. The survey cites the requests and coverage records without inlining "
            "them; the snapshot prune and issue 686's card reach no paper. With main's "
            "copies of the other four inputs, the four renderers write 68 byte-identical "
            "files at link revision 255049cb, and after review A's record edits the "
            "survey's HTML and Markdown again at 8fd21bb6. Retain v0.4.13, v0.1.7, v0.1.0 "
            "and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Reviewed October 21, 2026 against main d640ad8f for the records lane of 21 "
            "October (think-xl9i: review B of #708, the #703 final reply and closure, and "
            "the 703 review's erratum). results.yaml changes only T-224's significance "
            "rationale, outside the n11 ladder rungs paper_figures reads; adopt_houses.py "
            "only T-224's lineage paragraph and the 270 credit; result-requests.yaml only "
            "the #703 entry. Rendered with render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods at link revision "
            "b90a9312, the branch head, once from its tree and once with main's copies of "
            "those three inputs, n-270.md and the five claim documents: the 50 files the "
            "three write are byte-identical. Rendered the same way again at f021abc3, after "
            "review A of #710 changed the #703 entry's note and final reply: byte-identical "
            "again. No PDF was printed; each prints from that HTML. Retain v0.1.7, v0.1.0 "
            "and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/adopt_houses.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Reviewed October 21, 2026 against main d640ad8f for the records lane of 21 "
            "October (think-xl9i). The site v0.8.11 cut regenerated the five claim "
            "documents, and each of the 22 changed lines differs from main only in its "
            "source-link revision, d798819c to fbb3d573; the explainer links them rather "
            "than inlining them. results.yaml changes only T-224's significance rationale "
            "and adopt_houses.py only T-224's lineage paragraph and the 270 credit; the "
            "register's counts and the n11 citation the explainer reads are unchanged. "
            "Rendered with the browser's math pass at the branch head b90a9312, once from "
            "its tree and once with main's copies of results.yaml, adopt_houses.py, "
            "result-requests.yaml, n-270.md and the five claim documents: the 54 files it "
            "writes, its HTML and Markdown and the files at the site root, are "
            "byte-identical. It keeps v0.4.13; no PDF was printed, and it prints from that "
            "HTML."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review", "paper:n11-threshold-bound-review"),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/render_n11_lower_bounds_explainer_pdf.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
        ),
        reason=(
            "For the #703 lane of 21 October (T-224 at n = 270, its stage 4 review and "
            "its adoption as the house best packing at 270) against main a5bdb96a: both "
            "reviews read results.yaml only through paper_figures.ladder_records, which "
            "selects the n11 ladder rungs LADDER_RUNGS names and holds them to "
            "LADDER_DIGEST; T-224 and the 270 regularized-drawing item are outside that "
            "ladder, and no ladder row changes. adopt_houses.py gains T-224's prose, the "
            "270 credit and a string form of Prose.third_route; upper_bound_houses.py the "
            "packet, 270 in ADOPTED and the 21 October pass; upper_bound_reports.py one "
            "house reader. render_n11_lower_bounds_explainer_pdf.py changes only "
            "EXPECTED_PAGE_COUNT, the explainer's pagination check; these producers "
            "import its dated helper. Rendered at link revision 667fed68, once from this "
            "branch's tree and once with main's copies of the seven changed inputs "
            "(these five, result-requests.yaml and source-coverage.yaml): "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods leave the 50 files they write byte-identical between "
            "the trees. No PDF was printed; each prints from that HTML. Retain v0.1.7 "
            "and v0.1.0."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/render_n11_lower_bounds_explainer_pdf.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "For the #703 lane of 21 October (T-224 at n = 270, its stage 4 review and "
            "its adoption as the house best packing at 270) against main a5bdb96a: "
            "result requests, source coverage and results are citation targets whose "
            "existence the producer checks, not inlined text, and every cited path exists "
            "at both revisions; the #703 request, the n270 coverage source and the 270 "
            "override, and T-224 are not cited by the survey. adopt_houses.py, "
            "upper_bound_houses.py and upper_bound_reports.py change only the 270 "
            "adoption's writer inputs and one house reader, which do not enter its "
            "output; render_n11_lower_bounds_explainer_pdf.py, a render input, changes "
            "only EXPECTED_PAGE_COUNT, which the survey's producer does not read. "
            "Rendered at link revision 667fed68, once from this branch's tree and once "
            "with main's copies of the seven changed inputs: render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods leave the 50 "
            "files they write byte-identical between the trees. No PDF was printed; it "
            "prints from that HTML. Retain v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Reviewed October 21, 2026 against main 6b825f44 for the records lane of 21 "
            "October that records the replies posted on #664, #669 and #702 after #707 "
            "merged. result-requests.yaml changes only those three entries: three replies "
            "recorded, #664 closed, #702's blocked_on on #701 and its wait dropped, and "
            "each entry's notes brought up to date. Rendered with render_packing_methods "
            "at link revision 6b825f44, at the branch head 8ab7d264, once from its tree "
            "and once with main's result-requests.yaml: all 42 files it writes are "
            "byte-identical. No PDF was printed; it prints from that HTML. Retain v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/evand_arrangement_reports.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "For PR #704 (T-196's replay, its stage 4 review and its adoption at 227 and "
            "260) against main 99cfcc8a: the explainer reads results.yaml only for its "
            "count of entries and of novel ones, and T-196 changes neither; the bound "
            "citations and the composite figure record change at 227 and 260 only, which it "
            "does not draw; validate.py changes only the translation screen's sums; the "
            "house writer, house sources, adapter docstring and the kernel's sharp controls "
            "are not called by it; the site v0.8.7 cut changes the five claim documents "
            "only in their source-link revision, and the explainer links them rather than "
            "inlining them. "
            "Rendered at link revision 9acc078a, this branch after its merge of main "
            "99cfcc8a (#699, site v0.8.6) and its v0.8.7 cut, once from this branch's tree "
            "and once from a scratch copy holding main's bytes of the fifteen changed "
            "inputs (the five claim documents, bound-citations.json, composite-figure.json, "
            "adopt_houses, evand_arrangement_reports, upper_bound_houses, "
            "upper_bound_reports, validate.py, results.yaml, result-requests.yaml and "
            "source-coverage.yaml): render_n11_optimality_review, "
            "render_n11_threshold_bound_review, render_packing_methods and "
            "render_n11_lower_bounds_explainer write 68 files. 67 are byte-identical "
            "between the trees, and the explainer's HTML is identical once each tag's "
            "attributes are sorted: its browser math step orders a math span's style "
            "attribute differently from run to run, as three renders of main's tree "
            "showed on the branch's earlier head. No PDF was printed; each prints from "
            "that HTML. "
            "Re-taken by source review after the merge of main 4851d8193 (#705, site "
            "v0.8.7): #705 changes none of these inputs but the five claim documents, "
            "which the v0.8.8 cut regenerates and which differ from main's only in their "
            "source-link revision, 9cd35d1e to fe6f350d. "
            "Re-taken by source review after the merge of main e7de85ff6 (#701, site "
            "v0.8.8, explainer v0.4.12): of these inputs #701 changes the five claim "
            "documents, which the v0.8.9 cut regenerates and which differ from main's only "
            "in their source-link revision, and results.yaml, where its T-223 is in both "
            "trees and this branch's edits, T-196's and T-223's note on the house best "
            "packing at 260, still change neither count. "
            "run_negative_controls.py, changed after that merge, changes only the worker "
            "snapshot's UNREAD_WORKER_OUTPUTS and its comments, and importing each of the "
            "four producers loads no devtools.run_negative_controls. "
            "Re-taken by source review after review B of #704: its fixes change T-196's "
            "notes in results.yaml, which name T-223 and change neither count; the "
            "house writer's override reason, check and refresh in adopt_houses and "
            "its 70 reasons in source-coverage.yaml, which the explainer does not read; "
            "and comments in upper_bound_houses and run_negative_controls, which no "
            "producer loads. "
            "Re-taken by source review after the merge of main 6b825f441 (#707, site "
            "v0.8.9): of these inputs #707 changes the five claim documents, which the "
            "v0.8.10 cut regenerates and which differ from main's only in their "
            "source-link revision; results.yaml, where T-197's, T-219's, T-221's and "
            "T-222's prose leaves both counts at 223 entries and 32 novel ones; "
            "adopt_houses.py, which the explainer does not load; and "
            "bound-citations.json at 271 only. "
            "Re-taken after the merge of main 51ac9d7ee (#708 to #713, site v0.8.13, "
            "explainer v0.4.13). That merge withdrew this branch's site v0.8.10 cut, so "
            "the five claim documents are main's and leave these paths, and the next "
            "commit withdrew its change to run_negative_controls.py (review B4). "
            "Rendered at link revision fd7f939e, once from this branch's tree and once "
            "with main's bytes of the ten changed inputs (bound-citations.json, "
            "composite-figure.json, result-requests.yaml, adopt_houses, "
            "evand_arrangement_reports, upper_bound_houses, upper_bound_reports, "
            "results.yaml, source-coverage.yaml and validate.py): "
            "render_n11_optimality_review, render_n11_threshold_bound_review, "
            "render_packing_methods and render_n11_lower_bounds_explainer, the last with "
            "its pinned Chromium math pass, write 68 files, all byte-identical between "
            "the trees. No PDF was printed; each prints from that HTML. "
            "Re-taken after the merge of main 7eeab1f5e (#714, #712, site v0.8.14) and "
            "this branch's site v0.8.15 cut, which regenerates the five claim documents "
            "with only their source-link revision changed, 642464f8 to 5e16f345, and "
            "after the custody note's new reading in upper_bound_houses. Rendered at "
            "link revision 30ba79d8, the cut, once from this branch's tree and once "
            "with main's bytes of the fifteen changed inputs (the ten above and the "
            "five claim documents): the four renderers write 68 files, all "
            "byte-identical between the trees. No PDF was printed. "
            "Retain v0.4.13."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review", "paper:n11-threshold-bound-review"),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/evand_arrangement_reports.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
        ),
        reason=(
            "For PR #704 (T-196's replay, its stage 4 review and its adoption at 227 and "
            "260) against main 99cfcc8a: both reviews read results.yaml only through "
            "paper_figures.ladder_records, which selects the n11 ladder rungs LADDER_RUNGS "
            "names; T-196 is outside that ladder and no ladder row changes. The house "
            "writer, house sources, adapter docstring and the kernel's sharp controls are "
            "not called by these producers. "
            "Rendered at link revision 9acc078a, this branch after its merge of main "
            "99cfcc8a (#699, site v0.8.6) and its v0.8.7 cut, once from this branch's tree "
            "and once from a scratch copy holding main's bytes of the fifteen changed "
            "inputs (the five claim documents, bound-citations.json, composite-figure.json, "
            "adopt_houses, evand_arrangement_reports, upper_bound_houses, "
            "upper_bound_reports, validate.py, results.yaml, result-requests.yaml and "
            "source-coverage.yaml): render_n11_optimality_review, "
            "render_n11_threshold_bound_review, render_packing_methods and "
            "render_n11_lower_bounds_explainer write 68 files. 67 are byte-identical "
            "between the trees, and the explainer's HTML is identical once each tag's "
            "attributes are sorted: its browser math step orders a math span's style "
            "attribute differently from run to run, as three renders of main's tree "
            "showed on the branch's earlier head. No PDF was printed; each prints from "
            "that HTML. "
            "Re-taken by source review after the merge of main 4851d8193 (#705, site "
            "v0.8.7), which changes none of these inputs, and after the merge of main "
            "e7de85ff6 (#701, site v0.8.8), which adds T-223 to results.yaml outside the "
            "n11 ladder; this branch edits only T-223's notes there. "
            "run_negative_controls.py, changed after that merge, changes only the worker "
            "snapshot's UNREAD_WORKER_OUTPUTS and its comments, and importing each of the "
            "four producers loads no devtools.run_negative_controls. "
            "Re-taken by source review after review B of #704: its fixes change T-196's "
            "notes in results.yaml, outside the n11 ladder, the house writer's "
            "override reason, check and refresh in adopt_houses, and comments in "
            "upper_bound_houses and run_negative_controls, none of which these "
            "producers call. "
            "Re-taken by source review after the merge of main 6b825f441 (#707, site "
            "v0.8.9), whose results.yaml prose is outside the n11 ladder and whose "
            "adopt_houses.py prose these producers do not call. "
            "Re-taken after the merge of main 51ac9d7ee (#708 to #713, site v0.8.13, "
            "explainer v0.4.13). That merge withdrew this branch's site v0.8.10 cut, so "
            "the five claim documents are main's and leave these paths, and the next "
            "commit withdrew its change to run_negative_controls.py (review B4). "
            "Rendered at link revision fd7f939e, once from this branch's tree and once "
            "with main's bytes of the ten changed inputs (bound-citations.json, "
            "composite-figure.json, result-requests.yaml, adopt_houses, "
            "evand_arrangement_reports, upper_bound_houses, upper_bound_reports, "
            "results.yaml, source-coverage.yaml and validate.py): "
            "render_n11_optimality_review, render_n11_threshold_bound_review, "
            "render_packing_methods and render_n11_lower_bounds_explainer, the last with "
            "its pinned Chromium math pass, write 68 files, all byte-identical between "
            "the trees. No PDF was printed; each prints from that HTML. "
            "Re-taken after the merge of main 7eeab1f5e (#714, #712, site v0.8.14) and "
            "this branch's site v0.8.15 cut, which regenerates the five claim documents "
            "with only their source-link revision changed, 642464f8 to 5e16f345, and "
            "after the custody note's new reading in upper_bound_houses. Rendered at "
            "link revision 30ba79d8, the cut, once from this branch's tree and once "
            "with main's bytes of the fifteen changed inputs (the ten above and the "
            "five claim documents): the four renderers write 68 files, all "
            "byte-identical between the trees. No PDF was printed. "
            "Retain v0.1.7 and v0.1.0."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/evand_arrangement_reports.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "For PR #704 (T-196's replay, its stage 4 review and its adoption at 227 and "
            "260) against main 99cfcc8a: result requests, source coverage and results are "
            "citation targets whose existence the producer checks, not inlined text, and "
            "every cited path exists at both revisions; the #668 request, its coverage rows "
            "and T-196 are not cited by the survey, and the house writer, house sources, "
            "adapter and kernel do not enter its output. "
            "Rendered at link revision 9acc078a, this branch after its merge of main "
            "99cfcc8a (#699, site v0.8.6) and its v0.8.7 cut, once from this branch's tree "
            "and once from a scratch copy holding main's bytes of the fifteen changed "
            "inputs (the five claim documents, bound-citations.json, composite-figure.json, "
            "adopt_houses, evand_arrangement_reports, upper_bound_houses, "
            "upper_bound_reports, validate.py, results.yaml, result-requests.yaml and "
            "source-coverage.yaml): render_n11_optimality_review, "
            "render_n11_threshold_bound_review, render_packing_methods and "
            "render_n11_lower_bounds_explainer write 68 files. 67 are byte-identical "
            "between the trees, and the explainer's HTML is identical once each tag's "
            "attributes are sorted: its browser math step orders a math span's style "
            "attribute differently from run to run, as three renders of main's tree "
            "showed on the branch's earlier head. No PDF was printed; each prints from "
            "that HTML. "
            "Re-taken by source review after the merge of main 4851d8193 (#705, site "
            "v0.8.7), which changes none of these inputs, and after the merge of main "
            "e7de85ff6 (#701, site v0.8.8), whose T-223, #678 request and coverage rows "
            "the survey does not cite either. "
            "run_negative_controls.py, changed after that merge, changes only the worker "
            "snapshot's UNREAD_WORKER_OUTPUTS and its comments, and importing each of the "
            "four producers loads no devtools.run_negative_controls. "
            "Re-taken by source review after review B of #704: its fixes change T-196's "
            "notes in results.yaml, the de Winter source's note and the 70 adoption "
            "override reasons in source-coverage.yaml, none of which the survey cites, "
            "and the house writer's reason, check and refresh in adopt_houses and "
            "comments in upper_bound_houses and run_negative_controls, which do not "
            "enter its output. "
            "Re-taken by source review after the merge of main 6b825f441 (#707, site "
            "v0.8.9), whose result-requests.yaml entries, results.yaml prose and "
            "adopt_houses.py prose the survey does not cite. "
            "Re-taken after the merge of main 51ac9d7ee (#708 to #713, site v0.8.13, "
            "explainer v0.4.13). That merge withdrew this branch's site v0.8.10 cut, so "
            "the five claim documents are main's and leave these paths, and the next "
            "commit withdrew its change to run_negative_controls.py (review B4). "
            "Rendered at link revision fd7f939e, once from this branch's tree and once "
            "with main's bytes of the ten changed inputs (bound-citations.json, "
            "composite-figure.json, result-requests.yaml, adopt_houses, "
            "evand_arrangement_reports, upper_bound_houses, upper_bound_reports, "
            "results.yaml, source-coverage.yaml and validate.py): "
            "render_n11_optimality_review, render_n11_threshold_bound_review, "
            "render_packing_methods and render_n11_lower_bounds_explainer, the last with "
            "its pinned Chromium math pass, write 68 files, all byte-identical between "
            "the trees. No PDF was printed; each prints from that HTML. "
            "Re-taken after the merge of main 7eeab1f5e (#714, #712, site v0.8.14) and "
            "this branch's site v0.8.15 cut, which regenerates the five claim documents "
            "with only their source-link revision changed, 642464f8 to 5e16f345, and "
            "after the custody note's new reading in upper_bound_houses. Rendered at "
            "link revision 30ba79d8, the cut, once from this branch's tree and once "
            "with main's bytes of the fifteen changed inputs (the ten above and the "
            "five claim documents): the four renderers write 68 files, all "
            "byte-identical between the trees. No PDF was printed. "
            "Retain v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/adopt_houses.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Reviewed October 21, 2026 against main e7de85ff for the records lane of 21 "
            "October (think-8z7k, #664's credit at 271, #669's by-field answer). The site "
            "v0.8.9 cut regenerated the five claim documents, and each of the 22 changed "
            "lines differs from main only in its source-link revision, ec95f0b8 to "
            "f555a0f9; the explainer links them rather than inlining them. results.yaml "
            "changes only T-197's, T-219's, T-221's and T-222's prose, adopt_houses.py "
            "only the 271 credit and T-219's and T-222's prose, and bound-citations.json "
            "only the 271 upper citation's text; the register's counts and the n11 "
            "citation the explainer reads are unchanged. Rendered at the branch head "
            "db61aefd, once from its tree and once with main's results.yaml, "
            "adopt_houses.py, n-154.md, result-requests.yaml and bound-citations.json: its "
            "HTML and Markdown and the files it writes at the site root are byte-identical. "
            "A pair of renders at 7d67be1f differed only in where the browser math "
            "preparation serializes an empty style attribute on two math spans, as in the "
            "#446 disposition. It keeps v0.4.11; no PDF was printed, and it prints from "
            "that HTML."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/frontier/n-154.md",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Reviewed October 21, 2026 against main e7de85ff for the records lane of 21 "
            "October (think-8z7k, #664's credit at 271, #669's by-field answer, #689 and "
            "#694 closed, #702 triaged). results.yaml changes only T-197's, T-219's, "
            "T-221's and T-222's prose, outside the n11 ladder rungs paper_figures reads; "
            "adopt_houses.py only the 271 credit and T-219's and T-222's prose; n-154.md "
            "one sentence of T-222's section; and result-requests.yaml only the #664, #669, "
            "#674, #678, #689, #694 and #702 entries. Rendered with "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods at link revision e7de85ff, at the branch head "
            "db61aefd, once from its tree and once with main's "
            "copies of those four inputs and bound-citations.json: the files the three "
            "write are byte-identical. No PDF was printed; each prints from that HTML. "
            "Retain v0.1.7, v0.1.0 and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/result_status.py",),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "For PR #701's review A (finding A5): unfinished_sentence now adds its full "
            "stop only where an unfinished confirmation's `what` lacks one, so RESULTS.md "
            "and the result pages no longer print 'review.. Not priced.' for T-196 and "
            "T-223. None of the three papers prints an unfinished confirmation. Rendered "
            "at link revision 6051ebbe, once with this branch's result_status.py and once "
            "with the 6051ebbe copy loaded in its place: render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods leave the 50 "
            "files of the site tree byte-identical between the two. No PDF was printed; "
            "each prints from that HTML. Retain v0.1.7, v0.1.0 and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review", "paper:n11-threshold-bound-review"),
        paths=("packing/frontier/results.yaml",),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
        ),
        reason=(
            "For issue 678's registration (T-223 at n = 204 and 260) against main "
            "f8d54772: both reviews read results.yaml only through "
            "paper_figures.ladder_records, which selects the n11 ladder rungs LADDER_RUNGS "
            "names and holds them to LADDER_DIGEST; T-223 is an added entry outside that "
            "ladder, and no ladder row changes. Rendered at link revision f5349276, once "
            "from this branch's tree and once with main's copies of the three changed "
            "inputs (results.yaml, result-requests.yaml and source-coverage.yaml): "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods leave the 50 files of the site tree byte-identical "
            "between the trees. No PDF was printed; each prints from that HTML. Retain "
            "v0.1.7 and v0.1.0."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "For issue 678's registration (T-223 at n = 204 and 260) against main "
            "f8d54772: result requests, source coverage and results are citation targets "
            "whose existence the producer checks, not inlined text, and every cited path "
            "exists at both revisions; the #678 and #686 request changes, the "
            "couzo-issue678-2026-10-18 coverage source with its 83 beyond-horizon rows "
            "and the 60 rows it supersedes, and T-223 are not cited by the survey. "
            "Rendered at link revision f5349276, once from this branch's tree and once "
            "with main's copies of the three changed inputs (results.yaml, "
            "result-requests.yaml and source-coverage.yaml): render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods leave the 50 "
            "files of the site tree byte-identical between the trees. No PDF was printed; "
            "it prints from that HTML. Retain v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site v0.8.7 cut for the house best packing terminology (think-9v1i) "
            "regenerated the five claim documents, and each of the 22 changed lines differs "
            "from main 99cfcc8a only in its source-link revision, e6b9d98c to 9cd35d1e. "
            "The explainer links those documents rather than inlining them, so its HTML "
            "and Markdown are unchanged by them and it keeps v0.4.11. This is a "
            "source-reviewed disposition, as #695's was for v0.8.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/frontier/README.md",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Reviewed October 20, 2026 against main 99cfcc8a (think-9v1i): the frontier "
            "README's two house-rule passages now name the house best packing and link "
            "the synopsis's definition, and nothing else in it changes. Rendered with "
            "render_packing_methods at link revision 99cfcc8a, once from this branch's "
            "tree and once with main's copy of frontier/README.md: all 42 files it writes "
            "are byte-identical, and its PDF prints from that HTML and was not rebuilt. "
            "The survey keeps v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review", "paper:n11-threshold-bound-review"),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
        ),
        reason=(
            "For the evand lane of 20 October (T-221 at n = 308, T-222 at n = 154, both "
            "raised to V3/C3 and adopted as houses) against main d588ad98: both reviews "
            "read results.yaml only through paper_figures.ladder_records, which selects the "
            "n11 ladder rungs LADDER_RUNGS names and holds them to LADDER_DIGEST; T-221 and "
            "T-222 are added entries outside that ladder, and no ladder row changes. "
            "upper_bound_reports.py gains only two house readers, adopt_houses.py and "
            "upper_bound_houses.py only the 20 October pass's prose, credits and houses at "
            "154 and 308, and default_drawings.py loses only 308's settlement, none of "
            "which these producers call. Rendered at link revision 5ee03750, at the "
            "adoption's head febe2913, once from this branch's tree and once with main's "
            "copies of the eight changed inputs the three papers read (adopt_houses.py, "
            "default_drawings.py, upper_bound_houses.py, upper_bound_reports.py, "
            "results.yaml, result-requests.yaml, source-coverage.yaml and n-154.md): "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write 50 byte-identical files on both trees, and none "
            "of them names T-221, T-222, #689, #694 or either packet. No PDF was printed; "
            "each prints from that HTML. Retain v0.1.7 and v0.1.0."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/n-154.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "For the evand lane of 20 October (T-221 at n = 308, T-222 at n = 154, both "
            "raised to V3/C3 and adopted as houses) against main d588ad98: result requests, "
            "source coverage, the n = 154 case record and results are citation targets "
            "whose existence the producer checks, not inlined text, and every cited path "
            "exists at both revisions; the #689 and #694 requests, the coverage entries "
            "and T-221 and T-222 are not cited by the survey, and the adoption's rewrite of "
            "n-154.md enters none of its text. The two house readers upper_bound_reports.py "
            "gains, the 20 October pass's prose, credits and houses in adopt_houses.py and "
            "upper_bound_houses.py, and 308's settlement leaving default_drawings.py do not "
            "enter its output. Rendered at link revision 5ee03750, at the adoption's head "
            "febe2913, once from this branch's tree and once with main's copies of the "
            "eight changed inputs the three papers read (adopt_houses.py, "
            "default_drawings.py, upper_bound_houses.py, upper_bound_reports.py, "
            "results.yaml, result-requests.yaml, source-coverage.yaml and n-154.md): "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write 50 byte-identical files on both trees, and none "
            "of them names T-221, T-222, #689, #694 or either packet. No PDF was printed; "
            "it prints from that HTML. Retain v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review", "paper:n11-threshold-bound-review"),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
        ),
        reason=(
            "For PR687 (T-220 at n = 183) against main 012dcf9e: both reviews read "
            "results.yaml only through paper_figures.ladder_records, which selects the n11 "
            "ladder rungs LADDER_RUNGS names and holds them to LADDER_DIGEST; T-220 is an "
            "added n183 entry outside that ladder, and no ladder row changes. The house "
            "reader, writer and source changes are not called by these producers, and "
            "run_negative_controls.py changes only the snapshot cap and its comments. "
            "Rendered at link revision af1987e9, this branch after its merge of main "
            "012dcf9e (#692, site v0.8.3) and its edition cuts, once from this branch's "
            "tree and once with main's copies of the seven changed inputs (adopt_houses, "
            "run_negative_controls, upper_bound_houses and upper_bound_reports, "
            "results.yaml, result-requests.yaml and source-coverage.yaml): "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write 50 files, byte-identical between the trees. No "
            "PDF was printed; each prints from that HTML. Retain v0.1.7 and v0.1.0."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "For PR687 (T-220 at n = 183) against main 012dcf9e: result requests, source "
            "coverage and results are citation targets whose existence the producer "
            "checks, not inlined text, and every cited path exists at both revisions; the "
            "added #680 request, n183 coverage entry and T-220 entry are not cited by the "
            "survey. The house reader, writer and source changes do not enter its output, "
            "and run_negative_controls.py changes only the snapshot cap and its comments. "
            "Rendered at link revision af1987e9, this branch after its merge of main "
            "012dcf9e (#692, site v0.8.3) and its edition cuts, once from this branch's "
            "tree and once with main's copies of the seven changed inputs (adopt_houses, "
            "run_negative_controls, upper_bound_houses and upper_bound_reports, "
            "results.yaml, result-requests.yaml and source-coverage.yaml): "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write 50 files, byte-identical between the trees. No "
            "PDF was printed; each prints from that HTML. Retain v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("site",),
        paths=("packing/devtools/check_rational_witness_independent.py",),
        outputs=("atlas.html", "index.html", "results.html"),
        reason=(
            "Reviewed October 20, 2026 against main ded4727b (think-uomm): check_squares now "
            "takes each square's intervals on its own two edge normals once rather than once "
            "per pair, and builds the same eight exact Fraction gaps in the same order, so "
            "every pair gap and verdict it returns is unchanged. "
            "test_rational_witness_independent_contract holds it to the old pair_gap, kept "
            "verbatim, by Fraction equality on adversarial cases and retained views, and "
            "regularize_axis_components --verify-atlas passed with it, re-deriving the "
            "regularized index (which records the checker's verdict and pair count) and every "
            "retained view byte-identical. The checker is a candidate input only as a member "
            "of the site builders' import closure; no retained record changes, and the atlas, "
            "home and results pages draw those records. This is a measured disposition of the "
            "checker's outputs; no site rebuild byte comparison is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/check_rational_witness_independent.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Reviewed October 20, 2026 against main ded4727b (think-uomm): the independent "
            "checker computes each square's own-axis intervals once and returns the same "
            "exact gaps and verdicts, held to its old pair_gap verbatim by "
            "test_rational_witness_independent_contract and confirmed by a passing "
            "regularize_axis_components --verify-atlas, which requires the regularized index "
            "and views byte-identical. The checker is a candidate input only as a member of "
            "the paper builders' import closure; manuscripts, figures, scientific inputs, "
            "retained records and paper metadata are unchanged, and every paper keeps its "
            "edition. This is a measured disposition of the checker's outputs; no paper "
            "render or PDF redraw is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "PR #695's site v0.8.2 cut regenerated the five claim documents, and every "
            "changed line differs from main only in its source-link revision, a7fb8f2e to "
            "5998d0c3. The explainer links those documents rather than inlining them, so "
            "its HTML and Markdown are unchanged by them and it keeps v0.4.8. This is a "
            "source-reviewed disposition, as #514's was for v0.8.0."
        ),
    ),
    ReleaseNoPublicChange(
        components=("site",),
        paths=("packing/pyproject.toml",),
        outputs=("atlas.html", "index.html", "results.html"),
        reason=(
            "Reviewed October 20, 2026 against main b16ddeb0 (think-46yk): the only change "
            "is to [tool.pytest.ini_options], which loads the devtools.pytest_tmp test plugin "
            "and sets tmp_path_retention_policy and tmp_path_retention_count. Pytest reads "
            "them; the site build reads none of them, and no dependency, version or build "
            "setting changes, so no page's input changes. No site rebuild byte comparison "
            "is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/pyproject.toml",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Reviewed October 20, 2026 against main b16ddeb0 (think-46yk): the only change "
            "is to [tool.pytest.ini_options], which loads the devtools.pytest_tmp test plugin "
            "and sets tmp_path_retention_policy and tmp_path_retention_count. The paper "
            "builds read none of them, and no dependency, version or build setting changes; "
            "manuscripts, figures and paper metadata are unchanged and every paper keeps its "
            "edition. No paper render or PDF redraw is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site v0.8.5 cut for #680's News entry regenerated the five claim "
            "documents, and every changed line differs from main only in its source-link "
            "revision, 20d56718 to efd41b91. render_n11_lower_bounds_explainer, run once "
            "with main's five documents and once with this branch's, writes 54 files that "
            "are byte-identical. No PDF was printed; it prints from that HTML. The explainer "
            "keeps v0.4.10."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered at link revision d588ad98 (main, with #687), once with main's "
            "requests record and once with this branch's, the 42 files "
            "render_packing_methods writes are byte-identical. The PDF prints from that HTML. "
            "The record gains the final reply of 20 October 2026 on #680, which closes it, "
            "and the triage entry for #686 with 100 queued beyond-horizon results and one "
            "queued ask, which the survey does not read, so it keeps v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered at link revision 012dcf9e (main, with #692), once with main's "
            "requests record and once with this branch's, the 42 files "
            "render_packing_methods writes are byte-identical. The PDF prints from that HTML. "
            "The record gains the replies of 20 October 2026 to Evan Daniel on #659, #664, "
            "#669, #673 and #674, closes all but #664 and queues one ask there, which the "
            "survey does not read, so it keeps v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered at link revision 4b8aec9a (main, with #690), once with main's "
            "requests record and once with this branch's, the 42 files "
            "render_packing_methods writes are byte-identical. The PDF prints from that HTML. "
            "The record gains the reply records of 19 and 20 October 2026 on thirteen "
            "issues, closes #606 and #622 and queues two asks, which the survey does not "
            "read, so it keeps v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered at link revision a5acd570 (main, with #514 and #693), once with main's "
            "requests record and once with this branch's, the 42 files "
            "render_packing_methods writes are byte-identical. The PDF prints from that HTML. "
            "The record gains the #639 final reply and the #640 import reply of "
            "19 October 2026 and closes #639, which the survey does not read, so it "
            "keeps v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("site",),
        paths=(
            "packing/devtools/build_known_best_atlas.py",
            "packing/src/sqpack/witness.py",
        ),
        outputs=("atlas.html", "index.html", "results.html"),
        reason=(
            "Reviewed October 19, 2026 against main 14fd9e27 (think-ev4k): _margin_summary "
            "computes each square's axes and projections once and stops measuring a pair "
            "once its partial best gap exceeds the running minimum, and the atlas builder "
            "memoizes built cases and draws the composite test's poster from its own cases. "
            "An interleaved A/B rebuild of all 324 cases produced byte-identical witness and "
            "rendering text for 324 of 324, and build_known_best_atlas --check found every "
            "retained witness, margins included, byte-equal to the rebuild. The atlas, home "
            "and results pages draw those retained records, which do not change. This is a "
            "measured disposition of the records; no site rebuild byte comparison is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/build_known_best_atlas.py",
            "packing/src/sqpack/witness.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Reviewed October 19, 2026 against main 14fd9e27 (think-ev4k): the builder change "
            "only memoizes built cases and lets the composite test build its poster's own "
            "cases, and witness.py's margin summary returns the same values with less work "
            "(held to the exhaustive definition by test_margin_summary_matches_the_exhaustive_"
            "definition). The papers consume the retained atlas records it produces, and "
            "build_known_best_atlas --check found every retained witness and rendering "
            "byte-equal to the rebuild after the change; an interleaved A/B rebuild of all "
            "324 cases was byte-identical. Manuscripts, figures, scientific inputs and paper "
            "metadata are unchanged; every paper keeps its edition. This is a measured "
            "disposition of the records; no paper render or PDF redraw is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/n-146.md",
            "packing/frontier/n-236.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The evand lane of 19 October 2026 (#659, #664, #669, #673, #674) registers "
            "T-218 and T-219, raises T-197 to T-199 to V3/C3, adopts Evan Daniel's "
            "certificates as the houses at 155, 229, 236 and 271 with their house "
            "readers, drawings and case records, corrects the credit at 146 and 308, and "
            "maps the five requests; one unread review drawing leaves the worker "
            "snapshot (run_negative_controls). Rendered at link revision 028bc72e (main, "
            "site v0.7.35), once from main's tree and from this branch's at ecb4b31d, "
            "after its merge of main and the explainer's v0.4.9 cut, again at 4610c915, "
            "after the records-tier fixes, and at a8222aad, after the CI follow-ups and "
            "its merge of main b16ddeb0 (#691), render_packing_methods, "
            "render_n11_optimality_review and render_n11_threshold_bound_review write 50 "
            "files, byte-identical between the trees. Rendered again at link revision "
            "4b8aec9a, once from main's tree there (site v0.8.1, after #514, #693, #688 "
            "and #690) and once from this branch's at 2e480fa4, after its merges of main "
            "476049de and 4b8aec9a and the landed stamp, the same three write 50 files, "
            "byte-identical between the trees. No PDF was printed; each prints from that "
            "HTML. The three papers keep v0.1.7, v0.1.0 and v0.2.3; the explainer, whose "
            "register count moves to 219, takes v0.4.9."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/run_negative_controls.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "Reviewed October 19, 2026 against main 926cd764 for the #446 landing of "
            "T-205, T-206 and T-207: results.yaml changes only those three n68, n84 and "
            "n85 lower-bound entries and last_reviewed. The explainer reads the register "
            "for its count of 217 results and of apparently or confirmed novel ones, "
            "both unchanged since the three stay previously-published. The composite "
            "figure record and bound citations change only the n68, n84 and n85 lower "
            "displays and citations; Figure 2's totals and the n11 citation the paper "
            "reads are unchanged. The site v0.8.1 cut regenerated the five claim and "
            "card documents, which change only their source-link commit and are linked "
            "from the paper, not inlined. run_negative_controls.py changes only the "
            "snapshot cap and its comment and is not a paper producer. Its Markdown "
            "rendered at the base record tree and at the candidate head is identical, "
            "and its HTML differs at most in where the browser math preparation "
            "serializes one empty style attribute; the PDF prints that HTML. Retain "
            "v0.4.8; no PDF redraw or byte identity of the PDF is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review",),
        paths=(
            "packing/devtools/run_negative_controls.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
        ),
        reason=(
            "Reviewed October 19, 2026 against main 926cd764 for the #446 landing of "
            "T-205, T-206 and T-207: the changed results are the n68, n84 and n85 lower "
            "bounds, outside the n11 ladder rows this paper consumes, and "
            "run_negative_controls.py changes only the snapshot cap and its comment. Its "
            "HTML and Markdown rendered at the base record tree and at the candidate "
            "head with the same source-link revision are byte-identical. Retain v0.1.7; "
            "no PDF redraw is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-threshold-bound-review",),
        paths=(
            "packing/devtools/run_negative_controls.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
        ),
        reason=(
            "Reviewed October 19, 2026 against main 926cd764 for the #446 landing of "
            "T-205, T-206 and T-207: the changed results are the n68, n84 and n85 lower "
            "bounds, outside the n11 ladder rows, T-060 included, that this paper "
            "consumes, and run_negative_controls.py changes only the snapshot cap and "
            "its comment. Its HTML and Markdown rendered at the base record tree and at "
            "the candidate head with the same source-link revision are byte-identical. "
            "Retain v0.1.0; no PDF redraw is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/run_negative_controls.py",
            "packing/frontier/n-084.md",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Reviewed October 19, 2026 against main 926cd764 for the #446 landing of "
            "T-205, T-206 and T-207: the #446 request entry, the n84 case record and the "
            "three register entries are citation targets whose existence the producer "
            "checks, not inlined text, and every cited path exists at both revisions; "
            "run_negative_controls.py changes only the snapshot cap and its comment. Its "
            "HTML and Markdown rendered at the base record tree and at the candidate "
            "head with the same source-link revision are byte-identical. Retain v0.2.3; "
            "no PDF redraw is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "PR #514's site v0.8.0 cut regenerated the five claim documents, and every "
            "changed line differs from main only in its source-link revision, e00bfbe5 to "
            "98845675. The explainer links those documents rather than inlining them, so "
            "its HTML and Markdown are unchanged by them and it keeps v0.4.8. This is a "
            "source-reviewed disposition, as #645's was for v0.7.33."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Issue #538's request record gains its 19 October follow-up reply. Rendered "
            "at 6c8e4fc0 with and without that reply: all 42 files the survey's renderer "
            "writes are byte-identical, since the survey only links the request record, "
            "and its PDF prints from that HTML, so it keeps v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/overview_sections.py",
            "packing/devtools/register_evand_arrangements.py",
            "packing/devtools/register_gupta_reports.py",
            "packing/devtools/register_refinement_reports.py",
            "packing/devtools/register_ryxu_reports.py",
            "packing/devtools/render_overview.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The results page's overview and its Added filter (#514) change only the "
            "results page, the results table's rows and bar, the results page's byte "
            "ceiling's reason, each register entry's new `landed` day, and the register "
            "entries the import generators draft, which now write `landed`. Rendered at "
            "6ff2017d, after the merge of main 14fd9e27, once from this branch's tree and "
            "once with main's copies of its changed files: all 68 files the four papers' "
            "renderers write are byte-identical, the explainer's HTML included (the order "
            "of its empty style attribute on a math span can vary between two renders of "
            "the same code). Each PDF prints from that HTML, so every paper keeps its "
            "edition: v0.4.8, v0.1.7, v0.1.0 and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "PR #646's site v0.7.35 cut regenerated the five claim documents, and every "
            "changed line differs from main only in its source-link revision, 44cb20e9 to "
            "e00bfbe5. The explainer links those documents rather than inlining them, so "
            "its HTML and Markdown are unchanged by them and it keeps v0.4.8. This is a "
            "source-reviewed disposition, as #645's was for v0.7.33."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Issue #538's request record marks its trajectory-timing ask done by #685 and "
            "moves the unattributed Animate play message onto think-8vsk. Rendered at "
            "cc058a45 with and without that change: all 42 files the survey's renderer "
            "writes are byte-identical, and its PDF prints from that HTML, so it keeps "
            "v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/overview/rating-tooltips.js",
            "packing/devtools/render_changelog.py",
            "packing/devtools/render_overview.py",
            "packing/devtools/templates/site-nav.css",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "The News chooser correction reads News significance meanings from the "
            "label rubric in result-import.md, declared as a site input in "
            "render_overview, uses them in News cards and controls, and extends "
            "tooltip enhancement to News score buttons, whose press dismisses the "
            "tooltip, while retaining existing badge interactions. Compact in-place "
            "choices gain per-button borders and a visible focus outline. The four "
            "papers contain neither News controls nor compact in-place choosers; "
            "their existing navigation links and rating badges retain their behavior. "
            "Source review finds no manuscript, figure, credit, content date or "
            "print-style change in these paper exports. This is not a rendered "
            "byte-equality claim; the site alone takes a patch edition."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "Site v0.7.34 (#658) regenerates the five claim documents, and their only "
            "change is the source-link revision, d24b3bf9 to the cut's commit. The "
            "explainer links them by URL on main (repo_url for T025_CLAIM, T026_CLAIM, "
            "the proof card and claim_path) and never reads their text; its "
            "edition_file helper is defined but unused. Manuscript, scientific inputs, "
            "figures and paper metadata are unchanged, so the explainer keeps v0.4.8. "
            "This is a source-reviewed disposition; no render, PDF or byte identity is "
            "claimed for these paths."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/select_houses.py",
            "packing/frontier/n-088.md",
            "packing/frontier/n-102.md",
            "packing/frontier/n-123.md",
            "packing/frontier/n-126.md",
            "packing/frontier/n-175.md",
            "packing/frontier/n-199.md",
            "packing/frontier/n-267.md",
            "packing/frontier/n-295.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The records lane of 16 October 2026 for #639 and #640 (#658) maps the s(19) "
            "review onto T-194 (C1) and raises T-193 to V3/C3 in results.yaml, with the "
            "#639 and #640 request entries and their review fixes (A6 to A9). Under the "
            "house rule (#660) select_houses reads T-193's exact sides (evand_exact_side, "
            "in ALGEBRAIC_READERS) and stages its sixteen counts under think-ot5c, twelve "
            "of them re-pointed from T-174, so T-174's register text, its coverage source "
            "and the #574 request count 41 houses, not 53; adopt_houses names a "
            "re-staged house in the held sentence and a smaller staged one in its "
            "section, and its refresh rewrites those sixteen case records; its plan refuses "
            "T-193 at the nine counts where RE-1 owes its regularization a correction "
            "(CORRECTIONS_OWED), and a held sentence names what a re-staged house is "
            "(review B of #658). Re-taken on 19 October 2026 after the branch merged main "
            "with #665, #685 and #645: rendered at link revision 9fb8e147 (main, site "
            "v0.7.33), once from main's tree and once from this branch's at c9745477 after "
            "its merge of it, render_packing_methods, render_n11_optimality_review and "
            "render_n11_threshold_bound_review write 50 files, byte-identical between the "
            "two trees. The explainer prepares its math with a pinned Chromium this host "
            "lacks, so it is source-reviewed only: it reads results.yaml only to count "
            "the register's entries and its apparently new ones, 217 and 32 on both "
            "trees, and never calls select_houses or adopt_houses. No PDF was printed. "
            "All four papers keep v0.4.8, v0.1.7, v0.1.0 and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=("packing/src/sqpack/cli/validate.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "Reviewed October 19, 2026 against main f3d5da7b: the explainer's "
            "RENDER_INPUTS includes the entire sqpack tree, but its HTML, Markdown "
            "and PDF producer import closure excludes the validation CLI. This "
            "file changes only _site_layout_tests to disable pytest capture and "
            "enable existing Playwright wire/API logging for serial forwarders, "
            "and lets _run report a bounded tail of that command's output. "
            "Paper producers neither call that runner nor consume its logs. "
            "Manuscripts, scientific inputs, figures, paper metadata and the "
            "pre-cut publication link revision are unchanged; the five claim/card "
            "documents remain current. The article's last change remains October "
            "13, 2026, matching EXPLAINER_REVISED. Retain explainer v0.4.8 and the "
            "prepared site v0.7.32. This is a source-reviewed disposition, with "
            "no paper render, PDF redraw or output-byte comparison claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/probes/measure_atlas_views/layout.js",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "For the Atlas CSS repair against landed main f3d5da7b, review of all "
            "four HTML, Markdown and PDF producers finds no consumed content change. "
            "Their shells use KPress, paper-type, site-nav and paper-publication "
            "styles plus their own paper styles; none includes site.css or its "
            "site-atlas-grid rule. The layout probe is read by measure_atlas_views "
            "and browser tests, not by those producers; its broad probe declaration "
            "is a conservative candidate for the explainer and methods survey. "
            "The paused animation clock belongs only to the browser test. The five "
            "claim documents change only source-link revisions for site v0.7.32 "
            "and remain linked rather than inlined into papers; the README changes "
            "only its site edition sentence. Manuscripts, scientific inputs, "
            "figures and paper metadata are unchanged. Retain explainer v0.4.8 and "
            "methods survey v0.2.3. The optimality and threshold reviews have no "
            "changed candidate inputs and retain v0.1.7 and v0.1.0. This is a source-reviewed "
            "disposition; no paper render, PDF redraw or artifact byte identity "
            "is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/git_storage.py",
            "packing/devtools/upper_bound_houses.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "PR406 (review H1) moves stored_size, OR-18's size of a blob as Git stores "
            "it, from upper_bound_houses into the new devtools.git_storage, so that the "
            "added-blob guard shares it without importing the house tooling. The "
            "function body is unchanged and upper_bound_houses imports it under the same "
            "name; the module's other change is its docstring. Re-measured on main "
            "e929137a8 with this branch merged: six modules in each paper's producer "
            "import closure, the explainer's and the survey's PDF producer included, "
            "import upper_bound_houses: adopt_houses, build_known_best_atlas, "
            "check_results, check_source_coverage, register_regularized_bounds and "
            "run_negative_controls (review J1). Every one of them leaves stored_size, "
            "staged_sizes and print_sizes uncalled; only the module's own sizes command "
            "runs them, and the rest of git_storage serves only the added-blob guard, "
            "which no paper producer imports. Manuscripts, scientific inputs, figures and "
            "paper metadata are unchanged, so the explainer keeps v0.4.19, the "
            "optimality review v0.1.10, the threshold review v0.1.3 and the methods survey "
            "v0.2.6. Source-reviewed; no render or byte identity is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=("packing/src/sqpack/cli/validate.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "PR406 adds the Git-storage guard to the validation CLI push schedule "
            "and its status banner. The explainer declares the whole sqpack package, "
            "but the import closure of its fourteen Python producers, measured with "
            "pages_scope.import_closure on main e929137a8 with this branch merged, is "
            "145 files and holds no sqpack.cli module. The manuscript, certificate "
            "inputs, figures, rendering helpers and paper release metadata are "
            "unchanged against that main, so the paper retains v0.4.19. This is a "
            "source-based producer review; no paper export was rebuilt or compared for "
            "byte identity. The changed development.md is published as "
            "development.html, which since #729 deploys from main with no site "
            "edition, so this record names only the paper."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/check_case_prose.py",
            "packing/devtools/check_rung_figures.py",
            "packing/devtools/check_standing.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/regularize_axis_components.py",
            "packing/devtools/result_overview.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/frontier/results.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "For PR665 against landed main e0319ffd, a source-based review of the HTML, "
            "Markdown and PDF producers finds the consumed values unchanged: 217 "
            "registered results, 32 novel results, the n11 verified-lower citation, and "
            "Figure 2 caption totals 81 recent lower bounds and zero first proved here. "
            "Its n11 manuscripts, certificates, verifier text, figures and paper metadata "
            "are unchanged. Changed claim documents carry only refreshed source-link "
            "revisions and are linked rather than inlined. Changed house-selection, "
            "regularization, result-page and control tools are outside the paper output "
            "paths; the CLI validation change selects checks. The site patch owns the "
            "adopted houses. Retain v0.4.8; no render, PDF redraw or artifact byte "
            "identity is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review",),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/check_case_prose.py",
            "packing/devtools/check_rung_figures.py",
            "packing/devtools/check_standing.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/regularize_axis_components.py",
            "packing/devtools/result_overview.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
        ),
        reason=(
            "For PR665 against landed main e0319ffd, source review of the HTML, Markdown "
            "and PDF producers finds the complete consumed n11 ladder rows T010, T018, "
            "T025, T026, T033, T037, T060 and T061 unchanged. Changed result claims are "
            "T169, T170, T171 and T174, outside that ladder. Its manuscript, retained "
            "proof and figure inputs, renderers and own publication metadata are "
            "unchanged. The house-selection, regularization, result-page and control "
            "changes are not called by this paper producer. Retain v0.1.7; this is a "
            "source-based review, with no proof rerun, PDF redraw or artifact "
            "byte-identity claim."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-threshold-bound-review",),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/check_case_prose.py",
            "packing/devtools/check_rung_figures.py",
            "packing/devtools/check_standing.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/regularize_axis_components.py",
            "packing/devtools/result_overview.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
        ),
        reason=(
            "For PR665 against landed main e0319ffd, source review of the HTML, Markdown "
            "and PDF producers finds the consumed n11 ladder, including the T060 claim "
            "used for its gap caption, unchanged. The T169, T170, T171 and T174 claim "
            "edits are outside those consumed rows. Its manuscript, certificates, "
            "retained figure inputs, renderer and own publication metadata are unchanged. "
            "Changed house-selection, regularization, result-page and control tools are "
            "not called by this producer. Retain v0.1.0; no proof rerun, PDF redraw or "
            "artifact byte identity is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/check_case_prose.py",
            "packing/devtools/check_rung_figures.py",
            "packing/devtools/check_standing.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/regularize_axis_components.py",
            "packing/devtools/result_overview.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/frontier/n-029.md",
            "packing/frontier/n-070.md",
            "packing/frontier/n-084.md",
            "packing/frontier/n-086.md",
            "packing/frontier/n-102.md",
            "packing/frontier/n-103.md",
            "packing/frontier/n-105.md",
            "packing/frontier/n-108.md",
            "packing/frontier/n-123.md",
            "packing/frontier/n-126.md",
            "packing/frontier/n-127.md",
            "packing/frontier/n-129.md",
            "packing/frontier/n-130.md",
            "packing/frontier/n-131.md",
            "packing/frontier/n-146.md",
            "packing/frontier/n-153.md",
            "packing/frontier/n-154.md",
            "packing/frontier/n-175.md",
            "packing/frontier/n-179.md",
            "packing/frontier/n-180.md",
            "packing/frontier/n-207.md",
            "packing/frontier/n-208.md",
            "packing/frontier/n-209.md",
            "packing/frontier/n-236.md",
            "packing/frontier/n-237.md",
            "packing/frontier/n-238.md",
            "packing/frontier/n-239.md",
            "packing/frontier/n-261.md",
            "packing/frontier/n-267.md",
            "packing/frontier/n-295.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "For PR665 against landed main e0319ffd, source review of the HTML, Markdown "
            "and PDF producers finds every declared historical figure input unchanged, "
            "including the n29 and n51 SVGs, Casson n106 source and retained SQUISH n108 "
            "facts. Changed case records, result requests, source coverage and results "
            "are citation targets whose existence the producer checks; their bodies are "
            "not inlined. All cited paths remain present at both revisions. The C1 "
            "margin wording changes current openings at 15 additional citation targets, "
            "including n29, with every other byte and all metadata retained. The "
            "manuscript, renderer and own publication metadata are unchanged. "
            "House-selection, regularization, result-page and control changes do not "
            "enter its output. Retain v0.2.3; no search, PDF redraw or artifact byte "
            "identity is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "For PR407 against main 6833d05aa, the five generated claim documents "
            "differ only in GitHub source-link revisions, from a450742e to c0fc4f9d, "
            "the clean integration checkpoint before the site cut. Their claims, "
            "proofs, embedded certificates and verifier text are unchanged. The "
            "explainer checks these documents' presence and links to them; it does "
            "not inline their bodies. Its manuscript, certificate inputs, figures, "
            "renderer and own release metadata are unchanged, so it retains v0.4.8. "
            "This is a source-based review of the HTML, Markdown and PDF producers; "
            "no PDF redraw, proof rerun or artifact byte identity is claimed. Site "
            "v0.7.30 owns the published development-guide correction."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review",),
        paths=(
            "packing/devtools/acquire_source.py",
            "packing/devtools/apply_closed_form.py",
            "packing/devtools/render_n11_lower_bounds_explainer_pdf.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/verifier_registry.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
        ),
        reason=(
            "For PR 671, rendered HTML and Markdown against reviewed PR 679 candidate "
            "e22a9f9f4 and the current integration tree, using source-link revision "
            "e22a9f9f4 in both. Both outputs are byte-identical. The n11 optimality "
            "review retains its article, selected facts and figures, so its edition "
            "remains v0.1.7. The fine-net records, monotone case planning, safe packet "
            "publication and explainer pagination guard do not change these outputs."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-threshold-bound-review",),
        paths=(
            "packing/devtools/acquire_source.py",
            "packing/devtools/apply_closed_form.py",
            "packing/devtools/render_n11_lower_bounds_explainer_pdf.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/verifier_registry.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
        ),
        reason=(
            "For PR 671, rendered HTML and Markdown against reviewed PR 679 candidate "
            "e22a9f9f4 and the current integration tree, using source-link revision "
            "e22a9f9f4 in both. Both outputs are byte-identical. The n11 threshold review "
            "retains its article, selected facts and figures, so its edition remains "
            "v0.1.0. The fine-net records, monotone case planning, safe packet "
            "publication and explainer pagination guard do not change these outputs."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/acquire_source.py",
            "packing/devtools/apply_closed_form.py",
            "packing/devtools/render_n11_lower_bounds_explainer_pdf.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/verifier_registry.py",
            "packing/frontier/n-108.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "For PR 671, rendered HTML and Markdown against reviewed PR 679 candidate "
            "e22a9f9f4 and the current integration tree, using source-link revision "
            "e22a9f9f4 in both. Both outputs are byte-identical. The square-packing "
            "methods survey retains its article, selected facts and figures, so its "
            "edition remains v0.2.3. The fine-net records, monotone case planning, safe "
            "packet publication and explainer pagination guard do not change these "
            "outputs."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "Reviewed against main d167d4b86 for PR #679 A1: the validate.py delta "
            "only extends _rust_exact_geometry's Cargo feature-selection checks. It "
            "changes no paper renderer, input, proof, figure, substitution or citation. "
            "The paper's declared import closure conservatively includes this command "
            "module, but rendering the paper never runs that validation step. This is "
            "a source-path review, not an HTML/PDF byte comparison. The five generated "
            "claim documents only refresh their source links to PUBLICATION_REVISION; "
            "their claims, proofs, certificate bytes and verifier text are unchanged. "
            "The explainer keeps v0.4.7. Site v0.7.28 owns the published development-guide and "
            "synopsis changes."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/overview_sections.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Reviewed against PR #661 a87de0cf7: the only semantic change in this module "
            "adds the JoostdeWinter/square-packing entry to OTHER_PROJECTS. Its consumers "
            "are the site's project cards, filter choices and result-row project "
            "attribution, and intake discovery. None of the four paper renderers or "
            "their shared paper-front, navigation and colophon paths consumes these "
            "values; all other module definitions are unchanged. This addition changes "
            "no paper source, figure, fact substitution or citation link. This is a "
            "source-path review, not an HTML/PDF byte comparison: the four paper editions "
            "stay unchanged, and site v0.7.27 owns the card."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/frontier/results.yaml",
            "packing/campaign/result-requests.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Reviewed these exact shared inputs against PR #661 a87de0cf7: all 195 "
            "existing result objects, the n11 ladder entries and the novel-result count "
            "are unchanged; four reported entries add only counts 155, 227, 229 and 260. "
            "The explainer's live register total moves from 195 to 199, site data rather "
            "than a revision of its mathematics, as in the preceding release decision. "
            "The other n11 reviews use the unchanged ladder, and the methods manuscript "
            "only links these YAML records, with no data fact substitutions. All five "
            "freshly generated claim/card documents equal the parent and worktree "
            "bytes. No case upper lane, house, paper template or figure input changes. "
            "This is a source-scope review, not an HTML/PDF byte comparison; the paper "
            "editions stay unchanged."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=("packing/src/sqpack/cli/validate.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Reviewed the explainer's RENDER_INPUTS, which broadly includes the sqpack "
            "tree: this file's only change selects the validation step's release-impact "
            "baseline. The paper renderers do not call _synopsis; its caller is the "
            "validation step registry. No theorem, geometry, paper content or source-link "
            "revision changes, and the five generated claim documents remain byte-identical "
            "to the PR #661 parent. This is a source-path review, not an HTML/PDF byte "
            "comparison."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Reviewed render_packing_methods: render_all_facts returns no substitutions, "
            "and these request/source records are citation inputs without rendered "
            "content. The 18 October change adds queued issue claims and reads, records "
            "the already posted 432 reply and corrects the 446 transcription; none enters "
            "the manuscript. PR 667's paired 42-file comparison established the same "
            "boundary. The current review preserves the survey's v0.2.2 edition."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.26 for the adoption of T-195 at 29 regenerated the five "
            "claim documents at PUBLICATION_REVISION 337b84df, a commit of this branch "
            "kept reachable from main by the merge commit the PR merges with; with that "
            "revision read back as main's 83b4720e, each is byte-identical to main's, so "
            "the 32 repository links it pins are the only change, and no claim, "
            "certificate or command moves. A link revision follows the site's edition and "
            "is not a revision of the explainer, so it keeps v0.4.7. Source-compared; no "
            "render of the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.25 for the house rule (PR 660, think-sa5r) regenerated the "
            "five claim documents at PUBLICATION_REVISION 83b4720e, this branch's merge of "
            "main 6a3a7d8f, kept reachable from main by the merge commit the PR merges "
            "with. With that revision read back as v0.7.24's d421bac7, each is "
            "byte-identical to main's 6a3a7d8f, and between the two revisions those case "
            "directories change only in the five documents themselves, so the 32 "
            "repository links they pin are the only change, and no claim, certificate or "
            "command moves. A link revision follows the site's edition and is not a "
            "revision of the explainer, so it keeps v0.4.7. Source-compared; no render of "
            "the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.24, which pairs README's edition sentence with the atlas "
            "posters' v0.6.2 (PR 663, think-nv87), regenerated the five claim documents at "
            "PUBLICATION_REVISION d421bac7, kept reachable from main by the merge commit the "
            "PR merges with. With that revision read back as v0.7.23's 18ed93f5, each is "
            "byte-identical to main's c593e2bf, and between the two revisions those case "
            "directories change only in the five documents themselves, so the 32 "
            "repository links they pin are the only change, and no claim, certificate or "
            "command moves. A link revision follows the site's edition and is not a "
            "revision of the explainer, so it keeps v0.4.7. Source-compared; no render of "
            "the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.23 for the 16 October records and their regularization "
            "regenerated the five claim documents at PUBLICATION_REVISION 18ed93f5, this "
            "branch's re-pin after merging #656, kept reachable from main by the merge "
            "commit the PR merges with; with that revision read back as #654's 7d47bd4e, "
            "each is byte-identical to #656's, so the 32 repository links it pins are the "
            "only change, and no claim, certificate or command moves. A link revision "
            "follows the site's edition and is not a revision of the explainer, so it "
            "keeps v0.4.7. Source-compared; no render of the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/regularize_axis_components.py",
            "packing/devtools/regularize_evand.py",
            "packing/src/sqpack/cli/validate.py",
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/n-129.md",
            "packing/frontier/n-146.md",
            "packing/frontier/n-154.md",
            "packing/frontier/n-175.md",
            "packing/frontier/n-237.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "The records lane of 16 October 2026 (think-z7wn) raises T-185 to T-190 to V3/C3, "
            "moves fifteen houses to T-186, T-187, T-188 and T-190 with their case records, "
            "coverage overrides and adoption code, and regularizes six of the re-housed "
            "counts. Rendered at one link revision (e2e018f3), once from the base branch's "
            "tree (the regularization stack's top at 7e44e4bd) and once from this branch's, "
            "render_packing_methods, render_n11_optimality_review and "
            "render_n11_threshold_bound_review write 50 files, byte-identical between the two "
            "trees. The explainer's render needs a browser this host lacks, so it is "
            "source-reviewed only. No PDF was printed. The selection think-r3cl owed then "
            "drew grid-slack's views at 232, 264, 271 and 302 and settled 237, 303 and 304 "
            "in default_drawings, which changes only results.yaml's regularized_drawings "
            "items and those case records' regularization notes; rendered at link revision "
            "e2e018f3 from this branch at 796a1d03, the survey's and both reviews' 42 files "
            "each are byte-identical to main e2e018f3's. The owner's review then admitted "
            "Evan Daniel's view at 211, the layer's first review record "
            "(regularized/reviews.yaml), which regularize_evand and "
            "regularize_axis_components read and the papers do not; it changes only that "
            "count's regularized_drawings item and case note, and rendered at link "
            "revision e2e018f3 with it, the survey's and both reviews' 42 files each are "
            "byte-identical to main e2e018f3's. Merged over #656 with main, which holds "
            "#644, #653 and #654, this layer cuts its own site patch; rendered at link "
            "revision e2e018f3 from the merge, the survey's and both reviews' 42 files each "
            "are byte-identical to main e2e018f3's. All four papers keep v0.4.7, v0.1.7, "
            "v0.1.0 and v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.22 for the think-3zi3 regularization regenerated the five "
            "claim documents at PUBLICATION_REVISION 7d47bd4e, this branch's re-pin after "
            "merging #653's head 98f6626f, kept reachable from main by the merge commit "
            "the PR merges with; with that revision read back as #653's 3971c17b, each is "
            "byte-identical to #653's, so the 32 repository links it pins are the only "
            "change, and no claim, certificate or command moves. A link revision follows "
            "the site's edition and is not a revision of the explainer, so it keeps "
            "v0.4.7. Source-compared; no render of the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/default_drawings.py", "packing/frontier/results.yaml"),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Over #653's head 98f6626f, the think-3zi3 regularization takes 175, 232 and "
            "264 off PENDING_ALLOWED in default_drawings, which leaves it empty, and "
            "changes results.yaml only in its regularized_drawings items at those three "
            "counts. The papers read results.yaml's results, never regularized_drawings, "
            "and reach default_drawings only through shared import discovery, reading "
            "neither constant. Rendered at link revision e2e018f3 from this branch at "
            "7d47bd4e, the survey's and both reviews' 42 files each are byte-identical to "
            "the renders from main e2e018f3's tree; the explainer, whose render needs a "
            "browser this host lacks, is source-reviewed only, and no PDF was printed. "
            "All four papers keep their versions."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
            "site",
        ),
        paths=(
            "packing/atlas/known-best/default-drawings.json",
            "packing/devtools/default_drawings.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
            "atlas.html",
            "index.html",
            "results.html",
        ),
        reason=(
            "The think-0ut1 run of 16 October 2026 admits no view: it rewrites ten "
            "decided-no-better SETTLED entries (their runs, outcomes and evidence, no owed "
            "work left), so default-drawings.json changes only those counts' `states` rows "
            "(`decisions` and `why`); its `entries` are byte-identical to the base's. The "
            "site reads the record only through `regularized_defaults`, `credit_line` and "
            "`held_reasons`, which read `entries` and the index, never `states`, SETTLED or "
            "PENDING_ALLOWED, and no case record, view or index entry changes. The papers "
            "reach default_drawings only through shared import discovery and read neither "
            "constant. Review G2 of #644 then added default_drawings.orphaned_copies, "
            "which fails the state gate on a settled-runs copy no settlement names, and "
            "deleted the five such copies; the site and the papers read neither. Source "
            "review, no render; the site keeps v0.7.22 and the papers v0.4.7, v0.1.7, "
            "v0.1.0 and v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
        ),
        paths=("packing/devtools/regularize_select.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
        ),
        reason=(
            "The think-3zi3 run's fix changes only how regularize_select orders a driver "
            "count with no view among its candidates. The three papers reach the module "
            "only through shared import discovery and never run the selection, so their "
            "manuscripts, figures, credits and print rules are unchanged by source review. "
            "No render was taken, and they keep v0.4.7, v0.1.7 and v0.1.0."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/devtools/regularize_select.py",
            "packing/frontier/n-175.md",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The regularization run of 16 October 2026 on the three counts #598 re-housed "
            "(think-3zi3) changes n = 175's case record only in its generated "
            "regularization note, which the survey cites by link only, and fixes how the "
            "selection orders a driver count with no view, which the survey reaches only "
            "through shared import discovery and never runs. Rendered from main at "
            "e2e018f32 and from this branch at that one link revision, the survey's HTML "
            "and Markdown are byte-identical, as are the other 40 files the renderer "
            "writes. No PDF was printed (no pinned Chromium on this host), and the survey "
            "keeps v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.21 for the think-kpm3 regularization regenerated the five "
            "claim documents at PUBLICATION_REVISION 3971c17b, this branch's re-pin after "
            "merging main b35a6289, kept reachable from main by the merge commit the PR "
            "merges with; with that revision read back as main's 94dc2b59, each is "
            "byte-identical to main's, so the 32 repository links it pins are the only "
            "change, and no claim, certificate or command moves. A link revision follows "
            "the site's edition and is not a revision of the explainer, so it keeps "
            "v0.4.7. Source-compared; no render of the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/default_drawings.py", "packing/frontier/results.yaml"),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Over main b35a6289, which holds #644, the think-kpm3 regularization adds "
            "SETTLED's 304 and takes eight counts off PENDING_ALLOWED in default_drawings, "
            "and changes results.yaml only in its regularized_drawings items at the seven "
            "counts it draws. The papers read results.yaml's results, never "
            "regularized_drawings, and reach default_drawings only through shared import "
            "discovery, reading neither constant. Rendered at link revision e2e018f3 from "
            "this branch at 3971c17b, the survey's and both reviews' 42 files each are "
            "byte-identical to the renders from main e2e018f3's tree; the explainer, whose "
            "render needs a browser this host lacks, is source-reviewed only, and no PDF "
            "was printed. All four papers keep their versions."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/frontier/n-153.md",
            "packing/frontier/n-154.md",
            "packing/frontier/n-207.md",
            "packing/frontier/n-237.md",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The regularization run of 16 October 2026 on the eight counts #614 re-housed "
            "(think-kpm3) changes these case records only in their generated "
            "regularization note, which the survey does not quote: it cites them by link, "
            "as its results table's count links. Rendered from main at e2e018f32 and from "
            "this branch at that one link revision, the survey's HTML and Markdown are "
            "byte-identical, as are the other 40 files the renderer writes. No PDF was "
            "printed (no pinned Chromium on this host), and the survey keeps v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/regularized_drawings.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "#653's review A1 changes only which of this project's modifications a "
            "regularization note names: the same-side re-solve is credited where the run's "
            "output is the re-solve's, so the notes at 241 and 302, which no paper links, "
            "and results.yaml's regularized_drawings item at 302 now say unmodified. The "
            "papers read results.yaml's results, never regularized_drawings, and reach the "
            "module only through shared import discovery. Rendered from this branch's tree "
            "at 0082533ee, at the link revision e2e018f3, the survey's and both "
            "reviews' HTML and Markdown and the other 40 files each render writes are "
            "byte-identical to the renders from main e2e018f3's tree taken for #644 and "
            "for the survey's record above (42 of 42 files each); the explainer, whose "
            "render needs a browser this host lacks, is source-reviewed only, and no PDF "
            "was printed. All four papers keep their versions."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.20 for the think-la7h regularization regenerated the five "
            "claim documents at PUBLICATION_REVISION 94dc2b59, this branch's re-pin after "
            "merging main 80b116ed, kept reachable from main by the merge commit the PR "
            "merges with; with that revision read back as main's 3d4ada4c, each is "
            "byte-identical to main's, so the 32 repository links it pins are the only "
            "change, and no claim, certificate or command moves. A link revision follows "
            "the site's edition and is not a revision of the explainer, so it keeps "
            "v0.4.7. Source-compared; no render of the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.19 for T-184 and T-191 at V3/C1 regenerated the five claim "
            "documents at PUBLICATION_REVISION 3d4ada4c, this branch's re-pin after "
            "merging #652, kept reachable from main by the merge commit the PR merges "
            "with; with that revision read back as #652's 1cc0dbbe, each is "
            "byte-identical to #652's, so the 32 repository links it pins are the only "
            "change, and no claim, certificate or command moves. A link revision follows "
            "the site's edition and is not a revision of the explainer, so it keeps "
            "v0.4.7. Source-compared; no render of the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.18 for the October 16 review of s(76) = 9 and s(95) = 10 "
            "regenerated the five claim documents at PUBLICATION_REVISION 1cc0dbbe, the "
            "merge of main into this branch, kept reachable from main by the merge commit "
            "the PR merges with; with that revision read back as main's 815f3c67, each is "
            "byte-identical to main's, so the 32 repository links it pins are the only "
            "change, and no claim, certificate or command moves. A link revision follows "
            "the site's edition and is not a revision of the explainer, so it keeps "
            "v0.4.7. Source-compared; no render of the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.17 for the October 16 review of T-185 to T-190 regenerated "
            "the five claim documents at PUBLICATION_REVISION 815f3c67, the merge of main "
            "into this branch, kept reachable from main by the merge commit the PR merges "
            "with; with that revision read back as main's 1efce164, each is "
            "byte-identical to main's, so the 32 repository links it pins are the only "
            "change, and no claim, certificate or command moves. A link revision follows "
            "the site's edition and is not a revision of the explainer, so it keeps "
            "v0.4.7. Source-compared; no render of the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.16 for the October 16 review of the s(19) Lean proof "
            "regenerated the five claim documents at PUBLICATION_REVISION 1efce164, the "
            "merge of main into this branch, kept reachable from main by the merge commit "
            "the PR merges with; with that revision read back as main's 46ae34f9, each is "
            "byte-identical to main's, so the 32 repository links it pins are the only "
            "change, and no claim, certificate or command moves. A link revision follows "
            "the site's edition and is not a revision of the explainer, so it keeps "
            "v0.4.7. Source-compared; no render of the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=("site",),
        paths=("packing/src/sqpack/release.py",),
        outputs=("index.html", "about.html"),
        reason=(
            "Dates v0.7.11 October 16, 2026, the day its first Pages deployment went live "
            "(bbc12b61, the merge of PR 631 that landed stack 632, 2026-10-16T01:25:34Z), "
            "and records that deployment in the history's comment (think-tk0u, PR 627 "
            "review B3). The head edition stays v0.7.15 of October 16. No page prints a "
            "date from below the head: the pages stamp the head edition, the films the "
            "v0.4.2 entry, and site_urls --check finds the URL registry and sitemap "
            "unchanged. The deployed index.html and about.html name no v0.7.11. This is a "
            "source-reviewed disposition; no site rebuild or byte comparison is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("site",),
        paths=("packing/frontier/source-coverage.yaml",),
        outputs=(
            "about.html",
            "atlas.html",
            "conventions.html",
            "development.html",
            "epistemics.html",
            "index.html",
            "news.html",
            "papers.html",
            "readme.html",
            "results.html",
            "synopsis.html",
            "tutorial-advanced.html",
            "tutorial.html",
            "visualize.html",
        ),
        reason=(
            "Rendered on this branch over main e2e018f3 with the pin at 288a1a52, once "
            "with main's source register and once with the branch's, the site's pages, "
            "result overviews, case records, forwarders and assets are byte-identical in "
            "all 1470 files render_overview writes. The register moves the reviewed dates "
            "of UnitSquare Release 1 and SQUISH n153 to 16 October and adds a note on "
            "each read (PR 647 review A1). As a data commit it is followed by the re-pin "
            "to 4a9292ec (rule 1), which changes the data hash in the stamp every page "
            "prints; that change is the re-pin's, not the register's."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered on this branch over main e2e018f3 at link revision e2e018f3, once "
            "with main's requests record and source register and once with the branch's, "
            "the HTML and Markdown are byte-identical in all 42 files the renderer writes; "
            "the PDF prints from that HTML and was not rebuilt. The requests record gains "
            "#643's entry, the project's tracking issue for the Lean proof of ValidTilt9, "
            "and the source register moves the reviewed dates of UnitSquare Release 1 and "
            "SQUISH n153 to 16 October with a note on each read (PR 647 review A1); the "
            "survey prints none of them, so it keeps v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.15 for T-193 and T-194 regenerated the five claim documents "
            "at PUBLICATION_REVISION 46ae34f9, this branch's head before the cut, kept "
            "reachable from main by the merge commit the PR merges with; with that "
            "revision read back as 9fe5f941, each is byte-identical to the base's, so the "
            "32 repository links it pins are the only change, and no claim, certificate or "
            "command moves. A link revision follows the site's edition and is not a "
            "revision of the explainer, so it keeps v0.4.7. Source-compared; no render of "
            "the claim documents was taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/default_drawings.py",
            "packing/devtools/regularize_evand.py",
            "packing/frontier/results.yaml",
            "packing/frontier/n-105.md",
            "packing/frontier/n-129.md",
            "packing/frontier/n-146.md",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "The regularization run of 16 October 2026 (think-la7h) changes data only: "
            "default_drawings gains three SETTLED counts (204, 272, 303) and drops nine "
            "from PENDING_ALLOWED, results.yaml changes only its regularized_drawings "
            "items at 105, 129, 146, 156, 176 and 271, and the case records change only "
            "their generated regularization note. The papers read results.yaml's results "
            "(the counts of registered and novel results and the headline bound ladder), "
            "never regularized_drawings, reach default_drawings only through shared "
            "import discovery and read neither constant, and the survey cites n = 105, 129 "
            "and 146 by link only, as its results table's count links. Manuscripts, "
            "figures, credits and print rules are unchanged by source review. Rendered at "
            "one link revision (e2e018f3), once from main e2e018f3's tree and once from "
            "this branch's at 780d81b8, the survey's and both reviews' HTML, before the "
            "browser's math pass, their Markdown and the other 40 files each render "
            "writes are byte-identical (42 of 42 files each); the explainer, whose render "
            "needs a browser this host lacks, is source-reviewed only, and no PDF was "
            "rebuilt. Review D's pass (#644) then added default_drawings.recorded_runs, "
            "which holds each SETTLED entry's runs to a record, reworded the 272 and 303 "
            "outcomes, and added regularize_evand's read-only `rungs --check`; the papers "
            "read none of them, and rendered again at link revision e2e018f3 from this "
            "branch at ebe50691 and from main e2e018f3's tree, the survey's and both "
            "reviews' 42 files each are byte-identical. Review F's pass added "
            "default_drawings.run_records and --retain-runs, which hold a settlement's "
            "runs to the retained evidence, and regularize_evand.run_reports, which lets "
            "`rungs --check` read retained reports; the papers read none of them, and "
            "rendered at link revision e2e018f3 from this branch at 6079926b, the "
            "survey's and both reviews' 42 files each are byte-identical to main "
            "e2e018f3's. Review G's pass added the retained run evidence to the "
            "regularization-state step's touches in sqpack.cli.validate, which only the "
            "explainer declares, as part of the whole sqpack package, and made `rungs "
            "--check` account for each run directory; the papers read neither, the "
            "explainer is source-reviewed only, and rendered at link revision e2e018f3 "
            "from this branch at 2f31507c, the survey's and both reviews' 42 files each "
            "are byte-identical to main e2e018f3's. All four papers keep v0.4.7, v0.1.7, "
            "v0.1.0 and v0.2.2; the site takes the patch."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/exact_sides.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/frontier/README.md",
            "packing/frontier/n-070.md",
            "packing/frontier/n-084.md",
            "packing/frontier/n-086.md",
            "packing/frontier/n-088.md",
            "packing/frontier/n-102.md",
            "packing/frontier/n-103.md",
            "packing/frontier/n-105.md",
            "packing/frontier/n-108.md",
            "packing/frontier/n-123.md",
            "packing/frontier/n-126.md",
            "packing/frontier/n-127.md",
            "packing/frontier/n-129.md",
            "packing/frontier/n-130.md",
            "packing/frontier/n-131.md",
            "packing/frontier/n-146.md",
            "packing/frontier/n-153.md",
            "packing/frontier/n-175.md",
            "packing/frontier/n-179.md",
            "packing/frontier/n-180.md",
            "packing/frontier/n-199.md",
            "packing/frontier/n-207.md",
            "packing/frontier/n-208.md",
            "packing/frontier/n-209.md",
            "packing/frontier/n-236.md",
            "packing/frontier/n-238.md",
            "packing/frontier/n-239.md",
            "packing/frontier/n-261.md",
            "packing/frontier/n-267.md",
            "packing/frontier/n-295.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The house rule (think-sa5r) changes what `select_houses.select` derives, adds "
            "`exact_sides`, stages T-174's 53 counts in `PENDING_ADOPTION`, holds "
            "`default_drawings`' deferrals to the base record and measures staged witnesses "
            "(`upper_bound_houses sizes`); its records passes (reviews A2, C4 and C7 of "
            "#660) reword the notes of the 63 case records the hold and RP-3 named, ten "
            "of them moved below T-174 by #657, nine register entries, five source-register "
            "passages, two requests entries and one evidence limitation to say the hold of "
            "15 October and RP-3's wait ended. Rendered at link revision 6a3a7d8f from main "
            "6a3a7d8f and from this branch, as at 3301a1cf, 5012a97d and c593e2bf before, the "
            "optimality review's, the threshold-bound review's and the survey's HTML and "
            "Markdown are byte-identical, as are all 50 files the three renderers write; "
            "their PDFs print from that HTML and were not rebuilt. The explainer, which "
            "renders through a browser this host lacks, reads the register only to count "
            "its results and the new ones among them, which no edit here changes, and none "
            "of the other inputs: source-compared. All four papers keep v0.4.7, v0.1.7, "
            "v0.1.0 and v0.2.2. The site's case and result pages print the reworded notes, "
            "so the site needs an edition, cut in merge order."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
            "site",
        ),
        paths=("packing/devtools/adopt_houses.py", "packing/devtools/default_drawings.py"),
        outputs=(
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The intake's regularization step (think-g3q7) adds `regularization_owed` to "
            "the house-adoption writer, which its command line prints after a write and a "
            "dry run, and a docstring paragraph. The builders reach the module through "
            "`generate_frontier_case` and `source_supersession`, which call `holds`, "
            "`adopt_case`, `held_note` and `carries_held_note`, never `main` or the new "
            "functions; no case record, coverage row, deferral or prose the writer "
            "produces changes, and its new import of `default_drawings` is one the site's "
            "builders already make. In `default_drawings` (reviews A1 and B1 of #641), "
            "`count_state` no longer reads a count `PENDING_ALLOWED` names as regular as "
            "published, which changes no state today, since every listed count is "
            "pending: `default_drawings --check` passes on the committed record byte for "
            "byte. The new `--compare` report reads two records and no builder calls it; "
            "the builders read `decisions`, `regularized_defaults`, `held_reasons` and "
            "`credit_line`, none of them changed. No render was taken, and every "
            "component keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/default_drawings.py",
            "packing/devtools/regularize_axis_components.py",
            "packing/devtools/regularize_evand.py",
            "packing/devtools/regularize_select.py",
            "packing/devtools/regularized_drawings.py",
            "packing/devtools/render_case_pages.py",
            "packing/src/sqpack/cli/validate.py",
            "packing/frontier/n-070.md",
            "packing/frontier/n-102.md",
            "packing/frontier/n-103.md",
            "packing/frontier/n-236.md",
            "packing/frontier/n-261.md",
            "packing/frontier/n-295.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "The regularization-state record (think-gvke) changes the default-drawings "
            "generator, its decision split from its measuring, and its gate step, the axis "
            "tool's update, check and verify of the atlas index, the layer's admission and "
            "the selection's reference, both now the picture the atlas draws, the "
            "case-record regularization note and the case page's note. The papers reach "
            "these modules through shared import discovery and call none of the changed "
            "functions: no paper renders a case page, a case record's regularization note, "
            "the default-drawings record or the atlas index, or runs the selection. The "
            "survey cites the six case records by link only, as its results table's count "
            "links, and their only change is that note's text. Manuscripts, figures, "
            "credits and print rules are unchanged by source review. No render was taken "
            "(this host has no pinned Chromium), and all four papers keep v0.4.7, v0.1.7, "
            "v0.1.0 and v0.2.2; the site takes the patch."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site cut v0.7.14 regenerated the five claim documents at "
            "PUBLICATION_REVISION 9fe5f941, the merge of main 4e8c8987f; with that revision "
            "read back as main's 7627f47e, each is byte-identical to main's, so the 32 "
            "repository links it pins are the only change, and no claim, certificate or "
            "command moves. A link revision follows the site's edition and is not a "
            "revision of the explainer, so it keeps v0.4.7. Source-reviewed; no render was "
            "taken."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/news_highlights.py",
            "packing/devtools/render_changelog.py",
            "packing/devtools/render_overview.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "The homepage now selects existing canonical News entries and uses the "
            "archive's card renderer. The footer action and linked heading styles belong "
            "to the website. Standalone paper renderers do not call the changed News "
            "composition or include site.css. Removing the unused inline text callback "
            "retains the default Markdown, math, code and link rendering consumed by "
            "papers. The five claim documents change only their source-link revision pins "
            "for this site cut; mathematics, certificates and verifier code are "
            "unchanged. Paper manuscripts, figures and editions remain current. This is a "
            "source-reviewed disposition; no PDF redraw or byte-identity comparison is "
            "claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer", "site"),
        paths=("packing/src/sqpack/cli/validate.py",),
        outputs=(
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "The native validator isolates existing forwarder tests in a fresh "
            "serial process under the shared deadline and records browser progress "
            "and failures before interruption. The manual diagnostic runs fixed "
            "forwarder selections "
            "with wire logs and existing process cleanup; its workflow remains "
            "dispatch-only. Site and paper builders do not run these test commands "
            "or consume their diagnostics. Public renderers, manuscripts, figures "
            "and scientific inputs are unchanged, so both component editions remain "
            "current. This is a source-reviewed disposition; no PDF redraw or "
            "byte-identity comparison is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/news_highlights.py",
            "packing/devtools/render_changelog.py",
            "packing/devtools/site_topics.py",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "News topic selection, filter tallies, surname text-token rendering "
            "and homepage markup "
            "change only News consumers. The shared Results vocabulary and chip "
            "renderer retain their labels and markup. Standalone paper renderers "
            "do not call the changed News functions or include site.css; the optional "
            "inline text callback preserves default callers. Shared-delivery "
            "validation and its audit affect only the News authoring record. The five "
            "regenerated claim documents change only source-link revision pins for "
            "this site cut; their mathematics, certificates and verifier code are "
            "unchanged. Paper manuscripts, figures and editions remain current. "
            "This is a source-reviewed disposition; no release PDF redraw or "
            "byte-identity comparison is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered on this branch over main ee9cec6e at one link revision, once with "
            "main's requests record and once with the branch's, the survey's HTML after "
            "the math pass and its Markdown are byte-identical, as are the other 40 files "
            "the render writes, as they were over bbc12b61; over 22a67ce4 the HTML before "
            "that pass, the Markdown and those 40 files were too. The PDF prints from that "
            "HTML. The record gains the replies of 15 October 2026, six closes, the six "
            "closed entries' confirmation in their summaries and a note on #564, which the "
            "survey does not read, so it keeps v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered on this branch over main 22c0ebf0 at one link revision, once with "
            "main's requests record and once with the branch's, the HTML after the math "
            "pass and the Markdown are byte-identical in all 42 files the renderer writes, "
            "as they were over bbc12b61 and as the HTML before that pass and the Markdown "
            "were over 22a67ce4; the PDF prints from that HTML and was not rebuilt. The "
            "requests record gains the 15 October status replies on twelve of the owner's "
            "tracking issues and five notes; the survey prints none of them and keeps its "
            "edition."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer", "site"),
        paths=("packing/src/sqpack/cli/validate.py",),
        outputs=(
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "The validation CLI adds per-test phase journals only to native quick and "
            "slow pytest commands with external validation artifacts configured. "
            "Site and paper builders neither invoke these commands nor consume their "
            "journals. Test selection, deadlines and resource limits are unchanged. "
            "Public rendering helpers, manuscripts, figures and scientific inputs "
            "are unchanged, so site v0.7.10 and paper v0.4.7 remain current. This is "
            "a source-reviewed finding; no PDF byte-identity comparison is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/news_highlights.py",
            "packing/devtools/render_changelog.py",
            "packing/devtools/site_documents.py",
            "packing/devtools/templates/paper-publication.css",
            "packing/devtools/templates/paper-type.css",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "News and tutorial rendering helpers are selected through shared import "
            "discovery; standalone papers call none of the changed functions. The "
            "paper_front change corrects a stylesheet reference in its docstring. "
            "Existing centred and credits declarations move unchanged between two "
            "stylesheets that every paper already includes. New list-specific credit "
            "rules match tutorials, not the papers' div and span fronts. Standalone "
            "shells omit site.css, so site title spacing does not change paper heroes. "
            "Manuscripts, figures, credit content, computed title and credit layout, "
            "and print rules are unchanged by source review. CSS relocation changes "
            "HTML bytes; no PDF rebuild or byte-identity comparison is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("TUTORIAL.md",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "The survey declares TUTORIAL.md because its unchanged manuscript cites "
            "that file. Citation discovery checks the path and pins its URL; it does "
            "not import tutorial prose. The five actively cited aliases remain beside "
            "relevant current topic links. Survey manuscript, figures and front matter "
            "are unchanged; no PDF rebuild or byte-identity comparison is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "The native site cut regenerates these five claim documents with only "
            "GitHub source-link revision substitutions. Mathematical statements, "
            "certificate inputs and paper content are unchanged. No paper PDF was "
            "rebuilt or compared for byte identity."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/overview_sections.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Rendered on this branch over main 6e73ef1c with the browser's math pass, once "
            "with main's versions of these paths and once with the branch's, the Markdown "
            "and HTML differ only in the live register count beside T-018, 187 results "
            "registered so far and now 192. Over main 4c9af690 the HTML also differed in "
            "where an empty style attribute falls in one formula's span, which moves "
            "between two renders of the branch alone. The claim documents change only the "
            "revision their links pin. A register count follows the site's data and is not "
            "a revision of the paper, so the explainer keeps v0.4.7; the site takes v0.7.11. "
            "Rendered again after the PR #627 review fixes, with the register and source "
            "register as they stood at 52f02f5b and as fixed (T-188 to T-192's notes, "
            "significance and regularizations, two source notes), the Markdown is "
            "byte-identical and the HTML differs only in that same empty style attribute."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/overview_sections.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Rendered on this branch over main 6e73ef1c at one link revision, once with "
            "main's versions of these paths and once with the branch's, the three papers' "
            "HTML, Markdown and PDF are byte-identical, but for one main-side print of the "
            "optimality review, 4 bytes shorter from identical HTML; two further main-side "
            "prints equal the branch's three. The register gains T-188 to T-192 "
            "and edits T-081's claim and T-183's headline, the importer gains three "
            "readers, the About page a card for bengreff/s95-certificate, the requests "
            "record replies and entries, and the source register 267 beyond-horizon rows; "
            "none of the three papers reads any of them, so each keeps its edition: "
            "v0.1.7, v0.1.0 and v0.2.2. Rendered again after the PR #627 review fixes, "
            "with the register and source register as they stood at 52f02f5b and as fixed "
            "(T-188 to T-192's notes, significance and regularizations, two source notes), "
            "the three papers' HTML and Markdown are byte-identical."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/regularized_drawings.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/src/sqpack/cli/validate.py",
            "packing/src/sqpack/gate_budgets.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "The five regenerated claim documents differ only by the source revision "
            "in their GitHub links, verified against main at 31eaf633. The validation "
            "CLI removes automatic check reuse. The explainer's broad sqpack source "
            "declaration includes gate_budgets.py, whose changes govern hosted CALL "
            "timing policy and policy parsing; paper renderers consume neither. "
            "The drawing validator reuses fresh "
            "parsed inputs only within one call; exact report comparisons admit the "
            "imported counts they use and still rebuild every own certificate and "
            "equal the retained claim records. No paper manuscript, figure, scientific "
            "input or rendering helper changes. The lower-bounds paper "
            "retains v0.4.7; the site guide takes v0.7.9. No paper PDF was rebuilt "
            "or compared for byte identity in this slice."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/regularized_drawings.py",
            "packing/devtools/upper_bound_reports.py",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "PR620 changes validation input reuse and exact imported-side admission, "
            "with retained claim equality and drawing refusal/freshness controls. "
            "The same predicates validate every own certificate and each imported "
            "fact used by a comparison. The three manuscripts, figures and rendering helpers "
            "are unchanged, so their editions remain v0.1.7, v0.1.0 and v0.2.2. "
            "This is a source-based no-public-change review; these paper exports "
            "were not rebuilt or compared for byte identity in this slice."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/render_changelog.py",
            "packing/devtools/site_topics.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Result headlines use surnames, and T-153/T-154 descriptive prose is clearer. "
            "The lower-bounds explainer "
            "reads result and novelty counts, which are unchanged, and its n17 paragraph "
            "is fixed manuscript text. The optimality and threshold papers' ladder "
            "figures select none of the changed results. The methods survey substitutes "
            "no result "
            "record text. No paper manuscript, selected ladder value, figure input "
            "or result count changes. The changed news_entries, archived_news_targets "
            "and news_filters functions govern News eligibility, bookmark forwarding "
            "and topic controls; standalone paper renderers call none of them. The "
            "shared topic vocabulary adds only Project; existing result-kind labels "
            "and chip markup are unchanged. Papers retain their own styles and do not "
            "render project-topic chips. This reviewed source-consumer finding does not "
            "claim byte identity for unrebuilt PDFs."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/build_known_best_atlas.py",),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "The shared atlas producer changes only SUMMARY_PROSE, the descriptions "
            "written into the two composite SVGs. These three papers use its shared "
            "typography and publication helpers but consume neither composite. Their "
            "manuscripts, figures, mathematical inputs and helper implementations are "
            "unchanged, as confirmed by independent source and artifact reviews. "
            "They retain v0.1.7, v0.1.0 and v0.2.2 respectively. The lower-bounds "
            "explainer does embed the refreshed atlas and takes its own v0.4.7 patch. "
            "No byte-identity claim is made for unrebuilt PDFs."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "The validation CLI changes ordinary push selection and its explicit slow "
            "option; standalone paper rendering invokes neither. The five regenerated "
            "claim documents differ from main only in repository link revision, from "
            "312dab52 to 6f3d6cc2, as checked directly. Their embedded certificates and "
            "verifiers are unchanged. No paper manuscript, figure, mathematical check "
            "or font declaration changes. The paper keeps v0.4.6. No release PDF was "
            "redrawn or compared for byte identity in this slice."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/overview_sections.py",
            "packing/devtools/probes/preview_site/header.js",
            "packing/devtools/render_changelog.py",
            "packing/devtools/render_n11_lower_bounds_explainer.py",
            "packing/devtools/render_overview.py",
            "packing/devtools/site_topics.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "The shared-import changes affect site reading cards, News filtering and "
            "article metadata. Standalone paper renderers do not call the new card "
            "heading/date helpers or the changed News functions. Existing result topic "
            "keys and labels are unchanged; the removed Documentation topic described "
            "News. Regenerated claim documents only update the revision their links "
            "pin. Manuscripts, figures, scientific records and paper font styles are "
            "unchanged. The new code-symbol fonts are opt-in site assets; standalone "
            "paper font declarations retain their defaults. The preview probe only "
            "distinguishes header tabs from inline controls and changes no paper output. "
            "Each paper keeps its own edition. "
            "No release PDF was redrawn or "
            "compared for byte identity in this slice."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/apply_closed_form.py",
            "packing/devtools/census_atlas_contact_shades.py",
            "packing/devtools/check_half_angle_area.py",
            "packing/devtools/generate_frontier_case.py",
            "packing/devtools/regularize_axis_components.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Rendered from main at c4c690a3 and from this branch with the browser's math "
            "pass, every file the explainer writes is byte-identical but its HTML, which "
            "differs only in where an empty style attribute falls within one formula's span, "
            "as it does between any two renders. The 14 October records and the house "
            "adoption of 15 October 2026, with the site's v0.7.3 cut, do not reach the "
            "explainer, which keeps v0.4.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
        ),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/apply_closed_form.py",
            "packing/devtools/census_atlas_contact_shades.py",
            "packing/devtools/check_half_angle_area.py",
            "packing/devtools/generate_frontier_case.py",
            "packing/devtools/regularize_axis_components.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
        ),
        reason=(
            "Rendered from main at c4c690a3 and from this branch at one link revision, both "
            "papers' HTML, Markdown and PDF are byte-identical. The register's rungs and the "
            "house adoption of 15 October 2026 change the record and its writers; neither "
            "review cites them."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/apply_closed_form.py",
            "packing/devtools/census_atlas_contact_shades.py",
            "packing/devtools/check_half_angle_area.py",
            "packing/devtools/generate_frontier_case.py",
            "packing/devtools/regularize_axis_components.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/n-070.md",
            "packing/frontier/n-084.md",
            "packing/frontier/n-086.md",
            "packing/frontier/n-088.md",
            "packing/frontier/n-102.md",
            "packing/frontier/n-103.md",
            "packing/frontier/n-105.md",
            "packing/frontier/n-108.md",
            "packing/frontier/n-123.md",
            "packing/frontier/n-126.md",
            "packing/frontier/n-127.md",
            "packing/frontier/n-129.md",
            "packing/frontier/n-130.md",
            "packing/frontier/n-131.md",
            "packing/frontier/n-146.md",
            "packing/frontier/n-153.md",
            "packing/frontier/n-154.md",
            "packing/frontier/n-175.md",
            "packing/frontier/n-179.md",
            "packing/frontier/n-180.md",
            "packing/frontier/n-199.md",
            "packing/frontier/n-207.md",
            "packing/frontier/n-208.md",
            "packing/frontier/n-209.md",
            "packing/frontier/n-236.md",
            "packing/frontier/n-237.md",
            "packing/frontier/n-238.md",
            "packing/frontier/n-239.md",
            "packing/frontier/n-261.md",
            "packing/frontier/n-267.md",
            "packing/frontier/n-295.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Rendered from main at c4c690a3 and from this branch at one link revision, the "
            "survey's HTML, Markdown and PDF are byte-identical. Its account of the adopted "
            "houses is dated 11 and 12 October; the case records the house adoption of 15 "
            "October 2026 moves and the register's rungs reach none of its text."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer", "site"),
        paths=("packing/src/sqpack/campaign/ledger.py",),
        outputs=(
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The ledger's `dead_links` pattern moves, character for character, into the "
            "module constant `LINK_TARGET`, so a negative-control test can import it "
            "rather than copy it. What `dead_links` reports is unchanged, and no builder "
            "calls it. No render was taken, and both components keep their versions."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
            "site",
        ),
        paths=("packing/devtools/run_negative_controls.py",),
        outputs=(
            "development.html",
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The negative-control runner is in every builder's import closure through one "
            "path: `upper_bound_houses.custody` imports it inside the function, and only "
            "that module's `custody` subcommand calls it. No builder calls it or reads "
            "what this change edits: the files a mutation worker copies, the link rescue, "
            "the snapshot log and a `--baseline` mode. No render was taken; the finding "
            "rests on that import path, and every component keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
            "site",
        ),
        paths=("packing/devtools/run_negative_controls.py",),
        outputs=(
            "development.html",
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The runner's results-register reader also declares each regularization's "
            "`identity.measured_in`, so two lineage outputs reach mutation workers, and "
            "the snapshot log gains an entry (think-tddb). The import path is the one "
            "recorded for think-b6ir: the runner enters the builders' import closure only "
            "through `upper_bound_houses.custody`, and no builder calls it or reads which "
            "files a worker copies. No render was taken, and every component keeps its "
            "version."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Rendered on this branch over main 6964362b at one link revision, once with "
            "main's versions of these paths and once with the branch's, the HTML before the "
            "browser's math pass and the Markdown differ only in the live register count "
            "beside T-018, 184 results registered so far and now 187; the other 52 files the "
            "render writes are byte-identical. The claim documents change only the revision "
            "their links pin. A register count follows the site's data and is not a "
            "revision of the paper, so the explainer keeps v0.4.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered on this branch over main 6964362b at one link revision, once with "
            "main's versions of these paths and once with the branch's, the three papers' "
            "HTML before the browser's math pass and Markdown are byte-identical. The "
            "register gains T-185 to T-187 and edits T-152, T-158 and T-180's text, the "
            "requests record gains replies and entries, and the source register gains two "
            "rows and Xu's name; none of the three papers reads any of them, so each keeps "
            "its edition."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
            "site",
        ),
        paths=("packing/devtools/upper_bound_reports.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "about.html",
            "atlas.html",
            "conventions.html",
            "development.html",
            "epistemics.html",
            "index.html",
            "news.html",
            "papers.html",
            "readme.html",
            "results.html",
            "synopsis.html",
            "tutorial-advanced.html",
            "tutorial.html",
            "visualize.html",
        ),
        reason=(
            "Rendered on this branch over main 0dd9003e at one link revision, once with this "
            "branch's importer and once with main's in its place, the four papers' HTML and "
            "Markdown and every page, result overview and case record render_overview writes "
            "(1,452 files) are byte-identical. The "
            "importer gains an exact algebraic pending report and the house readers of two "
            "new packets, which no record or page reads yet."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/register_ryxu_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
        ),
        reason=(
            "Rendered from main at 9b32da04 and from this branch with the browser's math "
            "pass, all 55 files the explainer writes, its HTML, Markdown and PDF among "
            "them, are byte-identical. The site v0.7.2 cut moves the claim documents' link "
            "revision; the bound citations credit Xu by name at counts above 11; the "
            "register's credit prose, T-174 and T-180 change; none reaches the explainer, "
            "which keeps v0.4.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review", "paper:n11-threshold-bound-review"),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/register_ryxu_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
        ),
        reason=(
            "Rendered from main at 9b32da04 and from this branch, both papers' HTML, "
            "Markdown and PDF are byte-identical once the build commit their source links "
            "pin is normalized. The register credits Ryan Xu by name, T-174 and T-180 cite "
            "new receipts and evidence, and the house writers name him in the records they "
            "replay; neither review cites any of them."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/register_ryxu_reports.py",
            "packing/frontier/n-051.md",
            "packing/frontier/n-070.md",
            "packing/frontier/n-084.md",
            "packing/frontier/n-086.md",
            "packing/frontier/n-102.md",
            "packing/frontier/n-103.md",
            "packing/frontier/n-105.md",
            "packing/frontier/n-108.md",
            "packing/frontier/n-123.md",
            "packing/frontier/n-126.md",
            "packing/frontier/n-127.md",
            "packing/frontier/n-129.md",
            "packing/frontier/n-131.md",
            "packing/frontier/n-146.md",
            "packing/frontier/n-175.md",
            "packing/frontier/n-261.md",
            "packing/frontier/n-267.md",
            "packing/frontier/n-295.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "Rendered from main at 9b32da04 and from this branch, the HTML, Markdown and "
            "PDF are byte-identical once the build commit their source links pin is "
            "normalized. The case records name Ryan Xu in place of his handle, the "
            "requests record gains the 14 October replies, and Kevin Fang's rows beyond "
            "the corpus become verified; the survey prints none of them and keeps v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "TUTORIAL.md",
            "packing/devtools/news_highlights.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/probes/measure_atlas_views/layout.js",
            "packing/devtools/probes/measure_atlas_views/widen.js",
            "packing/devtools/render_changelog.py",
            "packing/devtools/render_overview.py",
            "packing/devtools/repo_links.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/site_documents.py",
            "packing/devtools/site_topics.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/templates/site-nav.css",
            "packing/devtools/templates/site-nav.html",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-lower-bounds-explainer.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "The four standalone paper manuscripts, mathematical figures and paper-owned "
            "styles are unchanged. The split tutorials publish through the reader-document "
            "pipeline; existing links retain their legacy section landings. Shared import "
            "and page inventories include those reader sources conservatively. News, "
            "topic labels, significance meters, article disclosures, reading-card discovery "
            "and navigation are site chrome. Shared chooser styles also serve the "
            "print-hidden navigation; the paper-owned typography is unchanged. The retained "
            "claim documents and their source-link pin match main. No byte-identical PDF "
            "rebuild is claimed."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review", "paper:n11-threshold-bound-review"),
        paths=(
            "packing/devtools/evand_arrangement_reports.py",
            "packing/devtools/generate_frontier_case.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
        ),
        reason=(
            "Rendered from main at 16ea3bd0 and from this branch at one link revision, "
            "both papers' HTML before the browser's math pass and their Markdown are "
            "byte-identical; the math pass and the PDF take that same HTML. The register "
            "gains T-161 to T-184, the importer reads longer literals, the case generator "
            "replays the closed form, and the site gains two project cards and two page "
            "budgets, none of which either review cites."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/evand_arrangement_reports.py",
            "packing/devtools/generate_frontier_case.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Rendered from main at 16ea3bd0 and from this branch, the HTML before the "
            "browser's math pass and the Markdown differ only in the live register count "
            "beside T-018, 160 results registered so far and now 184. The claim documents "
            "change only the revision their links pin. A register count follows the site's "
            "data and is not a revision of the paper, so the explainer keeps v0.4.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/evand_arrangement_reports.py",
            "packing/devtools/generate_frontier_case.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/run_negative_controls.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/n-105.md",
            "packing/frontier/n-108.md",
            "packing/frontier/n-126.md",
            "packing/frontier/n-127.md",
            "packing/frontier/n-129.md",
            "packing/frontier/n-130.md",
            "packing/frontier/n-131.md",
            "packing/frontier/n-153.md",
            "packing/frontier/n-154.md",
            "packing/frontier/n-175.md",
            "packing/frontier/n-179.md",
            "packing/frontier/n-180.md",
            "packing/frontier/n-207.md",
            "packing/frontier/n-208.md",
            "packing/frontier/n-209.md",
            "packing/frontier/n-236.md",
            "packing/frontier/n-237.md",
            "packing/frontier/n-238.md",
            "packing/frontier/n-239.md",
            "packing/frontier/n-261.md",
            "packing/frontier/n-267.md",
            "packing/frontier/n-295.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered from main at 16ea3bd0 and from this branch at one link revision, the "
            "HTML before the browser's math pass and the Markdown are byte-identical; the "
            "PDF prints from that HTML. Each case record gains the closed form's reported "
            "lower bound, its evidence and resource, a later source_reviewed date and a "
            "dated paragraph, which the case generator now replays; no house moves, so the "
            "survey's account of the adopted houses is unchanged and it keeps v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review", "paper:n11-threshold-bound-review"),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/check_half_angle_area.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/register_regularized_bounds.py",
            "packing/devtools/regularized_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
        ),
        reason=(
            "Rendered from main and from this branch at one link revision, both papers' "
            "HTML and Markdown are byte-identical, and each PDF prints from that HTML. "
            "The helpers adopt and draw upper-bound houses and the register gains T-157 "
            "to T-160, none of which either review cites."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/check_half_angle_area.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/register_regularized_bounds.py",
            "packing/devtools/regularized_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Rendered from main and from this branch, the HTML and Markdown differ only in "
            "the live register count beside T-018, 156 results registered so far and now "
            "160; the order of an empty style attribute on two math spans varies between "
            "any two renders. A register count follows the site's data and is not a "
            "revision of the paper, so the explainer keeps v0.4.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("TUTORIAL.md",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "The tutorial's explainer version label changes from v0.4.5 to v0.4.6. "
            "The methods survey links the tutorial's unchanged anchors without "
            "incorporating its body; its manuscript, figures, references and edition "
            "remain unchanged."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-threshold-bound-review",
            "paper:n11-optimality-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/build_known_best_atlas.py",
            "packing/devtools/overview_sections.py",
            "packing/devtools/render_changelog.py",
            "packing/devtools/render_composite_pdf.py",
            "packing/devtools/render_overview.py",
            "packing/devtools/repo_links.py",
            "packing/devtools/site_documents.py",
            "packing/devtools/validate_schemas.py",
            "packing/src/sqpack/release.py",
        ),
        outputs=(
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/n11-threshold-bound-review.pdf",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-optimality-review.pdf",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
            "papers/square-packing-methods-survey.pdf",
        ),
        reason=(
            "These shared helpers change About assembly, repository links, the "
            "Results legend, schema and closeout checks, and infographic export "
            "transactions. None changes the three untouched papers' manuscripts, figures, "
            "typography, front matter or content editions. The component resolver "
            "retains their own histories, statuses and dates while the site's "
            "history advances independently. Deployment citation "
            "provenance is independent of a paper revision."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "The site v0.6.3 cut regenerates the five claim documents at its new link "
            "revision and changes nothing else in them. The explainer rendered with "
            "main's claim documents and release module and with this branch's is "
            "byte-identical in all 54 files it writes, so the explainer keeps v0.4.6."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered on this branch over main bbc12b61 at one link revision, as over "
            "22a67ce4 before it, once with main's requests record and once with this "
            "branch's, the HTML and Markdown are byte-identical in all 42 files the "
            "renderer writes; the PDF prints from that HTML. The record gains the 15 "
            "October replies on #521 to #527 and #545, two ask notes, a second blocker on "
            "#523's ask and #521's reworded close_when, none of which the survey prints, "
            "so it keeps v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered on this branch over main 4e8c8987 at link revision 4e8c8987, as over "
            "22c0ebf0, ee9cec6e and 3685616d before it, once with main's requests record "
            "and once with this branch's, the HTML and Markdown are byte-identical in all "
            "42 files the renderer writes; the PDF prints from that HTML. The record gains "
            "the 16 October replies held for stack #632, on #413, #506, #533, #561, #573, "
            "#575, #583, #586, #593, #594, #607, #610, #613, #622 and #624, and the final "
            "reply on #596; the closing of #561, #575, #583, #586 and #596; notes on five "
            "replies edited in place, on the held replies on #570 and #574 and on #575's "
            "176, and on why #573 stays open; two statements marked outdated and "
            "corrected, on #506 and #593; #583's reworded not_registered, #596's summary "
            "and a reworded note on #613, none of which the survey prints, so it keeps "
            "v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered on this branch over main e2e018f3 at link revision e2e018f3, once "
            "with main's requests record and once with this branch's, the HTML and "
            "Markdown are byte-identical in all 42 files the renderer writes; the PDF "
            "prints from that HTML. The record gains the 16 October triage entries of #639 "
            "and #640, none of whose results is registered yet, and #622's moved "
            "read_through and a note quoting its author's answer on AI assistance, none "
            "of which the survey prints, so it keeps v0.2.2."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/overview_sections.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered on this branch over its base 71f6a413 (PR #642, on main e2e018f3) at "
            "link revision e2e018f3, once with the base's versions of every changed record "
            "and once with this branch's, the three papers' HTML and Markdown are "
            "byte-identical in all 50 files the renderers write; each PDF prints from that "
            "HTML. The register gains T-193 and T-194, the source register two sources and "
            "the requests record #639's and #640's mappings to them, and the site's Other "
            "Projects list a card for ofitzharding/sq19; none of the three papers prints "
            "any of them, so each keeps its edition: v0.1.7, v0.1.0 and v0.2.2. Rendered "
            "again with the branch after #639's replay (T-193 at V3/C3) and the card, the "
            "six files are byte-identical to the base's."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=("packing/devtools/overview_sections.py", "packing/frontier/results.yaml"),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Rendered on this branch over its base 71f6a413 with the browser's math pass, "
            "once with the base's versions of every changed record and once with this "
            "branch's, the Markdown and HTML differ only in the live register count beside "
            "T-018, 192 results registered so far and now 194, and the HTML also in where "
            "an empty style attribute falls in one formula's span, which moves between two "
            "renders of the same input; rendered again after #639's replay and the sq19 "
            "card, the same holds. A register count follows the site's data and is not a "
            "revision of the paper, so the explainer keeps v0.4.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered on this branch over main e2e018f3 at link revision e2e018f3, once "
            "with main's register and source register and once with this branch's, the "
            "four papers' HTML before the browser's math pass, which this host cannot run, "
            "and their Markdown are byte-identical; the PDFs print from that HTML. The "
            "register's T-184 and T-191 cite the s(76) and s(95) replays and the 16 October "
            "review, rise to V3/C1 and change their headline, claim, composition, "
            "next_rung, notes, artifacts and unfinished confirmations, with the register "
            "count unchanged, and the two "
            "source rows cite the replays; no paper prints any of it, so each keeps its "
            "edition."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-optimality-review", "paper:n11-threshold-bound-review"),
        paths=(
            "packing/devtools/adopt_houses.py",
            "packing/devtools/check_source_coverage.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
        ),
        reason=(
            "Rendered from this branch at 05ef0f60 and from main 804eff36 at link revision "
            "804eff36, the two reviews' HTML and Markdown are byte-identical; each PDF "
            "prints from that HTML. The register gains T-195, PR #622's N29 certificate, "
            "the house writer adopts it at 29, the coverage check reads a catalogue print "
            "to its last place, and the drawings record settles 29; neither review prints "
            "any of it, so each keeps its edition: v0.1.7 and v0.1.0."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/check_source_coverage.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Rendered from this branch at 05ef0f60 and from main 804eff36 with the "
            "browser's math pass, the Markdown and HTML differ only in the live register "
            "count beside T-018, 194 results registered so far and now 195. A register "
            "count follows the site's data and is not a revision of the paper, so the "
            "explainer keeps v0.4.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/check_results.py",
            "packing/devtools/overview_data.py",
            "packing/devtools/result_overview.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/validate_schemas.py",
            "packing/devtools/verifier_registry.py",
            "packing/frontier/README.md",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Rendered for PR #645 at link revision b23abea0, once from this branch's tree "
            "at a6e1bf30 and once with main's 14fd9e27 copies of the branch's changed files: "
            "the three papers' HTML and Markdown and every asset their renderers write are "
            "byte-identical, and each PDF prints from that HTML. The branch separates "
            "source verification from confirmation, moves T-154 from V0 to V3 and changes "
            "the assurance predicates, record links and the n = 17 page ceiling; none of "
            "the three papers prints T-154, its evidence or those predicates' results, so "
            "each keeps its edition: v0.1.7, v0.1.0 and v0.2.3."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/devtools/check_results.py",
            "packing/devtools/overview_data.py",
            "packing/devtools/result_overview.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/site_urls.py",
            "packing/devtools/validate_schemas.py",
            "packing/devtools/verifier_registry.py",
            "packing/frontier/results.yaml",
            "packing/src/sqpack/assurance.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "Rendered for PR #645 with the browser's math pass, once from this branch's "
            "tree at a6e1bf30 and once with main's 14fd9e27 copies of the branch's changed "
            "files: the Markdown is byte-identical and the HTML, 1,416,033 bytes on both, "
            "differs only in where an empty style attribute falls in two formulas' spans, "
            "which moves between two renders of the same input. The register count is 217 "
            "on both. The explainer prints no rung of T-154, so it keeps v0.4.8."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer",),
        paths=(
            "packing/cases/n11_fractional_certificate/t-018-proof-card.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-19-5.md",
            "packing/cases/n11_fractional_certificate/t-018-verifiable-claim-381-100.md",
            "packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md",
            "packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
        ),
        reason=(
            "PR #645's site v0.7.33 cut regenerated the five claim documents, and every "
            "changed line differs from main only in its source-link revision, b23abea0 to "
            "d24b3bf9. The explainer links those documents rather than inlining them, so "
            "its HTML and Markdown are unchanged by them and it keeps v0.4.8. This is a "
            "source-reviewed disposition; the render comparison above predates the cut."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
            "site",
        ),
        paths=("packing/devtools/run_negative_controls.py",),
        outputs=(
            "development.html",
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The runner's `UNREAD_WORKER_OUTPUTS` gains 220 historical files that mutation "
            "workers no longer copy, and the snapshot log gains an entry (think-bl1p). The "
            "import path is the one recorded for think-b6ir: the runner enters the "
            "builders' import closure only through `upper_bound_houses.custody`, and no "
            "builder calls it or reads which files a worker copies. No render was taken, "
            "and every component keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
            "site",
        ),
        paths=("packing/devtools/run_negative_controls.py",),
        outputs=(
            "development.html",
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The runner's `UNREAD_WORKER_OUTPUTS` gains 121 entries (599 files) and its "
            "`ON_REQUEST_IMPORT_TOOLS` four tools with their tests, which mutation workers "
            "no longer copy, and the snapshot log gains an entry (think-i903). The import "
            "path is the one recorded for think-b6ir and think-bl1p: the runner enters the "
            "builders' import closure only through `upper_bound_houses.custody`, and no "
            "builder calls it or reads which files a worker copies. No render was taken, "
            "and every component keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
            "site",
        ),
        paths=("packing/devtools/run_negative_controls.py",),
        outputs=(
            "development.html",
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The runner gains `module_name` and `registered_mentions`, which only "
            "`--audit-snapshot` calls, and the `REGULARIZATION_TOOLS` comment is corrected "
            "(think-wtso, think-cmbx). No prune list, cap or import changes. The import "
            "path is the one recorded for think-b6ir and think-bl1p: the runner enters the "
            "builders' import closure only through `upper_bound_houses.custody`, and no "
            "builder calls it or reads which files a worker copies. No render was taken, "
            "and every component keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
            "site",
        ),
        paths=("packing/devtools/run_negative_controls.py",),
        outputs=(
            "development.html",
            "index.html",
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The owner's reset of 22 October 2026 (think-d2he, think-t1lk): "
            "`SNAPSHOT_MAX_BYTES` goes from 255 to 512 MiB and its dated log of raises "
            "gives way to a short rationale, with four comments that cited the log "
            "repointed to it in Git. Worker selection is unchanged. The import path is "
            "the one recorded for think-b6ir and think-bl1p: the runner enters the "
            "builders' import closure only through `upper_bound_houses.custody`, and no "
            "builder calls it or reads the cap. No render was taken, and every component "
            "keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/render_changelog.py", "packing/src/sqpack/cli/validate.py"),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The S4 and S5 announcement gate (think-9wxc): `render_changelog` gains "
            "`check_announcements` and its helpers, called only by its own `main` under "
            "`--announcement-base`, and the records tier's synopsis step passes that flag. "
            "No existing function changes. The papers reach `render_changelog` only "
            "through `site_documents`, which calls `entry_anchor`, and no builder calls "
            "`validate._synopsis`. No render was taken, and every paper keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/render_changelog.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Review A of #735 and of #738 (think-9wxc): the announcement gate's owed "
            "items fail only a pull request that changes the register or News, and on main "
            "only warn. `check_announcements` returns its findings in three lists; two "
            "helpers are renamed to public names (`register_score`, `announcement_base`) "
            "and one is new (`edits_announcement_records`); `main` prints warnings. The "
            "papers reach `render_changelog` only through `site_documents`, which calls "
            "`entry_anchor`, unchanged. This also corrects #735's record above, whose "
            "`No existing function changes` was wrong: no function the papers reach "
            "changed, while `main` gained the flag and `_synopsis` passed it. No render "
            "was taken, and every paper keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:n11-lower-bounds-explainer", "paper:square-packing-methods-survey"),
        paths=(
            "packing/devtools/probes/prepare_n11_lower_bounds_explainer_math/measure_math.js",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The explainer's math extraction (think-qa8b) re-appends each extracted `style` "
            "attribute last, where Chromium places a style written through CSSOM when "
            "nothing reads the attribute list early. Every `style` in main's ordinary "
            "render already sits last, so this removes only the timing-dependent outlier "
            "that failed the twin-render check. Rendered with --prepare-math in pinned "
            "Chromium 151.0.7922.34 on 23 October: three fixed renders equal, in every "
            "written file, four unfixed renders whose concurrent twins agreed (12 of 12 "
            "comparisons), and six fixed concurrent pairs agree where unfixed pairs "
            "failed 2 of 6. The survey selects this probe as a broad builder input and "
            "does not run it; its HTML and Markdown are identical before and after. "
            "Every paper keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/overview/embed.js",
            "packing/devtools/overview_sections.py",
            "packing/devtools/probes/check_site_rendering/report.js",
            "packing/devtools/probes/measure_atlas_views/expansion.js",
            "packing/devtools/probes/measure_atlas_views/hold.js",
            "packing/devtools/probes/measure_atlas_views/layout.js",
            "packing/devtools/probes/measure_atlas_views/move.js",
            "packing/devtools/probes/measure_site_pages/math_faces.js",
            "packing/devtools/probes/preview_site/math_face.js",
            "packing/devtools/record_presentation.py",
            "packing/devtools/render_case_pages.py",
            "packing/devtools/render_contributors.py",
            "packing/devtools/site_tallies.py",
            "packing/devtools/templates/site-nav.css",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The Atlas that follows the scroll, the end of its Show More expander and the "
            "smaller choosers (think-apqd) change only site chrome the papers share: the "
            "head bootstrap gains a root attribute set only at an address ending in `/`, "
            "`/index.html` or `/atlas.html`, where the two Atlas pages are served and no "
            "paper is, "
            "`site-nav.css` the small chooser's size, which no paper uses, and the Atlas's "
            "markup, measuring tool and probes, which no paper runs. The case record's "
            "steps on its count's line change only the case pages, and the math-face "
            "probes lose the steps' surface. The profiles directory's introduction, the "
            "All Profiles label and the tallies' shared separator change only site pages. "
            "Rendered again on 23 October, after all of these, "
            "from this tree and from main 44df28b07 into empty site directories "
            "with source links pinned to 44df28b07 (69 files each): every paper's Markdown "
            "is byte-identical, and each paper's HTML differs only in the inlined head "
            "bootstrap and the hashed name of `site-nav.css`. Every paper keeps its "
            "version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/site_navigation.py",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The homepage keeps the name its renderer gives it, The Squares Project, as "
            "its title and link-preview title instead of its menu label, Overview (the "
            "owner, 23 October). `navigation_title` changes only for the site root's "
            "address, which no paper has and no paper's trail reaches. Rendered on 23 "
            "October from this tree into an empty site directory with source links "
            "pinned to 44df28b07 (69 files): every paper's Markdown is byte-identical "
            "to main 44df28b07's, and each paper's HTML is identical to the render of "
            "PR 746's head but for that head's later compaction of the inlined "
            "bootstrap. Every paper keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/probes/preview_site/header.js",
            "packing/devtools/render_contributors.py",
            "packing/devtools/source_supersession.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Three small cleanups no paper reads: the non-stacked profile tally joins its "
            "counts with the shared tally separator, a form only the tests call; the "
            "header probe's opening comment no longer describes the Film and Workbench "
            "tabs removed on 22 October; and the coverage register's YAML node tree is "
            "composed once per text, which changes no output. Rendered on 23 October from "
            "this tree and from main da117ad0b into empty site directories with source "
            "links pinned to da117ad0b (69 files each): every file, each paper's Markdown "
            "and HTML among them, is byte-identical. No PDF was printed; each prints from "
            "that HTML. Every paper keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=("packing/devtools/templates/site-nav.css",),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Only a comment in `site-nav.css` changes: the section-tab rules no longer "
            "name the Film/Workbench switcher, gone since 2026-10-22. Rendered on 24 "
            "October from this tree and with main 1aa953fad's stylesheet into empty site "
            "directories with source links pinned to 1aa953fad (69 files each): every "
            "paper's Markdown is byte-identical, and each paper's HTML differs only in "
            "the hashed name of the stylesheet. Every paper keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/frontier/n-105.md",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The authors' answers of 23 October on #670, #675 and #715 and T-226's "
            "lineage through T-186 (think-t5hc): the chain credit of T-226, T-228, T-223, "
            "T-225, T-229 and T-231, their claim and notes sentences, the 204 house's "
            "packing phrase in adopt_houses, the regularization credit the case records "
            "copy, and the request entries for #670, #675, #715, #719 and #734, against "
            "main 5664ac1e8 (#758): rendered at link revision f3154f21 into empty site "
            "directories, twice from this tree and once from it with main's four "
            "candidate inputs swapped in (69 files each), "
            "render_n11_lower_bounds_explainer with its math pass, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write every file byte-identical across all three. "
            "No result is registered, so the explainer's count is unchanged. Re-measured "
            "after review A's fixes (19867ffe7) and the merge of main 14b14f2d1: rendered "
            "at link revision 59614d78, twice from this tree and once with main "
            "14b14f2d1's four candidate inputs swapped in, all 69 files byte-identical "
            "again. Measured once more after the merge of main c5697c2f2 (#745, #750, "
            "#757, #759, #771), at link revision 54f34f78, twice from this tree and once "
            "with main c5697c2f2's four candidate inputs swapped in: all 69 files "
            "byte-identical across the three. No PDF was printed; each prints from that "
            "HTML. Retain v0.4.25, main's explainer after T-239, v0.1.11, v0.1.4 and "
            "v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/profile_records.py",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "T-163's family assessment and the owner's answer “Credit both "
            "(Recommended)” (think-rh4j, think-cwfi): the record index reads the stored "
            "record_scope assessment, which the gate recomputes, and credits every entry "
            "of one report registered twice; T-163's rationale, notes, next_rung and "
            "composition name Ryu's Theorem 1.3 window, the published note and why V2 is "
            "held; four entries name the beads that own their unfinished confirmations; "
            "and the requests record gains the fourteen tracking issues #772 to #780 and "
            "#782 to #786. Measured against main 5664ac1e8, 14b14f2d1 and 2c58b6373 "
            "(#750), and last, after review A's fixes (think-q5sr) and the merges of main "
            "c5697c2f2 (#757), 5f8f005a3 (#766) and 34eb8bb75 (#769), at link revisions "
            "5f8f005a and then 34eb8bb7: each time rendered "
            "into empty site directories, twice from this tree and once from it with that "
            "main's profile_records.py, results.yaml and result-requests.yaml swapped in, "
            "render_n11_lower_bounds_explainer, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write all 69 "
            "files byte-identical across the three. No PDF was printed; each prints from "
            "that HTML. Retain v0.4.25, main's explainer after T-239, v0.1.11, v0.1.4 and "
            "v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The stage 7 records of 24 October (think-9i18): the #446 follow-up and the "
            "#755 final reply, #755 closed, #534's result mapped to T-232, #536's ask "
            "done by T-235, and #603 read through a social comment, against main "
            "5f8f005a3 (#766): rendered at link revision 5f8f005a into empty site "
            "directories, twice from this tree and once from it with main's "
            "result-requests.yaml swapped in (43 files each), render_packing_methods "
            "writes every file byte-identical across all three. Measured again after the "
            "#670 and #734 final replies and the #719 follow-up were recorded, #734 "
            "closed: twice from this tree, 43 files each, byte-identical to each other "
            "and to the render with main's file. Measured once more after the merge of "
            "main 34eb8bb75 (#769), at link revision 34eb8bb7, twice from this tree and "
            "once with that main's result-requests.yaml swapped in: all 43 files "
            "byte-identical across the three, and again twice from this tree after the "
            "#715 and #719 follow-ups and the #732 import reply were recorded, both "
            "byte-identical to that render. Measured again after the merge of main "
            "11d0ab06b (#770), at link revision 11d0ab06, and last after the merge of "
            "main e5c1c64e3 (#756) and the sixteen replies posted after #770, at link "
            "revision e5c1c64e: each time twice from this tree and once with that main's "
            "result-requests.yaml swapped in, all 43 files byte-identical across the "
            "three. No PDF was printed; it prints from that HTML. Retain v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/check_results.py",
            "packing/devtools/site_resources.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The retention of Kevin Fang's note v0.9 and Lean proof (think-494l): T-163 "
            "from V2 to V3 with two new evidence entries, its claim, notes, composition, "
            "next steps and unfinished confirmations rewritten, two coverage sources and "
            "issue 603's requests entry, against main af9c9e850 (#745): rendered at link "
            "revision 46effd32 into empty site directories, twice from this tree at "
            "46effd32 and twice from the same tree with main's register, requests record "
            "and coverage record swapped in (69 files each), "
            "render_n11_lower_bounds_explainer, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write every file "
            "byte-identical across all four. Measured once more after merging main "
            "2c58b6373 (#750), at link revision 2d39f5ca with that main's three files "
            "swapped in: the same outcome, and the register stays at 238 results. After "
            "the two resource cards (site_resources.py), measured again at link revision "
            "2821d8a6 with that main's four files swapped in: the same outcome. Measured "
            "once more after merging main c5697c2f2 (#757), at link revision 0ffac35f "
            "with that main's four files swapped in: the same outcome, the register at 239 "
            "results. Measured once more after merging main 5f8f005a3 (#766), at link "
            "revision bba0bfff with that main's four files swapped in: the same outcome. "
            "And after merging main 34eb8bb75 (#769), at link revision d63381d5, and main "
            "11d0ab06b (#770), at link revision 8753d8dc, and main e5c1c64e3 (#756), at "
            "link revision b133025b, each with that main's four files swapped in: the same "
            "outcome. After review A's fixes (a third evidence entry, the replay of the "
            "note's 18 pieces, and T-163's claim, notes, next steps and composition) and "
            "the merge of main 6808d293a (#787), at link revision 98ce1995: twice from this "
            "tree and once with that main's four files swapped in, 69 files each, all "
            "byte-identical across the three; the explainer's math was prepared by the "
            "host's Chrome for Testing 153 headless shell through SQPACK_CHROMIUM, the same "
            "browser for every render. Main b2ea7b09c (#788), merged after, changes none "
            "of the four files, so that measurement stands for it. After review B's fixes, "
            "which add check_results.py (verification_level, a refactor of one atom), and "
            "the merge of main f354a34f5 (#736), at link revision 3d96fba0: twice from this "
            "tree and once with that main's five files swapped in, 69 files each, all "
            "byte-identical across the three, by the same browser. No PDF was printed; each "
            "prints from that HTML. Every paper keeps its version."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "Couzo's answers of 24 October on #672, #678 and #715 (think-mdfr): T-227's "
            "and T-225's credit sentences and T-227's notes, the request entries for "
            "#672, #678, #715, #534 and #536, and three sources' review dates, against "
            "main b2ea7b09c (#788): rendered at link revision ba711683 into empty site "
            "directories, twice from this tree and once from it with main's three "
            "candidate inputs swapped in (69 files each), "
            "render_n11_lower_bounds_explainer with its math pass, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write every file byte-identical across all three. "
            "No result is registered, so the explainer's count is unchanged. Measured "
            "again after #534's final reply record listed its report entry: "
            "render_packing_methods at the same link revision writes all 43 files "
            "byte-identical to that render. After review A's fixes and the merge of main "
            "f354a34f5 (#736), at link revision 92c52f36, and after the merge of main "
            "830dfb470 (#781) and the two TheSnakeFang reads, at link revision bb3d4913: "
            "each time twice from this tree and once with that main's three candidate "
            "inputs swapped in, 69 files each, all byte-identical across the three, the "
            "explainer's math prepared by the same headless shell every time. After "
            "#603's follow-up of 11:29:46Z was recorded, render_packing_methods at link "
            "revision bb3d4913 writes all 43 files byte-identical to that render. No PDF "
            "was printed; each prints from that HTML. Retain v0.4.25, v0.1.11, v0.1.4 and "
            "v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The #763 import (think-ptkk): T-240's registration of Francisco Couzo's "
            "certificates at 268 and 303 as reported, the 194 beyond-horizon rows of the "
            "couzo-issue763-2026-10-23 and couzo-964ee2b-2026-10-23 sources with their 186 "
            "supersessions, and #763's request entry, against main b2ea7b09c (#787, #788): "
            "rendered at link revision ac5fdd52 into empty site directories, twice from "
            "this tree and once from it with main's results.yaml, result-requests.yaml and "
            "source-coverage.yaml swapped in, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write all 51 "
            "files byte-identical across the three. The explainer, counting 239 to 240 "
            "results, takes v0.4.26 over main's v0.4.25. No PDF was printed for these "
            "three; each prints from that HTML. Retain v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/acquire_source.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The think-l49q import: T-241's and T-242's registration of Francisco Couzo's "
            "304 and Evan Daniel's exact descents at 268 and 304 as reported, their two "
            "coverage sources, the importer's read of a certificate another packet "
            "retains, #763's import reply, and reviews A's and B's credit, push-dating "
            "and twin-reader fixes (acquire_source.twin_bytes), against main 2ec489d1e "
            "(#789): rendered at link revision 2ec489d1 into empty site directories, twice "
            "from this tree at 3a9c5b60 and once from it with main's result-requests.yaml, "
            "acquire_source.py, upper_bound_reports.py, results.yaml and "
            "source-coverage.yaml swapped in, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write all 51 files byte-identical across the three. "
            "The explainer, counting 240 to 242 results, takes v0.4.27 over main's "
            "v0.4.26. No PDF was printed for these three; each prints from that HTML. "
            "Retain v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/evand_exact_certificates.py",
            "packing/devtools/goebel_construction.py",
            "packing/devtools/intake_ledger.py",
            "packing/frontier/README.md",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "W7 of the rows above 1024 (think-llit) moves Göbel's construction beyond 324 "
            "to the new maintained module goebel_construction, which intake_ledger now "
            "imports, adds a summary README for walks of more than 400 counts, and states "
            "the frontier README's beyond-horizon rules with no ceiling; #793's first "
            "review round moves evand_exact_certificates' header rule into header(), which "
            "parse calls with the same checks, messages and order. No paper reads Göbel's "
            "construction, a walk or the frontier README's Source Coverage text; they reach "
            "intake_ledger, the new module and the parser only through shared import "
            "discovery, and the survey declares the frontier README as a whole. Rendered "
            "from this branch's tree at ae6c93fe0 and from main 2ec489d1e's versions of the "
            "three changed files, at the link revision 2ec489d1e, the survey's and both "
            "reviews' HTML and Markdown and every other file the three renderers write are "
            "byte-identical (51 of 51); measured again after the merge of main 3480b5fd3 "
            "(#792), from the merged tree at 96bbef3b5 and from it with main's versions of "
            "the three files, at link revision 3480b5fd3: 51 of 51 byte-identical. The "
            "explainer, whose render needs a browser this host lacks, is source-reviewed "
            "only, and no PDF was printed. All four papers keep their versions, the "
            "explainer v0.4.27."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/contributors/people/alexchilton.md",
            "packing/contributors/people/aqibrazadev.md",
            "packing/contributors/people/kirill-tymchishin.md",
            "packing/contributors/people/kyleluecke.md",
            "packing/contributors/people/vladislav-lavrentev.md",
            "packing/devtools/intake_ledger.py",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The import of the Kaggle-notebook sides of the push that published 964ee2b, "
            "read commit by commit after #795's reviews A and B (think-lyf9): 185 "
            "beyond-horizon rows of nine new coverage sources at the 99 notebook counts, 86 "
            "supersessions of main's rows and 86 within the push, #763's request entries "
            "for them, the walk's commit order for reports of one instant and its gate "
            "(intake_ledger), and profiles for Kirill Tymchishin, Vladislav Lavrentev, "
            "kyleluecke, alexchilton and aqibrazadev, against main dd0061553 (#793): "
            "rendered at link revision df7c42cd into empty site directories, twice from "
            "this tree and once from it with main's result-requests.yaml, "
            "source-coverage.yaml and intake_ledger.py swapped in and the five profiles "
            "removed, render_n11_lower_bounds_explainer, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write all 69 "
            "files byte-identical across the three; measured first against main 3480b5fd3 "
            "(#792) at link revision e9164d19, with the same result. No register entry is "
            "added, so the explainer's result count is unchanged. No PDF was printed; each "
            "prints from that HTML. Retain v0.4.27, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "PR B of the #763 import (think-bk9r): T-240 from V0/C0 to V3/C3 after the 24 "
            "October review, with three evidence entries, its claim, notes and next steps "
            "rewritten, #763's requests entry, the adoption at 268 and 303 in the pass of 25 "
            "October with the in-corpus coverage source, the house writer's prose and "
            "credits, the reader, SETTLED[268] removed, the bound citations, the composite "
            "records and the screen's findings, against main 2ec489d1e (#789): rendered at "
            "link revision 8977b819 into empty site directories, twice from this tree and once "
            "from it with main's ten candidate inputs swapped in (69 files each), "
            "render_n11_lower_bounds_explainer with its math prepared by the host's Chrome "
            "for Testing headless shell through SQPACK_CHROMIUM, the same browser for every "
            "render, render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write every file byte-identical across all three. No "
            "result is registered, so the explainer's count is unchanged. No PDF was "
            "printed; each prints from that HTML. Measured again after the records tier's "
            "fixes (T-240's claim and notes, adopt_houses' prose rewrapped), at link revision "
            "dce05249 with the same ten files swapped in: twice from this tree and once "
            "swapped, 69 files each, all byte-identical across the three, by the same "
            "browser. Measured once more after the rigidity blocks and the composite "
            "figure's record at 268 and 303, at link revision ff9e896e with the same ten "
            "files swapped in: the same outcome. After review A's fixes to T-240's notes, at "
            "link revision 9ebc1357 with the same ten files swapped in: the same outcome. "
            "After the merge of main 3480b5fd3 (#792), which cut the explainer at v0.4.27, "
            "at link revision 180587e4 with that main's nine candidate inputs swapped in: "
            "twice from this tree and once swapped, 69 files each, all byte-identical "
            "across the three, by the same browser; both sides count 242 results. After the "
            "merge of main 2ed0ea740 (#793, #796, #795), at link revision 5adbe808 with "
            "that main's nine candidate inputs swapped in: twice from this tree and once "
            "swapped, 69 files each, all byte-identical across the three, by the same "
            "browser; both sides count 242 results. After T-240's notes said previous_source "
            "is the parent only at 268 and 303 (think-vm3m), at link revision be46a31a with "
            "the same nine files swapped in: the same outcome. Retain v0.4.27, v0.1.11, "
            "v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The #797 and Daniel deficiency-rows import (think-4tj5, think-f8py): #797's "
            "requests entry, against main 755ef426b (#794). Rendered by "
            "render_packing_methods at link revision 541a19d4 into empty site directories, "
            "twice from this tree and once with main's result-requests.yaml swapped in, 43 "
            "files each, all byte-identical across the three. No register entry changes. "
            "Retain v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The import of Couzo's 43f666c at or below 1024 and of #763's 13 recipes "
            "(think-gn29, think-g2qy): 122 beyond-horizon rows of the new source "
            "couzo-43f666c-2026-10-24, 13 of the new source couzo-issue763-2026-10-23-recipes "
            "(#800's review A, A1), their supersessions, and #763's request entries for them, "
            "against main 2ed0ea740 (#795): rendered at link revision ab7cbfb0 into empty site "
            "directories, twice from this tree and once with main's result-requests.yaml and "
            "source-coverage.yaml swapped in, render_packing_methods writes all 43 files "
            "byte-identical across the three; measured again after merging main 755ef426b "
            "(#794) at link revision 61602a47, after review A's source split at link "
            "revision 00f19d7f, and after merging main 3e1349802 (#801) at link revision "
            "5239214a with that main's two files swapped in, with the same result. No register "
            "entry is added. No PDF was printed; it prints from that HTML. Retain v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/site_resources.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The import of #798's twelve beyond-horizon rows and #755's answers "
            "(think-2l0q, think-fc1n): a new coverage source with 12 rows superseding 12 of "
            "main's, the #798 request entry and #755's, T-239's notes and claim, and "
            "upper_bound_reports admitting a derived fact beside a file its packet retains, "
            "against main 755ef426b (#794): rendered at link revision a2a4953a into empty "
            "site directories, twice from this tree and once from it with main's "
            "result-requests.yaml, upper_bound_reports.py, results.yaml and "
            "source-coverage.yaml swapped in, render_n11_lower_bounds_explainer, with its "
            "math prepared by Playwright's pinned headless shell, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write all 69 files byte-identical across the three; "
            "measured first against main 2ed0ea740 (#795) at link revision bda51090, with "
            "the same result. With the other-projects card for #798's gist added to "
            "site_resources.py, measured again at link revision 23bd0a0f with main's five "
            "changed inputs swapped in: twice from this tree and once swapped, 69 files "
            "each, all byte-identical across the three; and after fact_witness read the "
            "manifest only for a retained file, at link revision 275bfa37 with the same five "
            "files swapped in: the same outcome. After the merge of main 3e1349802 (#801) "
            "and review A's fixes, at link revision a2e585e7 with that main's five candidate "
            "inputs swapped in: twice from this tree and once swapped, 69 files each, all "
            "byte-identical across the three. After the merge of main 4089f9587 (#800) and "
            "the re-chain through 43f666c's rows, at link revision 5db7c5f6 with that main's "
            "five candidate inputs swapped in: the same outcome, 69 files each. No register "
            "entry is added, so the "
            "explainer's result count is unchanged. No PDF was printed; each prints from "
            "that HTML. Retain v0.4.27, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/regularized_drawings.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "H1 of think-hx0e and think-o4m0: T-241 and T-242 from V0/C0 to V3/C3 after the 24 "
            "October review, with four evidence entries, their claims, notes and next steps "
            "rewritten and the review's credit finding M-1 applied; #795's notebook rows at "
            "364, 450 and 874 credited to their finders alone in the coverage notes and "
            "#763's requests entry; the #763 reply of 25 October recorded; T-242 adopted at "
            "304 in the pass of 25 October with its house prose and credit, SETTLED[304] made "
            "again on the new witness, 268 staged for the next pull request, and the bound "
            "citations, composite records and the screen's findings, against main 755ef426b "
            "(#794): rendered at link revision d0c132c3 into empty site directories, twice "
            "from this tree and once from it with main's ten candidate inputs swapped in, "
            "render_n11_lower_bounds_explainer with its math prepared by the host's Chrome "
            "for Testing headless shell through SQPACK_CHROMIUM, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write all 69 files byte-identical across the three. No "
            "result is registered, so the explainer's count is unchanged. No PDF was "
            "printed; each prints from that HTML. Measured again after review A's fixes "
            "(#763's awaiting-author items, T-241's and T-242's claims and notes, a "
            "regularization item's own credit, the staging bead) and the merge of main "
            "3e1349802 (#801), at link revision 1881510f with that main's eleven candidate "
            "inputs, regularized_drawings.py among them, swapped in: twice from this tree "
            "and once swapped, 69 files each, all byte-identical across the three, by the "
            "same browser. After the merge of main 4089f9587 (#800) and the import reply of "
            "25 October recorded on #763, at link revision 37f9fc79 with that main's eleven "
            "candidate inputs swapped in: the same outcome. After the merge of main "
            "3bdff2443 (#802), at link revision 3287d38d with that main's eleven candidate "
            "inputs swapped in: the same outcome. Retain v0.4.27, v0.1.11, v0.1.4 and "
            "v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The mapping of the stage 4 review of Kevin Fang's Theorem A (think-vfz9): "
            "#797's requests entry, with the acknowledgement and the review, against main "
            "3e1349802 (#801). Rendered by render_packing_methods at link revision 8ceeb75d "
            "into empty site directories, twice from this tree and once with main's "
            "result-requests.yaml swapped in, 43 files each, all byte-identical across the "
            "three; measured again after merging main 4089f9587 (#800) at link revision "
            "64262ade with that main's result-requests.yaml swapped in, and after merging "
            "main 3bdff2443 (#802) and review A's fixes with the #798 and #755 replies, at "
            "link revision eb9cd8cc with that main's result-requests.yaml swapped in, and "
            "after merging main 3699ce15e (#803), at link revision 4eaa86c6 with that main's "
            "result-requests.yaml swapped in: the same result. No register entry changes. "
            "Retain v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/frontier/README.md",
        ),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "W8 of think-clgp: #799's requests entry with triage pending, and a sentence "
            "beside D2's recipe rule in the frontier README naming the two-strip checker, "
            "against main bb756e193 (#805). Rendered by render_packing_methods at link "
            "revision 52c7b2ce into empty site directories, twice from this tree and once "
            "with main's result-requests.yaml and frontier README swapped in, 43 files each, "
            "all byte-identical across the three. Measured again after review A of #808 set "
            "the entry's triage to done and reworded its summary, at link revision ff752564 "
            "with the same two inputs of main swapped in: the same outcome. After the second "
            "triage of #799 (think-z2mj) rebuilt the entry with version 2's results and "
            "the preprint, at link revision 6bc19ea4 with the same two inputs of main "
            "swapped in: the same outcome. No register entry changes. Retain v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/default_drawings.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The #806 import (think-2lzo, think-meci): T-243's registration of Evan "
            "Daniel's certificate at 182, its coverage source, the importer's reader for "
            "its packet and #806's requests entry; the 25 October review mapped, T-243 at "
            "V3/C3; and its adoption at 182 in the pass of 25 October with its "
            "regularization (upper_bound_houses, adopt_houses, SETTLED[182] removed from "
            "default_drawings). Against main bb756e193 (#805): rendered at link revision "
            "f8cca02c into empty site directories, twice from this tree and once from it "
            "with main's result-requests.yaml, upper_bound_reports.py, results.yaml and "
            "source-coverage.yaml swapped in, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write all 51 "
            "files byte-identical across the three. After the review's mapping, the "
            "adoption and the merge of main 886dddce6 (#808), at link revision a8184fe4 "
            "with that main's seven candidate inputs swapped in, and after review A's "
            "fixes (T-243's headline and notes), at link revision b909d2b5 with the same "
            "seven inputs of main swapped in: the same outcome. The "
            "explainer, counting 242 to 243 results, takes v0.4.28 over main's v0.4.27. No "
            "PDF was printed for these three; each prints from that HTML. Retain v0.1.11, "
            "v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/contributors/people/hyukdong-kim.md",
            "packing/devtools/render_n11_lower_bounds_explainer_pdf.py",
            "packing/devtools/site_resources.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The import of #804 (think-9vai): T-244 at 172 and 263, its coverage entry, "
            "#804's requests entry and Hyukdong Kim's profile, against main bb756e193 "
            "(#805). Rendered at link revision 7af71882 into empty site directories, twice "
            "from this tree and once with main's results.yaml, result-requests.yaml and "
            "source-coverage.yaml swapped in and the new profile set aside, 69 files each, "
            "by render_n11_lower_bounds_explainer with its Chromium math pass, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods: these three papers' files are byte-identical across "
            "the three renders. Only the explainer differs, in its count of registered "
            "results. Measured again after merging main 886dddce6 (#808), with issue 804's "
            "card in site_resources, T-244's headline by surname and #799's "
            "acknowledgement recorded, at link revision 5e08f28c, with that main's four "
            "inputs swapped in, and after merging main 46e355582 (#814, T-243), at link "
            "revision dd5fc01d with that main's four inputs swapped in, and after #806's "
            "final comment, #814's News and the explainer PDF's page count of 25, at link "
            "revision 1b75d2f7 with that main's four inputs and "
            "render_n11_lower_bounds_explainer_pdf.py swapped in, and after review A's "
            "fixes, at link revision 6997281d, and review B's, at d5dcd2d0, each with the "
            "same five inputs of main swapped in: the same outcome each time, the "
            "explainer counting 244 results against main's 243, which its v0.4.29 "
            "carries. Retain v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/contributors/people/ctjlewis.md",
            "packing/contributors/people/evan-daniel.md",
            "packing/contributors/people/jatloe.md",
            "packing/contributors/people/manasseh-ahmed.md",
            "packing/devtools/check_results.py",
            "packing/devtools/site_resources.py",
            "packing/frontier/n-029.md",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The think-4l14 import of #810: T-245's registration of Jatloe's Lean proof "
            "that s(12) = 4 as reported, its coverage source, #810's requests entry, "
            "Jatloe's new profile and the n12 sources on Lewis's and Ahmed's, against main "
            "bb756e193 (#805): rendered at link revision bb756e19 into empty site "
            "directories, twice from this tree at 015f1a19 and once from it with main's "
            "result-requests.yaml, ctjlewis.md, manasseh-ahmed.md, results.yaml and "
            "source-coverage.yaml swapped in and jatloe.md removed, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write all 51 files byte-identical across the three. "
            "The explainer, counting 242 to 243 results, takes v0.4.28 over main's "
            "v0.4.27. No PDF was printed for these three; each prints from that HTML. "
            "Measured again after the merge of main 886dddce6 (#808), at link revision "
            "1307c2c8 with that main's five candidate inputs swapped in and jatloe.md "
            "removed: twice from this tree and once swapped, 51 files each, all "
            "byte-identical across the three. Measured a third time after the merge of "
            "T-246's registration of Daniel's s(29) minimal polynomial as the new kind exact "
            "side (results.yaml, check_results.py, evan-daniel.md, n-029.md, "
            "result-requests.yaml and source-coverage.yaml) and the overview's card for "
            "Jatloe12SquaresFormalized (site_resources.py), at link revision 9b8b004c "
            "against main 886dddce6, with that main's nine candidate inputs swapped in and "
            "jatloe.md removed: twice from this tree and once swapped, 51 files each, all "
            "byte-identical across the three. The explainer's v0.4.28 counts 244 results. "
            "Measured a fourth time after T-245's citation of its statement audit "
            "(results.yaml), at link revision bfacba5a against the same main, swapped the "
            "same way: 51 files each, all byte-identical across the three. "
            "Main 46e355582 (#814) then registered T-243 at 182 and took the explainer's "
            "v0.4.28, and #813 holds T-244, so the merge of that main renumbered this "
            "branch's two results, registered here as T-243 and T-244 until then, T-245 "
            "and T-246, and the explainer, counting 243 to 245 results, takes v0.4.29 over "
            "main's v0.4.28. Measured a fifth time after that merge, at link revision "
            "ab33e3bd against main 46e355582, with that main's result-requests.yaml, "
            "ctjlewis.md, evan-daniel.md, manasseh-ahmed.md, check_results.py, "
            "site_resources.py, n-029.md, results.yaml and source-coverage.yaml swapped in "
            "and jatloe.md removed: twice from this tree and once swapped, 51 files each, "
            "all byte-identical across the three. "
            "Measured a sixth time after the explainer's page count moved to 25 "
            "(render_n11_lower_bounds_explainer_pdf.py), at link revision bbc8c864: "
            "twice from this tree and once with main's copy of that module swapped in, "
            "51 files each, all byte-identical across the three. "
            "Main 01e2b5295 (#813) then registered T-244 at 172 and 263 and took the "
            "explainer's v0.4.29 and its page count of 25, so after the merge of that main "
            "the explainer, counting 244 to 246 results, takes v0.4.30 over main's v0.4.29, "
            "and the page-count module, main's own again, is no longer a candidate input. "
            "Measured a seventh time after that merge, at link revision 8a36268c against "
            "main 01e2b5295, with that main's result-requests.yaml, ctjlewis.md, "
            "evan-daniel.md, manasseh-ahmed.md, check_results.py, site_resources.py, "
            "n-029.md, results.yaml and source-coverage.yaml swapped in and jatloe.md "
            "removed: twice from this tree and once swapped, 51 files each, all "
            "byte-identical across the three. "
            "Measured an eighth time after the Resources page's Jatloe12SquaresFormalized "
            "card was shortened to keep its section medium (site_resources.py), at link "
            "revision d0d72d41, swapped the same way: 51 files each, all byte-identical "
            "across the three, and identical to the seventh measurement's but for the link "
            "revision. "
            "Retain v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=("paper:square-packing-methods-survey",),
        paths=("packing/campaign/result-requests.yaml",),
        outputs=(
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The stage 7 replies of 25 October to #810, #545 and #811 recorded under each "
            "issue's replies, naming T-245 and T-246 at V0/C0 and their evidence, against "
            "main 272b411b4 (#812). Rendered by render_packing_methods at link revision "
            "49b0b78e into empty site directories, twice from this tree and once with "
            "main's result-requests.yaml swapped in, 43 files each, all byte-identical "
            "across the three. No register entry changes. Retain v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/validate_schemas.py",
            "packing/frontier/README.md",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The exact-side register (think-vgsw, #811): the register joins the schema "
            "corpus (validate_schemas.py), its check joins the records tier (validate.py), "
            "and the frontier README gains a section on it, against main 272b411b4 (#812). "
            "Rendered at link revision 57f70c3e into empty site directories, twice from "
            "this tree and once with main's validate_schemas.py, validate.py and frontier "
            "README.md swapped in: render_n11_optimality_review, "
            "render_n11_threshold_bound_review, render_packing_methods and "
            "render_n11_lower_bounds_explainer, with its pinned Chromium math pass, write "
            "all 69 files byte-identical across the three. Measured again after merging "
            "main 0785626cc (#815), at link revision a2a5748e: twice from this tree and "
            "once with that main's three files swapped in, all 69 files byte-identical "
            "across the three, and identical to the first measurement apart from the link "
            "revision in source links. No PDF was printed; each prints from that HTML. "
            "Retain v0.4.30, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/campaign/result-requests.yaml",
            "packing/devtools/adopt_houses.py",
            "packing/devtools/select_houses.py",
            "packing/devtools/upper_bound_houses.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
            "packing/src/sqpack/cli/validate.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "H2 of think-hx0e (think-3anz): T-242 adopted at 268 in the pass of 26 October "
            "with its credit, Daniel after Lavrentev, and 268 taken off the staging list; "
            "T-240's and T-242's notes and next steps, the coverage note, the bound citation "
            "at 268, the composite record's witness and rigidity scope there and the "
            "screen's findings; #763's notebook-rows follow-up and the final comments of "
            "#797 and #798 recorded, against main bb756e193 (#805): rendered at link "
            "revision 96be67d5 into empty site directories, twice from this tree and once "
            "from it with main's nine candidate inputs swapped in, "
            "render_n11_lower_bounds_explainer with its math prepared by the host's Chrome "
            "for Testing headless shell through SQPACK_CHROMIUM, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write all 69 files byte-identical across the three. No "
            "result is registered, so the explainer's count is unchanged. No PDF was "
            "printed; each prints from that HTML. Measured again after review A's fixes "
            "(T-240's and T-242's notes on think-20oj's scope, the #763 packet's README), "
            "at link revision db18b3bc with the same nine candidate inputs of main "
            "bb756e193 swapped in: the same outcome. Measured again after merging main "
            "2f974835a (#818) and recording #798's comment of 25 October, at link "
            "revision 6273902f with that main's nine candidate inputs swapped in: all 69 "
            "files byte-identical across the three again. Retain v0.4.30, v0.1.11, v0.1.4 "
            "and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/devtools/github_references.py",
            "packing/devtools/render_changelog.py",
            "packing/devtools/result_overview.py",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "News and result pages link their GitHub issues (think-i8ks): "
            "`github_references` gains `reporting_issues`, `issues_reporting`, "
            "`issue_url` and `cited_issues`, and no existing function changes; "
            "`render_changelog` gains the `issues` check and backfill and renders an "
            "entry's issues beside its PRs in `_entry_lines`; `result_overview."
            "links_section` adds an Issues row. The papers reach `render_changelog` "
            "only through `site_documents`, which calls `entry_anchor`, unchanged, reach "
            "`github_references` only through `overview_sections`' "
            "`parse_github_reference`, unchanged, and no paper builder calls "
            "`links_section`, `result_popover_html` or the News renderers, which only the "
            "site's pages and result pages call. Measured at link revision f2341b95: the "
            "four papers rendered into empty site directories twice from this tree and "
            "once with main's three changed modules swapped in, 69 files each, all "
            "byte-identical across the three, and again after the opening-day rule was "
            "added to the three modules, byte-identical again. Every paper keeps its "
            "version: v0.4.30, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/atlas/known-best/bound-citations.json",
            "packing/atlas/known-best/composite-figure.json",
            "packing/campaign/result-requests.yaml",
            "packing/frontier/results.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The backlog lane of 25 and 26 October (think-vvjk, think-kf3o, think-sb7a, "
            "PR #821): T-237 to C3 by the exact audit of Friedman's s(5) "
            "(E-n005-friedman-theorem2-audit), with n = 5's lower bound citation and "
            "composite record naming it; T-046's next_rung, unfinished confirmations and "
            "notes on its census route; the #773 and #785 requests entries. No result is "
            "registered. Measured at link revisions 1fede43c and 1f2507d4 against main "
            "2f974835a (#818), and at 9ed88d49 after the bound citation and composite "
            "record were regenerated; then, after merging main 5c50803d6 (#807), at link "
            "revision 70434a43 into empty site directories, twice from this tree and once "
            "with that main's bound-citations.json, composite-figure.json, "
            "result-requests.yaml and results.yaml swapped in, by "
            "render_n11_lower_bounds_explainer, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods: 69 files each, "
            "all byte-identical across the three every time. Measured again after merging "
            "main 85a1919da (#820), at link revision e29cf5f4 with that main's same four "
            "files swapped in: 69 files each, all byte-identical across the three. No PDF "
            "was printed. Retain v0.4.30, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-lower-bounds-explainer",
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/devtools/site_resources.py",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-lower-bounds-explainer.html",
            "papers/n11-lower-bounds-explainer.md",
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The intake records of 26 October (think-p7cq): #819's beyond-horizon row at "
            "344 and its source amundsk-issue819-2026-10-25, superseding the 964ee2b row "
            "there (source-coverage.yaml), the gist's card among the other projects "
            "(site_resources.py), and the requests entries of #819, #799, #565, #804 and "
            "#773 (result-requests.yaml); no register entry. Against main 85a1919da "
            "(#820): rendered at link revision b51aaf17 into empty site directories, twice "
            "from this tree and once with that main's three files swapped in, "
            "render_n11_lower_bounds_explainer, with its pinned Chromium math pass, "
            "render_n11_optimality_review, render_n11_threshold_bound_review and "
            "render_packing_methods write all 69 files byte-identical across the three. "
            "No PDF was printed; each prints from that HTML. Every paper keeps its "
            "version: v0.4.30, v0.1.11, v0.1.4 and v0.2.7."
        ),
    ),
    ReleaseNoPublicChange(
        components=(
            "paper:n11-optimality-review",
            "paper:n11-threshold-bound-review",
            "paper:square-packing-methods-survey",
        ),
        paths=(
            "packing/campaign/result-requests.yaml",
            "packing/contributors/people/chris-deotte.md",
            "packing/devtools/site_urls.py",
            "packing/devtools/upper_bound_reports.py",
            "packing/frontier/results.yaml",
            "packing/frontier/source-coverage.yaml",
        ),
        outputs=(
            "papers/n11-optimality-review.html",
            "papers/n11-optimality-review.md",
            "papers/n11-threshold-bound-review.html",
            "papers/n11-threshold-bound-review.md",
            "papers/square-packing-methods-survey.html",
            "papers/square-packing-methods-survey.md",
        ),
        reason=(
            "The imports of 26 October (w-imports-1026): T-247, Evan Daniel's packing at "
            "299 (#824), and T-248 to T-250, three reported Lean formalizations (#535, "
            "#537, #643), with their evidence, coverage and requests entries, the "
            "importer's optional short credit, Chris Deotte's contributor profile and "
            "the results page's byte ceiling raised to 1,500,000 for 250 results. "
            "Against main 9ebde24df (#823): rendered at link revision 24bb2581 into empty "
            "site directories, from this tree and with that main's five files swapped in "
            "and the profile removed, render_n11_optimality_review, "
            "render_n11_threshold_bound_review and render_packing_methods write their 67 "
            "files byte-identical across the two, measured again after the ceiling and "
            "the T-249 and T-250 claim edits. The explainer's two files differ in "
            "the registered result count, 250 against 246, so it takes v0.4.31. No PDF of "
            "these three was printed; each prints from that HTML. They keep v0.1.11, "
            "v0.1.4 and v0.2.7."
        ),
    ),
)


def component_history(component: str) -> tuple[PublicationHistoryEntry, ...]:
    """Retained editions for one component, including historical changelog references."""
    try:
        name = COMPONENT_HISTORY_NAMES[component]
    except KeyError as error:
        raise ValueError(f"unknown release component {component!r}") from error
    return globals()[name]


def component_version(component: str) -> str:
    """The current semantic core, without a draft label or a derivation suffix."""
    return component_history(component)[0].version


def parsed_version(version: str) -> tuple[int, int, int]:
    """A canonical public semantic-version core, with no status or data suffix."""
    match = re.fullmatch(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", version)
    if match is None:
        raise ValueError(f"{version!r} is not a version: vMAJOR.MINOR.PATCH")
    major, minor, patch = (int(part) for part in match.groups())
    return major, minor, patch


def successor_version(version: str, impact: ReleaseImpact) -> str:
    """One patch or minor successor for the complete component batch."""
    major, minor, patch = parsed_version(version)
    if impact == "patch":
        return f"v{major}.{minor}.{patch + 1}"
    if impact == "minor":
        return f"v{major}.{minor + 1}.0"
    raise ValueError(f"unknown release impact {impact!r}; choose patch or minor")


def published_infographic_version(repo: Path) -> str:
    """Read the authoritative main edition without executing prior release source.

    A working-tree successor stays a candidate through review, including redraws.
    Main retains the published baseline; pre-policy main used the site history.
    """
    result = subprocess.run(
        ["git", "-C", str(repo), "show", "origin/main:packing/src/sqpack/release.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(
            "an infographic redraw requires the local origin/main publication baseline"
        )
    fields = {
        target.id: node.value
        for node in ast.parse(result.stdout).body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    history = fields.get("INFOGRAPHIC_HISTORY", fields.get("PUBLICATION_HISTORY"))
    if isinstance(history, (ast.Tuple, ast.List)) and history.elts:
        first = history.elts[0]
        if isinstance(first, ast.Call):
            for keyword in first.keywords:
                if keyword.arg == "version" and isinstance(keyword.value, ast.Constant):
                    version = keyword.value.value
                    if isinstance(version, str):
                        parsed_version(version)
                        return version
    raise ValueError("main has no literal published infographic history head")


def validate_release_impacts(
    decisions: Sequence[ReleaseImpactDecision] | None = None,
    *,
    externally_changed: Iterable[str] = (),
    previous_versions: Mapping[str, str] | None = None,
) -> None:
    """Hold cuts to their owning history and require each delivered change's decision.

    The default checks the retained policy-era cuts. A release closeout additionally
    passes components whose public content changed; each must have a decision for its
    current edition. Callers determine that set from rendered changes, not file count,
    provenance changes, significance scores or evidence grades.
    """
    selected = RELEASE_IMPACTS if decisions is None else decisions
    indexed: dict[tuple[str, str], ReleaseImpactDecision] = {}
    for decision in selected:
        history = component_history(decision.component)
        versions = [entry.version for entry in history]
        key = (decision.component, decision.version)
        if key in indexed:
            raise ValueError(f"duplicate release-impact decision for {key}")
        if decision.version not in versions or decision.previous_version not in versions:
            raise ValueError(f"release-impact decision {key} names an unretained edition")
        index = versions.index(decision.version)
        if index + 1 >= len(versions) or versions[index + 1] != decision.previous_version:
            raise ValueError(
                f"release-impact decision {key} does not follow its owning history"
            )
        expected = successor_version(decision.previous_version, decision.impact)
        if decision.version != expected:
            raise ValueError(f"{key} requires its {decision.impact} successor {expected}")
        if not re.search(r"\w", decision.reason) or decision.reason.strip() != decision.reason:
            raise ValueError(f"release-impact decision {key} needs a trimmed reason")
        indexed[key] = decision
    for component, baseline in RELEASE_POLICY_BASELINES.items():
        versions = [entry.version for entry in component_history(component)]
        if baseline not in versions:
            raise ValueError(f"{component} has lost its retained policy baseline {baseline}")
        for version in versions[: versions.index(baseline)]:
            if (component, version) not in indexed:
                raise ValueError(f"{component} {version} needs a release-impact decision")
    for component in externally_changed:
        version = component_version(component)
        key = (component, version)
        if key not in indexed:
            raise ValueError(
                f"externally changed {component} needs an impact decision and successor"
            )
        if previous_versions is not None:
            if component not in previous_versions:
                raise ValueError(f"externally changed {component} has no previous edition")
            previous = previous_versions[component]
            if version == previous or indexed[key].previous_version != previous:
                raise ValueError(
                    f"externally changed {component} needs a successor to {previous}"
                )


#: The commit the committed claim documents link to
#: (`render_n11_lower_bounds_explainer.edition_file`), at this repository's short length. It is
#: pinned for the reason `DATA_REVISION` is: those documents are compared byte for byte with a
#: fresh render, so a link naming the build commit would fail their drift check forever. It is
#: in no version string. It moved when the claim documents were regenerated for a site
#: edition, and is FROZEN since site editions were retired on 22 October 2026 (think-wdqo):
#: `devtools.check_release_impact` refuses an edit to it. It must be a commit on `main`; the
#: site's own links name `main` itself (`devtools.repo_links`).
PUBLICATION_REVISION = "7ff5b129"


def data_pathspec() -> tuple[str, ...]:
    """`DATA_PATHS` less `DATA_EXCLUDED`, as the arguments git takes after `--`."""
    return (*DATA_PATHS, *(f":(exclude){path}" for path in DATA_EXCLUDED))


def _shallow_boundary(repo: Path) -> frozenset[str]:
    """The commits a shallow clone's history is cut at; none in a complete clone."""
    found = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--git-path", "shallow"],
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0:
        return frozenset()
    shallow = Path(found.stdout.strip())
    shallow = shallow if shallow.is_absolute() else repo / shallow
    return frozenset(shallow.read_text().split()) if shallow.is_file() else frozenset()


def data_revision(repo: Path) -> str:
    """The full hash of the last commit in `repo` that changed the data, as git says.

    Raises where git cannot say: outside a repository, and in a shallow clone whose cut
    falls before the answer. git reports the commit a shallow history is cut at as
    changing every path, since it cannot see that commit's parent, so the boundary is
    refused rather than returned: a version stamped from it would name the wrong data.
    """
    found = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--format=%H", "--", *data_pathspec()],
        capture_output=True,
        text=True,
        check=False,
    )
    revision = found.stdout.strip()
    if found.returncode != 0 or not revision:
        raise RuntimeError(
            f"git cannot name the last data commit in {repo}: "
            f"{found.stderr.strip() or 'no commit touches ' + ', '.join(DATA_PATHS)}"
        )
    if revision in _shallow_boundary(repo):
        raise RuntimeError(
            f"git cannot name the last data commit in {repo}: its shallow history is cut "
            f"at {revision[:12]}, so whether that commit changed the data cannot be seen"
        )
    return revision


def commit_date(repo: Path, revision: str) -> str:
    """The ISO date of the commit `revision` in `repo`: its author date, on the author's
    own calendar, which is the day a reader would say the change was made.

    The commit records its own offset, so the answer is the same on every machine. Raises
    where git cannot say: outside a repository, or for a commit this clone does not have.
    """
    found = subprocess.run(
        ["git", "-C", str(repo), "show", "-s", "--format=%as", f"{revision}^{{commit}}"],
        capture_output=True,
        text=True,
        check=False,
    )
    day = found.stdout.strip()
    if found.returncode != 0 or not day:
        raise RuntimeError(
            f"git cannot date {revision[:12]} in {repo}: "
            f"{found.stderr.strip() or 'no such commit'}"
        )
    return day


def last_change_date(repo: Path, *paths: str) -> str:
    """The ISO date of the last change to any of `paths`: the latest author date among
    the commits that changed one, merges excluded.

    A merge is excluded because it is not when anyone wrote the text, and the latest date
    is taken, not the first commit `git log` lists, because two branches merged out of
    order list the earlier change first. Raises where git cannot say, and in a shallow
    clone, where a change below the cut cannot be seen.
    """
    found = subprocess.run(
        ["git", "-C", str(repo), "log", "--no-merges", "--format=%H %as", "--", *paths],
        capture_output=True,
        text=True,
        check=False,
    )
    changes = [line.split() for line in found.stdout.splitlines() if line.strip()]
    if found.returncode != 0 or not changes:
        raise RuntimeError(
            f"git cannot date the last change to {', '.join(paths)} in {repo}: "
            f"{found.stderr.strip() or 'no commit changes it'}"
        )
    if _shallow_boundary(repo):
        raise RuntimeError(
            f"git cannot date the last change to {', '.join(paths)} in {repo}: its "
            "history is shallow, so a later change may lie below the cut"
        )
    return max(day for _commit, day in changes)


def data_version(repo: Path) -> str:
    """The shared version as git says it is now, which the pinned one must equal.

    Artifacts print `PUBLICATION_EDITION` rather than this, so that a render needs no
    history; this is what the drift check holds that pin to.
    """
    return f"{PUBLICATION_VERSION}-{data_revision(repo)[:DATA_REVISION_LENGTH]}"
