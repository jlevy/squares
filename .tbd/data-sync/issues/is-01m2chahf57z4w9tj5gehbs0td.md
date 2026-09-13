---
type: is
id: is-01m2chahf57z4w9tj5gehbs0td
title: Consolidate the workbench into a standalone package after cleanup
kind: epic
status: open
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
  - type: blocks
    target: is-01m2chakgrn8keadss1jcs401b
parent_id: is-01m28p7h39vcykq99dgjmvwv98
child_order_hints:
  - is-01m28p88qyq83eek30pja3np54
  - is-01m229an1fw0az9jgk0wcbg8c4
created_at: 2026-09-13T04:45:03.321Z
updated_at: 2026-09-13T05:09:53.042Z
---
Owner-selected follow-on phase at TOP-LEVEL packages/workbench/. All workbench-specific app, geometry/simulation, animation, view, IO, probes/tests, build, benchmark and capture tooling live in this one package. Package-local Python adapters may call general-purpose sqpack libraries; no second application tree in packing/devtools or spikes. Temporary compatibility wrappers need named consumers/removal conditions. Integrate current parent and repair records/evidence/strategy/benchmark/seed first; complete strict tbd Python and TS/JS floor with full source coverage and behavioral CI. Extract a pure browser/Node run API and deterministic animation consumers, versioned catalogue inputs, standalone scripts and static Pages output. Update layout docs, Python discovery, browser configs, hooks/gate selection and Pages filters for the root package. Search remains deferred until package and obsolete-consumer cleanup complete.

## Notes

All newly introduced workbench-specific files during the preceding repair phases also start in top-level packages/workbench with immediate lint/type/test discovery. Existing live files may receive narrow in-place repairs. The later package phase completes consolidation; it does not permit new scattered devtools or spike modules in the meantime.
