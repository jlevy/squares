---
type: is
id: is-01m2e0e4ct972w6eapcr8c3xjz
title: Publish the PR156 draft checkpoint with exact local gates and final hosted CI
kind: task
status: in_progress
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: codex@spud10.local
labels:
  - n11
dependencies:
  - type: blocks
    target: is-01m2csyyq4nzfqppqj639avs51
parent_id: is-01m2ctdap5jwdr8h4qb8dxwt8z
child_order_hints:
  - is-01m2e7adq6sc2j6mzgsx89sg8h
hold: null
hold_until: null
created_at: 2026-09-13T18:28:24.089Z
updated_at: 2026-09-13T20:28:42.596Z
started_at: 2026-09-13T18:35:26.795Z
---
Review and commit durable reviews, run-sheet status, records, and accepted source changes; reconcile origin/main with the merge-upstream shortcut; run required push gate; push PR156 as draft; update body with unique cost, exact head, admitted/refused contracts and remaining gates; wait for final hosted CI and sync beads. Do not mark ready while coordinator and run-sheet admission remain refused.

## Notes

PR156 clean local head 9c56e901 includes final formatted run-sheet blob 29517a3f; records 32/74, edit 45/74, 1165 docs and diff check pass; origin/main d507f5c7 remains an ancestor. First --push attempt stopped at collection in 58.56s because macOS Cairo loader path was absent; development.md prescribes DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib and import was verified. Corrected --push on the same clean head ran 1292.99s and FAILED its reachable behavioral tests step; output was truncated by the terminal response, so the exact failure is not yet established. Disk was at 101 MiB and pytest had no usable temp directory during the run; free space recovered to 838 MiB after the gate exited. An old lastfailed cache listed a calibration reader test and atlas import; the reader test now passes 6/6, so it does not identify the current failure. A standalone reachable rerun with --maxfail=1 and local captured output is active. No push, PR body update, or hosted CI on 9c until a genuine --push pass. Independent exact-head source composition review accepts the scoped 9c blobs and 23-path closure, but operational profile admission remains pending remote identity, table disposition, and positive runs.
