---
type: is
id: is-01m0v0s3c8y81w7sfrbvhehz8c
title: "PR 24 transition T2a: replace lost negctl receipt"
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - process
dependencies: []
parent_id: is-01m0v0ga616pdtr2n71pktm229
created_at: 2026-08-24T23:13:07.463Z
updated_at: 2026-08-24T23:13:07.463Z
---
The parallel focused-check wrapper returned the long negative-control command without a terminal exit/output receipt and did not retain its session id for polling. Discard that run, record the incident as a D-202 recurrence, rerun once through a direct receipt-preserving command, and keep think-b3bm as the systemic runbook owner.
