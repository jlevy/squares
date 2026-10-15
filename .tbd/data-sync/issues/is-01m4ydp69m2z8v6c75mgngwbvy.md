---
type: is
id: is-01m4ydp69m2z8v6c75mgngwbvy
title: Replace recurring mutation-snapshot cap repairs with measured input boundaries
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:59:14.226Z
updated_at: 2026-10-15T01:17:31.012Z
started_at: 2026-10-15T00:00:00.966Z
---
The bounded telemetry repair in commit 6756bda8d leaves only 49,267 bytes under the unchanged 216 MiB mutation-worker source cap. Future source growth can breach it again. Use the maintained snapshot inventory and actual registered command readers to design a durable declared-input boundary or other measured selection. Preserve every mathematical input, private-copy and indexing guarantees, custody checks, checked document links, and result-registration rescue. Keep primary research and failure evidence. Do not raise the cap or add broad suffix exclusions. Record repeated failures and migration cost in the CI retrospective. PR599 stabilization remains the immediate lane.

## Notes

Astra read-only source analysis is complete; no implementation, scan, profile or test ran. Final counter226476702 leaves15714 bytes under unchanged226492416 cap. The older7cn0 inventory is not a fresh final inventory; its correction is7760 copy operations/7759 unique paths. Existing named-copy deduplication already avoids3521762 bytes and cannot be claimed again.

First vertical slice: declare check_gate_budgets workflow inputs from its existing constants/load_walls result and rescue them explicitly; make campaign link rescue handle path fragments consistently with ledger.dead_links. Prove both hidden readers work without incidental review links, use private ordinary copies and remain in the private index. Proposed files: check_gate_budgets.py, run_negative_controls.py, test_snapshot_link_consumers.py and test_negative_controls.py. This first step promises no byte saving.

Then audit only archive targets rescued by outgoing links in documents no registered command checks. Preserve structural result-artifact/control/review rescue, full schema/registry joins, scientific packet/custody rosters, checked documents and conservative unknown consumers. Historical14.4MB is a candidate pool, not measured current headroom. Require fresh maintained --audit-snapshot receipts, old/new unmutated baselines, identical mutation refusals, fragment/missing/newly-registered/private-copy/symlink/fresh-input/index controls and a preregistered existing-harness --timings comparison including snapshot/index/whole wall/storage. Keep separate from the frozen PR599 branch; its stabilization remains the immediate lane.
