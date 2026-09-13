---
type: is
id: is-01m2ckzvnsawqg79z9ybspc3yt
title: Verify correctness repairs and strict new-source coverage before module migration
kind: task
status: open
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-phase-2
  - workbench-roadmap
dependencies:
  - type: blocks
    target: is-01m2ckzwew659djys62jdwq0fc
  - type: blocks
    target: is-01m2ckzwx4cbwvs1ewec005c2k
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T05:31:39.063Z
updated_at: 2026-09-13T06:24:56.412Z
---
Phase 2 checkpoint before broad package extraction. Record the integrated parent/leaf revision and named passing checks for R1-R5, R8 and R10; require package shell/discovery, correct evidence/strategy/benchmark/seed/snapshot admission, bounded shared resolver, full strict language floors, semantic CI and accessible stage. Historical data limitations remain explicit and are separately reconciled before release. Exact readiness comes from actual task dependencies and check receipts, not an epic status or manually written green claim.

## Notes

2026-09-13 measured strictlegacyworkbench1030errors, probes249. Fullstrict graduation and coherentTSmodulemigration must be one process, not1279JSDocpatches beforeextraction. This checkpoint stillrequires allR1/R2/R3/R5/R10/Resolve/API/semantic/accessibilityrepairs andstrict newsourcegate; it doesnotclaim legacygraduation. Removed4ylo prerequisite toavoidcycle;4ylo nowdependson finalmigrationg0lh andexplicitblocks9sdr. No newrelaxations or sourceexclusions allowed.
