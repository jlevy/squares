---
type: is
id: is-01m4s66pg12k212yjqbee5jp6n
title: "Documentation layout, conflict-free part: docs/project kind directories, lowercase component guides, layout guard"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-11-documentation-organization.md
delegate: claude-code@vm
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-12T23:12:14.337Z
updated_at: 2026-10-13T05:28:31.638Z
started_at: 2026-10-12T23:12:18.896Z
closed_at: 2026-10-13T05:28:31.638Z
close_reason: Merged in https://github.com/jlevy/squares/pull/576; deferred slices continue in think-xz7z.
resolution: null
duplicate_of: null
---
Implements the parts of PR #510's plan that no open pull request touches: slice 1 without site-urls.md, slice 6 without the sqverify_fast guides and the templates, and a narrowed layout check inside check_documentation. Slices 2-5 and the register-cited renames are deferred until the open-PR queue no longer edits SYNOPSIS.md, development.md, the frontier views and evidence.yaml.

## Notes

PR https://github.com/jlevy/squares/pull/576 opened at c0e02d536 (main merged at e96e9ea95); also maps paper-design.md and adds slice 0's touches and main-link guards.
