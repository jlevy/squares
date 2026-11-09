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
DATA_REVISION = "1566b839004443173d4cac0c4e8c9c0a8b66533f"

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
        version="v0.4.35",
        first_published="October 31, 2026",
        result_scope=(
            "Update the registered result count after the registration of one result "
            "from the intake of 31 October (T-261)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.34",
        first_published="October 31, 2026",
        result_scope=(
            "Update the registered result count after the registration of eight "
            "upper-bound results from the intake of 31 October (T-253 to T-260)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.33",
        first_published="October 31, 2026",
        result_scope=(
            "Update the registered result count after the registration of Mohsen Khalili "
            "and Sara Gharabaghi's s(44) = 7 (T-252)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.32",
        first_published="October 26, 2026",
        result_scope=(
            "Update the registered result count after the registration of Evan Daniel's "
            "packing at 299 (T-248) and three reported Lean formalizations (T-249 to "
            "T-251)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.31",
        first_published="October 26, 2026",
        result_scope=(
            "Update the registered result count after the registration of Hyukdong Kim's "
            "exact side at 297 (T-247)."
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
        previous_version="v0.4.34",
        version="v0.4.35",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of one result "
            "from the intake of 31 October (T-261)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.33",
        version="v0.4.34",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of eight "
            "upper-bound results from the intake of 31 October (T-253 to T-260)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.32",
        version="v0.4.33",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Mohsen Khalili "
            "and Sara Gharabaghi's s(44) = 7 (T-252)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.31",
        version="v0.4.32",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Evan Daniel's "
            "packing at 299 (T-248) and three reported Lean formalizations (T-249 to "
            "T-251)."
        ),
    ),
    ReleaseImpactDecision(
        component="paper:n11-lower-bounds-explainer",
        previous_version="v0.4.30",
        version="v0.4.31",
        impact="patch",
        reason=(
            "Update the registered result count after the registration of Hyukdong Kim's "
            "exact side at 297 (T-247)."
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
    """A reviewed, path-scoped finding that named component outputs did not change.

    Each is its own YAML file in `packing/release-records/no-public-change/`, which
    `devtools.release_records` reads, and never an entry in a tuple here: one shared tuple
    made every two open records pull requests conflict at each merge (think-nrp6).
    """

    components: tuple[str, ...]
    paths: tuple[str, ...]
    outputs: tuple[str, ...]
    reason: str


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
