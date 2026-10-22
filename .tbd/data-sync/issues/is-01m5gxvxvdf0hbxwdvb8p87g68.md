---
type: is
id: is-01m5gxvxvdf0hbxwdvb8p87g68
title: "PR #718 review B follow-ups (B1-B7): stale 229 prose, a test for adopt_houses._retained_672, 227 credit wording, n-103 commas, _walls sentence, two wordings, t-180 budget runway"
kind: task
status: in_progress
priority: 2
version: 6
delegate: coord-intake-1021b
labels:
  - records
dependencies: []
parent_id: is-01m5frzavxzvcqht1tf2edbfxp
child_order_hints:
  - is-01m5gzb8s9yjdr07syqkeq2v6g
hold: null
hold_until: null
created_at: 2026-10-22T04:28:19.181Z
updated_at: 2026-10-22T06:29:15.480Z
started_at: 2026-10-22T04:28:20.142Z
---
Review B of #718 (https://github.com/jlevy/squares/pull/718#issuecomment-6332701148, follow-up round 2 at c3ede79e2) found 7 Low items, deferred to the next records change (PR-B on claude/intake-2026-10-22, think-2vjc/think-f28n/think-pvav):
B1 results.yaml prose still describes 229 before #718: T-196 notes (:27625 'at 229 the case keeps T-199', :27611 'the case's ceiling'), T-198 notes (:27818 'houses the count'), T-199's and T-223's adoption sentences (:27938, :30585) should say T-225 replaced them on 22 October.
B2 add a unit test for adopt_houses._retained_672 plus assertions on n-229's body (check() reads front matter only).
B3 T-225's claim (results.yaml:30801-30807) and the packet README (:242-248) list 227 among 'Francisco Couzo's' packings; align with CREDITS[227] (de Winter's packing as refined in Couzo's #672 report).
B4 the doubled comma at n-103.md:239 and :418 (history text from the 11 October pass).
B5 _walls changed 'and every pair by at least' to 'and every pair clears by at least', differing from 52 recorded atoms; restore or migrate with a test.
B6 'is the house since' -> 'has been the house since' in T-227's claim and next_rung; n-227 '#672 report, reported in'.
B7 record the t-180 page budget's runway (450,000 against 402,418 at #718; ~1.5 KB per result, ~32 results) and name the bead that owns it.
blocked_on: none

## Notes

2026-10-22 c-lane-pr-b (PR-B, commit d045c4b93): B1 T-196/T-198/T-199/T-223 notes dated (T-225 replaced them on 22 October); B2 test_the_statements_that_672_was_not_retained_become_history (adopt_houses._retained_672 plus n-229 body asserts); B3 T-225's credit sentence and the evand-regularized README credit 227 as CREDITS[227]; B4 n-103.md commas; B5 _walls restores "and every pair by at least" in the all-clear branch, with a test against the 52 atoms; B6 T-227 "has been the house since" and the certificate-section writer says "published" after a credit ending in "report" (n-227.md too); B7 the t-180 budget reason records the runway and names think-v4me (new child bead owning it). Not closed here: think-v4me is an open child.

Branch claude/intake-2026-10-22 (from main 7359fa8b6). Commits: 9f5d9867a (packets, devtools.beyond_horizon_replay, receipts, records, tests), 8375ca986 (ledger upper-bounds-backlog-20261022), 15b885a9d (coverage rows, atoms, credit, intake-watch), 95a75d321 (requests; replies after #718 and #643; quoted scalars), d045c4b93 (review B of #718, B1-B7), b8045210c (views), e6d65154f (suite cost admission), cfeb44cc8 (DATA_REVISION re-pin).
Replay: all 205 rows (666: 11, 670: 72, 672: 44, 675: 78) verified on both maintained routes, all 1,218 controls refused by both; 282.8 positive CPU s, 1,305.5 s wall on 2 workers (2,604 row-s); all-pairs kernel at 464/922/996/998 agrees exactly (1,525,010 pairs, 649.2 CPU s); every side below Goebel; every certificate first committed at its issue's pin (de Winter at b9cdc16b).
Ledger: 432 claims at 124 counts, all recorded, none undecided; starts frozen at 804eff369; recomputed against main 7359fa8b6, no verdict changed from the triage.
2026-10-22 05:55Z c-lane-pr-b: draft PR https://github.com/jlevy/squares/pull/720 (label intake), last pushed head 5ab83974e9445e3da671a72c9c2defe9fdd5957a (ls-remote confirmed), after the release commits cfeb44cc8 (DATA_REVISION b8045210), cadf73fd9 (papers' record), 5ab83974e (site v0.8.20). Next: local --push tier running; hosted CI; then report to the coordinator. Verdict comment drafts: scratchpad replies/verdicts-prb/ (intake_comments --check passes).
2026-10-22 06:31Z c-lane-pr-b: PR https://github.com/jlevy/squares/pull/720 (draft, label intake) last pushed head 0b09ac278b400b6a67b9497f1494b0d43b1b87a0 (ls-remote confirmed). Hosted CI at 5286f1b69 (run 39730271004) failed suite-a, suite-b and suite-d on three stale statements, fixed in 9efff7252: the overview's other-projects card for joostdewinter.github.io and T-196's card (T-225 the house at 227 since 22 October); the house writer's historical() makes review B4's comma repair at 103; #715's test and packet README count the ten backlog rows #715's rows also supersede (#666 at 509, #670 at 866 and 925, #672 at 750, #675 at 547, 807, 809, 864, 923, 931). 0b09ac278 extends the papers' no-public-change record (re-rendered at link revision b8045210 from 9efff7252: the same 68 files; DATA_REVISION stays b8045210). Hosted at 0b09ac278: Packing validation 39732884021, Certificate page 39732883974 and Branch mergeability all pass. Local packing-validate --push (started at 5ab83974e): 66/67 steps; 18,867 passed, 8 failed = those four tests plus four known host-only (two fixed_core_packet reaping, two test_site_column_measurement). --source-bytes 232,400,158 (383,714 under the cap). Next: the coordinator's review and merge of #720 (S2 proposed, not applied); then the verdict comments drafted in scratchpad replies/verdicts-prb/. Review B4 is now also in the writer (adopt_houses historical()), so n-103's body stays the writer's output; think-v4me (t-180 runway) stays an open child, so this bead stays open.
