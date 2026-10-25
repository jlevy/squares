# Feature: Beyond-Horizon Rows Above n = 1024

**Date:** 2026-10-24 (last updated 2026-10-24)

**Author:** Claude (lane c-plan-1024-llit), for the intake coordinator coord-intake-1024
(bead think-llit)

**Status:** Draft

## Overview

The record keeps upper bounds beyond the n ≤ 324 corpus as dated beyond-horizon rows,
decided in report order, but only up to n = 1024. Every tool that writes or checks such
a row stops at 1024. Göbel’s construction stops at 1073, and every reading from 23
October takes it as the baseline beyond 324. On 23 October the owner decided to track
every count above 1024, with no ceiling (D1 on think-f2io). This plan lifts the ceiling
in one code slice, then records the rows in three records slices, in report order and
within the owner’s compute cap.
A fourth slice records the rows that wait on the questions still open.

The plan records nothing and changes no code.
Every price is in CPU-hours.

## Goals

- One report-order walk over every count above 1024 that any report reaches, under the
  owner’s answers of 23 October, with Göbel’s construction at every count.
- Every row that walk records written to the coverage register, each replayed on both
  maintained routes or decided exactly from its recipe, within N2’s cap.
- #732’s certificates above 1024 kept as hosted data (N3), and Couzo’s as the record’s
  D4 disposition recommends, each read through its manifest.
- The gate steps that grow with rows held to stated budgets, and every tier within its
  ceiling, with every row above 1024 in the record.
- The rule text in the frontier README and the runbook updated to match.

## Non-Goals

- **Rows to 1024.** Their walks are frozen and stay as written.
  #763’s and 43f666c’s rows to 1024 belong to think-ptkk (PR #789) and think-gn29.
- **Register entries.** A row beyond the corpus is not a register result, and nothing
  here takes a `T-NNN`.
- **A site table of the rows** (N5, below).
- **Göbel’s family formulas.** The catalogue states them, and the record trusts that
  statement up to 1073 today, as it will above.
  This plan computes the families further; it does not prove them again.
- **Friedman’s off-centre family as a baseline** (think-zkxy), and per-row credit (D5)
  beyond what the rows themselves need.
- **Writing recipes out as certificates.** The triage priced that at about 98 CPU-hours.
  A maintained checker decides the same recipes in seconds.

## Background

### What the Owner Decided

| Question | The owner’s answer, as the beads record it | Bead |
| --- | --- | --- |
| D1: track counts above 1024 | Yes, no ceiling; rows recorded as reported, as below 1024 | think-f2io |
| D2: recipe rows with no certificate file | Yes, “decided exactly from the recipe by a checker this project maintains”; the rule goes into the frontier README | think-f2io |
| D6: deletion bounds | Selected the option labelled “Yes, an earlier report (Recommended)”; whether such a bound gets a row of its own is still open | think-f2io, think-kzme |
| #613: Göbel as the baseline | Yes: “a rational row above Goebel’s exact side is not recorded” | think-8krd |
| Restatements below the print | “sub-print re-certifications are RESTATEMENTS, not new rows” | think-fwa9 |
| N2: compute for #732 | Under the 40 CPU-hour cap: all positives on both routes, plus six controls on a stratified 10% of #732’s files, about 36 CPU-hours with the rest | think-llit |
| N3: hosting | Nine `tar.xz` shards of about 128 MB that the owner publishes as hosted data; agents stage the manifest only | think-llit |

