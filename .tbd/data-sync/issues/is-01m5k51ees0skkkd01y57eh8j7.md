---
type: is
id: is-01m5k51ees0skkkd01y57eh8j7
title: Migrate overview assertions to dedicated Frontier and complete Atlas
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-frontier-tests
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T01:12:08.906Z
updated_at: 2026-10-23T01:18:57.731Z
started_at: 2026-10-23T01:12:20.140Z
---
Own only Frontier/Atlas stale expectations in test_overview.py; preserve route/content/navigation behavior and run focused tests alongside final CI.

## Notes

Own test_overview.py Frontier/Atlas migration and one canonical broad-record assertion in test_result_overview.py. Focused overview17passed with remaining canonical-ref failure from source loaded before worker fix; serif-introduction1passed35.32s. Atlas tile extractor now accepts hidden or expanded rest state. Ruff clean/scoped basedpyright0errors0warnings. Actual runtime gap found: result_overview.check_links fragments map1210 lacks frontier.html#n-N, causing T124 compaction and every-result fixture to raise missing-target SystemExit. Reported to source owner Frontier worker and root; no runtime edits by Sol. Await source repair then rerun exact canonical/compaction tests and checkpoint.
