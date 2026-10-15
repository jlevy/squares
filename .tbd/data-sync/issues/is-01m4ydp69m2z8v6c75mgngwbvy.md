---
type: is
id: is-01m4ydp69m2z8v6c75mgngwbvy
title: Replace recurring mutation-snapshot cap repairs with measured input boundaries
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:59:14.226Z
updated_at: 2026-10-15T01:10:22.356Z
started_at: 2026-10-15T00:00:00.966Z
---
The bounded telemetry repair in commit 6756bda8d leaves only 49,267 bytes under the unchanged 216 MiB mutation-worker source cap. Future source growth can breach it again. Use the maintained snapshot inventory and actual registered command readers to design a durable declared-input boundary or other measured selection. Preserve every mathematical input, private-copy and indexing guarantees, custody checks, checked document links, and result-registration rescue. Keep primary research and failure evidence. Do not raise the cap or add broad suffix exclusions. Record repeated failures and migration cost in the CI retrospective. PR599 stabilization remains the immediate lane.
