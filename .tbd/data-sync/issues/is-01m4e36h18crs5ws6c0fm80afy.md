---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 30
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
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T10:15:38.745Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Final clean frozen source is 1a7e4744c13dc6fcf7e911058dfa829ac03d2ff6. Product science/layout87b546, release pin and eight exports002a8911 remain unchanged; current PDFs, web/preview, geometry and records checks pass. Sixth narrow test stabilization is independently accepted, focused/static checks green. The previous98 full run failed a native initialization-phase control after all normal tests passed; the current complete push run has 64 prechecks passed with behavioral/overall results pending. Four final-head formal drafts and PR description are being rebound in parallel, with honest prior failures and review limitations. Current main533 compatibility was clear; hosted receipts must validate the fresh actual combined tree before publication readiness. PR, hosted fast/deferred checks and formal review publication remain pending. Keep epic open; no GitHub merge authorized.
