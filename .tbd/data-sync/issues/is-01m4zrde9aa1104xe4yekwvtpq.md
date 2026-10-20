---
type: is
id: is-01m4zrde9aa1104xe4yekwvtpq
title: Refuse deferred-worker reuse after a newer unsuccessful Deep run without a proof artifact
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zq0njqcj232mhnhc0nwfa3
hold: null
hold_until: null
created_at: 2026-10-15T12:25:56.265Z
updated_at: 2026-10-15T12:50:15.472Z
started_at: 2026-10-15T12:27:22.002Z
closed_at: 2026-10-15T12:50:15.472Z
close_reason: Retired before activation after independent source-provenance review. GitHub metadata identifies PR HEAD but cannot authenticate which merged workflow/source executed after associations disappear. Exact six-file candidate is preserved and reverse-apply verified in deferred-worker-reuse/retired-final.patch at basefc2; 88 passing focused tests do not close E1. D1/D2/E2 fixes remain prototype evidence only, with no production speed claim. All six source paths restored; no new proof framework. Separate live fast-proof issue is actively fixed under think-3d1m.
resolution: null
duplicate_of: null
---
Author disclosure in boundedreusecandidate: artifact-first discovery can find older green same-headproof even if newerDeepfailed beforepublishinganyartifact. Require bounded latest-relevant nativeDeep run lookup; newerfailed/inprogress/ambiguous -> execute normalworker. Add negativecontrols for newerfailed-noartifact and newerrunning; no service/framework/scans beyond one boundedquery. This is an unpublished candidate defect, notlive production. Root requestedauthorfix beforeindependentreview.
