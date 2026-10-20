---
type: is
id: is-01m4mx0j9pqqwhrt1awzys1ma4
title: "PR #398 A1: neither browser launch's SQPACK_CHROMIUM override is tested, and CI cannot observe it"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mx0hpjb3jb05gp9f1b5w8d
hold: null
hold_until: null
created_at: 2026-10-11T07:14:38.517Z
updated_at: 2026-10-11T07:31:41.815Z
started_at: 2026-10-11T07:14:46.685Z
closed_at: 2026-10-11T07:31:41.814Z
close_reason: "fixed in 5b43c74ca: test_both_browser_checks_launch_the_chromium_the_environment_names; fails when either launch reverts to bare launch()"
resolution: null
duplicate_of: null
---
Medium. packing/devtools/check_published_site.py workbench_startup (:1311-1313 merged tree) and forwarders_followed (:1407-1409). No test names BROWSER_OVERRIDE or executable_path; tests replace both functions whole, and CI runs with SQPACK_CHROMIUM unset. Fix: a test in tests/test_check_published_site.py with a fake sync_playwright whose launch records options and raises PlaywrightError; assert executable_path follows the variable. Review: https://github.com/jlevy/squares/pull/398#pullrequestreview-5482286271
