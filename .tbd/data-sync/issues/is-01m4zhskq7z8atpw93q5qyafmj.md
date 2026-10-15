---
type: is
id: is-01m4zhskq7z8atpw93q5qyafmj
title: "Q1: cover regenerated threshold claims in release-cut contracts"
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zh3apr6q86jmjggvd08bhr
hold: null
hold_until: null
created_at: 2026-10-15T10:30:15.014Z
updated_at: 2026-10-15T10:30:33.709Z
started_at: 2026-10-15T10:30:33.708Z
---
Senior review Q1 (Low): site cuts regenerate T-025/T-026, but component-owned selection currently includes only test_verify_claim.py; independent threshold embedding/refusal controls are in test_verify_threshold_claim.py. Add the owning threshold module to site selection (and existing lower-bounds claim selection consistently), prove real collected identities and run the quick contracts. Preserve exhaustive markers and full checkpoint obligations.
