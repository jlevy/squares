---
type: is
id: is-01m4ga4xg6bk26v9sm0g9kzkjg
title: Stabilize frontier loading layout in the publication check
kind: bug
status: closed
priority: 1
version: 5
delegate: codex-atlas-root
labels: []
dependencies: []
parent_id: is-01m4e36h18crs5ws6c0fm80afy
hold: null
hold_until: null
created_at: 2026-10-09T12:28:00.380Z
updated_at: 2026-10-09T13:44:10.726Z
started_at: 2026-10-09T12:28:17.593Z
closed_at: 2026-10-09T13:44:10.726Z
close_reason: Implemented, independently reviewed and qualified for PR474 source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 against main 6a0499ba4; combined tree c65da41410e89a8dedffe93d3c1e153adb05096d. Local named push 65/65 and hosted 93 fast + 13 actual deferred (106) plus Pages passed; final readiness receipts recorded.
resolution: null
duplicate_of: null
---
PR474 finalab5/actualC bcd10023 passes all93 hostedfast steps, but Pages overview job113815599600 fails frontier.html at1280pxdark CLS0.209 above the unchanged0.1 guard. Establish actual layout-shift source, compare source/base behavior, make bounded rendering correction if needed, and qualify maintained production metrics on the actual final tree. Preserve metrics thresholds, observer semantics, page coverage and asset/source custody.

## Notes

Completed in commit 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92: preload the existing PT Serif 400 italic font earlier, with root/nested asset contract coverage and matching documentation. A controlled delay reproduced the exact 27-pixel paragraph rewrap; local CLS 0.06019 did not reproduce the whole previous hosted score of 0.20859, which remains retained. All four independent source reviewers accepted the three-file delta. Focused 34 tests, lint, types and math-span checks pass; the final local incremental push tier passes 65/65. Actual final Pages 37934097749 passes on immutable combined checkout 1df1783aaba9acbe6f8f6299b0748a7ba32f864c with desktop dark CLS 0.0000352 under the unchanged 0.1 threshold. Bootstrap, credentials, observer, page coverage, no-JS behavior, font bytes, reader preferences and settled typography remain intact. The maintained final preview passes byte and markup verification. Final publication is in PR474 / think-142l.
