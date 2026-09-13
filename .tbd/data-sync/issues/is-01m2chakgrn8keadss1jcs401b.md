---
type: is
id: is-01m2chakgrn8keadss1jcs401b
title: Retire obsolete spike probes and duplicate entry points by consumer audit
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:45:05.422Z
updated_at: 2026-09-13T05:02:01.604Z
---
Inventory active product sources, unique semantic tests, superseded revision probes, standalone research instruments and retained records. Remove spurious or duplicate code only after proving no build/gate/doc/capture/benchmark consumers and replacing any unique assertions. Keep archived source, negative experiments, summaries and reproduction provenance. Move live sources into standalone workbench package; keep Python CLI wrappers thin and grouped. Avoid moving all spike files wholesale into flat devtools.

## Notes

Destination is top-level packages/workbench/ per owner. All workbench-specific tools move there; general-purpose Python research libraries can remain sqpack. Old devtools adapters are temporary and need live-consumer proof plus removal conditions. Inventory precedes extraction; removal depends on think-zisr. Retain archived sources and research provenance; recover exp-209 instrument under think-3hb7 rather than deleting its negative record.
