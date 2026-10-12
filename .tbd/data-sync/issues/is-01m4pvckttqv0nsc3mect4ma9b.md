---
type: is
id: is-01m4pvckttqv0nsc3mect4ma9b
title: "PR #512 B6: the audit never hashes the shared kernel sources against the manifest"
kind: bug
status: closed
priority: 3
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4pvbzwtey75pwyt8pwk5pzr
hold: null
hold_until: null
created_at: 2026-10-12T01:24:45.017Z
updated_at: 2026-10-12T02:48:45.869Z
started_at: 2026-10-12T01:33:24.233Z
closed_at: 2026-10-12T02:48:45.869Z
close_reason: "Fixed in 68aef9be6/bde21d708 on PR #512; dispositions https://github.com/jlevy/squares/pull/512#issuecomment-6116848163"
resolution: null
duplicate_of: null
---
Suggestion. receipt_checks compares source_sha256 to the manifest; kernel_checks compares two manifests; no tier runs acquire_source --check for this packet. Fix: hash the five shared kernel files against the manifest in kernel_checks, or add a --records step. Review: https://github.com/jlevy/squares/pull/512#pullrequestreview-5485844215
