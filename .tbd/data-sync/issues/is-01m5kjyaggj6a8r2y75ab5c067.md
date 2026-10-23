---
type: is
id: is-01m5kjyaggj6a8r2y75ab5c067
title: "Tracker audit 2026-10-23 part c: open and in-progress result-import beads (scratchpad audit/part-c.txt)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-audit-c-1023
labels:
  - audit
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T05:15:06.640Z
updated_at: 2026-10-23T05:31:00.153Z
started_at: 2026-10-23T05:15:07.669Z
---

## Notes

# Tracker audit, part c (c-audit-c-1023, review bead think-lrg9), 2026-10-23

68 beads, read-only. Sources: `tbd show` of each bead; `gh` issue and PR states, plus the
last comments on open issues; `origin/main` 44df28b07 (records identical to the checkout
31584003e); `check_requests --report` and `--backlog`; and `check_bead_tree.deferrals()`,
`regularization_deferrals()` and `adoption_deferrals()`, which list each bead the records
name as a live deferral. Rows: `result-c.tsv`.

## Counts by primary class

| Class | Count | Of which STALE-CLAIM |
| --- | --- | --- |
| DONE (close) | 21 | 2 (nj7h, wnsv); 4 more need a record edit first (hd6a, pvav, 6wtz, 8o5j) |
| SUPERSEDED | 2 | - (455r by the 20 Oct review; chgb by think-jh4w) |
| ACTIONABLE | 23 | 13 |
| WAITING-OWNER | 10 | 4 (qik6, ribz, qag2, phyb) |
| WAITING-COMPUTE | 6 | 1 (nqnl) |
| WAITING-EXTERNAL | 1 | 1 (xu4d) |
| STALE-CLAIM only (parent or epic, no own step) | 3 | 3 (zb5w, hg5s, e2sz) |
| UNSURE | 2 | - (lh7d, ve84: hand-kept ledgers that `check_requests --backlog` may replace) |

24 beads are `in_progress` under ended delegates: claude-code@vm, codex@spud10.local,
claude-code@spud10.local, user-eb-*, lane-new, lane-680, c-lane-692, c-lane-715-import,
ecstatic-edison-coordinator, claude-coordinator-014zkp7r, codex-intake-shared-reply-20261019.
The brief does not count coord-intake-1021b among the live lanes, so its beads are listed
as stale here too. think-cyal was written to at 02:26Z today by a 22 October lane; for it
the proposal is a reassignment to coord-intake-1023, not a reopen.

**Close now (DONE, no record edit):** rvv7, 30n2 (after closing 2jzy and reparenting
nhsd/adgd), mdnn, xik9, mu5v, e1u5, 2jzy, 3mry, qdcc (after its children), 5ij2, 8xr0, w77y,
h8jm, 115j, ql4v, nj7h (after reparenting 2d7f), wnsv (after reparenting); superseded: 455r,
chgb.