D4, hosting #715’s certificates above 1024, has no answer from the owner.
think-f2io recommended “a hosted-data manifest staged in the stage 2 PR; the owner
publishes data/couzo-715-certificates-v1”, and coord-intake-1023 recorded that “D4
follows as recommended (a hosted-data manifest, not Git blobs; OR-18) unless the owner
says otherwise”. That is the coordinator’s disposition, not the owner’s word, and this
plan follows it ([Hosted Custody](#hosted-custody-n3-d4-or-18)).

Still open: D3, D5, think-kzme’s sub-question on D6, N1, N4, N5 and N6.
[Open Questions](#open-questions) sorts them into those a stated rule or the record
already decides and those only the owner can answer.

### The Reports Above 1024

The stage 1 triage of 23 October (c-triage-1024-1023) counted these.
Its scratch files were lost with the interrupted session’s container, so the figures
here are the ones its bead notes kept, together with the later triages of #763
(think-cnn7) and 43f666c (think-cncq).
The walk in R1 derives every count again from the sources.

| Report | Reported | Above 1024 | Kind | Custody |
| --- | --- | --- | --- | --- |
| Kingbird catalogue, the capture of 2026-08-22 | before 22 August | 1453, 1765, 1850, 2043 | sides with minimal polynomials | retained page |
| Kevin Fang, `bef5c42` | 2026-10-12T19:13:41Z | 62 | certificates and composites | 4 MB, Git |
| Evan Daniel, `49907ec` | watched commit | 1092, 1228 (think-jtlq) | tilings | under 0.2 MB, Git |
| Robert Barnett, `d2356fa` | watched commit | 2043, below every other report | certificate | under 0.2 MB, Git |
| #666, Joost de Winter | issue | 8, at 1061 to 1568 | certificates | retained in its packet |
| #715, Francisco Couzo | 2026-10-21T20:55:57Z | 1,112 claims: about 129 files, 825 recipes, 158 deletions |  | hosted (D4): `data/couzo-715-certificates-v1` |
| Couzo’s index at `5a299b4` | push 2026-10-21T22:56:37Z | 5,078 counts: 95 certificates, 187 deletions, 4,796 tiling and L-border recipes | index and files | its files in the same release |
| #719, Mykhailo Polkovskyi | 2026-10-22 | 8, at 1061 to 1568 (think-9vr8) | derived facts | 0.06 MB, Git |
| #732, Polkovskyi | 2026-10-22T19:55:03Z | 5,078 files at 1025 to 9913, 5.21 GB | certificates | hosted: about 128 MB as nine shards |
| #763, Couzo | 2026-10-23T23:35:51Z | 233: 6 certificates, 1 deletion (1646), 226 recipes (1727 is a recipe plus a deletion); of `964ee2b`’s 908 unrequested rows, 6 are below every earlier report |  | in PR #789’s packet |
| `43f666c`, Couzo, with no issue | push 2026-10-24T06:10:44Z | 831 L-border recipes on 14 certificates |  | think-gn29’s packet |

Under D1 alone, the triage counted 4,489 rows at 4,345 counts, 4,319 of them #732’s. It
held 5,430 more: 4,787 recipes (D2), 172 deletions (D6), 467 publications above Göbel’s
construction, and 4 rows that depend on the Kingbird catalogue (N1). Since then D2 has
been answered yes, so the recipes become rows through the checker.
The Göbel answer was yes, so the 467 are not recorded.
#763 and `43f666c` arrived later and supersede many of #732’s rows.

#715’s own count differs between two reads.
On 22 October think-cyal found its 1,112 rows resting on 98 certificates (85 at their
own counts, 51.2 MB checkout, 9.1 MB as zlib stores them), with 171 deletions and 856
L-border constructions, 621 of those with a deletion.
The triage of 23 October gave about 129 files, 825 recipes and 158 deletions, and about
13 MB for Couzo’s files above 1024. R1’s walk settles the count.

### What Stops at 1024 Today

- **The ceiling.** `beyond_horizon_replay.LIMIT = 1024`
  (`packing/devtools/beyond_horizon_replay.py:233`) and `couzo_715_replay.LIMIT = 1024`
  (`packing/devtools/couzo_715_replay.py:113`). Every row above 1024 is “retained and
  not decided” (`held_claims`, `beyond_horizon_replay.py:1482`).
- **Göbel’s reach.** The retained program
  (`packing/resources/web/couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py`)
  builds its families only up to `LIMIT = 1100` (`goebel_beyond_horizon.py:57`). Its
  largest member is at 1073 (`intake_ledger.goebel_reach`,
  `packing/devtools/intake_ledger.py:1782`). Review B of #754 found that one count above
  1073 refuses a whole input, not just that count.
  An import is refused through `upper_bound_reports.compare`
  (`packing/devtools/upper_bound_reports.py:1767`), which builds every row before it
  writes and raises through `goebel_construction` (`upper_bound_reports.py:1621`). An
  earlier-publications receipt is refused through `standing_sides`
  (`beyond_horizon_replay.py:2106`). A gather is refused through
  `intake_ledger.tree_members` (`intake_ledger.py:1364`, with Göbel’s member at
  `intake_ledger.py:1418`).
- **No recipe checker.** A recipe is the `RECIPE` hold class
  (`beyond_horizon_replay.py:281`–`:293`): recorded in the walk, but with no row.
- **No hosted reader.** `certificate()` (`beyond_horizon_replay.py:1504`) reads a
  retained file or a derived fact, never a hosted object.
- **The check’s cost.** [Gate Cost](#gate-cost) measures it below.

## Design

### Approach

The work has two phases.
Phase 1 is one code slice (W7). It records nothing and changes no existing release’s
window, receipt, walk or row.
Phase 2 records the rows in report order, and each records slice lifts the windows of
the releases it records, in the same pull request as their receipts.

**Order.** #789 (think-ptkk, #763’s import to 1024) rewrites the same module: it adds a
fifth frozen walk, two releases and a `LIMIT` site.
It goes first, as think-cnn7’s plan implies, and W7 starts from the `main` that holds
it. W7 can land as one pull request or, under the `github-stacked-prs` grant, as a stack
of three, each layer with its own negative controls: `goebel_construction` and the reach
tests; `construction_checker`; then the ceiling, the hosted reader, the gate changes and
the rule text.

One walk decides every count above 1024, from all the reports to date.
It is gathered once, in R1, at
`packing/campaign/issue-intake/upper-bounds-above-1024-YYYYMMDD/`, read on the day R1
starts and with its starts frozen at that `main`. Each start holds the grid and Göbel’s
construction. Each later slice writes the rows that walk records for its own sources.
Where a report the walk records has not yet had its import written, the chain passes
over it until its rows land (`Awaiting`), as the history walk did below 1024. A report
published after the walk’s reading gets a walk of its own, as below 1024.

### The Ceiling: `LIMIT` and Every Use of It

Some uses of `LIMIT` describe walks and releases that are frozen at 1024; those keep the
value under a name that says so (`FROZEN_THROUGH`). The other uses act as a ceiling, and
W7 makes them read a release’s window or a walk’s counts instead.
W7 sets no window above 1024: every frozen walk and release on `main` when W7 starts
keeps its window. That is four walks and 18 releases at b2ea7b09c, and five walks and 20
releases once #789 merges.
Line numbers refer to `main` at b2ea7b09c, where these files are unchanged at 830dfb470,
and #789’s to its head at 3773d6025.

**`packing/devtools/beyond_horizon_replay.py`:**

| Site | Today | After W7 |
| --- | --- | --- |
| `:233` `LIMIT = 1024` | the module’s ceiling | `FROZEN_THROUGH`: the reach of the walks frozen at 1024; no longer a ceiling |
| `:428` `HISTORY_COUNTS` | the history walk’s counts | unchanged: a frozen walk |
| `:799`–`:818` `_rulings` (`"through": LIMIT`), `:824` `WALK_RULINGS` | both rulings through 1024 for every frozen walk | unchanged for those walks. The walk above 1024 lists both rulings with no `through` (`intake_ledger.NO_LIMIT`, `intake_ledger.py:1750`), so they reach its top count, as `answer_problems` (`intake_ledger.py:728`) requires |
| `:1472` `decided_claims`, `:1482` `held_claims` | a release decides its rows to 1024; rows above wait | a decided window per release: `Release.decided_above`, defaulting to the horizon, and `Release.decided_through`, defaulting to `FROZEN_THROUGH`. W7 changes no release’s window. R1 lifts #666’s, #719’s, `bef5c42`’s and `5a299b4`’s (`couzo-reconcile-2026-10-20`) and adds the #715 release; R2 lifts #732’s; R3 lifts #763’s and `964ee2b`’s |
| `:1841`–`:1850` `goebel` | requires `program.LIMIT >= LIMIT` | a frozen window keeps the retained program, so its receipt and `program` field stay as written; a window above 1024 reads the maintained module, requires its proved reach to cover the window, and writes `beyond-horizon-goebel-comparison-v2`, naming the module |
| `:1916` `"limit": LIMIT` in the claims record | 1024 | the release’s window |
| `:2106` `standing_sides` | refuses above 1073 (through `reports.goebel_construction`) | refuses only above the proved reach |
| `:2152` `release_sides` | reads rows above `LIMIT` from a clone | reads rows above the window from the packet or the hosted shard |
| `:2378` `ledger_sources` (`:2439`), `:2525` `release_715_claims` (`:2551`) | transcribe the #719 walk’s `sources.yaml` | unchanged: bound to that frozen walk, which `tests/test_beyond_horizon_replay.py:628`–`:650` holds |
| `:3086` `source_history` (`:3093`, `:3194`) | paths in `HISTORY_COUNTS` only | takes the walk’s counts; above 1024 it reads headers from the shards, and first commits from a blobless clone |
| `:3256` `release_walk_sources` (`:3291`, `:3311`, `:3320`) | claims to 1024 | the walk’s counts |
| `:3475` `later_commits` (`:3500`, `:3540`, `:3570`, `:3645`) | publications to 1024 | the walk’s counts; f1ceee4’s receipt keeps its `"limit": 1024` |
| `:4189` `walk_of` | one walk per release | takes the count: rows to 1024 stay with the release’s own walk, rows above with the walk above 1024 |
| `:4581` `chain_problems` (`:4600`) | skips counts above 1024 | every count a walk plans rows for, each walk to its own reach |
| `:4709` `construction_problems` (`:4723`) | rows from 325 to 1024 against `goebel_form` | every row beyond 324, with Göbel’s form from the maintained module |
| docstrings `:8`, `:88`, `:821`, `:904`, `:931`, `:2112`, `:2154`, `:2385`, `:2529`, `:4587`, `:4710` |  | rewritten with the code |

**#789’s additions to the same module** (its head, 3773d6025):

| Site | Today, on #789 | After W7 |
| --- | --- | --- |
| `:484` `ISSUE_763`, `:923` `ISSUE_763: _rulings()` | a fifth walk, #763’s claims to 1024, with both rulings through 1024 | unchanged: a frozen walk, but for its `RECIPE` hold, which think-gn29 drops for think-g2qy (see “The hold”) |
| `:1539`–`:1592`, `RELEASES` (from `:1374`) | 20 releases, adding #763 and `964ee2b`’s unrequested rows, each decided to 1024 | windows kept; R3 lifts both |
| `:4211` `claim_map_walk_sources` (`:4237`, docstring `:4215`, `:4230`) | `mapped_claims(item)` read only where `n <= LIMIT` | the walk’s counts, so the walk above 1024 reads #763’s mapped claims above 1024 |
| comments `:1541`, `:1563` |  | rewritten with the code |

**`packing/devtools/couzo_715_replay.py`:**

| Site | Today | After W7 |
| --- | --- | --- |
| `:113` `LIMIT = 1024`, `:114` `DECIDED = 173`, `:191` `decided_claims` | the decision of 21 October on #715, to 1024 | unchanged: its receipts are #715’s record to 1024 |
| `:151`, `:613`–`:623` `goebel` | the retained program, `program.LIMIT >= LIMIT` | unchanged: a frozen receipt, every count within the retained program’s reach, its `program` field naming the retained file (`couzo_715_replay.py:628`) |
| #715’s 1,112 claims above 1024 | not decided | added by R1, not W7: a `Release` for issue 715 in `beyond_horizon_replay` with `decided_above = 1024` and no `decided_through`, and its own `source_id`, `record` and `receipts` in the #715 packet (`Release` fields at `beyond_horizon_replay.py:954`–`:956`). `couzo_715_replay` owns the existing source’s claims record, and a coverage source declares one record. The precedents are Couzo’s `23aff0c` beside #670, and #789’s `964ee2b` beside #763 |

**Who reads which Göbel source.** `GOEBEL_PROGRAM` keeps naming the retained file
(`intake_ledger.py:200`). Every frozen receipt keeps its computation and its `program`
field: `couzo_678_replay.py:122` and `:925`, `couzo_715_replay.py:613`–`:628`, and
`beyond_horizon_replay.py:1841`–`:1861` for a frozen window.
The readers that must reach past 1073 move to the module:
`intake_ledger.py:1772`–`:1803` (`_goebel`, `goebel_reach`, `goebel_form`), and through
them `construction_side`, `tree_members`, `upper_bound_reports.goebel_construction`,
`standing_sides` and `construction_problems`. `check` reads only a receipt’s
`comparison` (`beyond_horizon_replay.py:4935`, `couzo_715_replay.py:807`), and the
agreement test holds both sources to the same sides from 325 to 1073. The tests that pin
the old reach change with them: `tests/test_intake_ledger.py:407`
(`goebel_reach() == 1073`) and `tests/test_beyond_horizon_replay.py:599`, `:640` and
`:1205`.

### Göbel’s Construction Beyond 1073

**Recommendation: extend the reach, in a maintained module that the retained program
re-verifies. Do not split the inputs at 1073.**

Splitting at 1073 would leave every count from 1074 to 9913 refused.
Of the 5,078 counts #732 reports above 1024, at most 49 lie between 1025 and 1073, so
the split would refuse more than 99% of them, and almost all of #715’s, #763’s and
`43f666c`’s. It would defer D1’s “no ceiling” rather than apply it.
It would also leave the 467 publications above Göbel’s construction undecided, against
the #613 answer.

Raising `LIMIT` in the retained program is unsafe.
Its loops stop at `a < 40` and `b < 80` (`goebel_beyond_horizon.py:106`–`:107`), so no
strip is built above 1617. At 1,573 counts between 1682 and 6116, where a strip with
`a ≥ 40` is least, the program would then give a side that is too large; above 6256 it
gives no side at all.
A row above Göbel’s true construction but below that side would be recorded.

This plan’s sample checks both claims, using a scratch script that reads the retained
program unchanged; W7 makes the sample a test (`OR-1`):

| Build | Members | Largest member | Against the retained program, 325 to 1073 | Final by the area bound |
| --- | ---: | --- | --- | --- |
| The retained program, `LIMIT = 1100` | 104 | 1073 | itself | — |
| The same loops, `LIMIT` raised to 10,500 | 186 | 6256; no strip above 1617 | — | wrong, too large, at 1,573 counts from 1682 to 6116 |
| Loop bounds derived from the limit, to 10,500 | 343 | 10,488 | 0 disagreements | every count from 325 to 10,000; the first it cannot prove is 10,346 |

The table to 10,000 takes 0.01 CPU-seconds in one descending pass.
Review A of #791 recomputed every figure here independently, in exact ℤ[√2].

**The module.** W7 adds `packing/devtools/goebel_construction.py`:

- It builds the three families the Kingbird catalogue states, with the `a` and `b`
  bounds derived from the build limit instead of fixed.
- It computes Göbel’s side at every count up to the limit in one descending pass (the
  least member at that count or above, by deletion), and caches it.
- **It proves each side final.** A member at count k packs k unit squares, so its side
  is at least √k. A least side S at count m is therefore final once every member up to
  ⌊S²⌋ is built. The test is exact: `p² + 2q² + 2pq√2 < B + 1` for `S = p + q√2` and
  build limit B.
- It derives the build limit from the largest count asked for, so there is no fixed
  reach. A count whose side the module cannot prove final is refused, as counts above
  1073 are today.
- The retained program stays unchanged, as the 15 October record, the regression oracle
  and the source of every frozen receipt (above).

**What the extended build already shows.** W7 derives these again from the module:

- **Daniel’s 1092 and 1228 are above Göbel’s construction**, so under think-8krd’s
  answer neither is recorded.
  At 1092 the side is 0.133 above the Göbel strip of 1102 less 10 squares, 33 + √2/2. At
  1228 it is 0.170 above the Göbel square of 1237 less 9, 18 + 25√2/2. The history walk
  already decided his 964 the same way (16 + 11√2). think-jtlq then closes with the
  walk’s verdicts and no rows.
- **The Kingbird catalogue’s four sides are below the construction:** 1453 by 0.079,
  1765 by 0.018, 1850 by 0.218 and 2043 by 0.011. The catalogue’s own text agrees with
  the forms the build picks.
  It says 1765 “Beats the s(1765) Göbel square” (22 + 29√2/2) and 2043 “Beats the
  s(2043) Göbel strip” (45 + √2/2).

### Recipe Rows: the Construction Checker (D2)

A recipe in Couzo’s indexes names a parent certificate (`source_n` and its path and
digest), `tiles_per_side` t, `layers` L and `deleted_squares`. The #715 receipt’s
`source_index` shows the form; at 365, for example, the parent is 328, with `t = 1` and
`L = 1`, and `328 + 19 + 18 = 365`.

**The lemma.** Let P be a packing of n₀ unit squares in the square `[0, S]²`.

- **Tiling:** t² translated copies of P pack `t²·n₀` squares in `[0, tS]²`.
- **One L-border:** around a container of side W, the layer adds `⌊W + 1⌋` unit squares
  along one side and `⌊W⌋` along the other, all inside `[0, W + 1]²` and outside
  `[0, W]²`. The layer’s capacity is `2⌊W⌋ + 1`.
- **The whole recipe** packs every count up to `t²·n₀ + Σ (2⌊tS + j⌋ + 1)`, the sum
  taken over `j = 0, …, L − 1`, at side `tS + L`. Deleting squares from a packing leaves
  a packing.

**The checker,** `packing/devtools/construction_checker.py`, decides a recipe exactly in
`Fraction`s. It holds the parent to the index’s path and SHA-256 and requires the parent
to have passed both routes with its controls refused.
It requires the stated bound to equal `tS + L` and the count to be the capacity less the
stated deletions. It refuses any recipe kind it does not read.
It refuses a parent that is a classical construction rather than a certificate the
record replays; Friedman’s waits on think-zkxy.
It refuses every Fang composite, naming unstated parts where his table states none; a
rule for one whose parts are stated waits on think-tj3x. Each release writes
`receipts/recipe-decisions.json`: the count, recipe, parent, capacity, side and verdict.
`check` derives it again.

**Parents that are not rows.** A recipe’s parent is often a certificate that no slice
replays, because its own count is not recorded.
#789 retains `n850.cert` but does not replay it: 850 restates f1ceee4 (think-fwa9), so
its filtered receipts hold no 328, 850 or 909. Yet 850 is the parent of #763’s
`850 + kL` rows (1033 to 1378) and of the six unrequested `964ee2b` rows R3 records
(`850 + 10L` to `850 + 15L`, 1530 to 1945). So each records slice replays, on both
routes with six controls, every recipe parent that is not already a replayed row, and
lists those parents in `recipe-decisions.json`. **Price:** about 8 to 10 CPU-seconds a
parent to 1024 (#715’s 8.2, #742’s about 10), and about 84 above 1024 (the triage’s 12
CPU-seconds a decision, for seven decisions).
R3 needs 850, about 10 CPU-seconds; that replay now exists, on both routes with its six
controls refused, in the #763 packet’s `receipts/recipe-decisions.json`, written by
think-gn29 for #763’s recipes at 1024 and below.
R1’s count is known only once its walk runs.
think-cyal counts 98 certificates under #715’s 1,112 rows, 85 of them at their own
counts, so about 13 are parents only: about 0.3 CPU-hours.
R1 states its count before replaying, and stops for the coordinator if the parents would
carry it past 5 CPU-hours.

**The hold.** In the code an answered `Held` has no row, and D2 makes a decided recipe a
row, so D2 does not apply as `Held.answer` (the coordinator confirmed this on
think-llit, 24 October):
- a recipe the walk records and the checker decides is a declared row carrying its
  recipe, decided into `receipts/recipe-decisions.json` (`recipe-decisions`);
- the `RECIPE` hold class holds only the recipes the checker refuses: classical parents
  (think-zkxy) and Fang’s composites (think-tj3x);
- the frozen walks keep their `RECIPE` holds as written, with one exception: #763’s 13
  recipes, which the checker decides, are the one frozen `RECIPE` hold dropped, in
  think-gn29 for think-g2qy (`_HELD_763` keeps 683 alone).
  The walk’s ledger and verdicts are unchanged, and the 13 are rows of a source of their
  own, `couzo-issue763-2026-10-23-recipes`, because they reach `main` a day after #763’s
  other rows (`Split`; #800’s review A, A1 and A2);
- `HELD_CLASSES[RECIPE]` (`beyond_horizon_replay.py:346`) keeps its text, because the
  frozen walks render it.

### Deletion Rows (D6)

**What exists,** all in `beyond_horizon_replay.py`. A row can delete squares already:
`Claim.deleted` (`:873`). The replay decides such a row as its parent’s first n poses
(`certificate`, `:1504`). The parent must be a certificate the release reads whole, so
its controls stand (`deletion_problems`, `:4831`). `DELETION_ANSWER` (`:316`) settles a
bound that deletes one square from the next count’s published certificate: it is an
earlier report, so a later side equal to it or above it is not recorded.

**What W7 adds:**

- Declared rows carry `deleted`, as think-kzme’s answer needs either way.
- The walk above 1024 applies `DELETION_ANSWER` to one-square deletions from the next
  count, which includes `5a299b4`’s index bounds of that kind.
- Deletions of two or more squares hold on think-kzme, as 751, 752 and 927 do today.

**What waits on think-kzme.** The deletions an issue claims stay recorded in the walk
but have no rows until think-kzme is answered: #715’s 158 above 1024, and #763’s 1646
and 1727. R1 decides their positives, so writing their rows in R4 costs only seconds.

### Hosted Custody (N3, D4, OR-18)

- **Shards for #732.** There are nine `tar.xz` shards, one for each of the source’s
  thousands folders (`certificates/1000-1999/` through `certificates/9000-9999/`). Each
  holds the `nN.cert` files above 1024 at 17cc220, under the source’s own paths.
  Members are sorted, regular files only, with fixed metadata; the owner’s N3 puts the
  set at about 128 MB. The shards hold all 5,078 files, not only the rows the walk
  records. A walk rerun after an answer then needs no second release, and a release’s
  bytes never change.
- **Manifest.** The lane writes `packing/hosted/mishapolk-issue732-above-1024-v1.yaml`,
  with tag `data/mishapolk-issue732-above-1024-v1`, using
  `python -m devtools.hosted_data stage`. The paths go under a directory that Git
  ignores. The lane commits the manifest; the owner runs `publish`.
- **Packet.** `mishapolk-issue732-2026-10-22` stays the packet, since 17cc220 is the
  revision it pins (N6, below).
  The files above 1024 are declared pinned-only, with the hosted manifest as the reason
  (stage 2’s rule), and are fetched outside the packet’s archived directory, as Ryu’s
  are. The custody chain runs from the SHA-256 the issue states for
  `certificates/manifest.json`, to that manifest’s SHA-256 for each file, to each shard
  member. The packet retains the manifest if `check_added_blobs` admits it, and otherwise
  pins it and hosts it in the same release.
- **Couzo’s files above 1024 (D4).** The record recommends hosting them, and this plan
  follows that disposition (see [What the Owner Decided](#what-the-owner-decided)).
  #715’s and `5a299b4`’s certificates above 1024 go in one release,
  `data/couzo-715-certificates-v1`, with its manifest at
  `packing/hosted/couzo-715-certificates-v1.yaml`. The lane stages it in R1 and the
  owner publishes it before R1 merges; the tag is kept, not dropped.
  The size has been measured twice.
  think-cyal’s read of 22 October gives 9.1 MB as zlib stores #715’s 98 certificates
  (51.2 MB checkout). The triage of 23 October gives about 13 MB for Couzo’s files above
  1024, “host or commit”.
  OR-18 counts as Git stores and sends tens of megabytes to a hosted release, so 9 to 13
  MB would also pass `check_added_blobs` (48 MiB a pull request, 5 MiB a blob).
  Git stays the fallback if the owner prefers it, settled before R1’s first commit.
  #763’s six certificates above 1024 are already in #789’s packet, in Git.
- **Reader.** `beyond_horizon_replay` asks `sqpack.hosted_data.require`
  (`packing/src/sqpack/hosted_data.py:444`) for an object, which checks the object’s
  size and SHA-256. For a shard, it then streams the members with `tarfile`. It refuses
  a member that is not a regular file, that escapes the shard or repeats, whose header
  size differs from the source manifest’s where that manifest states one, or whose
  SHA-256 is not the source manifest’s. It also bounds the shard’s unpacked total.
  The checks in `refinement_custody.py:399`–`:420` are the precedent.
- **Who reads hosted objects.** `filtered`, `exhaustive`, `check --replay` and
  `source-history` read them above 1024. The fast `check` reads none.
- **The other sources go into Git:** Fang’s 4 MB, #719’s 0.06 MB, and Daniel’s and
  Barnett’s, each under 0.2 MB. Each is checked with `check_added_blobs` before its
  first commit.

### Gate Cost

**Measured on this host on 24 October**, at b2ea7b09c, under `nice`, on the shared
4-core machine:

- **The fast check.** `test_the_receipts_records_and_coverage_rows_hold`
  (`tests/test_beyond_horizon_replay.py:146`), which runs `check(replay=False)` over the
  18 releases, takes 32.1 s.
- **Where its time goes.** Under a profiler, 76% of it parses whole certificates in
  `decided_sides` (`beyond_horizon_replay.py:1531`): 739 certificates parsed three
  times, 2,217 parses and 4.63 million rationals.
  The function runs once each from `release_problems` (`:4873`), `beyond_horizon_rows`
  (`:1875`) and `_cross_check_problems` (`:4903`). A further 18% is `custody`, which
  runs `acquire_source.check` over every retained file.
- **At #732’s scale.** #732’s 27.7 million squares above 1024 are about 83 million
  rationals in each pass.
  The same check would add on the order of 1,300 CPU-seconds to every run (three passes
  at the measured cost of a rational), and it would need the shards in CI.
- **The walk.** `render --check` over the history walk (700 counts) takes 1.0 s. A walk
  of about 5,000 counts projects to between 8 and 13 s.
- **The walk’s README.** The #732 walk’s README is 190,553 bytes for 390 counts, so a
  README of about 2.5 MB would come with 5,000 counts.
- **The register.** It loads in 0.145 CPU-seconds with its 1,484 beyond-horizon rows, at
  about 204 bytes per row; `check_source_coverage`, a `--records` step, takes 3.6 s of
  wall.
- **Where the gate runs these.** The two test files run in the pytest shards (`suite-a`
  to `suite-d`, ceilings of 335 to 360 s). `devtools/suite-file-costs.json` records 17.3
  seconds hosted for `tests/test_beyond_horizon_replay.py` and 1.0 s for
  `tests/test_intake_ledger.py`. `check_source_coverage` runs in
  `packing-validate --records`, whose ceiling is 300 s and which last measured 11.0 s
  ([development.md, the tiers](../../../../development.md#the-tiers)).

W7 therefore makes five changes:

- `decided_sides` reads only the header line (`_header`), once per release.
- The fast check holds a hosted row to its receipts and to the source index’s path,
  SHA-256 and exact bound, without opening a shard.
- Göbel’s side comes from the cached table instead of a scan of every member for each
  count (`goebel_at`).
- `intake_ledger render` writes a summary README once a walk passes a few hundred
  counts. The per-count verdicts stay in `ledger.json`, and the README keeps the tallies,
  each report, the rulings and the owner’s lists.
- W7 measures before and after, and so does each records slice.

**The targets** (`OR-14`, `OR-17`), with every row above 1024 recorded:

| Step that grows with rows | Where it runs | Today | Budget |
| --- | --- | --- | --- |
| `tests/test_beyond_horizon_replay.py`, including `check(replay=False)` with `chain_problems` and `construction_problems` over every row beyond 324 | the pytest shards | 32.1 s locally for its check test; 17.3 s hosted for the file | no more than today, in both figures; today’s rows alone should drop to about 8 s locally |
| `tests/test_intake_ledger.py`, the render check of every walk | the pytest shards | 1.0 s hosted | 15 s, which leaves room for the walk above 1024 |
| `check_source_coverage`, and each other module that loads the register | `--records`; the shards | 3.6 s; a load of 0.145 CPU-seconds | 6 s; 1.1 s a load |

The shard that holds each test file stays within its ceiling, and `--records` within its
300 seconds. The measurement is a tier wall, not one test: W7 measures `--records` and
the `suite-file-costs.json` figures before and after its change, and R2 measures them
again once #732’s rows are in.

### The Walk Above 1024

- **Reports and starts.** Every report in the table above enters in report order.
  `history-publications` and `earlier` scan the watched repositories above 1024 as well.
  Barnett’s repository joins `WATCHED_HOLDERS` (`beyond_horizon_replay.py:2597`), unless
  his side at 2043 comes through an issue instead.
- **The catalogue.** Its four sides enter under a new hold class, on N1: the walk
  records them and the chain passes over them, so only the verdicts that rest on them
  wait (`Resting`, `held-dependents`).
- **Restatements.** At 66 counts #732 is below #715’s print by less than 1e-12
  (think-f2io), so it restates #715 there and is not recorded.
- **A side within the print below the construction.** Any side the walk finds within the
  print below Göbel’s construction is held on think-oqjd.
  To 1024 there is none.
- **The rulings.** `answer_problems` holds: both rulings apply at every count, and
  nothing is named under `rulings_not_applied`.
- **Credit at 1061, 1413 and 1489.** R1 records #666’s and #719’s rows at these counts.
  #790 reads `1c17153`’s manifest as keeping Couzo’s staircase assemblies there,
  credited to Arslanov, Mustafin and Shangitbayev (2021) and to de Winter’s staircase
  and four-block constructions, as the previous source of Polkovskyi’s certificates.
  #790 says the import of the rows above 1024 cites the manifest, not the comment.
  The walk’s notes cite `1c17153`’s manifest at the three counts, and any per-row credit
  there waits on D5.

### The Rule Text

W7 updates the rules where they live:

- **The frontier README, Source Coverage and Freshness**
  (`packing/frontier/README.md:223` to `:234`). Rows are tracked beyond 324 with no
  ceiling, recorded as reported (D1). Göbel’s construction holds at every count, from
  the maintained module, each side final by the area bound.
  This replaces “holds every row from n = 325 to 1024”. A construction that an index or
  table states with no certificate file of its own (a tiling or L-border recipe on a
  certificate) is a row once the maintained checker decides it exactly from the recipe
  and the parent is replayed (D2). A deletion bound is no recipe row: one square below
  the next count’s certificate is an earlier report by D6, and any other deletion, or
  one an issue claims, waits on think-kzme (`deletion_holds`). A certificate kept as
  hosted data is read through its manifest, while its receipts and rows stay in Git
  (`OR-18`).
- **The frontier README, Adding or Reviewing a Result** (`:349`–`:355`): the same, in
  one sentence.
- **`packing/campaign/result-import.md`, Several Reports at One Count** (`:498`–`:499`
  at 830dfb470). “The 15 October packet’s retained program computes it exactly to 1073,
  where its reach ends” becomes the maintained module and its proved reach.
  A recipe sentence is added beside the deletion bullet.

### API Changes

- `devtools.goebel_construction` (new): `families(limit)`, `side(n)` (the form at n),
  `proved(n)`, `reach()`.
- `devtools.construction_checker` (new): `decide(recipe, parent)`, and controls
  `mutants(recipe)`.
- `beyond_horizon_replay.Release` gains `decided_above: int = HORIZON`,
  `decided_through: int | None = FROZEN_THROUGH` and `hosted: Path | None`, and
  `walk_of` takes the count.
  W7 sets none of them on an existing release.
- `beyond_horizon_replay.goebel` writes `beyond-horizon-goebel-comparison-v2`, naming
  the module, for a window above 1024. A frozen window keeps v1 and the retained
  program.
- The walk ledger gets rulings with no `through`, and a held class for the catalogue
  (N1).
- Records, written in the slices, not in W7: the walk directory above 1024; the lifted
  windows and their receipts; the release “#715” for rows above 1024, with a second
  coverage source in the #715 packet; `receipts/recipe-decisions.json`; and the two
  hosted manifests.

## Implementation Plan

### Phase 1: The Code Slice (W7)

W7 starts once #789 has merged, from the `main` that holds it.
It goes as one pull request or a stack of three ([Approach](#approach)), and it records
nothing.

- [x] `goebel_construction` and its tests.
  The readers that must reach past 1073 move to it; frozen receipts keep the retained
  program; the reach tests change.
- [x] The ceiling: every site in the tables above, #789’s included, `FROZEN_THROUGH` for
  the frozen walks and releases, `Release.decided_above` and `decided_through`, and
  `walk_of` by count.
- [x] The regression control: every existing receipt, frozen walk (`ledger.json`,
  `sources.yaml`, `README.md`) and claims record is rebuilt by its writer, with no
  replay, and compared byte for byte before and after W7. The writers that read clones
  (first commits, source history, earlier publications, later commits) are not rerun;
  #678’s Göbel receipt already differs from its writer at the base, by one word of its
  `families` sentence, and is left as committed.
- [x] The construction checker and its controls.
  The settled `RECIPE` hold is not built as `Held.answer`: in the code an answered hold
  has no row, and D2 makes a decided recipe a row.
  A recipe the walk records and does not hold is a declared row the checker decides
  (`recipe-decisions`), and the class holds only the recipes it refuses (think-llit’s
  note of 24 October).
- [x] Deletions: declared `deleted`, and `DELETION_ANSWER` above 1024.
- [x] The hosted reader, and `source-history` above 1024 reading shard headers.
- [x] Gate cost: header-only sides, the cached Göbel table, and the summary README;
  measured before and after.
  The summary starts above 400 walked counts, over every retained walk’s.
- [x] The rule text in the frontier README and the runbook.
- **Price:** under 0.1 CPU-hours (tests, the gate measurements, and the build to 10,500,
  which takes 0.01 CPU-seconds).

**W8, the two-strip checker (think-clgp).** #799 reports Mohsen Karimi’s 683 rows at
1184 to 3775 as parameters of a two-strip L-packing, with no certificate file and no
parent, so `construction_checker` cannot read them.

- [x] `devtools.two_strip_checker` decides such a row exactly from its parameters, with
  seven controls and a write-out builder.
  It agrees with both routes at five written-out counts and with Ryu’s Theorem 1.3
  packings.
- [x] #799’s packet `karimi-two-strip-2026-10-24` and its requests entry, triage
  pending.
- **Price:** about 0.02 CPU-hours: 7 CPU-seconds to decide all 683 with their controls,
  and 73 for the five counts on both routes with six controls each.

### Phase 2: The Records, in Report Order

Each records slice is one pull request, opened after the one before it merges.
Each is one item under the cap (think-lh7d).

| Slice | What it records | Depends on | CPU-hours | Basis |
| --- | --- | --- | ---: | --- |
| R1 | Gathers the walk. Lifts the windows of #666, #719, `bef5c42` and `5a299b4`, and adds the #715 release, each with its receipts. Rows of #666 (8), #719 (8; facts derived from its packet), #715 above 1024 (its new source), Couzo’s watched publications above 1024 (`5a299b4`’s index), Fang (62) and Barnett (2043). Daniel’s 1092 and 1228 are not recorded (think-jtlq). Replays the recipe parents that are not rows, and decides the positives of the deletions held on think-kzme. Stages `data/couzo-715-certificates-v1` | W7 merged; the owner publishes `data/couzo-715-certificates-v1` before R1 merges | about 4.3 | the triage: every source but #732, positives and all six controls, about 4 (#666, #719, #715, Fang and Barnett about 3.5); about 0.3 for some 13 parents |
| R2 | Lifts #732’s window. #732’s rows above 1024 (4,319 under the triage’s count, re-derived by the walk); the hosted manifest | R1 merged; the owner publishes `data/mishapolk-issue732-above-1024-v1` before R2 merges | about 32 | N2: positives on both routes for every recorded row, six controls on a stratified 10%, and an all-pairs sample at three counts below 2,000, about 0.3 of it at #742’s 0.33 CPU-ms per pair |
| R3 | Lifts #763’s and `964ee2b`’s windows. #763’s 233, `964ee2b`’s 6 unrequested rows below every earlier report, and `43f666c`’s 831 recipes. Replays 850 and any other parent that is not a row | R2 merged; #789 and think-gn29’s import to 1024 merged, since they retain the parents and replay the parents that are rows | about 0.1 | 6 certificates, 0.06 CPU-hours (think-cnn7); 850, about 10 CPU-seconds; recipes take seconds |
| R4 | Held rows after the answers: deletions (think-kzme), the four catalogue counts (N1), recipe kinds the checker does not read (think-zkxy, Fang’s composites), and per-row credit (D5) | the answers | seconds | R1 decided the positives; otherwise about 12 CPU-seconds per certificate above 1024, the triage’s average, so under 0.6 for all 160 deletions |
| **Total** |  |  | **about 36** | within N2 |

**R5, #799’s rows (think-5dc3).** #799 enters R1’s walk as a report, and its rows land
in a slice of their own after R1 and W8, each decided by `two_strip_checker`. R5 does
not need R2 or R3: the chain passes over their unlanded rows, which are written as
superseded when they land.
The triage priced it at about 0.8 CPU-hours, an item of its own outside N2’s 36: the
checker on every row, the written-out positives on both routes, and six controls at one
count per K. That scope and price are for version 1’s 683 rows.
Version 2 of the deposit (10.5281/zenodo.23628190, 2,824 rows to 9944) and the author’s
preprint arrived on #799 after the triage.
Their triage decides whether R5 covers 683 or 2,824 rows, and at 2,824 rows reaching
larger counts the price is at least four times as much.

**The stratified 10% (R2).** Within each thousands folder, the recorded rows are sorted
by count. Every tenth row is taken from a start the code fixes, about 432 of 4,319 in
all, plus up to nine more: each folder’s row with the least margin.
The receipt names the rule and the rows.
Every control of every certificate would cost about 157 CPU-hours, which N2 does not
buy.

**For each slice:**

- [ ] Retain or host the files, running `check_added_blobs` before the first commit.
- [ ] Lift the windows of the slice’s releases in the same commit as their receipts.
- [ ] `filtered` and `exhaustive`, the recipe parents that are not rows, recipe
  decisions, `goebel`, `claims-record`, `declare-rows` and `coverage-plan`. For R1 also
  `gather`, `render` and `check` of the walk.
- [ ] `python -m devtools.stamp_landed --apply` for each new source of beyond-horizon
  rows (result-import.md’s eighth record rule, on `main` since 830dfb470).
- [ ] `check --replay` for the slice’s releases, and the records tier.
- [ ] Requests entries, then the stage 7 replies after the merge: #666, #715, #719, #732
  and #763.

## Testing Strategy

**Negative controls first.** Each new check lands with its refusals tested before any of
its positives counts.

1. **The ceiling.**
   - Refusals: a frozen release asked to decide a claim above `FROZEN_THROUGH` is
     refused (its decided count no longer matches).
     A frozen walk’s rulings keep `"through": 1024`.
   - Regression: every existing receipt, frozen walk and claims record is rebuilt byte
     for byte the same before and after W7 ([Phase 1](#phase-1-the-code-slice-w7)).
2. **Göbel.**
   - Refusals: a count above the proved reach is refused by the gather, the import and
     the receipt (today’s test at 1074, adapted).
     The completeness test refuses the retained loops raised to 10,500, at all 1,573
     counts.
   - Positives: no disagreement with the retained program from 325 to 1073; every side
     proved up to the walk’s top count; and the catalogue’s own words at 1765 and 2043.
3. **The checker.**
   - Refusals:
     - a count one above the capacity;
     - a side one unit below `tS + L`;
     - a parent whose digest is altered, or whose count is wrong;
     - `t = 0`, or `L < 0`;
     - a parent that fails both routes, such as the duplicate-square control;
     - a parent that is not yet replayed;
     - a parent that is a classical construction, such as Friedman’s (think-zkxy);
     - a Fang composite whose parts the table does not state;
     - an unknown recipe kind;
     - a deletion of more squares than the parent holds.
   - Positives: the #715 packet’s filtered receipt holds 59 L-border files and 13
     deletion rows up to 1024, each written out in full and verified on both routes.
     For each, the checker’s capacity, side and verdict must agree with the replay.
     None of them tiles (t = 1 throughout), so W7 adds a fixture: a small replayed
     certificate tiled with t = 2, written out and replayed on both routes.
4. **The hosted reader.**
   - Refusals:
     - an object that is absent (`HostedDataMissingError` names the fetch);
     - an object that is truncated or altered (`require`’s size and SHA-256 checks);
     - a member whose bytes are altered, or that is larger than a member may be (the
       source states no sizes, so a member’s size is bounded, not compared, #793’s
       review A, A7); a missing or extra member; a member that repeats;
     - a pax or long-name record that decompresses past the bound (review C, C1);
     - a link, or a `..` path;
     - a shard whose unpacked total passes its bound.
   - Positive: shards built from a clone at 17cc220 read back byte for byte on a sample.
5. **The replay.**
   - Both routes refuse each certificate’s six controls before its positive counts: for
     every certificate in R1, every recipe parent replayed, and the 10% in R2.
   - Every positive runs on both routes.
   - The all-pairs kernel agrees at the sampled counts.
6. **The walk above 1024.**
   - Refusals:
     - a walk above 1024 whose rulings stop at 1024 fails `answer_problems`;
     - a deletion of two squares above 1024 is not settled by `DELETION_ANSWER` and
       stays held on think-kzme;
     - a catalogue side declared as a row before N1 is answered is refused by the
       coverage check.
   - Positives: `answer_problems` finds nothing to report; the 66 restatements are not
     recorded; `check --tree` holds Göbel’s member at every count; `held-dependents`
     names each verdict that rests on a hold.
7. **The gate.** The tier walls and the per-step figures are measured before and after
   W7, and in R2, against the budgets in [Gate Cost](#gate-cost).

## Rollout Plan

- **W7** follows #789, as one pull request or a stack of three.
  It registers nothing, so each pull request is labelled S1 and project.
  It should get a dedicated correctness review (exact arithmetic, persisted receipts,
  custody).
- **R1 to R3** are records pull requests labelled `intake`, each with an S label by the
  runbook’s rubric. #742, #732’s rows to 1024, was S2.
- **The owner’s two publishing steps.** `data/couzo-715-certificates-v1` before R1
  merges, and `data/mishapolk-issue732-above-1024-v1` before R2 merges.
- **R4** follows the answers, and each answer reruns the walk (`held-dependents`).
- **After each merge,** the stage 7 replies.

## Open Questions

### Decided by a Stated Rule or the Record

These need no owner answer before any slice.

- **D3 (335).** “Stage 3 registers what `ledger.json` records, and nothing it does not
  unless the owner names a key reason” (result-import.md, Several Reports at One Count).
  The walks leave #715’s 335 unrecorded.
  On `main` at 830dfb470 the current row at 335 is
  `mishapolk-issue732-f1ceee4-2026-10-23`
  (`packing/frontier/source-coverage.yaml:23474`), which supersedes Couzo’s 8 October
  row, and #789 records `964ee2b`’s 335 below it.
  A key reason would therefore add only a superseded #715 row.
  Nothing above 1024 depends on it, and nothing waits for it.
  think-f2io also recommended checking the 8 October decimal poses exactly first.
  That check belongs to think-cyal, whose acknowledgement on #715 promised it; with
  f1ceee4’s row current, it can only correct a superseded row.
- **D4 (hosting Couzo’s certificates above 1024).** The record’s disposition stands
  (quoted in [What the Owner Decided](#what-the-owner-decided)): host them, as
  `data/couzo-715-certificates-v1`, with the owner publishing.
  This is the record’s recommendation, not the owner’s word.
  At the measured 9 to 13 MB, OR-18 would also admit Git, so the owner may choose that
  instead before R1’s first commit ([Hosted Custody](#hosted-custody-n3-d4-or-18)).
- **N4 (one coverage file or a split).** The frontier README says the register “records
  … relevant claims beyond n = 324” (`packing/frontier/README.md:196`–`:199`). OR-18
  counts a record as a record, not bulk data.
  Measured: about 204 bytes per row, which compresses 17.7 times, so about 52 kB as Git
  stores 4,500 rows and about 115 kB for 10,000. The load takes 0.145 CPU-seconds today.
  Scaled by the file’s bytes or by its rows, it projects to 0.3 to 0.6 s with 4,500 more
  rows, and 0.5 to 1.1 s with 10,000 more.
  One file, then. A split would cost one loader across the 12 modules that read the rows.
  The question reopens only if W7’s gate measurement passes the budget in
  [Gate Cost](#gate-cost).
- **N6 (the #732 pin: 17cc220 or 7b6366f).** Stage 1 pins the head “unless the claim
  depends on an older revision”, and stage 2 adds that “files added later from the same
  revision join the packet they belong to”.
  The issue’s five digests are those of 17cc220’s indexes; 7b6366f withdraws 3426, which
  changes them. The claims therefore depend on 17cc220, the existing packet’s revision.
  3426 is above its own grid side, so it is not recorded at either pin, and nothing
  rests on the choice.

### For the Owner

No rule decides these.
Each recommendation is the coordinator’s, not the owner’s.

- **D5: per-row credit beyond the corpus.** The runbook decides the principle: a
  refinement is “credited to its finder after the finder of the packing it refines”
  (Several Reports at One Count), and the identity “stays the source’s claim until a
  measurement here decides it” (stage 3). A row beyond the corpus, though, has no field
  for it: its credit is its source’s. *Recommended:*
  - An optional per-row `refines` that names the source and count of the packing
    refined, written from the source’s own per-row statement.
  - A measurement (#769’s `pose-identity`) only where an author asks for credit or two
    statements conflict.
    Polkovskyi’s 11 counts follow #769’s measurement.
  - No row waits on this answer; the credit is added later.
- **think-kzme: does a deletion bound get a row?** *Recommended:* the recommendation on
  think-f2io.
  - No row of its own, except where an issue claims the count.
    Then the issue’s row is recorded at the bound, if it is below every earlier report,
    and replayed as the parent’s first n poses.
    Above 1024 that covers #715’s 158, and #763’s 1646 and 1727.
  - Bounds that delete two or more squares are earlier reports too.
    The replay already decides any deletion as the parent’s first n poses
    (`beyond_horizon_replay.py:51` to `:54`). The owner’s answer is only the selected
    label, and nothing in the question’s rationale, which was the coordinator’s, depends
    on how many squares are deleted.
    `DELETION_ANSWER`’s comment keeps such bounds outside the question’s words
    (`beyond_horizon_replay.py:315`), so they stay held until the owner answers.
- **N1: the Kingbird catalogue beyond 324.**
  - Today the start beyond 324 is a row or the grid.
    The order rule names issues, comments, pull requests and watched commits, and the
    catalogue is none of these.
  - *Recommended:* yes, the catalogue’s sides are earlier reports, as Göbel’s
    construction is: start members at their exact algebraic sides (the capture states
    each minimal polynomial), dated by the capture of 2026-08-22, with no rows of their
    own.
  - Above 1024 the answer decides 1453, 1765, 1850 and 2043.
  - It also reaches 626, where Ellsworth’s 27/2 + 17√2/2 continues Friedman’s series,
    which is think-zkxy’s question.
    A yes reruns the walks to 1024 at 626 only.
- **N5: does the site show rows above 1024?**
  - No page of the site lists beyond-horizon rows today, at any count: only the checks,
    the importers and the profile audit read them.
  - A table of about 10,000 rows, near 1 MB, is over the 600,000-byte page budget
    (development.md, Validation and Page Budgets).
  - *Recommended:* no table in this plan.
    The pages stay as they are; a one-line count on an existing page can come in a site
    plan.

## References

- Beads: think-llit (this plan), think-f2io (D1 to D6), think-kzme, think-8krd and #613,
  think-fwa9, think-cyal (#715’s import, which keeps its rows above 1024 queued),
  think-0gp6 (#732), think-jtlq (Daniel), think-cnn7 and think-ptkk (#763, PR #789),
  think-cncq and think-gn29 (`43f666c`), think-zkxy, think-oqjd, think-lh7d (the cap).
- #790, which reads `1c17153`’s manifest at 1061, 1413 and 1489.
- Review A of #791: https://github.com/jlevy/squares/pull/791#issuecomment-6383635522
- [Several Reports at One Count](../../../../packing/campaign/result-import.md#several-reports-at-one-count)
  and
  [The Compute Cap](../../../../packing/campaign/result-import.md#the-compute-cap-and-the-validation-backlog)
- [Frontier README, Source Coverage and Freshness](../../../../packing/frontier/README.md#source-coverage-and-freshness)
- [OR-18](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
  and [Publishing Hosted Data](../../../../development.md#publishing-hosted-data)
- Review B of #754: https://github.com/jlevy/squares/pull/754#issuecomment-6376229374

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
