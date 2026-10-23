---
type: is
id: is-01m5k51ees0skkkd01y57eh8j7
title: Migrate overview assertions to dedicated Frontier and complete Atlas
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-frontier-tests
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T01:12:08.906Z
updated_at: 2026-10-23T01:22:30.340Z
started_at: 2026-10-23T01:12:20.140Z
---
Own only Frontier/Atlas stale expectations in test_overview.py; preserve route/content/navigation behavior and run focused tests alongside final CI.

## Notes

Source-ready tests staged for coordinator combined commit. Frontier/Atlas focused overview17passed; serif introduction1passed35.32s. Canonical five real-link/compaction cases passed27.07s after worker validator fix; complete result_overview module66passed101.05s. Ruff/format/diff clean; scoped basedpyright0errors0warnings. Runtime validator missing Frontier anchors found/reported and repaired by Frontier owner; no runtime edits by Sol. Test changes preserve complete result/row-link and XML/compaction assertions, remove intentionally deleted history prose checks, separate Atlas graphics from Frontier table, accept full324 visibility state.
