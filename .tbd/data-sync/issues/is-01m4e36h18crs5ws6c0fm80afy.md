---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 37
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
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T11:53:44.568Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

PR474 published draft at490dab908a after normal local mainbead35 merge,338affected tests and staticfloor passed. Local full490 completed FAILED:64of65steps pass,15869normal tests pass plus52skips1xfail and sole suite-file costguard failure; pool lane not executed. Hosted fast37923898828 on actualC c229806b/tree2c7368 failed3of93steps: sparse rigidity sources, stale family census, and suitecostguard. Pages37923899026 passes. Actual manually dispatched deep37924058196 PASSES all13deferred logical steps on that C,182slow and61exhaustive tests. Three observed failures have tracked fixes d4m3,17si,tkz0; reaching contact-shade after family repair exposed only n211 regularizable diagnostic float drift, trackedpp32, under bounded diagnosis. Product layout,geometry,pin and exports unchanged. PR is draft, not merge-ready, no GitHub merge authorized. All failed/incomplete prior gates remain truthful in retained evidence. Next: final repair source acceptance, normal gate, fast and actual deferred hosted qualification, formal review/dispositions, readiness and bead closeout.
