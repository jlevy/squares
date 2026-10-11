---
type: is
id: is-01m4macaj7jmrrd1vqnxk74d40
title: Merge upstream site layout into contributor profiles and verify combined publication
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
child_order_hints:
  - is-01m4mafs7sfpch465k5p9fbg0f
hold: null
hold_until: null
created_at: 2026-10-11T01:49:00.870Z
updated_at: 2026-10-11T02:28:17.873Z
started_at: 2026-10-11T01:49:31.026Z
---
Follow merge-upstream shortcut: fetch and stack preflight, reconcile main6038af33c site layout with contributor profiles, preserve shared overlays and reviewed credits, validate, push PR490 and await CI.

## Notes

Implementation committed at 85e0ac66f, merging main6038af33c. Focused suites and full preview pass. Local push gate failed: reachable behavioral tests hit900s, partial output includes F without final traceback; diagnose rather than claiming timing-only. User requests WIP PR and agent handoff, so leave integration acceptance open. Next route work think-0v2c remains unstarted.
