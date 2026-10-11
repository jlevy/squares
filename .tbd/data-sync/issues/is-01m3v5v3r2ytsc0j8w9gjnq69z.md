---
type: is
id: is-01m3v5v3r2ytsc0j8w9gjnq69z
title: "check_pr_wall: a partial re-run on an advisory workflow should report NOT JUDGED and pass"
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-10-01T07:28:41.711Z
updated_at: 2026-10-06T08:28:48.586Z
closed_at: 2026-10-06T08:28:48.586Z
close_reason: "Done on main: 5457d7de0 (from PR 376) makes check_pr_wall report a partial re-run as NOT JUDGED and exit 0. PR 377 made wall ceilings and the per-test rule advisory on pull requests."
resolution: null
duplicate_of: null
---
packing-required fails any partial re-run because the jobs API mixes attempts (check_pr_wall.py measure, exit_status), so re-running only the failed jobs can never turn a PR green. Recommended by the 2026-10-01 CI review (think-53a2): on an advisory workflow, report NOT JUDGED and exit 0 for a partial re-run, and keep fail-closed for every other unmeasurable state. Also: the checks tier 140 s ceiling is tight (slowest green reading 137.1 s), and the per-test call-time backstops trip on the slow fleet for the same reason.
