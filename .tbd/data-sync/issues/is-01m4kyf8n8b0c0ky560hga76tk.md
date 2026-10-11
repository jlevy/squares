---
type: is
id: is-01m4kyf8n8b0c0ky560hga76tk
title: Re-enable shared-CI browser timing enforcement with controlled baseline evidence
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
assignee: jlevy
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ky07tt9a0s334a3cvzyfb3
hold: null
hold_until: null
created_at: 2026-10-10T22:20:54.298Z
updated_at: 2026-10-11T01:58:53.016Z
started_at: 2026-10-11T01:58:53.014Z
---
Scoped debt for PR #462 B1: longest native load task remained 300ms; LCP 4000ms and total blocking 600ms remain unchanged. Shared-runner timing is advisory only, while structural rendering guards remain blocking. Re-enable enforcement in ordinary CI after a dedicated controlled runner or repeated same-run fixed-baseline comparison defines a regression/noise envelope greater than measured variance; record runner/browser/protocol and baseline/noise evidence. Owner jlevy; no threshold increase or blind reruns.
