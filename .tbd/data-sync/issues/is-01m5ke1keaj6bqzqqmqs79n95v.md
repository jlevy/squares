---
type: is
id: is-01m5ke1keaj6bqzqqmqs79n95v
title: Audit PR737 main Pages deployment latency
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: sol-upstream-final
labels: []
dependencies: []
parent_id: is-01m5kcfhfdmgfb03gn3drg43rc
hold: null
hold_until: null
created_at: 2026-10-23T03:49:31.209Z
updated_at: 2026-10-23T03:53:48.404Z
started_at: 2026-10-23T03:49:37.034Z
closed_at: 2026-10-23T03:53:48.392Z
close_reason: Audited official main Pages run 39896243132 versus green PR run 39895010919. Main merge→public deploy ~6m45; overview critical path 4m26 (36s setup, 2m34 two render parity, 1m06 card parity/head checks), publish 1m12, deploy 10s; live verifier setup 50s + audit 1m41 ended red at 9m16 due five stale checker assertions. PR overview 4m29 with same 2m36 two renders and 1m05 card/head checks. Rebuild on main is tied to immutable merge SHA and published citations; simple artifact skip would break provenance. Findings reported to coordinator; no build or source change for latency audit.
resolution: null
duplicate_of: null
---
Measure actual PR versus main Pages workflow critical path, queue/setup/build/publish/deploy/live verification, and identify duplicated work versus required publication. Read-only audit with run/job evidence; no builds or source edits.
