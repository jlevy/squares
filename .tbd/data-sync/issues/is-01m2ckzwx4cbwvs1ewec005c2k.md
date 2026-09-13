---
type: is
id: is-01m2ckzwx4cbwvs1ewec005c2k
title: Implement versioned packing, catalogue and trace adapters in the package
kind: task
status: open
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-phase-3
  - workbench-roadmap
dependencies:
  - type: blocks
    target: is-01m2ckzxahng9d3m19w6bp5hfa
  - type: blocks
    target: is-01m26vyt1neawsx8w6t295mwft
  - type: blocks
    target: is-01m229amjwvykvfz1jhnjxdap9
parent_id: is-01m2chahf57z4w9tj5gehbs0td
created_at: 2026-09-13T05:31:40.323Z
updated_at: 2026-09-13T05:43:47.777Z
---
Phase 3 versioned data and IO in packages/workbench. Normalize stable IDs, radians, positive side, time/presence, effective seed/config, algorithm identity and source/guidance provenance. Validate count, finite geometry, walls and pairs/deepest overlap at the declared tolerance before retaining numerical evidence; carry actual validator provenance. Adapt legacy degree arrays, shared schema, sqpack.render and Motion Lab invariants. Package-local assembler emits versioned catalogue/palette from general sqpack APIs; generic run/replay does not require a catalogue or Python. Acceptance: supported round trips and explicit failures for unknown versions, malformed geometry, unsupported capabilities and evidence inflation.
