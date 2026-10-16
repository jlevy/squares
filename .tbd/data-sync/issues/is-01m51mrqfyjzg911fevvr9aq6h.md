---
type: is
id: is-01m51mrqfyjzg911fevvr9aq6h
title: Diagnose local validation startup delays and stale gate marker
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
created_at: 2026-10-16T06:00:40.694Z
updated_at: 2026-10-16T06:00:40.694Z
---
During the final profiles integration at 77fe330dd, --push passed all 68 prerequisites but its serial behavioral selection timed out at 900 seconds. An empty .gate-running directory dated October 14 remained with no active validator in this worktree; it was removed after inspecting active validators and their working directories. A diagnostic retry used the intended ten-worker exclusive phase but also timed out at 900 seconds, recording short nested-collection and worker-readiness timeouts plus browser Page.goto and timing-control failures. All 31 standard hosted checks passed on the same source. Investigate stale-marker ownership/recovery and host contention before changing any timeout or test contract; the local failures have not established a product regression. Current receipts live in external scratch contributor-profiles-01a126ff/tmp/profiles-final-merge-artifacts and the two profiles-final-merge-push logs. Serial focused reproduction is in progress; record its results and any remaining uncertainty.
