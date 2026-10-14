---
type: is
id: is-01m4vzkndywx39wgv6e7cgjgp5
title: Make infographic cuts resumable and enforce PDF edition ownership
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
created_at: 2026-10-14T01:14:42.489Z
updated_at: 2026-10-14T01:14:42.489Z
---
Precommit review A2/A3: update_composites replaces SVG before PNG/PDF generation, so an interrupted cut cannot retry its chosen edition; PDF updates and standalone PDF export bypass the same-version ownership guard. Stage and verify the complete family before promotion, preserve old outputs on generation failure, and enforce owning editions for all exports. Add producer-failure retry and same-version PDF refusal tests.
