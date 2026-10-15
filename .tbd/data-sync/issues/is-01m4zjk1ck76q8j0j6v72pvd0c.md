---
type: is
id: is-01m4zjk1ck76q8j0j6v72pvd0c
title: Evaluate native validation only for the built-in witness schema
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zctkhz4k6pcptm7kjkw9pe
hold: null
hold_until: null
created_at: 2026-10-15T10:44:08.210Z
updated_at: 2026-10-15T10:44:18.254Z
started_at: 2026-10-15T10:44:18.254Z
---
Distinct bounded follow-up to rejected VE016: assess whether the native backend can be used only for the built-in Witness/v2 schema, with every explicit/custom schema continuing through the unchanged Python validator. Inspect actual default-schema constraints and fresh-read/mutation semantics before any candidate. Reject if preserving defaults requires a broad compatibility layer, schema hash binding or disabling an oracle. If viable, preregister a separate experiment and prove independent acceptance/refusal equivalence, full witness semantics and custom-schema fallback before timing. No implementation or speed claim is accepted from the failed VE016 run; all rejected evidence stays retained. Root coordinates any complete-operation timing after delivery work so it is uncontended.
