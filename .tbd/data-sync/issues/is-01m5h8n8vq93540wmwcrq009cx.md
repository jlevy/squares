---
type: is
id: is-01m5h8n8vq93540wmwcrq009cx
title: "Snapshot: leave 121 more unread worker outputs and three on-request import tools out of mutation workers (option b, 2026-10-22, unchanged cap)"
kind: task
status: closed
priority: 1
version: 11
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: c-lane-snapshot-prune-1022
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
hold: null
hold_until: null
created_at: 2026-10-22T07:36:55.415Z
updated_at: 2026-10-22T11:10:59.544Z
started_at: 2026-10-22T07:36:59.996Z
closed_at: 2026-10-22T11:10:59.544Z
close_reason: "Merged as #721 (76496462b, 22 Oct 11:10Z). Review A approve-with-nits; A1 deferred to think-wtso, owner note think-cmbx. main at 261,568,999 B, 5,817,881 under 255 MiB."
resolution: null
duplicate_of: null
---
main 7359fa8b6 reads 231,655,578 B and open #720 232,400,158 B against SNAPSHOT_MAX_BYTES 232,783,872 (222 MiB, unchanged); #719's records (~0.5-0.8 MB) would cross it. Apply option (b) as #714 did: set A (121 entries, 4,782,231 B: regularized-drawing run evidence and selection data, regularized-bound views, the 14 October lane-claim copies and comment drafts, n17-20261008, two manual-source receipts, nine house-adoption prior-state receipts, ds7 lower-bound audit, author-checker profile timings/attribution) into UNREAD_WORKER_OUTPUTS, and set D on main (couzo_715_replay + test_upper_bound_reports_715, decide_undecided_comparisons, register_couzo_followup_report and their tests; 112,532 B) into ON_REQUEST_IMPORT_TOOLS, with a dated note. Evidence: --source-bytes before/after, --audit-snapshot --prune-candidate, 50-command --baseline with and without, 174 controls at -j 2, the worker tests, release records. Not in scope: think-d2he's stub copy-back, sets B and C, beyond_horizon_replay (#720 only), the cap.

## Notes

2026-10-22 07:58 c-lane-snapshot-prune-1022: worktree scratchpad/wt-views, branch claude/stoic-thompson-ku09fw from 7359fa8b6. ef71596d5: set A (121 entries, 599 files, 4,782,231 B) into UNREAD_WORKER_OUTPUTS, set D (3 tools + tests) into ON_REQUEST_IMPORT_TOOLS, note, ReleaseNoPublicChange, muglich test subset check. At ef71596d5: baselines 23 identical/26 times/1 scanner count; 174 controls fire (9m58s).
2026-10-22 08:45: merged origin/main (#720, 0281e7763) as ec9a04d09; 2d1612630 adds beyond_horizon_replay + test (set D now 8 files, 170,410 B) and re-measures the note. At 0281e7763 vs this tree: selector diff removes exactly 607 files, 4,952,641 B, adds none; audit 0 mentions/0 rescues/no zero entry; baselines 23 identical, 25 times only, exact verification +1 wall-paced progress line, check_no_embedded_js 1887->1879 files same verdict; four reds identical; no timeouts. --source-bytes 232,414,111 -> 227,473,806 (5,310,066 under 222 MiB). Tests: test_negative_controls+snapshot roster+link consumers+muglich 195 passed; four worker-test modules 131 passed (incl. 5 slow). records tier --jobs 1: rc 0 (52 tier steps). release impact + pin pass. NOT PUSHED YET (remote still 7359fa8b6). Running: 174 controls at 2d1612630. Next: push tier, push, draft PR, hosted CI.
2026-10-22 09:12: pushed 2d1612630 (ls-remote confirmed); draft PR #721 with S2 label. 174 controls fire at 2d1612630 (9m49s). push tier --jobs 2: 66/67, reachable behavioral tests timed out at 900 s (57%) with 2 unnamed failures before the cutoff; fallback reachable_tests --since origin/main --run -n 2 running. Next: name the 2 failures, update PR body, watch hosted CI.
2026-10-22 09:45: reachable_tests --since origin/main --run -n 2 at 2d1612630: 10,809 passed, 642 skipped, 1 xfailed, 4 failed (30m09s); all four fail alone with main's copies too (two fixed_core_packet reaping tests; two test_site_column_measurement tests, no Playwright chromium on this host). Hosted at 2d1612630: 31 pass, 28 skipped, 0 fail; runs 39753058475 (Packing validation), 39753058392 (Certificate page), 39753010310 (Branch mergeability) success. PR #721 body updated; draft, S2. Bead left in progress for the coordinator (merge, then close).
2026-10-22 10:20: main moved: #578 (d660905ec) raised the cap to 255 MiB, site v0.9.0, main 266,509,045 B (877,835 headroom). Merged as 4aaef4e9d (no conflicts; cap kept). At d660905ec: audit 129 candidates 0 mentions, 0 inline/result/contributor rescues, no zero entry; selector diff exactly 607 files, 4,952,641 B. Baselines d660905ec vs head: 23 identical, 26 times only, check_no_embedded_js 1910->1902 same verdict; reds identical. Tests: roster etc. 199 passed; four worker modules 131 passed. Release impact + pin (6a8c9033) pass. e6a1e0260: note re-measured, 261,568,999 B (5,817,881 under 255 MiB). LOCAL ONLY; remote still 2d1612630. Running controls -j 2 at e6a1e0260; next records --jobs 2, push, CI, PR body.
2026-10-22 10:25: controls -j 2 at e6a1e0260: 174 fire (11m55s, load 8-10). records --jobs 2: rc 0, 52 steps, 147 s. Pushed e6a1e0260 (ls-remote confirmed; main d660905ec is an ancestor). PR #721 body updated; hosted CI running.
2026-10-22 10:40: hosted at e6a1e0260: 31 pass, 28 skipped, 0 fail; runs 39762359509 (Packing validation), 39762359319 (Certificate page), 39762356265 (Branch mergeability) success; MERGEABLE/CLEAN. PR body updated. Bead left in progress for the coordinator (review, merge, then close).
