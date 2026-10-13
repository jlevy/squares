---
type: is
id: is-01m4s74psvrjyf4xxwxwpn5qwf
title: "#560: merge main, calibrate T-153's V/C/S and n-017's reported lane, ready to merge"
kind: task
status: in_progress
priority: 1
version: 4
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
updated_at: 2026-10-12T23:53:06.998Z
started_at: 2026-10-12T23:28:39.808Z
---
Layer 1 of the stack, PR https://github.com/jlevy/squares/pull/560. Merge origin/main (done at a55d2704b, re-pinned 5325ec843); apply the calibration audit's fixes to T-153's composition and next_rung and to n-017's priority note; keep reported_status: proved per the reported-lane rule (owner may flip); fix devtools/gap_ranking.py, which filters on reported_status and so dropped n = 17 from the open-case ranking; records and fast tiers; CI green; PR body updated with cost, validation and the final proof status.

## Notes

Layer 1 = https://github.com/jlevy/squares/pull/560 (branch claude/wizardly-meitner-wqn4x3-k17-records), bottom of GitHub stack 572. Main merged at a55d2704b; calibration fixes c8a61cc1b, gap_ranking e5759d96f, re-pin 813a8181f (hosted CI green), usage rollup 2b08364ce. Audit kept V0/C1, reviewed, S5; reported_status proved kept with the owner's alternative stated in the PR.
