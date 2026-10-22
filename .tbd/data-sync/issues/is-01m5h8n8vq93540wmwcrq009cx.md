---
type: is
id: is-01m5h8n8vq93540wmwcrq009cx
title: "Snapshot: leave 121 more unread worker outputs and three on-request import tools out of mutation workers (option b, 2026-10-22, unchanged cap)"
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: c-lane-snapshot-prune-1022
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
hold: null
hold_until: null
created_at: 2026-10-22T07:36:55.415Z
updated_at: 2026-10-22T08:10:01.566Z
started_at: 2026-10-22T07:36:59.996Z
---
main 7359fa8b6 reads 231,655,578 B and open #720 232,400,158 B against SNAPSHOT_MAX_BYTES 232,783,872 (222 MiB, unchanged); #719's records (~0.5-0.8 MB) would cross it. Apply option (b) as #714 did: set A (121 entries, 4,782,231 B: regularized-drawing run evidence and selection data, regularized-bound views, the 14 October lane-claim copies and comment drafts, n17-20261008, two manual-source receipts, nine house-adoption prior-state receipts, ds7 lower-bound audit, author-checker profile timings/attribution) into UNREAD_WORKER_OUTPUTS, and set D on main (couzo_715_replay + test_upper_bound_reports_715, decide_undecided_comparisons, register_couzo_followup_report and their tests; 112,532 B) into ON_REQUEST_IMPORT_TOOLS, with a dated note. Evidence: --source-bytes before/after, --audit-snapshot --prune-candidate, 50-command --baseline with and without, 174 controls at -j 2, the worker tests, release records. Not in scope: think-d2he's stub copy-back, sets B and C, beyond_horizon_replay (#720 only), the cap.

## Notes

2026-10-22 07:58 c-lane-snapshot-prune-1022: worktree scratchpad/wt-views, branch claude/stoic-thompson-ku09fw from 7359fa8b6. Local commit ef71596d5 (not pushed): UNREAD_WORKER_OUTPUTS +121 entries (599 files, 4,782,231 B), ON_REQUEST_IMPORT_TOOLS +6 (112,160 B), dated note, ReleaseNoPublicChange, muglich test subset check. Selector diff vs main: exactly those 605 files leave. Audit on main: 0 mentions, 0 rescues. --source-bytes 231,655,578 -> 226,772,979.
2026-10-22 08:12: at ef71596d5: 50-command --baseline main vs head: 23 identical, 26 times only, 1 differs (check_no_embedded_js reads 1885 -> 1879 Python files, same verdict); four reds identical; no timeouts. run_negative_controls -j 2: 174 fire (9m58s). snapshot_copy_roster+link_consumers+muglich: 23 passed. #720 merged as 0281e7763: next merge origin/main, add beyond_horizon_replay pair if evidence holds, re-measure, re-audit, re-run baselines and controls at the new head, tests, tiers, push, draft PR.
