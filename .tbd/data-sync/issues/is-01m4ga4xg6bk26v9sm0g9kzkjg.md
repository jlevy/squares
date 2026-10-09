---
type: is
id: is-01m4ga4xg6bk26v9sm0g9kzkjg
title: Stabilize frontier loading layout in the publication check
kind: bug
status: in_progress
priority: 1
version: 3
delegate: codex-atlas-root
labels: []
dependencies: []
parent_id: is-01m4e36h18crs5ws6c0fm80afy
hold: null
hold_until: null
created_at: 2026-10-09T12:28:00.380Z
updated_at: 2026-10-09T12:51:13.091Z
started_at: 2026-10-09T12:28:17.593Z
---
PR474 finalab5/actualC bcd10023 passes all93 hostedfast steps, but Pages overview job113815599600 fails frontier.html at1280pxdark CLS0.209 above the unchanged0.1 guard. Establish actual layout-shift source, compare source/base behavior, make bounded rendering correction if needed, and qualify maintained production metrics on the actual final tree. Preserve metrics thresholds, observer semantics, page coverage and asset/source custody.

## Notes

The published ab5 source has now passed all 106 ordinary hosted validation steps on immutable checkout bcd10023 (93 fast plus 13 actual dispatched deferred steps); Pages alone remains failed. Native metrics locate one dark desktop shift at 446.6 ms during font loading. A controlled delay of the existing PT Serif 400 italic face reproduces the exact hosted paragraph-fragment transition from y=591.359375 to y=564.359375, a 27 px rewrap. Local CLS is 0.06019 versus hosted 0.20859, so the full hosted score is not reproduced or explained away. The narrow repair adds that existing face to early preloads, with a behavioral asset contract and matching documentation. The protocol-aware credential bootstrap, observer, 0.1 threshold, page coverage, no-JS behavior and reader preferences stay intact. Independent correctness and performance reviews are underway. Root owns final qualification and publication; the bead stays open until the actual final Pages gate passes.
