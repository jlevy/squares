---
type: is
id: is-01m2chakgrn8keadss1jcs401b
title: Retire obsolete spike probes and duplicate entry points by consumer audit
kind: task
status: open
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-4
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
  - type: blocks
    target: is-01m2cm03rtrjcg98ejb9y56jn6
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:45:05.422Z
updated_at: 2026-09-13T05:43:48.775Z
---
Phase 4 deletion only. The early consumer/assertion inventory is think-a9gt and is completed before extraction. After think-zisr migrates live sources and unique coverage, remove only obsolete spike entry points, duplicate/revision probes, and temporary devtools wrappers whose consumers have migrated. Acceptance: every deletion cites the inventory disposition and replacement coverage or no-consumer evidence; no build/CI/capture/benchmark/documented invocation depends on the old tree. Retain research records, source archives, negative experiments and their reproduction tools. Consolidate workbench-specific surviving tools under packages/workbench.

## Notes

Destination is top-level packages/workbench/ per owner. All workbench-specific tools move there; general-purpose Python research libraries can remain sqpack. Old devtools adapters are temporary and need live-consumer proof plus removal conditions. Inventory precedes extraction; removal depends on think-zisr. Retain archived sources and research provenance; recover exp-209 instrument under think-3hb7 rather than deleting its negative record.
