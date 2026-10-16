---
type: is
id: is-01m51mrqfyjzg911fevvr9aq6h
title: Diagnose local validation startup delays and stale gate marker
kind: bug
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: null
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-16T06:00:40.694Z
updated_at: 2026-10-16T06:11:06.189Z
started_at: 2026-10-16T06:03:55.149Z
---
Two local pre-push runs at implementation 77fe330dd passed all 68 prerequisites but timed out after 900 seconds of behavioral tests. A verified stale empty gate marker was removed; ten-worker execution was restored, but the retry also timed out. Serial reproduction completed: six of eight selectors passed unchanged. Remaining failures are a nested collection exceeding 30 seconds and a static paragraph longest-task control measuring 402 ms against 300 ms. Three signal/readiness tests, Atlas navigation, representative result columns and the suite-plugin probe passed. Original first-run F833/F1284 identities remain unknown. Investigate marker ownership/recovery and host contention; no product regression or single cause has been established. No source or timeout changes were made. All 31 standard hosted checks pass on final documentation head e1f921bf0. Receipts are under external scratch contributor-profiles-01a126ff/tmp, including the two push logs, profiles-final-merge-artifacts, and serial-process-repro and serial-browser-repro logs.
