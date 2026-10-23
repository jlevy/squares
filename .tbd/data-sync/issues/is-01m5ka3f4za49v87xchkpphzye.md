---
type: is
id: is-01m5ka3f4za49v87xchkpphzye
title: Migrate result-filter browser fixture to canonical All Results
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-upstream-final
labels: []
dependencies: []
parent_id: is-01m5k19kqedc9vp30sk9wm3s5f
hold: null
hold_until: null
created_at: 2026-10-23T02:40:38.034Z
updated_at: 2026-10-23T02:44:01.834Z
started_at: 2026-10-23T02:40:46.999Z
closed_at: 2026-10-23T02:44:01.819Z
close_reason: At PR737 commit 67a03cb12, canonical result-filter browser fixture no longer renders retired recent-results.html. Added-date assertions inspect canonical result row IDs. Complete focused file passed 25 tests with six expected skips in 65.50s; Ruff check and format passed.
resolution: null
duplicate_of: null
---
Replace retired Recent Results fixture lookup with canonical results and compatibility-forwarder assertions in test_site_result_filters.py; preserve full filter coverage and run focused browser test file. Coordinator owns commit and push.
