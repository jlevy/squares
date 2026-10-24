---
type: is
id: is-01m5ghp413dqrnqz5w3ww2thdd
title: "Decide Couzo's 8 October decimal poses at 335 (and 336, 337, 341, 373, 374) exactly (D3 for #715)"
kind: task
status: open
priority: 2
version: 7
delegate: coord-intake-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m5g8xj3hqca5wcen9f71dtnd
hold: null
hold_until: null
created_at: 2026-10-22T00:55:25.968Z
updated_at: 2026-10-24T05:43:59.692Z
started_at: 2026-10-22T00:55:35.613Z
---
D3 of think-f2io, and a promise of the #715 acknowledgement (https://github.com/jlevy/squares/issues/715#issuecomment-6329883508): decide exactly whether Francisco Couzo's 8 October decimal report at n = 335 packs at its printed side, 18.822875655543559 (source couzo-extended-range-reports-2026-10-08, packet packing/resources/web/couzo-extended-reports-2026-10-08, facts/n-335.yaml: decimal centres and angles, "no geometry, native replay"). The 9 October exact certificate at 335 (02f9690, retained in packing/resources/web/couzo-exact-certificates-2026-10-09; #715 restates it byte for byte) is 1.78e-11 or more above that row, so the 22 October ledger (packing/campaign/issue-intake/upper-bounds-20261022) records neither it nor #715 at 335.

The same check settles whether the 8 October rows at 336, 337, 341, 373 and 374, which the 02f9690 certificates beat by under 1.2e-11, ever packed.

Not run in the #715 import: the poses are decimal angles, so an exact decision needs an interval or algebraic route for the trigonometry (or the author's own exact rationalization), which no maintained tool runs on these facts today; that is a W7 slice, not a seconds-long check.

Done when: each pose set is decided (feasible at its printed side, or infeasible with the overlap or wall named), the outcome is recorded with its receipt, and, if one is infeasible, the owner gets a concrete correction (the decimal row to deferred-conflict with a bead, and the certified 335 made current).
blocked_on: none

## Notes

2026-10-24 c-import-732c-1024 (think-e3im, PR #769, branch claude/intake-2026-10-24-issue732-f1ceee4): decided, per the owner's answer of 24 October that the existing process decides it ("we should have clear defined process for this already, why are you asking? if it is replaced by another one, we could indicate that too").

Tool: packing/devtools/couzo_decimal_decisions.py (decide --write; check). Receipt: packing/resources/web/mishapolk-issue732-f1ceee4-2026-10-23/receipts/couzo-8-october-decisions.json (the 8 October packet refuses extra files, so the receipt sits with the release whose 335 supersedes the row). 4.6 CPU s for six counts.

Four readings per count: literal (printed centres and radian angles, outward-rounded interval arithmetic at 60 digits with decimal_pose_margins' wall and pair formulas); near-axis read as 0 (every nonzero angle below 1e-10); the printed centres with the 9 October certificate's rotations (exact, both couzo_678_replay routes; only where the certificate is the same packing, centres within 1e-6); and the 9 October certificate itself (exact, both routes).

- 335: literal NOT a packing at 18.822875655543559 (21 squares cross a wall; worst square 2 by 7.77e-16, angle -1.55e-15 rad; no pair overlaps). Near-axis 0 (196 angles: 193 binary64 roundings of zero up to 3.1e-15 and three near-axis angles 1.1e-12, 9.0e-12, 4.7e-11, exactly the certificate's zeros): a PACKING at the print, least pair separation 5.86e-14. Certificate rotations at the print: packing on both routes. Certificate (1.78e-11 larger): packing.
- 336, 337: literal and near-axis both not packings at the print (near-axis: one wall by 4.0e-16 at 336, three by 1.0e-16 at 337). 341, 373, 374: literal not, near-axis a packing. At all five the 9 October certificate is another packing below the print (centres up to 5.3e-4 away), and its rows already supersede the 8 October ones.

Disposition: no deferred-conflict and no correction. The 335 row stays as printed (a report of a packing that exists at its print, read as its certificate reads it, within one unit of the print on either reading, as the ledger reads it); Polkovskyi's f1ceee4 row supersedes it, at least 1.61e-12 below on either reading (source-coverage.yaml; the 8 October source's notes and #715's n335 entry say so). Recommend closing this bead once PR #769 merges; the coordinator closes it (lane rules: notes only).

2026-10-24 c-fix-769-1024 (think-0mz5, PR #769 review A, A2: https://github.com/jlevy/squares/pull/769#issuecomment-6380362746). Outcome, closing these notes.

- Correction to the note above: "within one unit of the print on either reading" is false for the literal reading. Read literally, square 2 crosses the left wall by 7.77e-16 and square 308 the right wall by 6.88e-16, so the literal poses need a side of at least the print + 1.465e-15 (recomputed here at 60 digits from the 8 October packet's facts/n-335.yaml), outside the span of one unit either side of the 15-place print that the f1ceee4 walk's starts.yaml reads (…543558 to …543560). Nothing moves: f1ceee4's 335 is 1.607e-12 below the print and 1.94e-11 below the 9 October certificate, so it supersedes the row on either reading.
- Couzo's own answer on #715 (issuecomment-6375833547, 2026-10-23T22:16:52Z) states the same facts: the certificate is the 8 October packing in exact form, centres dilated by exactly 1 + 1e-12 about (1/2, 1/2), the three near-axis angles (4.73e-11, 9.02e-12, 1.10e-12 rad) set to 0, the literal print overshooting a wall by up to 7.8e-16; "the bound we stand behind is the certificate's". The 9 October certificate sets to 0 exactly the 88 printed zeros and the 196 angles below 1e-10 (284 in all) and keeps the next angle, 2.40e-10.
- At 341, 373 and 374 "with those angles at 0" is this decision's 1e-10 reading, not a certificate's: the 9 October certificates at those counts (and at 336, 337) are other packings.
- Record text, in PR #769: #715's n335 not_registered (result-requests.yaml) is the review's merged text; the packet README's 335 section and the 8 October source's note (source-coverage.yaml) cite the answer. When #766 merges, #769 takes the same text into #715's n335 block and drops #766's "the row's exact side is the one the certificate gives" (the walk reads the row at its print). The #715 reply (coordinator scratchpad triage-1023b/reply-715.md, with c732/715-followup.md folded in) gives Couzo this outcome after #766 and #769 merge.
- Disposition unchanged: no deferred conflict and no correction; the row stays listed as printed and is superseded by mishapolk-issue732-f1ceee4-2026-10-23. Ready to close when #769 merges (the coordinator closes it).
