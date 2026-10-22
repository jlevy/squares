---
type: is
id: is-01m5h3rxsgydmfjazs3vmw05wp
title: "Import Mishapolk: 122 upper bounds at 105–1568, incl. 105 and 204 in the corpus (#719)"
kind: task
status: in_progress
priority: 1
version: 13
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
child_order_hints:
  - is-01m5h5w2snqz3h2g480xs069kb
  - is-01m5h5w3jq53jn76r07a24jpyx
hold: null
hold_until: null
created_at: 2026-10-22T06:11:32.271Z
updated_at: 2026-10-22T19:08:46.466Z
started_at: 2026-10-22T06:11:33.610Z
---
Issue #719 (https://github.com/jlevy/squares/issues/719), opened 2026-10-22T05:30:47Z by Mishapolk (Mikhail Polk; repository Mishapolk/square-packing-records): 122 claimed strict improvements at N in [105, 1568], two in the case corpus (105: 5.18e-12 below the catalogue witness; 204: 1.006e-8 below T-225, the house since #718), 112 beyond the horizon at or below 1024, 8 above 1024 (1061-1568; owner decision D1, think-f2io). Many margins are ~1e-12 (likely re-solves of existing arrangements); several are 1e-4 to 2e-3 (447, 553, 601, 652, 701). Stage 0 owner; stage 1 triage (read-only, priced) first.
blocked_on: none

## Notes

2026-10-22 c-triage-719 (stage 1 triage, read-only, against main 7359fa8b6 and PR #720
at 5286f1b69). The full working files are in the coordinator's scratchpad, triage-719/:
claim-map.md, in-corpus.md, price.md, policy.md and acknowledgement.md, with the data and
scripts beside them.

## Claim Map

**Source.**
- Mishapolk/square-packing-records@12fc46678fa8eefa3f156ff37dfffd84c8f3a580 is public and
  an ancestor of main. The head dc440a88 adds only ISSUE_SUBMISSION_122.md, which equals
  the issue body.
- There is no licence, so custody is derived-only, as for #470, #573 and #593.
- The repository is watched, so its certificates are reports from their first commit:
  1851c2c (2026-10-22T05:29:48Z) for 121 of the 122, and 12fc466 (06:05:07Z) for 447.

**The issue's three versions.**
- 05:30:47Z: 221 counts to 4035, pinned at 1851c2c, credit "Mikhail Polk".
- 05:35:31Z: the same, credit "Mykhailo Polkovskyi".
- 06:05:31Z: 122 counts. 101 withdrawn, and 366 and 447 added. Credit "Mikhail Polk".

**Reconciliation.**
- All 122 SHA-256 digests match, and every header's n is its row.
- Every 16-place print is the binary64 of the exact header side; 76 of them fall below
  it. Compare and record exact sides, rounded up.
- The files are 11.41 MB checked out and 2.23 MB gzipped.

**Verdicts, exact.** Each side was held to every earlier report: main's rows, #720's rows,
every .cert blob and index bound in the Couzo, Daniel and de Winter histories before
1851c2c, and every claim in the committed ledgers.

| Verdict | Rows | Counts |
| --- | ---: | --- |
| New, in the corpus | 2 | 105 (5.183438442e-12 below T-174), 204 (1.006359727e-8 below T-225) |
| New, 325 to 1024 | 111 | All others at or below 1024 except 366 |
| New, above 1024 (D1, think-f2io) | 8 | 1061 to 1568: below #666 and Couzo's 5a299b4 (#715) at all eight |
| Not new | 1 | 366: Couzo 4e4c8ce best/n366.cert (15 October) is 8.19e-2 below, as for #624 |

- 120 of the 121 differ from the least earlier side at 12 places. At 631, #719 is
  2.73e-13 below Couzo's 4e4c8ce and 5a299b4 certificates, and all three print the same
  12 places.
- All 121 are below Göbel's constructions (#613).
- **Supersessions on main:** 42 of #686's rows, 42 of 487b058's, 16 of #715's, 7 of
  #678's, 3 of couzo-certificates-2026-10-14's and 1 of the 8 October reports. If #720
  merges first, #670's rows at 370, 452 and 536 instead.
