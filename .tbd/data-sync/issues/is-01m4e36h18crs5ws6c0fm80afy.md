---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 40
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
child_order_hints:
  - is-01m4fgak1gswjj6et81wfndgrm
  - is-01m4fgam2ghc99ka4m1nbjwt4c
  - is-01m4fgamsz4gh4nf00hbmt339k
  - is-01m4fqjt02p8hxaxbgq056z2mq
  - is-01m4g2jhzt6vgmd6yffk144zrr
  - is-01m4g4sxcx7y94bmrx1pqme2cb
  - is-01m4g7s24xrthh72q5ryfb5pfv
  - is-01m4g7s2kwntfe5p3g06ttgjak
  - is-01m4g7s31xde633mzd97dyg26w
  - is-01m4g81mr0zn0mv1hw933m1ntt
  - is-01m4ga4xg6bk26v9sm0g9kzkjg
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T13:44:09.924Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Final source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 is qualified against current main 6a0499ba4, with tree c65da41410e89a8dedffe93d3c1e153adb05096d. The final incremental push tier passed all 65 selected steps in 636.30 seconds (6,562 normal tests and three selected pool tests); the broader parent push receipt remains separately attributed. Hosted Fast 37934097685 passed 93 canonical steps, actual deferred dispatch 37934242931 passed 13 unique steps, and Pages 37934097749 passed, all on immutable combined checkout 1df1783aaba9acbe6f8f6299b0748a7ba32f864c with the final tree. The hosted frontier dark desktop CLS is 0.0000352 under the unchanged 0.1 guard. Independent senior, security, correctness and performance source reviews accept the bounded final changes; formal review records and A1 disposition are on PR474. Final readiness audit found no unresolved findings or unexpected check providers. The existing manual preview is rebuilt and verified without browser automation. Source, PDF edition and scientific claims are unchanged by this final font repair. Earlier failed and interrupted receipts remain retained; the slow-worker reporting-band overage (1,294 versus 1,250 seconds) remains under think-haam. Implemented and superseded children are closing; the epic, alternative intake and blocked automation follow-ups remain open. No GitHub merge is part of this task. PR: https://github.com/jlevy/squares/pull/474. Final publication status is recorded in the close reason.
