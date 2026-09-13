---
type: is
id: is-01m2dvhy0rjcpcz3jcjaxp3vxx
title: Seed the random start and the kernel's jiggle phases from independent streams
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m2ckzwew659djys62jdwq0fc
created_at: 2026-09-13T17:03:05.749Z
updated_at: 2026-09-13T17:03:05.749Z
---
Review 2026-09-13: createRandomPackStart (pack.ts ~376) and the kernel's jiggle phases (pack.ts ~436, kernel.ts ~395) both start seededRandom(effectiveSeed) from the same state, so the start poses and forcing draws are correlated. Any change alters fixed-seed results, so it must land with a deliberate, recorded update of the pack parity fixture (tests/fixtures/pack-parity.json) and the seed contract, not silently.