- **Earlier publications no row yet holds** are the nearest earlier side at 61 rows, and
  the ledger must transcribe them:
  - 4e4c8ce (think-yfoo): 18 counts, and 105.
  - 5a299b4's held re-certifications (think-fwa9): 19 counts.
  - 5a299b4 certificates no issue claims and no packet retains: 372, 409, 450, 453, 649,
    743, 810, 812, 933, 934, 990, 991 and 997. Each is below main's row by 1.1e-12 to
    6.2e-10, so each is an import of its own, with no bead yet: the sweep's "needs an
    owner" item for franciscouzo/square-packing.
  - 23aff0c root files at 370, 452 and 536.
- **Identity, sampled** (identity-sample.json; decides nothing):
  - Rows under 1e-9 re-certify the earlier packing. At 410, 535 and 631 the pairing is
    one to one, with the largest move about 2e-6.
  - Rows at about 1e-3 and more are mostly different arrangements: 447, 601, 652, 701,
    928, 932, 933, 991, 994, 996, 1061, 1128 and 1568.
- **105 and 204** (in-corpus.md):
  - 105: T-174's arrangement re-solved. One to one, largest move 0.049, turns up to 2.4°.
  - 204: the T-223/T-225 arrangement re-solved, with one square re-oriented 25.6°. Six
    squares moved more than 0.1. It does not pair with his own 13 and 14 October 204.
  - Both pass both maintained exact routes, with 6/6 controls refused, in a triage
    measurement.
  - Proposed: one register entry at V0/C0, pending adoption at both counts, with two
    `regularizations` items (of T-174 and of T-225, identity measured). Draft S2.
  - Adoption lapses 105's grid-slack view and SETTLED[204], and supersedes think-13e9's
    view, which lies 1.0055e-8 above #719 at 204.
- **Unrequested in the release.** LEGAL_VICTORIES.jsonl lists 451 counts.
  - Ten withdrawn rows are still new: 411, 451, 494, 495, 539, 540, 583, 587, 632 and 683,
    by 9.3e-13 to 1.14e-11. Ask the author.
  - Sub-print in-corpus files at 17 counts sit 1.1e-70 to 1.8e-19 below the house. Put
    them to the owner with think-fwa9; by default import none.
  - Three files fail both routes: n-133_breakthrough, n266_fresh and n275. No result; tell
    the author.
  - n204.cert, unclaimed, is 1.48e-11 below the claimed n-204.cert and valid. Ask.

## Price (price.md)

- **105 and 204.**
  - Replay of record: about 1 CPU-min (4.2 CPU-s filtered with controls, measured;
    all-pairs 24 to 59 CPU-s).
  - Review: one tbd-strong-max lane.
  - Adoption with both strong generators: 10 to 50 CPU-min.
- **111 rows at or below 1024.** About 26 CPU-min with six controls each (3 positives
  only), measured at 330, 447, 652 and 997 and modelled as 0.0215·n CPU-s. All-pairs at
  447, 652 and 997: 12 to 31 CPU-min.
- **8 rows above 1024.** About 4.4 CPU-min, measured at 1061 and 1568.
- All of it fits in minutes, so no validation bead is needed for what the issue asks. The
  optional full all-pairs (8 to 20 CPU-h) is recommended to be skipped.
- OR-18: 2.2 MB of derived facts in Git, and no data release.

