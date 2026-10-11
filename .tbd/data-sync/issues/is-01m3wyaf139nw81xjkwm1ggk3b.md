---
type: is
id: is-01m3wyaf139nw81xjkwm1ggk3b
title: "Import wand125: 34 rectangle-density lower bounds raised since T-046 (#281)"
kind: task
status: closed
priority: 2
version: 15
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
delegate: claude-code@vm
labels:
  - packing
  - result-import
dependencies:
  - type: blocks
    target: is-01m3yrzkz80qd1wv5sjr0kkkv0
parent_id: is-01m3yrdxte02c7bnygkke34ct4
hold: null
hold_until: null
created_at: 2026-10-01T23:55:45.056Z
updated_at: 2026-10-06T17:02:03.095Z
started_at: 2026-10-05T03:21:48.223Z
closed_at: 2026-10-06T17:02:03.095Z
close_reason: "Done and on main via #382 (d087422ed); reply posted 2026-10-06 and recorded"
resolution: null
duplicate_of: null
---
Result import process from stage 1. New lower-bound entry for the 34 counts, under a key for the 1a25a5e release; T-046 keeps its claim. Needs a third Packet in audit_wand125_rectangles and a third Registration in apply_wand125_rectangles. Complete replay 148.5 upstream CPU-h, about 230 worker-hours here. Land the 21 stranded receipts first (think-0rrj, think-20mv): 14 are of certificates this issue raises and all 21 still beat the verified bound.

## To finish (validation backlog, 2026-10-02)

T-068 (34 raised rectangle bounds, V0/C1). Per count, on runners: `.venv/bin/python3 -m devtools.audit_wand125_rectangles --packet 2026-10-01 --replay --n N --workers W --out DIR`, then `--merge DIR...` into resources/web/wand125-rectangle-certificates-2026-10-01/receipts/replay and `--check`, controls with `--control --n N`, then apply_wand125_rectangles. Expected CPU: 148.5 CPU-hours at the source; about 158 CPU-hours here for the 30 certificates left after dominance. Refutes: verify.cpp refusing a direction, or an input digest differing from the upstream run's; that count is recorded with replay_status failed. Moves the rung: each passing count is registered again as replayed (T-045 and T-070 precedent) and T-068 derives V3/C3 when all 34 pass. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.

## Notes

2026-10-01: stages 2 and 3 are in draft PR jlevy/squares#292 (branch claude/import-2026-10-01-requests, commit 2b7191461), stacked on #290. Stage 4 not started. The T-id was provisional then, and was quoted to no author before #292 merged on 2026-10-03.

2026-10-02 (PR #298): the 21 stranded receipts (b02,b04,b07,b08,b09) merged by audit_wand125_rectangles --merge (commit f5003d1da); apply raises the verified bound at 34 counts; register update in progress. T-068 replays: 30 certificates after dominance (66, 86, 87, 90 skipped if F/G verify), ~158 CPU-h; batch launch waits on the speed-up lane P1. Review docs/project/reviews/review-2026-10-02-wand125-rectangle-bounds-t068.md: no defect.

2026-10-05 (intake triage, think-nkzt): #292 and #298 merged on 2026-10-03, so stages 1 to 5 are on main.

- The 29 replayed certificates are T-074, at V3/C3 over 31 counts.
- T-068 stays reported, at V0/C1. Its next_rung says it has nothing of its own: the four counts no replay carries, n = 66, 86, 87 and 90, are held above these certificates by the source's mixed certificates (T-069, T-071), which were replayed.
- #281 was answered on 2026-10-03 (issuecomment-5972354358) with T-074 confirmed and T-068 reviewed.

What is left is one decision for the owner, because #281's close_when needs T-068 confirmed or refuted at all 34 counts, and the register says no replay is planned. The owner can either budget a replay of rect_n66_L8385, rect_n86_L9365, rect_n87_L941 and rect_n90_L95775 (verify.cpp at 201 directions, measured in CPU-hours: the 30 of 2 October took about 143 hours of wall), or accept T-068's next_rung and change #281's close_when to match. Another lane owns #281's entry, so its close_when is unchanged here. The reply on #281, think-pmxk's, follows from that decision.

2026-10-06 (lane R5 of the 6 October intake, think-wyf4; branch claude/ecstatic-pascal-pothtx-r5, not pushed): T-068 confirmed at all 34 counts, V3/C3 derived by check_results, independently re-implemented. Route: the sqverify-fast census rows of 3 October (all 34 VERIFIED at 201 directions, source 9985c465 = 4ddf37d9c, binary b7581bb2, 107-339 CPU-s each) plus format T control receipts of 6 October on main's crate d97758bb (binary 567a0fd5), all CONTROLS_REFUSED. sqverify_fast_census gained --control/--evidence for format T (cb1b4b88d); control point = least-bound leaf centre of least exact capture (rect_n87_L941's least-bound direction left the 99/100 mutant verifying). Separately prompted review docs/project/reviews/review-2026-10-06-sqverify-fast-format-t-route.md accepts with conditions; FT-1..FT-7 handled, FT-8..FT-11 notes. 34 evidence entries E-nNNN-wand125-rect-*-sqverify-fast-replay. No verified bound moves. Commits cb1b4b88d, 942473b60, pin 64826689a. Close condition of #281 met: T-068 confirmed at all 34 counts; the replayed entries are T-074 (29, verify.cpp) and T-068 itself (34, sqverify-fast). Optional source-checker replays of the four (n66, 86, 87, 90): think-j0dd. Lane bead: the coordinator closes.
