---
type: is
id: is-01m4v4ees39f9wsjv8b1bvj9w2
title: "Census tool: --stale and --reconcile repair the occurrence manifest after merges"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
created_at: 2026-10-13T17:20:00.288Z
updated_at: 2026-10-13T17:20:08.579Z
closed_at: 2026-10-13T17:20:08.579Z
close_reason: "Shipped in PR #578; see the bead description for commits."
resolution: null
duplicate_of: null
---
Merging main left reviewed credit spans stale and new spans unreviewed. contributor_census --stale lists them; --reconcile rewrites occurrences.yaml, joining only by a reviewed label or a sourced record spelling. Shipped in PR #578 (03afb55f4, a27944d5c).
