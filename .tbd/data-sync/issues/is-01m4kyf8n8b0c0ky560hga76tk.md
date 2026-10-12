---
type: is
id: is-01m4kyf8n8b0c0ky560hga76tk
title: Re-enable shared-CI browser timing enforcement with controlled baseline evidence
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
assignee: jlevy
delegate: null
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-10T22:20:54.298Z
updated_at: 2026-10-11T01:59:46.135Z
started_at: 2026-10-11T01:58:53.014Z
---
Scoped debt for PR #462 B1: longest native load task remained 300ms; LCP 4000ms and total blocking 600ms remain unchanged. Shared-runner timing is advisory only, while structural rendering guards remain blocking. Re-enable enforcement in ordinary CI after a dedicated controlled runner or repeated same-run fixed-baseline comparison defines a regression/noise envelope greater than measured variance; record runner/browser/protocol and baseline/noise evidence. Owner jlevy; no threshold increase or blind reruns.

## Notes

2026-10-11 polynomial stack refresh: the bead-tree gate found this open
timing-enforcement debt under the closed PR462 review bead think-mvh7. Reparented it to
the active CI process owner think-ht59 so the remaining work stays visible after that PR
merged. Scope, assignee jlevy and original evidence requirements are unchanged.
The polynomial producer now uses the same report-only timing receipt as the upstream
producers; this hierarchy repair supplies no controlled-run baseline and does not
complete timing enforcement.
The task remains open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
