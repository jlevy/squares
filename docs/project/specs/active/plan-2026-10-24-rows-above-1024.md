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
- #732’s certificates above 1024 kept as hosted data (N3), read through their manifest.
- A records-tier check no slower than it is today, with every row above 1024 in it.
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

Still open: D3, D5, think-kzme’s sub-question on D6, N1, N4, N5 and N6.
[Open Questions](#open-questions) sorts them into those a stated rule already decides
and those only the owner can answer.

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
| #715, Francisco Couzo | 2026-10-21T20:55:57Z | 1,112 claims: about 129 files, 825 recipes, 158 deletions |  | Git: about 13 MB raw, with the index’s files |
| Couzo’s index at `5a299b4` | push 2026-10-21T22:56:37Z | 5,078 counts: 95 certificates, 187 deletions, 4,796 tiling and L-border recipes | index and files | as above |
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

### What Stops at 1024 Today

- **The ceiling.** `beyond_horizon_replay.LIMIT = 1024`
  (`packing/devtools/beyond_horizon_replay.py:233`) and `couzo_715_replay.LIMIT = 1024`
  (`packing/devtools/couzo_715_replay.py:113`). Every row above 1024 is “retained and
  not decided” (`held_claims`, `:1482`).
- **Göbel’s reach.** The retained program
  (`packing/resources/web/couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py`)
  builds its families only up to `LIMIT = 1100` (`:57`). Its largest member is at 1073
  (`intake_ledger.goebel_reach`, `packing/devtools/intake_ledger.py:1782`). Review B of
  #754 found that one count above 1073 refuses a whole input, not just that count.
  An import is refused through `upper_bound_reports.compare` (`:1767`), which builds
  every row before it writes and raises through `goebel_construction` (`:1621`). An
  earlier-publications receipt is refused through `standing_sides` (`:2106`). A gather
  is refused through `intake_ledger.tree_members` (`:1364`, with Göbel’s member at
  `:1418`).
- **No recipe checker.** A recipe is the `RECIPE` hold class (`:281`–`:293`): recorded
  in the walk, but with no row.
- **No hosted reader.** `certificate()` (`:1504`) reads a retained file or a derived
  fact, never a hosted object.
- **The check’s cost.** [Gate Cost](#gate-cost) measures it below.

## Design

### Approach

The work has two phases.
Phase 1 is one code slice (W7) with no records in it.
Phase 2 records the rows in report order.

One walk decides every count above 1024, from all the reports to date.
It is gathered once, in R1, at
`packing/campaign/issue-intake/upper-bounds-above-1024-YYYYMMDD/`, read on the day R1
starts and with its starts frozen at that `main`. Each start holds the grid and Göbel’s
construction. Each later slice writes the rows that walk records for its own sources.
Where a report the walk records has not yet had its import written, the chain passes
over it until its rows land (`Awaiting`), as the history walk did below 1024. A report
published after the walk’s reading gets a walk of its own, as below 1024.

### The Ceiling: `LIMIT` and Every Use of It

Some uses of `LIMIT` describe walks that are frozen at 1024; those keep the value under
a name that says so (`FROZEN_THROUGH`). The other uses act as a ceiling, and those are
lifted. All line numbers refer to `main` at b2ea7b09c.

**`packing/devtools/beyond_horizon_replay.py`:**

| Site | Today | After W7 |
| --- | --- | --- |
| `:233` `LIMIT = 1024` | the module’s ceiling | `FROZEN_THROUGH`: the reach of the walks frozen at 1024; no longer a ceiling |
| `:428` `HISTORY_COUNTS` | the history walk’s counts | unchanged: a frozen walk |
| `:799`–`:818` `_rulings` (`"through": LIMIT`), `:824` `WALK_RULINGS` | both rulings through 1024 for the four walks | unchanged for those walks. The walk above 1024 lists both rulings with no `through` (`intake_ledger.NO_LIMIT`, `:1750`), so they reach its top count, as `answer_problems` (`intake_ledger.py:728`) requires |
| `:1472` `decided_claims`, `:1482` `held_claims` | a release decides its rows to 1024; rows above wait | a decided window per release (`Release.decided_through`, defaulting to 1024, so the 18 releases’ receipts stand); #666, #719, #732, `bef5c42` and `5a299b4` (`couzo-reconcile-2026-10-20`) take no ceiling |
| `:1841`–`:1850` `goebel` | requires `program.LIMIT >= LIMIT` | reads the maintained module, and requires its proved reach to cover the release’s top count |
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

**`packing/devtools/couzo_715_replay.py`:**

| Site | Today | After W7 |
| --- | --- | --- |
| `:113` `LIMIT = 1024`, `:114` `DECIDED = 173`, `:191` `decided_claims` | the decision of 21 October on #715, to 1024 | unchanged: its receipts are #715’s record to 1024 |
| `:151`, `:613`–`:623` `goebel` | the retained program, `program.LIMIT >= LIMIT` | the maintained module, which agrees with the retained program at every count to 1073, so the receipt does not change |
| #715’s 1,112 claims above 1024 | not decided | a `Release` for issue 715 in `beyond_horizon_replay`, deciding only above 1024, with its own `source_id`, `record` and `receipts` in the #715 packet (`Release` fields at `:954`–`:956`). `couzo_715_replay` owns the existing source’s claims record, and a coverage source declares one record. Couzo’s `23aff0c` beside #670 is the precedent |

The other readers of the retained program move to the maintained module too:
`intake_ledger.py:200` (`GOEBEL_PROGRAM`) and `:1772`–`:1803` (`_goebel`,
`goebel_reach`, `goebel_form`), and `couzo_678_replay.py:122` and `:925`. The tests that
pin the old reach change with them: `tests/test_intake_ledger.py:407`
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
strip is built above 1617. Between 1682 and 6116 the program would then take the least
of the squares alone, a side that is too large.
A row above Göbel’s true construction but below that side would be recorded.

This plan’s sample checks both claims, using a scratch script that reads the retained
program unchanged; W7 makes the sample a test (`OR-1`):

| Build | Members | Largest member | Against the retained program, 325 to 1073 | Final by the area bound |
| --- | ---: | --- | --- | --- |
| The retained program, `LIMIT = 1100` | 104 | 1073 | itself | — |
| The same loops, `LIMIT` raised to 10,500 | 186 | 6256; no strip above 1617 | — | wrong, too large, at 1,573 counts from 1682 to 6116 |
| Loop bounds derived from the limit, to 10,500 | 343 | at most 10,500 | 0 disagreements | every count from 325 to 10,000 |

The table to 10,000 takes 0.01 CPU-seconds in one descending pass.

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
- The retained program stays unchanged, as the 15 October record and the regression
  oracle. Receipts already written keep naming it.

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
It requires the stated bound to equal `tS + L` and the count to be within the capacity.
It refuses any recipe kind it does not read.
It refuses a parent that is a classical construction rather than a certificate the
record replays; Friedman’s waits on think-zkxy.
It refuses a Fang composite unless his table states the composite’s parts.
Each release writes `receipts/recipe-decisions.json`: the count, recipe, parent,
capacity, side and verdict.
`check` derives it again.

**The hold.** The `RECIPE` hold class (`beyond_horizon_replay.py:289`) becomes settled
for every recipe the checker decides.
D2’s answer applies as `Held.answer`, the way `DELETION_ANSWER` (`:316`) applies D6’s.

### Deletion Rows (D6)

**What exists.** A row can delete squares already: `Claim.deleted` (`:873`). The replay
decides such a row as its parent’s first n poses (`certificate`, `:1504`). The parent
must be a certificate the release reads whole, so its controls stand
(`deletion_problems`, `:4831`). `DELETION_ANSWER` (`:316`) settles a bound that deletes
one square from the next count’s published certificate: it is an earlier report, so a
later side equal to it or above it is not recorded.

**What W7 adds:**

- Declared rows carry `deleted`, as think-kzme’s answer needs either way.
- The walk above 1024 applies `DELETION_ANSWER` to one-square deletions from the next
  count, which includes `5a299b4`’s index bounds of that kind.
- Deletions of two or more squares hold on think-kzme, as 751, 752 and 927 do today.

**What waits on think-kzme.** The deletions an issue claims stay recorded in the walk
but have no rows until think-kzme is answered: #715’s 158 above 1024, and #763’s 1646
and 1727. R1 decides their positives, so writing their rows in R4 costs only seconds.

### Hosted Custody for #732 (N3, OR-18)

- **Shards.** There are nine `tar.xz` shards, one for each of the source’s thousands
  folders (`certificates/1000-1999/` through `certificates/9000-9999/`). Each holds the
  `nN.cert` files above 1024 at 17cc220, under the source’s own paths.
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
- **Reader.** `beyond_horizon_replay` asks `sqpack.hosted_data.require`
  (`packing/src/sqpack/hosted_data.py:444`) for a shard, which checks the shard’s size
  and SHA-256. It then streams the members with `tarfile`. It refuses a member that is
  not a regular file, that escapes the shard or repeats, or whose SHA-256 is not the
  source manifest’s. The checks in `refinement_custody.py:399`–`:420` are the precedent.
- **Who reads shards.** `filtered`, `exhaustive`, `check --replay` and `source-history`
  read them above 1024. The fast `check` reads none.
- **The other sources go into Git:** Couzo’s files above 1024 (about 13 MB raw, or 2 to
  3 MB as Git stores them at his zlib ratio of 4.3 to 6.5), Fang’s 4 MB, #719’s 0.06 MB,
  and Daniel’s and Barnett’s, each under 0.2 MB. Each is checked with
  `check_added_blobs` before its first commit.

### Gate Cost

**Measured on this host on 24 October**, at b2ea7b09c, under `nice`, on the shared
4-core machine:

- **The fast check.** `test_the_receipts_records_and_coverage_rows_hold`
  (`tests/test_beyond_horizon_replay.py:146`), which runs `check(replay=False)` over the
  18 releases, takes 32.1 s.
- **Where its time goes.** Under a profiler, 76% of it parses 2,217 whole certificates,
  4.63 million rationals, in `decided_sides` (`:1531`). That function runs three times
  for each release: from `release_problems` (`:4873`), `beyond_horizon_rows` (`:1875`)
  and `_cross_check_problems` (`:4903`). A further 18% is `custody`, which runs
  `acquire_source.check` over every retained file.
- **At #732’s scale.** #732’s 27.7 million squares above 1024 are about 83 million
  rationals in each pass.
  The same check would add on the order of 1,300 CPU-seconds to every run (three passes
  at the measured cost of a rational), and it would need the shards in CI.
- **The walk.** `render --check` over the history walk (700 counts) takes 1.0 s. A walk
  of about 5,000 counts projects to between 8 and 13 s.
- **The walk’s README.** The #732 walk’s README is 190,553 bytes for 390 counts, so a
  README of about 2.5 MB would come with 5,000 counts.
- **The register.** It loads in 0.145 CPU-seconds with its 1,484 beyond-horizon rows, at
  about 204 bytes per row.

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

**The target** (`OR-14`, `OR-17`): the records-tier check stays within today’s 32 s with
every row above 1024 recorded.
Today’s rows alone should drop to about 8 s.

### The Walk Above 1024

- **Reports and starts.** Every report in the table above enters in report order.
  `history-publications` and `earlier` scan the watched repositories above 1024 as well.
  Barnett’s repository joins `WATCHED_HOLDERS` (`:2597`), unless his side at 2043 comes
  through an issue instead.
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

### The Rule Text

W7 updates the rules where they live:

- **The frontier README, Source Coverage and Freshness**
  (`packing/frontier/README.md:223` to `:234`). Rows are tracked beyond 324 with no
  ceiling, recorded as reported (D1). Göbel’s construction holds at every count, from
  the maintained module, each side final by the area bound.
  This replaces “holds every row from n = 325 to 1024”. A construction that an index or
  table states with no certificate file of its own (a tiling, L-border or deletion
  recipe on a certificate) is a row once the maintained checker decides it exactly from
  the recipe and the parent is replayed (D2). A certificate kept as hosted data is read
  through its manifest, while its receipts and rows stay in Git (`OR-18`).
- **The frontier README, Adding or Reviewing a Result** (`:349`–`:355`): the same, in
  one sentence.
- **`packing/campaign/result-import.md`, Several Reports at One Count** (`:495`–`:496`).
  “The 15 October packet’s retained program computes it exactly to 1073, where its reach
  ends” becomes the maintained module and its proved reach.
  A recipe sentence is added beside the deletion bullet.

### API Changes

- `devtools.goebel_construction` (new): `families(limit)`, `side(n)` (the form at n),
  `proved(n)`, `reach()`.
- `devtools.construction_checker` (new): `decide(recipe, parent)`, and controls
  `mutants(recipe)`.
- `beyond_horizon_replay.Release` gains `decided_through: int | None = FROZEN_THROUGH`
  and `hosted: Path | None`. `walk_of` takes the count, and `RELEASES` gains the release
  “#715” for rows above 1024.
- The walk ledger gets rulings with no `through`, and a held class for the catalogue
  (N1).
- Records: the walk directory above 1024; `receipts/recipe-decisions.json`; the hosted
  manifest; and a second coverage source in the #715 packet.

## Implementation Plan

### Phase 1: The Code Slice (W7, One Pull Request)

- [ ] `goebel_construction` and its tests.
  Every reader of `GOEBEL_PROGRAM` moves to it, and the reach tests change.
- [ ] The ceiling: every site in the tables above, `FROZEN_THROUGH` for the frozen
  walks, `Release.decided_through`, and `walk_of` by count.
- [ ] The construction checker, its controls, and the settled `RECIPE` hold.
- [ ] Deletions: declared `deleted`, and `DELETION_ANSWER` above 1024.
- [ ] The hosted reader, and `source-history` above 1024 reading shard headers.
- [ ] Gate cost: header-only sides, the cached Göbel table, and the summary README;
  measured before and after.
- [ ] The rule text in the frontier README and the runbook.
- **Price:** under 0.1 CPU-hours (tests, the gate measurements, and the build to 10,500,
  which takes 0.01 CPU-seconds).

### Phase 2: The Records, in Report Order

Each records slice is one pull request, opened after the one before it merges.
Each is one item under the cap (think-lh7d).

| Slice | What it records | Depends on | CPU-hours | Basis |
| --- | --- | --- | ---: | --- |
| R1 | Gathers the walk. Rows of #666 (8), #719 (8; facts derived from its packet), #715 above 1024 (its new source), Couzo’s watched publications above 1024 (`5a299b4`’s index), Fang (62) and Barnett (2043). Daniel’s 1092 and 1228 are not recorded (think-jtlq). Decides the positives of the deletions held on think-kzme | W7 merged | about 4 | the triage: every source but #732, positives and all six controls (#666, #719, #715, Fang and Barnett about 3.5) |
| R2 | #732’s rows above 1024 (4,319 under the triage’s count, re-derived by the walk); the hosted manifest | R1 merged; the owner publishes the release before R2 merges | about 32 | N2: positives on both routes for every recorded row, six controls on a stratified 10%, and an all-pairs sample at three counts below 2,000, about 0.3 of it at #742’s 0.33 CPU-ms per pair |
| R3 | #763’s 233, `964ee2b`’s 6 unrequested rows below every earlier report, and `43f666c`’s 831 recipes | R2 merged; think-ptkk (#789) and think-gn29’s import to 1024 merged, since they replay the recipes’ parents | about 0.1 | 6 certificates, 0.06 CPU-hours (think-cnn7); recipes take seconds |
| R4 | Held rows after the answers: deletions (think-kzme), the four catalogue counts (N1), recipe kinds the checker does not read (think-zkxy, Fang’s composites), and per-row credit (D5) | the answers | seconds | R1 decided the positives; otherwise about 12 CPU-seconds per certificate above 1024, the triage’s average, so under 0.6 for all 160 deletions |
| **Total** |  |  | **about 36** | within N2 |

**The stratified 10% (R2).** Within each thousands folder, the recorded rows are sorted
by count. Every tenth row is taken from a start the code fixes, plus the folder’s row
with the least margin, about 432 of 4,319 in all.
The receipt names the rule and the rows.
Every control of every certificate costs about 157 CPU-hours, which N2 holds.

**For each slice:**

- [ ] Retain or host the files, running `check_added_blobs` before the first commit.
- [ ] `filtered` and `exhaustive`, recipe decisions, `goebel`, `claims-record`,
  `declare-rows` and `coverage-plan`. For R1 also `gather`, `render` and `check` of the
  walk.
- [ ] `check --replay` for the slice’s releases, and the records tier.
- [ ] Requests entries, then the stage 7 replies after the merge: #666, #715, #719, #732
  and #763.

## Testing Strategy

**Negative controls first.** Each new check lands with its refusals tested before any of
its positives counts.

1. **Göbel.**
   - Refusals: a count above the proved reach is refused by the gather, the import and
     the receipt (today’s test at 1074, adapted).
     The completeness test refuses the retained loops raised to 10,500, at all 1,573
     counts.
   - Positives: no disagreement with the retained program from 325 to 1073; every side
     proved up to the walk’s top count; and the catalogue’s own words at 1765 and 2043.
2. **The checker.**
   - Refusals:
     - a count one above the capacity;
     - a side one unit below `tS + L`;
     - a parent whose digest is altered, or whose count is wrong;
     - `t = 0`, or `L < 0`;
     - a parent that fails both routes, such as the duplicate-square control;
     - an unknown recipe kind;
     - a deletion of more squares than the parent holds.
   - Positives: the #715 packet’s filtered receipt holds 59 L-border files and 13
     deletion rows up to 1024, each written out in full and verified on both routes.
     For each, the checker’s capacity, side and verdict must agree with the replay.
     None of them tiles (t = 1 throughout), so W7 adds a fixture: a small replayed
     certificate tiled with t = 2, written out and replayed on both routes.
3. **The hosted reader.**
   - Refusals:
     - a shard that is absent (`HostedDataMissingError` names the fetch);
     - a shard that is truncated or altered (`require`’s size and SHA-256 checks);
     - a member whose bytes are altered, a missing or extra member, a member that
       repeats;
     - a link, or a `..` path.
   - Positive: shards built from a clone at 17cc220 read back byte for byte on a sample.
4. **The replay.**
   - Both routes refuse each certificate’s six controls before its positive counts: for
     every certificate in R1, and for the 10% in R2.
   - Every positive runs on both routes.
   - The all-pairs kernel agrees at the sampled counts.
5. **The walk.**
   - `answer_problems` finds nothing to report.
   - The 66 restatements are not recorded.
   - `check --tree` holds Göbel’s member at every count.
   - `held-dependents` names each verdict that rests on a hold.
6. **The gate.** It is measured before and after W7 and in each records slice, against
   the target above.

## Rollout Plan

- **W7** is one pull request.
  It registers nothing, so it is labelled S1 and project.
- **R1 to R3** are records pull requests labelled `intake`, each with an S label by the
  runbook’s rubric. #742, #732’s rows to 1024, was S2.
- **R2’s owner step.** The owner publishes `data/mishapolk-issue732-above-1024-v1`
  before R2 merges.
- **R4** follows the answers, and each answer reruns the walk (`held-dependents`).
- **After each merge,** the stage 7 replies.

## Open Questions

### Decided by a Stated Rule

These need no owner answer before any slice.

- **D3 (335).** “Stage 3 registers what `ledger.json` records, and nothing it does not
  unless the owner names a key reason” (result-import.md, Several Reports at One Count).
  The walks leave 335 unrecorded, and nothing above 1024 depends on it.
  Naming a key reason remains open to the owner; nothing waits for it.
- **N4 (one coverage file or a split).** The frontier README says the register “records
  … relevant claims beyond n = 324” (`packing/frontier/README.md:196`–`:199`). OR-18
  counts a record as a record, not bulk data.
  Measured: about 204 bytes per row, which compresses 17.7 times, so about 52 kB as Git
  stores 4,500 rows and about 115 kB for 10,000. The load time, 0.145 CPU-seconds today,
  projects to about 0.5 s. One file, then.
  A split would cost one loader across the 12 modules that read the rows.
  The question reopens only if W7’s gate measurement fails its target.
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
    (`beyond_horizon_replay.py:51` to `:54`), and nothing in the answer’s reasoning
    depends on how many squares are deleted.
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
  think-fwa9, think-0gp6 (#732), think-jtlq (Daniel), think-cnn7 and think-ptkk (#763),
  think-cncq and think-gn29 (`43f666c`), think-zkxy, think-oqjd, think-lh7d (the cap).
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
