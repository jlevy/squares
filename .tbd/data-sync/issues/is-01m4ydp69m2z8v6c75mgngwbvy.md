---
type: is
id: is-01m4ydp69m2z8v6c75mgngwbvy
title: Replace recurring mutation-snapshot cap repairs with measured input boundaries
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:59:14.226Z
updated_at: 2026-10-15T13:34:28.346Z
started_at: 2026-10-15T00:00:00.966Z
closed_at: 2026-10-15T13:34:28.346Z
close_reason: Independent source/ancestry audit against main 31eaf633 confirms the old snapshot-cap incident and proposed workflow-input/fragment rescue work are superseded by the landed PR611 checked-reader redesign and later identity-input closure. Relevant landed commits include c4a23fd80, 227c345eb, c8181dd77, 902ac9290, 848a6b1f1 and 119852eac. The exact legacy telemetry roster did not land and its saving is not claimed as deployed. No fresh headroom or three-minute performance result is asserted. Preserve the legacy receipts; do not re-port weaker snapshot code. Distinct unmutated-baseline and mutated-output assurance work remains open under think-nns5 and think-7wpx. Audit retained in ci-bead-disposition-audit-31eaf633.json.
resolution: null
duplicate_of: null
---
The bounded telemetry repair in commit 6756bda8d leaves only 49,267 bytes under the unchanged 216 MiB mutation-worker source cap. Future source growth can breach it again. Use the maintained snapshot inventory and actual registered command readers to design a durable declared-input boundary or other measured selection. Preserve every mathematical input, private-copy and indexing guarantees, custody checks, checked document links, and result-registration rescue. Keep primary research and failure evidence. Do not raise the cap or add broad suffix exclusions. Record repeated failures and migration cost in the CI retrospective. PR599 stabilization remains the immediate lane.

## Notes

Astra source analysis is complete; no implementation, scan, profile or test ran. The final counter is 226,476,702 bytes, leaving 15,714 under the unchanged 226,492,416-byte cap. The older 7cn0 audit is not a fresh inventory. Its correction records 7,760 copy operations over 7,759 unique paths. Existing deduplication already avoids 3,521,762 bytes; that saving cannot be claimed again.

First vertical slice: declare check_gate_budgets workflow inputs from its existing constants and load_walls result, then copy those exact private inputs explicitly. Make campaign link rescue handle path fragments consistently with ledger.dead_links. Prove both hidden readers work without incidental review links and remain ordinary private files in the source index. Files: check_gate_budgets.py, run_negative_controls.py, test_snapshot_link_consumers.py and test_negative_controls.py. This step promises no headroom gain.

Then audit only archive targets rescued by outgoing links in documents no registered command checks. Preserve result artifact/control/review rescue, full schema/registry joins, scientific packet/custody rosters, checked documents and conservative unknown consumers. The historical 14.4 MB estimate is a candidate pool, not a current saving. Require a fresh maintained audit, old/new unmutated baselines, identical mutation refusals, link/fragment/private-copy/symlink/fresh-input/index controls and a preregistered existing-harness comparison including snapshot preparation, indexing, total wall and portable storage. Keep this separate from frozen PR599; implementation remains outstanding.
