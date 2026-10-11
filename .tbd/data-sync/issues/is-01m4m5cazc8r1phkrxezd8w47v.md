---
type: is
id: is-01m4m5cazc8r1phkrxezd8w47v
title: Repair stale homepage and case-page test contracts from PR462 shard A
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4m588mffw9ac4ssy5qa9hhd
hold: null
hold_until: null
created_at: 2026-10-11T00:21:38.411Z
updated_at: 2026-10-11T00:26:46.995Z
started_at: 2026-10-11T00:21:51.877Z
closed_at: 2026-10-11T00:26:46.993Z
close_reason: Staged only owned test_overview.py and test_case_pages.py. All21 formerly failed nodes pass in25.52s; strengthenedAboutnode passes7.16s; Ruffcheck/format and diffcheck clean. Requestedstrokeassertion added; root owns helper implementation and finalverification.
resolution: null
duplicate_of: null
---
Own only test_overview.py and test_case_pages.py. Reconcile 21 CI assertions with intended layout preserving independent math/citation/filter coverage.
