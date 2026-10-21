---
type: is
id: is-01m5fabgy98ffjkatr3ggrh4xg
title: "Snapshot: extend UNREAD_WORKER_OUTPUTS with 223 unread historical outputs (option b, unchanged cap)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: c-lane-snapshot-prune
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T13:28:04.297Z
updated_at: 2026-10-21T14:15:54.532Z
started_at: 2026-10-21T13:28:09.142Z
---
main 51ac9d7ee reads 232,783,862 B, 10 under the 222 MiB cap; #712 (+17,031), #704 (+139,378) and #706 (+167,357) cannot land. Read-only analysis (scratchpad/snapshot-analysis.md, set C in snap/data-final.txt) finds 223 historical outputs in packing/campaign and packing/benchmarks (2,974,471 B) that no control reads, the class UNREAD_WORKER_OUTPUTS already covers. Extend it under the unchanged cap with the traced evidence the #464/#692 entries record (all 174 controls fire mutated; the 50 distinct commands print the same unmutated output with and without them), and a dated comment. Not in scope: the 39 on-request tools (a new family, the owner's assent), the atlas-print fonts (read by test_emission_precision), and the cap.

## Notes

2026-10-21 c-lane-snapshot-prune: branch claude/snapshot-unread-outputs-2026-10-21 (worktree scratchpad/wt-prune from 51ac9d7ee). Pushed 3763cbb9e: UNREAD_WORKER_OUTPUTS gains the 223 set-C files as 8 directory entries and name groups; an in-memory check shows the entries prune exactly snap/data-final.txt (223 files, 2,974,471 B, no other file). --source-bytes 232,783,862 -> 229,821,817 (2,962,055 under 222 MiB, comment counted). Baseline with entries running; controls, baseline without, tests and validation pending.
2026-10-21 13:58 c-lane-snapshot-prune: tests/test_negative_controls.py failed 3 with the full 223: it pins exp-140-owner-footprint-cover.json (canonical twin of a 2026-10-07 pruned stdout) and Session 105's fast-cpu4/fast-native source identities as present in workers. Those 3 (68,240 B) are excluded beyond the analysis: 220 files, 2,906,231 B (03f11bd87). In-memory --audit-snapshot of the 193 entries against main's selector: 0 mentions, 0 inline/result rescues, net == copied for every entry. Release: one ReleaseNoPublicChange (4 papers + site, run_negative_controls.py, the think-b6ir import-path argument); check_release_impact --baseline-ref origin/main passes, release_pin --check passes (eedeaf5bd). --source-bytes at eedeaf5bd: 229,891,287 (2,892,585 under 222 MiB). Baseline with entries (main tree) done; baseline without, controls and validation pending.
2026-10-21 14:25 c-lane-snapshot-prune: 50-command --baseline with the entries (main tree, 232,783,862 B) and without them (03f11bd87, 229,889,861 B): 24 byte-identical, 26 differ only in wall times and the preflight lease timestamp, 0 other differences; the same four red in both (full suite 3, validate_schemas 1, operating-rules append 1, test_change_scoped_selection 1). run_negative_controls -j 2 at eedeaf5bd: 174 fire as expected (8m51s). packing-validate --records --jobs 2: 52/52 tier steps passed (123 s). --push running; then the draft PR.
