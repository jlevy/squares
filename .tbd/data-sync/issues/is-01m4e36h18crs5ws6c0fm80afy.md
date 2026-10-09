---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 27
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
child_order_hints:
  - is-01m4fgak1gswjj6et81wfndgrm
  - is-01m4fgam2ghc99ka4m1nbjwt4c
  - is-01m4fgamsz4gh4nf00hbmt339k
  - is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T09:10:43.863Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Frozen reviewed branch df590029 has clean Git status; data/layout87b546, export source/pind832ce8 and unchanged eight asset blobs002a8911. Actual PDFs/preview/website focused and48-step records checks pass; current PDF was opened in Preview and revealed in Finder. Four source-clear formal drafts cover101changed/89reviewed/12bulk-excluded paths, bound mergebase3213d651b. Current target main e0b02b3ab has11upstream paths; only validate.py overlaps in disjoint hunks and no atlas data/export movement, so no regeneration indicated. Complete local df gate failed one serial empty-xdist control after all64prechecks/full normal tests passed; full detailed receipt and child diagnosis under think-z0vv/sk6o. Hosted fast/deferred checks must bind the actual combined tree after publication; current full pass/PR/reviews/CI remain pending. No GitHub merge authorized. Epic remains open for further requests.
