---
type: is
id: is-01m5jzpg6q6mjmf5zff98wga9e
title: Repair stale Atlas metadata and Recent Results filter tests
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-ci-tests
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-22T23:38:47.380Z
updated_at: 2026-10-22T23:42:05.354Z
started_at: 2026-10-22T23:38:57.126Z
closed_at: 2026-10-22T23:42:05.353Z
close_reason: null
resolution: null
duplicate_of: null
---
Mechanical CI follow-up in test_frontier_page.py, test_site_head.py and test_site_result_filters.py only. Preserve metadata defect detection and Added filter outcomes after the Results page split. Coordinate other owned files; no runtime changes.

## Notes

Assigned test-only changes complete: test_frontier_page expects Visual Atlas; test_site_head derives negative-fixture diagnostics from current RESULTS_META/ATLAS_META and asserts deliberate rename modifies content; test_site_result_filters renders Recent Results, captures full-window and newest-day arrival IDs before archive navigation, and exercises explicit archive added-since/day URLs now that user requested removal of Browse/Show-day links. All prior Added control/count/empty/malformed-date checks retained. Four exact CI-failing tests pass in 113.77s. Ruff format/check and git diff --check pass. Evidence: /Volumes/spud-ext2/agent-scratch/site-navigation-20261022/ci-mechanical-20df-tests.log. Root owns commit/push; no runtime files changed by this worker. Other failing assertions and nav formatting coordinated with their owners.
