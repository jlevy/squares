---
type: is
id: is-01m4wvthr2sdv6kr06cz7z38e6
title: Build versioned infographic candidates in hosted CI when local scratch is unavailable
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
hold: null
hold_until: null
created_at: 2026-10-14T09:27:48.214Z
updated_at: 2026-10-14T09:27:59.315Z
started_at: 2026-10-14T09:27:59.314Z
---
Add an optional dispatch-only candidate export job to existing Pages workflow. Reuse retained atomic full-pair generator/checker, pinned toolchain, read-only permissions and isolated artifact; no deployment or commits. Preserve ordinary publication/gate behavior. Validate source SHA and exact8export allowlist before importing into PR590; normalPages regenerates selected explainer. Local staging paused at32MiB externalfree.
