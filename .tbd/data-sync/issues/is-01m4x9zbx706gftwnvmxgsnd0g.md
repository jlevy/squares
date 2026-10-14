---
type: is
id: is-01m4x9zbx706gftwnvmxgsnd0g
title: Keep remaining browser arrivals and forwarder checks within measured test calls
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-14T13:35:06.149Z
updated_at: 2026-10-14T13:35:20.644Z
started_at: 2026-10-14T13:35:20.642Z
---
Actual enforced full38565361504/e709 has three browser/site CALL overruns: published_forwarders[False]14.13s, each_old_address query+fragment13.67s, overview writes/checks12.51s. Preserve all18fileURL variants,18HTTP script/no-script variants, real render and CLI write/check plus every corruption/restoration assertion. Split independently measured arrivals and reuse only an immutable production-generated routing inventory in the output-mutation controls; no eagerhidden construction, skipped coverage, marker/workflow/ceiling relaxation. Moderate agent owns tests/test_site_forwarders.py and tests/test_overview.py; root commits, strong independently reviews. Real hosted browser proof required; local scratch full.
