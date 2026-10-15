---
type: is
id: is-01m4zrde9aa1104xe4yekwvtpq
title: Refuse deferred-worker reuse after a newer unsuccessful Deep run without a proof artifact
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zq0njqcj232mhnhc0nwfa3
hold: null
hold_until: null
created_at: 2026-10-15T12:25:56.265Z
updated_at: 2026-10-15T12:27:22.003Z
started_at: 2026-10-15T12:27:22.002Z
---
Author disclosure in boundedreusecandidate: artifact-first discovery can find older green same-headproof even if newerDeepfailed beforepublishinganyartifact. Require bounded latest-relevant nativeDeep run lookup; newerfailed/inprogress/ambiguous -> execute normalworker. Add negativecontrols for newerfailed-noartifact and newerrunning; no service/framework/scans beyond one boundedquery. This is an unpublished candidate defect, notlive production. Root requestedauthorfix beforeindependentreview.
