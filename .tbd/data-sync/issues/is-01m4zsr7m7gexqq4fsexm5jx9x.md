---
type: is
id: is-01m4zsr7m7gexqq4fsexm5jx9x
title: "F1: remove automatic fast-check reuse based on unauthenticated artifact names"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T12:49:18.470Z
updated_at: 2026-10-15T12:49:26.606Z
started_at: 2026-10-15T12:49:26.605Z
---
Independent review found the same live source-authentication gap in baseline fc2ceae79: verified_merge_tree.py accepts a self-named tree artifact with successful native run/job names, without authenticating the executed PR merge source. Deferred work stays cold, but allowlisted fast checks can be skipped on main. Remove the automatic reuse path and its dead producer/verifier plumbing rather than introducing a provenance framework. Preserve every fast/scientific check, budgets and normal PR selection. Update the shared guide and meaningful workflow/selection controls. More main fast work may run, but no new proof API overhead or trusting self-declared artifact names. The retired deferred candidate and review evidence are preserved separately.
