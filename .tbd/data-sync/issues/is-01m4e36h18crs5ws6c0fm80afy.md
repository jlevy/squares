---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 39
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
updated_at: 2026-10-09T12:36:14.079Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

PR #474 remains draft at ab5fcb4c24fdf546d8c256c5c719eaca3ec61a91, integrated cleanly with main 6a0499ba4. All six stabilization repairs passed independent source acceptance. The completed local push tier passed all 65 selected steps in 1254.26 seconds: 15,870 normal tests passed (52 skips, one expected failure) and all nine pool tests passed; validator, tee, filter and shell exited zero. This is a named push tier, not a full 106-step gate. Hosted fast run 37929181842 passed all 93 canonical steps and its aggregate on actual immutable checkout bcd100238f171a02c2a4f57eb3b1183443aa3563, whose tree equals the published head. Actual dispatched deferred run 37929246380 is still running. Pages run 37929181857 failed the unchanged frontier loading-layout guard: dark desktop CLS 0.209 exceeds 0.1; tracked as think-9ymp. The ab5 manual preview has been rebuilt and verified, including unchanged PDF assets. Prior failed and interrupted gates remain retained without reinterpretation. Next: diagnose and repair native font reflow, qualify the final source, publish formal review dispositions, verify readiness, and close completed child beads. No GitHub merge has been requested or authorized.