**Close with a records change:** hd6a (#624) and pvav (#675) were closed on GitHub at 03:54Z
today but are still open in `result-requests.yaml`. 6wtz, 8o5j and phyb are still named by
intake-watch reads of evand/square-packing (5ad0069, 757b40b, 7d1407a).

## ACTIONABLE, by value

1. **think-f40c**: run the C3 censuses of T-200 to T-217. The owner authorised all 18 on
   17 October ("All 18, autonomously"). 14 rows are open, at 0.62 to 21.73 CPU-h each and
   about 78 CPU-h in all. Start with the five under 1.2 CPU-h. Needs CPU and runs in
   batches.
2. **think-ot5c**: write the algebraic house writer slice (a PR of hours), then about
   2.0 CPU-h for ten counts. It unblocks 18 staged adoptions.
3. **think-8kx2 + think-0lu6**: re-run the source checkers on the four certificates
   (about 1 CPU-minute) and edit the #669 and #674 request notes. One small records PR closes
   both beads.
4. **think-f28n / think-2vjc**: post the final comment and close #670 and #672; both report
   closeable. Minutes. This is probably already in scope of the live close-issues lane
   (think-5ip2).
5. **think-0arj**: T-192 C3, about 13.3 CPU-h (6.7 h wall at 2 threads). It needs no code
   and fits the cap. Schedule it when the host is quieter (load about 9.9 now).
6. **think-kjd7**: import s(42) >= 2749/400 at stages 2 and 3 (hours), then a census of
   about 15.2 CPU-h.
7. **think-jh0n**: stages 2 and 3 for #643 (ValidTilt9 Lean): retain and register at V0,
   hours, no CPU.
8. **think-2d7f**: re-priced at about 1.2 to 2.4 CPU-h on the filtered route; needs a
   `beyond_horizon_replay` declaration for 487b058. Its value is low because all 296 rows
   are superseded.
9. **think-v860**: fix the intake_ledger bound read, 1 to 2 h. **think-0b6l**: give #678's
   packet an import declaration (hours). **think-dquu**: reconcile the five unmerged
   serene-hopper commits and fix the build_known_best_atlas attribution (about 1 h).
10. **think-lrvl**: adopt_houses writes "Earlier house" (1 h). It touches every adopted case
    record, so run it after #742, the #719 branch and #731.
11. **think-5klg** (rectangle-container route) and **think-8eo1** (`continuous_pose_followup
    replay`): W7 code slices, a PR each.
12. **think-rx26**: an exact route for the decimal poses (a W7 slice), or ask Couzo for his
    rationalization. **think-z6aj**: measure the n=17 row-3 view (minutes; question below).
13. **think-57ei, think-ahr2, think-f8py, think-pf37, think-7l2j**: Lean formalization
    imports at stages 1 and 2 (hours each, no CPU). Do one Ryu packet for ahr2, f8py and
    pf37 together.

All code and records items can run in parallel with #742 and #736. Items that touch
`beyond_horizon_replay`, `result-requests.yaml` or case records should follow the #719
records branch `claude/intake-2026-10-23`, which is not yet on origin.

## Owner questions

- think-wu73: run wand125's interval-24 subset (about 22.4 CPU-h)?
- think-yeq9: if the filtered-route re-price comes in under the cap, release the hold and
  host the 23 MB of composites?
- think-dyyu / think-f2io: are recipe-only rows recorded at all?
- think-zn7s: budget for the 190 CPU-h pass. think-ojr9: a machine with 32 GB or more.
  think-nqnl: budget and a machine for the roughly 340 CPU-h sq19 build, or the 1 to 3 CPU-h
  subset.
- think-eucc: is zmx2 --full a required second route for T-191's C3?
- think-ribz: Q16, does a depth-12 refusal count as a zm_mixed.py control?
- think-qag2: l3oo decision 6, is #575 recorded at 176?
- think-phyb: ask the dropped 207 question on #639?
- think-a4x3 / think-xik9: post the five s(19) author questions (question 5 reworded)?
  Create an n-19 label (none exists)?
- think-8ido: Q2, is a square turned at its centre the same packing?
- think-z6aj: does the 13 October n=17 suspension cover upper-bound certificates?
- think-dquu: S2, may a sample that decides no count be cited by its result?
- think-a95t: confirm or reverse the default for structured credit at 308, 236 and 270.
- think-g0o4: credit #573's 153 and 207 as new arrangements or as PingYou Ltd's packings?
- think-qik6 / think-cyal: think-fwa9 (the sub-print class, O1) and think-f2io (above 1024,
  743/985 as O2, hosting).
- think-2d7f: is the replay of 296 superseded rows still wanted?

## UNSURE

- think-lh7d, think-ve84: keep the hand-kept backlog ledgers, or retire them for the
  generated `check_requests --backlog`?
- think-g0o4: `result-requests.yaml` does not yet name it on main. The live lane
  think-5ip2 is expected to add it; this audit did not check its branch.