**Proposed pull requests.**
- **PR-1, records(#719), stages 1 to 3.** Stacked on #720 (github-stacked-prs granted),
  which provides devtools.beyond_horizon_replay (#719 becomes a Release declaration), or
  after #720 merges. It carries:
  - the packet mishapolk-issue719-2026-10-22 and a ledger directory;
  - replays V-A and V-B;
  - the 111 rows and the 105/204 entry;
  - the requests record entry.
- **PR-2, stage 4 at 105 and 204.** Review, V3/C3, adoption and regularization; close
  think-13e9.
- **PR-3, on D1 = A.** The eight rows above 1024, with #666's and #715's.

## Owner and Author Questions

- **Owner.**
  - D1 (think-f2io) now also covers #719's 8 rows.
  - The in-corpus sub-print files (P4b) join think-fwa9's question.
  - If the owner sets a print floor for refinements, 631 falls under it (P1). Otherwise the
    rows carry 16 places.
- **Author** (acknowledgement.md):
  - the credit name: the record uses Mykhailo Polkovskyi, and the issue says Mikhail Polk;
  - per-row lineage, and the re-oriented square at 204;
  - the ten withdrawn rows;
  - n204.cert or n-204.cert;
  - the sub-print files;
  - a licence.

**Proposed child beads.**
1. "Validate Mishapolk #719 at 105 and 204: stage 4 replay and review, then adopt and
   regularize", labelled validation and result-import, with stage 4's block:
   - Claim: s(105) <= 674331486483935962030285457609/62500000000000000000000000000 and
     s(204) <= 882663895519250432/59604644775390625, Mishapolk/square-packing-records@12fc4667
     certificates/n-105.cert and n-204.cert; sqpack.verify and
     check_rational_witness_independent.
   - Run: filtered two-route replay with six controls, the all-pairs kernel's three jobs,
     two mutated certificates refused; the tbd-strong-max review; select_houses,
     adopt_houses, both strong generators at 105 and 204.
   - Cost: about 1 CPU-min of replay (measured), plus 10 to 50 CPU-min of regularization
     (receipts' 5 to 25 CPU-min a count).
   - Budget status: runnable; minutes.
   - Depends on: PR-1 registering the entry.
   - Done when: the entry is at V3/C3 with the review mapped; 105 and 204 are adopted and
     decided by both generators; think-13e9 is closed as superseded.
   - Machine note: shares the host at nice.
2. "Import Mishapolk #719: eight rows above 1024 (D1)", with blocked_on: think-f2io.
3. Under think-cyal or think-yfoo, not #719's: "Import Couzo's 5a299b4 certificates at 13
   counts no issue claims" (372, 409, 450, 453, 649, 743, 810, 812, 933, 934, 990, 991 and
   997).

<!-- Coordinator: blocked_on below is none because PR-1 can stack on #720 under the
github-stacked-prs grant. If you choose to wait for #720 to merge instead, replace it
with `blocked_on: jlevy/squares#720`. The rows above 1024 wait on think-f2io in child bead
2, not here. -->

2026-10-22 coord-intake-1021b: deferred from #720 review B (https://github.com/jlevy/squares/pull/720#issuecomment-6335921422) to this import, which is where they bite: B1 (Medium) beyond_horizon_replay.coverage_problems (:826-830) still requires each planned row to match exactly, including the 8 current #670 rows; #719 prints below #670 at 370, 452 and 536, so this import will fail --records with "the register's row is not the plan's": make coverage_problems accept a successor outside the walk (consistent with chain_problems), with a test. B2 (Low) the register notes for #678 and #715 (source-coverage.yaml:6127-6129, :7612-7616) still give the old supersession counts (57 + 2, 29; now 11 + 0 and 21): this import rewrites those sources' dated sentences; correct them then. B4 (suggestion) chain_problems prints "names X, not X" when the successor is right but the disposition is wrong: clarify the message.

2026-10-22 08:30 coord-intake-1021b: #720 merged (0281e7763). This import's records PR also carries the record edits for the four replies posted after #720 (scratchpad replies/0122d.md: apply0122d.py and the new comments.yaml beside upper-bounds-backlog-20261022). It waits on the snapshot prune PR (think-t1lk child) landing first.

2026-10-22 09:50 c-lane-719-import (WIP): branch claude/intake-2026-10-22 pushed at 650184e26 (not yet merged with main d660905ec, #578): b93126ed8 the replies after #720 and comments.yaml; 5e272e29b the packet mishapolk-issue719-2026-10-22 (derived facts, filtered replay 112/112 verified, 672 controls refused) and beyond_horizon_replay's fifth Release, walks, awaiting reports, B1 and B4; 405adf21f the ledger upper-bounds-issue719-20261022 (121 recorded, 366 not); f2f5cfac2 certify 105/204 and the all-pairs sample; 650184e26 111 rows, T-229 at 105 and 204 (V0/C0, regularizations of T-174 and T-225, measured), B2, the #719 requests entry. Next: check --replay (running), merge origin/main (#578, site v0.9.0), wait for the prune PR (think-t1lk child), re-pin, papers' record, cut v0.9.1, stamp_landed, validation, draft PR.

2026-10-22 c-lane-719-import (state at f9cee4736, pushed to claude/intake-2026-10-22, draft PR https://github.com/jlevy/squares/pull/722): stages 2-3, the replay and the release are done: main 76496462b (#721) merged at 449f65bb9, DATA_REVISION 6610be93, explainer v0.4.17 (count 229), three papers kept (68 files byte-identical twice), site v0.9.1 cut (PUBLICATION_REVISION ed8be61f), release_pin --check and check_release_impact pass; a read of Mishapolk/square-packing-records through dc440a88 in intake-watch.yaml (f9cee4736) clears the sweep. Recorded: the packet mishapolk-issue719-2026-10-22 (derived-only, 114 facts, 173 files bound to blobs, 8 above 1024 pinned by digest); beyond_horizon_replay's #719 Release (112 verified, 672 controls refused, check --replay OK; all-pairs sample at 447, 652 and 997 agrees); the ledger upper-bounds-issue719-20261022 (6 reports, 239 claims, 210 recorded); 111 rows 330-997, all current, superseding #686 42, couzo-verified-bounds-2026-10-14 39, #715 16, #678 7, couzo-certificates-2026-10-14 3, #670 3, couzo-extended-range-reports-2026-10-08 1; 366 not recorded (4e4c8ce 8.19e-2 below); 631 recorded on the exact comparison (2.73e-13 below 4e4c8ce and #715's held 5a299b4; same 12-place print), at '25.6568542495182812'; T-229 at 105 and 204 (V0/C0, pending adoption, draft S2, regularizations of T-174 and T-225, identity measured; stage 4 on think-4h23); B1, B2, B4; the replies after #720 and #719's requests entry (check_requests --github 0 differences); the merge of main d660905ec (#578) with census joins resolved. --source-bytes at f9cee4736: 262,309,736 of 267,386,880 (5,077,144 under). Next: hosted CI on #722 and the local reachable_tests run; then the coordinator's senior review and merge gate, and the acknowledgement (triage-719/acknowledgement.md, refreshed: name T-229 only once on main). Last pushed SHA f9cee4736.
blocked_on: jlevy/squares#722

2026-10-22 c-triage-1022b (read-only; coordinator scratchpad triage-1022b/couzo-residue-plan.md).

**What changes in #719's records after the Couzo history records PR.**

- `beyond_horizon_replay.WALKS[ISSUE_719].awaiting` names `4e4c8ce` (`think-yfoo`), and
  `23aff0c` and `5a299b4` (`think-tmwt`). Once the residue PR records their rows, each
  becomes a `later` source.
- These stay `Awaiting`, now on `think-fwa9`:
  - #715's 30;
  - `5a299b4`'s sub-print re-certifications at 366 and 372;
  - `23aff0c`'s deletion bound at 447 (D6).
- The walk's verdicts for #719's rows do not change.
- At 9 counts #686's rows become superseded by `5a299b4` before #719 (453, 649, 810, 812,
  933, 934, 990, 991, 997). If #719's reply on #686 says otherwise, `think-9vjn` owes a
  follow-up.

2026-10-22 c-lane-719-import: #722 head e0c612d87 (pushed, ls-remote confirmed). Since f9cee4736: results.html's ceiling moved to 1,300,000 as think-v1qe's measured choice (81762770a, reason with hosted and local timing at e0c612d87; RESULTS_ROOM_THROUGH 238; the lightening stays with think-v1qe), the three papers' record extended to site_urls.py (5a3adc744), and review A round 1 (comment 6342695333) addressed: A1 test_profile_records (81762770a, 00b9e5e7f); A2 least side per commit and count in ledger_sources, gather refuses two transcribed claims at a count, ledger re-gathered: 8 steps changed, no verdict (00b9e5e7f); A3 the issue's 11:35:16Z credit edit (Mykhailo Polkovskyi) in the requests entry (read through 11:35:16Z, name ask dropped), packet README, custody record and bibliography (1eaa8624c), T-229's claim and the source-coverage note left for stage 4 (think-4h23 note); A4 366 and 447 dated 06:05:31Z (00b9e5e7f); A5 B1 needs the successor's own later smaller row, mutant killed (00b9e5e7f); A6 custody claims only what is pinned, n105.cert named (1eaa8624c); A7 docstrings, A8 #715's 19 ties noted (00b9e5e7f). No DATA_REVISION re-pin (6610be93 stays). The reply draft (scratchpad triage-719/acknowledgement.md) now confirms the credit name instead of asking.

2026-10-22 c-lane-719-import: #727 (squaremath.org; site v0.9.1, explainer v0.4.17) merged into #722 at 5d2ee4a10 with main's release accounting; re-taken on top: DATA_REVISION 6610be93 (a9b8d8092), explainer v0.4.18 (f39b60022), three papers kept at v0.1.9/v0.1.2/v0.2.5 (7ff5b1292, 68 files byte-identical twice), site v0.9.2 (a287ece85, PUBLICATION_REVISION 7ff5b129). The branch adds no site URL, so the domain change needs nothing. Records tier 52/52; 657 site/overview/profile/release tests pass; --source-bytes 262,349,326 (5,037,554 under). Last pushed SHA a287ece85.
