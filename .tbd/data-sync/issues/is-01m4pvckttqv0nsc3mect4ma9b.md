---
type: is
id: is-01m4pvckttqv0nsc3mect4ma9b
title: "PR #512 B6: the audit never hashes the shared kernel sources against the manifest"
kind: bug
status: in_progress
priority: 3
version: 2
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4pvbzwtey75pwyt8pwk5pzr
hold: null
hold_until: null
created_at: 2026-10-12T01:24:45.017Z
updated_at: 2026-10-12T01:33:24.234Z
started_at: 2026-10-12T01:33:24.233Z
---
Suggestion. receipt_checks compares source_sha256 to the manifest; kernel_checks compares two manifests; no tier runs acquire_source --check for this packet. Fix: hash the five shared kernel files against the manifest in kernel_checks, or add a --records step. Review: https://github.com/jlevy/squares/pull/512#pullrequestreview-5485844215
