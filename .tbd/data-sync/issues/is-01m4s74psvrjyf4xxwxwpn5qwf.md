---
type: is
id: is-01m4s74psvrjyf4xxwxwpn5qwf
title: "#560: merge main, calibrate T-153's V/C/S and n-017's reported lane, ready to merge"
kind: task
status: closed
priority: 1
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m4s74qsz5g062xta2zrj76mp
parent_id: is-01m4s74nyjg5a9eqhf80q4xcv8
hold: null
hold_until: null
created_at: 2026-10-12T23:28:37.691Z
updated_at: 2026-10-13T17:07:34.839Z
started_at: 2026-10-12T23:28:39.808Z
closed_at: 2026-10-13T17:07:34.838Z
close_reason: "#560 merged into main in 5584b2283 (stack 572): T-153 registered at V0/C1, S5, status reviewed; n-017's reported lane proved by the owner's decision of 13 October, verified status open; D-520 and its test; senior and correctness reviews dispositioned (B3 deferred to think-r9zt)."
resolution: null
duplicate_of: null
---
Layer 1 of the stack, PR https://github.com/jlevy/squares/pull/560. Merge origin/main (done at a55d2704b, re-pinned 5325ec843); apply the calibration audit's fixes to T-153's composition and next_rung and to n-017's priority note; keep reported_status: proved per the reported-lane rule (owner may flip); fix devtools/gap_ranking.py, which filters on reported_status and so dropped n = 17 from the open-case ranking; records and fast tiers; CI green; PR body updated with cost, validation and the final proof status.

## Notes

Layer 1 = #560, head 55aa503d6 after merging main at ea227e62d (#576) on 13 Oct; stack 572. Close when #560 merges.
