---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 22
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
child_order_hints:
  - is-01m4fgak1gswjj6et81wfndgrm
  - is-01m4fgam2ghc99ka4m1nbjwt4c
  - is-01m4fgamsz4gh4nf00hbmt339k
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T05:10:47.931Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Continuation after new user layout revision: 818c4c372 is predecessor evidence, not final. Its full required --push against base3213 completed naturally in1350.65s: all64 pre-test steps passed; normal reachable suite14,079passed,17failed,54skipped,1xfail in1124.17s; no pool-heavy/final pass claimed. Failures tracked as think-221w(date/stamp),think-mk5k(web tokens/frontier),think-4emj(consumer declarations plus harness diagnosis). Ten strong-lane failures now pass under NORMAL temp retention with unchanged deadlines; only two explicit consumer declarations changed. Removed our nondefault retention-failed override from future runs; no custody/timeout guards relaxed. Latest user features are think-t6n5(PDF18complete right-aligned rows,360pitch,upper-left/left text) and think-avy3(web complete right-aligned rows/readable pan/more vertical space), claimed/synced and implemented in disjoint lanes. Shared known_best descriptor and inherited EXPLAINER_REVISED date corrected by root; docs updated. Keep all uniform body typography, grid half-width gap and markings, geometry/data pin9c and100Grid. Pending focused checks, maintained exports/actualPDF/preview, current full --push, PR/hosted/full checkpoint, updated review publication. No PR or merge-ready verdict yet; no GitHub merge authorized; epic stays open.
